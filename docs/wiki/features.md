# Features Guide

Complete reference for all entities, services, and features of Smart Appliance Monitor.

## Overview

Each configured appliance creates 15 entities in Home Assistant:
- 10 Sensors
- 2 Binary Sensors
- 2 Switches
- 1 Button

## Sensors

### State Sensor

**Entity ID**: `sensor.{appliance}_state`  
**Type**: Sensor  
**Device Class**: None  
**States**: `idle`, `running`, `finished`

Shows the current state of the appliance:
- **idle**: Appliance is off or in standby
- **running**: Active cycle in progress
- **finished**: Cycle completed, awaiting acknowledgment

**Usage**:
- Automation triggers
- Dashboard display
- Voice assistant queries

**Example Automation**:
```yaml
automation:
  - alias: "Notify when washing done"
    trigger:
      - platform: state
        entity_id: sensor.washing_machine_state
        to: "finished"
    action:
      - service: notify.mobile_app
        data:
          message: "Washing machine finished!"
```

### Cycle Duration

**Entity ID**: `sensor.{appliance}_cycle_duration`  
**Type**: Sensor  
**Device Class**: Duration  
**Unit**: minutes  
**State Class**: measurement

Current cycle duration in minutes. Updates every 30 seconds while running.

**Value**: `0` when idle or finished, increments during cycle

**Usage**:
- Real-time monitoring
- Progress tracking
- Estimated completion (with manual calculation)

### Cycle Energy

**Entity ID**: `sensor.{appliance}_cycle_energy`  
**Type**: Sensor  
**Device Class**: Energy  
**Unit**: kWh  
**State Class**: measurement

Energy consumed in current cycle.

**Value**: `0` when idle or finished, increments during cycle

**Usage**:
- Energy monitoring
- Efficiency comparisons
- Anomaly detection

### Cycle Cost

**Entity ID**: `sensor.{appliance}_cycle_cost`  
**Type**: Sensor  
**Device Class**: Monetary  
**Unit**: EUR (or your currency)  
**State Class**: measurement

Cost of current cycle based on energy and price.

**Calculation**: `energy (kWh) × price (€/kWh)`

**Value**: `0` when idle or finished, increments during cycle

**Note**: Uses current price from price entity or fixed price.

### Last Cycle Duration

**Entity ID**: `sensor.{appliance}_last_cycle_duration`  
**Type**: Sensor  
**Device Class**: Duration  
**Unit**: minutes  

Duration of the most recently completed cycle.

**Persistence**: Retained across restarts

**Usage**:
- Historical comparison
- Pattern recognition
- Automation conditions

**Example**:
```yaml
automation:
  - alias: "Alert if cycle too short"
    trigger:
      - platform: state
        entity_id: sensor.dishwasher_state
        to: "finished"
    condition:
      - condition: numeric_state
        entity_id: sensor.dishwasher_last_cycle_duration
        below: 30
    action:
      - service: notify.mobile_app
        data:
          message: "Dishwasher cycle unusually short - check for issues"
```

### Last Cycle Energy

**Entity ID**: `sensor.{appliance}_last_cycle_energy`  
**Type**: Sensor  
**Device Class**: Energy  
**Unit**: kWh  

Energy consumed in the most recently completed cycle.

**Persistence**: Retained across restarts

**Usage**:
- Energy tracking
- Efficiency monitoring
- Cost verification

### Last Cycle Cost

**Entity ID**: `sensor.{appliance}_last_cycle_cost`  
**Type**: Sensor  
**Device Class**: Monetary  
**Unit**: EUR (or your currency)  

Cost of the most recently completed cycle.

**Persistence**: Retained across restarts

**Note**: Reflects the price at the time of cycle completion.

### Daily Cycles

**Entity ID**: `sensor.{appliance}_daily_cycles`  
**Type**: Sensor  
**State Class**: measurement

Number of cycles completed today.

**Reset**: Automatically resets to 0 at midnight

**Usage**:
- Usage patterns
- Daily reports
- Anomaly detection (e.g., multiple unexpected cycles)

**Example Dashboard Card**:
```yaml
type: entity
entity: sensor.washing_machine_daily_cycles
name: "Washes Today"
icon: mdi:washing-machine
```

### Daily Cost

**Entity ID**: `sensor.{appliance}_daily_cost`  
**Type**: Sensor  
**Device Class**: Monetary  
**Unit**: EUR (or your currency)  
**State Class**: total

Total cost of all cycles today.

**Reset**: Automatically resets to 0 at midnight

**Calculation**: Sum of all cycle costs for the current day

**Usage**:
- Daily expense tracking
- Budget monitoring
- Energy dashboard integration

### Monthly Cost

**Entity ID**: `sensor.{appliance}_monthly_cost`  
**Type**: Sensor  
**Device Class**: Monetary  
**Unit**: EUR (or your currency)  
**State Class**: total

