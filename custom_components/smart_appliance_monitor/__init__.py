"""The Smart Appliance Monitor integration."""
from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.BINARY_SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Smart Appliance Monitor from a config entry."""
    _LOGGER.debug("Setting up Smart Appliance Monitor integration")
    
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {}
    
    # TODO: Implémenter le coordinator
    # coordinator = SmartApplianceCoordinator(hass, entry)
    # await coordinator.async_config_entry_first_refresh()
    # hass.data[DOMAIN][entry.entry_id] = coordinator
    
    # await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    _LOGGER.debug("Unloading Smart Appliance Monitor integration")
    
    # TODO: Implémenter le unload
    # unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    
    # if unload_ok:
    #     hass.data[DOMAIN].pop(entry.entry_id)
    
    # return unload_ok
    
    hass.data[DOMAIN].pop(entry.entry_id)
    return True

