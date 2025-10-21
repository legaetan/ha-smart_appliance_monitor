"""The Smart Appliance Monitor integration."""
from __future__ import annotations

import logging
from pathlib import Path

import voluptuous as vol

from homeassistant.components.http import StaticPathConfig
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv

from .const import (
    DOMAIN,
    CONF_APPLIANCE_TYPE,
    APPLIANCE_TYPE_WASHING_MACHINE,
    APPLIANCE_TYPE_DISHWASHER,
    APPLIANCE_TYPE_MONITOR,
    APPLIANCE_TYPE_NAS,
    APPLIANCE_TYPE_PRINTER_3D,
    APPLIANCE_TYPE_VMC,
)
from .coordinator import SmartApplianceCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.BINARY_SENSOR, Platform.BUTTON, Platform.SWITCH]

# Schémas des services
SERVICE_START_CYCLE_SCHEMA = vol.Schema(
    {
        vol.Required("entity_id"): cv.entity_id,
    }
)

SERVICE_STOP_MONITORING_SCHEMA = vol.Schema(
    {
        vol.Required("entity_id"): cv.entity_id,
    }
)

SERVICE_RESET_STATISTICS_SCHEMA = vol.Schema(
    {
        vol.Required("entity_id"): cv.entity_id,
    }
)

SERVICE_GENERATE_DASHBOARD_YAML_SCHEMA = vol.Schema(
    {
        vol.Required("entity_id"): cv.entity_id,
        vol.Optional("use_custom_cards", default=True): cv.boolean,
    }
)

SERVICE_EXPORT_TO_CSV_SCHEMA = vol.Schema(
    {
        vol.Required("entity_id"): cv.entity_id,
        vol.Optional("file_path"): cv.string,
    }
)

SERVICE_EXPORT_TO_JSON_SCHEMA = vol.Schema(
    {
        vol.Required("entity_id"): cv.entity_id,
        vol.Optional("file_path"): cv.string,
    }
)

SERVICE_FORCE_SHUTDOWN_SCHEMA = vol.Schema(
    {
        vol.Required("entity_id"): cv.entity_id,
    }
)

SERVICE_SYNC_WITH_ENERGY_DASHBOARD_SCHEMA = vol.Schema(
    {
        vol.Optional("entity_id"): cv.entity_id,
    }
)

SERVICE_EXPORT_ENERGY_CONFIG_SCHEMA = vol.Schema(
    {
        vol.Required("entity_id"): cv.entity_id,
    }
)

SERVICE_GET_ENERGY_DATA_SCHEMA = vol.Schema(
    {
        vol.Optional("period_start"): cv.string,
        vol.Optional("period_end"): cv.string,
        vol.Optional("devices"): cv.ensure_list,
    }
)

SERVICE_ANALYZE_CYCLES_SCHEMA = vol.Schema(
    {
        vol.Required("entity_id"): cv.entity_id,
        vol.Optional("analysis_type", default="all"): vol.In(["pattern", "comparative", "recommendations", "all"]),
        vol.Optional("cycle_count", default=10): cv.positive_int,
        vol.Optional("export_format", default="json"): vol.In(["json", "csv", "both"]),
        vol.Optional("save_export", default=False): cv.boolean,
    }
)

SERVICE_ANALYZE_ENERGY_DASHBOARD_SCHEMA = vol.Schema(
    {
        vol.Optional("period", default="today"): vol.In(["today", "yesterday", "week", "month"]),
        vol.Optional("compare_previous", default=False): cv.boolean,
        vol.Optional("include_recommendations", default=True): cv.boolean,
    }
)

