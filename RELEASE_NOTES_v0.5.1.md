# Smart Appliance Monitor v0.5.1 - Release Notes

**Release Date**: October 20, 2025

## 🎯 Focus of This Release

This version **0.5.1** resolves a critical issue: **data loss during Home Assistant restarts**. Now, all your running cycles and statistics are automatically saved and restored.

## 🔒 Major Feature: State Persistence

### The Problem Solved

**Before v0.5.1**:
- ❌ A washing machine cycle in progress during an HA restart was lost
- ❌ Duration and energy statistics were incorrect
- ❌ Cycle history was reset
- ❌ Users lost their data during updates or restarts

**With v0.5.1**:
- ✅ Running cycles automatically continue after restart
- ✅ Statistics are preserved and remain accurate
- ✅ History is saved for anomaly detection
- ✅ No manual intervention required

### How Does It Work?

The persistence system is **fully automatic**:

#### Automatic Save
- ✅ **At cycle start**: Initial state saved
- ✅ **At cycle end**: Complete statistics recorded
- ✅ **Every 30 seconds**: Updates during cycle

#### Smart Restore
- ✅ **At HA startup**: All states are restored
- ✅ **Data validation**: Obsolete statistics are reset
  - Daily stats from another day → Reset to zero
  - Monthly stats from another month → Reset to zero
  - Running cycles → Always restored

#### Storage Location
```
/config/.storage/smart_appliance_monitor.<entry_id>.json
```

### Concrete Example

#### Scenario: Washing Machine + HA Restart

1. **9:00 PM** - Washing machine starts
   - 💾 Save: Cycle started at 9:00 PM, initial energy 1.234 kWh

2. **9:30 PM** - You restart Home Assistant (update, etc.)
   - 📂 Automatic load of save file
   - ♻️ Restore: State `running`, cycle started at 9:00 PM

3. **9:45 PM** - Washing machine finishes
   - ✅ Correct end detection
   - 📊 **Duration calculated: 45 minutes** (from 9:00 PM, not 9:30 PM!)
   - 💰 **Correct energy and cost**
   - 🔔 Notification with accurate values

### What Is Saved

The system preserves all important data:

1. **Cycle State**
   - Current state (`idle`, `running`, `finished`)
   - Start time
   - Initial energy
   - Peak power

2. **Last Completed Cycle**
   - Total duration
   - Energy consumed
   - Calculated cost

3. **Daily Statistics**
   - Date
   - Number of cycles
   - Total energy
   - Total cost

4. **Monthly Statistics**
   - Year and month
   - Total energy
   - Total cost

5. **Cycle History**
   - Last 10 cycles for anomaly detection

6. **Configuration**
   - Monitoring enabled/disabled
   - Notifications enabled/disabled

## 📁 Storage Format

Data is stored in JSON:

```json
{
  "state": "running",
  "current_cycle": {
    "start_time": "2025-10-20T21:00:00",
    "start_energy": 1.234,
    "peak_power": 150.5
  },
  "last_cycle": {
    "start_time": "2025-10-20T19:00:00",
    "end_time": "2025-10-20T20:30:00",
    "duration": 90.0,
    "energy": 1.5
  },
  "daily_stats": {
    "date": "2025-10-20",
    "cycles": 3,
    "total_energy": 4.5,
    "total_cost": 1.13
  },
  "monthly_stats": {
    "year": 2025,
    "month": 10,
    "total_energy": 45.0,
    "total_cost": 11.32
  },
  "cycle_history": [],
  "monitoring_enabled": true,
  "notifications_enabled": true
}
```

## 🔧 Technical Implementation

### Files Created

1. **`docs/PERSISTENCE.md`** (183 lines)
   - Complete technical documentation
   - Storage format
   - Usage examples
   - Maintenance

2. **`RESUME_PERSISTANCE.md`** (150 lines)
   - Implementation summary in French
   - Problem and solution
   - Changes made

3. **`tests/test_persistence.py`** (279 lines)
   - Complete test suite (11 tests)
   - Serialization/deserialization tests
   - Save/restore tests
   - Data validation tests

### Files Modified

1. **`custom_components/smart_appliance_monitor/__init__.py`** (+4 lines)
   - Call to `restore_state()` at setup

2. **`custom_components/smart_appliance_monitor/coordinator.py`** (+186 lines)
   - Complete persistence system
   - Serialization/deserialization methods
   - Automatic save in events
   - Restore with validation

## ✅ Compatibility and Migration

### Backward Compatibility

✅ **100% backward compatible** with v0.5.0:
- No configuration changes required
- Existing configurations work immediately
- First save happens automatically during next cycle

### Migration

**No user action required**:
1. Install v0.5.1
2. Restart Home Assistant
3. System automatically starts saving

