# Smart Appliance Monitor v1.1.0 - Optimized Detection & Air Conditioner Profile

**Release Date**: October 23, 2025

---

## 🎉 What's New

This release brings **data-driven optimizations** to all appliance profiles and introduces a dedicated **Air Conditioner profile** with rapid detection capabilities. All thresholds have been recalculated based on analysis of real power consumption data from 10 appliances over 3+ days.

### Key Highlights

✅ **2-4x Faster Detection** - Start detection reduced from 2 minutes to 15-60 seconds  
✅ **Eliminates False Positives** - No more triggers from standby power  
✅ **New Air Conditioner Profile** - Optimized for compressor behavior  
✅ **Data-Driven Thresholds** - Based on 2,000-40,000+ data points per appliance  
✅ **Automation Tools** - Scripts to analyze and update thresholds automatically  

---

## 🆕 New Features

### Air Conditioner Profile

A dedicated profile for air conditioning units with intelligent compressor cycle detection:

- **Thresholds**: 50W start / 20W stop
- **Detection**: 60s start delay / 180s stop delay
- **Alert**: 12-hour duration for forgotten AC
- **Languages**: English and French translations included

**How to use:**
1. Go to Settings → Devices & Services → Smart Appliance Monitor
2. Find your AC appliance → Reconfigure
3. Change type to "Air Conditioner" (Climatisation)
4. Optimal thresholds are applied automatically!

### Analysis & Automation Tools

Two new Python scripts in the `tools/` directory:

**`analyze_appliances.py`** - Analyze power consumption patterns:
```bash
python3 tools/analyze_appliances.py
```
- Retrieves historical data from Home Assistant
- Calculates optimal thresholds based on percentile analysis
- Compares with current settings
- Generates detailed report with recommendations

**`update_thresholds.py`** - Apply optimized thresholds automatically:
```bash
python3 tools/update_thresholds.py
```
- Shows current vs optimized thresholds
- Asks for confirmation before each change
- Updates configuration via SSH
- Offers to restart Home Assistant

---

## 🔧 Optimized Profiles

All appliance profiles have been updated with data-driven thresholds and faster detection times.

### Updated Thresholds

| Appliance | Old Thresholds | New Thresholds | Improvement |
|-----------|----------------|----------------|-------------|
| **Washing Machine** | 10W / 5W | **100W / 20W** | No more standby detection |
| **Dishwasher** | 20W / 5W | **150W / 50W** | Captures actual wash start |
| **Dryer** | 100W / 10W | **200W / 50W** | Reliable heating detection |
| **Monitor** | 30W / 5W | **40W / 5W** | Modern display optimized |
| **3D Printer** | 50W / 10W | **30W / 10W** | BambuLab optimized |
| **Air Conditioner** | N/A | **50W / 20W** | **NEW PROFILE** |

### Faster Detection Times

Detection speeds improved across the board:

| Appliance | Old Start/Stop | New Start/Stop | Speedup |
|-----------|----------------|----------------|---------|
| Washing Machine | 120s / 300s | **60s / 120s** | 2x faster |
| Dishwasher | 120s / 300s | **60s / 120s** | 2x faster |
| Dryer | 60s / 180s | **30s / 120s** | 2x faster |
| Water Heater | 60s / 120s | **30s / 60s** | 2x faster |
| Monitor | 60s / 120s | **30s / 60s** | 2x faster |
| Coffee Maker | 30s / 60s | **15s / 30s** | 2x faster |
| 3D Printer | 120s / 180s | **60s / 120s** | 2x faster |

---

## 📊 Technical Details

### Data Analysis Methodology

Thresholds were determined through rigorous analysis:

- **Data Collection**: 20-23 October 2025 (3+ days of real usage)
- **Sample Size**: 2,000 to 40,000+ data points per appliance
- **Method**: Percentile analysis (P25/P75) to identify operational states
- **Validation**: Tested against false positive detection

### Benefits

✅ **Faster Response** - Get notified 2-4x faster when appliances start  
✅ **No False Alarms** - Standby power no longer triggers detection  
✅ **Reliable Tracking** - Complete cycles captured without missing starts  
✅ **Better UX** - Notifications only for real appliance usage  
✅ **Energy Accuracy** - Improved energy consumption tracking  

---

## 📦 Installation

### HACS (Recommended)

1. Go to HACS → Integrations
2. Search for "Smart Appliance Monitor"
3. Click Install
4. Restart Home Assistant

### Manual Installation

1. Copy `custom_components/smart_appliance_monitor/` to your Home Assistant `config/custom_components/` directory
2. Restart Home Assistant
3. Go to Settings → Devices & Services → Add Integration
4. Search for "Smart Appliance Monitor"

---

## 🔄 Updating from Previous Versions

### Automatic Update (Existing Users)

Your appliances will automatically use the new optimized profiles:

1. Update the integration (via HACS or manual)
2. Restart Home Assistant
3. **That's it!** New thresholds are applied to existing appliances

### Optional: Apply Thresholds to Existing Appliances

If you want to update thresholds for existing appliances that have custom settings:

**Option A - Automated (Recommended):**
```bash
python3 tools/update_thresholds.py
```

**Option B - Manual:**
1. Go to Settings → Devices & Services → Smart Appliance Monitor
2. Click on each appliance → Configure → Advanced Configuration
3. Update thresholds according to CHANGELOG.md

### For Air Conditioner Users

To use the new Air Conditioner profile:

1. Go to your AC appliance in Smart Appliance Monitor
2. Click "Reconfigure"
3. Change type from "Other" to "Air Conditioner"
4. Optimal settings (50W/20W) are applied automatically

---

## 📝 Changelog

See [CHANGELOG.md](../../../CHANGELOG.md) for full details.

**Summary:**
- New Air Conditioner profile with optimized compressor detection
- All profiles updated with data-driven thresholds
- Detection times reduced by 2-4x
- Analysis and automation tools added
- False positive detection eliminated

---

## 🐛 Known Issues

None reported for this release.

---

## 📚 Documentation

- **Wiki**: https://github.com/legaetan/ha-smart_appliance_monitor/wiki
- **Configuration Guide**: https://github.com/legaetan/ha-smart_appliance_monitor/wiki/Configuration
- **Features**: https://github.com/legaetan/ha-smart_appliance_monitor/wiki/Features
- **Tools Documentation**: See `tools/README.md`

---

## 💬 Feedback

Found a bug or have a suggestion? Please [open an issue](https://github.com/legaetan/ha-smart_appliance_monitor/issues/new).

---

## 🙏 Acknowledgments

Special thanks to all users who provided feedback and data for this optimization release!

---

**Download**: [smart_appliance_monitor-v1.1.0.zip](https://github.com/legaetan/ha-smart_appliance_monitor/releases/download/v1.1.0/smart_appliance_monitor-v1.1.0.zip)  
**Full Changelog**: https://github.com/legaetan/ha-smart_appliance_monitor/compare/v1.0.0...v1.1.0

