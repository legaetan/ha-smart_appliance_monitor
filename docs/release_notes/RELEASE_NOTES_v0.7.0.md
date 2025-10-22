# Release Notes v0.7.0 - AI-Powered Cycle Analysis 🤖

**Release Date**: October 21, 2025

## Overview

Smart Appliance Monitor v0.7.0 introduces comprehensive AI-powered analysis capabilities, bringing intelligent insights and optimization recommendations to your appliance monitoring. Using Home Assistant AI Tasks, the integration can now analyze your usage patterns, compare against historical data, and provide personalized recommendations to reduce energy consumption and costs.

## 🌟 Highlights

- **🤖 AI-Powered Analysis**: Leverage OpenAI, Claude, Ollama, or any HA-compatible AI to analyze appliance usage
- **📊 Three Analysis Types**: Pattern, Comparative, and Recommendations analysis
- **💡 Energy Optimization**: Identify potential savings and optimal usage hours
- **🏠 Global Dashboard Analysis**: AI analysis of entire home energy consumption
- **🔄 Automatic Triggering**: Optional automatic analysis after each cycle
- **🌍 Bilingual**: Full support in English and French

## 🆕 What's New

### AI Analysis Features

#### Individual Appliance Analysis
Analyze your appliances to understand:
- **Usage Patterns**: When and how you use your appliances
- **Energy Trends**: Whether consumption is increasing or decreasing
- **Optimization Opportunities**: How to reduce costs and energy usage
- **Personalized Recommendations**: Tailored advice based on your habits

#### Global Energy Dashboard Analysis
Get a bird's-eye view of your home:
- **Efficiency Score**: Overall home energy efficiency (0-100)
- **Top Consumers**: Identify which appliances use the most energy
- **Optimization Opportunities**: Where to focus your efforts
- **Monthly Savings Potential**: Estimated savings if recommendations are followed

### New Services

1. **`configure_ai`** - Set up AI analysis for all appliances
2. **`analyze_cycles`** - Analyze individual appliance usage
3. **`analyze_energy_dashboard`** - Analyze global home consumption

### New Entities

- **AI Analysis Sensor** (`sensor.<appliance>_ai_analysis`) - Stores analysis results per appliance
- **AI Analysis Switch** (`switch.<appliance>_ai_analysis`) - Enable/disable analysis per appliance
- **Energy Dashboard AI Sensor** (`sensor.sam_energy_dashboard_ai_analysis`) - Global efficiency score

## 🚀 Getting Started

### Prerequisites

1. **Home Assistant AI Integration**: Configure an AI Task entity
   - OpenAI Conversation
   - Anthropic Claude
   - Google Generative AI
   - Ollama (local)
   - Or any other HA-compatible AI provider

2. **Cycle History**: Enable anomaly detection on your appliances to build cycle history (5-10 cycles recommended)

### Quick Setup

1. **Configure AI Task**:
   ```yaml
   service: smart_appliance_monitor.configure_ai
   data:
     ai_task_entity: ai_task.openai_ai_task
     enable_ai_analysis: true
     ai_analysis_trigger: manual  # or auto_cycle_end
   ```

2. **Analyze an Appliance**:
   ```yaml
   service: smart_appliance_monitor.analyze_cycles
   data:
     entity_id: sensor.washing_machine_state
     analysis_type: all
     cycle_count: 10
   ```

3. **Check Results**: View `sensor.washing_machine_ai_analysis` for insights and recommendations

### Detailed Testing Guide

See [TESTING_AI.md](../TESTING_AI.md) for comprehensive setup instructions and test scenarios.

## 📖 Example Use Cases

### Cost Savings
**Scenario**: You want to reduce your electricity bill.

**Solution**: Run AI analysis to identify:
- Peak usage hours when electricity is most expensive
- Recommended off-peak hours for running appliances
- Estimated monthly savings by shifting usage

**Example Output**:
```
Status: needs_improvement
Recommendations:
  - Shift washing machine usage to 22:00-06:00 for off-peak rates
  - Reduce average cycle duration by using eco mode
  - Schedule dishwasher during weekend off-peak hours
Potential Savings: 2.5 kWh/month (€0.63/month)
```

### Maintenance Alerts
**Scenario**: Detect when appliances might need maintenance.

**Solution**: Comparative analysis identifies unusual patterns:
- Increasing energy consumption over time
- Longer cycle durations than normal
- Unusual power spikes

**Example Output**:
```
Status: normal
Insights:
  - Average consumption increased by 15% over last month
  - This may indicate need for maintenance or cleaning
  - Consider descaling or filter cleaning
```

