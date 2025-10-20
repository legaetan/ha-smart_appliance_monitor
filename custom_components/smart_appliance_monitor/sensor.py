"""Sensors pour Smart Appliance Monitor."""
from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfEnergy, UnitOfTime
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    DOMAIN,
    CONF_APPLIANCE_TYPE,
    CONF_PRICE_KWH,
    SESSION_BASED_TYPES,
    STATE_IDLE,
    STATE_RUNNING,
    STATE_FINISHED,
)
from .coordinator import SmartApplianceCoordinator
from .entity import SmartApplianceEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Smart Appliance Monitor sensors."""
    coordinator: SmartApplianceCoordinator = hass.data[DOMAIN][entry.entry_id]
    
    entities = [
        SmartApplianceStateSensor(coordinator),
        SmartApplianceCycleDurationSensor(coordinator),
        SmartApplianceCycleEnergySensor(coordinator),
        SmartApplianceCycleCostSensor(coordinator),
        SmartApplianceLastCycleDurationSensor(coordinator),
        SmartApplianceLastCycleEnergySensor(coordinator),
        SmartApplianceLastCycleCostSensor(coordinator),
        SmartApplianceDailyCyclesSensor(coordinator),
        SmartApplianceDailyCostSensor(coordinator),
        SmartApplianceDailyEnergySensor(coordinator),
        SmartApplianceMonthlyCostSensor(coordinator),
        SmartApplianceMonthlyEnergySensor(coordinator),
    ]
    
    # Ajouter sensor anomaly score si activé
    if coordinator.anomaly_detection_enabled:
        entities.append(SmartApplianceAnomalyScoreSensor(coordinator))
    
    async_add_entities(entities)
    _LOGGER.info(
        "Sensors créés pour '%s' (%d entités)",
        coordinator.appliance_name,
        len(entities),
    )


class SmartApplianceStateSensor(SmartApplianceEntity, SensorEntity):
    """Sensor pour l'état actuel de l'appareil."""

    _attr_device_class = SensorDeviceClass.ENUM
    _attr_options = [STATE_IDLE, STATE_RUNNING, STATE_FINISHED]
    _attr_translation_key = "state"

    def __init__(self, coordinator: SmartApplianceCoordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, "state")
        self._attr_name = "État"
    
    @property
    def native_value(self) -> str:
        """Return the state of the sensor."""
        return self.coordinator.data.get("state", STATE_IDLE)
    
    @property
    def icon(self) -> str:
        """Return the icon to use in the frontend."""
        state = self.native_value
        if state == STATE_RUNNING:
            return "mdi:power"
        elif state == STATE_FINISHED:
            return "mdi:check-circle"
        else:
            return "mdi:power-off"
    
    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional state attributes."""
        attributes = {
            "monitoring_enabled": self.coordinator.monitoring_enabled,
        }
        
        if self.coordinator.data.get("current_cycle"):
            cycle = self.coordinator.data["current_cycle"]
            attributes["current_power"] = self.coordinator.data.get("power")
            attributes["peak_power"] = cycle.get("peak_power")
        
        return attributes


class SmartApplianceCycleDurationSensor(SmartApplianceEntity, SensorEntity):
    """Sensor pour la durée du cycle en cours."""

    _attr_device_class = SensorDeviceClass.DURATION
    _attr_native_unit_of_measurement = UnitOfTime.MINUTES
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, coordinator: SmartApplianceCoordinator) -> None:
        """Initialize the sensor."""
        appliance_type = coordinator.entry.data.get(CONF_APPLIANCE_TYPE)
        is_session_based = appliance_type in SESSION_BASED_TYPES
        
        entity_id = "session_duration" if is_session_based else "cycle_duration"
        super().__init__(coordinator, entity_id)
        
        self._attr_translation_key = entity_id
        self._attr_name = "Durée de session" if is_session_based else "Durée du cycle"
    
    @property
    def native_value(self) -> float:
        """Return the duration of the current cycle in minutes."""
        if self.coordinator.data.get("state") != STATE_RUNNING:
            return 0
        
        return self.coordinator.state_machine.get_cycle_duration()
    
    @property
    def icon(self) -> str:
        """Return the icon to use in the frontend."""
        return "mdi:timer-outline"


