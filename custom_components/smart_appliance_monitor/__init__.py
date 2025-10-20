"""The Smart Appliance Monitor integration."""
from __future__ import annotations

import logging

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv

from .const import DOMAIN
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
        
        # Trouver le coordinator correspondant à l'entité
        coordinator = _get_coordinator_from_entity_id(hass, entity_id)
        if coordinator is None:
            _LOGGER.error("Impossible de trouver le coordinator pour l'entité %s", entity_id)
            return
        
        _LOGGER.info("Démarrage manuel d'un cycle pour '%s'", coordinator.appliance_name)
        
        # Force l'état à RUNNING (à utiliser uniquement pour les tests)
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
            _LOGGER.error("Impossible de trouver le coordinator pour l'entité %s", entity_id)
            return
        
        _LOGGER.info("Arrêt de la surveillance pour '%s'", coordinator.appliance_name)
        coordinator.set_monitoring_enabled(False)
        await coordinator.async_request_refresh()
    
    async def handle_reset_statistics(call: ServiceCall) -> None:
        """Handle reset_statistics service call."""
        entity_id = call.data["entity_id"]
        
        coordinator = _get_coordinator_from_entity_id(hass, entity_id)
        if coordinator is None:
            _LOGGER.error("Impossible de trouver le coordinator pour l'entité %s", entity_id)
            return
        
        _LOGGER.info("Réinitialisation des statistiques pour '%s'", coordinator.appliance_name)
        coordinator.reset_statistics()
        await coordinator.async_request_refresh()
    
    # Enregistrer les services
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
    
    _LOGGER.info("Services Smart Appliance Monitor enregistrés")


def _get_coordinator_from_entity_id(hass: HomeAssistant, entity_id: str) -> SmartApplianceCoordinator | None:
    """Get coordinator from entity_id."""
    # Extraire l'entry_id de l'entity_id (format: sensor.{entry_id}_{type})
    for entry_id, coordinator in hass.data.get(DOMAIN, {}).items():
        if isinstance(coordinator, SmartApplianceCoordinator):
            if entry_id in entity_id or coordinator.entry.entry_id in entity_id:
                return coordinator
    
    return None

