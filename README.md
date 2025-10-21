# Smart Appliance Monitor

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> Transform any smart plug into an intelligent appliance monitoring system for Home Assistant.

## Overview

Smart Appliance Monitor is a Home Assistant custom integration that automatically detects and tracks appliance cycles (washing machines, dishwashers, dryers, water heaters, etc.) using power consumption data from smart plugs.

## Features

### Core Features
- **Automatic Cycle Detection** - Intelligent start/stop detection with configurable thresholds
- **11 Appliance Types** - Optimized profiles for washing machines, dishwashers, dryers, ovens, water heaters, coffee makers, monitors, NAS, 3D printers, VMC, and more
- **Smart Terminology** - Adaptive naming (cycle/session) based on appliance type for better UX
- **Comprehensive Statistics** - Track duration, energy consumption, and cost per cycle/session
- **Unplugged Detection** - Automatic detection when appliance is disconnected or powered off
- **Advanced Notifications** - Multi-service support (Mobile App, Telegram, Persistent, Custom)
- **Granular Notification Control** - Enable/disable by type (9 notification types available)
- **Dynamic Pricing** - Support for variable electricity rates via Home Assistant entities
- **Flexible Reconfiguration** - Modify all settings without losing historical data
- **30 Entities per Appliance** - Complete monitoring suite with sensors, binary sensors, switches
- **Custom Services** - Programmatic control via Home Assistant services (7 services available)
- **Bilingual** - Full interface in English and French

### Advanced Features (v0.5.0+)
- **Auto-Shutdown** - Automatically turn off appliances after inactivity to save energy
- **Energy Management** - Set limits and budgets for energy consumption (cycle, daily, monthly)
- **Scheduling** - Define allowed usage hours and blocked days for optimal energy usage
- **Anomaly Detection** - AI-powered detection of unusual consumption patterns
- **Data Export** - Export statistics to CSV or JSON for external analysis
- **Energy Dashboard Integration** - Native support for Home Assistant Energy Dashboard
- **State Persistence** (v0.5.1) - Cycles and statistics are preserved across Home Assistant restarts

### Energy Dashboard Suite (v0.6.0+) ⚡ *NEW*
- **Automatic Sync Detection** - Check if devices are configured in Energy Dashboard on startup
- **Energy Storage Reader** - Read-only access to `.storage/energy` for advanced analytics
- **Sync Services** - Comprehensive sync checking and configuration export
- **Custom Energy Dashboard** - Advanced energy analytics beyond native HA capabilities
- **Period Comparisons** - Compare energy usage across custom time periods
- **Top Consumers** - Identify and track your highest energy consumers
- **Efficiency Scoring** - Get device efficiency scores and optimization recommendations

## Supported Appliances

Works with any appliance connected via a smart plug with power monitoring:

- Washing machines
- Dishwashers
- Dryers
- Water heaters
- Ovens
- Coffee makers
- Screens/Monitors
- NAS
- 3D Printers
- VMC (Ventilation)
- And more!

## Quick Start

### Installation

#### Manual Installation

1. Copy the `custom_components/smart_appliance_monitor` folder to your Home Assistant `config/custom_components` directory
2. Restart Home Assistant
3. Add the integration via Settings → Devices & Services → Add Integration
4. Search for "Smart Appliance Monitor"

#### HACS Installation (Coming Soon)

Will be available through HACS custom repositories.

### Basic Configuration

1. **Add Integration**: Settings → Devices & Services → Add Integration → Smart Appliance Monitor
   - Dashboard templates are automatically installed with the integration
2. **Configure Appliance**:
   - Name: "Washing Machine"
   - Type: Select from dropdown (washing_machine, dishwasher, etc.)
   - Power Sensor: Select your smart plug's power sensor
   - Energy Sensor: Select your smart plug's energy sensor
   - Price: Enter fixed price or select an entity for dynamic pricing
3. **Adjust Settings** (Optional): Click "Configure" → "Advanced Configuration (Multi-step)" to fine-tune thresholds
   - **Step 1**: Detection thresholds (power levels)
   - **Step 2**: Detection delays & alerts (in minutes/hours)
   - **Step 3**: Notification settings
   - **Step 4**: Expert settings (optional, activated via toggle)

### Appliance Type Profiles

The integration automatically applies optimized thresholds based on appliance type:

| Appliance Type | Start Threshold | Stop Threshold | Alert Duration |
|----------------|-----------------|----------------|----------------|
| Water Heater   | 1000W           | 50W            | 4h             |
| Oven/Dryer     | 100W            | 10W            | 2h             |
| Dishwasher     | 20W             | 5W             | 3h             |
| Washing Machine| 10W             | 5W             | 3h             |
| Coffee Maker   | 50W             | 5W             | 30min          |
| Monitor        | 30W             | 5W             | 8h             |
| NAS            | 50W             | 20W            | 6h             |
| 3D Printer     | 50W             | 10W            | 24h            |
| VMC            | 20W             | 10W            | 2h             |

