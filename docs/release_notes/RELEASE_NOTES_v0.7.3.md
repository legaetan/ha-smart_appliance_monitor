# Release Notes - v0.7.3

**Release Date**: October 21, 2025  
**Type**: Bug Fix Release  
**Priority**: High (Recommended for all v0.7.x users)

---

## 🐛 Bug Fixes

### AI Analysis Response Parsing

**Problem**: AI analysis results were appearing empty - the `recommendations` and `insights` fields in `sensor.<appliance>_ai_analysis` remained blank even after successful analysis.

**Root Cause**: The AI Task service was not adhering to the strict JSON structure requirements, and the parsing logic was reading from the wrong response key.

**Solution**:
- ✅ Switched from strict JSON structure to Markdown-based AI responses
- ✅ Implemented robust Markdown parser to extract structured data from AI responses
- ✅ Corrected response key from `response["text"]` to `response["data"]`
- ✅ Added extensive debug logging to track AI response processing

**Impact**: AI analysis now returns complete, structured data with actionable recommendations and insights.

---

### Coordinator Entity Matching

**Problem**: Calling `analyze_cycles` service resulted in error: `Unable to find coordinator for entity sensor.chauffe_eau_etat`

**Root Cause**: The `_get_coordinator_from_entity_id()` function couldn't properly match entities when appliance names contained underscores (e.g., "Chauffe-Eau" → `chauffe_eau`).

**Solution**:
- ✅ Improved slug matching logic to handle underscores in appliance names
- ✅ Added explicit `appliance_slug + "_"` check at the beginning of entity suffix
- ✅ Made coordinator discovery more robust

**Impact**: All appliances with multi-word names (containing spaces or hyphens) now work correctly with AI analysis services.

---

### AI Prompt Engineering

**Improvements**:
- Enhanced AI prompts to request structured Markdown format with explicit headers
- Added mandatory requirements for concrete recommendations and insights
- Improved guidance for AI to provide actionable, non-empty content
- Set `structure` parameter to `None` to allow free-form Markdown responses

---

## 🔧 Technical Changes

### Files Modified

1. **`custom_components/smart_appliance_monitor/ai_client.py`**
   - Completely rewrote `_process_cycle_analysis_response()` to parse Markdown
   - Added `parse_section()` helper function
   - Enhanced error handling for malformed responses
   - Added extensive debug logging

2. **`custom_components/smart_appliance_monitor/__init__.py`**
   - Improved `_get_coordinator_from_entity_id()` function
   - More robust entity-to-coordinator matching

3. **Version Files**
   - `version` → `0.7.3`
   - `manifest.json` → `"version": "0.7.3"`

### Debugging Improvements

- Added `_LOGGER.debug` statements for raw AI responses
- Added logging for each parsed section (summary, status, recommendations, etc.)
- Better error messages when coordinator cannot be found

---

## 📦 Migration Guide

### From v0.7.0, v0.7.1, or v0.7.2

1. **Update the integration** to v0.7.3
2. **Restart Home Assistant**
3. **Test AI analysis** with any appliance:
   ```yaml
   service: smart_appliance_monitor.analyze_cycles
   data:
     entity_id: sensor.your_appliance_etat
     analysis_type: all
     cycle_count: 10
   ```
4. **Check the results** in `sensor.your_appliance_ai_analysis`
5. **Verify logs** for detailed parsing information (if needed)

### Configuration Changes

**No configuration changes required** - this is a pure bug fix release.

---

## ⚠️ Known Limitations

- AI analysis still requires manual configuration via `smart_appliance_monitor.configure_ai` service
- Markdown parsing assumes specific header names (Summary, Status, Recommendations, etc.)
- Some AI models may still return empty sections if they don't follow the prompt structure

---

## 🎯 What's Next?

Version 0.7.4 (planned) will include:
- Automatic AI configuration detection
- Support for alternative AI response formats
- Enhanced prompt templates for better AI guidance
- Improved error recovery for malformed AI responses

---

## 📝 Detailed Changelog

See [CHANGELOG.md](../../CHANGELOG.md#073---2025-10-21) for complete technical details.

---

## 🙏 Credits

This release fixes critical issues reported by the community. Thank you for your feedback and testing!

**Issues Resolved**:
- Empty AI analysis recommendations and insights
- Coordinator matching errors for multi-word appliance names
- Improved debugging capabilities for AI response processing


