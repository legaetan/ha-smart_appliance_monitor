# Testing Dashboard Integration

## Overview

This guide provides comprehensive testing instructions for the unified multi-tab dashboard feature introduced in Smart Appliance Monitor.

## ⚠️ Important Notes

**Recent Corrections Applied:**
- ✅ Sections converted to cards automatically
- ✅ Fallback to standard cards if custom cards not installed
- ✅ Overview view built dynamically with real entities
- ✅ Custom cards detection implemented
- ✅ Detailed logging added

**See** `DASHBOARD_CORRECTIONS_APPLIED.md` for full details.

## Prerequisites

- Home Assistant running with Smart Appliance Monitor installed
- At least 2-3 appliances configured
- Access to Home Assistant Developer Tools
- Access to File Editor or SSH for checking storage files

## Test Scenarios

### 1. Initial Dashboard Creation

**Test: Create the dashboard for the first time**

```yaml
# In Developer Tools > Services
service: smart_appliance_monitor.create_dashboard
data:
  force_recreate: false
```

**Expected Results:**
- ✅ Service call successful
- ✅ Dashboard appears at `/lovelace/smart-appliances`
- ✅ Overview tab visible as first tab
- ✅ One tab per configured appliance
- ✅ Tabs show appliance icons
- ✅ Configuration file created at `.storage/smart_appliance_monitor.dashboard_config`

**Check Dashboard Structure:**
1. Navigate to `/lovelace/smart-appliances`
2. Verify tabs:
   - Tab 1: "Overview" (global view)
   - Tab 2+: Each configured appliance

**Check Storage File:**
```bash
cat .storage/smart_appliance_monitor.dashboard_config
```

Expected structure:
```json
{
  "dashboard_id": "smart_appliances",
  "global_settings": {
    "use_custom_cards": true,
    "auto_update": true,
    "color_scheme": {...}
  },
  "overview_config": {...},
  "appliance_views": {...}
}
```

---

### 2. Auto-Update: Add New Appliance

**Test: Dashboard automatically adds a view when appliance is added**

1. Add a new appliance via Configuration > Integrations > Add Integration
2. Configure a new Smart Appliance Monitor instance
3. Wait 5 seconds

**Expected Results:**
- ✅ New tab appears in dashboard automatically
- ✅ Tab shows appliance icon and name
- ✅ View contains all appliance sections
- ✅ Log message: "Dashboard view added for [appliance_name]"

**Verify in Logs:**
```
Smart Appliance Monitor: Dashboard view added for Lave-Linge
```

---

### 3. Auto-Update: Remove Appliance

**Test: Dashboard automatically removes a view when appliance is removed**

1. Remove an appliance via Configuration > Integrations
2. Delete the Smart Appliance Monitor instance
3. Wait 5 seconds

**Expected Results:**
- ✅ Tab disappears from dashboard automatically
- ✅ Overview tab still present
- ✅ Other tabs unaffected
- ✅ Log message: "Dashboard view removed for [appliance_name]"

---

### 4. Manual Update

**Test: Manually update the dashboard**

```yaml
service: smart_appliance_monitor.update_dashboard
```

**Expected Results:**
- ✅ Service call successful
- ✅ Dashboard refreshed
- ✅ All current appliances have tabs
- ✅ Removed appliances' tabs are gone

---

### 5. Configure Global Settings

**Test: Apply global configuration changes**

```yaml
service: smart_appliance_monitor.configure_dashboard
data:
  global_settings:
    use_custom_cards: false
    auto_update: true
    color_scheme:
      primary: "#e74c3c"
      secondary: "#3498db"
```

**Expected Results:**
- ✅ Configuration saved to storage
- ✅ Dashboard rebuilt with new settings
- ✅ Custom cards disabled (standard cards used)
- ✅ Primary color changed

**Verify:**
1. Check storage file for updated values
2. Reload dashboard and check colors
3. Check if standard cards replaced custom cards

---

### 6. Configure Overview Sections

**Test: Control which sections appear in Overview**

```yaml
service: smart_appliance_monitor.configure_dashboard
data:
  overview_sections:
    - metrics
    - monitoring
    - energy_costs
```

**Expected Results:**
- ✅ Overview tab shows only specified sections
- ✅ Other sections hidden
- ✅ Individual appliance tabs unaffected

---

### 7. Configure Per-Appliance View

**Test: Customize individual appliance view**

```yaml
service: smart_appliance_monitor.configure_dashboard
data:
  appliance_views:
    lave_linge:
      enabled: true
      template: washing_machine
      color: "#9b59b6"
      sections:
        status: true
        statistics: true
        controls: true
        ai_analysis: false
```

**Expected Results:**
- ✅ Lave-Linge tab color changed to purple
- ✅ AI Analysis section hidden
- ✅ Other sections visible
- ✅ Template remains washing_machine

---

### 8. Toggle View On/Off

**Test: Enable/disable individual views**

```yaml
# Disable a view
service: smart_appliance_monitor.toggle_view
data:
  appliance_id: lave_vaisselle
  enabled: false
```

**Expected Results:**
- ✅ Lave-Vaisselle tab disappears
- ✅ Configuration updated (enabled: false)
- ✅ Other tabs unaffected

