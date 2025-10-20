# Dashboard Templates

Pre-configured Lovelace dashboard templates for Smart Appliance Monitor.

## Overview

This folder contains YAML templates for creating beautiful, functional dashboards for each appliance type. Each template includes:

- **Status card**: Current state with visual indicators
- **Statistics cards**: Duration, energy, cost
- **Control switches**: Monitoring and notifications
- **History graph**: Power consumption over time
- **Cost tracking**: Daily and monthly costs

## Available Templates

- `generic.yaml` - Universal template for any appliance
- `washing_machine.yaml` - Optimized for washing machines
- `dishwasher.yaml` - Optimized for dishwashers
- `monitor.yaml` - For screens/monitors (session-based)
- `nas.yaml` - For NAS devices (session-based)
- `printer_3d.yaml` - For 3D printers (long durations)
- `vmc.yaml` - For ventilation systems (session-based)

## Usage

### Option 1: Automatic (Using Service)

Use the `smart_appliance_monitor.create_dashboard` service to automatically create a dashboard:

```yaml
service: smart_appliance_monitor.create_dashboard
data:
  entity_id: sensor.washing_machine_state
  use_custom_cards: true  # Use custom cards if available
```

This will:
1. Detect the appliance type
2. Load the appropriate template
3. Replace all entity IDs with your appliance's entities
4. Create a new dashboard or update existing one
5. Return the dashboard URL

### Option 2: Manual Copy-Paste

1. Open the template file for your appliance type
2. Copy the entire YAML content
3. In Home Assistant:
   - Go to **Settings** → **Dashboards**
   - Click **+ Add Dashboard**
   - Choose **Start from scratch**
   - Add a new view
   - Click **⋮** → **Raw configuration editor**
   - Paste the YAML
4. **Important**: Replace all placeholder entity IDs:
   - Find: `{APPLIANCE_ID}` (e.g., `washing_machine`)
   - Replace with your actual entity IDs

**Example replacements**:
- `sensor.{APPLIANCE_ID}_state` → `sensor.washing_machine_state`
- `sensor.{APPLIANCE_ID}_cycle_duration` → `sensor.washing_machine_cycle_duration`
- etc.

## Custom Cards

Templates support two modes:

### Standard Mode (use_custom_cards: false)
Uses only built-in Home Assistant cards:
- `entities` card
- `sensor` card
- `history-graph` card
- `gauge` card

**Pros**: Works immediately, no additional installation
**Cons**: Less visual appeal, fewer features

### Custom Cards Mode (use_custom_cards: true)
Uses community custom cards for enhanced visuals:
- [mini-graph-card](https://github.com/kalkih/mini-graph-card) - Beautiful graphs
- [button-card](https://github.com/custom-cards/button-card) - Stylish buttons
- [mushroom-cards](https://github.com/piitaya/lovelace-mushroom) - Modern UI
- `smart-appliance-cycle-card` - Our custom cycle card
- `smart-appliance-stats-card` - Our custom statistics card

**Pros**: Beautiful, modern interface with animations
**Cons**: Requires HACS and card installation

## Installing Custom Cards

### Via HACS (Recommended)

1. Open HACS in Home Assistant
2. Go to **Frontend**
3. Click **Explore & Download Repositories**
4. Search and install:
   - "Mini Graph Card"
   - "Button Card"
   - "Mushroom Cards"

### Our Custom Cards

1. Copy files from `/www/smart-appliance-cards/` to your `<config>/www/` folder:
   ```bash
   cp -r www/smart-appliance-cards/ <your-ha-config>/www/
   ```

2. In Home Assistant, go to **Settings** → **Dashboards** → **Resources**

3. Add resources:
   - URL: `/local/smart-appliance-cards/smart-appliance-cycle-card.js`
   - Type: JavaScript Module
   - URL: `/local/smart-appliance-cards/smart-appliance-stats-card.js`
   - Type: JavaScript Module

4. Restart Home Assistant

## Template Structure

Each template contains:

### 1. Header Section
```yaml
title: {Appliance Name}
icon: mdi:washing-machine
```

### 2. Status Overview
- Large state indicator (idle/running/finished)
- Current cycle/session progress
- Running time and energy

### 3. Current Cycle/Session
- Duration (with gauge)
- Energy consumption
- Estimated cost
- Running indicator

### 4. Controls
- Monitoring switch
- Notifications master switch
- Notification type switches (4)
- Reset statistics button

### 5. History & Statistics
- Power consumption graph (last 24h)
- Daily statistics
- Monthly statistics
- Last cycle/session data

### 6. Alerts
- Duration alert indicator
- Unplugged warning

## Customization

### Colors

Modify color schemes by editing the template:

```yaml
# Change state colors
style: |
  ha-card {
    {% if is_state('sensor.washing_machine_state', 'running') %}
      --primary-color: #4CAF50;  # Green for running
    {% elif is_state('sensor.washing_machine_state', 'finished') %}
      --primary-color: #2196F3;  # Blue for finished
    {% endif %}
  }
```

### Icons

Change icons per appliance type:

```yaml
icon: mdi:washing-machine  # Washing machine
icon: mdi:dishwasher       # Dishwasher
icon: mdi:tumble-dryer     # Dryer
icon: mdi:monitor          # Monitor
icon: mdi:nas              # NAS
icon: mdi:printer-3d       # 3D Printer
icon: mdi:fan              # VMC
```

### Layout

Reorder sections by moving YAML blocks:

```yaml
cards:
  - type: vertical-stack  # Section 1
    cards: [...]
  - type: vertical-stack  # Section 2
    cards: [...]
```

## Examples

### Minimal Dashboard

```yaml
title: Laundry Room
views:
  - title: Overview
    cards:
      - type: entities
        title: Washing Machine
        entities:
          - sensor.washing_machine_state
          - sensor.washing_machine_cycle_duration
          - switch.washing_machine_monitoring
```

### Multi-Appliance Dashboard

Combine multiple templates in one dashboard with tabs:

```yaml
title: Smart Appliances
views:
  - title: Washing Machine
    path: washing-machine
    # ... paste washing_machine.yaml content
  
  - title: Dishwasher
    path: dishwasher
    # ... paste dishwasher.yaml content
  
  - title: Dryer
    path: dryer
    # ... paste generic.yaml content with dryer entities
```

## Troubleshooting

### Cards not showing
- Check entity IDs are correct
- Verify entities exist in Developer Tools → States
- Check browser console for errors (F12)

### Custom cards missing
- Install via HACS
- Add resources in Dashboard Resources
- Clear browser cache (Ctrl+Shift+R)

### Graphs empty
- Ensure power sensor has history
- Wait for at least one data point (30s)
- Check recorder configuration

### Wrong icons
- Verify icon names at [Material Design Icons](https://pictogrammers.com/library/mdi/)
- Format: `mdi:icon-name`

## Tips

1. **Start with generic template**: Test with `generic.yaml` before specialized ones
2. **Use card-mod**: For advanced styling (requires card-mod via HACS)
3. **Mobile view**: Test on mobile - adjust card sizes if needed
4. **Performance**: Don't add too many graphs on one page
5. **Updates**: Templates may update with new versions - check changelog

## See Also

- [Home Assistant Dashboards](https://www.home-assistant.io/dashboards/) - Official documentation
- [Lovelace YAML](https://www.home-assistant.io/lovelace/yaml-mode/) - YAML mode guide
- [HACS](https://hacs.xyz/) - Home Assistant Community Store

---

**Version**: 0.3.0  
**Last Updated**: October 2025