SERVICE_CONFIGURE_AI_SCHEMA = vol.Schema(
    {
        vol.Optional("ai_task_entity"): cv.entity_id,
        vol.Optional("global_price_entity"): cv.entity_id,
        vol.Optional("enable_ai_analysis"): cv.boolean,
        vol.Optional("ai_analysis_trigger"): vol.In(["auto_cycle_end", "manual", "periodic_daily", "periodic_weekly"]),
    }
)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Smart Appliance Monitor from a config entry."""
    _LOGGER.info("Setting up Smart Appliance Monitor integration for '%s'", entry.data.get("appliance_name"))
    
    hass.data.setdefault(DOMAIN, {})
    
    # Initialize global config manager if not already done
    if "global_config" not in hass.data[DOMAIN]:
        from .storage_config import GlobalConfigManager
        global_config = GlobalConfigManager(hass)
        await global_config.async_load()
        hass.data[DOMAIN]["global_config"] = global_config
        _LOGGER.info("Global AI configuration manager initialized")
    
    # Créer le coordinator
    coordinator = SmartApplianceCoordinator(hass, entry)
    
    # Restaurer l'état depuis le stockage persistant
    await coordinator.restore_state()
    
    # Load global AI configuration
    await coordinator.load_global_ai_config()
    
    await coordinator.async_config_entry_first_refresh()
    
    # Stocker le coordinator
    hass.data[DOMAIN][entry.entry_id] = coordinator
    
    # Charger les platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    # Energy Dashboard synchronization check (async)
    hass.async_create_task(_async_check_energy_sync(hass, coordinator))
    
    # Enregistrer les services (une seule fois)
    # Check for one of the latest services to ensure all are registered (v0.7.0+)
    if not hass.services.has_service(DOMAIN, "configure_ai"):
        await async_setup_services(hass)
        _LOGGER.info("Smart Appliance Monitor services registered (13 services including AI)")
    
    # Register frontend resources for custom Lovelace cards (once)
    if not hasattr(hass.data[DOMAIN], "_frontend_registered"):
        await _register_frontend_resources(hass)
        hass.data[DOMAIN]["_frontend_registered"] = True
    
    # Écouter les changements d'options
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))
    
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    _LOGGER.info("Unloading Smart Appliance Monitor integration for '%s'", entry.data.get("appliance_name"))
    
    # Décharger les platforms
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    
    return unload_ok


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry when options change."""
    await hass.config_entries.async_reload(entry.entry_id)


async def _async_check_energy_sync(
    hass: HomeAssistant,
    coordinator: SmartApplianceCoordinator,
) -> None:
    """Check Energy Dashboard synchronization on startup.
    
    Args:
        hass: Home Assistant instance
        coordinator: Appliance coordinator
    """
    from .energy import EnergyDashboardSync
    
    try:
        sync_handler = EnergyDashboardSync(hass, coordinator)
        sync_status = await sync_handler.get_sync_status()
        
        status = sync_status.get("status")
        if status == "synced":
            _LOGGER.info(
                "✅ %s is synced with Energy Dashboard",
                coordinator.appliance_name
            )
        elif status == "not_configured":
            _LOGGER.warning(
                "⚠️ %s is NOT in Energy Dashboard. "
                "Use 'smart_appliance_monitor.sync_with_energy_dashboard' to get instructions.",
                coordinator.appliance_name
            )
        else:
            _LOGGER.debug(
                "Cannot check Energy Dashboard sync for %s: %s",
                coordinator.appliance_name,
                sync_status.get("message")
            )
    except Exception as err:
        _LOGGER.debug(
            "Energy Dashboard sync check failed for %s: %s",
            coordinator.appliance_name,
            err
        )


async def _register_frontend_resources(hass: HomeAssistant) -> None:
    """Register frontend resources for custom Lovelace cards."""
    # Get the path to the www directory (in integration folder)
    www_path = Path(__file__).parent / "www" / "smart-appliance-cards" / "dist"
    
    if not www_path.exists():
        _LOGGER.warning("Custom cards directory not found at %s", www_path)
        return
    
    # Register static path for cards - HACS compatible path
    await hass.http.async_register_static_paths(
        [
            StaticPathConfig(
                url_path="/hacsfiles/smart-appliance-cards",
                path=str(www_path),
                cache_headers=False,
            )
        ]
    )
    
    # Verify card files exist
    cards = [
        "smart-appliance-cycle-card.js",
        "smart-appliance-stats-card.js"
    ]
    
    for card in cards:
        card_path = www_path / card
        if card_path.exists():
            _LOGGER.info("Registered custom Lovelace card: %s", card)
        else:
            _LOGGER.warning("Card file not found: %s", card)


