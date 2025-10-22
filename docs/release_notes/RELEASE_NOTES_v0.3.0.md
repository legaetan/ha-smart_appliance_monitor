# Smart Appliance Monitor v0.3.0 - Dashboard Templates

**Release Date**: October 20, 2025

## 🎨 Dashboard System

Version **0.3.0** introduces a complete **dashboard template system** with 7 pre-configured templates and automatic generation service.

## ✨ Key Features

### 7 Dashboard Templates
Pre-configured Lovelace YAML templates for every appliance type:
- **`generic.yaml`** - Universal template
- **`washing_machine.yaml`** - Optimized for 1-3h cycles
- **`dishwasher.yaml`** - Optimized for 2-4h cycles  
- **`monitor.yaml`** - For PC/displays (session-based, up to 8h)
- **`nas.yaml`** - For NAS devices (activity detection)
- **`printer_3d.yaml`** - For 3D printers (24h+ cycles)
- **`vmc.yaml`** - For ventilation (boost mode detection)

### Auto-Generation Service
New **`generate_dashboard_yaml`** service:
- Automatically detects appliance type
- Loads appropriate template
- Replaces all entity ID placeholders
- Sends persistent notification with YAML code
- Logs for easy copy-paste

### Dashboard Sections
Each dashboard includes 6 sections:
1. **Status Overview** - Visual state card with badges
2. **Current Cycle/Session** - Duration gauge, energy, cost
3. **Power Consumption** - 24h graph with Mini Graph Card
4. **Controls** - All switches and buttons
5. **Statistics** - Last cycle, daily, monthly
6. **Alerts** - Conditional warnings

### Custom Card Support
Templates integrate:
- **Mushroom Cards** - Modern UI
- **Mini Graph Card** - Power visualization
- **Conditional Cards** - Smart alerts
- **Template Cards** - Dynamic colors/icons

## 📦 Installation

### Via HACS
1. Update Smart Appliance Monitor to v0.3.0
2. Install custom cards (Mushroom, Mini Graph Card)
3. Generate dashboard with service:
   ```yaml
   service: smart_appliance_monitor.generate_dashboard_yaml
   data:
     entity_id: sensor.washing_machine_state
   ```
4. Copy YAML from notification to your dashboard

## 🔧 Technical Details

- **Templates Location:** `/dashboards/templates/`
- **Total YAML:** ~1,500 lines
- **Service:** `generate_dashboard_yaml`
- **Language:** English (EN) default, French (FR) in translations

**Breaking Changes:** None

---

**Version**: 0.3.0  
**Date**: October 20, 2025  
**Download**: [smart_appliance_monitor-v0.3.0.zip](https://github.com/legaetan/ha-smart_appliance_monitor/releases/download/v0.3.0/smart_appliance_monitor-v0.3.0.zip)

