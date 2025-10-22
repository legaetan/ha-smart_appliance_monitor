# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.8.1] - 2025-10-22

### Fixed

**Documentation Audit and Corrections**
- Fixed obsolete version numbers across all documentation (0.5.1→0.8.0 in wiki, 0.6.0→0.8.0 in README)
- Corrected entity count in Features.md (32→33 entities: 14 sensors per appliance + 1 global AI sensor)
- Fixed missing EnergyDashboardAIAnalysisSensor documentation
- Corrected "Latest" version indicators in README and release notes index

### Added

**Documentation Enhancements**
- Created comprehensive Cycle-History.md wiki page (540+ lines)
  - Complete guide for cycle history system
  - Service documentation with all parameters
  - 5 detailed use cases
  - Best practices and troubleshooting
  - Event documentation
- Added v0.8.0 services documentation in Features.md and README.md
  - `get_cycle_history` service fully documented
  - `import_historical_cycles` service with examples and warnings
- Added "What's New" sections for v0.8.0, v0.7.0, v0.6.0 in wiki Home page
- Added Cycle-History link to wiki sidebar

### Changed

**Documentation Updates**
- Updated Installation.md with all new modules (ai_client.py, history.py, import_history.py, energy_storage.py, energy_dashboard.py, storage_config.py)
- Updated Advanced-Features.md to reference v0.5.0 through v0.8.0
- Updated README.md "Recent Improvements" section with proper version ordering
- Updated Home Assistant version requirement (2024.1→2023.8) in Installation.md
- Reorganized wiki structure with better feature version indicators

### Documentation Files Modified
- `docs/wiki-github/Home.md` - Version and features update
- `docs/wiki-github/Features.md` - Entity count, services, v0.8.0 section
- `docs/wiki-github/Cycle-History.md` - **NEW comprehensive guide**
- `docs/wiki-github/_Sidebar.md` - Added Cycle-History link
- `docs/wiki-github/Installation.md` - Updated file structure
- `docs/wiki-github/Advanced-Features.md` - Version references
- `README.md` - Recent improvements, services documentation
- `docs/release_notes/README.md` - Latest version indicator

**Impact**: All documentation now accurately reflects v0.8.0 codebase with complete feature coverage

## [0.8.0] - 2025-10-22

### Added

**Cycle History System**
- Added persistent cycle history storage via Home Assistant Recorder
- Added `get_cycle_history` service for querying historical cycles with advanced filters
- Added `import_historical_cycles` service for reconstructing cycles from raw sensor data
- Added hybrid storage: 30 recent cycles in memory + unlimited cycles in Recorder database
- Added automatic cycle event recording to Recorder (no configuration required)

**History Services**
- `get_cycle_history`: Query cycles with filters (period, duration, energy, limit)
  - Returns cycles with start/end times, energy, cost, duration, peak power
  - Provides aggregated statistics (total energy, cost, average duration)
  - Fires `smart_appliance_monitor_cycle_history` event with complete data
- `import_historical_cycles`: Reconstruct past cycles from sensor history
  - Supports dry-run mode for preview before import
  - Detects cycles that occurred before integration installation
  - Supports `replace_existing` mode to clean and reimport with different thresholds
  - Provides monthly statistics breakdown

**Database Integration**
- Cycles automatically stored as events in Home Assistant Recorder
- SQL queries optimized for modern Recorder structure (event_type_id, time_fired_ts)
- Automatic deletion of existing cycles when using `replace_existing: true`
- Support for querying cycles across appliance lifetime

### Changed

**Cycle Storage**
- Increased in-memory cycle history from 10 to 30 cycles
- Enhanced cycle events with complete metadata (start_time, end_time, start_energy, end_energy, peak_power)
- All cycles now include `imported` and `reimported` flags for tracking data source

**Documentation**
- Added comprehensive Cycle History System section in README
- Added step-by-step import examples with warnings
- Updated services.yaml with detailed parameter descriptions
- Added cautionary notes about `replace_existing` parameter

### Fixed

**Recorder Compatibility**
- Fixed SQL queries to use modern Recorder schema (event_type_id instead of event_type)
- Fixed event querying to properly join event_data table
- Fixed timestamp handling to use time_fired_ts (float) instead of time_fired (datetime)
- Added graceful handling when event types don't exist in database

**File Changes**
- `custom_components/smart_appliance_monitor/__init__.py`: Added history service handlers
- `custom_components/smart_appliance_monitor/history.py` (new): Cycle history manager
- `custom_components/smart_appliance_monitor/import_history.py` (new): Historical cycle importer
- `custom_components/smart_appliance_monitor/coordinator.py`: Increased cycle history size, enriched events
- `custom_components/smart_appliance_monitor/services.yaml`: Added new services documentation
- `custom_components/smart_appliance_monitor/manifest.json`: Version bump to 0.8.0
- `README.md`: Added Cycle History System documentation

### Migration Notes

**From v0.7.x to v0.8.0**
- No breaking changes - existing cycles continue working normally
- New services available immediately after update
- Existing cycle events in Recorder are compatible with new system
- Use `replace_existing: true` with caution - it permanently deletes cycles

**Important Warnings**
- `replace_existing: true` permanently deletes existing cycles in the specified period
- Always test with `dry_run: true` before actual import
- Historical import requires sensor data to exist in Recorder (respects purge_keep_days)

## [0.7.6] - 2025-10-22

### Fixed

**AI Analysis Storage and Persistence**
- Fixed AI analysis results not being saved to storage immediately after completion
- Fixed `last_ai_analysis_result` remaining `null` after AI analysis completes
- Fixed cycle history (`cycle_history`) always being empty in storage files
- Fixed AI analysis failing with `'>' not supported between instances of 'NoneType' and 'int'` error when AI returns `None` for energy savings
- Added immediate state save (`await self._save_state()`) after AI analysis completion

**Cycle History Management**
- Cycle history now saved **always** for all appliances (not only when anomaly detection is enabled)
- Cycles are now properly stored in `.storage/smart_appliance_monitor.{entry_id}` files
- Historical cycle data now available for AI analysis and statistics

### Changed

**Storage Behavior**
- AI analysis results are now persisted immediately when analysis completes (no delay)
- Cycle history is maintained for all appliances regardless of anomaly detection setting
- Maximum cycle history size: 10 cycles (configurable via `_max_history_size`)

### Technical Details

**Files Modified**:
- `custom_components/smart_appliance_monitor/coordinator.py`:
  - Added `await self._save_state()` in `async_trigger_ai_analysis()` after storing result (line 683)
  - Removed conditional `if self.anomaly_detection_enabled` for cycle history storage (line 426)
  - Cycle history now populated for all appliances
- `custom_components/smart_appliance_monitor/ai_client.py`:
  - Fixed `_build_full_analysis_text()` to handle `None` values from AI using `or 0` operator (line 403-404)

**Impact**: 
- AI analysis results now persist correctly across Home Assistant restarts
- Cycle history is available for all appliances, improving AI analysis quality
- No more empty `cycle_history` arrays in storage files

## [0.7.5] - 2025-10-22

### Fixed

**AI Analysis Robustness**
- Fixed AI analysis failing when OpenAI/Google AI returns `None` for energy savings values
- Fixed coordinator lookup using entity registry instead of fragile name-based matching
- Fixed AI analysis state persistence across Home Assistant restarts
- Fixed AI switch persistence - switches now remain enabled after HA restart
- Fixed MAX_TOKENS errors by using structured responses from `ai_task.generate_data`
- Fixed dashboard recommendations display format (now shows proper bullet lists instead of Python arrays)

**Coordinator Entity Lookup**
- Refactored `_get_coordinator_from_entity_id()` to use entity registry and `entry_id`
- Eliminates failures when appliance names contain spaces or special characters
- More reliable service calls (AI analysis, export, etc.) for all appliances

**AI Analysis State Management**
- Added `last_ai_analysis_result` to persistent storage
- Analysis results now survive Home Assistant restarts
- Sensors show previous analysis status instead of defaulting to "not_analyzed"

### Changed

**AI Integration Improvements**
- AI analysis now uses structured responses via `ai_task.generate_data` (more reliable)
- Simplified AI prompts to reduce token usage and prevent timeouts
- Added safe float conversion with None handling for AI response values
- Switch state changes immediately trigger state persistence (no delay)

### Technical Details

