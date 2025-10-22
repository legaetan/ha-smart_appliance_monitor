# Smart Appliance Monitor v0.4.0 - Enhanced Configuration UX

**Release Date**: October 20, 2025

## 🎨 Configuration Redesign

Version **0.4.0** completely redesigns the configuration experience with a **4-step multi-step flow** and **natural time units** (minutes/hours instead of seconds).

## ✨ Key Improvements

### Multi-Step Configuration Flow
Configuration now split into logical steps:
1. **Detection Thresholds** - Power thresholds (start/stop)
2. **Delays & Alerts** - Time delays with expert mode toggle
3. **Notifications** - Service selection and notification types
4. **Expert Settings** - Advanced parameters (optional)

**Benefits:**
- 2-5 fields per screen instead of overwhelming single form
- Logical progression through configuration
- Expert options hidden by default

### Natural Time Units
**Before v0.4.0:**
- ⏱️ Start delay: 10-600 seconds
- ⏱️ Stop delay: 10-1800 seconds  
- ⏱️ Alert duration: 1800-86400 seconds

**After v0.4.0:** ✅
- ⏱️ Start delay: 0.5-10 **minutes**
- ⏱️ Stop delay: 0.5-30 **minutes**
- ⏱️ Alert duration: 0.5-24 **hours**

Much more intuitive!

### Expert Mode
Advanced settings hidden by default:
- Unplugged detection timeout
- Custom notification service name
- Accessible via toggle in step 2

### Enhanced Descriptions
Every field now has:
- Clear explanation of what it does
- Concrete examples adapted to appliance type
- Recommended value ranges
- Contextual help

## 📊 Configuration Example

### Simple User Flow
```
Step 1: Thresholds
  - Start power: 100W
  - Stop power: 10W

Step 2: Delays
  - Start delay: 2 minutes
  - Stop delay: 3 minutes
  - Expert mode: OFF → Skip to Step 3

Step 3: Notifications
  - Services: Telegram, Mobile App
  - Types: Cycle complete, Long duration
```

### Expert User Flow
```
Same as above, but in Step 2:
  - Expert mode: ON → Continue to Step 4

Step 4: Expert Settings
  - Unplugged timeout: 5 minutes
  - Custom service: my_custom_notifier
```

## 🔧 Technical Details

**Files Modified:**
- `config_flow.py` - 210+ lines refactored
  - Multi-step implementation
  - Automatic unit conversions
  - Conditional navigation
- `strings.json` - Complete restructuring
  - 4 step definitions
  - Enhanced descriptions
- `translations/fr.json` - Full French localization

**Backward Compatibility:** ✅ 100%
- Existing configurations load without modification
- Old seconds values automatically converted for display
- Modified values converted back to seconds for storage
- No migration needed

**Unit Conversions:**
- Display: seconds → minutes/hours
- Storage: minutes/hours → seconds
- Internal format unchanged

## 📦 Installation

### Via HACS
1. Update Smart Appliance Monitor to v0.4.0
2. Restart Home Assistant  
3. Reconfigure appliances to see new UI (optional)

### Notes
- Existing configurations continue to work
- Reconfiguration recommended to benefit from new UX
- All translations updated (EN/FR)

---

**Version**: 0.4.0  
**Date**: October 20, 2025  
**Download**: [smart_appliance_monitor-v0.4.0.zip](https://github.com/legaetan/ha-smart_appliance_monitor/releases/download/v0.4.0/smart_appliance_monitor-v0.4.0.zip)