Total cost of all cycles this month.

**Reset**: Automatically resets to 0 on the 1st of each month

**Calculation**: Sum of all cycle costs for the current month

**Usage**:
- Monthly expense tracking
- Budget planning
- Long-term cost analysis

## Binary Sensors

### Running

**Entity ID**: `binary_sensor.{appliance}_running`  
**Type**: Binary Sensor  
**Device Class**: running

Indicates whether the appliance is currently running a cycle.

**States**:
- **ON**: Appliance is running
- **OFF**: Appliance is idle or finished

**Usage**:
- Simple on/off automation triggers
- Dashboard indicators
- Voice assistant status queries

**Example**:
```yaml
automation:
  - alias: "Flash lights when dryer done"
    trigger:
      - platform: state
        entity_id: binary_sensor.dryer_running
        from: "on"
        to: "off"
    action:
      - service: light.turn_on
        target:
          entity_id: light.living_room
        data:
          flash: short
```

### Duration Alert

**Entity ID**: `binary_sensor.{appliance}_alert_duration`  
**Type**: Binary Sensor  
**Device Class**: problem

Indicates whether the current cycle has exceeded the expected duration.

**States**:
- **ON**: Cycle running longer than alert_duration setting
- **OFF**: Normal operation

**Note**: Only active if duration alert is enabled in Advanced Configuration.

**Usage**:
- Maintenance alerts
- Anomaly detection
- Automation for stuck cycles

**Example**:
```yaml
automation:
  - alias: "Alert on stuck dishwasher"
    trigger:
      - platform: state
        entity_id: binary_sensor.dishwasher_alert_duration
        to: "on"
    action:
      - service: notify.mobile_app
        data:
          message: "Dishwasher running unusually long - check for issues"
          title: "Appliance Alert"
```

## Switches

### Monitoring Switch

**Entity ID**: `switch.{appliance}_monitoring`  
**Type**: Switch

Controls whether cycle detection is active for this appliance.

**States**:
- **ON**: Monitoring enabled (default)
- **OFF**: Monitoring disabled

**Behavior When OFF**:
- No cycle detection
- No statistics updates
- No notifications
- Entities remain available but static

**Usage**:
- Temporarily disable monitoring
- Maintenance mode
- Energy saving (prevents unnecessary updates)

**Persistence**: State persists across restarts

**Example**:
```yaml
automation:
  - alias: "Disable monitoring during vacation"
    trigger:
      - platform: state
        entity_id: input_boolean.vacation_mode
        to: "on"
    action:
      - service: switch.turn_off
        target:
          entity_id: switch.washing_machine_monitoring
```

### Notifications Switch

**Entity ID**: `switch.{appliance}_notifications`  
**Type**: Switch

Controls whether notifications are sent for this appliance.

**States**:
- **ON**: Notifications enabled (default)
- **OFF**: Notifications disabled

**Behavior When OFF**:
- Monitoring continues
- Statistics still track
- No notifications sent

**Usage**:
- Quiet hours
- Do not disturb mode
- Selective notification management

**Independent**: Works independently of monitoring switch

**Example**:
```yaml
automation:
  - alias: "Disable notifications at night"
    trigger:
      - platform: time
        at: "22:00:00"
    action:
      - service: switch.turn_off
        target:
          entity_id: 
            - switch.washing_machine_notifications
            - switch.dishwasher_notifications
```

## Buttons

### Reset Statistics

**Entity ID**: `button.{appliance}_reset_stats`  
**Type**: Button

Resets all statistics for the appliance.

**Effect**:
- Clears last cycle data
- Resets daily cycles counter
- Resets daily cost
- Resets monthly cost
- Current cycle continues if running

**Usage**:
- After appliance replacement
- Start fresh tracking
- After major reconfiguration
- Data cleanup

**Confirmation**: No confirmation dialog - immediate action

**Example**:
```yaml
automation:
  - alias: "Reset stats monthly"
    trigger:
      - platform: time
        at: "00:00:01"
    condition:
      - condition: template
        value_template: "{{ now().day == 1 }}"
    action:
      - service: button.press
        target:
          entity_id: button.dishwasher_reset_stats
```

## Services

### start_cycle

**Service**: `smart_appliance_monitor.start_cycle`

Manually trigger a cycle start.

**Parameters**:
- `device_id` (required): Target appliance device ID

**Use Cases**:
- Testing cycle detection
- Manual tracking when auto-detection not suitable
- Override detection logic

**Example**:
```yaml
service: smart_appliance_monitor.start_cycle
data:
  device_id: "abc123..."
```

**Note**: Useful for debugging or situations where automatic detection is disabled.

### stop_monitoring

**Service**: `smart_appliance_monitor.stop_monitoring`

Disable monitoring for a specific appliance.

**Parameters**:
- `device_id` (required): Target appliance device ID