**Files Modified**:
- `custom_components/smart_appliance_monitor/__init__.py` - Entity registry-based coordinator lookup
- `custom_components/smart_appliance_monitor/coordinator.py` - Persistent AI results, async switch saves
- `custom_components/smart_appliance_monitor/ai_client.py` - Structured responses, safe float conversion
- `custom_components/smart_appliance_monitor/switch.py` - Async switch state methods
- `custom_components/smart_appliance_monitor/const.py` - Added CYCLE_ANALYSIS_STRUCTURE
- `dashboards/sam-energy-dashboard.yaml` - Fixed recommendations formatting with Jinja loops

**Impact**: 
- AI analysis now works reliably for all appliances regardless of naming
- Analysis results persist across reboots
- Reduced AI timeout errors through structured responses
- Better user experience with preserved switch states

**Migration Notes**:
- Existing installations: First AI analysis after upgrade will populate persistent storage
- Dashboard templates automatically updated for better formatting
- No manual intervention required

## [0.7.4] - 2025-10-21

### Fixed

**Negative Energy Values Validation**
- Fixed critical issue causing negative energy consumption values in statistics
- Root cause: Energy sensor resets (e.g., ESPHome device reboots) created negative cycle energy values
- Added comprehensive validation in `_on_cycle_finished()` to detect and skip negative cycle energies
- Added validation on state restoration to automatically reset corrupted negative statistics
- Negative values now logged as warnings with clear indication of data integrity issues

**Data Integrity Protection**
- Implemented automatic recovery when negative totals are detected
- Daily and monthly statistics automatically reset to safe values (0 or current cycle energy)
- Prevents cascading data corruption across multiple cycles
- Detailed error logging for debugging data issues

### Changed

**Coordinator Statistics Handling**
- Enhanced `_on_cycle_finished()` with multi-level validation:
  1. Detect negative cycle energy (sensor reset indicator)
  2. Skip adding negative values to cumulative totals
  3. Check if totals became negative despite validation
  4. Auto-reset negative totals with error logging
- Enhanced `restore_state()` to validate and correct negative values on integration load
- All negative value detections include appliance name and context in logs

### Technical Details

**Files Modified**:
- `custom_components/smart_appliance_monitor/coordinator.py` - Added validation logic

**Impact**: 
- Prevents future negative value accumulation
- Automatic recovery from existing corrupted statistics
- AI analysis now receives valid data for accurate recommendations
- Energy Dashboard integration no longer affected by data corruption

**Migration Notes**:
- Existing installations with negative values: Values will be automatically corrected on next cycle completion
- Manual reset still available via "Reset Statistics" button if immediate correction needed

## [0.7.3] - 2025-10-21

### Fixed

**AI Analysis Response Parsing**
- Fixed AI analysis results appearing empty (recommendations and insights fields)
- Switched from strict JSON structure to Markdown-based AI responses
- Implemented robust Markdown parser to extract structured data from AI responses
- Corrected response key from `response["text"]` to `response["data"]` for AI Task integration
- Added extensive debug logging to track AI response processing

**Coordinator Entity Matching**
- Fixed `Unable to find coordinator for entity` error when calling `analyze_cycles` service
- Improved `_get_coordinator_from_entity_id()` function to handle underscores in appliance names
- Now correctly matches entities like `sensor.chauffe_eau_etat` to "Chauffe-Eau" appliance
- Made slug matching more robust with explicit `appliance_slug + "_"` check

**AI Prompt Engineering**
- Enhanced AI prompts to request structured Markdown format with explicit headers
- Added mandatory requirements for concrete recommendations and insights
- Improved guidance for AI to provide actionable, non-empty content
- Set `structure` parameter to `None` to allow free-form Markdown responses

### Changed

**AI Client Implementation**
- Completely rewrote `_process_cycle_analysis_response()` to parse Markdown instead of JSON
- Added `parse_section()` helper function to extract content under Markdown headers
- Enhanced error handling for malformed AI responses
- Preserved `full_analysis` attribute with complete raw Markdown text

### Technical Details

**Files Modified**:
- `custom_components/smart_appliance_monitor/ai_client.py` - Markdown parser implementation
- `custom_components/smart_appliance_monitor/__init__.py` - Robust coordinator matching
- `custom_components/smart_appliance_monitor/manifest.json` - Version bump to 0.7.3
- `version` - Version bump to 0.7.3

**Debugging Improvements**:
- Added `_LOGGER.debug` statements for raw AI responses
- Added logging for each parsed section (summary, status, recommendations, etc.)
- Better error messages when coordinator cannot be found

## [0.7.2] - 2025-10-21

### Fixed

**Service Registration**
- Fixed critical bug preventing AI services from being registered on integration updates
- Changed service registration check from `start_cycle` to `configure_ai` to ensure v0.7 services load
- Added explicit logging when services are registered
- All 13 services now properly available after update from v0.6 to v0.7

**Issue**: Users upgrading from v0.6.0 to v0.7.0 would not get the 3 new AI services (`configure_ai`, `analyze_cycles`, `analyze_energy_dashboard`) because the code only checked if `start_cycle` service existed, which it did.

**Solution**: Now checks for `configure_ai` service specifically, ensuring all services are re-registered when updating to v0.7+.

### Documentation

