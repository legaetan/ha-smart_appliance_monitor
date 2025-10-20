# Reconfiguration Guide

Learn how to modify all settings of your Smart Appliance Monitor integration without losing historical data.

## Overview

The reconfiguration feature allows you to change base settings (appliance type, sensors, pricing) while preserving:
- All statistics
- Cycle history
- Entity configurations
- Automation references

## Accessing Reconfiguration

### Step 1: Navigate to Integration

1. Go to **Settings** → **Devices & Services**
2. Find **Smart Appliance Monitor**
3. Click on your appliance (e.g., "Water Heater")

### Step 2: Click Reconfigure

You'll see a **Reconfigure** button. Click it to open the reconfiguration dialog.

The form will be pre-filled with your current values.

## What Can Be Changed

The reconfiguration flow allows modifying all base settings:

| Parameter           | Can Change | Effect |
|---------------------|------------|--------|
| Appliance Name      | ✅ Yes     | Updates device and entity names |
| Appliance Type      | ✅ Yes     | Changes default thresholds in Advanced Config |
| Power Sensor        | ✅ Yes     | Switches to new power source |
| Energy Sensor       | ✅ Yes     | Switches to new energy source |
| Price Entity        | ✅ Yes     | Changes or removes dynamic pricing |
| Fixed Price         | ✅ Yes     | Updates fallback price value |
| Thresholds (W)      | ❌ No      | Use Advanced Configuration instead |
| Delays (s)          | ❌ No      | Use Advanced Configuration instead |
| Alert Settings      | ❌ No      | Use Advanced Configuration instead |

**Note**: Threshold and timing parameters are configured through **Configure** → **Advanced Configuration**, not reconfiguration.

## Common Use Cases

### 1. Change Appliance Type to Optimize Thresholds

**Scenario**: You configured a water heater as "Other" with default 50W threshold, but it actually starts at 1500W.

**Steps**:
1. Click **Reconfigure**
2. Change **Appliance Type** to "Water Heater"
3. Click **Submit**

**Result**:
- Integration reloads with new settings
- Advanced Configuration now shows 1000W start threshold as default
- All statistics preserved

**Next Step**: Go to **Configure** → **Advanced Configuration** to accept the new profile defaults or customize further.

### 2. Switch from Fixed to Dynamic Pricing

**Scenario**: You want to track costs with time-of-use pricing instead of a fixed rate.

