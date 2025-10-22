# Smart Appliance Monitor v0.5.0 - Advanced Features Release

**Release Date**: October 21, 2025

## 🎉 Major Release - 10 New Entities per Appliance!

Version **0.5.0** brings **massive feature additions** with advanced energy management, scheduling, anomaly detection, and data export capabilities. This release adds **10 new entities** per appliance (30 total entities).

## ✨ Key Features

### 🔌 Auto-Shutdown
Automatically turn off appliances after cycles complete to save energy:
- Configurable delay (5-60 minutes)
- Requires a switch/plug entity
- Safety notification before shutdown
- Manual `force_shutdown` service for testing
- New switch: `switch.auto_shutdown`

### ⚡ Energy Management
Monitor and control energy consumption with limits:
- **Per-cycle limit** - Alert if single cycle exceeds threshold
- **Daily limit** - Monitor daily energy usage
- **Monthly limit** - Track monthly consumption
- **Monthly budget** - Set cost budget in EUR
- New sensors: `binary_sensor.energy_limit_exceeded`, `binary_sensor.budget_exceeded`
- New switch: `switch.energy_limits`

### 📅 Usage Scheduling
Control when appliances can be used:
- **Allowed hours** - Define time windows (e.g., 22h-7h for off-peak)
- **Blocked days** - Prevent usage on specific days
- **Two modes**:
  - **Notification only** - Alert when used outside schedule
  - **Strict block** - Prevent appliance from running
- New sensor: `binary_sensor.usage_allowed`
- New switch: `switch.scheduling`
- Supports time ranges crossing midnight

### 🔍 Anomaly Detection
Intelligent detection of unusual cycles:
- Detects cycles **too short** (<50% of average)
- Detects cycles **too long** (>200% of average)
- Detects **abnormal energy consumption** (±50% from average)
- Based on last 10 cycles
- Real-time anomaly score (0-100%)
- New sensors: `binary_sensor.anomaly_detected`, `sensor.anomaly_score`

### 📊 Data Export
Export your data in multiple formats:
- **CSV Export** - Tabular format for spreadsheets
  - Service: `smart_appliance_monitor.export_to_csv`
- **JSON Export** - Structured data for analysis
  - Service: `smart_appliance_monitor.export_to_json`
- Includes cycle history, statistics, and configuration
- Optional automatic file saving

### 🏠 Energy Dashboard Integration
Native Home Assistant Energy Dashboard support:
- Proper `device_class` and `state_class` for energy sensors
- Compatible sensors: `daily_energy`, `monthly_energy`, `cycle_energy`
- New helper module for configuration
- Step-by-step integration instructions

## 📊 New Entities (10 per appliance)

### Sensors (3)
- `sensor.daily_energy` - Daily consumption (kWh)
- `sensor.monthly_energy` - Monthly consumption (kWh)
- `sensor.anomaly_score` - Anomaly score (0-100%)

### Binary Sensors (4)
- `binary_sensor.energy_limit_exceeded` - Energy limit status
- `binary_sensor.budget_exceeded` - Budget status
- `binary_sensor.usage_allowed` - Schedule compliance
- `binary_sensor.anomaly_detected` - Anomaly alert

### Switches (3)
- `switch.auto_shutdown` - Auto-shutdown control
- `switch.energy_limits` - Energy monitoring control
- `switch.scheduling` - Scheduling control

**Total: 30 entities per appliance** (was 20 in v0.4.1)

## 🚀 Installation

### Via HACS
1. Update Smart Appliance Monitor to v0.5.0
2. Restart Home Assistant
3. Configure new features in Options Flow

### New Users
1. Install via HACS
2. Add integration via UI
3. Follow configuration wizard (now with 6 steps)

## ⚙️ Configuration

### Enhanced Configuration Flow
New optional configuration steps:
- **Energy Management** - Set energy limits and budget
- **Scheduling** - Define allowed hours and blocked days
- **Expert Settings** - Now includes auto-shutdown options

### Accessing New Features
1. Go to **Settings** → **Devices & Services**
2. Find your appliance and click **Configure**
3. Enable "Advanced Configuration" in delays step
4. Configure Energy Management and Scheduling

## 📝 Examples

### Energy Limits
```yaml
# Per-cycle: 2 kWh max
# Daily: 5 kWh max
# Monthly: 50 kWh max
# Budget: €10/month
```

### Scheduling
```yaml
# Off-peak hours only
allowed_hours: "22:00-07:00"
blocked_days: []
mode: "notification_only"
```

### Auto-Shutdown
```yaml
# Shutdown after 10 minutes of inactivity
delay: 10
entity: switch.washing_machine_plug
```

## 🔧 Technical Details

### New Modules
- `export.py` (235 lines) - Data export management
- `energy.py` (175 lines) - Energy Dashboard helper

### Files Modified
- `const.py` (+100 lines) - 50+ new constants
- `config_flow.py` (+150 lines) - Enhanced configuration
- `coordinator.py` (+350 lines) - Feature logic
- `switch.py` (+130 lines) - New switches
- `sensor.py` (+150 lines) - New sensors
- `binary_sensor.py` (+160 lines) - New binary sensors
- `notify.py` (+170 lines) - New notification types
- `services.yaml` (+60 lines) - New services

### Breaking Changes
**None** - Fully backward compatible. All new features are optional and disabled by default.

### Migration Notes
- Existing configurations work without changes
- Monthly stats now include `total_energy` field
- New options available in Options Flow
- No database migration required

## 📚 Documentation

- [Installation Guide](https://github.com/legaetan/ha-smart_appliance_monitor/wiki/Installation)
- [Energy Management](https://github.com/legaetan/ha-smart_appliance_monitor/wiki/Energy-Management)
- [Scheduling](https://github.com/legaetan/ha-smart_appliance_monitor/wiki/Scheduling)
- [Full Changelog](https://github.com/legaetan/ha-smart_appliance_monitor/blob/main/CHANGELOG.md)

## ⚠️ Known Limitations

- Anomaly detection requires at least 3 completed cycles
- Auto-shutdown requires a controllable switch entity
- Scheduling supports one time window per day
- Custom cards still require manual build

---

**Version**: 0.5.0  
**Date**: October 21, 2025  
**Download**: [smart_appliance_monitor-v0.5.0.zip](https://github.com/legaetan/ha-smart_appliance_monitor/releases/download/v0.5.0/smart_appliance_monitor-v0.5.0.zip)

