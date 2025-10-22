# Release Notes - v0.8.1 - Documentation Update

**Release Date**: October 22, 2025  
**Type**: Documentation Release  
**Download**: [smart_appliance_monitor-v0.8.1.zip](https://github.com/legaetan/ha-smart_appliance_monitor/releases/tag/v0.8.1)

---

## 📚 Overview

Version 0.8.1 is a **documentation-focused release** that fixes numerous inconsistencies found during a comprehensive audit of the project documentation. No code changes were made - this release ensures all documentation accurately reflects the v0.8.0 codebase.

---

## 🔍 What Was Fixed

### Version Inconsistencies

**Problem**: Documentation showed outdated versions across multiple files  
**Fixed**:
- Wiki Home.md: Updated from v0.5.1 to v0.8.0
- README.md: Changed "Latest" indicator from v0.6.0 to v0.8.0
- Release notes index: Updated final version from v0.7.4 to v0.8.1
- All "What's New" sections now include v0.6.0, v0.7.0, and v0.8.0

### Entity Count Corrections

**Problem**: Features.md listed 32 entities but code has 33  
**Fixed**:
- Corrected count: 14 sensors per appliance + 1 global AI sensor = 15 total sensors
- Total entities: 33 (15 sensors + 7 binary sensors + 10 switches + 1 button)
- Documented the global `sensor.sam_energy_dashboard_ai_analysis` sensor

### Missing v0.8.0 Documentation

**Problem**: Cycle History System (v0.8.0) not documented in wiki  
**Fixed**:
- Created comprehensive **Cycle-History.md** wiki page (540+ lines)
- Added `get_cycle_history` service documentation with all parameters
- Added `import_historical_cycles` service documentation with examples
- Included warnings about `replace_existing` parameter
- Added to wiki sidebar navigation

### Incomplete File Structure

**Problem**: Installation.md missing new modules from v0.6.0-v0.8.0  
**Fixed**: Updated file structure to include:
- `ai_client.py` (v0.7.0)
- `history.py` (v0.8.0)
- `import_history.py` (v0.8.0)
- `energy_storage.py` (v0.6.0)
- `energy_dashboard.py` (v0.6.0)
- `storage_config.py` (v0.7.0)

---

## ✨ What Was Added

### New Wiki Page: Cycle-History.md

A complete guide for the Cycle History System featuring:

**Architecture**
- Hybrid storage model explanation
- 30 in-memory + unlimited in Recorder
- Data structure documentation

**Services Documentation**
- `get_cycle_history` with all parameters and examples
- `import_historical_cycles` with dry-run workflow
- Safety warnings for `replace_existing` parameter

**Use Cases**
1. Recover pre-installation data
2. Monthly cost reports
3. Efficiency analysis (before/after maintenance)
4. Anomaly investigation
5. Re-import with corrected thresholds

**Best Practices**
- Extend Recorder retention
- Always use dry-run first
- Import incrementally
- Regular backups

**Troubleshooting**
- No cycles found during import
- Import takes too long
- Duplicate cycles
- Incorrect cycle detection

**Events Documentation**
- `smart_appliance_monitor_cycle_history`
- `smart_appliance_monitor_import_completed`

### Enhanced README.md

**Added**:
- "Recent Improvements" section reorganized with v0.8.1, v0.8.0, and v0.7.x
- Complete service documentation for cycle history services
- Code examples with all parameters
- Feature highlights for each version

### Updated Wiki Navigation

**Added**:
- Cycle-History link in sidebar under "Energy & AI (v0.6.0+)"
- Better organization of advanced features by version

---

## 📝 Files Modified

### Documentation Files (9 files)

1. **docs/wiki-github/Home.md**
   - Version: 0.5.1 → 0.8.1
   - Added v0.8.1, v0.8.0, v0.7.0, v0.6.0 "What's New" sections
   - Corrected entity count (30 → 33)

2. **docs/wiki-github/Features.md**
   - Added "New in v0.8.0" section at top
   - Documented `get_cycle_history` and `import_historical_cycles` services
   - Corrected entity count (32 → 33)
   - Added global sensor documentation

3. **docs/wiki-github/Cycle-History.md** ⭐ **NEW**
   - 540+ lines of comprehensive documentation
   - Complete service reference
   - Use cases and best practices
   - Events and troubleshooting

4. **docs/wiki-github/_Sidebar.md**
   - Added Cycle-History link

5. **docs/wiki-github/Installation.md**
   - Updated file structure with all modules
   - Home Assistant version: 2024.1 → 2023.8

6. **docs/wiki-github/Advanced-Features.md**
   - Updated to reference v0.5.0 through v0.8.0
   - Added links to AI Analysis, Energy Dashboard, Cycle History

7. **README.md**
   - Reorganized "Recent Improvements" with correct version order
   - Added cycle history services documentation
   - Updated examples and code snippets

8. **docs/release_notes/README.md**
   - Added v0.8.1 entry
   - Updated "Latest version" indicator

9. **CHANGELOG.md**
   - Added v0.8.1 entry with all documentation changes

### Version Files (2 files)

1. **version** - 0.8.0 → 0.8.1
2. **custom_components/smart_appliance_monitor/manifest.json** - 0.8.0 → 0.8.1

---

## 📊 Documentation Audit Summary

### Issues Found and Fixed

| Category | Issues Found | Status |
|----------|-------------|--------|
| Version inconsistencies | 3 files | ✅ Fixed |
| Entity count errors | 1 file | ✅ Fixed |
| Missing v0.8.0 docs | 2 services | ✅ Fixed |
| Missing wiki pages | 1 page | ✅ Created |
| Incomplete file lists | 1 file | ✅ Updated |
| **TOTAL** | **12 major issues** | **✅ All Fixed** |

### Documentation Coverage

- ✅ All versions (v0.2.0 to v0.8.1) properly documented
- ✅ All 15 services documented with examples
- ✅ All 33 entities documented
- ✅ All advanced features cross-referenced
- ✅ Wiki navigation complete and consistent

---

## 🔄 Migration from v0.8.0

### Breaking Changes

**None** - This is a documentation-only release.

### Installation

Simply update to v0.8.1 - no configuration changes needed.

#### Via HACS

1. Open HACS in Home Assistant
2. Go to "Integrations"
3. Find "Smart Appliance Monitor"
4. Click "Update" to v0.8.1
5. No restart required (documentation only)

#### Manual Installation

1. Download `smart_appliance_monitor-v0.8.1.zip`
2. Extract to `custom_components/smart_appliance_monitor/`
3. No restart required (documentation only)

---

## 📚 Documentation Resources

### Updated Wiki Pages

- [Home](https://github.com/legaetan/ha-smart_appliance_monitor/wiki/Home) - Now shows v0.8.1
- [Features](https://github.com/legaetan/ha-smart_appliance_monitor/wiki/Features) - Complete entity reference
- [Cycle History](https://github.com/legaetan/ha-smart_appliance_monitor/wiki/Cycle-History) - NEW complete guide
- [AI Analysis](https://github.com/legaetan/ha-smart_appliance_monitor/wiki/AI-Analysis) - AI features
- [Energy Dashboard](https://github.com/legaetan/ha-smart_appliance_monitor/wiki/Energy-Dashboard) - Integration guide

### Main Documentation

- [README.md](https://github.com/legaetan/ha-smart_appliance_monitor/blob/main/README.md) - Project overview
- [CHANGELOG.md](https://github.com/legaetan/ha-smart_appliance_monitor/blob/main/CHANGELOG.md) - Version history
- [Release Notes Index](https://github.com/legaetan/ha-smart_appliance_monitor/blob/main/docs/release_notes/README.md) - All releases

---

## 🎯 Why This Release Matters

This release ensures that:

1. **New users** see accurate information about current features
2. **Existing users** can find complete documentation for all services
3. **Contributors** have consistent reference material
4. **Version numbers** are synchronized across all files
5. **Entity counts** match the actual codebase
6. **Wiki navigation** is complete and logical

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/legaetan/ha-smart_appliance_monitor/issues)
- **Discussions**: [GitHub Discussions](https://github.com/legaetan/ha-smart_appliance_monitor/discussions)
- **Wiki**: [Complete Documentation](https://github.com/legaetan/ha-smart_appliance_monitor/wiki)

---

## 🙏 Acknowledgments

Thank you for using Smart Appliance Monitor! This documentation update ensures everyone has access to accurate, comprehensive information about all features.

---

**Documentation matters - Happy monitoring!** 📚✨

