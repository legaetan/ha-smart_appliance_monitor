# Configuration Guide

This guide covers the initial setup and advanced configuration of Smart Appliance Monitor.

## Initial Setup

### Step 1: Add Integration

1. Go to **Settings** → **Devices & Services**
2. Click **Add Integration** (bottom right button)
3. Search for "Smart Appliance Monitor"
4. Click on it to start configuration

### Step 2: Basic Configuration

You'll be presented with a configuration form:

#### Appliance Name
**Field**: `appliance_name`  
**Required**: Yes  
**Example**: "Washing Machine", "Dishwasher", "Water Heater"

Enter a descriptive name for your appliance. This name will be used:
- As the device name in Home Assistant
- In notifications
- As prefix for all entity names

#### Appliance Type
**Field**: `appliance_type`  
**Required**: Yes  
**Options**:
- Oven
- Dishwasher
- Washing Machine
- Dryer
- Water Heater
- Coffee Maker
- Other

**Important**: The selected type automatically applies optimized threshold values (see Appliance Profiles below).

#### Power Sensor
**Field**: `power_sensor`  
**Required**: Yes  
**Type**: Entity selector (sensor domain)

Select the power sensor from your smart plug. This sensor should provide power readings in Watts (W).

**Example**: `sensor.washing_machine_plug_power`

#### Energy Sensor
**Field**: `energy_sensor`  
**Required**: Yes  
**Type**: Entity selector (sensor domain)

Select the energy sensor from your smart plug. This sensor should provide energy readings in kWh or Wh.

**Example**: `sensor.washing_machine_plug_energy`

#### Price Entity (Optional)
**Field**: `price_entity`  
**Required**: No  
**Type**: Entity selector (sensor or input_number domain)

Select an entity that contains the current electricity price. This enables dynamic pricing (e.g., peak/off-peak hours).

**Example**: `input_number.electricity_price`

If left empty, the fixed price will be used.

#### Price per kWh
**Field**: `price_kwh`  
**Required**: Yes  
**Default**: 0.2516  
**Type**: Number (positive float)

Enter your electricity price per kWh in your local currency. This is used if no price entity is selected, or as a fallback if the entity is unavailable.

**Example**: 0.25 (for $0.25/kWh or €0.25/kWh)

### Step 3: Complete Setup

Click **Submit** to create the integration. Home Assistant will:
1. Validate the selected sensors
2. Create 15 entities for the appliance
3. Start monitoring automatically

## Appliance Profiles

Each appliance type has optimized default thresholds:

### Water Heater
- **Start Threshold**: 1000W (high power consumption)
- **Stop Threshold**: 50W
- **Start Delay**: 60 seconds
- **Stop Delay**: 120 seconds
- **Alert Duration**: 4 hours

**Use Case**: High-power appliances with long heating cycles.

### Oven
- **Start Threshold**: 100W
- **Stop Threshold**: 10W
- **Start Delay**: 60 seconds
- **Stop Delay**: 180 seconds (cooling phase)
- **Alert Duration**: 2 hours

**Use Case**: Medium-power appliances with moderate cycles.

### Dishwasher
- **Start Threshold**: 20W (low initial draw)
- **Stop Threshold**: 5W
- **Start Delay**: 120 seconds
- **Stop Delay**: 300 seconds
- **Alert Duration**: 3 hours

**Use Case**: Variable power appliances with long cycles.

### Washing Machine
- **Start Threshold**: 10W (very sensitive)
- **Stop Threshold**: 5W
- **Start Delay**: 120 seconds
- **Stop Delay**: 300 seconds
- **Alert Duration**: 3 hours

**Use Case**: Detects even eco modes with low power draw.

### Dryer
- **Start Threshold**: 100W
- **Stop Threshold**: 10W
- **Start Delay**: 60 seconds
- **Stop Delay**: 180 seconds
- **Alert Duration**: 2 hours

**Use Case**: High-power appliances with steady consumption.

### Coffee Maker
- **Start Threshold**: 50W
- **Stop Threshold**: 5W
- **Start Delay**: 30 seconds (quick detection)
- **Stop Delay**: 60 seconds (quick detection)
- **Alert Duration**: 30 minutes

**Use Case**: Short cycles requiring fast response.

### Other
- **Start Threshold**: 50W
- **Stop Threshold**: 5W
- **Start Delay**: 120 seconds
- **Stop Delay**: 300 seconds
- **Alert Duration**: 2 hours

**Use Case**: General-purpose profile for unknown appliances.

## Advanced Configuration

After initial setup, you can fine-tune detection thresholds:

### Accessing Advanced Settings

1. Go to **Settings** → **Devices & Services**
2. Find **Smart Appliance Monitor**
3. Click on your appliance
4. Click **Configure**
5. Select **Advanced Configuration**