### Usage Optimization
**Scenario**: Optimize household energy consumption.

**Solution**: Global dashboard analysis provides:
- Home-wide efficiency score
- Top energy consumers
- Specific optimization recommendations per appliance

**Example Output**:
```
Efficiency Score: 72/100
Top Consumers:
  1. Water Heater (45% of consumption)
  2. Washing Machine (23%)
  3. Dryer (18%)
Recommendations:
  - Lower water heater temperature to 55°C
  - Use cold water cycles for washing machine
  - Consider air-drying instead of using dryer
Estimated Monthly Savings: €12.50
```

## 💰 Cost Considerations

### Cloud AI Providers (OpenAI, Claude)
- **Per-cycle analysis**: ~$0.01-0.03
- **Dashboard analysis**: ~$0.02-0.05
- **Monthly estimate** (10 appliances, weekly analysis): ~$2-5

### Local AI (Ollama)
- **Cost**: Free (hardware only)
- **Faster responses**: 5-15 seconds vs 10-30 seconds
- **Privacy**: All data stays local
- **Recommendation**: Use Llama 2, Mistral, or similar

## 🎯 Best Practices

### For Best Results

1. **Build History First**: Wait for 5-10 cycles before analyzing
2. **Enable Anomaly Detection**: Ensures cycle history is tracked
3. **Start Manual**: Test with `manual` trigger before enabling `auto_cycle_end`
4. **Review Regularly**: Weekly or monthly analysis provides best insights
5. **Act on Recommendations**: Implement suggestions and re-analyze to measure improvement

### Automation Examples

**Daily Dashboard Analysis**:
```yaml
automation:
  - alias: "Daily Energy Analysis"
    trigger:
      - platform: time
        at: "23:00:00"
    action:
      - service: smart_appliance_monitor.analyze_energy_dashboard
        data:
          period: today
          compare_previous: true
```

**Weekly Appliance Deep Dive**:
```yaml
automation:
  - alias: "Weekly Washing Machine Analysis"
    trigger:
      - platform: time_pattern
        hours: "20"
      - platform: time
        at: "20:00:00"
    condition:
      - condition: time
        weekday: [sun]
    action:
      - service: smart_appliance_monitor.analyze_cycles
        data:
          entity_id: sensor.washing_machine_state
          analysis_type: all
          cycle_count: 15
```

## 🔧 Technical Details

### Architecture
- **No Direct API Calls**: All AI communication via Home Assistant AI Tasks
- **Structured Responses**: Validated fields with type checking
- **Persistent Storage**: Configuration saved in `.storage/smart_appliance_monitor.global_config`
- **Event-Driven**: Fires events for completed/failed analyses

### Data Privacy
- **Local Processing**: Export and formatting done locally
- **Opt-In**: AI analysis is disabled by default
- **Per-Appliance Control**: Enable/disable analysis for specific appliances
- **Data Control**: Optional export for review before sending to AI

### Performance
- **Analysis Time**: 10-30 seconds (cloud) or 5-15 seconds (local)
- **Cache**: Analysis results cached in sensor
- **Async**: Non-blocking operations
- **Background**: Auto-analysis runs in background

## 🐛 Known Issues

None at this time. Please report any issues on [GitHub](https://github.com/legaetan/ha-smart_appliance_monitor/issues).

## 🔄 Upgrade Instructions

### From v0.6.0
1. Restart Home Assistant to load new modules
2. Configure AI using the `configure_ai` service
3. Enable AI analysis switch for desired appliances
4. Run your first analysis!

### From Earlier Versions
1. Upgrade to v0.6.0 first (if not already done)
2. Follow upgrade instructions above

**Note**: No breaking changes. All existing features work as before.

## 📚 Documentation

- **README.md** - Updated with AI features section
- **TESTING_AI.md** - Complete testing guide with 6 test scenarios
- **CHANGELOG.md** - Detailed technical changes
- **services.yaml** - Service documentation for Developer Tools

## 🙏 Feedback & Contributions

We'd love to hear about your experience with AI analysis!

- **Feedback**: Share your results and suggestions on GitHub Discussions
- **Issues**: Report bugs on GitHub Issues
- **Contributions**: Pull requests welcome!

## 🎉 Thank You

Thank you to the Home Assistant community for feedback and testing, and to all AI providers for making their models accessible through Home Assistant.

---

**Enjoy smarter energy monitoring!** 🤖⚡

*Smart Appliance Monitor - Making your home smarter, one appliance at a time.*

