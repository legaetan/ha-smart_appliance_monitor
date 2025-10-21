# Testing AI Analysis Features

This document provides step-by-step instructions for testing the AI analysis features of Smart Appliance Monitor.

## Prerequisites

1. **Home Assistant AI Integration**: You need an AI Task entity configured in Home Assistant
   - Options: OpenAI, Anthropic Claude, Google Generative AI, Ollama (local), etc.
   - Configure via Settings → Devices & Services → Add Integration → OpenAI Conversation (or other AI provider)

2. **Smart Appliance Monitor**: At least one appliance configured with:
   - Anomaly detection enabled (to have cycle history)
   - At least 5-10 completed cycles for meaningful analysis

3. **API Key**: If using cloud AI (OpenAI, Claude), ensure you have a valid API key configured

## Configuration Steps

### 1. Configure AI Task Entity

First, create an AI Task entity in Home Assistant:

```yaml
# configuration.yaml
ai_task:
  - name: "OpenAI AI Task"
    api_key: !secret openai_api_key
    model: "gpt-4o"  # or gpt-4-turbo, gpt-3.5-turbo
```

Or use the UI:
- Go to Settings → Devices & Services
- Add Integration → OpenAI Conversation
- Enter your API key
- The AI Task entity will be created automatically (e.g., `ai_task.openai_ai_task`)

### 2. Configure Global AI Settings

Use the new `configure_ai` service to set up AI analysis:

**Via Developer Tools → Services:**

```yaml
service: smart_appliance_monitor.configure_ai
data:
  ai_task_entity: ai_task.openai_ai_task
  enable_ai_analysis: true
  ai_analysis_trigger: manual  # Start with manual for testing
```

**Expected Result**: You should see a persistent notification confirming the configuration was updated.

### 3. Enable AI Analysis Switch for an Appliance

Navigate to your appliance's entity list and turn on the AI Analysis switch:

- Entity: `switch.<appliance_name>_ai_analysis`
- Turn it ON

**Note**: The switch will only be available if `ai_task_entity` is configured globally.

## Testing Scenarios

### Test 1: Manual Cycle Analysis

**Prerequisites**: The appliance has completed at least 3-5 cycles with anomaly detection enabled.

**Steps**:

1. Open Developer Tools → Services
2. Select `smart_appliance_monitor.analyze_cycles`
3. Fill in the parameters:
   ```yaml
   service: smart_appliance_monitor.analyze_cycles
   data:
     entity_id: sensor.washing_machine_state  # Replace with your appliance
     analysis_type: all
     cycle_count: 10
     save_export: false
   ```
4. Click "Call Service"

**Expected Results**:

1. Service executes successfully (check logs for any errors)
2. After 10-30 seconds, check the AI analysis sensor:
   - Entity: `sensor.<appliance_name>_ai_analysis`
   - State should be: `optimized`, `normal`, or `needs_improvement`
   - Attributes should contain:
     - `last_analysis_date`
     - `summary`
     - `recommendations` (list)
     - `energy_savings_kwh`
     - `energy_savings_eur`
     - `optimal_hours`
     - `full_analysis`
3. If notifications are enabled, you should receive a notification with the analysis summary

**Troubleshooting**:

- If no result appears, check Home Assistant logs for errors
- Verify the AI Task entity is responding: try calling it directly via Developer Tools
- Ensure the appliance has cycle history (check `sensor.<appliance>_anomaly_score` attributes)

### Test 2: Automatic Analysis After Cycle

**Prerequisites**: Test 1 completed successfully.

**Steps**:

1. Update AI configuration to auto-trigger:
   ```yaml
   service: smart_appliance_monitor.configure_ai
   data:
     ai_analysis_trigger: auto_cycle_end
   ```
2. Start and complete a cycle on the appliance
3. Wait for the cycle to finish

**Expected Results**:

1. When the cycle finishes, you receive the "Cycle Finished" notification as usual
2. Within 1-2 minutes, the AI analysis should be triggered automatically
3. The `sensor.<appliance>_ai_analysis` should update with new analysis
4. You should receive a second notification with AI analysis results

**Note**: Check logs for messages like:
```
Auto-triggering AI analysis for '<appliance_name>' after cycle finished
AI analysis completed for '<appliance_name>': status=<status>
```

### Test 3: Energy Dashboard Analysis

**Prerequisites**: Multiple appliances configured in Smart Appliance Monitor.

**Steps**:

1. Open Developer Tools → Services
2. Select `smart_appliance_monitor.analyze_energy_dashboard`
3. Fill in the parameters:
   ```yaml
   service: smart_appliance_monitor.analyze_energy_dashboard
   data:
     period: today
     compare_previous: true
   ```
4. Click "Call Service"

**Expected Results**:

1. Service executes successfully
2. Check logs for the efficiency score
3. An event `smart_appliance_monitor_energy_dashboard_analysis_completed` is fired
4. The analysis includes:
   - Global efficiency score (0-100)
   - Top consumers
   - Optimization opportunities
   - Estimated monthly savings

**Advanced**: Create a sensor to capture the dashboard analysis results:

```yaml
# configuration.yaml
template:
  - trigger:
      - platform: event
        event_type: smart_appliance_monitor_energy_dashboard_analysis_completed
    sensor:
      - name: "SAM Energy Efficiency Score"
        state: "{{ trigger.event.data.efficiency_score }}"
        attributes:
          trend: "{{ trigger.event.data.consumption_trend }}"
          period: "{{ trigger.event.data.period }}"
```

### Test 4: Pattern Analysis

