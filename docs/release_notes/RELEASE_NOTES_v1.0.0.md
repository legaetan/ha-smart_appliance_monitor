# Release Notes - Smart Appliance Monitor v1.0.0

## 🎉 Major Release: Integrated Dashboard System

**Release Date**: October 23, 2025

This is a **major milestone** release introducing a complete integrated dashboard management system for Smart Appliance Monitor. Version 1.0.0 brings a revolutionary way to visualize and manage your appliances with automated dashboard generation and Energy Dashboard-style graphs.

---

## 🌟 Highlights

### Integrated Dashboard System

Smart Appliance Monitor now includes a **complete dashboard management system** that eliminates manual YAML copy-pasting:

- **Automated Dashboard Generation**: Create beautiful dashboards with a single service call
- **Configuration Panel**: Dedicated sidebar panel "Smart Appliances Config" for dashboard management
- **YAML Mode**: User-editable YAML files for maximum flexibility
- **Energy Dashboard Integration**: Modern graphs inspired by Home Assistant's native Energy Dashboard

### Key Benefits

✅ **No More Manual Configuration** - Dashboard YAML generated automatically  
✅ **Energy Dashboard Style** - Beautiful consumption graphs and donut charts  
✅ **Real Entity Integration** - Uses your actual configured power/energy sensors  
✅ **Multi-Tab Interface** - Overview + individual tabs for each appliance  
✅ **Configuration UI** - Interactive panel for dashboard customization  

---

## 📋 What's New

### Dashboard Features

#### 1. **Automated Dashboard Generation**
Generate complete dashboard YAML with one service call:

```yaml
service: smart_appliance_monitor.generate_dashboard_yaml
data:
  output_path: /config/dashboards/smart-appliances.yaml  # Optional
```

The service creates a fully configured multi-tab dashboard with:
- Overview tab with energy graphs and real-time monitoring
- Individual tabs for each configured appliance
- All entities automatically discovered and validated

#### 2. **Configuration Panel**
Access via **"Smart Appliances Config"** in your Home Assistant sidebar:
- View all configured appliances
- Generate/regenerate dashboard
- View configuration instructions
- Manage dashboard settings

#### 3. **Energy Dashboard Style Graphs**

**Overview Tab includes:**
- **Daily Energy Summary**: Total kWh and cost for today
- **7-Day Energy Graph**: Column chart showing consumption trends
- **Energy Distribution**: Donut chart showing which appliances consume most
- **Real-Time Monitoring**: Live power consumption for all appliances
- **Top Consumers**: Dynamic ranking by energy usage

#### 4. **Individual Appliance Tabs**
Each appliance gets its own detailed view with:
- Current state and cycle/session monitoring
- Gauge for cycle duration
- Energy consumption statistics
- Power consumption graphs
- Control switches and buttons
- Notifications configuration

### New Services

#### `smart_appliance_monitor.generate_dashboard_yaml`
Generate or update the dashboard YAML file.

**Parameters:**
- `output_path` (optional): Custom path for YAML output

**Example:**
```yaml
service: smart_appliance_monitor.generate_dashboard_yaml
data:
  output_path: /config/dashboards/my-appliances.yaml
```

#### `smart_appliance_monitor.configure_dashboard`
Update dashboard configuration programmatically.

**Parameters:**
- `global_settings`: Dashboard-wide settings
- `overview_sections`: Customize overview sections
- `appliance_views`: Per-appliance view settings

#### `smart_appliance_monitor.toggle_view`
Enable or disable individual appliance views.

**Parameters:**
- `appliance_id`: Appliance identifier
- `enabled`: true/false

---

## 🛠️ Technical Improvements

### Direct Entity Integration
- **No Entity ID Guessing**: Uses actual configured `power_sensor` and `energy_sensor`
- **Entity Registry Scan**: SAM-generated entities discovered automatically
- **Real-Time Validation**: Entities verified to exist before adding to dashboard
- **Simplified Logic**: Removed complex entity mapping and guessing algorithms

### Architecture Changes
- **New Module**: `dashboard_manager.py` (858 lines) - Complete dashboard lifecycle
- **Configuration Storage**: `dashboard_config.py` - Persistent dashboard settings
- **Panel Registration**: `panel.py` - Sidebar panel integration
- **Frontend Components**: Web Components for interactive configuration UI
- **Template System Removed**: All cards now built programmatically in Python

### Energy Dashboard Integration
New helper methods in `energy_dashboard.py`:
- `async_get_hourly_breakdown()` - Hourly energy data for graphs
- `async_get_device_distribution()` - Distribution with percentages
- `async_get_device_ranking()` - Ranking by consumption

