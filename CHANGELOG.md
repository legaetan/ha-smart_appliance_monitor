# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.1] - 2025-10-20

### Added
- **Bundled Dashboard Templates** - Templates now included directly in the integration
  - 7 templates embedded in `/custom_components/smart_appliance_monitor/dashboards/`
  - Automatic installation, no manual setup required
  - Users can override templates by creating `/config/dashboards/templates/`

### Changed
- **Template Loading Priority** - Smart template resolution
  1. First checks `/config/dashboards/templates/` (user custom templates)
  2. Then falls back to `/custom_components/smart_appliance_monitor/dashboards/` (bundled templates)
  - Allows users to customize templates without modifying integration files
  - Ensures templates always available out-of-the-box

### Fixed
- **Dashboard Generation Error** - Fixed "No such file or directory" error
  - Templates no longer require manual creation in `/config/dashboards/templates/`
  - Service `generate_dashboard_yaml` now works immediately after installation
  - Better error handling with clear fallback mechanism

### Improved
- **User Experience** - Zero configuration for dashboard templates
  - No need to read installation docs for basic usage
  - Templates "just work" after integration installation
  - Advanced users can still customize by placing templates in `/config/dashboards/templates/`

### Technical Details
- Templates location: `/custom_components/smart_appliance_monitor/dashboards/*.yaml`
- Custom templates location: `/config/dashboards/templates/*.yaml` (optional)
- Priority: custom → bundled → generic
- Backward compatible with existing custom template setups

## [0.4.0] - 2025-10-20

### Added

#### Multi-Step Configuration Flow
- **4-Step Advanced Configuration** - Configuration divided into logical steps
  - Step 1: Detection Thresholds (start/stop power thresholds)
  - Step 2: Detection Delays & Alerts (with expert mode toggle)
  - Step 3: Notifications (services and types selection)
  - Step 4: Expert Settings (optional, only if expert mode enabled)
- Better UX with focused screens instead of single overwhelming form
- Progressive navigation through configuration process

#### User-Friendly Time Units
- **Minutes for delays** - Instead of seconds for better comprehension
  - Start delay: 0.5-10 minutes (was 10-600 seconds)
  - Stop delay: 0.5-30 minutes (was 10-1800 seconds)
- **Hours for alerts** - Instead of seconds for duration alerts
  - Alert duration: 0.5-24 hours (was 1800-86400 seconds)
- **Minutes for unplugged timeout** - In expert settings
  - Unplugged timeout: 1-60 minutes (was 60-3600 seconds)
- Automatic bidirectional conversion (display ↔ storage)
- Values still stored in seconds internally for full backward compatibility

#### Expert Mode
- **Optional Expert Settings** - Advanced parameters hidden by default
  - Unplugged detection timeout
  - Custom notification service name
- Toggle in Step 2 to access expert settings
- Simplified interface for standard users
- Full power for advanced users when needed

#### Enhanced Descriptions
- **Detailed explanations** for every configuration field
- **Concrete examples** adapted to appliance type
  - "100W for oven, 10W for washing machine"
- **Recommended value ranges** clearly indicated
- **Contextual help** explaining what each parameter does

### Changed

#### Configuration Flow
- Options flow completely refactored from single to multi-step
- `async_step_init()` - Now handles only thresholds (step 1)
- New `async_step_delays()` - Handles delays and alerts (step 2)
- New `async_step_notifications()` - Handles notification settings (step 3)
- New `async_step_expert()` - Handles expert parameters (step 4)
- State persistence across steps with `self._options`

#### Translation Files
- English strings updated with 4 new step definitions
- French translations updated with complete localization
- All field labels updated to reflect new units
- Descriptions significantly enhanced in both languages

### Improved

#### User Experience
- **Reduced cognitive load** - 2-5 fields per screen instead of 10
- **Clearer progression** - Logical flow from thresholds → delays → notifications
- **Natural units** - Minutes and hours instead of seconds
- **Better accessibility** - Expert options hidden by default
- **Contextual guidance** - Each step has clear description and purpose

#### Configuration Quality
- **Easier to understand** - Natural time units (2 min vs 120 sec)
- **Harder to make mistakes** - Smaller ranges with appropriate steps
- **Better defaults visible** - Values make more sense to users
- **Flexible validation** - Supports decimal values (1.5 minutes = 90 seconds)

### Technical Details

#### Files Modified
- `config_flow.py` - 210+ lines refactored
  - Multi-step flow implementation
  - Automatic unit conversions (min↔sec, h↔sec)
  - Conditional navigation (expert mode)
  