## Documentation

### User Guides (GitHub Wiki)

Complete documentation available on the GitHub Wiki:
- [Installation Guide](https://github.com/legaetan/ha-smart_appliance_monitor/wiki/Installation) - Detailed installation instructions
- [Configuration Guide](https://github.com/legaetan/ha-smart_appliance_monitor/wiki/Configuration) - Complete configuration reference
- [Reconfiguration Guide](https://github.com/legaetan/ha-smart_appliance_monitor/wiki/Reconfiguration) - How to modify settings without data loss
- [Features Guide](https://github.com/legaetan/ha-smart_appliance_monitor/wiki/Features) - Comprehensive feature documentation

Or browse locally: [docs/wiki-github/](docs/wiki-github/)

### Developer Documentation

- [Contributing Guide](CONTRIBUTING.md) - How to contribute to the project
- [Architecture](ARCHITECTURE.md) - Technical architecture and component overview
- [Changelog](CHANGELOG.md) - Version history and changes
- [Release Notes](docs/release_notes/) - Detailed release notes for each version
- [State Persistence](docs/PERSISTENCE.md) - Technical documentation on cycle persistence system (v0.5.1+)

## Entities Created

For each configured appliance, the integration creates **up to 30 entities**:

### Sensors (13)
- **State** - Current appliance state (idle/running/finished)
- **Cycle/Session Duration** - Duration of current cycle/session (adaptive naming)
- **Cycle/Session Energy** - Energy consumed in current cycle/session
- **Cycle/Session Cost** - Cost of current cycle/session
- **Last Cycle/Session Duration** - Duration of last completed cycle/session
- **Last Cycle/Session Energy** - Energy of last completed cycle/session
- **Last Cycle/Session Cost** - Cost of last completed cycle/session
- **Daily Cycles/Sessions** - Number of cycles/sessions today (adaptive naming)
- **Daily Cost** - Total cost today
- **Daily Energy** - Total energy consumed today (kWh) ⚡ *NEW v0.5.0*
- **Monthly Cost** - Total cost this month
- **Monthly Energy** - Total energy consumed this month (kWh) ⚡ *NEW v0.5.0*
- **Anomaly Score** - Real-time anomaly score (0-100%) *NEW v0.5.0 - Optional*

### Binary Sensors (7)
- **Running** - Is appliance currently running
- **Duration Alert** - Has cycle exceeded expected duration (optional)
- **Unplugged** - Is appliance disconnected or powered off
- **Energy Limit Exceeded** - Has any energy limit been exceeded *NEW v0.5.0 - Optional*
- **Budget Exceeded** - Has monthly budget been exceeded *NEW v0.5.0 - Optional*
- **Usage Allowed** - Is current usage within allowed schedule *NEW v0.5.0 - Optional*
- **Anomaly Detected** - Is an anomaly currently detected *NEW v0.5.0 - Optional*

### Switches (9)
- **Monitoring** - Enable/disable cycle monitoring
- **Notifications** - Enable/disable all notifications
- **Notify Cycle Started** - Enable/disable start notifications
- **Notify Cycle Finished** - Enable/disable completion notifications
- **Notify Alert Duration** - Enable/disable duration alerts
- **Notify Unplugged** - Enable/disable unplugged alerts
- **Auto Shutdown** - Enable/disable automatic shutdown *NEW v0.5.0 - Optional*
- **Energy Limits** - Enable/disable energy limits monitoring *NEW v0.5.0 - Optional*
- **Scheduling** - Enable/disable usage scheduling *NEW v0.5.0 - Optional*

### Buttons (1)
- **Reset Statistics** - Clear all statistics and start fresh

## Services

### Core Services

#### `smart_appliance_monitor.start_cycle`
Manually start a cycle (useful for testing or manual tracking).

#### `smart_appliance_monitor.stop_monitoring`
Stop monitoring for a specific appliance.

#### `smart_appliance_monitor.reset_statistics`
Reset all statistics for a specific appliance.

#### `smart_appliance_monitor.generate_dashboard_yaml`
Generate optimized dashboard YAML for the appliance.

### Data Export Services

#### `smart_appliance_monitor.export_to_csv`
Export appliance data to CSV format. Optionally save to file.

#### `smart_appliance_monitor.export_to_json`
Export appliance data to JSON format. Optionally save to file.

### Energy Management Services

#### `smart_appliance_monitor.force_shutdown`
Manually trigger auto-shutdown for testing (requires auto-shutdown to be enabled).

### Energy Dashboard Services ⚡ *NEW v0.6.0*

#### `smart_appliance_monitor.sync_with_energy_dashboard`
Check synchronization status between SAM devices and Home Assistant Energy Dashboard. Generates a detailed report showing which devices are synced, which are missing, and provides setup instructions.

```yaml
# Sync all devices
service: smart_appliance_monitor.sync_with_energy_dashboard

# Sync specific device
service: smart_appliance_monitor.sync_with_energy_dashboard
data:
  entity_id: sensor.washing_machine_state
```

#### `smart_appliance_monitor.export_energy_config`
Export Energy Dashboard configuration for a specific device. Provides JSON configuration and step-by-step instructions to add the device to Energy Dashboard manually.

```yaml
service: smart_appliance_monitor.export_energy_config
data:
  entity_id: sensor.dishwasher_state
```

#### `smart_appliance_monitor.get_energy_data`
Retrieve aggregated energy data for SAM devices with period filtering and device breakdown. Perfect for custom dashboards and data analysis.

```yaml
service: smart_appliance_monitor.get_energy_data
data:
  period_start: "2025-10-21T00:00:00"
  period_end: "2025-10-21T23:59:59"
  devices:
    - "Washing Machine"
    - "Dishwasher"
```

## Dynamic Pricing

Configure variable electricity rates:

```yaml
# configuration.yaml
input_number:
  electricity_price:
    name: Current Electricity Price
    min: 0
    max: 1
    step: 0.0001
    unit_of_measurement: "€/kWh"

# Update price based on time or tariff
automation:
  - alias: "Update Electricity Price"
    trigger:
      - platform: time
        at: "07:00:00"  # Peak hours start
      - platform: time
        at: "22:00:00"  # Off-peak hours start
    action:
      - service: input_number.set_value
        target:
          entity_id: input_number.electricity_price
        data:
          value: >
            {% if now().hour >= 22 or now().hour < 7 %}
              0.1821  # Off-peak rate
            {% else %}
              0.2516  # Peak rate
            {% endif %}
```

Then select `input_number.electricity_price` when configuring the integration.

## Recent Improvements

### v0.6.0 (Latest) ✅ *NEW*
- ✅ **Energy Dashboard Integration Suite** - Comprehensive integration with HA Energy Dashboard
  - Automatic sync detection on appliance startup
  - Read-only access to `.storage/energy` file for safe analytics
  - Sync status checking for all devices
  - Configuration export with step-by-step instructions
  - Parent sensor suggestions for hierarchical organization
- ✅ **Advanced Energy Analytics** - Custom energy dashboard backend
  - Period data analysis (today, yesterday, custom periods)
  - Device breakdown with consumption percentages
  - Period comparisons (today vs yesterday)
  - Top consumers identification and ranking
  - Energy efficiency scoring system
  - Dashboard summary with key metrics
- ✅ **New Services** - Three powerful new services
  - `sync_with_energy_dashboard` - Check sync status
  - `export_energy_config` - Export JSON configuration
  - `get_energy_data` - Retrieve aggregated energy data
- ✅ **Custom Energy Dashboard Template** - Ready-to-use dashboard YAML
  - Summary cards with totals and comparisons
  - Device breakdown visualizations
  - Energy timeline and trends
  - Top consumers ranking
  - Cost analysis and efficiency scores
  - Quick actions and integration status
- ✅ **Complete Documentation** - New Energy Dashboard guide

### v0.5.1 ✅
- ✅ **State Persistence** - Cycles and statistics preserved across Home Assistant restarts
  - No more lost data when restarting HA during a cycle
  - Automatic save/restore of cycle state, statistics, and history
  - Intelligent validation (daily/monthly stats reset when obsolete)

### v0.5.0 ✅
- ✅ **Energy Dashboard integration** - Native support with proper sensor configuration
- ✅ **Data export** - CSV and JSON export with complete statistics
- ✅ **Auto-shutdown** - Automatic power off after inactivity
- ✅ **Energy Management** - Limits and budgets for consumption control
- ✅ **Usage Scheduling** - Time-based usage control
- ✅ **Anomaly Detection** - Basic pattern-based detection

## Future Features & Roadmap

See [IDEAS.md](docs/IDEAS.md) for planned features, enhancements, and long-term roadmap.

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- [Report a Bug](https://github.com/legaetan/ha-smart_appliance_monitor/issues)
- [Request a Feature](https://github.com/legaetan/ha-smart_appliance_monitor/issues)
- [Discussions](https://github.com/legaetan/ha-smart_appliance_monitor/discussions)

## Acknowledgments

- Home Assistant community
- HACS maintainers
- All contributors and testers

---

**If you find this project useful, please give it a star on GitHub!**
