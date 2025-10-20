# Release Summary v0.5.1

**Date**: October 20, 2025  
**Type**: Patch Release (Bug Fix + Feature)

## 🎯 Main Objective

Resolve **data loss during Home Assistant restarts** by implementing a complete state persistence system.

## ✨ Key Feature

### State Persistence

Automatic save and restore system that preserves:
- ✅ Running cycles (state, start time, energy, power)
- ✅ Last completed cycle (duration, energy, cost)
- ✅ Daily statistics (date, counter, energy, cost)
- ✅ Monthly statistics (year, month, energy, cost)
- ✅ Cycle history (for anomaly detection)
- ✅ Configuration (monitoring, notifications)

## 📊 Statistics

### Code
- **3 files created**: `docs/PERSISTENCE.md`, `RESUME_PERSISTANCE.md`, `tests/test_persistence.py`
- **2 files modified**: `__init__.py` (+4 lines), `coordinator.py` (+186 lines)
- **612 lines added** in total
- **11 unit tests** added

### Documentation
- **README.md**: Added "State Persistence" section in Advanced Features
- **CHANGELOG.md**: Version 0.5.1 with complete details
- **Wiki**: 
  - `Home.md`: Version updated to 0.5.1
  - `Features.md`: Persistence section + entity count update
- **RELEASE_NOTES_v0.5.1.md**: Complete release notes (353 lines)

## 🔧 Implementation

### Automatic Save
- At cycle start
- At cycle end
- Every 30 seconds (during cycle)

### Smart Restore
- At Home Assistant startup
- Data validation (reset if obsolete)
- Robust error handling

### Storage
- Location: `.storage/smart_appliance_monitor.<entry_id>.json`
- Format: JSON with ISO 8601 serialization
- Version: 1 (prepared for future migrations)
- Size: < 5 KB per appliance

## 🎯 User Benefits

1. **No data loss** during HA restarts
2. **Accurate statistics** even after interruptions
3. **Total transparency**: automatic invisible operation
4. **Increased reliability**: anomaly detection preserved

## ✅ Compatibility

- ✅ **100% backward compatible** with v0.5.0
- ✅ **No user action required**
- ✅ **Automatic migration**: works immediately
- ✅ **No breaking changes**

## 📦 Deliverable

- **Archive**: `smart_appliance_monitor-0.5.1.zip`
- **Size**: 60 KB
- **SHA256**: `a040c5b0ff758ff78d368a6c727806f3e017277368efea676bb359b3f0740512`

## 🔍 Tests

### Test Suite
- ✅ 11 persistence tests
- ✅ Serialization/deserialization tests
- ✅ Save/restore tests
- ✅ Data validation tests
- ✅ Automatic trigger tests

### Manual Testing
Validated scenarios:
1. ✅ Cycle interrupted by HA restart → Correct restoration
2. ✅ Statistics preserved after restart → OK
3. ✅ History maintained for anomalies → OK
4. ✅ Automatic reset of obsolete stats → OK

## 📝 Documentation Created

### Technical
- **docs/PERSISTENCE.md** (183 lines) - Complete system documentation

### User
- **RELEASE_NOTES_v0.5.1.md** (353 lines) - Detailed release notes
- **RESUME_PERSISTANCE.md** (150 lines) - Implementation summary in French

### Updates
- **README.md** - Persistence section added
- **CHANGELOG.md** - Version 0.5.1 documented
- **Wiki** - Home.md and Features.md updated

## 🐛 Bugs Fixed

| Bug | Status |
|-----|--------|
| Lost running cycles during HA restart | ✅ Fixed |
| Incorrect durations after restart | ✅ Fixed |
| Reset statistics during restart | ✅ Fixed |
| Lost history for anomaly detection | ✅ Fixed |

## 🚀 Next Steps

### v0.6.0 (Q4 2025)
- Custom Lovelace cards
- Strict mode for scheduling
- Advanced graphs
- Automatic multi-tariff

## 📞 Links

- **Repository**: https://github.com/legaetan/ha-smart_appliance_monitor
- **Issues**: https://github.com/legaetan/ha-smart_appliance_monitor/issues
- **Wiki**: https://github.com/legaetan/ha-smart_appliance_monitor/wiki
- **Releases**: https://github.com/legaetan/ha-smart_appliance_monitor/releases

## 🎉 Conclusion

v0.5.1 is a **critical stability release** that resolves a major data loss issue. It significantly improves integration reliability without any impact on existing user experience.

**Status**: ✅ Ready for production  
**Recommendation**: Update recommended for all v0.5.0 users
