# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.5.3] - 2025-10-21

### Fixed

#### HACS Installation Structure
- **Fixed cards not being installed via HACS** - Moved www/ folder into integration directory
  - Moved `www/` from repository root to `custom_components/smart_appliance_monitor/www/`
  - Updated path resolution in `_register_frontend_resources()` function
  - Cards now properly installed when updating via HACS
  - Fixed path to be relative to integration folder instead of config root

### Technical Details

**Files Modified:**
- `custom_components/smart_appliance_monitor/__init__.py` - Updated www_path to `Path(__file__).parent / "www" / ...`
- Repository structure - Moved `www/` folder into integration directory

**Breaking Changes:** None

**Migration Notes:** 
- Users who installed v0.5.2: Update to v0.5.3 to get cards automatically installed
- Cards will be available at `/hacsfiles/smart-appliance-cards/` after update

## [0.5.2] - 2025-10-20

### Added

#### Frontend Cards Auto-Installation
- **Automatic Lovelace cards registration** - Custom cards now automatically available after HACS installation
  - Cards registered at `/hacsfiles/smart-appliance-cards/` path
  - Two cards included: `smart-appliance-cycle-card.js` and `smart-appliance-stats-card.js`
  - Auto-detection and validation of card files at startup
  - Informative logs for successful registration

#### Build System
- **Pre-compiled card assets** - Cards are now pre-built and versioned in Git
  - Compiled JavaScript files included in `www/smart-appliance-cards/dist/`
  - No manual build step required for users
  - Cards ready to use immediately after installation

### Changed

#### Documentation
- **Updated installation instructions** - Simplified setup process documented
  - New "Automatic Installation" section in cards README
  - Clear instructions for adding resources to Lovelace (one-time setup)
  - Maintained "Manual Installation" section for advanced users

#### Build Configuration
- **Updated .gitignore** - Frontend build artifacts now properly managed
  - `node_modules/` excluded from version control
  - Compiled `dist/` files explicitly included for distribution

### Technical Details

**Files Modified:**
- `custom_components/smart_appliance_monitor/__init__.py` - Added `_register_frontend_resources()` function
- `.gitignore` - Added exceptions for compiled card files
- `www/smart-appliance-cards/README.md` - Updated installation documentation
- `www/smart-appliance-cards/dist/` - Added pre-compiled cards (38KB + 43KB)

**Breaking Changes:** None

**Migration Notes:** 
- Existing installations: Cards will be automatically available after update
- Users must add resources to Lovelace once (see documentation)

## [0.5.1] - 2025-10-20

### Added

#### State Persistence System
- **Automatic state persistence** - All cycle data and statistics preserved across Home Assistant restarts
  - Cycle state (`idle`, `running`, `finished`) saved automatically
  - Current cycle data preserved (start time, start energy, peak power)
  - Last completed cycle data retained (duration, energy, cost)
  - Daily statistics saved (date, cycle count, total energy, total cost)
  - Monthly statistics saved (year, month, total energy, total cost)
  - Cycle history preserved for anomaly detection
  - Configuration state saved (monitoring enabled, notifications enabled)
  
- **Smart validation** - Data integrity checks on restore
  - Daily statistics reset if date has changed
  - Monthly statistics reset if month has changed
  - Current cycle always restored regardless of date
  
- **Storage system** - Using Home Assistant's native `.storage` system
  - Location: `<config_dir>/.storage/smart_appliance_monitor.<entry_id>.json`
  - Version: 1 (prepared for future migrations)
  - Automatic save on: cycle start, cycle finish, every 30s during cycle
  - Automatic restore on Home Assistant startup

#### Documentation
- **docs/PERSISTENCE.md** - Complete technical documentation
  - Storage format and location
  - Serialization details
  - Error handling
  - Examples and use cases
  
- **RESUME_PERSISTANCE.md** - Implementation summary in French
  - Problem statement and solution
  - Files modified and created
  - Concrete usage examples

#### Tests
- **tests/test_persistence.py** - Comprehensive test suite (11 tests)
  - Serialization/deserialization tests
  - Save/restore cycle verification
  - Obsolete data reset validation
  - Automatic save trigger tests

