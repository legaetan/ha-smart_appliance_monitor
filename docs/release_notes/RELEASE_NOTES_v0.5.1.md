# Smart Appliance Monitor v0.5.1 - Release Notes

**Release Date**: October 20, 2025

## 🔒 Major Feature: State Persistence

This version **0.5.1** resolves a critical issue: **data loss during Home Assistant restarts**. Now, all your running cycles and statistics are automatically saved and restored.

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

## 🎯 Key Benefits

### 1. No Data Loss
- Your cycles are no longer interrupted by restarts
- Statistics remain reliable and accurate
- History is preserved

### 2. Better Experience
- Complete transparency: you notice no difference
- Increased reliability: your data is always there
- Confidence: no fear of restarting HA

### 3. Accurate Statistics
- Durations calculated from actual cycle start
- Exact energy and costs
- Notifications with correct values

## 🔧 How It Works

The persistence system is **fully automatic**:

### Automatic Save
- ✅ At cycle start: Initial state saved
- ✅ At cycle end: Complete statistics recorded
- ✅ Every 30 seconds: Updates during cycle

### Smart Restore
- ✅ At HA startup: All states are restored
- ✅ Data validation: Obsolete statistics are reset
- ✅ Storage: `.storage/smart_appliance_monitor.<entry_id>.json`

## 📊 What's Saved

- **Cycle State**: Current state, start time, energy, power
- **Last Cycle**: Duration, energy, cost
- **Daily Statistics**: Date, cycles count, energy, cost
- **Monthly Statistics**: Year, month, energy, cost
- **Cycle History**: Last 10 cycles for anomaly detection
- **Configuration**: Monitoring and notifications states

## ✅ Compatibility

- ✅ **100% backward compatible** with v0.5.0
- ✅ **No user action required**
- ✅ **No breaking changes**

## 🚀 Installation

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

## 🐛 Bug Fixes

- ✅ Lost running cycles during HA restart
- ✅ Incorrect durations after restart
- ✅ Reset statistics during restart
- ✅ Lost history for anomaly detection

## 📚 Documentation

- **Technical**: [docs/PERSISTENCE.md](docs/PERSISTENCE.md) - Complete system documentation
- **Wiki**: Updated with persistence information
- **Changelog**: [CHANGELOG.md](CHANGELOG.md) - Full technical details

## 📥 Download

- **Archive**: `smart_appliance_monitor-0.5.1.zip` (60 KB)
- **SHA256**: `a040c5b0ff758ff78d368a6c727806f3e017277368efea676bb359b3f0740512`

---

**Full Changelog**: [v0.5.0...v0.5.1](https://github.com/legaetan/ha-smart_appliance_monitor/compare/v0.5.0...v0.5.1)

