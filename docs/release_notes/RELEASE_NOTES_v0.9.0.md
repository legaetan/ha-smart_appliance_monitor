# Release Notes - v0.9.0

**Release Date**: October 22, 2025

## 🚨 Important: Breaking Changes

**This release introduces breaking changes that require user action after upgrading.**

### Price Configuration Changed

**What changed:** Price configuration (electricity cost) is now **centralized and global** for all appliances. Per-appliance pricing has been removed.

**Why:** This change simplifies management, ensures consistency across all appliances, and enables advanced features like automatic tariff detection.

**Action Required:** After upgrading, you **must** configure global pricing once using the new `set_global_config` service:

```yaml
service: smart_appliance_monitor.set_global_config
data:
  global_price_entity: sensor.electricity_price  # Option 1: Dynamic price from a sensor
  global_price_fixed: 0.2516                      # Option 2: Fixed price per kWh
  enable_ai_analysis: true
  ai_analysis_trigger: manual
  ai_task_entity: ai_task.openai
```

**Migration Help:**
- A persistent notification will appear automatically after upgrade with detailed instructions
- Your cycle history and statistics are preserved
- Only the price configuration needs to be updated

### AI Analysis Changes

**"Comparative" Analysis Type Removed**

The `comparative` analysis type has been removed. Use these alternatives:
- `pattern` - Focus on usage patterns and trends
- `recommendations` - Concrete optimization recommendations
- `all` - Combined analysis with both patterns and recommendations

**Service Renamed**

- Old: `smart_appliance_monitor.configure_ai`
- New: `smart_appliance_monitor.set_global_config`

The old service still works but is deprecated and will log warnings. It will be removed in v1.0.0.

---

## ✨ New Features

### Global Configuration System

**Centralized Pricing and AI Settings**

Configure once, apply to all appliances:

```yaml
service: smart_appliance_monitor.set_global_config
data:
  # Price Configuration
  global_price_entity: sensor.electricity_price  # Dynamic from sensor
  global_price_fixed: 0.2516                      # Or fixed value as fallback
  
  # AI Configuration
  ai_task_entity: ai_task.openai
  enable_ai_analysis: true
  ai_analysis_trigger: manual
```

**Benefits:**
- Configure once instead of per appliance
- Consistent pricing across all appliances
- Simpler management
- Better automation capabilities

### Tariff Detection (Peak/Off-Peak)

**Automatic Detection of Electricity Tariff Structure**

New service `detect_tariff_system` analyzes your price history to detect peak/off-peak rates:

```yaml
service: smart_appliance_monitor.detect_tariff_system
```

**Features:**
- Analyzes 7 days of price history
- Automatically detects peak and off-peak rates
- Identifies transition hours (e.g., "06:00-22:00" for peak hours)
- Calculates estimated savings potential
- Results automatically used in AI analysis recommendations

**Example Results:**
```yaml
detected_type: peak_offpeak
peak_price: 0.25 EUR/kWh
offpeak_price: 0.18 EUR/kWh
transition_hours: [6, 22]
estimated_savings_potential: 3.5%
```

### Dynamic Currency Support

**Automatic Currency Detection**

Cost sensors now automatically use your Home Assistant configured currency:

**Before (v0.8.x):**
- Currency hardcoded to EUR
- All cost values shown in EUR regardless of location

**After (v0.9.0):**
- Currency from Home Assistant configuration (`hass.config.currency`)
- Automatic fallback to EUR if not configured
- Currency-specific icons (EUR, USD, GBP, CHF, JPY, CNY)

**Supported Currencies:**
- 🇪🇺 EUR - Euro (mdi:currency-eur)
- 🇺🇸 USD - US Dollar (mdi:currency-usd)
- 🇬🇧 GBP - British Pound (mdi:currency-gbp)
- 🇨🇭 CHF - Swiss Franc (mdi:currency-chf)
- 🇯🇵 JPY - Japanese Yen (mdi:currency-jpy)
- 🇨🇳 CNY - Chinese Yuan (mdi:currency-cny)

**Where It's Used:**
- All cost sensors (cycle cost, daily cost, monthly cost, total cost)
- AI analysis exports and prompts
- Event data (`smart_appliance_monitor_cycle_finished`)
- Statistics and reports

### Enhanced AI Analysis

**Tariff-Aware Prompts**