Test pattern detection by analyzing usage at different times:

**Steps**:

1. Run analysis with only pattern type:
   ```yaml
   service: smart_appliance_monitor.analyze_cycles
   data:
     entity_id: sensor.washing_machine_state
     analysis_type: pattern
     cycle_count: 15
   ```

**Expected Analysis Content**:

- Most common usage hours
- Most common days of the week
- Recommendations for off-peak usage
- Potential cost savings by shifting to off-peak hours

### Test 5: Comparative Analysis

Test anomaly detection and trend identification:

**Steps**:

1. Run analysis with only comparative type:
   ```yaml
   service: smart_appliance_monitor.analyze_cycles
   data:
     entity_id: sensor.washing_machine_state
     analysis_type: comparative
     cycle_count: 20
   ```

**Expected Analysis Content**:

- Comparison of current cycle vs average
- Detection of unusual energy consumption
- Trends (increasing/stable/decreasing consumption)
- Alerts for potential maintenance needs

### Test 6: Export Data for Manual Review

Export cycle data to review what the AI receives:

**Steps**:

1. Run analysis with export enabled:
   ```yaml
   service: smart_appliance_monitor.analyze_cycles
   data:
     entity_id: sensor.washing_machine_state
     analysis_type: all
     cycle_count: 10
     export_format: both
     save_export: true
   ```

**Expected Results**:

1. Two files created in `/config/`:
   - `sam_export_<appliance_name>_cycles.json` - Full structured data
   - `sam_export_<appliance_name>_cycles.csv` - Tabular cycle history

2. Review these files to understand what data the AI receives

## Common Issues and Solutions

### Issue 1: "No AI Task entity configured"

**Solution**: Run the `configure_ai` service first to set the `ai_task_entity`.

### Issue 2: "Cannot trigger AI analysis: no AI Task entity configured"

**Cause**: The coordinator hasn't loaded the global config yet.

**Solution**:
1. Restart Home Assistant
2. Or reload the integration via Settings → Devices & Services

### Issue 3: AI analysis returns empty or generic results

**Cause**: Not enough cycle history.

**Solution**:
1. Ensure anomaly detection is enabled for the appliance
2. Wait for at least 5-10 cycles to complete
3. Check the `cycle_history` attribute in the exported data

### Issue 4: AI Task service call times out

**Cause**: AI provider API is slow or rate-limited.

**Solution**:
1. Check AI provider status
2. Verify API key is valid
3. Try with a smaller `cycle_count` (e.g., 5 instead of 10)
4. Consider using a local AI model (Ollama) for faster responses

### Issue 5: Analysis sensor shows "not_analyzed"

**Cause**: No analysis has been run yet, or analysis failed.

**Solution**:
1. Check Home Assistant logs for errors
2. Manually trigger analysis via service
3. Verify all prerequisites are met

## Performance Notes

- **Response Time**: AI analysis typically takes 10-30 seconds depending on:
  - AI provider (local vs cloud)
  - Amount of data (cycle_count)
  - Analysis type (all vs specific)
  
- **API Costs**: If using cloud AI (OpenAI, Claude):
  - Each cycle analysis costs approximately $0.01-0.03
  - Energy dashboard analysis costs approximately $0.02-0.05
  - Consider using GPT-3.5-turbo for lower costs
  
- **Rate Limiting**: Cloud AI providers have rate limits
  - Don't set `ai_analysis_trigger` to `auto_cycle_end` for frequently-used appliances
  - Consider `periodic_daily` instead

## Automation Examples

### Daily Energy Dashboard Analysis

```yaml
automation:
  - alias: "Daily Energy Dashboard AI Analysis"
    trigger:
      - platform: time
        at: "23:00:00"
    action:
      - service: smart_appliance_monitor.analyze_energy_dashboard
        data:
          period: "today"
          compare_previous: true
```

### Weekly Washing Machine Analysis

```yaml
automation:
  - alias: "Weekly Washing Machine Analysis"
    trigger:
      - platform: time
        at: "20:00:00"
      - platform: time_pattern
        # Every Sunday
        weekday: 0
    condition:
      - condition: time
        weekday:
          - sun
    action:
      - service: smart_appliance_monitor.analyze_cycles
        data:
          entity_id: sensor.washing_machine_state
          analysis_type: all
          cycle_count: 15
```

### Analysis After High Energy Consumption

```yaml
automation:
  - alias: "Analyze High Consumption Cycles"
    trigger:
      - platform: state
        entity_id: sensor.washing_machine_state
        to: "finished"
    condition:
      - condition: template
        value_template: "{{ states('sensor.washing_machine_last_cycle_energy') | float > 1.5 }}"
    action:
      - service: smart_appliance_monitor.analyze_cycles
        data:
          entity_id: sensor.washing_machine_state
          analysis_type: comparative
          cycle_count: 5
```

## Next Steps

Once testing is complete:

1. **Enable automatic analysis** for frequently-used appliances (but watch API costs)
2. **Create dashboards** to display AI insights
3. **Set up automations** to act on recommendations
4. **Monitor savings** by implementing suggested optimizations
5. **Share feedback** on the GitHub repository

## Support

If you encounter issues:

1. Check Home Assistant logs: Settings → System → Logs
2. Enable debug logging for detailed information:
   ```yaml
   logger:
     default: info
     logs:
       custom_components.smart_appliance_monitor: debug
   ```
3. Report issues on GitHub with:
   - Home Assistant version
   - Smart Appliance Monitor version
   - AI Task provider
   - Relevant log excerpts

