# Installation Guide

This guide covers all installation methods for Smart Appliance Monitor.

## Requirements

### System Requirements
- Home Assistant 2024.1 or higher
- Smart plug with power monitoring capabilities
- Energy sensor on the smart plug

### Supported Smart Plugs
Any smart plug that provides the following entities in Home Assistant:
- Power sensor (in Watts)
- Energy sensor (in kWh or Wh)

**Examples:**
- Sonoff S31
- Shelly Plug S
- TP-Link/Kasa smart plugs
- Zigbee smart plugs (via Zigbee2MQTT or ZHA)
- Z-Wave smart plugs

## Installation Methods

### Method 1: Manual Installation

#### Step 1: Download

Download the latest release from [GitHub Releases](https://github.com/legaetan/ha-smart_appliance_monitor/releases).

#### Step 2: Extract Files

Extract the `smart_appliance_monitor` folder from the zip file.

#### Step 3: Copy to Home Assistant

Copy the entire `smart_appliance_monitor` folder to your Home Assistant `custom_components` directory:

```
/config/custom_components/smart_appliance_monitor/
```

Your directory structure should look like:

```
config/
├── custom_components/
│   └── smart_appliance_monitor/
│       ├── __init__.py
│       ├── binary_sensor.py
│       ├── button.py
│       ├── config_flow.py
│       ├── const.py
│       ├── coordinator.py
│       ├── device.py
│       ├── entity.py
│       ├── manifest.json
│       ├── notify.py
│       ├── sensor.py
│       ├── services.yaml
│       ├── state_machine.py
│       ├── strings.json
│       ├── switch.py
│       └── translations/
│           └── fr.json
```

#### Step 4: Restart Home Assistant

Restart Home Assistant to load the integration:
- Settings → System → Restart
- Or use CLI: `ha core restart`

### Method 2: HACS Installation (Coming Soon)

The integration will be available through HACS custom repositories.

Once available:

1. Open HACS in Home Assistant
2. Go to "Integrations"
3. Click the three dots in the top right
4. Select "Custom repositories"
5. Add repository URL: `https://github.com/legaetan/ha-smart_appliance_monitor`
6. Category: Integration
7. Click "Add"
8. Click "Install" on Smart Appliance Monitor
9. Restart Home Assistant

### Method 3: Git Clone (Development)

For developers or advanced users who want to track the latest changes:

```bash
cd /config/custom_components
git clone https://github.com/legaetan/ha-smart_appliance_monitor.git smart_appliance_monitor
```

To update:

```bash
cd /config/custom_components/smart_appliance_monitor
git pull
```

Restart Home Assistant after updating.

## Verification

### Check Installation

After restarting Home Assistant:

1. Go to **Settings** → **Devices & Services**
2. Click **Add Integration** (bottom right)
3. Search for "Smart Appliance Monitor"
4. If you see it in the list, installation was successful

### Check Logs

If the integration doesn't appear, check logs:

```bash
tail -f /config/home-assistant.log | grep smart_appliance_monitor
```

Look for any error messages related to the integration.

### Common Installation Issues

#### Integration Not Found

**Problem**: Integration doesn't appear in the add integration list.

**Solutions:**
1. Verify folder structure is correct
2. Ensure all files were copied
3. Check file permissions
4. Restart Home Assistant again
5. Clear browser cache

#### Import Errors

**Problem**: Logs show import errors.

**Solutions:**
1. Verify Home Assistant version (2024.1+)
2. Check all required files are present
3. Ensure no file corruption during copy

## Next Steps

Once installed, proceed to:
- [Configuration Guide](configuration.md) - Set up your first appliance
- [Features Guide](features.md) - Learn about available features

## Uninstallation

### Remove Integration Instances

1. Go to **Settings** → **Devices & Services**
2. Find **Smart Appliance Monitor**
3. Click the three dots on each instance
4. Select **Delete**
5. Confirm deletion

### Remove Files

After removing all instances:

```bash
rm -rf /config/custom_components/smart_appliance_monitor
```

Restart Home Assistant.

## Upgrading

### Manual Upgrade

1. Download the new release
2. Stop Home Assistant (optional, but safer)
3. Backup your `custom_components/smart_appliance_monitor` folder
4. Replace with new files
5. Restart Home Assistant

### HACS Upgrade (When Available)

1. Open HACS
2. Go to Integrations
3. Find Smart Appliance Monitor
4. Click "Update" if available
5. Restart Home Assistant

**Note**: Configuration and statistics are preserved during upgrades.

## Troubleshooting

### Clean Reinstall

If you encounter persistent issues:

1. Remove all integration instances (Settings → Devices & Services)
2. Delete the `smart_appliance_monitor` folder
3. Restart Home Assistant
4. Reinstall using one of the methods above
5. Add integration again

### Enable Debug Logging

Add to `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.smart_appliance_monitor: debug
```

Restart Home Assistant and check logs for detailed information.

### Get Help

If problems persist:
- Check [GitHub Issues](https://github.com/legaetan/ha-smart_appliance_monitor/issues)
- Open a new issue with:
  - Home Assistant version
  - Integration version
  - Relevant log excerpts
  - Description of the problem

## Requirements File

For developers, dependencies are listed in `requirements-dev.txt`:

```
pytest>=7.4.0
pytest-cov>=4.1.0
pytest-homeassistant-custom-component>=0.13.0
ruff>=0.0.292
black>=23.9.1
mypy>=1.5.1
```

Install with:

```bash
pip install -r requirements-dev.txt
```

