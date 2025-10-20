"""Binary sensors pour Smart Appliance Monitor."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, STATE_RUNNING, CONF_ENABLE_ALERT_DURATION
from .coordinator import SmartApplianceCoordinator
from .entity import SmartApplianceEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Smart Appliance Monitor binary sensors."""
    coordinator: SmartApplianceCoordinator = hass.data[DOMAIN][entry.entry_id]
    
    entities = [
        SmartApplianceRunningBinarySensor(coordinator),
        SmartApplianceUnpluggedBinarySensor(coordinator),
    ]
    
    # Ajouter le binary sensor d'alerte seulement si activé
    if entry.options.get(CONF_ENABLE_ALERT_DURATION, False):
        entities.append(SmartApplianceAlertDurationBinarySensor(coordinator))
    
    async_add_entities(entities)
    _LOGGER.info(
        "Binary sensors créés pour '%s' (%d entités)",
        coordinator.appliance_name,
        len(entities),
    )


class SmartApplianceRunningBinarySensor(SmartApplianceEntity, BinarySensorEntity):
    """Binary sensor indiquant si l'appareil est en marche."""

    _attr_device_class = BinarySensorDeviceClass.RUNNING
    _attr_translation_key = "running"

    def __init__(self, coordinator: SmartApplianceCoordinator) -> None:
        """Initialize the binary sensor."""
        super().__init__(coordinator, "running")
        self._attr_name = "En marche"
    
    @property
    def is_on(self) -> bool:
        """Return True if the appliance is running."""
        return self.coordinator.data.get("state") == STATE_RUNNING
    
    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional state attributes."""
        attributes = {}
        
        if self.is_on and self.coordinator.data.get("current_cycle"):
            cycle = self.coordinator.data["current_cycle"]
            attributes["start_time"] = cycle.get("start_time")
            attributes["peak_power"] = cycle.get("peak_power")
        
        return attributes


class SmartApplianceAlertDurationBinarySensor(SmartApplianceEntity, BinarySensorEntity):
    """Binary sensor pour l'alerte de durée excessive."""

    _attr_device_class = BinarySensorDeviceClass.PROBLEM
    _attr_translation_key = "alert_duration"

    def __init__(self, coordinator: SmartApplianceCoordinator) -> None:
        """Initialize the binary sensor."""
        super().__init__(coordinator, "alert_duration")
        self._attr_name = "Alerte durée"
        self._alert_triggered = False
        
        # Écouter les événements d'alerte
        self.coordinator.hass.bus.async_listen(
            f"{DOMAIN}_alert_duration",
            self._handle_alert_event,
        )
    
    async def _handle_alert_event(self, event) -> None:
        """Handle alert duration event."""
        if event.data.get("entry_id") == self.coordinator.entry.entry_id:
            self._alert_triggered = True
            self.async_write_ha_state()
    
    @property
    def is_on(self) -> bool:
        """Return True if alert is triggered."""
        # Réinitialiser l'alerte si le cycle est terminé
        if self.coordinator.data.get("state") != STATE_RUNNING:
            self._alert_triggered = False
        
        return self._alert_triggered
    
    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional state attributes."""
        attributes = {}
        
        if self.is_on and self.coordinator.data.get("current_cycle"):
            from datetime import datetime
            cycle = self.coordinator.data["current_cycle"]
            start_time = cycle.get("start_time")
            if start_time:
                duration = (datetime.now() - start_time).total_seconds() / 60
                attributes["duration_minutes"] = round(duration, 1)
                attributes["alert_threshold"] = self.coordinator.state_machine.alert_duration / 60
        
        return attributes


class SmartApplianceUnpluggedBinarySensor(SmartApplianceEntity, BinarySensorEntity):
    """Binary sensor pour détecter si l'appareil est débranché."""

    _attr_device_class = BinarySensorDeviceClass.PROBLEM
    _attr_translation_key = "unplugged"

    def __init__(self, coordinator: SmartApplianceCoordinator) -> None:
        """Initialize the binary sensor."""
        super().__init__(coordinator, "unplugged")
        self._attr_name = "Débranché"
    
    @property
    def is_on(self) -> bool:
        """Return True if the appliance is detected as unplugged."""
        return self.coordinator.state_machine.is_unplugged()
    
    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional state attributes."""
        from datetime import datetime
        
        time_at_zero = self.coordinator.state_machine.get_time_at_zero_power(datetime.now())
        unplugged_timeout = self.coordinator.state_machine.unplugged_timeout
        
        return {
            "time_at_zero_power": round(time_at_zero, 1),
            "unplugged_timeout": unplugged_timeout,
            "detection_progress": min(100, round((time_at_zero / unplugged_timeout) * 100, 1)),
        }

