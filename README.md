# Smart Appliance Monitor

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> Transform any smart plug into an intelligent appliance monitoring system for Home Assistant.

## Overview

Smart Appliance Monitor is a Home Assistant custom integration that automatically detects and tracks appliance cycles (washing machines, dishwashers, dryers, water heaters, etc.) using power consumption data from smart plugs.

## Features

- **Automatic Cycle Detection** - Intelligent start/stop detection with configurable thresholds
- **11 Appliance Types** - Optimized profiles for washing machines, dishwashers, dryers, ovens, water heaters, coffee makers, monitors, NAS, 3D printers, VMC, and more
- **Smart Terminology** - Adaptive naming (cycle/session) based on appliance type for better UX
- **Comprehensive Statistics** - Track duration, energy consumption, and cost per cycle/session
- **Unplugged Detection** - Automatic detection when appliance is disconnected or powered off
- **Advanced Notifications** - Multi-service support (Mobile App, Telegram, Persistent, Custom)
- **Granular Notification Control** - Enable/disable by type (started, finished, alert, unplugged)
- **Dynamic Pricing** - Support for variable electricity rates via Home Assistant entities
- **Flexible Reconfiguration** - Modify all settings without losing historical data
- **19 Entities per Appliance** - Sensors, binary sensors, switches for complete monitoring
- **Custom Services** - Programmatic control via Home Assistant services
- **Bilingual** - Full interface in English and French

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
2. **Configure Appliance**:
   - Name: "Washing Machine"
   - Type: Select from dropdown (washing_machine, dishwasher, etc.)
   - Power Sensor: Select your smart plug's power sensor
   - Energy Sensor: Select your smart plug's energy sensor
   - Price: Enter fixed price or select an entity for dynamic pricing
3. **Adjust Settings** (Optional): Click "Configure" → "Advanced Configuration" to fine-tune thresholds

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

## Entities Created

For each configured appliance, the integration creates **19 entities**:

### Sensors (10)
- **State** - Current appliance state (idle/running/finished)
- **Cycle/Session Duration** - Duration of current cycle/session (adaptive naming)
- **Cycle/Session Energy** - Energy consumed in current cycle/session
- **Cycle/Session Cost** - Cost of current cycle/session
- **Last Cycle/Session Duration** - Duration of last completed cycle/session
- **Last Cycle/Session Energy** - Energy of last completed cycle/session
- **Last Cycle/Session Cost** - Cost of last completed cycle/session
- **Daily Cycles/Sessions** - Number of cycles/sessions today (adaptive naming)
- **Daily Cost** - Total cost today
- **Monthly Cost** - Total cost this month

### Binary Sensors (3)
- **Running** - Is appliance currently running
- **Duration Alert** - Has cycle exceeded expected duration (optional)
- **Unplugged** - Is appliance disconnected or powered off

### Switches (6)
- **Monitoring** - Enable/disable cycle monitoring
- **Notifications** - Enable/disable all notifications
- **Notify Cycle Started** - Enable/disable start notifications
- **Notify Cycle Finished** - Enable/disable completion notifications
- **Notify Alert Duration** - Enable/disable duration alerts
- **Notify Unplugged** - Enable/disable unplugged alerts

### Buttons (1)
- **Reset Statistics** - Clear all statistics and start fresh

## Services

### `smart_appliance_monitor.start_cycle`
Manually start a cycle (useful for testing or manual tracking).

### `smart_appliance_monitor.stop_monitoring`
Stop monitoring for a specific appliance.

### `smart_appliance_monitor.reset_statistics`
Reset all statistics for a specific appliance.

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