AI analysis now includes tariff context automatically:

```
Tariff System Information:
- Peak rate: 0.25 EUR/kWh (06:00-22:00)
- Off-peak rate: 0.18 EUR/kWh
- Estimated savings potential: 3.5%

Calculate potential cost savings by shifting usage to off-peak hours.
```

**Currency-Aware Recommendations**

AI uses your configured currency in all recommendations:

```yaml
analysis_type: recommendations
results:
  optimal_hours: ["22:00-06:00"]
  energy_savings_cost: "3.50 USD"  # Uses your currency
  tariff_aware: true
```

**Improved Analysis Types**

- `pattern`: Focuses exclusively on usage patterns, trends, and scheduling opportunities
- `recommendations`: Prioritizes concrete actions for optimization and cost savings
- `all`: Combined comprehensive analysis with both patterns and recommendations

### Real-Time Cost Calculation

**Accurate Cost Tracking During Cycles**

**Before (v0.8.x):**
- Cost calculated only at cycle end
- Price changes during cycle not reflected

**After (v0.9.0):**
- Cost recalculated in real-time as cycle progresses
- Uses current price at each update
- Final `cost_per_kwh` stored with cycle
- More accurate cost tracking

**Event Data Enhanced:**

```yaml
event: smart_appliance_monitor_cycle_finished
data:
  cost: 0.75
  cost_per_kwh: 0.2516
  currency: EUR
  energy: 3.0
```

---

## 🔧 Changes

### Services

**New Services:**
- `set_global_config` - Configure global pricing and AI settings
- `detect_tariff_system` - Analyze price history for tariff detection

**Deprecated Services:**
- `configure_ai` - Use `set_global_config` instead (will be removed in v1.0.0)

**Updated Services:**
- `analyze_cycles` - Removed `comparative` analysis type, kept `pattern`, `recommendations`, `all`

### Configuration

**Appliance Configuration Simplified:**

Removed from appliance setup:
- `price_entity` - Now global only
- `price_kwh` - Now global only

Kept in appliance setup:
- `appliance_name`
- `appliance_type`
- `power_sensor`
- `energy_sensor`
- All threshold and notification settings

### Sensors

**Cost Sensors Updated:**

All cost sensors now include:
- Dynamic unit of measurement based on configured currency
- Currency-specific icons
- Currency in attributes

Updated sensors:
- `sensor.<appliance>_cycle_cost`
- `sensor.<appliance>_last_cycle_cost`
- `sensor.<appliance>_daily_cost`
- `sensor.<appliance>_monthly_cost`

### AI Export Data

**Enhanced Export Structure:**

New `pricing_info` section in AI exports:

```yaml
pricing_info:
  current_price: 0.2516
  currency: EUR
  has_tariff_system: true
  tariff_type: peak_offpeak
  peak_price: 0.25
  offpeak_price: 0.18
  peak_hours: "06:00-22:00"
  estimated_savings_potential: 3.5
```

---

## 🐛 Fixes

- Fixed currency hardcoded to EUR in all cost sensors
- Fixed per-appliance pricing causing inconsistencies
- Fixed cost calculations not accounting for price changes during cycles
- Fixed AI prompts not including tariff information
- Fixed missing currency context in AI analysis

---

## 📚 Documentation Updates

- Added breaking changes notice in README.md
- Updated all service examples to use `set_global_config`
- Updated AI analysis documentation with new types
- Added currency support documentation
- Added tariff detection guide
- Updated French translations for all new features

---

## 🔄 Migration Guide

### Step 1: Upgrade to v0.9.0

```bash
# Copy new files to your Home Assistant
cp -r custom_components/smart_appliance_monitor /config/custom_components/
```

### Step 2: Restart Home Assistant

```bash
# Restart Home Assistant
# A persistent notification will appear with migration instructions
```

### Step 3: Configure Global Pricing

Option A - Using a Sensor (Recommended for Dynamic Pricing):
```yaml
service: smart_appliance_monitor.set_global_config
data:
  global_price_entity: sensor.electricity_price
  enable_ai_analysis: true
  ai_task_entity: ai_task.openai
```

Option B - Using Fixed Price:
```yaml
service: smart_appliance_monitor.set_global_config
data:
  global_price_fixed: 0.2516
  enable_ai_analysis: true
  ai_task_entity: ai_task.openai
```