### Changed

#### Coordinator (`coordinator.py`)
- Added `Store` import from `homeassistant.helpers.storage`
- New constants: `STORAGE_VERSION = 1`, `STORAGE_KEY = "state"`
- New instance variable: `self._store` for persistent storage
- New methods:
  - `_save_state()` - Saves complete coordinator state
  - `restore_state()` - Restores state from storage
  - `_serialize_cycle()` / `_deserialize_cycle()` - Cycle data conversion
  - `_serialize_stats()` / `_deserialize_stats()` - Statistics conversion
- Enhanced event handlers to trigger automatic saves:
  - `_on_cycle_started()` - Saves on cycle start
  - `_on_cycle_finished()` - Saves on cycle completion
- Enhanced `_async_update_data()` - Periodic save during running cycles

#### Integration Init (`__init__.py`)
- Added `restore_state()` call during coordinator setup
- Ensures state restoration before first update

### Fixed
- **Data loss on restart** - Cycles and statistics no longer lost when Home Assistant restarts
- **Incorrect duration calculation** - Cycles correctly track duration even across restarts
- **Lost daily/monthly statistics** - All statistics properly preserved

### Technical Details

#### Files Created
- `docs/PERSISTENCE.md` (183 lines) - Technical documentation
- `RESUME_PERSISTANCE.md` (150 lines) - Implementation summary
- `tests/test_persistence.py` (279 lines) - Test suite

#### Files Modified
- `custom_components/smart_appliance_monitor/__init__.py` (+4 lines) - State restoration
- `custom_components/smart_appliance_monitor/coordinator.py` (+186 lines) - Complete persistence system

#### Storage Format
```json
{
  "state": "running",
  "current_cycle": {...},
  "last_cycle": {...},
  "daily_stats": {...},
  "monthly_stats": {...},
  "cycle_history": [],
  "monitoring_enabled": true,
  "notifications_enabled": true
}
```

### Benefits

1. **No Data Loss** - Running cycles continue correctly after HA restart
2. **Accurate Statistics** - Duration and energy calculations remain precise
3. **Better UX** - Users don't lose tracking data during maintenance
4. **Reliable Anomaly Detection** - Cycle history preserved for ML analysis

### Breaking Changes

None - This release is fully backward compatible. The persistence system gracefully handles missing storage files.

### Migration Notes

- No action required from users
- Existing configurations will start saving state automatically
- First restart after upgrade will not restore data (nothing saved yet)
- Subsequent restarts will benefit from persistence

### Known Limitations

- Storage files are not automatically backed up (use HA backup system)
- No migration system yet for future storage version changes
- No service to manually trigger save operation

## [0.5.0] - 2025-10-21

### Added

#### Auto-Shutdown Feature
- **Automatic appliance shutdown** after configurable inactivity period (5-60 minutes)
  - Optional feature, disabled by default
  - Configurable delay after cycle finish or prolonged inactivity
  - Requires configuration of a switch/plug entity to cut power
  - New event: `EVENT_AUTO_SHUTDOWN`
  - New configuration options: `CONF_ENABLE_AUTO_SHUTDOWN`, `CONF_AUTO_SHUTDOWN_DELAY`, `CONF_AUTO_SHUTDOWN_ENTITY`
  - New switch: `switch.auto_shutdown` to enable/disable the feature
  - Notification sent before shutdown
  - Service `force_shutdown` for manual testing

#### Energy Management System
- **Energy limits monitoring** with configurable thresholds
  - Per-cycle energy limit (e.g., 2 kWh max per cycle)
  - Daily energy limit (e.g., 5 kWh max per day)
  - Monthly energy limit (e.g., 50 kWh max per month)
  - Monthly cost budget (e.g., 10€ max per month)
  - New configuration options: `CONF_ENABLE_ENERGY_LIMITS`, `CONF_ENERGY_LIMIT_CYCLE`, `CONF_ENERGY_LIMIT_DAILY`, `CONF_ENERGY_LIMIT_MONTHLY`, `CONF_COST_BUDGET_MONTHLY`
  - New binary sensors:
    - `binary_sensor.energy_limit_exceeded` - Indicates if any energy limit is exceeded
    - `binary_sensor.budget_exceeded` - Indicates if monthly budget is exceeded
  - New switch: `switch.energy_limits` to enable/disable energy monitoring
  - Automatic notifications when limits are exceeded
  - Reset notifications on new day/month

