# Smart Appliance Monitor v0.5.3 - HACS Installation Fix

## 🐛 Bug Fix Release

This release fixes a critical issue from v0.5.2 where custom Lovelace cards were **not being installed** when updating via HACS.

## ✅ What's Fixed

### HACS Installation Issue
- **Cards now properly installed** - Moved `www/` folder into the integration directory
- **Correct path resolution** - Updated code to use relative paths within the integration
- **HACS compatibility** - Repository structure now follows HACS best practices
- **Automatic installation works** - Cards are now correctly copied during HACS updates

### Technical Changes
- Moved `www/` from repository root to `custom_components/smart_appliance_monitor/www/`
- Updated `_register_frontend_resources()` to use `Path(__file__).parent / "www" / ...`
- Updated `.gitignore` paths to match new structure

## 📦 Installation

### Via HACS (Recommended)
1. Update Smart Appliance Monitor to v0.5.3 in HACS
2. Restart Home Assistant
3. Add the cards as Lovelace resources:
   - `/hacsfiles/smart-appliance-cards/smart-appliance-cycle-card.js`
   - `/hacsfiles/smart-appliance-cards/smart-appliance-stats-card.js`
4. Clear browser cache and start using the cards!

### Manual Installation
Download `smart_appliance_monitor-v0.5.3.zip` and extract to your `custom_components` directory.

## 🔍 For Users Who Installed v0.5.2

If you installed v0.5.2, the cards were not properly copied to your installation. Please:

1. Update to v0.5.3 via HACS
2. Restart Home Assistant
3. The cards will now be available at `/hacsfiles/smart-appliance-cards/`

## 📝 Full Changelog

### Fixed
- Fixed cards not being installed via HACS - Moved www/ folder into integration directory
- Updated path resolution in `_register_frontend_resources()` function
- Cards now properly installed when updating via HACS

### Technical Details

**Files Modified:**
- `custom_components/smart_appliance_monitor/__init__.py` - Updated www_path
- `.gitignore` - Updated paths to match new structure
- Repository structure - Moved `www/` folder into integration directory

**Breaking Changes:** None

**Migration Notes:** 
- Users who installed v0.5.2: Update to v0.5.3 to get cards automatically installed
- Cards will be available at `/hacsfiles/smart-appliance-cards/` after update

## 📚 Documentation

For complete documentation, see:
- [Installation Guide](https://github.com/legaetan/ha-smart_appliance_monitor/wiki/Installation)
- [Cards Documentation](https://github.com/legaetan/ha-smart_appliance_monitor/tree/main/custom_components/smart_appliance_monitor/www/smart-appliance-cards)
- [Full Changelog](https://github.com/legaetan/ha-smart_appliance_monitor/blob/main/CHANGELOG.md)

## 🐛 Bug Reports

Found a bug? Please [open an issue](https://github.com/legaetan/ha-smart_appliance_monitor/issues).

---

**Full Changelog**: [v0.5.2...v0.5.3](https://github.com/legaetan/ha-smart_appliance_monitor/compare/v0.5.2...v0.5.3)

