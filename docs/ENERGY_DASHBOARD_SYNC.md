# Energy Dashboard Synchronization

**Version**: 0.9.1+ (Unreleased)  
**Date**: October 2025

This document describes the Energy Dashboard synchronization features in Smart Appliance Monitor.

---

## Overview

The `sync_with_energy_dashboard` service provides bidirectional integration between Smart Appliance Monitor (SAM) and Home Assistant's native Energy Dashboard.

### Key Features

1. **Smart Device Matching**: Automatically finds SAM appliances in Energy Dashboard using multiple matching strategies
2. **Global Price Sync**: Retrieves and applies electricity pricing from Energy Dashboard to all SAM appliances
3. **Detailed Reporting**: Provides comprehensive sync status and recommendations

---

## How It Works

### 1. Device Detection

The service uses the **configured energy sensor** from each SAM appliance (the sensor from your smart plug) to find matching entries in the Energy Dashboard.

**Example**:
```yaml
# SAM Configuration
appliance_name: "Lave Linge"
energy_sensor: "sensor.lave_linge_consommation"  # ← This sensor is used

# Energy Dashboard (.storage/energy)
device_consumption:
  - stat_consumption: "sensor.lave_linge_consommation"  # ← Match found!
    name: "Lave Linge"
```

### 2. Fuzzy Matching

If exact sensor match fails, the service uses intelligent fuzzy matching:

#### Strategy 1: Exact Name Match
```python
SAM: "Lave Linge"
Energy Dashboard: "Lave Linge"
→ ✅ Match
```

#### Strategy 2: Normalized Name Match (no accents)
```python
SAM: "Sèche-Linge"
Energy Dashboard: "Seche Linge"
→ ✅ Match (accents removed, hyphens normalized)
```

#### Strategy 3: Partial Name Match
```python
SAM: "Bambulab X1C"
Energy Dashboard: "X1C"
→ ✅ Match (partial contains)
```

#### Strategy 4: Sensor Pattern Match
```python
SAM appliance_name: "lave_linge"
Energy sensor: "sensor.lave_linge_consommation"
→ ✅ Match (base name extraction)
```

### 3. Global Price Synchronization

**NEW in v0.9.1**: The service now retrieves the global electricity price from Energy Dashboard and applies it to **all** SAM appliances.

#### Price Sources

**Option A: Dynamic Price Entity**
```json
{
  "entity_energy_price": "input_number.edf_price_kwh"
}
```
→ Reads current value from the entity (e.g., 0.4500 €/kWh)

**Option B: Static Price**
```json
{
  "number_energy_price": 0.20
}
```
→ Uses fixed price value

#### Application Logic

```python
# 1. Retrieve global price (once for all devices)
price = get_price_from_energy_dashboard()  # 0.4500 €/kWh

# 2. Apply to ALL SAM coordinators
for coordinator in all_sam_appliances:
    coordinator.price_kwh = 0.4500  # ✅ Global price
```

**Result**: All 9 appliances now use the same price (0.4500 €/kWh)

---

## Service Usage

### Call the Service

**Developer Tools → Services**

```yaml
service: smart_appliance_monitor.sync_with_energy_dashboard
data:
  entity_id: sensor.lave_linge_state  # Optional: sync specific appliance
  # Omit entity_id to sync all appliances
```

### Expected Output

**Notification: Energy Dashboard Sync Report**

```
🔄 Energy Dashboard Sync Report

Total SAM devices: 9
Synced: 9
Not configured: 0

💰 Global price applied: 0.4500 €/kWh
Source: input_number.edf_price_kwh
Applied to: All 9 appliances

✅ Synced devices:
- Lave Linge
- Lave Vaisselle
- VMC
- Four
- Chauffe-Eau
- Séche Linge
- Bambulab X1C
- Ecran PC
- Bureau PC
```

---

## Technical Implementation

### Files Modified

**1. `energy.py`**
- Added `sync_price_from_energy_dashboard()` method
- Enhanced `get_sync_status()` to use configured energy sensor
- Added `_find_device_by_name_fuzzy()` for intelligent matching

**2. `__init__.py`**
- Modified `handle_sync_with_energy_dashboard()` service handler
- Implemented global price retrieval and application
- Enhanced notification message with price sync results

**3. `energy_storage.py`**
- No changes (existing read-only access to `.storage/energy` file)

### Code Flow

