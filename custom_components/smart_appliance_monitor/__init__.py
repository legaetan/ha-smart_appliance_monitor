"""The Smart Appliance Monitor integration."""
from __future__ import annotations

import logging
from pathlib import Path

import voluptuous as vol

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


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Smart Appliance Monitor from a config entry."""
    _LOGGER.info("Setting up Smart Appliance Monitor integration for '%s'", entry.data.get("appliance_name"))
    
    hass.data.setdefault(DOMAIN, {})
    
    # Créer le coordinator
    coordinator = SmartApplianceCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()
    
    # Stocker le coordinator
    hass.data[DOMAIN][entry.entry_id] = coordinator
    
    # Charger les platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    # Enregistrer les services (une seule fois)
    if not hass.services.has_service(DOMAIN, "start_cycle"):
        await async_setup_services(hass)
    
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
        
        # Load template
        templates_path = Path(__file__).parent.parent.parent / "dashboards" / "templates"
        template_file = templates_path / f"{template_name}.yaml"
        
        if not template_file.exists():
            _LOGGER.warning(
                "Template %s not found, using generic template",
                template_name
            )
            template_file = templates_path / "generic.yaml"
        
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