class SmartApplianceCycleEnergySensor(SmartApplianceEntity, SensorEntity):
    """Sensor pour l'énergie consommée pendant le cycle en cours."""

    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_native_unit_of_measurement = UnitOfEnergy.WATT_HOUR
    _attr_state_class = SensorStateClass.TOTAL_INCREASING

    def __init__(self, coordinator: SmartApplianceCoordinator) -> None:
        """Initialize the sensor."""
        appliance_type = coordinator.entry.data.get(CONF_APPLIANCE_TYPE)
        is_session_based = appliance_type in SESSION_BASED_TYPES
        
        entity_id = "session_energy" if is_session_based else "cycle_energy"
        super().__init__(coordinator, entity_id)
        
        self._attr_translation_key = entity_id
        self._attr_name = "Énergie de session" if is_session_based else "Énergie du cycle"
    
    @property
    def native_value(self) -> float:
        """Return the energy consumed during the current cycle in Wh."""
        if self.coordinator.data.get("state") != STATE_RUNNING:
            return 0
        
        current_energy = self.coordinator.data.get("energy", 0)
        energy_kwh = self.coordinator.state_machine.get_cycle_energy(current_energy)
        return round(energy_kwh * 1000, 1)  # Convertir kWh en Wh
    
    @property
    def icon(self) -> str:
        """Return the icon to use in the frontend."""
        return "mdi:lightning-bolt"


class SmartApplianceCycleCostSensor(SmartApplianceEntity, SensorEntity):
    """Sensor pour le coût du cycle en cours."""

    _attr_device_class = SensorDeviceClass.MONETARY
    _attr_native_unit_of_measurement = "EUR"
    _attr_state_class = SensorStateClass.TOTAL

    def __init__(self, coordinator: SmartApplianceCoordinator) -> None:
        """Initialize the sensor."""
        appliance_type = coordinator.entry.data.get(CONF_APPLIANCE_TYPE)
        is_session_based = appliance_type in SESSION_BASED_TYPES
        
        entity_id = "session_cost" if is_session_based else "cycle_cost"
        super().__init__(coordinator, entity_id)
        
        self._attr_translation_key = entity_id
        self._attr_name = "Coût de session" if is_session_based else "Coût du cycle"
    
    @property
    def native_value(self) -> float:
        """Return the cost of the current cycle in EUR."""
        if self.coordinator.data.get("state") != STATE_RUNNING:
            return 0
        
        current_energy = self.coordinator.data.get("energy", 0)
        energy_kwh = self.coordinator.state_machine.get_cycle_energy(current_energy)
        cost = energy_kwh * self.coordinator.price_kwh
        return round(cost, 2)
    
    @property
    def icon(self) -> str:
        """Return the icon to use in the frontend."""
        return "mdi:currency-eur"
    
    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional state attributes."""
        return {
            "price_kwh": self.coordinator.price_kwh,
        }


class SmartApplianceLastCycleDurationSensor(SmartApplianceEntity, SensorEntity):
    """Sensor pour la durée du dernier cycle."""

    _attr_device_class = SensorDeviceClass.DURATION
    _attr_native_unit_of_measurement = UnitOfTime.MINUTES
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, coordinator: SmartApplianceCoordinator) -> None:
        """Initialize the sensor."""
        appliance_type = coordinator.entry.data.get(CONF_APPLIANCE_TYPE)
        is_session_based = appliance_type in SESSION_BASED_TYPES
        
        entity_id = "last_session_duration" if is_session_based else "last_cycle_duration"
        super().__init__(coordinator, entity_id)
        
        self._attr_translation_key = entity_id
        self._attr_name = "Durée de la dernière session" if is_session_based else "Durée du dernier cycle"
    
    @property
    def native_value(self) -> float | None:
        """Return the duration of the last cycle in minutes."""
        last_cycle = self.coordinator.data.get("last_cycle")
        if not last_cycle:
            return None
        
        return last_cycle.get("duration", 0)
    
    @property
    def icon(self) -> str:
        """Return the icon to use in the frontend."""
        return "mdi:timer"
    
    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional state attributes."""
        last_cycle = self.coordinator.data.get("last_cycle")
        if not last_cycle:
            return {}
        
        return {
            "start_time": last_cycle.get("start_time"),
            "end_time": last_cycle.get("end_time"),
            "peak_power": last_cycle.get("peak_power"),
        }


