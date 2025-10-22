# Smart Appliance Monitor v0.5.2 - Automatic Lovelace Cards Installation

## 🎉 What's New

This release brings **automatic installation** of custom Lovelace cards when you install or update Smart Appliance Monitor via HACS. No more manual build steps or complex setup!

## ✨ Key Features

### Automatic Cards Registration
- **Zero configuration required** - Cards are automatically registered when the integration loads
- **HACS compatible** - Cards available at `/hacsfiles/smart-appliance-cards/`
- **Pre-built assets** - No need to install Node.js or run build commands
- **Two beautiful cards included**:
  - `smart-appliance-cycle-card.js` - Real-time cycle monitoring
  - `smart-appliance-stats-card.js` - Comprehensive statistics

### Simplified Installation

After installing via HACS, simply add the cards as Lovelace resources (one-time setup):

1. Go to **Settings** → **Dashboards** → **Resources**
2. Add both cards:
   - `/hacsfiles/smart-appliance-cards/smart-appliance-cycle-card.js`
   - `/hacsfiles/smart-appliance-cards/smart-appliance-stats-card.js`
3. Clear browser cache and you're done!

## 📦 Installation

### Via HACS (Recommended)
1. Install or update Smart Appliance Monitor from HACS
2. Add the cards as resources (see above)
3. Start using the cards in your dashboards

### Manual Installation
Download `smart_appliance_monitor-v0.5.2.zip` and extract to your `custom_components` directory.

## 🔧 Changes

- **Added**: Frontend resource registration in `__init__.py`
- **Added**: Pre-compiled card assets in `www/smart-appliance-cards/dist/`
- **Changed**: Updated `.gitignore` to version compiled files
- **Changed**: Updated documentation with automatic installation instructions

## 📝 Technical Details

**Files Modified:**
- `custom_components/smart_appliance_monitor/__init__.py` - Added `_register_frontend_resources()` function
- `.gitignore` - Added exceptions for compiled card files
- `www/smart-appliance-cards/README.md` - Updated installation documentation
- `www/smart-appliance-cards/dist/` - Added pre-compiled cards (38KB + 43KB)

**Breaking Changes:** None

**Migration Notes:** 
- Existing installations: Cards will be automatically available after update
- Users must add resources to Lovelace once (see documentation)

## 📚 Documentation

For complete documentation, see:
- [Installation Guide](https://github.com/legaetan/ha-smart_appliance_monitor/wiki/Installation)
- [Cards Documentation](https://github.com/legaetan/ha-smart_appliance_monitor/tree/main/www/smart-appliance-cards)
- [Full Changelog](https://github.com/legaetan/ha-smart_appliance_monitor/blob/main/CHANGELOG.md)

## 🐛 Bug Reports

Found a bug? Please [open an issue](https://github.com/legaetan/ha-smart_appliance_monitor/issues).

---

**Full Changelog**: [v0.5.1...v0.5.2](https://github.com/legaetan/ha-smart_appliance_monitor/compare/v0.5.1...v0.5.2)

