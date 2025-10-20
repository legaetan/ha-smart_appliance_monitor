"""Tests pour les binary sensors."""
from __future__ import annotations

from datetime import datetime, timedelta
from unittest.mock import MagicMock, AsyncMock, patch

import pytest

from custom_components.smart_appliance_monitor.binary_sensor import (
    SmartApplianceRunningBinarySensor,
    SmartApplianceAlertDurationBinarySensor,
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
        "daily_stats": {"cycles": 0, "total_energy": 0.0, "total_cost": 0.0},
        "monthly_stats": {"total_cost": 0.0},
        "monitoring_enabled": True,
        "notifications_enabled": True,
    }


@pytest.fixture
def running_binary_sensor(mock_hass, mock_config_entry):
    """Fixture pour créer un binary sensor running."""
    from custom_components.smart_appliance_monitor.coordinator import SmartApplianceCoordinator
    
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    return SmartApplianceRunningBinarySensor(coordinator)


@pytest.fixture
def alert_binary_sensor(mock_hass, mock_config_entry):
    """Fixture pour créer un binary sensor alert."""
    from custom_components.smart_appliance_monitor.coordinator import SmartApplianceCoordinator
    
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    return SmartApplianceAlertDurationBinarySensor(coordinator)


def test_running_sensor_init(running_binary_sensor):
    """Test l'initialisation du binary sensor running."""
    assert running_binary_sensor.entity_type == "running"
    assert running_binary_sensor._attr_name == "En marche"
    assert running_binary_sensor.unique_id.endswith("_running")


def test_running_sensor_off_when_idle(running_binary_sensor, mock_coordinator_data):
    """Test que le sensor est off quand l'appareil est idle."""
    mock_coordinator_data["state"] = STATE_IDLE
    running_binary_sensor.coordinator.data = mock_coordinator_data
    
    assert running_binary_sensor.is_on is False


def test_running_sensor_on_when_running(running_binary_sensor, mock_coordinator_data):
    """Test que le sensor est on quand l'appareil est en marche."""
    mock_coordinator_data["state"] = STATE_RUNNING
    mock_coordinator_data["current_cycle"] = {
        "start_time": datetime.now(),
        "peak_power": 150.0,
    }
    running_binary_sensor.coordinator.data = mock_coordinator_data
    
    assert running_binary_sensor.is_on is True


def test_running_sensor_off_when_finished(running_binary_sensor, mock_coordinator_data):
    """Test que le sensor est off quand le cycle est terminé."""
    mock_coordinator_data["state"] = STATE_FINISHED
    running_binary_sensor.coordinator.data = mock_coordinator_data
    
    assert running_binary_sensor.is_on is False


def test_running_sensor_attributes_when_running(running_binary_sensor, mock_coordinator_data):
    """Test les attributs supplémentaires quand l'appareil est en marche."""
    start_time = datetime(2025, 10, 20, 18, 30, 0)
    mock_coordinator_data["state"] = STATE_RUNNING
    mock_coordinator_data["current_cycle"] = {
        "start_time": start_time,
        "peak_power": 200.0,
    }
    running_binary_sensor.coordinator.data = mock_coordinator_data
    
    attributes = running_binary_sensor.extra_state_attributes
    
    assert "start_time" in attributes
    assert "peak_power" in attributes
    assert attributes["start_time"] == start_time
    assert attributes["peak_power"] == 200.0


def test_running_sensor_no_attributes_when_idle(running_binary_sensor, mock_coordinator_data):
    """Test qu'il n'y a pas d'attributs supplémentaires quand idle."""
    mock_coordinator_data["state"] = STATE_IDLE
    running_binary_sensor.coordinator.data = mock_coordinator_data
    
    attributes = running_binary_sensor.extra_state_attributes
    
    assert attributes == {}


def test_alert_sensor_init(alert_binary_sensor):
    """Test l'initialisation du binary sensor alert."""
    assert alert_binary_sensor.entity_type == "alert_duration"
    assert alert_binary_sensor._attr_name == "Alerte durée"
    assert alert_binary_sensor.unique_id.endswith("_alert_duration")
    assert alert_binary_sensor._alert_triggered is False


def test_alert_sensor_off_by_default(alert_binary_sensor, mock_coordinator_data):
    """Test que le sensor alert est off par défaut."""
    alert_binary_sensor.coordinator.data = mock_coordinator_data
    
    assert alert_binary_sensor.is_on is False


@pytest.mark.asyncio
async def test_alert_sensor_triggered_by_event(alert_binary_sensor, mock_coordinator_data):
    """Test que l'alerte est déclenchée par un événement."""
    from custom_components.smart_appliance_monitor.const import DOMAIN
    
    mock_coordinator_data["state"] = STATE_RUNNING
    alert_binary_sensor.coordinator.data = mock_coordinator_data
    
    # Créer un mock d'événement
    event = MagicMock()
    event.data = {"entry_id": alert_binary_sensor.coordinator.entry.entry_id}
    
    # Déclencher l'événement
    await alert_binary_sensor._handle_alert_event(event)
    
    assert alert_binary_sensor.is_on is True


def test_alert_sensor_reset_when_cycle_finished(alert_binary_sensor, mock_coordinator_data):
    """Test que l'alerte se réinitialise quand le cycle se termine."""
    # Déclencher l'alerte
    alert_binary_sensor._alert_triggered = True
    
    # Le cycle se termine
    mock_coordinator_data["state"] = STATE_FINISHED
    alert_binary_sensor.coordinator.data = mock_coordinator_data
    
    assert alert_binary_sensor.is_on is False
    assert alert_binary_sensor._alert_triggered is False


def test_alert_sensor_attributes_when_triggered(alert_binary_sensor, mock_coordinator_data):
    """Test les attributs supplémentaires quand l'alerte est déclenchée."""
    start_time = datetime.now() - timedelta(hours=2, minutes=15)
    
    mock_coordinator_data["state"] = STATE_RUNNING
    mock_coordinator_data["current_cycle"] = {
        "start_time": start_time,
    }
    alert_binary_sensor.coordinator.data = mock_coordinator_data
    alert_binary_sensor._alert_triggered = True
    alert_binary_sensor.coordinator.state_machine.alert_duration = 7200  # 2 heures
    
    attributes = alert_binary_sensor.extra_state_attributes
    
    assert "duration_minutes" in attributes
    assert "alert_threshold" in attributes
    assert attributes["duration_minutes"] >= 135  # 2h15 = 135 min
    assert attributes["alert_threshold"] == 120  # 7200 / 60 = 120 min

