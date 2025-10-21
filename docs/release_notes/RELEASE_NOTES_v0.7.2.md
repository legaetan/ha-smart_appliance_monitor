# Release Notes v0.7.2 - Bug Fixes & Documentation

**Release Date**: October 21, 2025

## Overview

Version 0.7.2 is a **critical bug fix release** that resolves the service registration issue preventing AI services from loading when upgrading from v0.6.0 to v0.7.0. This release also includes comprehensive wiki documentation for all AI-powered features introduced in v0.7.0.

**⚠️ Important**: If you installed v0.7.0 or v0.7.1, please update to v0.7.2 and restart Home Assistant to access all AI services.

## 🐛 Critical Bug Fixes

### Service Registration Issue

**Problem**: Users upgrading from v0.6.0 to v0.7.0/v0.7.1 could not access the three new AI services:
- `smart_appliance_monitor.configure_ai`
- `smart_appliance_monitor.analyze_cycles`
- `smart_appliance_monitor.analyze_energy_dashboard`

**Root Cause**: The integration checked if the `start_cycle` service existed before registering services. Since this service was present in v0.6.0, the code assumed all services were already registered and skipped registration of the new v0.7.0 AI services.

**Solution**: Changed the check to look for `configure_ai` service instead. Now when updating to v0.7.2, the integration correctly detects that AI services are missing and registers all 13 services.

**Code Change** (`__init__.py` line 161):
```python
# Before (v0.7.0/v0.7.1)
if not hass.services.has_service(DOMAIN, "start_cycle"):
    await async_setup_services(hass)

# After (v0.7.2)
if not hass.services.has_service(DOMAIN, "configure_ai"):
    await async_setup_services(hass)
    _LOGGER.info("Smart Appliance Monitor services registered (13 services including AI)")
```

**Impact**: 
- ✅ All 13 services now properly available after updating
- ✅ No data loss or configuration changes required
- ✅ Existing configurations preserved
- ✅ Simple Home Assistant restart fixes the issue

---

## 📚 Documentation Enhancements

### New: AI-Powered Analysis Wiki Page

Created comprehensive wiki documentation for all AI features introduced in v0.7.0:

**Location**: `docs/wiki-github/AI-Analysis.md` (500+ lines)

**Contents**:
- **Overview** - Complete introduction to AI analysis capabilities
- **Prerequisites** - Setup guide for OpenAI, Claude, Ollama, and Google AI
- **Configuration** - Global AI setup with `configure_ai` service
- **Services** - Detailed documentation for all 3 AI services
- **Sensors** - AI analysis sensor attributes and usage
- **Examples** - 10+ automation examples for various use cases
- **Cost Considerations** - Cloud vs local AI comparison with cost estimates
- **Troubleshooting** - Solutions for common issues

**Key Sections**:

#### Service Documentation
- `configure_ai` - Set up AI globally with examples
- `analyze_cycles` - Analyze individual appliances
- `analyze_energy_dashboard` - Analyze entire home

Each service includes:
- Parameter descriptions and options
- Complete YAML examples
- Expected responses
- Use case scenarios

#### Automation Examples
1. Weekly appliance analysis
2. Daily dashboard reports
3. Auto-analysis after long cycles
4. Efficiency alerts
5. Monthly savings reports

#### Troubleshooting Guide
- Service not found → Update to v0.7.2
- AI Task entity not recognized → Configuration steps
- Analysis fails → Multiple solutions with diagnostics
- No notification received → Notification settings check
- Analysis takes too long → Performance optimization tips

### Updated: Wiki Sidebar

**Change**: Added new "Energy & AI (v0.6.0+)" section

**Before**:
```markdown
**Advanced Features (v0.5.0+)**
* [Advanced Features Overview](Advanced-Features)
* [Energy Management](Energy-Management)
* [Usage Scheduling](Scheduling)
* [Data Export](Data-Export)
```

**After**:
```markdown
**Advanced Features (v0.5.0+)**
* [Advanced Features Overview](Advanced-Features)
* [Energy Management](Energy-Management)
* [Usage Scheduling](Scheduling)
* [Data Export](Data-Export)

**Energy & AI (v0.6.0+)**
* [Energy Dashboard Integration](Energy-Dashboard)
* [AI-Powered Analysis](AI-Analysis)
```

### Updated: Features.md Page

**Added**:
- v0.7.0 features section with AI capabilities
- v0.6.0 features section with Energy Dashboard
- Updated entity counts (32 entities per appliance)
- Cross-references to new wiki pages

**Entity Count Update**:
- **v0.5.0**: 30 entities per appliance
- **v0.7.0**: 32 entities per appliance
  - +1 sensor: AI analysis sensor
  - +1 switch: AI analysis enable/disable switch

### Links Verification

All internal wiki links have been verified:
- ✅ Cross-references between pages work
- ✅ Sidebar navigation functional
- ✅ External GitHub links valid
- ✅ Service documentation references correct

---

## 🔄 Migration Guide

### From v0.7.0 or v0.7.1

**Steps**:
1. Update integration to v0.7.2 via HACS
2. **Restart Home Assistant** (required)
3. Verify services are available:
   - Go to Developer Tools → Services
   - Search for "smart_appliance_monitor"
   - Should see all 13 services including `configure_ai`

**No other action required**:
- Configurations preserved
- Data intact
- Settings unchanged

### From v0.6.0 or Earlier

**Recommended**: Update directly to v0.7.2 (skip v0.7.0/v0.7.1)

