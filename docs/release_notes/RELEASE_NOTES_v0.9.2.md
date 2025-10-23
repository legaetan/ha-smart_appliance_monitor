# Smart Appliance Monitor v0.9.2 - Bug Fixes & Code Quality

**Release Date**: January 23, 2025  
**Type**: Bug Fix Release  
**Download**: [smart_appliance_monitor-v0.9.2.zip](https://github.com/legaetan/ha-smart_appliance_monitor/releases/tag/v0.9.2)

## Overview

This release fixes critical bugs affecting notification persistence and the Energy Dashboard sync service, while also improving code quality by properly implementing the Home Assistant translation system.

## 🐛 Bug Fixes

### Notification Persistence Fixed

**Problem**: Notification switch states (cycle_started, cycle_finished, alert_duration, unplugged) were not saved and were reset to default values after Home Assistant restart.

**Solution**: 
- Added `notification_type_switches` dictionary to the state persistence system in `coordinator.py`
- Notification switches now trigger state save when toggled
- States are properly restored from `.storage/smart_appliance_monitor.{entry_id}` on restart

**Impact**: Your notification preferences will now be preserved across Home Assistant restarts.

### Energy Dashboard Sync Service Error Fixed

**Problem**: The `sync_with_energy_dashboard` service failed with error: "property 'price_kwh' of 'SmartApplianceCoordinator' object has no setter"

**Solution**:
- Updated the service to use the `GlobalConfigManager` for price management (introduced in v0.9.0)
- Removed direct assignments to the read-only `price_kwh` property
- Service now properly updates global price configuration for all appliances

**Impact**: The Energy Dashboard sync service now works correctly and updates global pricing without errors.

## 🔧 Code Quality Improvements

### Entity Name Translation System

**What Changed**: Removed 33 hardcoded French entity names (`_attr_name`) and implemented proper Home Assistant translation system.

**Technical Details**:
- Removed `_attr_name` assignments in:
  - `sensor.py`: 15 sensors
  - `binary_sensor.py`: 7 binary sensors
  - `switch.py`: 10 switches
  - `button.py`: 1 button
- Entity IDs remain in English (e.g., `sensor.clim_cycle_cost`)
- Display names are now translated automatically via `_attr_translation_key` system
- Uses `translations/fr.json` for French, `strings.json` for English

**Impact for Users**:
- ✅ **Existing installations**: No impact - entity IDs are preserved in entity registry
- ✅ **New installations**: Cleaner entity ID generation from the start
- ✅ **Developers**: Better code maintainability and follows Home Assistant best practices

## 📋 Installation

### For New Users

1. Download via HACS or manually from [GitHub Releases](https://github.com/legaetan/ha-smart_appliance_monitor/releases/tag/v0.9.2)
2. Restart Home Assistant
3. Add integration via UI: Settings → Devices & Services → Add Integration → Smart Appliance Monitor

### For Existing Users

#### Via HACS (Recommended)
1. Open HACS
2. Go to Integrations
3. Find "Smart Appliance Monitor"
4. Click "Update"
5. Restart Home Assistant

#### Manual Update
1. Download the latest release
2. Extract to `custom_components/smart_appliance_monitor/`
3. Restart Home Assistant

## 🔍 What to Test

After updating:

1. **Notification Persistence**:
   - Toggle notification switches on/off
   - Restart Home Assistant
   - Verify switches maintain their state

2. **Energy Dashboard Sync**:
   - Call service `smart_appliance_monitor.sync_with_energy_dashboard`
   - Verify no errors in logs
   - Check that global price is synced correctly

3. **Entity Names**:
   - Check that entity friendly names are properly translated
   - Verify entity IDs remain in English

## 📝 Full Changelog

See [CHANGELOG.md](https://github.com/legaetan/ha-smart_appliance_monitor/blob/main/CHANGELOG.md) for complete details.

## 🔗 Documentation

- **Wiki**: https://github.com/legaetan/ha-smart_appliance_monitor/wiki
- **Installation Guide**: https://github.com/legaetan/ha-smart_appliance_monitor/wiki/Installation
- **Configuration Guide**: https://github.com/legaetan/ha-smart_appliance_monitor/wiki/Configuration

## 🐛 Found a Bug?

Please report issues on [GitHub Issues](https://github.com/legaetan/ha-smart_appliance_monitor/issues) with:
- Home Assistant version
- Integration version
- Detailed description
- Relevant logs from `Settings → System → Logs`

## 🙏 Thank You

Thank you for using Smart Appliance Monitor! Your feedback helps improve the integration.

---

**Previous Release**: [v0.9.1](https://github.com/legaetan/ha-smart_appliance_monitor/releases/tag/v0.9.1) - Dashboard Enhancements & Energy Dashboard Integration