- `strings.json` - Complete restructuring
  - 4 step definitions (init, delays, notifications, expert)
  - New field names with unit suffixes
  - Enhanced descriptions with examples
  
- `translations/fr.json` - Full French localization
  - All 4 steps translated
  - Natural French expressions
  - Localized examples

#### Backward Compatibility
- ✅ **100% backward compatible**
- Existing configurations load without modification
- Old values in seconds automatically converted to minutes/hours for display
- Modified values automatically converted back to seconds for storage
- No migration script needed
- Internal storage format unchanged

#### Unit Conversions
```python
# Display conversion
start_delay_minutes = config_value_seconds / 60

# Storage conversion  
config_value_seconds = user_input_minutes * 60
```

### Notes
- Expert mode toggle is not persisted in configuration (UI-only flag)
- All validation ranges adapted to new units
- Decimal values supported (e.g., 1.5 hours = 5400 seconds)
- Documentation updated with migration guide

### Breaking Changes
None - This is a UX improvement release with full backward compatibility.

## [0.3.0] - 2025-10-20

### Added

#### Dashboard Templates (7)
- **Dashboard Template System** - Pre-configured Lovelace YAML templates for each appliance type
  - `generic.yaml` - Universal template for any appliance
  - `washing_machine.yaml` - Optimized for washing machines (1-3h cycles)
  - `dishwasher.yaml` - Optimized for dishwashers (2-4h cycles)
  - `monitor.yaml` - For screens/displays (session-based, up to 8h)
  - `nas.yaml` - For NAS devices (session-based, intensive activity detection)
  - `printer_3d.yaml` - For 3D printers (extended cycles up to 24h+)
  - `vmc.yaml` - For ventilation systems (session-based, boost mode detection)

#### Dashboard Generation Service
- **`generate_dashboard_yaml` Service** - Automatically generates dashboard YAML
  - Detects appliance type and loads appropriate template
  - Replaces all entity ID placeholders automatically
  - Sends persistent notification with complete YAML code
  - Logs full YAML for easy copy-paste
  - Optional custom cards support parameter

#### Dashboard Features
- **6 Pre-configured Sections per Dashboard**:
  - Status Overview - Large visual card with state and badges
  - Current Cycle/Session - Duration gauge, energy, cost
  - Power Consumption - 24h power graph with Mini Graph Card
  - Controls - All switches and buttons in one place
  - Statistics - Last cycle, daily, and monthly stats
  - Alerts - Conditional cards for duration/unplugged warnings
  
- **Custom Card Integration**:
  - Mushroom Cards for modern UI
  - Mini Graph Card for power consumption visualization
  - Conditional cards for alerts
  - Template cards with dynamic colors and icons

- **Adaptive Layouts**:
  - Templates adapt to appliance type (cycle vs session terminology)
  - Gauge ranges optimized per appliance type
  - Appropriate icons and colors
  - Mobile-friendly responsive design

#### Documentation
- **Dashboard README** (`/dashboards/README.md`) - Complete guide with:
  - Installation instructions for custom cards
  - Manual and service-based setup methods
  - Customization examples
  - Troubleshooting guide
  - Multi-appliance dashboard examples
  
- **Wiki Page** (`Dashboards.md`) - Comprehensive documentation:
  - Quick start guide
  - Template descriptions
  - Screenshot galleries (to be added)
  - Custom card installation
  - Advanced customization

### Changed
- **English as Default Language** - All code, services, and templates now in English
  - Python code messages translated to English
  - Service definitions (`services.yaml`) in English
  - Dashboard templates in English
  - French translations maintained in `fr.json`
  
- **Notification Messages** - Dashboard generation notifications in English

### Technical Details
- **Template System**: 7 YAML files in `/dashboards/templates/`
- **Service Implementation**: `generate_dashboard_yaml` in `__init__.py`
- **Total Lines of YAML**: ~1,500 lines across all templates
- **Custom Cards Supported**: Mushroom, Mini Graph Card, Button Card

### Breaking Changes
None - This is a feature addition release.

### Notes
- Custom cards (Mushroom, Mini Graph Card) must be installed via HACS for full visual experience
- Templates work with standard HA cards but are optimized for custom cards
- Dashboard YAML must be manually copied to dashboard (auto-creation planned for v0.4.0)

## [0.2.0] - 2025-10-20

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

## [0.2.0] - 2025-10-20

### Added

#### New Appliance Types (4)
- **Monitor (Écran)** - Screen/display usage session tracking
  - 30W start threshold, 5W stop threshold
  - 8-hour alert duration for long sessions
  - Uses "session" terminology instead of "cycle"
