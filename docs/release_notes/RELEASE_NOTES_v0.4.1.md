# Smart Appliance Monitor v0.4.1 - Bundled Dashboard Templates

**Release Date**: October 20, 2025

## 🎉 Template Installation Simplified

Version **0.4.1** fixes a critical issue where dashboard generation failed due to missing templates. Templates are now **bundled with the integration** and work out-of-the-box!

## ✅ What's Fixed

### Dashboard Generation Error
**Before v0.4.1:**
- ❌ `generate_dashboard_yaml` service failed with "No such file or directory"
- ❌ Users had to manually create `/config/dashboards/templates/` folder
- ❌ Templates had to be manually copied
- ❌ Error-prone installation process

**After v0.4.1:** ✅
- ✅ Templates bundled in `/custom_components/smart_appliance_monitor/dashboards/`
- ✅ Dashboard generation works immediately after installation
- ✅ Zero configuration required
- ✅ Templates "just work"

## 🚀 New Features

### Bundled Dashboard Templates
7 templates now included in the integration:
- `washing_machine.yaml` - Washing machine dashboard
- `dishwasher.yaml` - Dishwasher dashboard
- `vmc.yaml` - VMC/ventilation dashboard
- `monitor.yaml` - PC monitor dashboard
- `printer_3d.yaml` - 3D printer dashboard
- `nas.yaml` - NAS dashboard
- `generic.yaml` - Generic appliance dashboard

### Smart Template Priority
The integration now checks templates in this order:
1. **User custom templates** - `/config/dashboards/templates/` (optional)
2. **Bundled templates** - `/custom_components/smart_appliance_monitor/dashboards/`
3. **Generic fallback** - Always available

This allows:
- ✅ Immediate use of bundled templates
- ✅ Customization by placing templates in `/config/dashboards/templates/`
- ✅ No risk of breaking on updates

## 📦 Installation

### Via HACS
1. Update Smart Appliance Monitor to v0.4.1
2. Restart Home Assistant
3. Dashboard generation now works!

### Testing
Try generating a dashboard:
```yaml
service: smart_appliance_monitor.generate_dashboard_yaml
data:
  entity_id: sensor.washing_machine_state
```

## 🔧 Technical Details

**Files Added:**
- 7 dashboard templates in `/custom_components/smart_appliance_monitor/dashboards/`

**Files Modified:**
- `__init__.py` - Updated template resolution logic with priority system

**Breaking Changes:** None

**Migration Notes:**
- Existing custom templates in `/config/dashboards/templates/` continue to work
- Bundled templates serve as fallback
- Fully backward compatible

## 📚 Advanced Usage

### Customizing Templates
Want to customize a template?

1. Copy it to `/config/dashboards/templates/`:
   ```bash
   cp custom_components/smart_appliance_monitor/dashboards/washing_machine.yaml \
      config/dashboards/templates/washing_machine.yaml
   ```

2. Edit your copy - it will take priority over the bundled version

3. Your customizations persist across updates

---

**Version**: 0.4.1  
**Date**: October 20, 2025  
**Download**: [smart_appliance_monitor-v0.4.1.zip](https://github.com/legaetan/ha-smart_appliance_monitor/releases/download/v0.4.1/smart_appliance_monitor-v0.4.1.zip)

