# Smart Appliance Monitor v0.5.4 - API Compatibility Fix

## 🐛 Critical Bug Fix

This release fixes a **critical startup error** from v0.5.3 that prevented the integration from loading due to incorrect Home Assistant API usage.

## ✅ What's Fixed

### AttributeError on Startup
- **Fixed integration loading error** - Updated to use correct async API method
- **Error resolved**: `AttributeError: 'HomeAssistantHTTP' object has no attribute 'register_static_path'`
- **Cards now properly registered** at `/hacsfiles/smart-appliance-cards/`
- **Integration loads successfully** without errors

### Technical Changes
- Changed `hass.http.register_static_path()` to `hass.http.async_register_static_paths()`
- Updated to use list of dictionaries format for path registration
- Compatible with Home Assistant 2023.8+

## 🔍 Error That Was Fixed

If you saw this error in your logs:
```
AttributeError: 'HomeAssistantHTTP' object has no attribute 'register_static_path'. 
Did you mean: 'async_register_static_paths'?
```

This is now fixed in v0.5.4!

## 📦 Installation

### Via HACS (Recommended)
1. Update Smart Appliance Monitor to v0.5.4 in HACS
2. **Restart Home Assistant**
3. Check logs - no more errors!
4. Add the cards as Lovelace resources (if not already done):
   - `/hacsfiles/smart-appliance-cards/smart-appliance-cycle-card.js`
   - `/hacsfiles/smart-appliance-cards/smart-appliance-stats-card.js`
5. Clear browser cache and start using the cards!

### Manual Installation
Download `smart_appliance_monitor-v0.5.4.zip` and extract to your `custom_components` directory.

## ✨ After Update

After updating to v0.5.4 and restarting:

1. ✅ Integration loads without errors
2. ✅ Cards are accessible at `/hacsfiles/smart-appliance-cards/`
3. ✅ All your appliance monitors work correctly
4. ✅ Add resources to Lovelace and use the beautiful cards!

## 📝 Full Changelog

### Fixed
- Fixed AttributeError on startup - Updated to use correct async API method
- Changed `hass.http.register_static_path()` to `hass.http.async_register_static_paths()`
- Cards now properly registered without errors
- Integration loads successfully on Home Assistant 2023.8+

### Technical Details

**Files Modified:**
- `custom_components/smart_appliance_monitor/__init__.py` - Updated to use `async_register_static_paths()` API

**Breaking Changes:** None

**Migration Notes:** 
- Users who installed v0.5.3: Update to v0.5.4 to fix startup errors
- Restart Home Assistant after update
- Cards will be properly registered at `/hacsfiles/smart-appliance-cards/`

## 📚 Documentation

For complete documentation, see:
- [Installation Guide](https://github.com/legaetan/ha-smart_appliance_monitor/wiki/Installation)
- [Cards Documentation](https://github.com/legaetan/ha-smart_appliance_monitor/tree/main/custom_components/smart_appliance_monitor/www/smart-appliance-cards)
- [Full Changelog](https://github.com/legaetan/ha-smart_appliance_monitor/blob/main/CHANGELOG.md)

## 🐛 Bug Reports

Found a bug? Please [open an issue](https://github.com/legaetan/ha-smart_appliance_monitor/issues).

---

**Full Changelog**: [v0.5.3...v0.5.4](https://github.com/legaetan/ha-smart_appliance_monitor/compare/v0.5.3...v0.5.4)

