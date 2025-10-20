"""Buttons pour Smart Appliance Monitor."""
from __future__ import annotations

import logging

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import SmartApplianceCoordinator
from .entity import SmartApplianceEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Smart Appliance Monitor buttons."""
    coordinator: SmartApplianceCoordinator = hass.data[DOMAIN][entry.entry_id]
    
    entities = [
        SmartApplianceResetStatsButton(coordinator),
    ]
    
    async_add_entities(entities)
    _LOGGER.info(
        "Buttons créés pour '%s' (%d entités)",
        coordinator.appliance_name,
        len(entities),
    )


class SmartApplianceResetStatsButton(SmartApplianceEntity, ButtonEntity):
    """Bouton pour réinitialiser les statistiques."""

    _attr_translation_key = "reset_stats"

    def __init__(self, coordinator: SmartApplianceCoordinator) -> None:
        """Initialize the button."""
        super().__init__(coordinator, "reset_stats")
        self._attr_name = "Réinitialiser les statistiques"
    
    @property
    def icon(self) -> str:
        """Return the icon to use in the frontend."""
        return "mdi:refresh"
    
    async def async_press(self) -> None:
        """Handle the button press."""
        _LOGGER.info(
            "Réinitialisation des statistiques pour '%s'",
            self.coordinator.appliance_name,
        )
        
        # Réinitialiser les statistiques via le coordinator
        self.coordinator.reset_statistics()
        
        # Forcer une mise à jour des entités
        await self.coordinator.async_request_refresh()
        
        # Émettre un événement
        self.hass.bus.async_fire(
            f"{DOMAIN}_stats_reset",
            {
                "appliance_name": self.coordinator.appliance_name,
                "entry_id": self.coordinator.entry.entry_id,
            },
        )

