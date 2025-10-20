"""Tests pour les sensors."""
from __future__ import annotations

from datetime import datetime, date
from unittest.mock import MagicMock

import pytest

from custom_components.smart_appliance_monitor.sensor import (
    SmartApplianceStateSensor,
    SmartApplianceCycleDurationSensor,
    SmartApplianceCycleEnergySensor,
    SmartApplianceCycleCostSensor,
    SmartApplianceLastCycleDurationSensor,
    SmartApplianceLastCycleEnergySensor,
    SmartApplianceLastCycleCostSensor,
    SmartApplianceDailyCyclesSensor,
    SmartApplianceDailyCostSensor,
    SmartApplianceMonthlyCostSensor,
)
from custom_components.smart_appliance_monitor.const import STATE_IDLE, STATE_RUNNING, STATE_FINISHED


@pytest.fixture
def mock_coordinator_data():
    """Fixture pour créer des données de coordinator."""
    return {
        "power": 10.0,
        "energy": 1.0,
        "state": STATE_IDLE,
        "current_cycle": None,
        "last_cycle": None,
        "daily_stats": {
            "date": date.today(),
            "cycles": 0,
            "total_energy": 0.0,
            "total_cost": 0.0,
        },
        "monthly_stats": {
            "year": 2025,
            "month": 10,
            "total_cost": 0.0,
        },
        "monitoring_enabled": True,
        "notifications_enabled": True,
    }


@pytest.fixture
def state_sensor(mock_hass, mock_config_entry):
    """Fixture pour créer un sensor d'état."""
    from custom_components.smart_appliance_monitor.coordinator import SmartApplianceCoordinator
    
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    return SmartApplianceStateSensor(coordinator)


def test_state_sensor_init(state_sensor):
    """Test l'initialisation du sensor d'état."""
    assert state_sensor.entity_type == "state"
    assert state_sensor._attr_name == "État"
    assert state_sensor.unique_id.endswith("_state")


def test_state_sensor_idle(state_sensor, mock_coordinator_data):
    """Test le sensor d'état quand l'appareil est idle."""
    mock_coordinator_data["state"] = STATE_IDLE
    state_sensor.coordinator.data = mock_coordinator_data
    
    assert state_sensor.native_value == STATE_IDLE
    assert state_sensor.icon == "mdi:power-off"


def test_state_sensor_running(state_sensor, mock_coordinator_data):
    """Test le sensor d'état quand l'appareil est en marche."""
    mock_coordinator_data["state"] = STATE_RUNNING
    mock_coordinator_data["power"] = 150.0
    mock_coordinator_data["current_cycle"] = {
        "start_time": datetime.now(),
        "peak_power": 200.0,
    }
    state_sensor.coordinator.data = mock_coordinator_data
    
    assert state_sensor.native_value == STATE_RUNNING
    assert state_sensor.icon == "mdi:power"
    
    attributes = state_sensor.extra_state_attributes
    assert attributes["monitoring_enabled"] is True
    assert attributes["current_power"] == 150.0
    assert attributes["peak_power"] == 200.0


def test_state_sensor_finished(state_sensor, mock_coordinator_data):
    """Test le sensor d'état quand le cycle est terminé."""
    mock_coordinator_data["state"] = STATE_FINISHED
    state_sensor.coordinator.data = mock_coordinator_data
    
    assert state_sensor.native_value == STATE_FINISHED
    assert state_sensor.icon == "mdi:check-circle"


def test_cycle_duration_sensor(mock_hass, mock_config_entry, mock_coordinator_data):
    """Test le sensor de durée du cycle."""
    from custom_components.smart_appliance_monitor.coordinator import SmartApplianceCoordinator
    
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    sensor = SmartApplianceCycleDurationSensor(coordinator)
    
    # Pas de cycle en cours
    mock_coordinator_data["state"] = STATE_IDLE
    sensor.coordinator.data = mock_coordinator_data
    assert sensor.native_value == 0
    
    # Cycle en cours
    mock_coordinator_data["state"] = STATE_RUNNING
    sensor.coordinator.data = mock_coordinator_data
    sensor.coordinator.state_machine.get_cycle_duration = MagicMock(return_value=23.5)
    
    assert sensor.native_value == 23.5


def test_cycle_energy_sensor(mock_hass, mock_config_entry, mock_coordinator_data):
    """Test le sensor d'énergie du cycle."""
    from custom_components.smart_appliance_monitor.coordinator import SmartApplianceCoordinator
    
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    sensor = SmartApplianceCycleEnergySensor(coordinator)
    
    # Pas de cycle en cours
    mock_coordinator_data["state"] = STATE_IDLE
    sensor.coordinator.data = mock_coordinator_data
    assert sensor.native_value == 0
    
    # Cycle en cours : 1.234 kWh = 1234 Wh
    mock_coordinator_data["state"] = STATE_RUNNING
    mock_coordinator_data["energy"] = 2.0
    sensor.coordinator.data = mock_coordinator_data
    sensor.coordinator.state_machine.get_cycle_energy = MagicMock(return_value=1.234)
    
    assert sensor.native_value == 1234.0


def test_cycle_cost_sensor(mock_hass, mock_config_entry, mock_coordinator_data):
    """Test le sensor de coût du cycle."""
    from custom_components.smart_appliance_monitor.coordinator import SmartApplianceCoordinator
    
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    sensor = SmartApplianceCycleCostSensor(coordinator)
    
    # Pas de cycle en cours
    mock_coordinator_data["state"] = STATE_IDLE
    sensor.coordinator.data = mock_coordinator_data
    assert sensor.native_value == 0
    
    # Cycle en cours : 1.234 kWh * 0.2516 €/kWh = 0.31 €
    mock_coordinator_data["state"] = STATE_RUNNING
    mock_coordinator_data["energy"] = 2.0
    sensor.coordinator.data = mock_coordinator_data
    sensor.coordinator.state_machine.get_cycle_energy = MagicMock(return_value=1.234)
    
    cost = sensor.native_value
    assert cost == pytest.approx(0.31, abs=0.01)
    
    # Vérifier les attributs
    attributes = sensor.extra_state_attributes
    assert attributes["price_kwh"] == 0.2516