### Step 4: (Optional) Detect Tariff System

If you have variable electricity pricing (peak/off-peak):

```yaml
service: smart_appliance_monitor.detect_tariff_system
```

This will analyze your price history and enhance AI recommendations.

### Step 5: Update Automations

If you used `configure_ai` in automations, update to `set_global_config`:

**Before:**
```yaml
service: smart_appliance_monitor.configure_ai
data:
  ai_task_entity: ai_task.openai
```

**After:**
```yaml
service: smart_appliance_monitor.set_global_config
data:
  ai_task_entity: ai_task.openai
  global_price_fixed: 0.2516
```

### Step 6: Update AI Analysis Calls

If you used `comparative` analysis type, switch to alternatives:

**Before:**
```yaml
service: smart_appliance_monitor.analyze_cycles
data:
  entity_id: sensor.washing_machine_state
  analysis_type: comparative
```

**After (choose one):**
```yaml
service: smart_appliance_monitor.analyze_cycles
data:
  entity_id: sensor.washing_machine_state
  analysis_type: recommendations  # For optimization tips
  # OR
  analysis_type: pattern  # For usage patterns
  # OR
  analysis_type: all  # For combined analysis
```

---

## 🧪 Testing Recommendations

After migration, test:

1. **Cost Calculation**: Verify cost sensors show correct values in your currency
2. **Global Config**: Ensure price is applied to all appliances
3. **Tariff Detection**: Run detection and check results in notification
4. **AI Analysis**: Run analysis and verify currency in recommendations
5. **Currency**: Check that all cost sensors use your Home Assistant currency

---

## 📋 Technical Details

### Modified Files

**Core Files:**
- `const.py` - Removed comparative type, added global config constants
- `storage_config.py` - Added currency, tariff detection, global price methods
- `coordinator.py` - Global price config, detect_tariff_system(), currency support

**Sensors:**
- `sensor.py` - Dynamic currency in 4 cost sensors with adaptive icons

**Configuration:**
- `config_flow.py` - Removed price fields from appliance configuration

**Services:**
- `services.yaml` - New services definitions, deprecated configure_ai
- `__init__.py` - New service handlers, migration detection

**AI & Export:**
- `export.py` - Added pricing_info builder with tariff details
- `ai_client.py` - 4 new prompt methods (pattern, recommendations, combined, tariff_context)

**Translations:**
- `strings.json` - Updated English translations
- `translations/fr.json` - Updated French translations

### Storage Structure Changes

**Global Configuration (.storage/smart_appliance_monitor_global):**
```json
{
  "ai_task_entity": "ai_task.openai",
  "global_price_entity": "sensor.electricity_price",
  "global_price_fixed": 0.2516,
  "enable_ai_analysis": true,
  "ai_analysis_trigger": "manual",
  "tariff_detection": {
    "detected_type": "peak_offpeak",
    "peak_price": 0.25,
    "offpeak_price": 0.18,
    "transition_hours": [6, 22],
    "last_analysis": "2025-10-22T10:30:00"
  }
}
```

---

## 🔗 Links

- **Full Changelog**: [CHANGELOG.md](../../CHANGELOG.md#090---2025-10-22)
- **Installation Guide**: [Installation.md](../wiki-github/Installation.md)
- **Configuration Guide**: [Configuration.md](../wiki-github/Configuration.md)
- **AI Analysis Guide**: [AI-Analysis.md](../wiki-github/AI-Analysis.md)
- **GitHub Repository**: https://github.com/legaetan/ha-smart_appliance_monitor
- **Issue Tracker**: https://github.com/legaetan/ha-smart_appliance_monitor/issues

---

## 💬 Support

If you encounter issues during migration:

1. Check the persistent notification for detailed instructions
2. Review logs for deprecation warnings
3. Consult the [Configuration Wiki](../wiki-github/Configuration.md)
4. Open an issue on [GitHub](https://github.com/legaetan/ha-smart_appliance_monitor/issues)

---

## 🙏 Thank You

Thank you for using Smart Appliance Monitor! This major update lays the foundation for more intelligent energy management features in future releases.

**What's Next:**
- Config Flow UI for global configuration (planned for v0.10.0)
- Advanced tariff scheduling recommendations
- Multi-currency support for export reports
- Enhanced AI analysis with cost optimization priorities