```yaml
# Re-enable the view
service: smart_appliance_monitor.toggle_view
data:
  appliance_id: lave_vaisselle
  enabled: true
```

**Expected Results:**
- ✅ Lave-Vaisselle tab reappears
- ✅ Tab restored with previous settings

---

### 9. Force Recreate

**Test: Completely rebuild the dashboard**

```yaml
service: smart_appliance_monitor.create_dashboard
data:
  force_recreate: true
```

**Expected Results:**
- ✅ Dashboard deleted and recreated
- ✅ All tabs present
- ✅ Configuration preserved
- ✅ Views match current config

**Use Case:** Dashboard corrupted or manual Lovelace edits need to be overwritten

---

### 10. Configuration Panel (Sidebar)

**Test: Access configuration panel**

1. Navigate to Home Assistant sidebar
2. Look for "⚡ Smart Appliances Settings" or similar entry
3. Click to open panel

**Expected Results:**
- ✅ Panel opens
- ✅ Global settings section visible
- ✅ Overview configuration visible
- ✅ List of all appliances with status
- ✅ Buttons: Create, Update, Configure, etc.

**Note:** Frontend panel implementation may require additional testing once JavaScript is loaded.

---

### 11. Performance Test

**Test: Dashboard with many appliances (stress test)**

**Setup:**
- Configure 10+ appliances
- Create dashboard

**Expected Results:**
- ✅ Dashboard loads in < 5 seconds
- ✅ All tabs present
- ✅ Navigation smooth
- ✅ No memory leaks
- ✅ No lag when switching tabs

---

### 12. Persistence Test

**Test: Configuration survives restart**

1. Configure dashboard with custom settings
2. Restart Home Assistant
3. Check dashboard

**Expected Results:**
- ✅ Dashboard still exists
- ✅ Configuration preserved
- ✅ Custom colors/settings intact
- ✅ All tabs present

---

### 13. Migration Test

**Test: Upgrade from version without dashboard feature**

1. Install new version with dashboard feature
2. Restart Home Assistant

**Expected Results:**
- ✅ Integration loads successfully
- ✅ Default dashboard config created
- ✅ No errors in logs
- ✅ Dashboard can be created via service

---

### 14. Error Handling

**Test: Invalid configuration**

```yaml
service: smart_appliance_monitor.configure_dashboard
data:
  appliance_views:
    nonexistent_appliance:
      enabled: true
```

**Expected Results:**
- ✅ Error logged (appliance not found)
- ✅ Dashboard not rebuilt
- ✅ Existing config intact

---

### 15. Template Switching

**Test: Change appliance template**

```yaml
service: smart_appliance_monitor.configure_dashboard
data:
  appliance_views:
    mon_serveur:
      template: nas  # Instead of generic
```

**Expected Results:**
- ✅ View rebuilt with NAS template
- ✅ Cards specific to NAS appear
- ✅ Appliance data still correct

---

## Logs to Monitor

Enable debug logging for detailed information:

```yaml
# configuration.yaml
logger:
  default: info
  logs:
    custom_components.smart_appliance_monitor: debug
```

**Key Log Messages:**

- `Dashboard managers initialized`
- `Dashboard configuration panel registered`
- `Dashboard view added for [appliance_name]`
- `Dashboard view removed for [appliance_name]`
- `Rebuilding dashboard...`
- `Dashboard created/updated successfully`

---

## Common Issues and Solutions

### Dashboard doesn't appear

**Solution:**
1. Check logs for errors
2. Verify Lovelace is not in YAML mode
3. Try force recreate: `force_recreate: true`

### Auto-update not working

**Solution:**
1. Check config: `auto_update: true`
2. Verify listeners registered
3. Check logs for errors

### Missing tabs

**Solution:**
1. Check view is enabled in config
2. Verify coordinator exists
3. Run `update_dashboard` service

### Colors not applying

**Solution:**
1. Check color format: `#RRGGBB`
2. Rebuild dashboard
3. Clear browser cache

---

## Success Criteria

All tests pass if:

- ✅ Dashboard created successfully
- ✅ Auto-update works (add/remove appliances)
- ✅ Configuration persists across restarts
- ✅ Customization applies correctly
- ✅ No errors in logs
- ✅ Performance acceptable (< 5s load time)

---

## Testing Checklist

Use this checklist to track testing progress:

- [ ] Initial dashboard creation
- [ ] Auto-add appliance view
- [ ] Auto-remove appliance view
- [ ] Manual update
- [ ] Configure global settings
- [ ] Configure overview sections
- [ ] Configure per-appliance view
- [ ] Toggle view on/off
- [ ] Force recreate
- [ ] Configuration panel access
- [ ] Performance with 10+ appliances
- [ ] Persistence after restart
- [ ] Migration from old version
- [ ] Error handling
- [ ] Template switching

---

## Reporting Issues

When reporting issues, include:

1. **Home Assistant version**
2. **Smart Appliance Monitor version**
3. **Steps to reproduce**
4. **Expected vs actual results**
5. **Relevant logs** (with debug enabled)
6. **Storage file contents** (`.storage/smart_appliance_monitor.dashboard_config`)
7. **Screenshot of dashboard or error**

---

## Next Steps

After successful testing:

1. Test in production environment
2. Gather user feedback
3. Document any issues
4. Update release notes
5. Create user guide/wiki

