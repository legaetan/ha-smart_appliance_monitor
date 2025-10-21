# 🚀 Quick Start - Smart Appliance Cards

## Quick Installation

### 1. Build

```bash
cd /workspace/www/smart-appliance-cards
npm install
npm run build
```

### 2. Copy to Home Assistant

```bash
# Copy dist folder to Home Assistant
cp -r dist /path/to/homeassistant/config/www/smart-appliance-cards/
```

### 3. Add Resources in HA

Settings → Dashboards → Resources → Add Resource

**Resource 1**:
- URL: `/local/smart-appliance-cards/dist/smart-appliance-cycle-card.js`
- Type: JavaScript Module

**Resource 2**:
- URL: `/local/smart-appliance-cards/dist/smart-appliance-stats-card.js`
- Type: JavaScript Module

### 4. Restart HA and Clear Cache

- Restart Home Assistant
- Clear browser cache (Ctrl+Shift+R)

---

## Quick Usage

### Add a Card

In a dashboard:
1. Edit Dashboard
2. Add Card
3. Search for "Smart Appliance"

### Minimal Configuration

```yaml
type: custom:smart-appliance-cycle-card
entity: sensor.washing_machine_state
```

```yaml
type: custom:smart-appliance-stats-card
entity: sensor.washing_machine_state
```

---

## Full Documentation

- **README.md** - Complete user guide
- **examples/** - Configuration examples

---

**Version**: 0.4.0  
**Date**: October 20, 2025  
**Status**: ✅ Ready to use