#### Scheduling System
- **Usage scheduling** with allowed time windows and blocked days
  - Configure allowed hours (e.g., 22h-7h for off-peak hours)
  - Block specific days of the week (e.g., Sunday)
  - Two modes: "notification_only" or "strict_block"
  - New configuration options: `CONF_ENABLE_SCHEDULING`, `CONF_ALLOWED_HOURS_START`, `CONF_ALLOWED_HOURS_END`, `CONF_BLOCKED_DAYS`, `CONF_SCHEDULING_MODE`
  - New binary sensor: `binary_sensor.usage_allowed` - Indicates if current usage is within allowed schedule
  - New switch: `switch.scheduling` to enable/disable scheduling
  - Notification if appliance used outside allowed hours
  - Support for time ranges crossing midnight (e.g., 22:00-07:00)

#### Anomaly Detection
- **Intelligent anomaly detection** based on historical patterns
  - Detects cycles that are too short (<50% of average duration)
  - Detects cycles that are too long (>200% of average duration)
  - Detects abnormal energy consumption (±50% from average)
  - Based on history of last 10 cycles
  - New configuration option: `CONF_ENABLE_ANOMALY_DETECTION`
  - New binary sensor: `binary_sensor.anomaly_detected` - Active when anomaly is detected
  - New sensor: `sensor.anomaly_score` (0-100%) - Real-time anomaly score
  - Automatic notification when anomaly is detected
  - Cycle history tracking in coordinator

#### Data Export
- **CSV export** - Export appliance data to CSV format
  - Current cycle, last cycle, daily and monthly statistics
  - Configuration details included
  - Service: `smart_appliance_monitor.export_to_csv`
  - Optional file path parameter for automatic saving
  - CSV content returned in notification and logs

- **JSON export** - Export appliance data to JSON format
  - Complete structured data export
  - Includes cycle history for anomaly detection
  - Service: `smart_appliance_monitor.export_to_json`
  - Optional file path parameter for automatic saving
  - JSON content returned in notification and logs

- New module: `export.py` - Data export management
  - `SmartApplianceDataExporter` class
  - Export summary generation

#### Energy Dashboard Integration
- **Native Energy Dashboard support**
  - Sensors marked with proper device_class and state_class
  - New module: `energy.py` - Energy Dashboard helper
  - `EnergyDashboardHelper` class for configuration assistance
  - Functions to generate Energy Dashboard configuration
  - Instructions for adding appliances to Energy Dashboard
  - Compatible sensors: `daily_energy`, `monthly_energy`, `cycle_energy`

#### New Sensors (3)
- `sensor.daily_energy` - Daily energy consumption (kWh) with TOTAL state class
- `sensor.monthly_energy` - Monthly energy consumption (kWh) with TOTAL state class
- `sensor.anomaly_score` - Current anomaly score (0-100%)

#### New Binary Sensors (4)
- `binary_sensor.energy_limit_exceeded` - Energy limit status
- `binary_sensor.budget_exceeded` - Budget exceeded status
- `binary_sensor.usage_allowed` - Usage scheduling status
- `binary_sensor.anomaly_detected` - Anomaly detection status

#### New Switches (3)
- `switch.auto_shutdown` - Enable/disable automatic shutdown
- `switch.energy_limits` - Enable/disable energy limits monitoring
- `switch.scheduling` - Enable/disable usage scheduling

#### New Services (3)
- `export_to_csv` - Export data to CSV format
- `export_to_json` - Export data to JSON format
- `force_shutdown` - Manual shutdown trigger (for testing)

