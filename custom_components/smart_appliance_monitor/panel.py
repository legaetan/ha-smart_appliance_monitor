"""Panel configuration for Smart Appliance Monitor dashboard management."""
from __future__ import annotations

import logging

from homeassistant.components import frontend
from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)

PANEL_URL = "smart-appliances-config"
PANEL_TITLE = "Smart Appliances Config"
PANEL_ICON = "mdi:cog-sync"


async def async_register_panel(hass: HomeAssistant) -> None:
    """Register the Smart Appliances configuration panel."""
    try:
        # Register the panel as an iframe
        await frontend.async_register_built_in_panel(
            hass,
            "iframe",
            PANEL_TITLE,
            PANEL_ICON,
            PANEL_URL,
            {"url": "/smart_appliance_monitor_frontend/sam-config-panel.html"},
            require_admin=True,
        )

        _LOGGER.info("Smart Appliances configuration panel registered at /%s", PANEL_URL)

    except Exception as err:
        _LOGGER.error("Error registering configuration panel: %s", err)
        raise


async def async_unregister_panel(hass: HomeAssistant) -> None:
    """Unregister the Smart Appliances configuration panel."""
    try:
        await hass.components.frontend.async_remove_panel(PANEL_URL)
        _LOGGER.info("Smart Appliances configuration panel unregistered")
    except Exception as err:
        _LOGGER.error("Error unregistering configuration panel: %s", err)


