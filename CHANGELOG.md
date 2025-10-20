# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-10-20

### Added

#### Core Features
- **Automatic Cycle Detection** - State machine-based detection with configurable thresholds and delays
- **Data Coordinator** - Centralized data management with 30-second polling interval
- **Configuration Flow** - Complete UI-based configuration and reconfiguration
- **Multi-language Support** - Full interface in English and French

#### Entities (14 per appliance)
- **Sensors (10)**:
  - State (idle/running/finished)
  - Cycle duration, energy, and cost (current cycle)
  - Last cycle duration, energy, and cost
  - Daily cycles count and cost
  - Monthly cost
- **Binary Sensors (2)**:
  - Running status
  - Duration alert
- **Switches (2)**:
  - Monitoring enable/disable
  - Notifications enable/disable
- **Buttons (1)**:
  - Reset statistics

#### Services
- `start_cycle` - Manually trigger cycle start
- `stop_monitoring` - Disable monitoring for specific appliance
- `reset_statistics` - Clear all statistics

#### Appliance Profiles
Pre-configured optimized thresholds for different appliance types:
- **Oven** - 100W start threshold, 2h alert
- **Dishwasher** - 20W start threshold, 3h alert
- **Washing Machine** - 10W start threshold, 3h alert
- **Dryer** - 100W start threshold, 2h alert
- **Water Heater** - 1000W start threshold, 4h alert
- **Coffee Maker** - 50W start threshold, 30min alert
- **Other** - 50W start threshold, 2h alert

#### Dynamic Pricing
- Support for electricity price via Home Assistant entities (`input_number` or `sensor`)
- Automatic fallback to fixed price if entity unavailable
- Real-time cost calculation based on current rate

#### Reconfiguration
- Modify all base settings without losing statistics
- Update appliance type (thresholds auto-adapt)
- Change sensors (power/energy)
- Switch between fixed and dynamic pricing
- Rename appliances

#### Notifications
- Cycle started notifications with appliance details
- Cycle finished notifications with duration, energy, and cost
- Duration alert notifications for cycles exceeding expected time
- Automatic fallback to persistent notifications

#### Testing
- 75+ unit tests across all components
- ~95% code coverage
- Fixtures for common test scenarios
- Pytest configuration with markers

#### Documentation
- Comprehensive README
- Development guide
- Implementation summary
- Complete API documentation in code

### Technical Details

#### Components Implemented
- `state_machine.py` - Cycle detection logic (260 lines)
- `coordinator.py` - Data coordination (389 lines)
- `config_flow.py` - Configuration UI (256 lines)
- `sensor.py` - Sensor platform (395 lines)
- `binary_sensor.py` - Binary sensor platform (124 lines)
- `switch.py` - Switch platform (128 lines)
- `button.py` - Button platform (80 lines)
- `notify.py` - Notification system (230 lines)
- `entity.py` - Base entity class (50 lines)
- `device.py` - Device utilities (70 lines)
- `services.yaml` - Service definitions (51 lines)

#### Statistics Tracking
- Per-cycle statistics (duration, energy, cost)
- Daily statistics (cycle count, total cost)
- Monthly statistics (total cost)
- Persistent storage across restarts

#### Configuration Options
- Appliance name and type
- Power and energy sensors
- Electricity price (fixed or entity-based)
- Start/stop thresholds (W)
- Start/stop delays (seconds)
- Duration alert threshold (seconds)
- Duration alert enable/disable

### Performance
- Lightweight polling (30-second intervals)
- Efficient state machine with minimal overhead
- Optimized sensor updates
- Smart caching of price data

### Known Limitations
- Single appliance per configuration entry
- No machine learning auto-calibration (planned for v0.5.0)
- No built-in dashboard generation (planned for v0.5.0)
- No direct Energy Dashboard integration (planned for v0.2.0)

## [Unreleased]

### Planned for v0.2.0
- HACS publication
- Energy Dashboard integration
- Data export (CSV, JSON)
- Enhanced automation support
- Graphs in notifications

### Planned for v0.5.0
- Machine learning auto-calibration
- Intelligent cycle pattern detection
- Automatic threshold adjustment
- Cycle duration predictions

### Planned for v1.0.0
- Automatic dashboard generation
- Multi-appliance groups
- Advanced analytics
- Third-party API integration

[0.1.0]: https://github.com/legaetan/ha-smart_appliance_monitor/releases/tag/v0.1.0