**Steps**:
1. Create an `input_number` for price (see [Configuration Guide](configuration.md#dynamic-pricing-configuration))
2. Click **Reconfigure**
3. Select your `input_number.electricity_price` in **Price Entity**
4. Click **Submit**

**Result**:
- Future cycle costs calculated with dynamic pricing
- Automatic adjustment based on entity value
- Historical cycles keep their recorded costs

### 3. Replace Smart Plug

**Scenario**: Your Sonoff plug failed and you replaced it with a Shelly plug. The entity IDs changed.

**Steps**:
1. Click **Reconfigure**
2. Update **Power Sensor**: `sensor.shelly_plug_power`
3. Update **Energy Sensor**: `sensor.shelly_plug_energy`
4. Click **Submit**

**Result**:
- Monitoring continues with new sensors
- No data loss
- Seamless transition

### 4. Rename Appliance

**Scenario**: You want to use a more descriptive name.

**Steps**:
1. Click **Reconfigure**
2. Change **Appliance Name**: "Oven" → "Kitchen Built-in Oven"
3. Click **Submit**

**Result**:
- Device name updated
- All entity names updated
- Notifications use new name
- Automations continue working (entity IDs unchanged)

## Reconfiguration vs Advanced Configuration

Understanding the difference:

### Reconfiguration (Base Settings)
**Access**: Reconfigure button  
**Purpose**: Change fundamental parameters  
**Changes**:
- Appliance identification
- Data sources
- Pricing method

**When to use**:
- Changing appliance type
- Replacing hardware
- Switching pricing model
- Correcting initial setup mistakes

### Advanced Configuration (Detection Settings)
**Access**: Configure button  
**Purpose**: Fine-tune detection behavior  
**Changes**:
- Power thresholds
- Timing delays
- Alert settings

**When to use**:
- Improving detection accuracy
- Reducing false positives/negatives
- Adjusting alert timing
- Customizing for specific appliance behavior

## What Happens During Reconfiguration

### Behind the Scenes

1. **Validation**: New sensor entities are checked for existence
2. **Update**: Configuration entry data is updated
3. **Reload**: Integration reloads with new settings
4. **Preservation**: Statistics and entity states are maintained

### Data Preservation

**Preserved**:
- ✅ Last cycle data (duration, energy, cost)
- ✅ Daily/monthly statistics
- ✅ Entity histories in Home Assistant database
- ✅ Automation triggers and references
- ✅ Custom entity settings (areas, icons, etc.)

**Not Preserved**:
- ❌ Current cycle in progress (will restart detection)

**Recommendation**: Reconfigure when appliance is idle to avoid interrupting active cycles.

## After Reconfiguration

### Verify New Settings

1. Check the device page - all entities should be present
2. Verify new sensors are providing data:
   - Check power sensor value
   - Check energy sensor value
3. If using dynamic pricing, verify price entity value

### Test Cycle Detection

1. Start your appliance
2. Monitor the running binary sensor
3. Verify cycle start detection
4. Verify cycle end detection

### Adjust Thresholds if Needed

If the new appliance type's default thresholds don't work perfectly:
1. Go to **Configure** → **Advanced Configuration**
2. Adjust thresholds based on test results
3. Test again

## Troubleshooting

### Integration Won't Reload

**Symptom**: Error message after clicking Submit

**Solutions**:
1. Verify selected sensors exist and provide valid data
2. Check Home Assistant logs for specific error
3. Try selecting different sensors
4. If persistent, delete and re-add integration

### Entities Not Updating

**Symptom**: After reconfiguration, entities show unavailable

**Solutions**:
1. Restart Home Assistant
2. Check sensor entities are working
3. Review logs for errors
4. Verify integration shows as loaded

### Statistics Missing

**Symptom**: Historical data not showing

**Solutions**:
1. Check entity history in Developer Tools → States
2. Statistics are preserved in database, may take time to show
3. Recent statistics (last cycle, daily, monthly) should be immediate

### Wrong Thresholds Applied

**Symptom**: Detection not working after type change

**Action**: This is expected. The new appliance type's default thresholds are available in Advanced Configuration, but you must either accept them or set custom values.

**Steps**:
1. **Configure** → **Advanced Configuration**
2. Review the default values (based on new type)
3. Adjust if needed
4. Save

## Best Practices

### When to Reconfigure

**Good Times**:
- Appliance is idle
- No active cycles
- During scheduled maintenance
- After hardware changes

**Avoid**:
- During active cycles
- Peak usage times
- If unsure about new settings

### Testing After Changes

**Checklist**:
- [ ] Entities show correct values
- [ ] Power reading updates
- [ ] Energy reading updates
- [ ] Price entity reads correctly (if applicable)
- [ ] Cycle detection works
- [ ] Notifications arrive
- [ ] Statistics still accessible

### Backup

Before major changes:
1. Note current configuration values
2. Export automations using the integration
3. Screenshot entity settings if customized

## Advanced: Entity ID Stability

**Important**: Entity IDs do NOT change during reconfiguration.

**Example**:
- Before: `sensor.washing_machine_state`
- After rename to "Laundry Room Washer": `sensor.washing_machine_state` (unchanged)

**Benefit**: Automations, scripts, and dashboards continue working without modification.

**Entity Names**: Display names will update to reflect the new appliance name.

## Frequency of Reconfiguration

Reconfiguration is designed for infrequent use:
- Hardware replacement
- Major configuration corrections
- Type misidentification
- Pricing model changes

**Not needed for**:
- Threshold adjustments (use Advanced Configuration)
- Temporary disable (use monitoring switch)
- Testing (use manual cycle service)

## Getting Help

If you encounter issues:
1. Check Home Assistant logs
2. Review this guide
3. Check [GitHub Issues](https://github.com/legaetan/ha-smart_appliance_monitor/issues)
4. Open a new issue with:
   - What you tried to change
   - Error messages
   - Log excerpts

## Related Documentation

- [Configuration Guide](configuration.md) - Initial setup and advanced settings
- [Features Guide](features.md) - All entities and services
- [Installation Guide](installation.md) - Setup instructions