#### New Configuration Steps
- **Step: Energy Management** (optional) - Configure energy limits and budget
- **Step: Scheduling** (optional) - Configure allowed hours and blocked days
- **Enhanced Expert Step** - Now includes auto-shutdown configuration

### Changed

#### Configuration Flow
- Added `configure_advanced` toggle in delays step to access energy management and scheduling
- Added `enable_anomaly_detection` toggle in delays step
- Expert step now includes auto-shutdown configuration (delay and entity selection)
- Configuration flow now has up to 6 steps total (init → delays → [energy_management] → [scheduling] → [expert] → notifications)

#### Coordinator
- Monthly stats now track both energy and cost (`total_energy` added)
- New methods: `set_auto_shutdown_enabled()`, `set_energy_limits_enabled()`, `set_scheduling_enabled()`
- New check methods: `_check_auto_shutdown()`, `_check_energy_limits()`, `_check_scheduling()`, `_check_anomaly_detection()`
- New event handlers: `_on_auto_shutdown()`, `_on_energy_limit_exceeded()`, `_on_budget_exceeded()`, `_on_usage_out_of_schedule()`, `_on_anomaly_detected()`
- Cycle history tracking for anomaly detection (`_cycle_history` list)
- Auto-shutdown timer management (`_auto_shutdown_timer`)
- Energy limit notification flags to prevent spam
- Integrated all new features into `_async_update_data()` method

#### Notification System
- Added 5 new notification types: auto_shutdown, energy_limit, budget, schedule, anomaly
- New notification methods in `notify.py`:
  - `notify_auto_shutdown()`
  - `notify_energy_limit_exceeded()`
  - `notify_budget_exceeded()`
  - `notify_usage_out_of_schedule()`
  - `notify_anomaly_detected()`

### Improved

#### Statistics
- Monthly energy tracking added (was cost-only before)
- Cycle history for machine learning analysis
- Better reset logic for daily/monthly boundaries

#### Code Quality
- All new features follow existing architecture patterns
- Comprehensive error handling in all new modules
- Logging added for all major operations
- Type hints throughout new code

### Technical Details

#### Files Created
- `custom_components/smart_appliance_monitor/export.py` (235 lines)
- `custom_components/smart_appliance_monitor/energy.py` (175 lines)

#### Files Modified
- `const.py` (+100 lines) - 50+ new constants for all features
- `config_flow.py` (+150 lines) - 2 new steps, enhanced expert step
- `coordinator.py` (+350 lines) - All feature logic and checks
- `switch.py` (+130 lines) - 3 new switch classes
- `sensor.py` (+150 lines) - 3 new sensor classes
- `binary_sensor.py` (+160 lines) - 4 new binary sensor classes
- `notify.py` (+170 lines) - 5 new notification methods
- `services.yaml` (+60 lines) - 3 new service definitions
- `__init__.py` (+120 lines) - 3 new service handlers
- `manifest.json` - Version updated to 0.5.0

#### Total Entity Count
- **Sensors**: 13 (was 10)
  - Added: `daily_energy`, `monthly_energy`, `anomaly_score`
- **Binary Sensors**: 7 (was 3)
  - Added: `energy_limit_exceeded`, `budget_exceeded`, `usage_allowed`, `anomaly_detected`
- **Switches**: 9 (was 6)
  - Added: `auto_shutdown`, `energy_limits`, `scheduling`
- **Buttons**: 1 (unchanged)

**Total per appliance: 30 entities** (was 20)

### Breaking Changes

None - This release is fully backward compatible. All new features are optional and disabled by default.

### Migration Notes

- Existing configurations will continue to work without changes
- No database migration required
- Monthly stats now include `total_energy` field (automatically initialized to 0.0)
- New configuration options available in Options Flow

### Known Limitations

- Anomaly detection requires at least 3 completed cycles for meaningful analysis
- Auto-shutdown requires a switch/plug entity that can be controlled by Home Assistant
- Scheduling does not support multiple time windows (only one per day)
- Custom cards still require manual build (run `npm install && npm run build` in `/www/smart-appliance-cards/`)

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