**Steps**:
1. Update integration to v0.7.2 via HACS
2. Restart Home Assistant
3. Configure AI analysis:
   ```yaml
   service: smart_appliance_monitor.configure_ai
   data:
     ai_task_entity: ai_task.openai_ai_task
     enable_ai_analysis: true
     ai_analysis_trigger: manual
   ```
4. Read the [AI-Powered Analysis Guide](https://github.com/legaetan/ha-smart_appliance_monitor/wiki/AI-Analysis)

---

## 📊 Complete Service List

After updating to v0.7.2, all 13 services are available:

**Core Services (v0.2.0)**:
1. `start_cycle` - Manual cycle start
2. `stop_monitoring` - Disable monitoring
3. `reset_statistics` - Clear stats

**Dashboard & Export (v0.3.0 - v0.5.0)**:
4. `generate_dashboard_yaml` - Generate Lovelace dashboard
5. `export_to_csv` - Export data to CSV
6. `export_to_json` - Export data to JSON
7. `force_shutdown` - Manual auto-shutdown trigger

**Energy Dashboard (v0.6.0)**:
8. `sync_with_energy_dashboard` - Check Energy Dashboard sync
9. `export_energy_config` - Export Energy Dashboard config
10. `get_energy_data` - Retrieve aggregated energy data

**AI Analysis (v0.7.0)**:
11. `configure_ai` - Configure global AI settings ⭐ **NEW**
12. `analyze_cycles` - Analyze appliance cycles with AI ⭐ **NEW**
13. `analyze_energy_dashboard` - Analyze home energy with AI ⭐ **NEW**

---

## 🧪 Testing Recommendations

### Verify Services Available

```yaml
# Test in Developer Tools → Services
service: smart_appliance_monitor.configure_ai
data:
  ai_task_entity: ai_task.openai_ai_task
  enable_ai_analysis: false  # Just testing service availability
```

**Expected**: Service executes successfully, notification sent

### Test AI Analysis (if configured)

```yaml
# Prerequisite: Configure an AI Task entity first
service: smart_appliance_monitor.analyze_cycles
data:
  entity_id: sensor.washing_machine_state
  analysis_type: pattern
  cycle_count: 5
```

**Expected**: Analysis completes in 10-30 seconds, notification received

### Check Logs

```bash
# Look for service registration message
tail -f /config/home-assistant.log | grep "Smart Appliance Monitor services registered"
```

**Expected**: Log message appears after restart

---

## 📝 Technical Details

### Files Modified

| File | Change | Lines |
|------|--------|-------|
| `__init__.py` | Service registration fix | 3 |
| `manifest.json` | Version bump to 0.7.2 | 1 |
| `CHANGELOG.md` | v0.7.2 section added | 72 |
| `AI-Analysis.md` | NEW wiki page | 527 |
| `_Sidebar.md` | Added Energy & AI section | 5 |
| `Features.md` | Added v0.7.0 and v0.6.0 sections | 20 |
| `RELEASE_NOTES_v0.7.2.md` | This file | 300+ |

**Total**: ~928 lines modified/added

### Code Quality

- ✅ No breaking changes
- ✅ Backward compatible with v0.7.0 and v0.7.1
- ✅ No database migrations required
- ✅ All existing features functional
- ✅ Type hints maintained
- ✅ Logging enhanced for debugging

---

## 🎯 What This Release Fixes

### Before v0.7.2

**Scenario**: User with v0.6.0 updates to v0.7.0
- ❌ AI services not registered
- ❌ `configure_ai` service not found
- ❌ Developer Tools shows only 10 services
- ❌ Error: "Action smart_appliance_monitor.configure_ai introuvable"
- ❌ AI features completely inaccessible

### After v0.7.2

**Scenario**: User with v0.6.0 updates to v0.7.2
- ✅ All 13 services properly registered
- ✅ `configure_ai` service available
- ✅ Developer Tools shows all services
- ✅ AI features fully functional
- ✅ Complete documentation available

---

## 🚀 Next Steps

### For New Users

1. Install Smart Appliance Monitor v0.7.2 via HACS
2. Configure an appliance
3. (Optional) Set up AI Task integration
4. (Optional) Configure AI analysis
5. Read the wiki: [Getting Started](https://github.com/legaetan/ha-smart_appliance_monitor/wiki/Home)

### For Existing Users

1. Update to v0.7.2 via HACS
2. Restart Home Assistant
3. Explore AI features: [AI Guide](https://github.com/legaetan/ha-smart_appliance_monitor/wiki/AI-Analysis)
4. Set up Energy Dashboard sync: [Energy Guide](https://github.com/legaetan/ha-smart_appliance_monitor/wiki/Energy-Dashboard)

---

## 🐛 Known Issues

None at this time. All v0.7.0 features are now fully functional.

---

## 💬 Support & Feedback

- **Report Bugs**: [GitHub Issues](https://github.com/legaetan/ha-smart_appliance_monitor/issues)
- **Request Features**: [GitHub Discussions](https://github.com/legaetan/ha-smart_appliance_monitor/discussions)
- **Get Help**: [Home Assistant Community Forum](https://community.home-assistant.io/)
- **Documentation**: [Wiki](https://github.com/legaetan/ha-smart_appliance_monitor/wiki)

---

## 🙏 Thank You

Thank you to the users who reported the service registration issue and helped test the fix. Your feedback makes this integration better for everyone!

---

**Enjoy reliable AI-powered energy monitoring!** 🤖⚡

*Smart Appliance Monitor v0.7.2 - Making your home smarter, one appliance at a time.*

