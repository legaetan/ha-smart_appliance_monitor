# Smart Appliance Monitor v0.5.5 - Critical Bug Fixes

## 🐛 Critical Bug Fixes Release

This release fixes **two critical errors** from v0.5.4 that prevented the integration from loading and caused runtime failures.

## ✅ What's Fixed

### 1. StaticPathConfig API Error
- **Error Fixed**: `AttributeError: 'dict' object has no attribute 'url_path'`
- **Issue**: Using dict instead of `StaticPathConfig` object for frontend resource registration
- **Solution**: Properly import and use `StaticPathConfig` from Home Assistant HTTP component
- **Impact**: Integration now loads successfully and cards are properly registered

### 2. Missing set_enabled Method
- **Error Fixed**: `AttributeError: 'SmartApplianceNotifier' object has no attribute 'set_enabled'`
- **Issue**: Method missing from `SmartApplianceNotifier` class
- **Solution**: Added `set_enabled()` method to control global notification state
- **Impact**: State restoration works correctly, notification switches function properly

## 🔍 Errors That Were Fixed

If you saw these errors in your logs from v0.5.4:

```
AttributeError: 'dict' object has no attribute 'url_path'
```

```
AttributeError: 'SmartApplianceNotifier' object has no attribute 'set_enabled'
```

**These are now completely fixed in v0.5.5!** ✅

## 📦 Installation

### Via HACS (Recommended)
1. Update Smart Appliance Monitor to **v0.5.5** in HACS
2. **Restart Home Assistant**
3. Check logs - no more errors!
4. All features now work correctly

### Manual Installation
Download `smart_appliance_monitor-v0.5.5.zip` and extract to your `custom_components` directory.

## ✨ After Update

After updating to v0.5.5 and restarting:

✅ **Integration loads without errors**  
✅ **Cards are properly registered at `/hacsfiles/smart-appliance-cards/`**  
✅ **State restoration works correctly**  
✅ **Notification switches function properly**  
✅ **All appliance monitors work correctly**  
✅ **All features fully functional**  

## 🎯 How to Use the Cards

After installation, add the resources to Lovelace (one-time setup):

1. Go to **Settings** → **Dashboards** → **Resources**
2. Click **+ Add Resource**
3. Add both cards:

**Cycle Card:**
- URL: `/hacsfiles/smart-appliance-cards/smart-appliance-cycle-card.js`
- Resource type: **JavaScript Module**

**Stats Card:**
- URL: `/hacsfiles/smart-appliance-cards/smart-appliance-stats-card.js`
- Resource type: **JavaScript Module**

4. Clear browser cache (Ctrl+Shift+R)
5. Cards are ready to use!

## 📝 Full Changelog

### Fixed

#### Critical Bug Fixes
- **Fixed StaticPathConfig API usage** - Corrected frontend resource registration
  - Changed from dict to `StaticPathConfig` object for `async_register_static_paths()`
  - Fixed `AttributeError: 'dict' object has no attribute 'url_path'` error
  - Cards now properly registered without errors
  
- **Fixed missing set_enabled method** - Added global notification toggle
  - Added `set_enabled()` method to `SmartApplianceNotifier` class
  - Fixed `AttributeError: 'SmartApplianceNotifier' object has no attribute 'set_enabled'`
  - State restoration now works correctly
  - Notification switches now function properly

### Technical Details

**Files Modified:**
- `custom_components/smart_appliance_monitor/__init__.py` - Added `StaticPathConfig` import and usage
- `custom_components/smart_appliance_monitor/notify.py` - Added `set_enabled()` method

**Breaking Changes:** None

**Migration Notes:** 
- Users who installed v0.5.4: Update to v0.5.5 to fix all startup and runtime errors
- Integration will load successfully and all features will work correctly
- State restoration from previous sessions now works without errors

## 📚 Documentation

For complete documentation, see:
- [Installation Guide](https://github.com/legaetan/ha-smart_appliance_monitor/wiki/Installation)
- [Cards Documentation](https://github.com/legaetan/ha-smart_appliance_monitor/tree/main/custom_components/smart_appliance_monitor/www/smart-appliance-cards)
- [Full Changelog](https://github.com/legaetan/ha-smart_appliance_monitor/blob/main/CHANGELOG.md)

## 🐛 Bug Reports

Found a bug? Please [open an issue](https://github.com/legaetan/ha-smart_appliance_monitor/issues).

---

**Full Changelog**: [v0.5.4...v0.5.5](https://github.com/legaetan/ha-smart_appliance_monitor/compare/v0.5.4...v0.5.5)

