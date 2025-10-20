"""Switches pour Smart Appliance Monitor."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    DOMAIN,
    NOTIF_TYPE_CYCLE_STARTED,
    NOTIF_TYPE_CYCLE_FINISHED,
    NOTIF_TYPE_ALERT_DURATION,
    NOTIF_TYPE_UNPLUGGED,
)
from .coordinator import SmartApplianceCoordinator
from .entity import SmartApplianceEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Smart Appliance Monitor switches."""
    coordinator: SmartApplianceCoordinator = hass.data[DOMAIN][entry.entry_id]
    
    entities = [
        SmartApplianceMonitoringSwitch(coordinator),
        SmartApplianceNotificationsSwitch(coordinator),
        SmartApplianceNotificationCycleStartedSwitch(coordinator),
        SmartApplianceNotificationCycleFinishedSwitch(coordinator),
        SmartApplianceNotificationAlertDurationSwitch(coordinator),
        SmartApplianceNotificationUnpluggedSwitch(coordinator),
    ]
    
    async_add_entities(entities)
    _LOGGER.info(
        "Switches créés pour '%s' (%d entités)",
        coordinator.appliance_name,
        len(entities),
    )


class SmartApplianceMonitoringSwitch(SmartApplianceEntity, SwitchEntity):
    """Switch pour activer/désactiver la surveillance."""

    _attr_translation_key = "monitoring"

    def __init__(self, coordinator: SmartApplianceCoordinator) -> None:
        """Initialize the switch."""
        super().__init__(coordinator, "monitoring")
        self._attr_name = "Surveillance"
    
    @property
    def icon(self) -> str:
        """Return the icon to use in the frontend."""
        return "mdi:monitor-eye" if self.is_on else "mdi:monitor-off"
    
    @property
    def is_on(self) -> bool:
        """Return True if monitoring is enabled."""
        return self.coordinator.monitoring_enabled
    
    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on monitoring."""
        _LOGGER.info(
            "Activation de la surveillance pour '%s'",
            self.coordinator.appliance_name,
        )
        self.coordinator.set_monitoring_enabled(True)
        await self.coordinator.async_request_refresh()
        self.async_write_ha_state()
    
    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off monitoring."""
        _LOGGER.info(
            "Désactivation de la surveillance pour '%s'",
            self.coordinator.appliance_name,
        )
        self.coordinator.set_monitoring_enabled(False)
        await self.coordinator.async_request_refresh()
        self.async_write_ha_state()
    
    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional state attributes."""
        return {
            "state": self.coordinator.data.get("state"),
        }


class SmartApplianceNotificationsSwitch(SmartApplianceEntity, SwitchEntity):
    """Switch pour activer/désactiver les notifications."""

    _attr_translation_key = "notifications"

    def __init__(self, coordinator: SmartApplianceCoordinator) -> None:
        """Initialize the switch."""
        super().__init__(coordinator, "notifications")
        self._attr_name = "Notifications"
    
    @property
    def icon(self) -> str:
        """Return the icon to use in the frontend."""
        return "mdi:bell-ring" if self.is_on else "mdi:bell-off"
    
    @property
    def is_on(self) -> bool:
        """Return True if notifications are enabled."""
        return self.coordinator.notifications_enabled
    
    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on notifications."""
        _LOGGER.info(
            "Activation des notifications pour '%s'",
            self.coordinator.appliance_name,
        )
        self.coordinator.set_notifications_enabled(True)
        await self.coordinator.async_request_refresh()
        self.async_write_ha_state()
    
    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off notifications."""
        _LOGGER.info(
            "Désactivation des notifications pour '%s'",
            self.coordinator.appliance_name,
        )
        self.coordinator.set_notifications_enabled(False)
        await self.coordinator.async_request_refresh()
        self.async_write_ha_state()


class SmartApplianceNotificationCycleStartedSwitch(SmartApplianceEntity, SwitchEntity):
    """Switch pour activer/désactiver les notifications de démarrage de cycle."""

    _attr_translation_key = "notification_cycle_started"

    def __init__(self, coordinator: SmartApplianceCoordinator) -> None:
        """Initialize the switch."""
        super().__init__(coordinator, "notification_cycle_started")
        self._attr_name = "Notification cycle démarré"
        self._attr_entity_registry_enabled_default = True
    
    @property
    def icon(self) -> str:
        """Return the icon to use in the frontend."""
        return "mdi:play-circle" if self.is_on else "mdi:play-circle-outline"
    
    @property
    def is_on(self) -> bool:
        """Return True if notification type is enabled."""
        return self.coordinator.notifier.notification_type_switches.get(NOTIF_TYPE_CYCLE_STARTED, True)
    
    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on notification type."""
        self.coordinator.notifier.set_notification_type_enabled(NOTIF_TYPE_CYCLE_STARTED, True)
        self.async_write_ha_state()
    
    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off notification type."""
        self.coordinator.notifier.set_notification_type_enabled(NOTIF_TYPE_CYCLE_STARTED, False)
        self.async_write_ha_state()


class SmartApplianceNotificationCycleFinishedSwitch(SmartApplianceEntity, SwitchEntity):
    """Switch pour activer/désactiver les notifications de fin de cycle."""

    _attr_translation_key = "notification_cycle_finished"

    def __init__(self, coordinator: SmartApplianceCoordinator) -> None:
        """Initialize the switch."""
        super().__init__(coordinator, "notification_cycle_finished")
        self._attr_name = "Notification cycle terminé"
        self._attr_entity_registry_enabled_default = True
    
    @property
    def icon(self) -> str:
        """Return the icon to use in the frontend."""
        return "mdi:check-circle" if self.is_on else "mdi:check-circle-outline"
    
    @property
    def is_on(self) -> bool:
        """Return True if notification type is enabled."""
        return self.coordinator.notifier.notification_type_switches.get(NOTIF_TYPE_CYCLE_FINISHED, True)
    
    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on notification type."""
        self.coordinator.notifier.set_notification_type_enabled(NOTIF_TYPE_CYCLE_FINISHED, True)
        self.async_write_ha_state()
    
    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off notification type."""
        self.coordinator.notifier.set_notification_type_enabled(NOTIF_TYPE_CYCLE_FINISHED, False)
        self.async_write_ha_state()


class SmartApplianceNotificationAlertDurationSwitch(SmartApplianceEntity, SwitchEntity):
    """Switch pour activer/désactiver les notifications d'alerte de durée."""

    _attr_translation_key = "notification_alert_duration"

    def __init__(self, coordinator: SmartApplianceCoordinator) -> None:
        """Initialize the switch."""
        super().__init__(coordinator, "notification_alert_duration")
        self._attr_name = "Notification alerte durée"
        self._attr_entity_registry_enabled_default = True
    
    @property
    def icon(self) -> str:
        """Return the icon to use in the frontend."""
        return "mdi:timer-alert" if self.is_on else "mdi:timer-alert-outline"
    
    @property
    def is_on(self) -> bool:
        """Return True if notification type is enabled."""
        return self.coordinator.notifier.notification_type_switches.get(NOTIF_TYPE_ALERT_DURATION, True)
    
    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on notification type."""
        self.coordinator.notifier.set_notification_type_enabled(NOTIF_TYPE_ALERT_DURATION, True)
        self.async_write_ha_state()
    
    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off notification type."""
        self.coordinator.notifier.set_notification_type_enabled(NOTIF_TYPE_ALERT_DURATION, False)
        self.async_write_ha_state()


class SmartApplianceNotificationUnpluggedSwitch(SmartApplianceEntity, SwitchEntity):
    """Switch pour activer/désactiver les notifications de débranché."""

    _attr_translation_key = "notification_unplugged"

    def __init__(self, coordinator: SmartApplianceCoordinator) -> None:
        """Initialize the switch."""
        super().__init__(coordinator, "notification_unplugged")
        self._attr_name = "Notification débranché"
        self._attr_entity_registry_enabled_default = True
    
    @property
    def icon(self) -> str:
        """Return the icon to use in the frontend."""
        return "mdi:power-plug-off" if self.is_on else "mdi:power-plug-off-outline"
    
    @property
    def is_on(self) -> bool:
        """Return True if notification type is enabled."""
        return self.coordinator.notifier.notification_type_switches.get(NOTIF_TYPE_UNPLUGGED, True)
    
    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on notification type."""
        self.coordinator.notifier.set_notification_type_enabled(NOTIF_TYPE_UNPLUGGED, True)
        self.async_write_ha_state()
    
    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off notification type."""
        self.coordinator.notifier.set_notification_type_enabled(NOTIF_TYPE_UNPLUGGED, False)
        self.async_write_ha_state()

