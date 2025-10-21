# Smart Appliance Monitor - Custom Cards

[![Version](https://img.shields.io/badge/version-0.4.0-blue.svg)](https://github.com/legaetan/ha-smart_appliance_monitor)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Custom Lovelace cards designed specifically for Smart Appliance Monitor integration.

## 🎉 Now Available - v0.4.0

Two beautiful, feature-rich custom cards to enhance your appliance monitoring experience in Home Assistant!

### Cards Included

#### 1. `smart-appliance-cycle-card` 
**Display current cycle/session with visual progress**

**Features**:
- ✅ Animated cycle status (idle/running/finished)
- ✅ Real-time duration and energy display
- ✅ Color-coded states with smooth animations
- ✅ Quick action buttons (start, stop monitoring, reset stats)
- ✅ Alert indicators (unplugged, duration exceeded)
- ✅ Support for both cycle and session terminology
- ✅ Visual configuration editor
- ✅ Auto-detection of appliance type

#### 2. `smart-appliance-stats-card`
**Comprehensive statistics with tabbed interface**

**Features**:
- ✅ Tabbed interface (Today / Week / Month)
- ✅ Statistics cards with icons (cycles, energy, cost, duration)
- ✅ Trend indicators with arrows (↑ ↓ →)
- ✅ Efficiency metrics section
- ✅ Visual configuration editor
- ✅ Responsive design (mobile & desktop)
- ✅ Adaptive terminology (cycle/session)

## 📸 Screenshots

*Screenshots will be added after testing in Home Assistant*

## 🎯 Quick Start

### Minimal Configuration

```yaml
# Cycle Card - Show current cycle status
type: custom:smart-appliance-cycle-card
entity: sensor.washing_machine_state

# Stats Card - Show statistics
type: custom:smart-appliance-stats-card
entity: sensor.washing_machine_state
```

That's it! The cards will auto-detect your appliance type, terminology, and all related entities.

## 📦 Installation

### Automatic Installation (Recommended)

**Good news!** If you installed the Smart Appliance Monitor integration via HACS, the custom cards are **automatically available** after installation. No manual setup required!

The cards are automatically registered at:
- `/hacsfiles/smart-appliance-cards/smart-appliance-cycle-card.js`
- `/hacsfiles/smart-appliance-cards/smart-appliance-stats-card.js`

#### Add Resources to Lovelace

After installing the integration, you just need to add the resources to Lovelace:

1. Go to **Settings** → **Dashboards**
2. Click the **⋮** menu → **Resources**
3. Click **+ Add Resource**
4. Add both cards:

**Cycle Card:**
- URL: `/hacsfiles/smart-appliance-cards/smart-appliance-cycle-card.js`
- Resource type: **JavaScript Module**

**Stats Card:**
- URL: `/hacsfiles/smart-appliance-cards/smart-appliance-stats-card.js`
- Resource type: **JavaScript Module**

5. Clear browser cache (Ctrl+Shift+R)
6. The cards are now ready to use!

### Manual Installation (Advanced Users)

If you want to install the cards separately or customize them:

#### Step 1: Install Dependencies
```bash
cd /path/to/homeassistant/config/www/smart-appliance-cards
npm install --no-bin-links  # Use --no-bin-links for remote filesystems
```

#### Step 2: Build the Cards
```bash
# If npm run build doesn't work due to symlink issues, use:
node node_modules/rollup/dist/bin/rollup -c
```

This creates the compiled files in the `dist/` folder:
- `dist/smart-appliance-cycle-card.js`
- `dist/smart-appliance-stats-card.js`

#### Step 3: Add Resources
In Home Assistant:
1. Go to **Settings** → **Dashboards**
2. Click the **⋮** menu → **Resources**
3. Click **+ Add Resource**
4. Add both cards:

**Cycle Card:**
- URL: `/local/smart-appliance-cards/dist/smart-appliance-cycle-card.js`
- Resource type: **JavaScript Module**

**Stats Card:**
- URL: `/local/smart-appliance-cards/dist/smart-appliance-stats-card.js`
- Resource type: **JavaScript Module**

5. Restart Home Assistant and clear browser cache (Ctrl+Shift+R)

## 🎨 Configuration

### Cycle Card Options

```yaml
type: custom:smart-appliance-cycle-card
entity: sensor.washing_machine_state  # Required

# Optional settings
name: "My Washing Machine"             # Override auto-detected name
icon: mdi:washing-machine              # Override auto-detected icon
show_power_graph: true                 # Show mini power graph (default: true)
show_action_buttons: true              # Show action buttons (default: true)
show_current_power: false              # Show current power value (default: false)
graph_hours: 0.5                       # Graph duration in hours (default: 0.5)
theme: auto                            # auto | light | dark (default: auto)
```

### Stats Card Options

```yaml
type: custom:smart-appliance-stats-card
entity: sensor.washing_machine_state  # Required

# Optional settings
name: "Statistics"                     # Override auto-detected name
icon: mdi:chart-box                    # Custom icon (default: mdi:chart-box)
default_tab: today                     # today | week | month (default: today)
show_trends: true                      # Show trend indicators (default: true)
show_efficiency: true                  # Show efficiency metrics (default: true)
chart_type: bar                        # bar | line (default: bar)
theme: auto                            # auto | light | dark (default: auto)
```

### Visual Editor

Both cards include a visual configuration editor! Just click "Show Code Editor" → "Show Visual Editor" in the Lovelace card settings.

## 📖 Examples

See the [`examples/`](examples/) folder for complete configuration examples:
- [`cycle-card-basic.yaml`](examples/cycle-card-basic.yaml) - Minimal cycle card setup
- [`cycle-card-advanced.yaml`](examples/cycle-card-advanced.yaml) - Advanced configurations
- [`stats-card-basic.yaml`](examples/stats-card-basic.yaml) - Minimal stats card setup
- [`stats-card-advanced.yaml`](examples/stats-card-advanced.yaml) - Complete dashboard examples

## 🔧 Development

### Setup Development Environment

```bash
cd /workspace/www/smart-appliance-cards
npm install
```

### Build for Production

```bash
npm run build
```

### Development Mode (Watch)

```bash
npm run watch
```

This will automatically rebuild the cards when you make changes.

### Project Structure

```
www/smart-appliance-cards/
├── src/
│   ├── cards/              # Card components
│   ├── utils/              # Helper functions
│   └── styles/             # CSS styles
├── dist/                   # Compiled output
├── examples/               # YAML examples
├── package.json
├── rollup.config.js
└── README.md
```

## 🐛 Troubleshooting

### Cards Not Showing

1. **Check Resources**: Ensure both cards are added in Dashboard Resources
2. **Clear Cache**: Hard refresh browser (Ctrl+Shift+R)
3. **Check Console**: Open browser console (F12) for errors
4. **Verify Entity**: Make sure the entity exists in Developer Tools → States

### Entity Not Found

The card requires a **state sensor** entity like `sensor.washing_machine_state`. Make sure:
- Smart Appliance Monitor integration is installed
- Appliance is configured correctly
- Entity name matches your configuration

### Styles Not Applied

1. Check that Home Assistant theme is loaded
2. Try different theme settings (auto/light/dark)
3. Clear browser cache

## 🤝 Contributing

Contributions are welcome! See [CONTRIBUTING.md](../../CONTRIBUTING.md) for guidelines.

**Helpful areas**:
- Adding real power graph implementation
- Improving chart visualizations
- Adding more configuration options
- Bug fixes and optimizations
- Documentation improvements

## 📋 Roadmap & Future Enhancements

For planned features and future enhancements, see [IDEAS.md](../../../../docs/IDEAS.md).

Current version includes:
- ✅ Basic cycle card implementation
- ✅ Basic stats card implementation
- ✅ Visual editors
- ✅ Auto-detection features
- ✅ Bilingual support (EN/FR)
- ✅ Automatic HACS installation

## 📄 License

MIT License - See [LICENSE](../../LICENSE) for details.

## 🙏 Acknowledgments

- Home Assistant community
- lit-element framework
- Smart Appliance Monitor users and testers

---

**Version**: 0.4.0  
**Status**: ✅ Available - Development Complete  
**Last Updated**: October 20, 2025

For more information, visit the [Smart Appliance Monitor repository](https://github.com/legaetan/ha-smart_appliance_monitor).

