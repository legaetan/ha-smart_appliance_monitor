# Release Notes - v0.7.4

**Release Date**: October 21, 2025  
**Type**: Critical Bug Fix Release  
**Priority**: Critical (Highly Recommended for all users)

---

## 🚨 Critical Fix

### Negative Energy Values

**Problem**: Users were experiencing negative energy consumption values in their statistics (e.g., -4551.384 kWh for daily/monthly totals), making all analytics and AI recommendations completely unreliable.

**Root Cause**: When ESPHome devices (or other energy sensors) are rebooted or reset, their energy counters restart from 0. If a cycle spans across a reboot, the end energy value becomes **lower** than the start energy value, creating a **negative cycle energy** that gets added to cumulative statistics.

**Example**:
```
Cycle starts: start_energy = 4555.745 kWh
Device reboots during cycle
Cycle ends: end_energy = 0.316 kWh (counter reset)
Result: energy = 0.316 - 4555.745 = -4555.429 kWh ❌
```

**Solution**:
- ✅ **Multi-level validation** to detect and handle negative values
- ✅ **Automatic skipping** of negative cycle energies (with warning log)
- ✅ **Auto-recovery** if totals become negative despite validation
- ✅ **State restoration validation** to correct existing corrupted data
- ✅ **Detailed logging** for troubleshooting data integrity issues

---

## 🔧 Technical Changes

### Validation in `_on_cycle_finished()`

**Level 1 - Cycle Energy Validation**:
```python
if energy < 0:
    _LOGGER.warning(
        "Énergie de cycle négative détectée (%.3f kWh) pour '%s'. "
        "Cela indique probablement un reset du compteur. Cycle ignoré dans les stats.",
        energy,
        self.appliance_name,
    )
    # Cycle is counted but energy/cost not added to totals
```

**Level 2 - Total Validation**:
```python
if self.daily_stats["total_energy"] < 0:
    _LOGGER.error(
        "Total d'énergie quotidienne négatif détecté (%.3f kWh) pour '%s'. "
        "Réinitialisation des statistiques quotidiennes.",
        self.daily_stats["total_energy"],
        self.appliance_name,
    )
    self.daily_stats["total_energy"] = max(0, energy)
    self.daily_stats["total_cost"] = max(0, cost)
```

### Validation in `restore_state()`

**On Integration Reload/Restart**:
```python
if self.daily_stats.get("total_energy", 0) < 0:
    _LOGGER.warning(
        "Énergie quotidienne négative détectée lors de la restauration "
        "(%.3f kWh) pour '%s'. Réinitialisation à 0.",
        self.daily_stats["total_energy"],
        self.appliance_name,
    )
    self.daily_stats["total_energy"] = 0.0
    self.daily_stats["total_cost"] = 0.0
```

---

## 📦 Migration Guide

### Automatic Recovery (Recommended)

**Option 1: Wait for next cycle**
1. Update to v0.7.4
2. Reload the integration (or restart Home Assistant)
3. When the next cycle completes, negative values will be automatically corrected

**Option 2: Manual reset**
1. Update to v0.7.4
2. Press the "Reset Statistics" button for affected appliances
3. Statistics immediately reset to 0

### What to Expect

**Before v0.7.4**:
```yaml
sensor.chauffe_eau_energie_du_jour:
  state: "-4551.384"  # ❌ Negative!
  attributes:
    total_cost: -888.43  # ❌ Negative cost!
```

**After v0.7.4 (automatic correction)**:
```yaml
sensor.chauffe_eau_energie_du_jour:
  state: "0.0"  # ✅ Corrected!
  attributes:
    total_cost: 0.0  # ✅ Corrected!
```

**After next valid cycle**:
```yaml
sensor.chauffe_eau_energie_du_jour:
  state: "0.316"  # ✅ Valid energy!
  attributes:
    total_cost: 0.06  # ✅ Valid cost!
```

---

## 🎯 Impact

### AI Analysis

**Before**: AI reported "needs_improvement" due to data inconsistencies:
> *"The 'Chauffe-Eau' water heater is currently in a state that needs_improvement primarily due to significant data inconsistencies preventing accurate historical analysis. The overall energy consumption figures provided are erroneous (negative values)..."*

**After**: AI provides accurate, actionable recommendations:
> *"The 'Chauffe-Eau' water heater completed one cycle recently, consuming 0.316 kWh over 11.9 minutes... initial observations suggest normal operation for the single recorded event, with opportunities for optimization through scheduling and temperature management."*

### Energy Dashboard

- ✅ No more negative kWh values
- ✅ Accurate cost calculations
- ✅ Reliable consumption tracking
- ✅ Valid comparison with other appliances

### User Experience

- ✅ No manual intervention needed (automatic recovery)
- ✅ Clear warning logs if sensor resets detected
- ✅ "Reset Statistics" button still available for manual correction
- ✅ Future sensor resets handled gracefully

---

## 🔍 Debugging

### Log Messages to Watch For

**Negative cycle energy detected** (expected after device reboot):
```
WARNING (MainThread) [custom_components.smart_appliance_monitor.coordinator] 
Énergie de cycle négative détectée (-4555.429 kWh) pour 'Chauffe-Eau'. 
Cela indique probablement un reset du compteur. Cycle ignoré dans les stats.
```

**Total became negative** (should be rare with new validation):
```
ERROR (MainThread) [custom_components.smart_appliance_monitor.coordinator] 
Total d'énergie quotidienne négatif détecté (-4551.384 kWh) pour 'Chauffe-Eau'. 
Réinitialisation des statistiques quotidiennes.
```

**Corrupted data corrected on load**:
```
WARNING (MainThread) [custom_components.smart_appliance_monitor.coordinator] 
Énergie quotidienne négative détectée lors de la restauration (-4551.384 kWh) pour 'Chauffe-Eau'. 
Réinitialisation à 0.
```

---

## ⚠️ Known Limitations

- **First cycle after sensor reset** will not have accurate energy measurement (expected)
- **Historical data** is not retroactively corrected (only current day/month)
- **ESPHome device resets** during a cycle will still trigger warnings (this is informational)

---

## 📝 Files Modified

- `custom_components/smart_appliance_monitor/coordinator.py` (+55 lines)
  - Enhanced `_on_cycle_finished()` with validation
  - Enhanced `restore_state()` with validation
  - Added detailed logging

---

## 🙏 Credits

This release fixes a critical data integrity issue that affected AI analysis and energy tracking. Special thanks to users who reported negative energy values and provided detailed logs for debugging!

---

## 📋 Detailed Changelog

See [CHANGELOG.md](../../CHANGELOG.md#074---2025-10-21) for complete technical details.

