# Release Notes - Smart Appliance Monitor

This directory contains detailed release notes for each version of Smart Appliance Monitor.

## 📋 Version Index

### Version 1.0.x - Integrated Dashboard System 🎉

- **[v1.0.0](RELEASE_NOTES_v1.0.0.md)** - October 23, 2025 - **MAJOR RELEASE**: Integrated Dashboard System 🎨
  - **NEW**: Complete integrated dashboard management system
  - **NEW**: Automated dashboard generation with YAML mode
  - **NEW**: Configuration panel "Smart Appliances Config" in sidebar
  - **NEW**: Energy Dashboard style graphs (7-day, donut chart, real-time)
  - **NEW**: 3 new services (generate_dashboard_yaml, configure_dashboard, toggle_view)
  - **NEW**: Multi-tab dashboard (overview + individual appliance tabs)
  - **CHANGED**: Direct entity integration (no more entity ID guessing)
  - **CHANGED**: All dashboard cards built programmatically in Python
  - **REMOVED**: All YAML template files (14 templates deleted)
  - **REMOVED**: Template loading system completely removed

### Version 0.9.x - Global Configuration & Dynamic Currency 🌍

- **[v0.9.2](RELEASE_NOTES_v0.9.2.md)** - January 23, 2025 - Bug Fixes & Code Quality 🐛
  - **FIXED**: Notification switches not preserving state after restart
  - **FIXED**: Energy Dashboard sync service error ("price_kwh has no setter")
  - **CHANGED**: Removed hardcoded French entity names for proper translation system
  - **IMPROVED**: Better code maintainability following HA best practices

- **[v0.9.1](RELEASE_NOTES_v0.9.1.md)** - October 23, 2025 - Dashboard Enhancement & Energy Integration 🎨
  - **NEW**: Complete dashboard redesign with 9 comprehensive views
  - **NEW**: Generic card templates system (`_card_templates.yaml`)
  - **NEW**: 4 new appliance templates (water heater, oven, dryer, desktop)
  - **NEW**: Global price synchronization from Energy Dashboard
  - **ENHANCED**: Smart sensor matching with fuzzy logic (4 strategies)
  - **ENHANCED**: All appliance templates updated to v1.0.0 (10+ sections)
  - **FIXED**: Energy Dashboard sync now uses configured sensors
  - **FIXED**: Price applies uniformly to all appliances

- **[v0.9.0](RELEASE_NOTES_v0.9.0.md)** - October 22, 2025 - Global Configuration System ⚠️ **BREAKING CHANGES**
  - **BREAKING**: Price configuration now global only
  - **BREAKING**: "Comparative" AI analysis type removed
  - **BREAKING**: Service `configure_ai` deprecated
  - **NEW**: `set_global_config` service for global configuration
  - **NEW**: `detect_tariff_system` service for automatic peak/off-peak detection
  - **NEW**: Dynamic currency support from Home Assistant
  - **ENHANCED**: AI prompts with tariff context and currency
  - **ENHANCED**: Real-time cost calculation during cycles

### Version 0.8.x - Cycle History System 📊

- **[v0.8.1](RELEASE_NOTES_v0.8.1.md)** - October 22, 2025 - Documentation Update 📚
  - **FIXES**: Complete documentation audit
  - Fixed obsolete version numbers in wiki and README
  - Fixed entity count (32→33)
  - New Cycle-History.md wiki page (540+ lines)
  - Complete v0.8.0 services documentation
  - Updated all links and references

- **[v0.8.0](RELEASE_NOTES_v0.8.0.md)** - October 22, 2025 - Cycle History System 🎉
  - **NEW FEATURE**: Persistent cycle history system
  - `get_cycle_history` service with advanced filters
  - `import_historical_cycles` service for past cycle reconstruction
  - Hybrid storage: 30 cycles in memory + unlimited in Recorder
  - Automatic recording in HA database
  - `replace_existing` mode support for cleanup and reimport
  - Optimized SQL queries for modern Recorder
  - Complete documentation with examples and warnings

### Version 0.7.x - AI Analysis 🤖

- **[v0.7.4](RELEASE_NOTES_v0.7.4.md)** - October 21, 2025 - Negative Energy Values Fix 🚨
  - **CRITICAL**: Fixed negative energy values (-4551 kWh → 0 kWh)
  - Cause: ESPHome sensor resets creating negative cycle energies
  - Multi-level validation to detect and ignore negative energies
  - Auto-recovery of corrupted statistics on restart
  - Detailed logging for data issue debugging
  - AI analysis now functional with valid data

- **[v0.7.3](RELEASE_NOTES_v0.7.3.md)** - October 21, 2025 - AI Analysis Bug Fixes 🐛
  - **CRITICAL**: Fixed AI response parsing (empty recommendations and insights)
  - Switched from strict JSON to Markdown parsing
  - Fixed coordinator matching for appliance names with underscores
  - Improved AI prompts with explicit Markdown structure
  - Added detailed debug logs for AI response tracking
  - Fixed response key: `response["text"]` → `response["data"]`

- **[v0.7.2](RELEASE_NOTES_v0.7.2.md)** - October 21, 2025 - Bug Fixes & Documentation 🐛
  - **CRITICAL**: Fixed AI service registration bug
  - All 13 services now available after update
  - Complete wiki documentation for AI features (500+ lines)
  - Updated wiki sidebar with "Energy & AI" section
  - Verified and fixed wiki links
  - Migration guide from v0.6.0, v0.7.0, and v0.7.1

