# Release Notes - Smart Appliance Monitor v0.9.1

**Release Date**: October 23, 2025  
**Type**: Minor Release - Dashboard Enhancement & Energy Integration

---

## 🎉 What's New

### Complete Dashboard Redesign

We've completely redesigned the dashboard system with a focus on organization, reusability, and comprehensive monitoring capabilities.

**Main Dashboard - 9 Dedicated Views**:

1. **Vue d'Ensemble** - Get a quick overview of all your appliances
   - Global metrics and active appliances counter
   - Real-time status cards for all 9 appliances
   - Top energy consumers of the day
   - Active alerts summary

2. **Monitoring** - Real-time monitoring dashboard
   - Live state indicators for all appliances
   - Power consumption graphs
   - Current power readings

3. **Détails Appareils** - Detailed view for each appliance
   - Individual cards with custom SAM components
   - Cycle/session statistics
   - Energy and cost tracking per appliance

4. **Énergie & Coûts** - Energy cost management
   - Daily and monthly cost tracking
   - Energy Dashboard integration status
   - Cost breakdown by appliance

5. **Analyse IA** - AI-powered insights
   - AI analysis controls for each appliance
   - Pattern detection results
   - Optimization recommendations
   - Comparative analysis

6. **Alertes & Anomalies** - Monitoring and alerts
   - Duration alerts configuration
   - Anomaly detection status
   - Alert history

7. **Gestion Énergie** - Energy management
   - Energy limits configuration
   - Budget tracking
   - Scheduling controls
   - Auto-shutdown features

8. **Contrôles Globaux** - Master controls
   - Global notification switches
   - Bulk appliance management
   - System-wide settings

9. **Export & Services** - Data export and advanced features
   - CSV/JSON export
   - Energy Dashboard sync
   - Advanced services access

### New Template System

**Generic Card Templates** (`_card_templates.yaml`):
- 11 reusable card templates for consistent design
- Easy customization and maintenance
- Reduced code duplication

**New Appliance Templates**:
- `water_heater.yaml` - For water heaters (Chauffe-Eau)
- `oven.yaml` - For ovens (Four)
- `dryer.yaml` - For clothes dryers (Sèche-Linge)
- `desktop.yaml` - For desktop PCs (Bureau PC)

**Updated Templates** (all now v1.0.0):
- `dishwasher.yaml` - 10 comprehensive sections
- `washing_machine.yaml` - 10 comprehensive sections
- `monitor.yaml` - 11 sections with session tracking
- `nas.yaml` - 12 sections for NAS monitoring
- `printer_3d.yaml` - 12 sections for 3D printer monitoring
- `vmc.yaml` - 13 sections for VMC/ventilation monitoring
- `generic.yaml` - Fully refactored with templates

### Enhanced Energy Dashboard Integration

**Smart Device Matching**:
The `sync_with_energy_dashboard` service now uses intelligent matching to find your appliances:

1. **Uses Real Sensors**: Now syncs with your actual smart plug energy sensors instead of SAM-generated sensors
2. **Fuzzy Matching**: Multiple strategies to match appliances:
   - Exact name match
   - Normalized name match (removes accents, handles hyphens)
   - Partial name match (Bambulab X1C ⊃ X1C)
   - Sensor pattern match (lave_linge_consommation ≈ lave_linge)

**Global Price Synchronization** ⭐ NEW:
- Automatically retrieves electricity price from Energy Dashboard
- Applies one global price to all appliances (as it should be!)
- Supports both dynamic price entities (`input_number.edf_price_kwh`) and static prices
- Detailed sync report shows:
  - Number of appliances synced
  - Applied price and source
  - List of synced devices

**Example Sync Report**:
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

## 🔧 Installation & Upgrade

### New Installation

1. Download `smart_appliance_monitor-v0.9.1.zip` from releases
2. Extract to `custom_components/smart_appliance_monitor/`
3. Restart Home Assistant
4. Add integration via UI: Settings → Devices & Services → Add Integration → Smart Appliance Monitor

### Upgrade from v0.9.0

