"""Tests pour les switches."""
from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from custom_components.smart_appliance_monitor.switch import (
    SmartApplianceMonitoringSwitch,
    SmartApplianceNotificationsSwitch,
)
from custom_components.smart_appliance_monitor.const import STATE_IDLE


@pytest.fixture
def mock_coordinator_data():
    """Fixture pour créer des données de coordinator."""
    return {
        "power": 10.0,
        "energy": 1.0,
        "state": STATE_IDLE,
        "monitoring_enabled": True,
        "notifications_enabled": True,
    }


@pytest.fixture
def monitoring_switch(mock_hass, mock_config_entry):
    """Fixture pour créer un switch de surveillance."""
    from custom_components.smart_appliance_monitor.coordinator import SmartApplianceCoordinator
    
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    return SmartApplianceMonitoringSwitch(coordinator)


@pytest.fixture
def notifications_switch(mock_hass, mock_config_entry):
    """Fixture pour créer un switch de notifications."""
    from custom_components.smart_appliance_monitor.coordinator import SmartApplianceCoordinator
    
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    return SmartApplianceNotificationsSwitch(coordinator)


def test_monitoring_switch_init(monitoring_switch):
    """Test l'initialisation du switch de surveillance."""
    assert monitoring_switch.entity_type == "monitoring"
    assert monitoring_switch._attr_name == "Surveillance"
    assert monitoring_switch.unique_id.endswith("_monitoring")


def test_monitoring_switch_is_on(monitoring_switch):
    """Test que le switch est on quand la surveillance est activée."""
    monitoring_switch.coordinator.monitoring_enabled = True
    assert monitoring_switch.is_on is True
    assert monitoring_switch.icon == "mdi:monitor-eye"


def test_monitoring_switch_is_off(monitoring_switch):
    """Test que le switch est off quand la surveillance est désactivée."""
    monitoring_switch.coordinator.monitoring_enabled = False
    assert monitoring_switch.is_on is False
    assert monitoring_switch.icon == "mdi:monitor-off"


@pytest.mark.asyncio
async def test_monitoring_switch_turn_on(monitoring_switch):
    """Test l'activation de la surveillance."""
    monitoring_switch.coordinator.set_monitoring_enabled = MagicMock()
    monitoring_switch.coordinator.async_request_refresh = AsyncMock()
    
    await monitoring_switch.async_turn_on()
    
    monitoring_switch.coordinator.set_monitoring_enabled.assert_called_once_with(True)
    monitoring_switch.coordinator.async_request_refresh.assert_called_once()


@pytest.mark.asyncio
async def test_monitoring_switch_turn_off(monitoring_switch):
    """Test la désactivation de la surveillance."""
    monitoring_switch.coordinator.set_monitoring_enabled = MagicMock()
    monitoring_switch.coordinator.async_request_refresh = AsyncMock()
    
    await monitoring_switch.async_turn_off()
    
    monitoring_switch.coordinator.set_monitoring_enabled.assert_called_once_with(False)
    monitoring_switch.coordinator.async_request_refresh.assert_called_once()


def test_monitoring_switch_attributes(monitoring_switch, mock_coordinator_data):
    """Test les attributs supplémentaires du switch de surveillance."""
    monitoring_switch.coordinator.data = mock_coordinator_data
    
    attributes = monitoring_switch.extra_state_attributes
    assert attributes["state"] == STATE_IDLE


def test_notifications_switch_init(notifications_switch):
    """Test l'initialisation du switch de notifications."""
    assert notifications_switch.entity_type == "notifications"
    assert notifications_switch._attr_name == "Notifications"
    assert notifications_switch.unique_id.endswith("_notifications")


def test_notifications_switch_is_on(notifications_switch):
    """Test que le switch est on quand les notifications sont activées."""
    notifications_switch.coordinator.notifications_enabled = True
    assert notifications_switch.is_on is True
    assert notifications_switch.icon == "mdi:bell-ring"


def test_notifications_switch_is_off(notifications_switch):
    """Test que le switch est off quand les notifications sont désactivées."""
    notifications_switch.coordinator.notifications_enabled = False
    assert notifications_switch.is_on is False
    assert notifications_switch.icon == "mdi:bell-off"


@pytest.mark.asyncio
async def test_notifications_switch_turn_on(notifications_switch):
    """Test l'activation des notifications."""
    notifications_switch.coordinator.set_notifications_enabled = MagicMock()
    notifications_switch.coordinator.async_request_refresh = AsyncMock()
    
    await notifications_switch.async_turn_on()
    
    notifications_switch.coordinator.set_notifications_enabled.assert_called_once_with(True)
    notifications_switch.coordinator.async_request_refresh.assert_called_once()


@pytest.mark.asyncio
async def test_notifications_switch_turn_off(notifications_switch):
    """Test la désactivation des notifications."""
    notifications_switch.coordinator.set_notifications_enabled = MagicMock()
    notifications_switch.coordinator.async_request_refresh = AsyncMock()
    
    await notifications_switch.async_turn_off()
    
    notifications_switch.coordinator.set_notifications_enabled.assert_called_once_with(False)
    notifications_switch.coordinator.async_request_refresh.assert_called_once()