```
1. User clicks "Synchroniser Energy Dashboard" button
   ↓
2. Service: sync_with_energy_dashboard
   ↓
3. Get global price from Energy Dashboard (once)
   - Read .storage/energy
   - Extract entity_energy_price or number_energy_price
   - Get current price value
   ↓
4. Apply price to all SAM coordinators
   - coordinator.price_kwh = global_price
   ↓
5. For each appliance:
   - Check if configured energy sensor is in Energy Dashboard
   - Use fuzzy matching if exact match fails
   - Record sync status
   ↓
6. Generate and display sync report
   - Synced devices list
   - Global price information
   - Not configured devices (if any)
```

---

## Configuration Requirements

### In Energy Dashboard

**Go to**: Settings → Dashboards → Energy

**Required Configuration**:
```yaml
# Energy Source
Grid Consumption: sensor.index_edf_galinky
Energy Price: input_number.edf_price_kwh  # ← Price entity

# Device Consumption (for each appliance)
- Device: Lave Linge
  Sensor: sensor.lave_linge_consommation  # ← Must match SAM config
```

### In Smart Appliance Monitor

**Required Configuration**:
```yaml
# Appliance Configuration
Appliance Name: "Lave Linge"
Energy Sensor: "sensor.lave_linge_consommation"  # ← Must exist in Energy Dashboard
```

**Note**: The energy sensor must be the same in both SAM and Energy Dashboard for automatic sync to work.

---

## Troubleshooting

### Issue: "Not in Energy Dashboard"

**Cause**: Energy sensor not configured in Energy Dashboard

**Solution**:
1. Go to Settings → Dashboards → Energy
2. Click "Add Consumption"
3. Select the sensor: `sensor.xxx_consommation`
4. Save
5. Re-run sync service

### Issue: "No price configured"

**Cause**: No price entity or static price in Energy Dashboard

**Solution**:
1. Go to Settings → Dashboards → Energy
2. Edit Grid Consumption
3. Add Energy Price: Select an entity (e.g., `input_number.edf_price_kwh`)
4. Or enter a static price
5. Save
6. Re-run sync service

### Issue: Price not applied to appliances

**Cause**: Coordinator price update may require restart

**Solution**:
1. Check logs for "Applied global price to 'XXX'" messages
2. If price still not applied, restart Home Assistant
3. Price should persist after restart (stored in coordinator)

---

## Benefits

### For Users

1. **Single Source of Truth**: Configure electricity price once in Energy Dashboard
2. **Automatic Sync**: All SAM appliances use the same price automatically
3. **Dynamic Pricing**: Supports time-of-use tariffs via price entities
4. **No Duplicate Configuration**: Don't need to set price for each appliance

### For Developers

1. **Read-Only Access**: Service only reads `.storage/energy` (no write operations)
2. **Safe Operation**: No risk of corrupting Energy Dashboard configuration
3. **Intelligent Matching**: Multiple fallback strategies ensure device detection
4. **Comprehensive Logging**: Detailed logs for debugging sync issues

---

## Future Enhancements

Potential features for future versions:

1. **Tariff Schedule Sync**: Import peak/off-peak hours from Energy Dashboard
2. **Historical Data Alignment**: Compare SAM stats with Energy Dashboard data
3. **Two-Way Sync**: Export SAM device configurations to Energy Dashboard
4. **Cost Reconciliation**: Detect and report cost discrepancies between systems
5. **Automatic Periodic Sync**: Schedule regular syncs (e.g., daily at midnight)

---

## API Reference

### Service: `smart_appliance_monitor.sync_with_energy_dashboard`

**Parameters**:
- `entity_id` (optional): Specific appliance sensor to sync (e.g., `sensor.lave_linge_state`)
  - If omitted: Syncs all SAM appliances

**Returns**: None (creates persistent notification)

**Side Effects**:
- Updates `coordinator.price_kwh` for all appliances
- Creates persistent notification with sync report
- Logs sync status for each appliance

**Exceptions**:
- `EnergyStorageError`: Cannot read `.storage/energy` file
- Handles gracefully: Reports error in notification

---

## Related Documentation

- [Energy Dashboard Integration](Energy-Dashboard.md)
- [Global Configuration](docs/wiki-github/Configuration.md)
- [Services Reference](services.yaml)
- [Energy Storage Reader](energy_storage.py)

---

## Changelog

### v0.9.1 (Unreleased)
- Added global price synchronization
- Improved device matching with fuzzy logic
- Enhanced sync report with price information
- Now uses configured energy sensor instead of SAM-generated sensors

### v0.7.0
- Initial implementation of `sync_with_energy_dashboard`
- Basic device detection and status reporting