1. Download and extract new version
2. Replace files in `custom_components/smart_appliance_monitor/`
3. (Optional) Copy dashboard templates from `dashboards/templates/` to your HA config
4. Restart Home Assistant
5. Click "Synchroniser Energy Dashboard" to sync prices

**Note**: No breaking changes. Fully backward compatible with v0.9.0.

---

## 📊 Using the New Dashboard

### Import Main Dashboard

1. Copy `dashboards/templates/sam-energy-dashboard.yaml` to your HA
2. Go to Settings → Dashboards
3. Create new dashboard or edit existing
4. Use "Raw Configuration Editor" and paste the YAML
5. Save and explore the 9 views!

### Import Individual Appliance Templates

Each template can be used standalone:

```yaml
# Example: Import washing machine template
# Copy dashboards/templates/washing_machine.yaml
# Customize the appliance name in the file
# Import as a dashboard view
```

### Using Card Templates

All templates now use the shared card template system:

1. Ensure `_card_templates.yaml` is in the same directory
2. Templates automatically reference common card designs
3. Customize once in `_card_templates.yaml`, applies everywhere

---

## 🔌 Energy Dashboard Integration Setup

### Step 1: Configure Energy Dashboard

**Settings → Dashboards → Energy**

1. Add your appliances' energy sensors:
   - Click "Add Consumption"
   - Select sensor (e.g., `sensor.lave_linge_consommation`)
   - Give it a name
   - Save

2. Configure energy price:
   - Edit Grid Consumption
   - Add Energy Price entity (e.g., `input_number.edf_price_kwh`)
   - Or enter static price
   - Save

### Step 2: Sync with SAM

In your SAM dashboard:
1. Click "Synchroniser Energy Dashboard" button
2. Check notification for sync status
3. All prices automatically updated!

**Result**: Your electricity price from Energy Dashboard is now applied to all SAM appliances automatically.

---

## 🐛 Bug Fixes

- Fixed Energy Dashboard sync to correctly identify appliances already configured
- Fixed price synchronization to apply uniformly to all appliances (global pricing)
- Removed external dependency on `custom:bar-card` for better compatibility

---

## 📖 Documentation

### New Documentation

- **Energy Dashboard Sync Guide**: `docs/ENERGY_DASHBOARD_SYNC.md`
  - Complete technical documentation
  - Device detection strategies
  - Price synchronization details
  - Troubleshooting guide

- **Dashboard Templates Guide**: `dashboards/README.md`
  - Template usage instructions
  - Custom cards documentation
  - Customization guide
  - Troubleshooting

### Updated Documentation

- **CHANGELOG.md**: Full version history
- **README.md**: Updated with v0.9.1 features

---

## 🔜 What's Next

We're continuously improving Smart Appliance Monitor! Upcoming features:

- **Tariff Schedule Sync**: Import peak/off-peak hours from Energy Dashboard
- **Historical Data Alignment**: Compare SAM stats with Energy Dashboard
- **Enhanced AI Analysis**: More intelligent pattern detection
- **Mobile Dashboard**: Optimized mobile interface

---

## 📝 Full Changelog

See [CHANGELOG.md](../CHANGELOG.md#091---2025-10-23) for complete technical details.

---

## 🤝 Contributing

Found a bug? Have a feature request?

- **GitHub Issues**: https://github.com/legaetan/ha-smart_appliance_monitor/issues
- **Wiki**: https://github.com/legaetan/ha-smart_appliance_monitor/wiki
- **Discussions**: Share your dashboards and configurations!

---

## 💙 Thank You

Thank you for using Smart Appliance Monitor! This release represents a major step forward in dashboard usability and Energy Dashboard integration.

If you find this integration useful, please consider:
- ⭐ Starring the repository
- 📣 Sharing with the Home Assistant community
- 📝 Contributing improvements

---

**Download**: [smart_appliance_monitor-v0.9.1.zip](../../releases/tag/v0.9.1)

**Previous Release**: [v0.9.0 Release Notes](RELEASE_NOTES_v0.9.0.md)

