# Dashboard YAML Mode

## Overview

Starting from version 0.10.0, the Smart Appliance Monitor dashboard uses **YAML mode** instead of direct storage manipulation. This provides better transparency, portability, and control over your dashboard configuration.

## How it Works

1. **Generate the Dashboard**: Call the `smart_appliance_monitor.generate_dashboard_yaml` service
2. **Configure Home Assistant**: Add dashboard configuration to your `configuration.yaml`
3. **Restart**: Restart Home Assistant to load the dashboard
4. **Enjoy**: Access your dashboard from the sidebar with the ⚡ icon

## Step-by-Step Setup

### 1. Generate the Dashboard YAML

Go to **Developer Tools** → **Services** and call:

```yaml
service: smart_appliance_monitor.generate_dashboard_yaml
data: {}
```

This creates the file: `config/dashboards/smart-appliances.yaml`

### 2. Add Configuration

Edit your `configuration.yaml` and add:

```yaml
lovelace:
  mode: storage
  dashboards:
    smart-appliances:
      mode: yaml
      title: "Smart Appliances"
      icon: mdi:lightning-bolt
      filename: dashboards/smart-appliances.yaml
```

**Note**: If you already have a `lovelace:` section, just add the `dashboards:` part.

### 3. Verify and Restart

1. Go to **Developer Tools** → **YAML** → **Check Configuration**
2. If valid, restart Home Assistant
3. The dashboard will appear in your sidebar!

## Custom Output Path

You can specify a custom location for the YAML file:

```yaml
service: smart_appliance_monitor.generate_dashboard_yaml
data:
  output_path: "/config/my-custom-location/sam-dashboard.yaml"
```

Don't forget to update the `filename` in `configuration.yaml` accordingly.

## Updating the Dashboard

Whenever you:
- Add or remove an appliance
- Change configuration via the "Smart Appliances Config" panel
- Want to refresh the dashboard

Just call `smart_appliance_monitor.generate_dashboard_yaml` again and restart Home Assistant.

## Advantages of YAML Mode

✅ **Transparent**: You can see and edit the dashboard configuration
✅ **Versionable**: Commit to Git for backup and history
✅ **Portable**: Easy to copy to other Home Assistant instances
✅ **Debuggable**: YAML errors are clear in logs
✅ **Flexible**: Manual customization is possible
✅ **Standard**: Uses Home Assistant's native dashboard approach

## Migration from Storage Mode

If you used a previous version (v0.9.x or earlier) with storage mode:

1. Call `smart_appliance_monitor.generate_dashboard_yaml`
2. Add configuration to `configuration.yaml`
3. Restart Home Assistant
4. (Optional) Delete old storage files:
   - `.storage/lovelace.smart-appliances`
   - Remove entry from `.storage/lovelace_dashboards`

## Customization

### Dashboard Title and Icon

Edit `configuration.yaml`:

```yaml
lovelace:
  dashboards:
    smart-appliances:
      title: "My Custom Title"  # Change this
      icon: mdi:flash           # Change this
      # ... rest of config
```

### Dashboard Content

Use the **Smart Appliances Config** panel (sidebar) to:
- Enable/disable appliance tabs
- Choose colors and templates
- Toggle sections (statistics, controls, etc.)
- Configure custom cards usage

After making changes, regenerate the YAML file.

### Manual Editing

You can manually edit `dashboards/smart-appliances.yaml` for advanced customizations. However, note that regenerating the dashboard will overwrite your manual changes.

## Troubleshooting

### Dashboard not appearing

1. Check YAML syntax: **Developer Tools** → **YAML** → **Check Configuration**
2. Verify the file exists: `config/dashboards/smart-appliances.yaml`
3. Check `configuration.yaml` has the correct `filename` path
4. Restart Home Assistant completely

### Dashboard is empty or shows errors

1. Check Home Assistant logs for YAML parsing errors
2. Regenerate the dashboard: `smart_appliance_monitor.generate_dashboard_yaml`
3. Verify all entities exist (check if appliances are configured)

### Changes not reflecting

1. After regenerating, you **must restart** Home Assistant
2. Clear browser cache (Ctrl+F5 or Cmd+Shift+R)
3. YAML dashboards don't auto-reload like storage dashboards

## FAQ

**Q: Can I have both storage and YAML dashboards?**
A: Yes! This configuration is compatible with other dashboards in storage mode.

**Q: Will my dashboard update automatically when I add appliances?**
A: No, you need to call `generate_dashboard_yaml` again and restart HA.

**Q: Can I edit the YAML file directly?**
A: Yes, but your changes will be overwritten when you regenerate the dashboard.

**Q: Do I need to restart HA every time?**
A: Yes, YAML dashboards require a restart to reload changes.

## See Also

- [Dashboard Configuration Guide](../README.md#dashboard)
- [Configuration Panel Documentation](Configuration.md)
- [Customization Examples](Dashboards.md)