class SmartApplianceLastCycleEnergySensor(SmartApplianceEntity, SensorEntity):
    """Sensor pour l'énergie du dernier cycle."""

    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_native_unit_of_measurement = UnitOfEnergy.WATT_HOUR
    _attr_state_class = SensorStateClass.TOTAL

    def __init__(self, coordinator: SmartApplianceCoordinator) -> None:
        """Initialize the sensor."""
        appliance_type = coordinator.entry.data.get(CONF_APPLIANCE_TYPE)
        is_session_based = appliance_type in SESSION_BASED_TYPES
        
        entity_id = "last_session_energy" if is_session_based else "last_cycle_energy"
        super().__init__(coordinator, entity_id)
        
        self._attr_translation_key = entity_id
        self._attr_name = "Énergie de la dernière session" if is_session_based else "Énergie du dernier cycle"
    
    @property
    def native_value(self) -> float | None:
        """Return the energy of the last cycle in Wh."""
        last_cycle = self.coordinator.data.get("last_cycle")
        if not last_cycle:
            return None
        
        energy_kwh = last_cycle.get("energy", 0)
        return round(energy_kwh * 1000, 1)  # Convertir kWh en Wh
    
    @property
    def icon(self) -> str:
        """Return the icon to use in the frontend."""
        return "mdi:lightning-bolt-outline"


class SmartApplianceLastCycleCostSensor(SmartApplianceEntity, SensorEntity):
    """Sensor pour le coût du dernier cycle."""

    _attr_device_class = SensorDeviceClass.MONETARY
    _attr_native_unit_of_measurement = "EUR"
    _attr_state_class = SensorStateClass.TOTAL

    def __init__(self, coordinator: SmartApplianceCoordinator) -> None:
        """Initialize the sensor."""
        appliance_type = coordinator.entry.data.get(CONF_APPLIANCE_TYPE)
        is_session_based = appliance_type in SESSION_BASED_TYPES
        
        entity_id = "last_session_cost" if is_session_based else "last_cycle_cost"
        super().__init__(coordinator, entity_id)
        
        self._attr_translation_key = entity_id
        self._attr_name = "Coût de la dernière session" if is_session_based else "Coût du dernier cycle"
    
    @property
    def native_value(self) -> float | None:
        """Return the cost of the last cycle in EUR."""
        last_cycle = self.coordinator.data.get("last_cycle")
        if not last_cycle:
            return None
        
        energy_kwh = last_cycle.get("energy", 0)
        cost = energy_kwh * self.coordinator.price_kwh
        return round(cost, 2)
    
    @property
    def icon(self) -> str:
        """Return the icon to use in the frontend."""
        return "mdi:currency-eur"


class SmartApplianceDailyCyclesSensor(SmartApplianceEntity, SensorEntity):
    """Sensor pour le nombre de cycles journaliers."""

    _attr_state_class = SensorStateClass.TOTAL

    def __init__(self, coordinator: SmartApplianceCoordinator) -> None:
        """Initialize the sensor."""
        appliance_type = coordinator.entry.data.get(CONF_APPLIANCE_TYPE)
        is_session_based = appliance_type in SESSION_BASED_TYPES
        
        entity_id = "daily_sessions" if is_session_based else "daily_cycles"
        super().__init__(coordinator, entity_id)
        
        self._attr_translation_key = entity_id
        self._attr_name = "Sessions du jour" if is_session_based else "Cycles du jour"
    
    @property
    def native_value(self) -> int:
        """Return the number of cycles today."""
        daily_stats = self.coordinator.data.get("daily_stats", {})
        return daily_stats.get("cycles", 0)
    
    @property
    def icon(self) -> str:
        """Return the icon to use in the frontend."""
        return "mdi:counter"
    
    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional state attributes."""
        daily_stats = self.coordinator.data.get("daily_stats", {})
        return {
            "date": daily_stats.get("date"),
            "total_energy": round(daily_stats.get("total_energy", 0), 3),
        }


class SmartApplianceDailyCostSensor(SmartApplianceEntity, SensorEntity):
    """Sensor pour le coût journalier."""

    _attr_device_class = SensorDeviceClass.MONETARY
    _attr_native_unit_of_measurement = "EUR"
    _attr_state_class = SensorStateClass.TOTAL
    _attr_translation_key = "daily_cost"

    def __init__(self, coordinator: SmartApplianceCoordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, "daily_cost")
        self._attr_name = "Coût du jour"
    
    @property
    def native_value(self) -> float:
        """Return the cost today in EUR."""
        daily_stats = self.coordinator.data.get("daily_stats", {})
        return round(daily_stats.get("total_cost", 0), 2)
    
    @property
    def icon(self) -> str:
        """Return the icon to use in the frontend."""
        return "mdi:cash"
    
    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional state attributes."""
        daily_stats = self.coordinator.data.get("daily_stats", {})
        return {
            "date": daily_stats.get("date"),
            "cycles": daily_stats.get("cycles", 0),
        }