def test_last_cycle_duration_sensor(mock_hass, mock_config_entry, mock_coordinator_data):
    """Test le sensor de durée du dernier cycle."""
    from custom_components.smart_appliance_monitor.coordinator import SmartApplianceCoordinator
    
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    sensor = SmartApplianceLastCycleDurationSensor(coordinator)
    
    # Pas de dernier cycle
    mock_coordinator_data["last_cycle"] = None
    sensor.coordinator.data = mock_coordinator_data
    assert sensor.native_value is None
    
    # Dernier cycle disponible
    start_time = datetime(2025, 10, 20, 18, 30, 0)
    end_time = datetime(2025, 10, 20, 19, 15, 0)
    mock_coordinator_data["last_cycle"] = {
        "start_time": start_time,
        "end_time": end_time,
        "duration": 45.0,
        "peak_power": 200.0,
    }
    sensor.coordinator.data = mock_coordinator_data
    
    assert sensor.native_value == 45.0
    
    # Vérifier les attributs
    attributes = sensor.extra_state_attributes
    assert attributes["start_time"] == start_time
    assert attributes["end_time"] == end_time
    assert attributes["peak_power"] == 200.0


def test_last_cycle_energy_sensor(mock_hass, mock_config_entry, mock_coordinator_data):
    """Test le sensor d'énergie du dernier cycle."""
    from custom_components.smart_appliance_monitor.coordinator import SmartApplianceCoordinator
    
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    sensor = SmartApplianceLastCycleEnergySensor(coordinator)
    
    # Pas de dernier cycle
    mock_coordinator_data["last_cycle"] = None
    sensor.coordinator.data = mock_coordinator_data
    assert sensor.native_value is None
    
    # Dernier cycle : 1.234 kWh = 1234 Wh
    mock_coordinator_data["last_cycle"] = {
        "duration": 45.0,
        "energy": 1.234,
    }
    sensor.coordinator.data = mock_coordinator_data
    
    assert sensor.native_value == 1234.0


def test_last_cycle_cost_sensor(mock_hass, mock_config_entry, mock_coordinator_data):
    """Test le sensor de coût du dernier cycle."""
    from custom_components.smart_appliance_monitor.coordinator import SmartApplianceCoordinator
    
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    sensor = SmartApplianceLastCycleCostSensor(coordinator)
    
    # Pas de dernier cycle
    mock_coordinator_data["last_cycle"] = None
    sensor.coordinator.data = mock_coordinator_data
    assert sensor.native_value is None
    
    # Dernier cycle : 1.234 kWh * 0.2516 €/kWh = 0.31 €
    mock_coordinator_data["last_cycle"] = {
        "duration": 45.0,
        "energy": 1.234,
    }
    sensor.coordinator.data = mock_coordinator_data
    
    cost = sensor.native_value
    assert cost == pytest.approx(0.31, abs=0.01)


def test_daily_cycles_sensor(mock_hass, mock_config_entry, mock_coordinator_data):
    """Test le sensor de cycles journaliers."""
    from custom_components.smart_appliance_monitor.coordinator import SmartApplianceCoordinator
    
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    sensor = SmartApplianceDailyCyclesSensor(coordinator)
    
    # 3 cycles aujourd'hui
    mock_coordinator_data["daily_stats"] = {
        "date": date.today(),
        "cycles": 3,
        "total_energy": 4.567,
        "total_cost": 1.15,
    }
    sensor.coordinator.data = mock_coordinator_data
    
    assert sensor.native_value == 3
    
    # Vérifier les attributs
    attributes = sensor.extra_state_attributes
    assert attributes["date"] == date.today()
    assert attributes["total_energy"] == 4.567


def test_daily_cost_sensor(mock_hass, mock_config_entry, mock_coordinator_data):
    """Test le sensor de coût journalier."""
    from custom_components.smart_appliance_monitor.coordinator import SmartApplianceCoordinator
    
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    sensor = SmartApplianceDailyCostSensor(coordinator)
    
    # Coût du jour
    mock_coordinator_data["daily_stats"] = {
        "date": date.today(),
        "cycles": 3,
        "total_energy": 4.567,
        "total_cost": 1.15,
    }
    sensor.coordinator.data = mock_coordinator_data
    
    assert sensor.native_value == 1.15
    
    # Vérifier les attributs
    attributes = sensor.extra_state_attributes
    assert attributes["date"] == date.today()
    assert attributes["cycles"] == 3


def test_monthly_cost_sensor(mock_hass, mock_config_entry, mock_coordinator_data):
    """Test le sensor de coût mensuel."""
    from custom_components.smart_appliance_monitor.coordinator import SmartApplianceCoordinator
    
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    sensor = SmartApplianceMonthlyCostSensor(coordinator)
    
    # Coût du mois
    mock_coordinator_data["monthly_stats"] = {
        "year": 2025,
        "month": 10,
        "total_cost": 12.75,
    }
    sensor.coordinator.data = mock_coordinator_data
    
    assert sensor.native_value == 12.75
    
    # Vérifier les attributs
    attributes = sensor.extra_state_attributes
    assert attributes["year"] == 2025
    assert attributes["month"] == 10