### Advanced Parameters

#### Start Threshold (W)
**Range**: 1-5000W  
**Default**: Based on appliance type

Minimum power consumption to trigger cycle start. If your appliance doesn't detect starts:
- **Increase**: If false starts occur (e.g., standby mode triggers detection)
- **Decrease**: If starts are missed (e.g., eco modes not detected)

#### Stop Threshold (W)
**Range**: 1-100W  
**Default**: Based on appliance type

Maximum power consumption to trigger cycle stop. Adjust if:
- **Increase**: Cycle ends too early (e.g., during pause or rinse phases)
- **Decrease**: Cycle continues too long after completion

#### Start Delay (seconds)
**Range**: 10-600 seconds  
**Default**: Based on appliance type

Time power must stay above threshold before confirming cycle start. This prevents false positives from brief power spikes.

- **Increase**: More false starts occurring
- **Decrease**: Need faster detection (but risk more false positives)

#### Stop Delay (seconds)
**Range**: 10-1800 seconds  
**Default**: Based on appliance type

Time power must stay below threshold before confirming cycle stop. This prevents premature end detection during pauses.

- **Increase**: Cycle ending during pauses/intermediate phases
- **Decrease**: Need faster end detection (but risk premature endings)

#### Enable Duration Alert
**Type**: Boolean  
**Default**: False

Enable notifications when a cycle exceeds the expected duration.

#### Alert Duration (seconds)
**Range**: 1800-21600 seconds  
**Default**: Based on appliance type

Maximum expected cycle duration before alerting. Only applies if duration alert is enabled.

## Dynamic Pricing Configuration

### Creating a Price Entity

#### Method 1: Input Number

Add to `configuration.yaml`:

```yaml
input_number:
  electricity_price:
    name: Electricity Price
    min: 0
    max: 1
    step: 0.0001
    unit_of_measurement: "€/kWh"
    mode: box
```

#### Method 2: Template Sensor

For automatic price updates based on time:

```yaml
template:
  - sensor:
      - name: "Current Electricity Price"
        unique_id: current_electricity_price
        unit_of_measurement: "€/kWh"
        state: >
          {% set hour = now().hour %}
          {% if hour >= 22 or hour < 7 %}
            0.1821
          {% else %}
            0.2516
          {% endif %}
```

### Updating Price via Automation

```yaml
automation:
  - alias: "Update Electricity Price - Peak Hours"
    trigger:
      - platform: time
        at: "07:00:00"
    action:
      - service: input_number.set_value
        target:
          entity_id: input_number.electricity_price
        data:
          value: 0.2516

  - alias: "Update Electricity Price - Off-Peak Hours"
    trigger:
      - platform: time
        at: "22:00:00"
    action:
      - service: input_number.set_value
        target:
          entity_id: input_number.electricity_price
        data:
          value: 0.1821
```

### Selecting Price Entity

During initial configuration or reconfiguration:
1. In the **Price Entity** field, select your `input_number.electricity_price` or template sensor
2. The integration will use the current value from this entity
3. Costs are calculated in real-time based on the entity's value

**Benefits**:
- Automatic cost calculation with variable rates
- Support for time-of-use tariffs
- Integration with dynamic pricing systems

## Testing Your Configuration

### Manual Cycle Test

1. Turn on your appliance
2. Monitor the entities:
   - `binary_sensor.{appliance}_running` should turn ON after start_delay
   - `sensor.{appliance}_state` should show "running"
   - `sensor.{appliance}_cycle_duration` should start incrementing

3. When appliance finishes:
   - `binary_sensor.{appliance}_running` should turn OFF after stop_delay
   - `sensor.{appliance}_state` should show "finished"
   - Last cycle sensors should populate with statistics

### Check Notifications

If notifications are enabled:
- You should receive a "Cycle Started" notification
- You should receive a "Cycle Finished" notification with statistics

### Debugging

If detection doesn't work as expected:

1. Check the power sensor readings match your expectations
2. Review logs for state machine transitions:
   ```
   Settings → System → Logs
   Filter: "smart_appliance_monitor"
   ```

3. Adjust thresholds in Advanced Configuration
4. Test again

## Multiple Appliances

To monitor multiple appliances:
1. Add the integration multiple times (once per appliance)
2. Each will create its own device with 15 entities
3. Each can have different settings and profiles

**Example**:
- Smart Appliance Monitor (Washing Machine)
- Smart Appliance Monitor (Dishwasher)
- Smart Appliance Monitor (Dryer)

## Next Steps

- [Reconfiguration Guide](reconfiguration.md) - Modify settings without losing data
- [Features Guide](features.md) - Learn about all entities and services

