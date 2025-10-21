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
        SmartApplianceAutoShutdownSwitch(coordinator),
        SmartApplianceEnergyLimitsSwitch(coordinator),
        SmartApplianceSchedulingSwitch(coordinator),
        SmartApplianceAIAnalysisSwitch(coordinator),
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


class SmartApplianceAutoShutdownSwitch(SmartApplianceEntity, SwitchEntity):
    """Switch pour activer/désactiver l'extinction automatique."""

    _attr_translation_key = "auto_shutdown"

    def __init__(self, coordinator: SmartApplianceCoordinator) -> None:
        """Initialize the switch."""
        super().__init__(coordinator, "auto_shutdown")
        self._attr_name = "Extinction automatique"
        self._attr_entity_registry_enabled_default = False
    
    @property
    def icon(self) -> str:
        """Return the icon to use in the frontend."""
        return "mdi:power-sleep" if self.is_on else "mdi:power-off"
    
    @property
    def is_on(self) -> bool:
        """Return True if auto-shutdown is enabled."""
        return self.coordinator.auto_shutdown_enabled
    
    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on auto-shutdown."""
        _LOGGER.info(
            "Activation de l'extinction automatique pour '%s'",
            self.coordinator.appliance_name,
        )
        self.coordinator.set_auto_shutdown_enabled(True)
        await self.coordinator.async_request_refresh()
        self.async_write_ha_state()
    
    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off auto-shutdown."""
        _LOGGER.info(
            "Désactivation de l'extinction automatique pour '%s'",
            self.coordinator.appliance_name,
        )
        self.coordinator.set_auto_shutdown_enabled(False)
        await self.coordinator.async_request_refresh()
        self.async_write_ha_state()


class SmartApplianceEnergyLimitsSwitch(SmartApplianceEntity, SwitchEntity):
    """Switch pour activer/désactiver les limites énergétiques."""

    _attr_translation_key = "energy_limits"

    def __init__(self, coordinator: SmartApplianceCoordinator) -> None:
        """Initialize the switch."""
        super().__init__(coordinator, "energy_limits")
        self._attr_name = "Limites énergétiques"
        self._attr_entity_registry_enabled_default = False
    
    @property
    def icon(self) -> str:
        """Return the icon to use in the frontend."""
        return "mdi:gauge-full" if self.is_on else "mdi:gauge-empty"
    
    @property
    def is_on(self) -> bool:
        """Return True if energy limits are enabled."""
        return self.coordinator.energy_limits_enabled
    
    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on energy limits."""
        _LOGGER.info(
            "Activation des limites énergétiques pour '%s'",
            self.coordinator.appliance_name,
        )
        self.coordinator.set_energy_limits_enabled(True)
        await self.coordinator.async_request_refresh()
        self.async_write_ha_state()
    
    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off energy limits."""
        _LOGGER.info(
            "Désactivation des limites énergétiques pour '%s'",
            self.coordinator.appliance_name,
        )
        self.coordinator.set_energy_limits_enabled(False)
        await self.coordinator.async_request_refresh()
        self.async_write_ha_state()


class SmartApplianceSchedulingSwitch(SmartApplianceEntity, SwitchEntity):
    """Switch pour activer/désactiver la planification."""

    _attr_translation_key = "scheduling"

    def __init__(self, coordinator: SmartApplianceCoordinator) -> None:
        """Initialize the switch."""
        super().__init__(coordinator, "scheduling")
        self._attr_name = "Planification"
        self._attr_entity_registry_enabled_default = False
    
    @property
    def icon(self) -> str:
        """Return the icon to use in the frontend."""
        return "mdi:calendar-clock" if self.is_on else "mdi:calendar-remove"
    
    @property
    def is_on(self) -> bool:
        """Return True if scheduling is enabled."""
        return self.coordinator.scheduling_enabled
    
    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on scheduling."""
        _LOGGER.info(
            "Activation de la planification pour '%s'",
            self.coordinator.appliance_name,
        )
        self.coordinator.set_scheduling_enabled(True)
        await self.coordinator.async_request_refresh()
        self.async_write_ha_state()
    
    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off scheduling."""
        _LOGGER.info(
            "Désactivation de la planification pour '%s'",
            self.coordinator.appliance_name,
        )
        self.coordinator.set_scheduling_enabled(False)
        await self.coordinator.async_request_refresh()
        self.async_write_ha_state()


class SmartApplianceAIAnalysisSwitch(SmartApplianceEntity, SwitchEntity):
    """Switch to enable/disable AI analysis."""

    _attr_translation_key = "ai_analysis"

    def __init__(self, coordinator: SmartApplianceCoordinator) -> None:
        """Initialize the switch."""
        super().__init__(coordinator, "ai_analysis")
        self._attr_name = "AI Analysis"
        self._attr_entity_registry_enabled_default = False
    
    @property
    def icon(self) -> str:
        """Return the icon to use in the frontend."""
        return "mdi:brain" if self.is_on else "mdi:brain-off"
    
    @property
    def is_on(self) -> bool:
        """Return True if AI analysis is enabled."""
        return getattr(self.coordinator, "ai_analysis_enabled", False)
    
    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on AI analysis."""
        _LOGGER.info(
            "Enabling AI analysis for '%s'",
            self.coordinator.appliance_name,
        )
        self.coordinator.set_ai_analysis_enabled(True)
        await self.coordinator.async_request_refresh()
        self.async_write_ha_state()
    
    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off AI analysis."""
        _LOGGER.info(
            "Disabling AI analysis for '%s'",
            self.coordinator.appliance_name,
        )
        self.coordinator.set_ai_analysis_enabled(False)
        await self.coordinator.async_request_refresh()
        self.async_write_ha_state()
    
    @property
    def available(self) -> bool:
        """Return True if AI Task entity is configured."""
        # Check if global AI config has an AI Task entity
        global_config = self.hass.data.get(DOMAIN, {}).get("global_config")
        if not global_config:
            return False
        
        ai_task_entity = global_config.get_sync("ai_task_entity")
        return ai_task_entity is not None