**Effect**: Same as turning off the monitoring switch

**Use Cases**:
- Automation-based disabling
- Group control of multiple appliances
- Temporary suspension

**Example**:
```yaml
service: smart_appliance_monitor.stop_monitoring
data:
  device_id: "abc123..."
```

### reset_statistics

**Service**: `smart_appliance_monitor.reset_statistics`

Reset all statistics for a specific appliance.

**Parameters**:
- `device_id` (required): Target appliance device ID

**Effect**: Same as pressing the reset statistics button

**Use Cases**:
- Automated resets
- Scripted data management
- Maintenance workflows

**Example**:
```yaml
service: smart_appliance_monitor.reset_statistics
data:
  device_id: "abc123..."
```

## Notifications

### Types

#### Cycle Started
Sent when an appliance begins a cycle.

**Content**:
- Appliance name
- Start time
- Current power draw

**Actions**:
- Stop Monitoring

#### Cycle Finished
Sent when a cycle completes.

**Content**:
- Appliance name
- Duration
- Energy consumed
- Cost

**Actions**:
- View Details
- Reset Statistics

#### Duration Alert
Sent when a cycle exceeds expected duration.

**Content**:
- Appliance name
- Current duration
- Expected duration

**Actions**:
- Stop Cycle
- Dismiss Alert

### Customization

Notifications respect:
- Notification switch state
- Mobile app notification settings
- Home Assistant notification services

**Fallback**: If mobile_app service unavailable, uses persistent_notification.

## Events

The integration fires Home Assistant events that can be used in automations:

### smart_appliance_monitor_cycle_started

**Data**:
- `appliance_name`
- `appliance_type`
- `entry_id`

### smart_appliance_monitor_cycle_finished

**Data**:
- `appliance_name`
- `appliance_type`
- `entry_id`
- `duration`
- `energy`
- `cost`

### smart_appliance_monitor_alert_duration

**Data**:
- `appliance_name`
- `appliance_type`
- `entry_id`
- `duration`

**Example**:
```yaml
automation:
  - alias: "Log cycle completion"
    trigger:
      - platform: event
        event_type: smart_appliance_monitor_cycle_finished
    action:
      - service: logbook.log
        data:
          name: "{{ trigger.event.data.appliance_name }}"
          message: "Completed in {{ trigger.event.data.duration }} minutes"
```

## Integration with Home Assistant Features

### Energy Dashboard

Sensors can be added to the Energy Dashboard:
- Use monthly_cost sensor for cost tracking
- Energy sensors track consumption

### History & Recorder

All sensor data is automatically recorded and available in:
- History panel
- Logbook
- Database for long-term analysis

### Template Sensors

Create custom sensors based on integration data:

```yaml
template:
  - sensor:
      - name: "Average Wash Cost"
        unit_of_measurement: "EUR"
        state: >
          {% set daily = states('sensor.washing_machine_daily_cost')|float %}
          {% set cycles = states('sensor.washing_machine_daily_cycles')|int %}
          {% if cycles > 0 %}
            {{ (daily / cycles)|round(2) }}
          {% else %}
            0
          {% endif %}
```

### Statistics & Long Term Data

Monthly cost sensors use state_class: total, enabling:
- Long-term statistics
- Energy Dashboard integration
- Historical data retention

## Tips & Best Practices

### Dashboard Cards

**Recommended Cards**:
- Entity card for state sensor
- Gauge card for cycle duration
- History graph for cost sensors
- Button card for reset

**Example**:
```yaml
type: entities
entities:
  - entity: sensor.washing_machine_state
  - entity: binary_sensor.washing_machine_running
  - entity: sensor.washing_machine_cycle_duration
  - entity: sensor.washing_machine_cycle_cost
  - entity: sensor.washing_machine_daily_cycles
  - entity: switch.washing_machine_monitoring
  - entity: button.washing_machine_reset_stats
```

### Automation Ideas

1. **TTS Announcements**: Announce when cycles finish
2. **LED Indicators**: Change light colors based on state
3. **Smart Scheduling**: Track usage patterns for off-peak optimization
4. **Maintenance Reminders**: Alert after X cycles
5. **Cost Alerts**: Notify if daily/monthly budget exceeded

## Troubleshooting

### Entities Unavailable

**Check**:
1. Integration loaded correctly
2. Power/energy sensors available
3. Home Assistant logs for errors

### Incorrect Readings

**Verify**:
1. Source sensor units (W, kWh)
2. Threshold settings appropriate
3. Delays configured correctly

### No Notifications

**Check**:
1. Notification switch ON
2. Mobile app configured
3. Home Assistant notification service working

## Related Documentation

- [Configuration Guide](configuration.md) - Setup and settings
- [Reconfiguration Guide](reconfiguration.md) - Modify settings
- [Installation Guide](installation.md) - Setup instructions

