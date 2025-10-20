# Smart Appliance Monitor - Custom Cards

## Planned for Future Release

Custom Lovelace cards specifically designed for Smart Appliance Monitor are **planned for v0.4.0** or later.

### Planned Cards

#### 1. `smart-appliance-cycle-card.js`
**Purpose**: Display current cycle/session with visual progress

**Features** (planned):
- Animated cycle status (idle/running/finished)
- Real-time duration and energy display
- Mini power consumption graph
- Quick action buttons (stop monitoring, reset stats)
- Color-coded states
- Support for both cycle and session terminology

#### 2. `smart-appliance-stats-card.js`
**Purpose**: Comprehensive statistics display

**Features** (planned):
- Tabbed interface (Today / Week / Month)
- Comparative charts (energy, cost, duration)
- Trend indicators (↑ ↓ →)
- Cost breakdown visualizations
- Efficiency metrics

### Why Not in v0.2.0/v0.3.0?

Custom Lovelace cards require:
- JavaScript/TypeScript development
- lit-element framework knowledge
- Extensive testing across browsers
- Card editor configuration
- Distribution via HACS

To deliver quality features faster, we prioritized:
✅ Core functionality (unplugged detection, advanced notifications)
✅ Dashboard templates (using existing community cards)
✅ Service for easy dashboard generation

### Current Solution

The dashboard templates in `/dashboards/templates/` use popular, well-maintained community cards:
- **[Mushroom Cards](https://github.com/piitaya/lovelace-mushroom)** - Modern, beautiful UI
- **[Mini Graph Card](https://github.com/kalkih/mini-graph-card)** - Flexible graphs
- **[Button Card](https://github.com/custom-cards/button-card)** - Highly customizable buttons

These provide excellent visualization without custom card development.

### Installation Instructions (Future)

When custom cards are released, installation will be:

#### Via HACS (Recommended)
1. Open HACS
2. Go to Frontend
3. Search "Smart Appliance Monitor Cards"
4. Install

#### Manual
1. Copy files to `/config/www/smart-appliance-cards/`
2. Add resources in Dashboard Resources:
   - `/local/smart-appliance-cards/smart-appliance-cycle-card.js`
   - `/local/smart-appliance-cards/smart-appliance-stats-card.js`
3. Restart Home Assistant

### Contributing

Interested in developing these cards? Contributions are welcome!

**Skills needed**:
- JavaScript/TypeScript
- lit-element framework
- Home Assistant Lovelace card development
- UI/UX design

See [CONTRIBUTING.md](../../CONTRIBUTING.md) for guidelines.

### Timeline

- **v0.2.0** (Current): Core features, notifications, unplugged detection
- **v0.3.0**: Dashboard templates and generation service ✅
- **v0.4.0** (Target: Q1 2026): Custom cards development
- **v0.5.0**: HACS publication, ML features

### Alternatives

While waiting for custom cards, explore:
- [Lovelace Card Mod](https://github.com/thomasloven/lovelace-card-mod) - Style existing cards
- [ApexCharts Card](https://github.com/RomRider/apexcharts-card) - Advanced charting
- [Auto-entities Card](https://github.com/thomasloven/lovelace-auto-entities) - Dynamic card generation

### Mockups & Design

Design mockups for the planned cards will be shared on the GitHub Wiki and Discussions.

### Updates

Watch the [GitHub repository](https://github.com/legaetan/ha-smart_appliance_monitor) for updates on custom card development.

---

**Version**: 0.3.0  
**Status**: Planned for v0.4.0  
**Last Updated**: October 2025