- **NAS** - Network storage intensive activity detection
  - 50W start threshold (detects intensive activity above baseline)
  - 20W stop threshold (return to idle)
  - 6-hour alert duration for long backups/transfers
  - Uses "session" terminology instead of "cycle"
- **3D Printer (Imprimante 3D)** - Long-duration print monitoring
  - 50W start threshold, 10W stop threshold
  - 24-hour alert duration (essentially disabled for very long prints)
- **VMC (Ventilation)** - Ventilation boost mode detection
  - 20W start threshold, 10W stop threshold
  - 2-hour alert duration for extended boost periods
  - Uses "session" terminology instead of "cycle"

#### Session-Based Terminology
- Smart terminology adaptation based on appliance type
- Monitor, NAS, and VMC now use "session" terminology for better UX
- Dynamic sensor naming: `session_duration`, `session_energy`, `session_cost`, `daily_sessions`
- Automatic translation key selection based on appliance type
- Improves clarity for devices with continuous or intensive operation patterns

#### Unplugged Detection
- **New Binary Sensor**: `binary_sensor.unplugged`
  - Detects when appliance is disconnected or powered off
  - Configurable timeout (default: 5 minutes at 0W)
  - Device class: `PROBLEM`
  - Extra attributes: `time_at_zero_power`, `unplugged_timeout`, `detection_progress`
- Automatic notification when appliance detected as unplugged
- Helps identify power issues and accidental disconnections
- Tracks zero-power duration in state machine

#### Advanced Notification System
- **Multi-service notification support**:
  - Mobile App (automatic detection of available mobile_app_* services)
  - Telegram (with markdown formatting)
  - Persistent Notification (fallback)
  - Custom service (user-configurable)
- **Per-notification-type control** with 4 configurable types:
  - Cycle/Session Started
  - Cycle/Session Finished
  - Alert Duration
  - Unplugged Alert
- **Two-level control system**:
  - Configuration via Options Flow (persistent settings)
  - Quick-toggle switches for each notification type
- Notification service configuration in Options Flow
- Custom notification service name support
- Intelligent service availability detection

#### New Switches (4)
- `switch.notification_cycle_started` - Toggle start notifications
- `switch.notification_cycle_finished` - Toggle completion notifications
- `switch.notification_alert_duration` - Toggle duration alerts
- `switch.notification_unplugged` - Toggle unplugged alerts
- All switches enabled by default
- Independent control without affecting configuration
- Icons adapt to switch state

#### Configuration Options
- `unplugged_timeout` - Time at 0W before detecting as unplugged (60-3600s, default: 300s)
- `notification_services` - Multi-select for notification services
- `notification_types` - Multi-select for notification types to receive
- `custom_notify_service` - Custom notification service name

### Changed
- **Sensor entity IDs** now adapt based on appliance type
  - Cycle-based: `cycle_duration`, `cycle_energy`, etc.
  - Session-based: `session_duration`, `session_energy`, etc.
- **Notification system** completely refactored for extensibility
  - SmartApplianceNotifier class redesigned
  - Support for simultaneous multiple services
  - Service-specific formatting (e.g., Telegram markdown)
- **Binary sensor platform** extended with unplugged detection
- **Switch platform** extended with 4 notification type switches
- **State machine** enhanced with zero-power tracking
- **Coordinator** integrated all new systems and event handlers

### Improved
- **Better UX** with context-aware terminology (cycle vs session)
- **Flexible notification configuration** at multiple levels
  - Global enable/disable switch
  - Service selection in options
  - Type selection in options
  - Individual switches per type
- **Enhanced monitoring** with unplugged detection
- **Better device categorization** with 11 appliance types total
- **More granular control** over notification behavior
- **Documentation** significantly expanded

### Technical Details
- Total entities per appliance: **19** (up from 15)
  - 10 Sensors (adaptive naming)
  - 3 Binary Sensors (running, alert_duration, **unplugged**)
  - 6 Switches (monitoring, notifications, **4 notification type switches**)
  - 1 Button (reset stats)
- New events: `smart_appliance_monitor_unplugged`
- State machine now tracks zero-power time
- Coordinator handles 4 event types (was 3)
- Full bilingual support (EN/FR) for all new features

## [Unreleased]

### Planned for v0.3.0
- Dashboard templates (7 appliance-specific templates)
- Service `create_dashboard` for automatic dashboard generation
- Custom cards (smart-appliance-cycle-card, smart-appliance-stats-card)
- HACS publication
- Energy Dashboard integration
- Data export (CSV, JSON)

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