class SmartApplianceDailyEnergySensor(SmartApplianceEntity, SensorEntity):
    """Sensor pour l'énergie journalière."""

    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR
    _attr_state_class = SensorStateClass.TOTAL
    _attr_translation_key = "daily_energy"

    def __init__(self, coordinator: SmartApplianceCoordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, "daily_energy")
        self._attr_name = "Énergie du jour"
    
    @property
    def native_value(self) -> float:
        """Return the energy today in kWh."""
        daily_stats = self.coordinator.data.get("daily_stats", {})
        return round(daily_stats.get("total_energy", 0), 3)
    
    @property
    def icon(self) -> str:
        """Return the icon to use in the frontend."""
        return "mdi:lightning-bolt"
    
    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional state attributes."""
        daily_stats = self.coordinator.data.get("daily_stats", {})
        return {
            "date": daily_stats.get("date"),
            "cycles": daily_stats.get("cycles", 0),
            "total_cost": round(daily_stats.get("total_cost", 0), 2),
        }


class SmartApplianceMonthlyCostSensor(SmartApplianceEntity, SensorEntity):
    """Sensor pour le coût mensuel."""

    _attr_device_class = SensorDeviceClass.MONETARY
    _attr_native_unit_of_measurement = "EUR"
    _attr_state_class = SensorStateClass.TOTAL
    _attr_translation_key = "monthly_cost"

    def __init__(self, coordinator: SmartApplianceCoordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, "monthly_cost")
        self._attr_name = "Coût du mois"
    
    @property
    def native_value(self) -> float:
        """Return the cost this month in EUR."""
        monthly_stats = self.coordinator.data.get("monthly_stats", {})
        return round(monthly_stats.get("total_cost", 0), 2)
    
    @property
    def icon(self) -> str:
        """Return the icon to use in the frontend."""
        return "mdi:cash-multiple"
    
    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional state attributes."""
        monthly_stats = self.coordinator.data.get("monthly_stats", {})
        return {
            "year": monthly_stats.get("year"),
            "month": monthly_stats.get("month"),
            "total_energy": round(monthly_stats.get("total_energy", 0), 3),
        }


class SmartApplianceMonthlyEnergySensor(SmartApplianceEntity, SensorEntity):
    """Sensor pour l'énergie mensuelle."""

    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR
    _attr_state_class = SensorStateClass.TOTAL
    _attr_translation_key = "monthly_energy"

    def __init__(self, coordinator: SmartApplianceCoordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, "monthly_energy")
        self._attr_name = "Énergie du mois"
    
    @property
    def native_value(self) -> float:
        """Return the energy this month in kWh."""
        monthly_stats = self.coordinator.data.get("monthly_stats", {})
        return round(monthly_stats.get("total_energy", 0), 3)
    
    @property
    def icon(self) -> str:
        """Return the icon to use in the frontend."""
        return "mdi:lightning-bolt-circle"
    
    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional state attributes."""
        monthly_stats = self.coordinator.data.get("monthly_stats", {})
        return {
            "year": monthly_stats.get("year"),
            "month": monthly_stats.get("month"),
            "total_cost": round(monthly_stats.get("total_cost", 0), 2),
        }


class SmartApplianceAnomalyScoreSensor(SmartApplianceEntity, SensorEntity):
    """Sensor pour le score d'anomalie."""

    _attr_native_unit_of_measurement = "%"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_translation_key = "anomaly_score"

    def __init__(self, coordinator: SmartApplianceCoordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, "anomaly_score")
        self._attr_name = "Score d'anomalie"
    
    @property
    def native_value(self) -> float:
        """Return the anomaly score (0-100)."""
        return self.coordinator.get_anomaly_score()
    
    @property
    def icon(self) -> str:
        """Return the icon to use in the frontend."""
        score = self.native_value
        if score >= 70:
            return "mdi:alert-circle"
        elif score >= 40:
            return "mdi:alert"
        else:
            return "mdi:check-circle"
    
    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional state attributes."""
        return {
            "history_size": len(self.coordinator._cycle_history),
            "detection_enabled": self.coordinator.anomaly_detection_enabled,
            "current_state": self.coordinator.data.get("state"),
        }

