# Release Notes - v0.8.0 - Cycle History System

**Release Date**: October 22, 2025  
**Type**: Feature Release  
**Download**: [smart_appliance_monitor-v0.8.0.zip](https://github.com/legaetan/ha-smart_appliance_monitor/releases/tag/v0.8.0)

---

## 🎉 Overview

Version 0.8.0 introduces a complete **Cycle History System** that brings long-term cycle data persistence and advanced querying capabilities to Smart Appliance Monitor. This release enables users to access their complete appliance usage history and reconstruct cycles from past sensor data.

---

## ✨ Key Features

### 1. Persistent Cycle History

**Hybrid Storage Architecture**:
- **30 recent cycles** kept in memory for fast access (anomaly detection, AI analysis)
- **Unlimited cycles** stored in Home Assistant Recorder database
- **Automatic synchronization** - every completed cycle is saved to both systems
- **No configuration required** - cycles are automatically recorded by Home Assistant

### 2. New Service: `get_cycle_history`

Query historical cycles with powerful filtering capabilities:

```yaml
service: smart_appliance_monitor.get_cycle_history
data:
  entity_id: sensor.washing_machine_state
  period_start: "2025-09-01T00:00:00"
  period_end: "2025-10-22T23:59:59"
  min_duration: 30      # Optional: cycles longer than 30 minutes
  max_energy: 2.0       # Optional: cycles under 2 kWh
  limit: 100            # Optional: max results
```

**Features**:
- Filter by period, duration, energy consumption
- Get aggregated statistics (total energy, cost, averages)
- Fires `smart_appliance_monitor_cycle_history` event with complete data
- Returns cycles with full metadata (start/end times, energy, peak power)

### 3. New Service: `import_historical_cycles`

Reconstruct cycles from raw sensor history - perfect for importing data from before the integration was installed:

```yaml
# Step 1: Preview with dry-run
service: smart_appliance_monitor.import_historical_cycles
data:
  entity_id: sensor.washing_machine_state
  period_start: "2025-07-01T00:00:00"
  dry_run: true

# Step 2: Import for real
service: smart_appliance_monitor.import_historical_cycles
data:
  entity_id: sensor.washing_machine_state
  period_start: "2025-07-01T00:00:00"
  dry_run: false
```

**Features**:
- Analyzes power sensor history to detect past cycles
- Dry-run mode for safe preview
- Monthly statistics breakdown
- `replace_existing` mode to clean and reimport with corrected settings

---

## 🔧 Technical Improvements

### Database Integration
- Optimized SQL queries for modern Home Assistant Recorder schema
- Uses `event_type_id` and `time_fired_ts` for compatibility
- Efficient event storage and retrieval
- Automatic cleanup when using `replace_existing: true`

### Enhanced Cycle Data
- All cycles now include complete metadata:
  - Start and end timestamps
  - Start and end energy readings
  - Peak power consumption
  - Duration, energy consumed, cost
  - Import source tracking (`imported`, `reimported` flags)

---

## 📖 Use Cases

1. **Long-term Analysis**: Track appliance usage patterns over months or years
2. **Cost Tracking**: Calculate total energy costs across any time period
3. **Efficiency Comparison**: Compare cycles before and after maintenance
4. **Historical Recovery**: Import cycles from before integration installation
5. **AI Analysis**: Provide more data points for better AI-powered insights
6. **Custom Dashboards**: Build reports with historical cycle statistics

---

## ⚠️ Important Warnings

### `replace_existing` Parameter

The `replace_existing: true` parameter **permanently deletes** all existing cycles for the specified appliance in the given period before importing new ones.

**Always**:
1. Test with `dry_run: true` first to preview
2. Understand that deletion is permanent
3. Ensure you have backups if needed

### Recorder Requirements

- Historical import requires power sensor data to exist in Recorder
- Recorder retention policy affects how far back you can query (default: 10 days)
- Extend retention in `configuration.yaml` if needed:
  ```yaml
  recorder:
    purge_keep_days: 90  # Keep 90 days of history
  ```

---

## 📦 Installation

### Via HACS (Recommended)

1. Open HACS in Home Assistant
2. Go to "Integrations"
3. Search for "Smart Appliance Monitor"
4. Click "Update" to v0.8.0
5. Restart Home Assistant

### Manual Installation

1. Download `smart_appliance_monitor-v0.8.0.zip`
2. Extract to `custom_components/smart_appliance_monitor/`
3. Restart Home Assistant
4. New services will be available immediately

---

## 🔄 Migration from v0.7.x

### Breaking Changes
**None** - This is a fully backward-compatible release.

### What Happens to Existing Data
- All existing cycles continue working normally
- New services are available immediately
- Existing cycle events in Recorder are compatible
- No reconfiguration required

### Recommendations
1. Start by querying existing cycles with `get_cycle_history`
2. Use `import_historical_cycles` with `dry_run: true` to preview imports
3. Consider importing historical data if you had sensors before installing the integration

---

## 📝 Changelog

### Added
- Persistent cycle history via Home Assistant Recorder
- `get_cycle_history` service with advanced filters
- `import_historical_cycles` service for historical data reconstruction
- Hybrid storage: 30 in-memory + unlimited in database
- Automatic cycle event recording (no configuration needed)

### Changed
- Increased in-memory cycle history from 10 to 30 cycles
- Enhanced cycle events with complete metadata
- Improved documentation with cycle history system guide

### Fixed
- SQL queries compatibility with modern Recorder schema
- Event querying to properly use event_type_id
- Timestamp handling with time_fired_ts

---

## 📚 Documentation

- **Full Changelog**: [CHANGELOG.md](https://github.com/legaetan/ha-smart_appliance_monitor/blob/main/CHANGELOG.md)
- **README**: [README.md](https://github.com/legaetan/ha-smart_appliance_monitor/blob/main/README.md)
- **Testing Guide**: [docs/TEST_CYCLE_HISTORY.md](https://github.com/legaetan/ha-smart_appliance_monitor/blob/main/docs/TEST_CYCLE_HISTORY.md)
- **Wiki**: [GitHub Wiki](https://github.com/legaetan/ha-smart_appliance_monitor/wiki) *(to be updated)*

---

## 🐛 Known Issues

None reported.

---

## 🙏 Acknowledgments

Thank you to all users for your feedback and feature requests that made this release possible!

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/legaetan/ha-smart_appliance_monitor/issues)
- **Discussions**: [GitHub Discussions](https://github.com/legaetan/ha-smart_appliance_monitor/discussions)
- **Wiki**: [Documentation](https://github.com/legaetan/ha-smart_appliance_monitor/wiki)

---

**Happy monitoring!** 🚀