async def async_setup_services(hass: HomeAssistant) -> None:
    """Set up services for Smart Appliance Monitor."""
    
    async def handle_start_cycle(call: ServiceCall) -> None:
        """Handle start_cycle service call."""
        entity_id = call.data["entity_id"]
        
        # Find coordinator for entity
        coordinator = _get_coordinator_from_entity_id(hass, entity_id)
        if coordinator is None:
            _LOGGER.error("Unable to find coordinator for entity %s", entity_id)
            return
        
        _LOGGER.info("Manual cycle start for '%s'", coordinator.appliance_name)
        
        # Force state to RUNNING (for testing purposes only)
        from .const import STATE_RUNNING, EVENT_CYCLE_STARTED
        from datetime import datetime
        
        coordinator.state_machine.state = STATE_RUNNING
        coordinator.state_machine.current_cycle = {
            "start_time": datetime.now(),
            "start_energy": coordinator.data.get("energy", 0),
            "peak_power": coordinator.data.get("power", 0),
        }
        
        await coordinator._handle_event(EVENT_CYCLE_STARTED)
        await coordinator.async_request_refresh()
    
    async def handle_stop_monitoring(call: ServiceCall) -> None:
        """Handle stop_monitoring service call."""
        entity_id = call.data["entity_id"]
        
        coordinator = _get_coordinator_from_entity_id(hass, entity_id)
        if coordinator is None:
            _LOGGER.error("Unable to find coordinator for entity %s", entity_id)
            return
        
        _LOGGER.info("Stopping monitoring for '%s'", coordinator.appliance_name)
        coordinator.set_monitoring_enabled(False)
        await coordinator.async_request_refresh()
    
    async def handle_reset_statistics(call: ServiceCall) -> None:
        """Handle reset_statistics service call."""
        entity_id = call.data["entity_id"]
        
        coordinator = _get_coordinator_from_entity_id(hass, entity_id)
        if coordinator is None:
            _LOGGER.error("Unable to find coordinator for entity %s", entity_id)
            return
        
        _LOGGER.info("Resetting statistics for '%s'", coordinator.appliance_name)
        coordinator.reset_statistics()
        await coordinator.async_request_refresh()
    
    async def handle_generate_dashboard_yaml(call: ServiceCall) -> None:
        """Handle generate_dashboard_yaml service call."""
        entity_id = call.data["entity_id"]
        use_custom_cards = call.data.get("use_custom_cards", True)
        
        coordinator = _get_coordinator_from_entity_id(hass, entity_id)
        if coordinator is None:
            _LOGGER.error("Unable to find coordinator for entity %s", entity_id)
            return
        
        _LOGGER.info("Generating dashboard YAML for '%s'", coordinator.appliance_name)
        
        # Get appliance type
        appliance_type = coordinator.entry.data.get(CONF_APPLIANCE_TYPE, "other")
        appliance_name = coordinator.appliance_name
        
        # Map appliance type to template name
        template_map = {
            APPLIANCE_TYPE_WASHING_MACHINE: "washing_machine",
            APPLIANCE_TYPE_DISHWASHER: "dishwasher",
            APPLIANCE_TYPE_MONITOR: "monitor",
            APPLIANCE_TYPE_NAS: "nas",
            APPLIANCE_TYPE_PRINTER_3D: "printer_3d",
            APPLIANCE_TYPE_VMC: "vmc",
        }
        
        template_name = template_map.get(appliance_type, "generic")
        
        # Mapper au nom d'icône
        icon_map = {
            APPLIANCE_TYPE_WASHING_MACHINE: "mdi:washing-machine",
            APPLIANCE_TYPE_DISHWASHER: "mdi:dishwasher",
            APPLIANCE_TYPE_MONITOR: "mdi:monitor",
            APPLIANCE_TYPE_NAS: "mdi:nas",
            APPLIANCE_TYPE_PRINTER_3D: "mdi:printer-3d",
            APPLIANCE_TYPE_VMC: "mdi:fan",
            "oven": "mdi:stove",
            "dryer": "mdi:tumble-dryer",
            "water_heater": "mdi:water-boiler",
            "coffee_maker": "mdi:coffee-maker",
        }
        
        icon = icon_map.get(appliance_type, "mdi:power-plug")
        
        # Load template - check first in user custom templates
        # then fallback to integration bundled templates
        config_templates_path = Path(__file__).parent.parent.parent / "dashboards" / "templates"
        integration_templates_path = Path(__file__).parent / "dashboards"
        
        # Try user custom templates first
        template_file = config_templates_path / f"{template_name}.yaml"
        if not template_file.exists():
            # Fallback to integration bundled templates
            template_file = integration_templates_path / f"{template_name}.yaml"
        
        # If still not found, try generic
        if not template_file.exists():
            _LOGGER.warning(
                "Template %s not found in config or integration, trying generic",
                template_name
            )
            template_file = config_templates_path / "generic.yaml"
            if not template_file.exists():
                template_file = integration_templates_path / "generic.yaml"
        
        try:
            with open(template_file, "r", encoding="utf-8") as f:
                template_content = f.read()
        except Exception as e:
            _LOGGER.error("Error reading template: %s", e)
            await hass.services.async_call(
                "persistent_notification",
                "create",
                {
                    "title": "Dashboard Generation Error",
                    "message": f"Unable to read template: {e}",
                    "notification_id": f"dashboard_error_{coordinator.entry.entry_id}",
                },
            )
            return
        
        # Extract appliance_id from coordinator (last segment of entry_id)
        appliance_id = coordinator.entry.entry_id.split("_")[-1] if "_" in coordinator.entry.entry_id else appliance_name.lower().replace(" ", "_")
        
        # Replace placeholders
        dashboard_yaml = template_content.replace("{APPLIANCE_NAME}", appliance_name)
        dashboard_yaml = dashboard_yaml.replace("{APPLIANCE_ID}", appliance_id)
        dashboard_yaml = dashboard_yaml.replace("{ICON}", icon)
        
        # If use_custom_cards is False, we could remove custom cards
        # For now, we leave as is and inform the user
        
        # Create persistent notification with YAML
        notification_message = (
            f"Dashboard YAML generated for **{appliance_name}**\n\n"
            f"**Appliance Type**: {appliance_type}\n"
            f"**Template Used**: {template_name}.yaml\n"
            f"**Custom Cards**: {'Yes' if use_custom_cards else 'No'}\n\n"
            f"**Instructions**:\n"
            f"1. Copy the YAML below\n"
            f"2. Go to Settings → Dashboards → + Add Dashboard\n"
            f"3. Choose 'Start from scratch'\n"
            f"4. Add a view and paste the YAML in raw editor mode\n\n"
            f"**Dashboard YAML**:\n"
            f"```yaml\n{dashboard_yaml}\n```\n\n"
            f"The complete YAML is also in the logs (INFO level)."
        )
        
        # Send notification
        await hass.services.async_call(
            "persistent_notification",
            "create",
            {
                "title": f"📊 Dashboard {appliance_name}",
                "message": notification_message,
                "notification_id": f"dashboard_yaml_{coordinator.entry.entry_id}",
            },
        )
        
        # Log complete YAML
        _LOGGER.info(
            "Dashboard YAML generated for '%s' (type: %s, template: %s):\n%s",
            appliance_name,
            appliance_type,
            template_name,
            dashboard_yaml
        )
        
        _LOGGER.info(
            "Dashboard YAML for '%s' generated successfully. Check the notification or logs.",
            appliance_name
        )
    
    async def handle_export_to_csv(call: ServiceCall) -> None:
        """Handle export_to_csv service call."""
        entity_id = call.data["entity_id"]
        file_path = call.data.get("file_path")
        
        coordinator = _get_coordinator_from_entity_id(hass, entity_id)
        if coordinator is None:
            _LOGGER.error("Unable to find coordinator for entity %s", entity_id)
            return
        
        _LOGGER.info("Exporting data to CSV for '%s'", coordinator.appliance_name)
        
        from .export import SmartApplianceDataExporter
        exporter = SmartApplianceDataExporter(coordinator)
        csv_content = exporter.export_to_csv(file_path)
        
        # Send notification with export summary
        summary = exporter.get_export_summary()
        message = (
            f"Data exported to CSV for **{coordinator.appliance_name}**\n\n"
            f"**Export Summary**:\n"
            f"- Has current cycle: {summary['has_current_cycle']}\n"
            f"- Has last cycle: {summary['has_last_cycle']}\n"
            f"- Daily cycles: {summary['daily_cycles']}\n"
        )
        if file_path:
            message += f"\n**File saved to**: {file_path}"
        else:
            message += f"\n\nCSV content is in the logs."
        
        await hass.services.async_call(
            "persistent_notification",
            "create",
            {
                "title": f"📊 CSV Export - {coordinator.appliance_name}",
                "message": message,
                "notification_id": f"export_csv_{coordinator.entry.entry_id}",
            },
        )
        
        if not file_path:
            _LOGGER.info("CSV export for '%s':\n%s", coordinator.appliance_name, csv_content[:500])
    
    async def handle_export_to_json(call: ServiceCall) -> None:
        """Handle export_to_json service call."""
        entity_id = call.data["entity_id"]
        file_path = call.data.get("file_path")
        
        coordinator = _get_coordinator_from_entity_id(hass, entity_id)
        if coordinator is None:
            _LOGGER.error("Unable to find coordinator for entity %s", entity_id)
            return
        
        _LOGGER.info("Exporting data to JSON for '%s'", coordinator.appliance_name)
        
        from .export import SmartApplianceDataExporter
        exporter = SmartApplianceDataExporter(coordinator)
        json_content = exporter.export_to_json(file_path)
        
        # Send notification with export summary
        summary = exporter.get_export_summary()
        message = (
            f"Data exported to JSON for **{coordinator.appliance_name}**\n\n"
            f"**Export Summary**:\n"
            f"- Has current cycle: {summary['has_current_cycle']}\n"
            f"- Has last cycle: {summary['has_last_cycle']}\n"
            f"- Daily cycles: {summary['daily_cycles']}\n"
            f"- History size: {summary['history_size']}\n"
        )
        if file_path:
            message += f"\n**File saved to**: {file_path}"
        else:
            message += f"\n\nJSON content is in the logs."
        
        await hass.services.async_call(
            "persistent_notification",
            "create",
            {
                "title": f"📊 JSON Export - {coordinator.appliance_name}",
                "message": message,
                "notification_id": f"export_json_{coordinator.entry.entry_id}",
            },
        )
        
        if not file_path:
            _LOGGER.info("JSON export for '%s':\n%s", coordinator.appliance_name, json_content[:500])
    
    async def handle_force_shutdown(call: ServiceCall) -> None:
        """Handle force_shutdown service call."""
        entity_id = call.data["entity_id"]
        
        coordinator = _get_coordinator_from_entity_id(hass, entity_id)
        if coordinator is None:
            _LOGGER.error("Unable to find coordinator for entity %s", entity_id)
            return
        
        if not coordinator.auto_shutdown_enabled or not coordinator.auto_shutdown_entity:
            _LOGGER.warning(
                "Cannot force shutdown for '%s': auto-shutdown not enabled or entity not configured",
                coordinator.appliance_name
            )
            await hass.services.async_call(
                "persistent_notification",
                "create",
                {
                    "title": "Force Shutdown Failed",
                    "message": (
                        f"Cannot force shutdown for {coordinator.appliance_name}.\n"
                        "Auto-shutdown must be enabled and an entity must be configured."
                    ),
                    "notification_id": f"force_shutdown_error_{coordinator.entry.entry_id}",
                },
            )
            return
        
        _LOGGER.info("Force shutdown for '%s'", coordinator.appliance_name)
        await coordinator._on_auto_shutdown()
    
    async def handle_sync_with_energy_dashboard(call: ServiceCall) -> None:
        """Handle sync_with_energy_dashboard service call."""
        entity_id = call.data.get("entity_id")
        
        from .energy import EnergyDashboardSync
        from .energy_storage import EnergyStorageReader
        
        # If entity_id provided, sync specific appliance
        if entity_id:
            coordinator = _get_coordinator_from_entity_id(hass, entity_id)
            if coordinator is None:
                _LOGGER.error("Unable to find coordinator for entity %s", entity_id)
                return
            
            coordinators = [coordinator]
        else:
            # Sync all SAM appliances
            coordinators = [
                coord for coord in hass.data.get(DOMAIN, {}).values()
                if isinstance(coord, SmartApplianceCoordinator)
            ]
        
        _LOGGER.info("Syncing %d appliance(s) with Energy Dashboard", len(coordinators))
        
        # Generate sync report
        synced = []
        not_configured = []
        
        for coord in coordinators:
            sync_handler = EnergyDashboardSync(hass, coord)
            sync_status = await sync_handler.get_sync_status()
            
            if sync_status["status"] == "synced":
                synced.append(sync_status)
            elif sync_status["status"] == "not_configured":
                not_configured.append(sync_status)
        
        # Create notification with report
        message_lines = [
            f"**Energy Dashboard Sync Report**\n",
            f"**Total SAM devices**: {len(coordinators)}",
            f"**Synced**: {len(synced)}",
            f"**Not configured**: {len(not_configured)}\n",
        ]
        
        if synced:
            message_lines.append("**✅ Synced devices:**")
            for status in synced:
                message_lines.append(f"- {status['appliance_name']}")
            message_lines.append("")
        
        if not_configured:
            message_lines.append("**⚠️ Not in Energy Dashboard:**")
            for status in not_configured:
                message_lines.append(f"- {status['appliance_name']}")
                message_lines.append(f"  Sensor: `{status['energy_sensor']}`")
            message_lines.append("")
            message_lines.append(
                "**To add**: Go to Settings → Dashboards → Energy → Add Consumption"
            )
        
        await hass.services.async_call(
            "persistent_notification",
            "create",
            {
                "title": "🔄 Energy Dashboard Sync",
                "message": "\n".join(message_lines),
                "notification_id": "energy_dashboard_sync",
            },
        )
        
        _LOGGER.info("Energy Dashboard sync completed: %d synced, %d not configured", 
                     len(synced), len(not_configured))
    
    async def handle_export_energy_config(call: ServiceCall) -> None:
        """Handle export_energy_config service call."""
        entity_id = call.data["entity_id"]
        
        coordinator = _get_coordinator_from_entity_id(hass, entity_id)
        if coordinator is None:
            _LOGGER.error("Unable to find coordinator for entity %s", entity_id)
            return
        
        from .energy import EnergyDashboardSync
        import json
        
        sync_handler = EnergyDashboardSync(hass, coordinator)
        suggested_config = await sync_handler.suggest_energy_config()
        
        # Format as JSON for easy copy-paste
        json_config = json.dumps(suggested_config, indent=2, ensure_ascii=False)
        
        # Get current sync status
        sync_status = await sync_handler.get_sync_status()
        
        message = [
            f"**Energy Dashboard Configuration Export**\n",
            f"**Appliance**: {coordinator.appliance_name}",
            f"**Current Status**: {sync_status['status']}\n",
        ]
        
        if sync_status["status"] == "synced":
            message.append("✅ This appliance is already configured in Energy Dashboard.")
        else:
            message.append("**Configuration to add:**\n")
            message.append("```json")
            message.append(json_config)
            message.append("```\n")
            message.append("**Instructions:**")
            message.append("1. Go to Settings → Dashboards → Energy")
            message.append("2. Click 'Add Consumption'")
            message.append(f"3. Select sensor: `{suggested_config['stat_consumption']}`")
            message.append("4. Enter name (optional)")
            
            if "included_in_stat" in suggested_config:
                message.append(f"5. Check 'Include in parent' and select: `{suggested_config['included_in_stat']}`")
            
            message.append("6. Save")
        
        await hass.services.async_call(
            "persistent_notification",
            "create",
            {
                "title": f"📤 Energy Config - {coordinator.appliance_name}",
                "message": "\n".join(message),
                "notification_id": f"energy_config_export_{coordinator.entry.entry_id}",
            },
        )
        
        _LOGGER.info(
            "Energy config exported for '%s': %s",
            coordinator.appliance_name,
            json_config
        )
    
    async def handle_get_energy_data(call: ServiceCall) -> None:
        """Handle get_energy_data service call."""
        from datetime import datetime, timedelta
        from .energy_storage import EnergyStorageReader
        
        # Parse parameters
        period_start = call.data.get("period_start")
        period_end = call.data.get("period_end")
        devices = call.data.get("devices", [])
        
        # Default to today if not specified
        if not period_start:
            period_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        else:
            period_start = datetime.fromisoformat(period_start)
        
        if not period_end:
            period_end = datetime.now()
        else:
            period_end = datetime.fromisoformat(period_end)
        
        # Get all SAM coordinators or filter by devices
        coordinators = [
            coord for coord in hass.data.get(DOMAIN, {}).values()
            if isinstance(coord, SmartApplianceCoordinator)
        ]
        
        if devices:
            coordinators = [
                coord for coord in coordinators
                if coord.appliance_name in devices
            ]
        
        # Collect energy data
        energy_data = {
            "period": {
                "start": period_start.isoformat(),
                "end": period_end.isoformat(),
            },
            "devices": [],
            "total_energy_kwh": 0.0,
            "total_cost": 0.0,
        }
        
        for coord in coordinators:
            device_data = {
                "name": coord.appliance_name,
                "type": coord.appliance_type,
                "daily_energy_kwh": round(coord.daily_stats.get("total_energy", 0), 3),
                "daily_cost": round(coord.daily_stats.get("total_cost", 0), 2),
                "monthly_energy_kwh": round(coord.monthly_stats.get("total_energy", 0), 3),
                "monthly_cost": round(coord.monthly_stats.get("total_cost", 0), 2),
            }
            
            energy_data["devices"].append(device_data)
            energy_data["total_energy_kwh"] += device_data["daily_energy_kwh"]
            energy_data["total_cost"] += device_data["daily_cost"]
        
        # Round totals
        energy_data["total_energy_kwh"] = round(energy_data["total_energy_kwh"], 3)
        energy_data["total_cost"] = round(energy_data["total_cost"], 2)
        
        # Fire event with data (for custom cards to listen)
        hass.bus.async_fire(
            f"{DOMAIN}_energy_data",
            energy_data
        )
        
        _LOGGER.info(
            "Energy data retrieved for %d devices: %.3f kWh, %.2f €",
            len(coordinators),
            energy_data["total_energy_kwh"],
            energy_data["total_cost"]
        )
        
        # Also create a notification
        message = [
            f"**Energy Data Report**\n",
            f"**Period**: {period_start.strftime('%Y-%m-%d %H:%M')} → {period_end.strftime('%Y-%m-%d %H:%M')}",
            f"**Devices**: {len(coordinators)}",
            f"**Total Energy**: {energy_data['total_energy_kwh']} kWh",
            f"**Total Cost**: {energy_data['total_cost']} €\n",
            "**Breakdown:**",
        ]
        
        for device in energy_data["devices"]:
            message.append(f"- **{device['name']}**: {device['daily_energy_kwh']} kWh (€{device['daily_cost']})")
        
        await hass.services.async_call(
            "persistent_notification",
            "create",
            {
                "title": "⚡ Energy Data",
                "message": "\n".join(message),
                "notification_id": "energy_data_report",
            },
        )
    
    async def handle_analyze_cycles(call: ServiceCall) -> None:
        """Handle analyze_cycles service call."""
        entity_id = call.data["entity_id"]
        analysis_type = call.data.get("analysis_type", "all")
        cycle_count = call.data.get("cycle_count", 10)
        export_format = call.data.get("export_format", "json")
        save_export = call.data.get("save_export", False)
        
        coordinator = _get_coordinator_from_entity_id(hass, entity_id)
        if coordinator is None:
            _LOGGER.error("Unable to find coordinator for entity %s", entity_id)
            return
        
        _LOGGER.info(
            "Starting AI analysis for '%s' (type: %s, cycles: %d)",
            coordinator.appliance_name,
            analysis_type,
            cycle_count,
        )
        
        # Export data if requested
        if save_export:
            from .export import SmartApplianceDataExporter
            exporter = SmartApplianceDataExporter(coordinator)
            
            if export_format in ("json", "both"):
                json_path = f"/config/sam_export_{coordinator.appliance_name}_cycles.json"
                exporter.export_to_json(file_path=json_path)
                _LOGGER.info("Exported data to JSON: %s", json_path)
            
            if export_format in ("csv", "both"):
                csv_path = f"/config/sam_export_{coordinator.appliance_name}_cycles.csv"
                csv_content = exporter.export_cycles_history_csv(cycle_count=cycle_count)
                from pathlib import Path
                Path(csv_path).write_text(csv_content, encoding="utf-8")
                _LOGGER.info("Exported data to CSV: %s", csv_path)
        
        # Trigger AI analysis
        result = await coordinator.async_trigger_ai_analysis(
            analysis_type=analysis_type,
            cycle_count=cycle_count,
        )
        
        if result:
            _LOGGER.info(
                "AI analysis completed for '%s': status=%s",
                coordinator.appliance_name,
                result.get("status"),
            )
            
            # Send notification if enabled
            if coordinator.notifications_enabled:
                await coordinator.notifier.notify_ai_analysis(result)
        else:
            _LOGGER.error("AI analysis failed for '%s'", coordinator.appliance_name)
    
    async def handle_analyze_energy_dashboard(call: ServiceCall) -> None:
        """Handle analyze_energy_dashboard service call."""
        period = call.data.get("period", "today")
        compare_previous = call.data.get("compare_previous", False)
        include_recommendations = call.data.get("include_recommendations", True)
        
        _LOGGER.info(
            "Starting Energy Dashboard AI analysis (period: %s, compare: %s)",
            period,
            compare_previous,
        )
        
        # Get global config and AI Task entity
        global_config = hass.data.get(DOMAIN, {}).get("global_config")
        if not global_config:
            _LOGGER.error("No global configuration found for AI analysis")
            return
        
        ai_task_entity = global_config.get_sync("ai_task_entity")
        if not ai_task_entity:
            _LOGGER.error("No AI Task entity configured")
            return
        
        try:
            from .energy_dashboard import CustomEnergyDashboard
            from .ai_client import SmartApplianceAIClient
            
            # Get dashboard data
            dashboard = CustomEnergyDashboard(hass)
            export_data = await dashboard.export_for_ai_analysis(
                period=period,
                compare_previous=compare_previous,
            )
            
            # Analyze with AI
            ai_client = SmartApplianceAIClient(hass, ai_task_entity)
            result = await ai_client.async_analyze_energy_dashboard(
                dashboard_data=export_data,
                period=period,
                compare_previous=compare_previous,
            )
            
            _LOGGER.info(
                "Energy Dashboard AI analysis completed: score=%d",
                result.get("efficiency_score", 0),
            )
            
            # Update the global sensor if it exists
            sensor_entity_id = f"sensor.{DOMAIN}_energy_dashboard_ai_analysis"
            if sensor_entity_id in hass.states.async_entity_ids():
                # Get the sensor and update it
                # Note: This requires the sensor to be set up globally
                _LOGGER.info("Energy Dashboard analysis result: %s", result)
            
            # Fire event with result
            hass.bus.fire(
                f"{DOMAIN}_energy_dashboard_analysis_completed",
                {
                    "period": period,
                    "efficiency_score": result.get("efficiency_score", 0),
                    "consumption_trend": result.get("consumption_trend", "unknown"),
                },
            )
            
        except Exception as err:
            _LOGGER.error("Energy Dashboard AI analysis failed: %s", err)
    
    async def handle_configure_ai(call: ServiceCall) -> None:
        """Handle configure_ai service call to set global AI configuration."""
        ai_task_entity = call.data.get("ai_task_entity")
        global_price_entity = call.data.get("global_price_entity")
        enable_ai_analysis = call.data.get("enable_ai_analysis")
        ai_analysis_trigger = call.data.get("ai_analysis_trigger")
        
        # Get global config
        global_config = hass.data.get(DOMAIN, {}).get("global_config")
        if not global_config:
            _LOGGER.error("Global configuration manager not found")
            return
        
        # Update configuration
        updates = {}
        if ai_task_entity is not None:
            updates["ai_task_entity"] = ai_task_entity
        if global_price_entity is not None:
            updates["global_price_entity"] = global_price_entity
        if enable_ai_analysis is not None:
            updates["enable_ai_analysis"] = enable_ai_analysis
        if ai_analysis_trigger is not None:
            updates["ai_analysis_trigger"] = ai_analysis_trigger
        
        if updates:
            await global_config.async_update(updates)
            _LOGGER.info("Global AI configuration updated: %s", updates)
            
            # Reload config for all coordinators
            for entry_id, coordinator in hass.data.get(DOMAIN, {}).items():
                if isinstance(coordinator, SmartApplianceCoordinator):
                    await coordinator.load_global_ai_config()
                    _LOGGER.debug("Reloaded AI config for '%s'", coordinator.appliance_name)
            
            # Send confirmation notification
            await hass.services.async_call(
                "persistent_notification",
                "create",
                {
                    "title": "✅ AI Configuration Updated",
                    "message": f"Global AI analysis configuration has been updated.\n\n{updates}",
                    "notification_id": "sam_ai_config_updated",
                },
            )
        else:
            _LOGGER.warning("No configuration changes provided")
    
    # Register services
    hass.services.async_register(
        DOMAIN,
        "start_cycle",
        handle_start_cycle,
        schema=SERVICE_START_CYCLE_SCHEMA,
    )
    
    hass.services.async_register(
        DOMAIN,
        "stop_monitoring",
        handle_stop_monitoring,
        schema=SERVICE_STOP_MONITORING_SCHEMA,
    )
    
    hass.services.async_register(
        DOMAIN,
        "reset_statistics",
        handle_reset_statistics,
        schema=SERVICE_RESET_STATISTICS_SCHEMA,
    )
    
    hass.services.async_register(
        DOMAIN,
        "generate_dashboard_yaml",
        handle_generate_dashboard_yaml,
        schema=SERVICE_GENERATE_DASHBOARD_YAML_SCHEMA,
    )
    
    hass.services.async_register(
        DOMAIN,
        "export_to_csv",
        handle_export_to_csv,
        schema=SERVICE_EXPORT_TO_CSV_SCHEMA,
    )
    
    hass.services.async_register(
        DOMAIN,
        "export_to_json",
        handle_export_to_json,
        schema=SERVICE_EXPORT_TO_JSON_SCHEMA,
    )
    
    hass.services.async_register(
        DOMAIN,
        "force_shutdown",
        handle_force_shutdown,
        schema=SERVICE_FORCE_SHUTDOWN_SCHEMA,
    )
    
    hass.services.async_register(
        DOMAIN,
        "sync_with_energy_dashboard",
        handle_sync_with_energy_dashboard,
        schema=SERVICE_SYNC_WITH_ENERGY_DASHBOARD_SCHEMA,
    )
    
    hass.services.async_register(
        DOMAIN,
        "export_energy_config",
        handle_export_energy_config,
        schema=SERVICE_EXPORT_ENERGY_CONFIG_SCHEMA,
    )
    
    hass.services.async_register(
        DOMAIN,
        "get_energy_data",
        handle_get_energy_data,
        schema=SERVICE_GET_ENERGY_DATA_SCHEMA,
    )
    
    hass.services.async_register(
        DOMAIN,
        "analyze_cycles",
        handle_analyze_cycles,
        schema=SERVICE_ANALYZE_CYCLES_SCHEMA,
    )
    
    hass.services.async_register(
        DOMAIN,
        "analyze_energy_dashboard",
        handle_analyze_energy_dashboard,
        schema=SERVICE_ANALYZE_ENERGY_DASHBOARD_SCHEMA,
    )
    
    hass.services.async_register(
        DOMAIN,
        "configure_ai",
        handle_configure_ai,
        schema=SERVICE_CONFIGURE_AI_SCHEMA,
    )
    
    _LOGGER.info("Services Smart Appliance Monitor enregistrés")


def _get_coordinator_from_entity_id(hass: HomeAssistant, entity_id: str) -> SmartApplianceCoordinator | None:
    """Get coordinator from entity_id."""
    # Extraire le nom de l'appareil de l'entity_id
    # Format: sensor.{appliance_name}_{type} ou domain.{appliance_name}_{type}
    parts = entity_id.split(".", 1)
    if len(parts) != 2:
        return None
    
    # Essayer de trouver le coordinator correspondant
    for entry_id, coordinator in hass.data.get(DOMAIN, {}).items():
        if isinstance(coordinator, SmartApplianceCoordinator):
            # Vérifier si l'entity_id correspond à cet appareil
            # On vérifie avec le nom de l'appareil (en minuscules et sans espaces)
            appliance_slug = coordinator.appliance_name.lower().replace(" ", "_")
            if parts[1].startswith(appliance_slug):
                return coordinator
            
            # Fallback: vérifier si l'entry_id est dans l'entity_id (ancien comportement)
            if entry_id in entity_id or coordinator.entry.entry_id in entity_id:
                return coordinator
    
    return None