- **[v0.7.1](RELEASE_NOTES_v0.7.1.md)** - October 21, 2025 - Historical Release Notes Recovery 📚
  - Recovery of all historical release notes (v0.2.0 to v0.5.0)
  - Permanent documentation system established
  - Complete organization of past releases
  - Updated release workflow

- **[v0.7.0](RELEASE_NOTES_v0.7.0.md)** - October 21, 2025 - AI-Powered Cycle Analysis 🤖
  - AI analysis of appliance cycles via Home Assistant AI Tasks
  - Support for OpenAI, Claude, Ollama, and other AI providers
  - Three analysis types: Pattern, Comparative, Recommendations
  - Global energy dashboard analysis
  - New services: `configure_ai`, `analyze_cycles`, `analyze_energy_dashboard`
  - New AI analysis sensors and switches
  - Complete testing guide (TESTING_AI.md)
  - Bilingual documentation (EN/FR)

### Version 0.6.x - Energy Dashboard Integration ⚡

- **[v0.6.0](RELEASE_NOTES_v0.6.0.md)** - October 21, 2025 - Energy Dashboard Integration Suite
  - `.storage/energy` file reader (read-only)
  - Automatic synchronization with Energy Dashboard
  - Sync and configuration export services
  - Custom Energy Dashboard with advanced analytics
  - Multi-period comparisons
  - Custom dashboard template

### Version 0.5.x - Advanced Features & Fixes ⚡

- **[v0.5.7](RELEASE_NOTES_v0.5.7.md)** - October 21, 2025 - Documentation & Roadmap 📚
  - New centralized IDEAS.md file (297 lines)
  - 3 new major ideas added
  - Release notes organized in dedicated folder
  - Clean and professional documentation

- **[v0.5.6](RELEASE_NOTES_v0.5.6.md)** - October 21, 2025 - Bilingual Support (French) 🇫🇷
  - French/English support for custom cards
  - Automatic language detection
  - Bilingual entity mapping

- **[v0.5.5](RELEASE_NOTES_v0.5.5.md)** - October 21, 2025 - Critical Fixes
  - Fixed StaticPathConfig API
  - Added missing `set_enabled()` method
  - Functional state restoration

- **[v0.5.4](RELEASE_NOTES_v0.5.4.md)** - October 21, 2025 - API Fix
  - Migration to `async_register_static_paths`
  - Fixed Home Assistant compatibility

- **[v0.5.3](RELEASE_NOTES_v0.5.3.md)** - October 21, 2025 - Automatic Installation
  - Custom cards automatically installed via HACS
  - Automatic frontend resource registration
  - Complete HACS integration

- **[v0.5.2](RELEASE_NOTES_v0.5.2.md)** - October 21, 2025 - Frontend Resources
  - First attempt at automatic card installation
  - Documentation improvements

- **[v0.5.1](RELEASE_NOTES_v0.5.1.md)** - October 20, 2025 - State Persistence
  - Persistence of cycles and statistics
  - Automatic restoration after HA restart
  - Intelligent data validation

- **[v0.5.0](RELEASE_NOTES_v0.5.0.md)** - October 21, 2025 - Advanced Features Release 🚀
  - Automatic auto-shutdown after cycles
  - Energy Management with limits and budget
  - Usage Scheduling (allowed hours, blocked days)
  - Intelligent Anomaly Detection
  - Data Export (CSV/JSON)
  - Energy Dashboard Integration
  - 10 new entities per appliance (30 total)

### Version 0.4.x - Configuration UX Improvements 🎨

- **[v0.4.1](RELEASE_NOTES_v0.4.1.md)** - October 20, 2025 - Bundled Dashboard Templates
  - Templates included directly in integration
  - 7 templates for each appliance type
  - Automatic resolution and immediate generation
  - Easy customization

- **[v0.4.0](RELEASE_NOTES_v0.4.0.md)** - October 20, 2025 - Enhanced Configuration UX
  - Multi-step configuration (4 steps)
  - Natural units (minutes/hours instead of seconds)
  - Expert Mode for advanced options
  - Improved descriptions and contextual help

### Version 0.3.x - Dashboard System 📊

- **[v0.3.0](RELEASE_NOTES_v0.3.0.md)** - October 20, 2025 - Dashboard Templates
  - Complete dashboard template system
  - 7 pre-configured templates per appliance type
  - Automatic `generate_dashboard_yaml` service
  - Mushroom Cards and Mini Graph Card support
  - 6 sections per dashboard (status, cycle, power, controls, stats, alerts)

### Version 0.2.x - Initial Release 🎉

- **[v0.2.0](RELEASE_NOTES_v0.2.0.md)** - October 20, 2025 - Initial Public Release
  - First public release
  - Automatic cycle detection
  - 14 entities per appliance
  - Complete Configuration Flow UI
  - Notification system (Telegram, Mobile App, Persistent)
  - Multi-language support (EN/FR)

---

## 📚 Related Resources

- **CHANGELOG**: [CHANGELOG.md](../../CHANGELOG.md) - Complete version history
- **IDEAS**: [IDEAS.md](../IDEAS.md) - Future features and roadmap
- **GitHub Releases**: [Releases](https://github.com/legaetan/ha-smart_appliance_monitor/releases)

---

## 🔖 Versioning Convention

This project follows [Semantic Versioning](https://semver.org/):
- **MAJOR** (x.0.0) - Breaking changes
- **MINOR** (0.x.0) - New features (backward compatible)
- **PATCH** (0.0.x) - Bug fixes (backward compatible)

---

**Latest version**: v0.9.0  
**Date**: October 22, 2025