**Wiki Enhancements**
- **NEW**: Created comprehensive [AI-Powered Analysis wiki page](https://github.com/legaetan/ha-smart_appliance_monitor/wiki/AI-Analysis)
  - Complete AI features documentation (v0.7.0)
  - Configuration examples for OpenAI, Claude, and Ollama
  - All three services documented with examples
  - Cost considerations and optimization tips
  - Troubleshooting section with common issues
  - 10+ automation examples
  
- **UPDATED**: Wiki sidebar now includes "Energy & AI (v0.6.0+)" section
  - Added Energy Dashboard Integration link
  - Added AI-Powered Analysis link
  - Better organization of advanced features
  
- **UPDATED**: Features.md page
  - Added v0.7.0 features section
  - Added v0.6.0 features section
  - Updated entity counts (32 entities per appliance in v0.7.0)
  - Clear links to new documentation pages

**Links Verified**
- All internal wiki links checked and working
- Cross-references between pages validated
- External links to GitHub docs confirmed

### Technical Details

**Files Modified**:
- `custom_components/smart_appliance_monitor/__init__.py` - Service registration fix
- `custom_components/smart_appliance_monitor/manifest.json` - Version bump
- `docs/wiki-github/AI-Analysis.md` - NEW comprehensive guide (500+ lines)
- `docs/wiki-github/_Sidebar.md` - Added Energy & AI section
- `docs/wiki-github/Features.md` - Updated with v0.6 and v0.7 features
- `CHANGELOG.md` - This changelog

### Migration Notes

**From v0.7.0 or v0.7.1**:
- **Action required**: Restart Home Assistant to register AI services
- Services will automatically be available after restart
- No configuration changes needed
- Existing AI configurations preserved

**From v0.6.0 or earlier**:
- Update to v0.7.2 (skip v0.7.0/v0.7.1)
- Restart Home Assistant
- Configure AI using the new `configure_ai` service
- See [AI-Powered Analysis Guide](https://github.com/legaetan/ha-smart_appliance_monitor/wiki/AI-Analysis)

## [0.7.1] - 2025-10-21

### Changed

**Documentation & Project Organization**
- Release notes now permanently stored in `docs/release_notes/`
- Updated `.cursorrules` with new release workflow
- Release notes are versioned and committed to repository
- Improved release checklist with testing guide requirements
- Updated project structure documentation

### Fixed

**Release Process**
- Release notes are no longer temporary files
- Complete release history preserved in `docs/release_notes/`
- Release notes index maintained in `docs/release_notes/README.md`
- Better organization for long-term project maintenance

## [0.7.0] - 2025-10-21

### Added

#### AI-Powered Cycle Analysis 🤖

**AI Client Integration (`ai_client.py`)**
- **New module** `SmartApplianceAIClient` for AI-powered analysis via Home Assistant AI Tasks
- Uses `ai_task.generate_data` service (no direct API calls)
- Support for OpenAI, Claude, Ollama, and any HA-compatible AI provider
- Three analysis methods:
  - `async_analyze_cycle_data()` - Individual appliance cycle analysis
  - `async_analyze_energy_dashboard()` - Global home energy analysis
- Structured response parsing with field validation
- Optimized prompts for pattern, comparative, and recommendation analysis
- Error handling and timeout management

**Global AI Configuration (`storage_config.py`)**
- **New module** `GlobalConfigManager` for persistent AI configuration
- Storage in `.storage/smart_appliance_monitor.global_config`
- Methods: `async_load()`, `async_save()`, `async_get()`, `async_set()`, `async_update()`
- Accessible by all coordinators via `hass.data[DOMAIN]["global_config"]`
- Stores: AI Task entity, global price entity, analysis trigger, enable/disable state

**Enhanced Data Export**
- **New method** `export_for_ai_analysis()` in `export.py`
  - Structured JSON with cycle history (last N cycles)
  - Aggregated statistics (mean, stdev, min/max)
  - Temporal patterns (most common hours and days)
  - Comparison current vs historical
- **New method** `export_cycles_history_csv()` for tabular export
- Metadata includes: appliance config, type profile, pricing

**Energy Dashboard AI Analysis**
- **New method** `export_for_ai_analysis()` in `energy_dashboard.py`
  - Aggregated data for all appliances
  - Period-based exports (today/yesterday/week/month)
  - Optional comparison with previous period
  - Device breakdowns and top consumers
  - Pricing information

**New AI Analysis Services**
1. **`analyze_cycles`** - Analyze individual appliance cycles
   - Parameters: entity_id, analysis_type, cycle_count, export_format, save_export
   - Analysis types: pattern, comparative, recommendations, all
   - Optional data export to /config files
   - Auto-sends notification if enabled
   
2. **`analyze_energy_dashboard`** - Global home energy analysis
   - Parameters: period, compare_previous, include_recommendations
   - Analyzes all appliances together
   - Provides efficiency score (0-100)
   - Identifies top consumers and optimization opportunities
   
3. **`configure_ai`** - Configure global AI settings
   - Parameters: ai_task_entity, global_price_entity, enable_ai_analysis, ai_analysis_trigger
   - Reloads config for all coordinators
   - Sends confirmation notification

**New AI Analysis Sensors**
- **Per-appliance sensor** `sensor.<appliance>_ai_analysis`
  - State: optimized/normal/needs_improvement/not_analyzed
  - Attributes: last_analysis_date, analysis_type, summary, recommendations, insights
  - Attributes: energy_savings_kwh, energy_savings_eur, optimal_hours
  - Attributes: full_analysis, cycle_count_analyzed
  
- **Global dashboard sensor** `sensor.sam_energy_dashboard_ai_analysis`
  - State: Efficiency score (0-100)
  - Attributes: global_recommendations, top_optimization_opportunities
  - Attributes: estimated_monthly_savings_eur, peak_hours, off_peak_recommendations
  - Attributes: inefficient_devices, consumption_trend

**New AI Analysis Switch**
- **Switch** `switch.<appliance>_ai_analysis`
  - Enable/disable AI analysis per appliance
  - Independent of global configuration (local override)
  - Icon: mdi:brain / mdi:brain-off
  - Only available when AI Task entity configured

**Coordinator AI Integration**
- **New properties**: `ai_analysis_enabled`, `ai_analysis_trigger`, `ai_task_entity`, `last_ai_analysis_result`
- **New method** `async_trigger_ai_analysis()` - Trigger analysis programmatically
- **New method** `load_global_ai_config()` - Load AI config on startup
- **Auto-trigger** support: Analysis triggered automatically after cycle completion if configured
- **Events**: `EVENT_AI_ANALYSIS_COMPLETED`, `EVENT_AI_ANALYSIS_FAILED`

**AI Analysis Notifications**
- **New notification type** `NOTIF_TYPE_AI_ANALYSIS`
- **New method** `notify_ai_analysis()` in `notify.py`
- Rich notifications with status emoji, summary, recommendations, savings
- Mobile app actions: "View Details", "Re-analyze"
- Color-coded by status (green/orange/blue)

**Translations and Documentation**
- Added AI analysis keys to `strings.json` (English)
- Added AI analysis keys to `translations/fr.json` (French)
- Bilingual support for all UI elements
- New selectors: ai_analysis_trigger, ai_analysis_type
- Service documentation in `services.yaml`

**Testing and Documentation**
- **New file** `TESTING_AI.md` - Complete testing guide
  - Setup instructions for AI Task entities
  - 6 detailed test scenarios
  - Troubleshooting section
  - Performance notes and cost estimates
  - Automation examples
- Updated `README.md` with AI Analysis Features section
- Service usage examples with expected results

### Changed

- **Coordinator** now loads global AI config on initialization
- **`__init__.py`** initializes global config manager on first entry setup
- **Notification types** list extended with AI analysis
- **Sensor entity count** increased to 14 per appliance (added AI sensor)
- **Switch entity count** increased to 10 per appliance (added AI switch)
- **Service count** increased to 13 total services (added 3 AI services)

### Fixed

- Proper handling of missing AI Task entity (graceful degradation)
- Sensor availability based on global AI configuration
- Cache invalidation when global config changes

### Technical Details

**Architecture**
- AI analysis flows through: Trigger → Coordinator → Exporter → AI Client → HA AI Task → Response Parser → Sensor/Notification
- No direct API calls - everything via Home Assistant AI Tasks
- Structured responses using AI Task `structure` parameter
- Response validation and error handling at each step

**Performance**
- AI analysis: 10-30 seconds depending on provider and data size
- Local AI (Ollama): ~5-15 seconds
- Cloud AI (OpenAI/Claude): ~10-30 seconds
- API costs: ~$0.01-0.03 per cycle analysis, ~$0.02-0.05 per dashboard analysis

**Compatibility**
- ✅ No breaking changes
- ✅ Optional feature (disabled by default)
- ✅ Compatible with all existing features
- ✅ Works with any HA AI Task provider
- ✅ Bilingual interface (EN/FR)

## [0.6.0] - 2025-10-21

### Added

#### Energy Dashboard Integration Suite 🎉

**Energy Storage File Reader (`energy_storage.py`)**
- **New module** for read-only access to Home Assistant's `.storage/energy` file
- Class `EnergyStorageReader` with caching system (5 min TTL)
- Methods to read energy sources and device consumption configurations
- Safe error handling for missing or invalid files
- Sync report generation comparing SAM devices with Energy Dashboard

**Energy Dashboard Synchronization (`energy.py` enhanced)**
- **New class** `EnergyDashboardSync` for advanced sync management
- `get_sync_status()` - Check if appliance is in Energy Dashboard
- `suggest_energy_config()` - Generate suggested configuration with parent sensors
- `find_similar_devices()` - Detect Energy Dashboard devices that could use SAM
- `generate_sync_report()` - Comprehensive sync report with recommendations
- Bilingual instructions (English/French) for adding devices

**Three New Services**
1. **`sync_with_energy_dashboard`** - Check sync status for all or specific SAM devices
   - Generates detailed notification with synced/missing devices
   - Provides setup instructions for missing devices
   - Supports filtering by entity_id or sync all devices
   
2. **`export_energy_config`** - Export Energy Dashboard configuration
   - Generates JSON configuration ready to use
   - Includes parent sensor suggestions when applicable
   - Step-by-step instructions in notification
   
3. **`get_energy_data`** - Retrieve aggregated energy data
   - Period filtering (start/end dates)
   - Device filtering (specific devices or all)
   - Returns breakdown by device with costs
   - Fires event for custom dashboard cards

**Custom Energy Dashboard Backend (`energy_dashboard.py`)**
- **New module** with `CustomEnergyDashboard` class for advanced analytics
- `get_period_data()` - Energy data for custom time periods
- `get_devices_breakdown()` - Device consumption breakdown with percentages
- `get_comparison_data()` - Compare two periods (today vs yesterday, etc.)
- `get_daily_timeline()` - Hourly energy consumption timeline
- `get_top_consumers()` - Identify top N energy consumers
- `get_energy_efficiency_score()` - Calculate efficiency scores with recommendations
- `get_dashboard_summary()` - Complete dashboard summary with all metrics

**Custom Energy Dashboard Template**
- **New template** `dashboards/energy_dashboard.yaml` with complete UI
- Summary cards (total energy, cost, active devices)
- Device breakdown with bar charts
- Energy timeline (hourly visualization)
- Top 5 consumers ranking
- Monthly overview with statistics
- Cost analysis graphs
- Efficiency scores display
- Quick actions (sync, export, navigate)
- Integration status monitoring

**Automatic Sync Detection**
- Automatic check on appliance startup
- Logs sync status (✅ synced / ⚠️ not configured)
- Non-intrusive background task

**Service Documentation**
- Complete documentation in `services.yaml` for all three new services
- Examples and parameter descriptions
- Advanced options clearly marked

**Complete Wiki Documentation**
- **New guide** `docs/wiki-github/Energy-Dashboard.md` (570 lines)
- Architecture overview and features
- Getting started guide
- Service documentation with examples
- Custom dashboard installation and usage
- Troubleshooting section
- Best practices
- Advanced topics (raw data access, custom sensors, events)

### Changed

#### Documentation Updates
- **README.md** - Added "Energy Dashboard Suite (v0.6.0+)" section
- Documented 10 services (organized by category)
- Added service examples with YAML code
- Updated "Recent Improvements" with v0.6.0 details

- **IDEAS.md** - Marked 3 features as completed
  - Energy Storage File Integration ✅
  - Custom Energy Dashboard ✅
  - Enhanced Energy Dashboard Integration ✅
- Added "Recent Completions (v0.6.0)" section with detailed impact
- Updated priority matrix with status column

#### Configuration
- Added `CONF_ENABLE_ENERGY_DASHBOARD_SYNC` constant
- Added `EVENT_ENERGY_DASHBOARD_SYNCED` event

### Technical Details

**New Files Created:**
- `custom_components/smart_appliance_monitor/energy_storage.py` (270 lines)
- `custom_components/smart_appliance_monitor/energy_dashboard.py` (419 lines)
- `custom_components/smart_appliance_monitor/dashboards/energy_dashboard.yaml` (330 lines)
- `docs/wiki-github/Energy-Dashboard.md` (570 lines)

**Files Modified:**
- `custom_components/smart_appliance_monitor/__init__.py` (+280 lines)
  - Added 3 service schemas
  - Added 3 service handlers
  - Added automatic sync check on startup
  - Registered 3 new services
- `custom_components/smart_appliance_monitor/energy.py` (+216 lines)
  - Added `EnergyDashboardSync` class
  - Enhanced with sync and detection methods
- `custom_components/smart_appliance_monitor/const.py` (+3 lines)
  - New constants for Energy Dashboard integration
- `custom_components/smart_appliance_monitor/services.yaml` (+54 lines)
  - Documentation for 3 new services
- `README.md` (+77 lines)
  - New Energy Dashboard section
  - Service documentation
- `docs/IDEAS.md` (+94 lines)
  - Completion status updates
  - Recent completions section

**Architecture:**
- Read-only access to `.storage/energy` (safe, non-invasive)
- Modular design with dedicated modules for each feature
- Event-driven system for custom dashboards
- Cache system to minimize file I/O

**Code Quality:**
- ✅ All code comments in English
- ✅ Bilingual user-facing strings (EN/FR)
- ✅ No linter errors
- ✅ Follows Home Assistant best practices
- ✅ Type hints on all functions
- ✅ Comprehensive error handling

### Impact

**For Users:**
- Seamless integration with native Energy Dashboard
- Advanced analytics beyond HA's native capabilities
- Easy setup with automatic sync detection
- Clear instructions for manual configuration
- Foundation for future ML-based features

**For Developers:**
- Clean, modular architecture
- Extensible backend for future enhancements
- Event system for custom cards
- Well-documented APIs

**Statistics:**
- ~2300 new lines of code
- 3 new modules
- 3 new services
- 1 new dashboard template
- 1 comprehensive wiki guide

### Migration Notes

No breaking changes. This is a purely additive release.

**To use the new features:**
1. Restart Home Assistant after update
2. Check logs for automatic sync detection
3. Use `sync_with_energy_dashboard` service to get sync report
4. Use `export_energy_config` to add devices to Energy Dashboard
5. Optionally install custom dashboard template

### Future Enhancements

This release lays the foundation for:
- Custom energy Lovelace card (v0.7.0)
- Automatic appliance detection via consumption analysis
- ML-based energy optimization recommendations
- Historical data analysis with Recorder integration

---

## [0.5.7] - 2025-10-21

### Added

#### Documentation Consolidation & Future Roadmap
- **Created central IDEAS.md** - Comprehensive future features and roadmap (297 lines)
  - Organized by 6 themes: UI, ML, Energy, Integrations, Architecture, Advanced
  - Sub-organized by priority: Court terme / Moyen terme / Long terme
  - Includes priority matrix with impact and effort estimates
  - **3 major new feature ideas added:**
    1. **Energy Storage File Integration** - Auto-sync with HA's `.storage/energy` config
    2. **Custom Energy Dashboard** - Advanced customizable energy monitoring dashboard
    3. **Automatic Appliance Detection** 🔥 - Smart detection of unconfigured appliances
- **Reorganized release notes** - Created `docs/release_notes/` with comprehensive index
  - All release notes (v0.5.1 to v0.5.6) moved to dedicated folder
  - Added index file with quick navigation
- **Cleaned all documentation** - Removed scattered roadmap references
  - README.md: Simplified with reference to IDEAS.md
  - ARCHITECTURE.md: Focused on current architecture
  - Custom cards docs: Consolidated roadmap
  - Wiki pages: Updated "future feature" mentions with links to IDEAS.md

### Changed

#### Documentation Structure
- **Release notes location** - Moved from root to `docs/release_notes/`
- **Future features reference** - All docs now point to central IDEAS.md
- **Wiki references** - Replaced "(future feature)" with "(voir IDEAS.md)"

### Technical Details

**New Files:**
- `docs/IDEAS.md` - Central roadmap and future features hub
- `docs/release_notes/README.md` - Release notes index
- `docs/release_notes/RELEASE_NOTES_docs_2025-10-21.md` - This documentation release

**Files Modified:**
- `README.md` - Added IDEAS.md reference, cleaned roadmap
- `ARCHITECTURE.md` - Removed future enhancements section
- `custom_components/smart_appliance_monitor/www/smart-appliance-cards/README.md` - Updated roadmap
- `custom_components/smart_appliance_monitor/www/smart-appliance-cards/PROJECT_STATUS.txt` - Updated limitations
- `docs/wiki-github/Advanced-Features.md` - Updated future feature references
- `docs/wiki-github/Scheduling.md` - Updated future feature references
- `docs/wiki-github/Dashboards.md` - Updated future feature references
- `docs/wiki-github/Advanced-Notifications.md` - Updated future feature references

**Breaking Changes:** None - Documentation only

**Migration Notes:**
- No action required - this is a documentation-only release
- Integration functionality remains at v0.5.6 level
- New IDEAS.md provides clear vision for project future

## [0.5.6] - 2025-10-21

### Fixed

#### French Language Support for Custom Cards
- **Added bilingual support for custom Lovelace cards** - Cards now work with French entity names
  - Support for `_etat` suffix (French) in addition to `_state` (English)
  - Automatic detection and mapping of French entity names:
    - `duree_du_cycle` / `cycle_duration`
    - `energie_du_cycle` / `cycle_energy`
    - `cout_du_cycle` / `cycle_cost`
    - `en_marche` / `running`
    - `debranche` / `unplugged`
    - `surveillance` / `monitoring`
    - And all other entity translations
  - Cards automatically detect language from entity suffix
  - No configuration changes needed - works automatically

### Technical Details

**Files Modified:**
- `custom_components/smart_appliance_monitor/www/smart-appliance-cards/src/utils/helpers.js` - Added bilingual entity mapping
- `custom_components/smart_appliance_monitor/www/smart-appliance-cards/dist/*` - Rebuilt cards with language support

**Breaking Changes:** None

**Migration Notes:**
- Existing installations with French entity names: Update to v0.5.6 and cards will work immediately
- Existing installations with English entity names: No changes needed, backward compatible

## [0.5.5] - 2025-10-21

### Fixed

#### Critical Bug Fixes
- **Fixed StaticPathConfig API usage** - Corrected frontend resource registration
  - Changed from dict to `StaticPathConfig` object for `async_register_static_paths()`
  - Fixed `AttributeError: 'dict' object has no attribute 'url_path'` error
  - Cards now properly registered without errors
  
- **Fixed missing set_enabled method** - Added global notification toggle
  - Added `set_enabled()` method to `SmartApplianceNotifier` class
  - Fixed `AttributeError: 'SmartApplianceNotifier' object has no attribute 'set_enabled'`
  - State restoration now works correctly
  - Notification switches now function properly

### Technical Details

**Files Modified:**
- `custom_components/smart_appliance_monitor/__init__.py` - Added `StaticPathConfig` import and usage
- `custom_components/smart_appliance_monitor/notify.py` - Added `set_enabled()` method

**Breaking Changes:** None

**Migration Notes:** 
- Users who installed v0.5.4: Update to v0.5.5 to fix all startup and runtime errors
- Integration will load successfully and all features will work correctly
- State restoration from previous sessions now works without errors

## [0.5.4] - 2025-10-21

### Fixed

#### Home Assistant API Compatibility
- **Fixed AttributeError on startup** - Updated to use correct async API method
  - Changed `hass.http.register_static_path()` to `hass.http.async_register_static_paths()`
  - Fixed `'HomeAssistantHTTP' object has no attribute 'register_static_path'` error
  - Cards now properly registered without errors
  - Integration loads successfully on Home Assistant 2023.8+

### Technical Details

**Files Modified:**
- `custom_components/smart_appliance_monitor/__init__.py` - Updated to use `async_register_static_paths()` API

**Breaking Changes:** None

**Migration Notes:** 
- Users who installed v0.5.3: Update to v0.5.4 to fix startup errors
- Cards will be properly registered at `/hacsfiles/smart-appliance-cards/` after update and restart

## [0.5.3] - 2025-10-21

### Fixed

#### HACS Installation Structure
- **Fixed cards not being installed via HACS** - Moved www/ folder into integration directory
  - Moved `www/` from repository root to `custom_components/smart_appliance_monitor/www/`
  - Updated path resolution in `_register_frontend_resources()` function
  - Cards now properly installed when updating via HACS
  - Fixed path to be relative to integration folder instead of config root

### Technical Details

**Files Modified:**
- `custom_components/smart_appliance_monitor/__init__.py` - Updated www_path to `Path(__file__).parent / "www" / ...`
- Repository structure - Moved `www/` folder into integration directory

**Breaking Changes:** None

**Migration Notes:** 
- Users who installed v0.5.2: Update to v0.5.3 to get cards automatically installed
- Cards will be available at `/hacsfiles/smart-appliance-cards/` after update

## [0.5.2] - 2025-10-20

### Added

#### Frontend Cards Auto-Installation
- **Automatic Lovelace cards registration** - Custom cards now automatically available after HACS installation
  - Cards registered at `/hacsfiles/smart-appliance-cards/` path
  - Two cards included: `smart-appliance-cycle-card.js` and `smart-appliance-stats-card.js`
  - Auto-detection and validation of card files at startup
  - Informative logs for successful registration

#### Build System
- **Pre-compiled card assets** - Cards are now pre-built and versioned in Git
  - Compiled JavaScript files included in `www/smart-appliance-cards/dist/`
  - No manual build step required for users
  - Cards ready to use immediately after installation

### Changed

#### Documentation
- **Updated installation instructions** - Simplified setup process documented
  - New "Automatic Installation" section in cards README
  - Clear instructions for adding resources to Lovelace (one-time setup)
  - Maintained "Manual Installation" section for advanced users

#### Build Configuration
- **Updated .gitignore** - Frontend build artifacts now properly managed
  - `node_modules/` excluded from version control
  - Compiled `dist/` files explicitly included for distribution

### Technical Details

**Files Modified:**
- `custom_components/smart_appliance_monitor/__init__.py` - Added `_register_frontend_resources()` function
- `.gitignore` - Added exceptions for compiled card files
- `www/smart-appliance-cards/README.md` - Updated installation documentation
- `www/smart-appliance-cards/dist/` - Added pre-compiled cards (38KB + 43KB)

**Breaking Changes:** None

**Migration Notes:** 
- Existing installations: Cards will be automatically available after update
- Users must add resources to Lovelace once (see documentation)

## [0.5.1] - 2025-10-20

### Added

#### State Persistence System
- **Automatic state persistence** - All cycle data and statistics preserved across Home Assistant restarts
  - Cycle state (`idle`, `running`, `finished`) saved automatically
  - Current cycle data preserved (start time, start energy, peak power)
  - Last completed cycle data retained (duration, energy, cost)
  - Daily statistics saved (date, cycle count, total energy, total cost)
  - Monthly statistics saved (year, month, total energy, total cost)
  - Cycle history preserved for anomaly detection
  - Configuration state saved (monitoring enabled, notifications enabled)
  
- **Smart validation** - Data integrity checks on restore
  - Daily statistics reset if date has changed
  - Monthly statistics reset if month has changed
  - Current cycle always restored regardless of date
  
- **Storage system** - Using Home Assistant's native `.storage` system
  - Location: `<config_dir>/.storage/smart_appliance_monitor.<entry_id>.json`
  - Version: 1 (prepared for future migrations)
  - Automatic save on: cycle start, cycle finish, every 30s during cycle
  - Automatic restore on Home Assistant startup

#### Documentation
- **docs/PERSISTENCE.md** - Complete technical documentation
  - Storage format and location
  - Serialization details
  - Error handling
  - Examples and use cases
  
- **RESUME_PERSISTANCE.md** - Implementation summary in French
  - Problem statement and solution
  - Files modified and created
  - Concrete usage examples

#### Tests
- **tests/test_persistence.py** - Comprehensive test suite (11 tests)
  - Serialization/deserialization tests
  - Save/restore cycle verification
  - Obsolete data reset validation
  - Automatic save trigger tests

### Changed

#### Coordinator (`coordinator.py`)
- Added `Store` import from `homeassistant.helpers.storage`
- New constants: `STORAGE_VERSION = 1`, `STORAGE_KEY = "state"`
- New instance variable: `self._store` for persistent storage
- New methods:
  - `_save_state()` - Saves complete coordinator state
  - `restore_state()` - Restores state from storage
  - `_serialize_cycle()` / `_deserialize_cycle()` - Cycle data conversion
  - `_serialize_stats()` / `_deserialize_stats()` - Statistics conversion
- Enhanced event handlers to trigger automatic saves:
  - `_on_cycle_started()` - Saves on cycle start
  - `_on_cycle_finished()` - Saves on cycle completion
- Enhanced `_async_update_data()` - Periodic save during running cycles

#### Integration Init (`__init__.py`)
- Added `restore_state()` call during coordinator setup
- Ensures state restoration before first update

### Fixed
- **Data loss on restart** - Cycles and statistics no longer lost when Home Assistant restarts
- **Incorrect duration calculation** - Cycles correctly track duration even across restarts
- **Lost daily/monthly statistics** - All statistics properly preserved

### Technical Details

#### Files Created
- `docs/PERSISTENCE.md` (183 lines) - Technical documentation
- `RESUME_PERSISTANCE.md` (150 lines) - Implementation summary
- `tests/test_persistence.py` (279 lines) - Test suite

#### Files Modified
- `custom_components/smart_appliance_monitor/__init__.py` (+4 lines) - State restoration
- `custom_components/smart_appliance_monitor/coordinator.py` (+186 lines) - Complete persistence system

#### Storage Format
```json
{
  "state": "running",
  "current_cycle": {...},
  "last_cycle": {...},
  "daily_stats": {...},
  "monthly_stats": {...},
  "cycle_history": [],
  "monitoring_enabled": true,
  "notifications_enabled": true
}
```

### Benefits

1. **No Data Loss** - Running cycles continue correctly after HA restart
2. **Accurate Statistics** - Duration and energy calculations remain precise
3. **Better UX** - Users don't lose tracking data during maintenance
4. **Reliable Anomaly Detection** - Cycle history preserved for ML analysis

### Breaking Changes

None - This release is fully backward compatible. The persistence system gracefully handles missing storage files.

### Migration Notes

- No action required from users
- Existing configurations will start saving state automatically
- First restart after upgrade will not restore data (nothing saved yet)
- Subsequent restarts will benefit from persistence

### Known Limitations

- Storage files are not automatically backed up (use HA backup system)
- No migration system yet for future storage version changes
- No service to manually trigger save operation

## [0.5.0] - 2025-10-21

### Added

#### Auto-Shutdown Feature
- **Automatic appliance shutdown** after configurable inactivity period (5-60 minutes)
  - Optional feature, disabled by default
  - Configurable delay after cycle finish or prolonged inactivity
  - Requires configuration of a switch/plug entity to cut power
  - New event: `EVENT_AUTO_SHUTDOWN`
  - New configuration options: `CONF_ENABLE_AUTO_SHUTDOWN`, `CONF_AUTO_SHUTDOWN_DELAY`, `CONF_AUTO_SHUTDOWN_ENTITY`
  - New switch: `switch.auto_shutdown` to enable/disable the feature
  - Notification sent before shutdown
  - Service `force_shutdown` for manual testing

#### Energy Management System
- **Energy limits monitoring** with configurable thresholds
  - Per-cycle energy limit (e.g., 2 kWh max per cycle)
  - Daily energy limit (e.g., 5 kWh max per day)
  - Monthly energy limit (e.g., 50 kWh max per month)
  - Monthly cost budget (e.g., 10€ max per month)
  - New configuration options: `CONF_ENABLE_ENERGY_LIMITS`, `CONF_ENERGY_LIMIT_CYCLE`, `CONF_ENERGY_LIMIT_DAILY`, `CONF_ENERGY_LIMIT_MONTHLY`, `CONF_COST_BUDGET_MONTHLY`
  - New binary sensors:
    - `binary_sensor.energy_limit_exceeded` - Indicates if any energy limit is exceeded
    - `binary_sensor.budget_exceeded` - Indicates if monthly budget is exceeded
  - New switch: `switch.energy_limits` to enable/disable energy monitoring
  - Automatic notifications when limits are exceeded
  - Reset notifications on new day/month

#### Scheduling System
- **Usage scheduling** with allowed time windows and blocked days
  - Configure allowed hours (e.g., 22h-7h for off-peak hours)
  - Block specific days of the week (e.g., Sunday)
  - Two modes: "notification_only" or "strict_block"
  - New configuration options: `CONF_ENABLE_SCHEDULING`, `CONF_ALLOWED_HOURS_START`, `CONF_ALLOWED_HOURS_END`, `CONF_BLOCKED_DAYS`, `CONF_SCHEDULING_MODE`
  - New binary sensor: `binary_sensor.usage_allowed` - Indicates if current usage is within allowed schedule
  - New switch: `switch.scheduling` to enable/disable scheduling
  - Notification if appliance used outside allowed hours
  - Support for time ranges crossing midnight (e.g., 22:00-07:00)

#### Anomaly Detection
- **Intelligent anomaly detection** based on historical patterns
  - Detects cycles that are too short (<50% of average duration)
  - Detects cycles that are too long (>200% of average duration)
  - Detects abnormal energy consumption (±50% from average)
  - Based on history of last 10 cycles
  - New configuration option: `CONF_ENABLE_ANOMALY_DETECTION`
  - New binary sensor: `binary_sensor.anomaly_detected` - Active when anomaly is detected
  - New sensor: `sensor.anomaly_score` (0-100%) - Real-time anomaly score
  - Automatic notification when anomaly is detected
  - Cycle history tracking in coordinator

#### Data Export
- **CSV export** - Export appliance data to CSV format
  - Current cycle, last cycle, daily and monthly statistics
  - Configuration details included
  - Service: `smart_appliance_monitor.export_to_csv`
  - Optional file path parameter for automatic saving
  - CSV content returned in notification and logs

- **JSON export** - Export appliance data to JSON format
  - Complete structured data export
  - Includes cycle history for anomaly detection
  - Service: `smart_appliance_monitor.export_to_json`
  - Optional file path parameter for automatic saving
  - JSON content returned in notification and logs

- New module: `export.py` - Data export management
  - `SmartApplianceDataExporter` class
  - Export summary generation

#### Energy Dashboard Integration
- **Native Energy Dashboard support**
  - Sensors marked with proper device_class and state_class
  - New module: `energy.py` - Energy Dashboard helper
  - `EnergyDashboardHelper` class for configuration assistance
  - Functions to generate Energy Dashboard configuration
  - Instructions for adding appliances to Energy Dashboard
  - Compatible sensors: `daily_energy`, `monthly_energy`, `cycle_energy`

#### New Sensors (3)
- `sensor.daily_energy` - Daily energy consumption (kWh) with TOTAL state class
- `sensor.monthly_energy` - Monthly energy consumption (kWh) with TOTAL state class
- `sensor.anomaly_score` - Current anomaly score (0-100%)

#### New Binary Sensors (4)
- `binary_sensor.energy_limit_exceeded` - Energy limit status
- `binary_sensor.budget_exceeded` - Budget exceeded status
- `binary_sensor.usage_allowed` - Usage scheduling status
- `binary_sensor.anomaly_detected` - Anomaly detection status

#### New Switches (3)
- `switch.auto_shutdown` - Enable/disable automatic shutdown
- `switch.energy_limits` - Enable/disable energy limits monitoring
- `switch.scheduling` - Enable/disable usage scheduling

#### New Services (3)
- `export_to_csv` - Export data to CSV format
- `export_to_json` - Export data to JSON format
- `force_shutdown` - Manual shutdown trigger (for testing)

#### New Configuration Steps
- **Step: Energy Management** (optional) - Configure energy limits and budget
- **Step: Scheduling** (optional) - Configure allowed hours and blocked days
- **Enhanced Expert Step** - Now includes auto-shutdown configuration

### Changed

#### Configuration Flow
- Added `configure_advanced` toggle in delays step to access energy management and scheduling
- Added `enable_anomaly_detection` toggle in delays step
- Expert step now includes auto-shutdown configuration (delay and entity selection)
- Configuration flow now has up to 6 steps total (init → delays → [energy_management] → [scheduling] → [expert] → notifications)

#### Coordinator
- Monthly stats now track both energy and cost (`total_energy` added)
- New methods: `set_auto_shutdown_enabled()`, `set_energy_limits_enabled()`, `set_scheduling_enabled()`
- New check methods: `_check_auto_shutdown()`, `_check_energy_limits()`, `_check_scheduling()`, `_check_anomaly_detection()`
- New event handlers: `_on_auto_shutdown()`, `_on_energy_limit_exceeded()`, `_on_budget_exceeded()`, `_on_usage_out_of_schedule()`, `_on_anomaly_detected()`
- Cycle history tracking for anomaly detection (`_cycle_history` list)
- Auto-shutdown timer management (`_auto_shutdown_timer`)
- Energy limit notification flags to prevent spam
- Integrated all new features into `_async_update_data()` method

#### Notification System
- Added 5 new notification types: auto_shutdown, energy_limit, budget, schedule, anomaly
- New notification methods in `notify.py`:
  - `notify_auto_shutdown()`
  - `notify_energy_limit_exceeded()`
  - `notify_budget_exceeded()`
  - `notify_usage_out_of_schedule()`
  - `notify_anomaly_detected()`

### Improved

#### Statistics
- Monthly energy tracking added (was cost-only before)
- Cycle history for machine learning analysis
- Better reset logic for daily/monthly boundaries

#### Code Quality
- All new features follow existing architecture patterns
- Comprehensive error handling in all new modules
- Logging added for all major operations
- Type hints throughout new code

### Technical Details

#### Files Created
- `custom_components/smart_appliance_monitor/export.py` (235 lines)
- `custom_components/smart_appliance_monitor/energy.py` (175 lines)

#### Files Modified
- `const.py` (+100 lines) - 50+ new constants for all features
- `config_flow.py` (+150 lines) - 2 new steps, enhanced expert step
- `coordinator.py` (+350 lines) - All feature logic and checks
- `switch.py` (+130 lines) - 3 new switch classes
- `sensor.py` (+150 lines) - 3 new sensor classes
- `binary_sensor.py` (+160 lines) - 4 new binary sensor classes
- `notify.py` (+170 lines) - 5 new notification methods
- `services.yaml` (+60 lines) - 3 new service definitions
- `__init__.py` (+120 lines) - 3 new service handlers
- `manifest.json` - Version updated to 0.5.0

#### Total Entity Count
- **Sensors**: 13 (was 10)
  - Added: `daily_energy`, `monthly_energy`, `anomaly_score`
- **Binary Sensors**: 7 (was 3)
  - Added: `energy_limit_exceeded`, `budget_exceeded`, `usage_allowed`, `anomaly_detected`
- **Switches**: 9 (was 6)
  - Added: `auto_shutdown`, `energy_limits`, `scheduling`
- **Buttons**: 1 (unchanged)

**Total per appliance: 30 entities** (was 20)

### Breaking Changes

None - This release is fully backward compatible. All new features are optional and disabled by default.

### Migration Notes

- Existing configurations will continue to work without changes
- No database migration required
- Monthly stats now include `total_energy` field (automatically initialized to 0.0)
- New configuration options available in Options Flow

### Known Limitations

- Anomaly detection requires at least 3 completed cycles for meaningful analysis
- Auto-shutdown requires a switch/plug entity that can be controlled by Home Assistant
- Scheduling does not support multiple time windows (only one per day)
- Custom cards still require manual build (run `npm install && npm run build` in `/www/smart-appliance-cards/`)

## [0.4.1] - 2025-10-20

### Added
- **Bundled Dashboard Templates** - Templates now included directly in the integration
  - 7 templates embedded in `/custom_components/smart_appliance_monitor/dashboards/`
  - Automatic installation, no manual setup required
  - Users can override templates by creating `/config/dashboards/templates/`

### Changed
- **Template Loading Priority** - Smart template resolution
  1. First checks `/config/dashboards/templates/` (user custom templates)
  2. Then falls back to `/custom_components/smart_appliance_monitor/dashboards/` (bundled templates)
  - Allows users to customize templates without modifying integration files
  - Ensures templates always available out-of-the-box

### Fixed
- **Dashboard Generation Error** - Fixed "No such file or directory" error
  - Templates no longer require manual creation in `/config/dashboards/templates/`
  - Service `generate_dashboard_yaml` now works immediately after installation
  - Better error handling with clear fallback mechanism

### Improved
- **User Experience** - Zero configuration for dashboard templates
  - No need to read installation docs for basic usage
  - Templates "just work" after integration installation
  - Advanced users can still customize by placing templates in `/config/dashboards/templates/`

### Technical Details
- Templates location: `/custom_components/smart_appliance_monitor/dashboards/*.yaml`
- Custom templates location: `/config/dashboards/templates/*.yaml` (optional)
- Priority: custom → bundled → generic
- Backward compatible with existing custom template setups

## [0.4.0] - 2025-10-20

### Added

#### Multi-Step Configuration Flow
- **4-Step Advanced Configuration** - Configuration divided into logical steps
  - Step 1: Detection Thresholds (start/stop power thresholds)
  - Step 2: Detection Delays & Alerts (with expert mode toggle)
  - Step 3: Notifications (services and types selection)
  - Step 4: Expert Settings (optional, only if expert mode enabled)
- Better UX with focused screens instead of single overwhelming form
- Progressive navigation through configuration process

#### User-Friendly Time Units
- **Minutes for delays** - Instead of seconds for better comprehension
  - Start delay: 0.5-10 minutes (was 10-600 seconds)
  - Stop delay: 0.5-30 minutes (was 10-1800 seconds)
- **Hours for alerts** - Instead of seconds for duration alerts
  - Alert duration: 0.5-24 hours (was 1800-86400 seconds)
- **Minutes for unplugged timeout** - In expert settings
  - Unplugged timeout: 1-60 minutes (was 60-3600 seconds)
- Automatic bidirectional conversion (display ↔ storage)
- Values still stored in seconds internally for full backward compatibility

#### Expert Mode
- **Optional Expert Settings** - Advanced parameters hidden by default
  - Unplugged detection timeout
  - Custom notification service name
- Toggle in Step 2 to access expert settings
- Simplified interface for standard users
- Full power for advanced users when needed

#### Enhanced Descriptions
- **Detailed explanations** for every configuration field
- **Concrete examples** adapted to appliance type
  - "100W for oven, 10W for washing machine"
- **Recommended value ranges** clearly indicated
- **Contextual help** explaining what each parameter does

### Changed

#### Configuration Flow
- Options flow completely refactored from single to multi-step
- `async_step_init()` - Now handles only thresholds (step 1)
- New `async_step_delays()` - Handles delays and alerts (step 2)
- New `async_step_notifications()` - Handles notification settings (step 3)
- New `async_step_expert()` - Handles expert parameters (step 4)
- State persistence across steps with `self._options`

#### Translation Files
- English strings updated with 4 new step definitions
- French translations updated with complete localization
- All field labels updated to reflect new units
- Descriptions significantly enhanced in both languages

### Improved

#### User Experience
- **Reduced cognitive load** - 2-5 fields per screen instead of 10
- **Clearer progression** - Logical flow from thresholds → delays → notifications
- **Natural units** - Minutes and hours instead of seconds
- **Better accessibility** - Expert options hidden by default
- **Contextual guidance** - Each step has clear description and purpose

#### Configuration Quality
- **Easier to understand** - Natural time units (2 min vs 120 sec)
- **Harder to make mistakes** - Smaller ranges with appropriate steps
- **Better defaults visible** - Values make more sense to users
- **Flexible validation** - Supports decimal values (1.5 minutes = 90 seconds)

### Technical Details

#### Files Modified
- `config_flow.py` - 210+ lines refactored
  - Multi-step flow implementation
  - Automatic unit conversions (min↔sec, h↔sec)
  - Conditional navigation (expert mode)
  
- `strings.json` - Complete restructuring
  - 4 step definitions (init, delays, notifications, expert)
  - New field names with unit suffixes
  - Enhanced descriptions with examples
  
- `translations/fr.json` - Full French localization
  - All 4 steps translated
  - Natural French expressions
  - Localized examples

#### Backward Compatibility
- ✅ **100% backward compatible**
- Existing configurations load without modification
- Old values in seconds automatically converted to minutes/hours for display
- Modified values automatically converted back to seconds for storage
- No migration script needed
- Internal storage format unchanged

#### Unit Conversions
```python
# Display conversion
start_delay_minutes = config_value_seconds / 60

# Storage conversion  
config_value_seconds = user_input_minutes * 60
```

### Notes
- Expert mode toggle is not persisted in configuration (UI-only flag)
- All validation ranges adapted to new units
- Decimal values supported (e.g., 1.5 hours = 5400 seconds)
- Documentation updated with migration guide

### Breaking Changes
None - This is a UX improvement release with full backward compatibility.

## [0.3.0] - 2025-10-20

### Added

#### Dashboard Templates (7)
- **Dashboard Template System** - Pre-configured Lovelace YAML templates for each appliance type
  - `generic.yaml` - Universal template for any appliance
  - `washing_machine.yaml` - Optimized for washing machines (1-3h cycles)
  - `dishwasher.yaml` - Optimized for dishwashers (2-4h cycles)
  - `monitor.yaml` - For screens/displays (session-based, up to 8h)
  - `nas.yaml` - For NAS devices (session-based, intensive activity detection)
  - `printer_3d.yaml` - For 3D printers (extended cycles up to 24h+)
  - `vmc.yaml` - For ventilation systems (session-based, boost mode detection)

#### Dashboard Generation Service
- **`generate_dashboard_yaml` Service** - Automatically generates dashboard YAML
  - Detects appliance type and loads appropriate template
  - Replaces all entity ID placeholders automatically
  - Sends persistent notification with complete YAML code
  - Logs full YAML for easy copy-paste
  - Optional custom cards support parameter

#### Dashboard Features
- **6 Pre-configured Sections per Dashboard**:
  - Status Overview - Large visual card with state and badges
  - Current Cycle/Session - Duration gauge, energy, cost
  - Power Consumption - 24h power graph with Mini Graph Card
  - Controls - All switches and buttons in one place
  - Statistics - Last cycle, daily, and monthly stats
  - Alerts - Conditional cards for duration/unplugged warnings
  
- **Custom Card Integration**:
  - Mushroom Cards for modern UI
  - Mini Graph Card for power consumption visualization
  - Conditional cards for alerts
  - Template cards with dynamic colors and icons

- **Adaptive Layouts**:
  - Templates adapt to appliance type (cycle vs session terminology)
  - Gauge ranges optimized per appliance type
  - Appropriate icons and colors
  - Mobile-friendly responsive design

#### Documentation
- **Dashboard README** (`/dashboards/README.md`) - Complete guide with:
  - Installation instructions for custom cards
  - Manual and service-based setup methods
  - Customization examples
  - Troubleshooting guide
  - Multi-appliance dashboard examples
  
- **Wiki Page** (`Dashboards.md`) - Comprehensive documentation:
  - Quick start guide
  - Template descriptions
  - Screenshot galleries (to be added)
  - Custom card installation
  - Advanced customization

### Changed
- **English as Default Language** - All code, services, and templates now in English
  - Python code messages translated to English
  - Service definitions (`services.yaml`) in English
  - Dashboard templates in English
  - French translations maintained in `fr.json`
  
- **Notification Messages** - Dashboard generation notifications in English

### Technical Details
- **Template System**: 7 YAML files in `/dashboards/templates/`
- **Service Implementation**: `generate_dashboard_yaml` in `__init__.py`
- **Total Lines of YAML**: ~1,500 lines across all templates
- **Custom Cards Supported**: Mushroom, Mini Graph Card, Button Card

### Breaking Changes
None - This is a feature addition release.

### Notes
- Custom cards (Mushroom, Mini Graph Card) must be installed via HACS for full visual experience
- Templates work with standard HA cards but are optimized for custom cards
- Dashboard YAML must be manually copied to dashboard (auto-creation planned for v0.4.0)

## [0.2.0] - 2025-10-20

### Added

#### Core Features
- **Automatic Cycle Detection** - State machine-based detection with configurable thresholds and delays
- **Data Coordinator** - Centralized data management with 30-second polling interval
- **Configuration Flow** - Complete UI-based configuration and reconfiguration
- **Multi-language Support** - Full interface in English and French

#### Entities (14 per appliance)
- **Sensors (10)**:
  - State (idle/running/finished)
  - Cycle duration, energy, and cost (current cycle)
  - Last cycle duration, energy, and cost
  - Daily cycles count and cost
  - Monthly cost
- **Binary Sensors (2)**:
  - Running status
  - Duration alert
- **Switches (2)**:
  - Monitoring enable/disable
  - Notifications enable/disable
- **Buttons (1)**:
  - Reset statistics

#### Services
- `start_cycle` - Manually trigger cycle start
- `stop_monitoring` - Disable monitoring for specific appliance
- `reset_statistics` - Clear all statistics

#### Appliance Profiles
Pre-configured optimized thresholds for different appliance types:
- **Oven** - 100W start threshold, 2h alert
- **Dishwasher** - 20W start threshold, 3h alert
- **Washing Machine** - 10W start threshold, 3h alert
- **Dryer** - 100W start threshold, 2h alert
- **Water Heater** - 1000W start threshold, 4h alert
- **Coffee Maker** - 50W start threshold, 30min alert
- **Other** - 50W start threshold, 2h alert

#### Dynamic Pricing
- Support for electricity price via Home Assistant entities (`input_number` or `sensor`)
- Automatic fallback to fixed price if entity unavailable
- Real-time cost calculation based on current rate

#### Reconfiguration
- Modify all base settings without losing statistics
- Update appliance type (thresholds auto-adapt)
- Change sensors (power/energy)
- Switch between fixed and dynamic pricing
- Rename appliances

#### Notifications
- Cycle started notifications with appliance details
- Cycle finished notifications with duration, energy, and cost
- Duration alert notifications for cycles exceeding expected time
- Automatic fallback to persistent notifications

#### Testing
- 75+ unit tests across all components
- ~95% code coverage
- Fixtures for common test scenarios
- Pytest configuration with markers

#### Documentation
- Comprehensive README
- Development guide
- Implementation summary
- Complete API documentation in code

### Technical Details

#### Components Implemented
- `state_machine.py` - Cycle detection logic (260 lines)
- `coordinator.py` - Data coordination (389 lines)
- `config_flow.py` - Configuration UI (256 lines)
- `sensor.py` - Sensor platform (395 lines)
- `binary_sensor.py` - Binary sensor platform (124 lines)
- `switch.py` - Switch platform (128 lines)
- `button.py` - Button platform (80 lines)
- `notify.py` - Notification system (230 lines)
- `entity.py` - Base entity class (50 lines)
- `device.py` - Device utilities (70 lines)
- `services.yaml` - Service definitions (51 lines)

#### Statistics Tracking
- Per-cycle statistics (duration, energy, cost)
- Daily statistics (cycle count, total cost)
- Monthly statistics (total cost)
- Persistent storage across restarts

#### Configuration Options
- Appliance name and type
- Power and energy sensors
- Electricity price (fixed or entity-based)
- Start/stop thresholds (W)
- Start/stop delays (seconds)
- Duration alert threshold (seconds)
- Duration alert enable/disable

### Performance
- Lightweight polling (30-second intervals)
- Efficient state machine with minimal overhead
- Optimized sensor updates
- Smart caching of price data

### Known Limitations
- Single appliance per configuration entry
- No machine learning auto-calibration (planned for v0.5.0)
- No built-in dashboard generation (planned for v0.5.0)
- No direct Energy Dashboard integration (planned for v0.2.0)

## [0.2.0] - 2025-10-20

### Added

#### New Appliance Types (4)
- **Monitor (Écran)** - Screen/display usage session tracking
  - 30W start threshold, 5W stop threshold
  - 8-hour alert duration for long sessions
  - Uses "session" terminology instead of "cycle"
- **NAS** - Network storage intensive activity detection
  - 50W start threshold (detects intensive activity above baseline)
  - 20W stop threshold (return to idle)
  - 6-hour alert duration for long backups/transfers
  - Uses "session" terminology instead of "cycle"
- **3D Printer (Imprimante 3D)** - Long-duration print monitoring
  - 50W start threshold, 10W stop threshold
  - 24-hour alert duration (essentially disabled for very long prints)
- **VMC (Ventilation)** - Ventilation boost mode detection
  - 20W start threshold, 10W stop threshold
  - 2-hour alert duration for extended boost periods
  - Uses "session" terminology instead of "cycle"

#### Session-Based Terminology
- Smart terminology adaptation based on appliance type
- Monitor, NAS, and VMC now use "session" terminology for better UX
- Dynamic sensor naming: `session_duration`, `session_energy`, `session_cost`, `daily_sessions`
- Automatic translation key selection based on appliance type
- Improves clarity for devices with continuous or intensive operation patterns

#### Unplugged Detection
- **New Binary Sensor**: `binary_sensor.unplugged`
  - Detects when appliance is disconnected or powered off
  - Configurable timeout (default: 5 minutes at 0W)
  - Device class: `PROBLEM`
  - Extra attributes: `time_at_zero_power`, `unplugged_timeout`, `detection_progress`
- Automatic notification when appliance detected as unplugged
- Helps identify power issues and accidental disconnections
- Tracks zero-power duration in state machine

#### Advanced Notification System
- **Multi-service notification support**:
  - Mobile App (automatic detection of available mobile_app_* services)
  - Telegram (with markdown formatting)
  - Persistent Notification (fallback)
  - Custom service (user-configurable)
- **Per-notification-type control** with 4 configurable types:
  - Cycle/Session Started
  - Cycle/Session Finished
  - Alert Duration
  - Unplugged Alert
- **Two-level control system**:
  - Configuration via Options Flow (persistent settings)
  - Quick-toggle switches for each notification type
- Notification service configuration in Options Flow
- Custom notification service name support
- Intelligent service availability detection

#### New Switches (4)
- `switch.notification_cycle_started` - Toggle start notifications
- `switch.notification_cycle_finished` - Toggle completion notifications
- `switch.notification_alert_duration` - Toggle duration alerts
- `switch.notification_unplugged` - Toggle unplugged alerts
- All switches enabled by default
- Independent control without affecting configuration
- Icons adapt to switch state

#### Configuration Options
- `unplugged_timeout` - Time at 0W before detecting as unplugged (60-3600s, default: 300s)
- `notification_services` - Multi-select for notification services
- `notification_types` - Multi-select for notification types to receive
- `custom_notify_service` - Custom notification service name

### Changed
- **Sensor entity IDs** now adapt based on appliance type
  - Cycle-based: `cycle_duration`, `cycle_energy`, etc.
  - Session-based: `session_duration`, `session_energy`, etc.
- **Notification system** completely refactored for extensibility
  - SmartApplianceNotifier class redesigned
  - Support for simultaneous multiple services
  - Service-specific formatting (e.g., Telegram markdown)
- **Binary sensor platform** extended with unplugged detection
- **Switch platform** extended with 4 notification type switches
- **State machine** enhanced with zero-power tracking
- **Coordinator** integrated all new systems and event handlers

### Improved
- **Better UX** with context-aware terminology (cycle vs session)
- **Flexible notification configuration** at multiple levels
  - Global enable/disable switch
  - Service selection in options
  - Type selection in options
  - Individual switches per type
- **Enhanced monitoring** with unplugged detection
- **Better device categorization** with 11 appliance types total
- **More granular control** over notification behavior
- **Documentation** significantly expanded

### Technical Details
- Total entities per appliance: **19** (up from 15)
  - 10 Sensors (adaptive naming)
  - 3 Binary Sensors (running, alert_duration, **unplugged**)
  - 6 Switches (monitoring, notifications, **4 notification type switches**)
  - 1 Button (reset stats)
- New events: `smart_appliance_monitor_unplugged`
- State machine now tracks zero-power time
- Coordinator handles 4 event types (was 3)
- Full bilingual support (EN/FR) for all new features