---

## 📚 Installation & Setup

### Step 1: Update Integration
Update Smart Appliance Monitor to v1.0.0 via HACS or manual installation.

### Step 2: Restart Home Assistant
A restart is required to load the new dashboard system.

### Step 3: Generate Dashboard

**Option A: Via Configuration Panel**
1. Go to Settings → Devices & Services
2. Click "Smart Appliances Config" in sidebar
3. Click "Generate Dashboard" button
4. Follow the instructions displayed

**Option B: Via Service Call**
```yaml
service: smart_appliance_monitor.generate_dashboard_yaml
```

### Step 4: Add to configuration.yaml
Add the generated dashboard to your `configuration.yaml`:

```yaml
lovelace:
  mode: storage  # Or yaml if you prefer
  dashboards:
    smart-appliances:
      mode: yaml
      title: "Smart Appliances"
      icon: mdi:lightning-bolt
      filename: dashboards/smart-appliances.yaml
```

### Step 5: Restart Home Assistant
One more restart to load the dashboard configuration.

### Step 6: Access Dashboard
Your new dashboard will appear in the sidebar as "Smart Appliances"!

---

## 🔄 Migration Guide

### From v0.9.x
- **No Breaking Changes**: All existing features continue to work
- **Dashboard is Optional**: You can keep using your current setup
- **Seamless Upgrade**: Simply update and follow setup steps above

### What Happens to Old Templates?
- Old YAML templates in `dashboards/templates/` have been removed
- If you had custom templates, back them up before upgrading
- The new system generates everything programmatically

---

## 📖 Documentation

### New Documentation Files
- **`docs/DASHBOARD_YAML_MODE.md`**: Complete guide for YAML mode dashboard
- **`docs/TESTING_DASHBOARD.md`**: Testing guide for dashboard features
- **`README_DASHBOARD.md`**: Quick start guide

### Updated Documentation
- **`README.md`**: Added Dashboard System section
- **`CHANGELOG.md`**: Complete changelog for v1.0.0

---

## 🐛 Bug Fixes

- Fixed "Entité non trouvée" (Entity not found) issues in overview tab
- Corrected entity ID resolution to use actual configured sensors
- Fixed entity mapping for appliances with accented characters (e.g., "Sèche-Linge")
- Improved error handling in dashboard generation

---

## ⚠️ Known Issues

1. **ApexCharts Requirement**: Advanced energy graphs require `apexcharts-card` HACS frontend
   - **Workaround**: Fallback to standard `history-graph` if not installed
   
2. **Manual Configuration Step**: Users must add dashboard to `configuration.yaml`
   - **Why**: HA security restrictions prevent automatic `configuration.yaml` modification
   
3. **Restart Required**: Dashboard changes require HA restart
   - **Why**: YAML mode dashboards are loaded at startup

---

## 🔮 Future Enhancements

Planned for future releases:
- **Inline Dashboard Display**: Show dashboard directly in configuration panel
- **Popup Configuration**: Configure dashboard settings via dialogs
- **Theme Customization**: Choose color schemes and themes
- **Layout Options**: Customize card arrangement and sizes
- **Advanced Filters**: Filter appliances by type, status, consumption

---

## 📊 Statistics

### Code Changes
- **New Files**: 5 files (dashboard_manager.py, dashboard_config.py, panel.py, 2 frontend files)
- **Modified Files**: 7 files (__init__.py, energy_dashboard.py, services.yaml, strings.json, translations/fr.json)
- **Deleted Files**: 14 template YAML files
- **Lines of Code**: +1,500 lines added

### Features
- **3 New Services**: Dashboard generation and configuration
- **5 New Graphs**: Energy consumption visualizations
- **1 New Panel**: Configuration UI in sidebar
- **∞ Possibilities**: Fully customizable dashboard system

---

## 🙏 Acknowledgments

Special thanks to the Home Assistant community for feedback and testing!

---

## 📦 Download

- **GitHub Release**: [v1.0.0](https://github.com/legaetan/ha-smart_appliance_monitor/releases/tag/v1.0.0)
- **HACS**: Update via HACS custom repositories

---

## 📞 Support

- **Documentation**: [GitHub Wiki](https://github.com/legaetan/ha-smart_appliance_monitor/wiki)
- **Issues**: [GitHub Issues](https://github.com/legaetan/ha-smart_appliance_monitor/issues)
- **Discussions**: [GitHub Discussions](https://github.com/legaetan/ha-smart_appliance_monitor/discussions)

---

**Enjoy your new integrated dashboard system! 🎉**

