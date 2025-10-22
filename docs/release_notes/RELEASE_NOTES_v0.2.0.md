# Smart Appliance Monitor v0.2.0 - Initial Release

**Release Date**: October 20, 2025

## 🎉 Initial Public Release

Version **0.2.0** is the first public release of Smart Appliance Monitor, a complete solution for monitoring smart plugs and tracking appliance cycles in Home Assistant.

## ✨ Core Features

### Automatic Cycle Detection
- State machine-based detection
- Configurable power thresholds (start/stop)
- Configurable delays for accuracy
- Idle → Running → Finished states

### Complete Entity Set
**14 entities per appliance:**

**Sensors (10):**
- Current state (idle/running/finished)
- Cycle duration, energy, cost (current)
- Last cycle duration, energy, cost
- Daily cycles count and cost
- Monthly cost

**Binary Sensors (2):**
- Running status
- Unplugged detection

**Switches (1):**
- Monitoring control

**Buttons (1):**
- Reset statistics

### Notification System
Multiple notification services:
- **Telegram** - Rich notifications with inline actions
- **Mobile App** - Push notifications with actionable buttons
- **Persistent Notifications** - In-HA notifications

5 notification types:
- Cycle start
- Cycle finish
- Long duration alert
- Unplugged warning
- Statistics reset confirmation

### Configuration Flow
- Complete UI-based configuration
- Power threshold setup
- Detection delays configuration
- Notification service selection
- Bilingual interface (EN/FR)

### Multi-Language Support
- English as default language
- Complete French translations
- All UI elements localized

## 📊 Technical Details

### Architecture
- **State Machine:** Robust cycle detection
- **Data Coordinator:** 30-second polling
- **Device Integration:** Proper HA device grouping
- **Statistics Tracking:** Daily and monthly

### Entity Count Per Appliance
- **Total:** 14 entities
- **Sensors:** 10
- **Binary Sensors:** 2
- **Switches:** 1
- **Buttons:** 1

### Services
- `reset_statistics` - Reset all counters
- `force_state` - Manual state override (debug)

## 📦 Installation

### Via HACS
1. Add custom repository in HACS
2. Install "Smart Appliance Monitor"
3. Restart Home Assistant
4. Add integration via UI

### Configuration
1. Select power sensor
2. Configure power thresholds
3. Set detection delays
4. Choose notification services
5. Done!

## 🎯 Use Cases

### Washing Machine
```
Start threshold: 10W
Stop threshold: 5W
Start delay: 60s
Stop delay: 180s
```

### Dishwasher
```
Start threshold: 10W
Stop threshold: 5W  
Start delay: 120s
Stop delay: 300s
```

### Dryer
```
Start threshold: 100W
Stop threshold: 10W
Start delay: 60s
Stop delay: 300s
```

## 📚 Documentation

- [GitHub Wiki](https://github.com/legaetan/ha-smart_appliance_monitor/wiki)
- [Installation Guide](https://github.com/legaetan/ha-smart_appliance_monitor/wiki/Installation)
- [Configuration Guide](https://github.com/legaetan/ha-smart_appliance_monitor/wiki/Configuration)

## 🚀 Roadmap

Planned for future releases:
- Dashboard templates
- Enhanced configuration UX
- Data export capabilities
- Energy management features
- AI-powered analytics

---

**Version**: 0.2.0  
**Date**: October 20, 2025  
**Download**: [smart_appliance_monitor-v0.2.0.zip](https://github.com/legaetan/ha-smart_appliance_monitor/releases/download/v0.2.0/smart_appliance_monitor-v0.2.0.zip)

