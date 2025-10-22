# Smart Appliance Monitor v0.6.0 - Energy Dashboard Integration Suite

## 🎉 Major Release: Complete Energy Dashboard Integration

This release brings comprehensive integration with Home Assistant's native Energy Dashboard, featuring automatic synchronization, advanced analytics, and a custom dashboard template.

---

## ⚡ Key Features

### 1. Automatic Energy Dashboard Synchronization

- **Automatic Sync Detection** - Check on appliance startup if devices are configured in Energy Dashboard
- **Smart Reporting** - Detailed sync status with actionable recommendations
- **Read-only Access** - Safe, non-invasive reading of `.storage/energy` configuration

### 2. Three Powerful New Services

#### `sync_with_energy_dashboard`
Check synchronization status for all SAM devices or a specific one. Generates a comprehensive report showing which devices are synced and which need configuration.

```yaml
service: smart_appliance_monitor.sync_with_energy_dashboard
```

#### `export_energy_config`
Export the Energy Dashboard configuration for any device with step-by-step setup instructions.

```yaml
service: smart_appliance_monitor.export_energy_config
data:
  entity_id: sensor.washing_machine_state
```

#### `get_energy_data`
Retrieve aggregated energy data with period filtering and device breakdown.

```yaml
service: smart_appliance_monitor.get_energy_data
data:
  period_start: "2025-10-21T00:00:00"
  period_end: "2025-10-21T23:59:59"
```

### 3. Advanced Energy Analytics

- **Period Comparisons** - Compare energy usage across custom time periods (today vs yesterday, week vs week, etc.)
- **Device Breakdown** - Detailed consumption breakdown with percentages for each appliance
- **Top Consumers** - Identify and rank your highest energy consumers
- **Efficiency Scoring** - Get device-specific efficiency scores with optimization recommendations
- **Cost Analysis** - Track costs across different periods with trend analysis

### 4. Custom Energy Dashboard Template

Ready-to-use dashboard template (`dashboards/energy_dashboard.yaml`) featuring:

- **Summary Cards** - Total energy, costs, and active devices at a glance
- **Visual Breakdown** - Bar charts showing consumption by device
- **Energy Timeline** - Hourly visualization of energy usage
- **Top Consumers** - Ranking of your biggest energy users
- **Efficiency Metrics** - Overall and per-device efficiency scores
- **Quick Actions** - One-click sync, export, and navigation
- **Integration Status** - Real-time monitoring of Energy Dashboard sync

---

## 📦 What's Included

### New Modules

1. **`energy_storage.py`** (270 lines)
   - Read-only Energy Dashboard configuration reader
   - Caching system to minimize file I/O
   - Comprehensive error handling

2. **`energy_dashboard.py`** (419 lines)
   - Advanced analytics engine
   - Period comparison logic
   - Efficiency scoring algorithms

3. **`Energy-Dashboard.md`** (570 lines)
   - Complete user guide
   - Service documentation with examples
   - Troubleshooting and best practices

### Enhanced Modules

- **`energy.py`** - New `EnergyDashboardSync` class for sync management
- **`__init__.py`** - Three new services with automatic startup checks
- **`const.py`** - New constants for Energy Dashboard integration

---

## 🚀 Getting Started

### Installation

1. **Update the integration**:
   - Download `smart_appliance_monitor-v0.6.0.zip`
   - Extract to `/config/custom_components/`
   - Restart Home Assistant

2. **Check sync status**:
   ```yaml
   service: smart_appliance_monitor.sync_with_energy_dashboard
   ```

3. **Add missing devices** to Energy Dashboard:
   - Use the `export_energy_config` service for instructions
   - Or manually via Settings → Dashboards → Energy → Add Consumption

4. **Install custom dashboard** (optional):
   - Copy `dashboards/energy_dashboard.yaml`
   - Create new dashboard and paste YAML

### Quick Example

```yaml
# Check sync for all devices
service: smart_appliance_monitor.sync_with_energy_dashboard

# Export config for washing machine
service: smart_appliance_monitor.export_energy_config
data:
  entity_id: sensor.washing_machine_state

# Get today's energy data
service: smart_appliance_monitor.get_energy_data
data:
  period_start: "{{ now().replace(hour=0, minute=0).isoformat() }}"
  period_end: "{{ now().isoformat() }}"
```

---

## 📊 Impact

**For Users:**
- ✅ Seamless integration with Home Assistant Energy Dashboard
- ✅ Advanced analytics beyond native capabilities
- ✅ Automatic detection and easy configuration
- ✅ Foundation for future AI/ML features

**Statistics:**
- 3 new modules (~1,000 lines of code)
- 3 new services
- 1 custom dashboard template
- 1 comprehensive documentation guide
- Total: ~2,300 new lines of code

---

## 🔧 Technical Details

- **Architecture**: Read-only, non-invasive access to `.storage/energy`
- **Performance**: Caching system with 5-minute TTL
- **Compatibility**: Home Assistant 2023.x+
- **Dependencies**: None (uses built-in HA components)
- **Code Quality**: ✅ No linter errors, full type hints, comprehensive error handling

---

## 📚 Documentation

- **Complete Guide**: [Energy Dashboard Integration](https://github.com/legaetan/ha-smart_appliance_monitor/wiki/Energy-Dashboard)
- **Full Changelog**: See [CHANGELOG.md](CHANGELOG.md)
- **Roadmap**: See [IDEAS.md](docs/IDEAS.md)

---

## 🎯 What's Next?

This release lays the foundation for exciting future features:

- **v0.7.0**: Custom Energy Lovelace card with interactive visualizations
- **Future**: Automatic appliance detection via consumption analysis
- **Future**: ML-based energy optimization recommendations
- **Future**: Historical data analysis with Recorder integration

---

## 💡 Migration Notes

**No breaking changes!** This is a purely additive release.

All existing configurations and data are preserved. Simply restart Home Assistant after updating to start using the new features.

---

## 🙏 Acknowledgments

Thanks to the Home Assistant community for feedback and feature requests that inspired this release!

---

## 📥 Download

**Download**: [smart_appliance_monitor-v0.6.0.zip](https://github.com/legaetan/ha-smart_appliance_monitor/releases/download/v0.6.0/smart_appliance_monitor-v0.6.0.zip)

**SHA256**: *Will be added after release creation*

---

**Full Changelog**: https://github.com/legaetan/ha-smart_appliance_monitor/blob/main/CHANGELOG.md

