# Build Guide - Smart Appliance Cards

## 🎯 Objective

This document explains how to compile the cards for production and install them in Home Assistant.

## 📋 Prerequisites

- Node.js v16+ and npm installed
- Access to Home Assistant server
- Write permissions to `/config/www/`

## 🔨 Build Steps

### 1. Install Dependencies

```bash
cd /workspace/www/smart-appliance-cards
npm install
```

**Expected**: Installation of all dependencies (lit, rollup, babel, etc.)

### 2. Production Build

```bash
npm run build
```

**Result**: Compiled files created in `dist/`:
- `dist/smart-appliance-cycle-card.js` (~50KB minified)
- `dist/smart-appliance-stats-card.js` (~50KB minified)

### 3. Verify Build

Check that files exist:
```bash
ls -lh dist/
```

Should display:
```
smart-appliance-cycle-card.js
smart-appliance-stats-card.js
```

### 4. Syntax Check (Optional)

```bash
npm run lint
```

Auto-fix errors:
```bash
npm run format
```

## 📦 Install in Home Assistant

### Option A: Local Installation (Development)

If Home Assistant is on the same machine:

```bash
# Create destination folder
mkdir -p /path/to/homeassistant/config/www/smart-appliance-cards/dist

# Copy compiled files
cp dist/*.js /path/to/homeassistant/config/www/smart-appliance-cards/dist/

# Copy examples too (optional)
cp -r examples /path/to/homeassistant/config/www/smart-appliance-cards/
```

### Option B: Remote Installation (Server)

If Home Assistant is on a remote server:

```bash
# Via SCP
scp -r dist/*.js user@homeassistant:/config/www/smart-appliance-cards/dist/

# Via SFTP
sftp user@homeassistant
> cd /config/www
> mkdir smart-appliance-cards
> cd smart-appliance-cards
> mkdir dist
> cd dist
> put dist/*.js
> bye
```

### Option C: Via Samba/SMB (Easiest)

1. Open Home Assistant network share
2. Navigate to `config/www/`
3. Create folder `smart-appliance-cards/dist/`
4. Manually copy `.js` files

## 🔧 Configure in Home Assistant

### 1. Add Resources

In Home Assistant:

1. **Settings** → **Dashboards**
2. Menu **⋮** → **Resources**
3. Click **+ Add Resource**

**First Resource - Cycle Card**:
- URL: `/local/smart-appliance-cards/dist/smart-appliance-cycle-card.js`
- Resource type: **JavaScript Module**

**Second Resource - Stats Card**:
- URL: `/local/smart-appliance-cards/dist/smart-appliance-stats-card.js`
- Resource type: **JavaScript Module**

### 2. Restart Home Assistant

**Important**: Restart HA after adding resources.

```bash
# Via interface
Settings → System → Restart

# Or via CLI
ha core restart
```

### 3. Clear Browser Cache

On each browser/device:
- **Windows/Linux**: Ctrl + Shift + R
- **Mac**: Cmd + Shift + R
- **Mobile**: Clear Companion app cache

## ✅ Verify Installation

### Test 1: JavaScript Console

Open console (F12) in browser and verify:

```javascript
// Should display version info
// "SMART-APPLIANCE-CYCLE-CARD v0.4.0"
// "SMART-APPLIANCE-STATS-CARD v0.4.0"
```

### Test 2: Add a Card

1. Go to a dashboard
2. Click **Edit Dashboard**
3. Click **+ Add Card**
4. Search for "Smart Appliance"

**Expected**: See appear:
- Smart Appliance Cycle Card
- Smart Appliance Stats Card

### Test 3: Basic Configuration

Add a card with minimal config:

```yaml
type: custom:smart-appliance-cycle-card
entity: sensor.washing_machine_state
```

**Expected**: Card displays without error

## 🐛 Troubleshooting

### Error: "Custom element doesn't exist"

**Cause**: Resources not loaded

**Solution**:
1. Check URL in Resources
2. Verify files exist
3. Restart HA
4. Clear browser cache

### Error: "Entity not found"

**Cause**: Incorrect entity ID

**Solution**:
1. Check in Developer Tools → States
2. Entity must be `sensor.xxx_state`
3. Smart Appliance Monitor must be installed

### Empty Card or Rendering Error

**Cause**: JavaScript error

**Solution**:
1. Open browser console (F12)
2. Look for red errors
3. Verify lit version (must be 3.x)

### Incorrect Styles

**Cause**: HA theme not loaded

**Solution**:
1. Verify HA theme is active
2. Try theme: 'light' or 'dark' in config
3. Clear browser cache

## 🚀 Development Mode

For real-time development and testing:

### 1. Watch Mode

```bash
npm run watch
```

Leave terminal open. Files are automatically recompiled on changes.

### 2. Symbolic Link (Linux/Mac)

Instead of copying, create a link:

```bash
ln -s /workspace/www/smart-appliance-cards/dist /path/to/homeassistant/config/www/smart-appliance-cards/dist
```

**Advantage**: Changes are immediately available after rebuild.

### 3. Development Cycle

1. Modify code in `src/`
2. Watch build automatically recompiles
3. Refresh browser (Ctrl+Shift+R)
4. Test changes

## 📊 Compiled File Structure

```
dist/
├── smart-appliance-cycle-card.js      # Cycle card compiled + minified
└── smart-appliance-stats-card.js      # Stats card compiled + minified
```

Each file contains:
- Main card code
- Configuration editor
- All utilities (helpers, formatters, constants)
- CSS styles
- Embedded lit-element dependency

**Size**: ~40-60 KB per file (minified)

## 🔍 Quality Verification

### Check Minification

```bash
# Files should be compact (no comments, minified code)
head -n 5 dist/smart-appliance-cycle-card.js
```

### Check Imports

```bash
# All imports should be resolved (no relative paths)
grep "import.*from" dist/*.js
```

**Expected**: No results (imports are bundled)

## 📝 Pre-Release Checklist

- [ ] `npm install` executed without errors
- [ ] `npm run build` successful
- [ ] `dist/*.js` files created
- [ ] File sizes < 100KB each
- [ ] No lint errors
- [ ] Manual tests in HA successful
- [ ] Documentation up to date
- [ ] YAML examples tested

## 🎉 Next Steps

Once build is verified:

1. **Test** all features
2. **Fix** any bugs
3. **Optimize** if needed
4. **Document** known issues
5. **Prepare** v0.4.0 release

## 💡 Tips

### Performance

- Cards use update interval of 1s (running) or 30s (idle)
- Limit cards per dashboard (max 10)
- Use compact mode on mobile

### Compatibility

- Home Assistant 2024.1+
- Modern browsers (Chrome 90+, Firefox 88+, Safari 14+)
- Mobile: iOS 14+, Android 10+

### Customization

- All HA themes are supported
- CSS Variables can be overridden
- See `src/styles/common-styles.js` for variables

---

**Last updated**: October 20, 2025  
**Version**: 0.4.0  
**Author**: Smart Appliance Monitor Team