**Note**: First restart after installation won't restore anything (no existing save), but all subsequent restarts will benefit from persistence.

## 🎉 User Benefits

### 1. No Data Loss
- Your cycles are no longer interrupted by restarts
- Statistics remain reliable and accurate
- History is preserved

### 2. Better Experience
- Complete transparency: you notice no difference
- Increased reliability: your data is always there
- Confidence: no fear of restarting HA

### 3. Reliable Anomaly Detection
- Cycle history is preserved
- ML analysis remains relevant
- Patterns are correctly identified

### 4. Accurate Statistics
- Durations calculated from actual cycle start
- Exact energy and costs
- Notifications with correct values

## 📊 Performance

The persistence system is optimized:

- ⚡ **Asynchronous save**: Non-blocking, no performance impact
- ⚡ **Lightweight files**: < 5 KB typically per appliance
- ⚡ **Minimal impact**: Saves every 30s only if cycle running
- ⚡ **Fast restore**: Instant loading at startup

## 🔍 Error Handling

The system is **resilient**:

- **Corrupted file**: Integration starts with default values
- **Missing file**: Normal first initialization
- **Save failure**: Error logged, operation continues
- **Restore failure**: Clean start without restored data

## 📚 Documentation

### Technical Documentation

- **[docs/PERSISTENCE.md](docs/PERSISTENCE.md)** - Complete system documentation
  - Overview
  - Storage format
  - Detailed operation
  - Usage examples
  - Maintenance

### User Documentation (Wiki)

- Wiki updated with persistence information
- "State Persistence" section in Features Guide
- Mentions on Home page

## 🚀 Installation and Upgrade

### New Users

1. Download `smart_appliance_monitor-0.5.1.zip`
2. Extract to `/config/custom_components/`
3. Restart Home Assistant
4. Configure your appliances via UI

### Upgrade from v0.5.0

1. Replace contents of `/config/custom_components/smart_appliance_monitor/`
2. Restart Home Assistant
3. ✅ Your configurations are preserved
4. ✅ Persistence starts automatically

### Upgrade from v0.4.x or Earlier

1. Install v0.5.1
2. Restart Home Assistant
3. Your appliances continue to work
4. Access new v0.5.0 features via **Options** if desired

## 🐛 Bug Fixes

This version fixes:
- ❌ **Lost running cycles** during HA restart → ✅ Fixed
- ❌ **Incorrect durations** after restart → ✅ Fixed
- ❌ **Reset statistics** during restart → ✅ Fixed
- ❌ **Lost history** for anomaly detection → ✅ Fixed

## ⚠️ Breaking Changes

**No breaking changes** in this version!

All existing configurations continue to work without modification.

## 🔮 Next Steps

### Version 0.6.0 (Planned Q4 2025)

- **Custom Cards**: Dedicated Lovelace cards
- **Strict mode**: Physical blocking with scheduling
- **Advanced graphs**: Consumption history
- **Multi-tariff**: Automatic peak/off-peak support

## 💡 Usage Examples

### Use Case 1: HA Maintenance

```
Before v0.5.1:
- Washing machine starts at 9:00 PM
- HA update at 9:30 PM
- Cycle lost, wrong statistics ❌

With v0.5.1:
- Washing machine starts at 9:00 PM
- HA update at 9:30 PM
- Cycle continues, accurate data ✅
```

### Use Case 2: Unexpected Restart

```
Before v0.5.1:
- 3D printer running (8h print)
- Brief power outage
- HA restarts, print tracking lost ❌

With v0.5.1:
- 3D printer running (8h print)
- Brief power outage
- HA restarts, print tracking restored ✅
```

### Use Case 3: Monthly Statistics

```
Before v0.5.1:
- 15 cycles this month, $25
- HA restart
- Monthly statistics lost ❌

With v0.5.1:
- 15 cycles this month, $25
- HA restart
- Monthly statistics preserved ✅
```

## 🙏 Acknowledgments

Thanks to all users who reported this issue and helped identify critical use cases.

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/legaetan/ha-smart_appliance_monitor/issues)
- **Discussions**: [GitHub Discussions](https://github.com/legaetan/ha-smart_appliance_monitor/discussions)
- **Wiki**: [Complete Documentation](https://github.com/legaetan/ha-smart_appliance_monitor/wiki)

## 📥 Download

- **ZIP Archive**: `smart_appliance_monitor-0.5.1.zip`
- **Size**: 60 KB
- **SHA256 Checksum**: `a040c5b0ff758ff78d368a6c727806f3e017277368efea676bb359b3f0740512`

---

**Version**: 0.5.1  
**Date**: October 20, 2025  
**Compatibility**: Home Assistant 2023.x+  
**License**: MIT

**Full Changelog**: [CHANGELOG.md](CHANGELOG.md)
