"""Tests pour la fonctionnalité de planification d'utilisation."""
from __future__ import annotations

from datetime import datetime, time
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from homeassistant.core import HomeAssistant

from custom_components.smart_appliance_monitor.coordinator import (
    SmartApplianceCoordinator,
)
from custom_components.smart_appliance_monitor.const import (
    CONF_ENABLE_SCHEDULING,
    CONF_ALLOWED_HOURS_START,
    CONF_ALLOWED_HOURS_END,
    CONF_BLOCKED_DAYS,
    CONF_SCHEDULING_MODE,
    SCHEDULING_MODE_NOTIFICATION,
    SCHEDULING_MODE_STRICT,
    EVENT_USAGE_OUT_OF_SCHEDULE,
)


@pytest.mark.asyncio
async def test_scheduling_disabled_by_default(mock_hass, mock_config_entry):
    """Test que la planification est désactivée par défaut."""
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    
    assert coordinator.scheduling_enabled is False
    assert coordinator.allowed_hours_start is None
    assert coordinator.allowed_hours_end is None
    assert coordinator.blocked_days == []
    assert coordinator.scheduling_mode == SCHEDULING_MODE_NOTIFICATION


@pytest.mark.asyncio
async def test_scheduling_enabled(mock_hass, mock_config_entry):
    """Test l'activation de la planification."""
    mock_config_entry.options = {
        CONF_ENABLE_SCHEDULING: True,
        CONF_ALLOWED_HOURS_START: "22:00",
        CONF_ALLOWED_HOURS_END: "07:00",
        CONF_BLOCKED_DAYS: ["sunday"],
        CONF_SCHEDULING_MODE: SCHEDULING_MODE_NOTIFICATION,
    }
    
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    
    assert coordinator.scheduling_enabled is True
    assert coordinator.allowed_hours_start == time(22, 0)
    assert coordinator.allowed_hours_end == time(7, 0)
    assert coordinator.blocked_days == ["sunday"]
    assert coordinator.scheduling_mode == SCHEDULING_MODE_NOTIFICATION


@pytest.mark.asyncio
async def test_usage_allowed_within_hours(mock_hass, mock_config_entry):
    """Test que l'utilisation est autorisée pendant les heures autorisées."""
    mock_config_entry.options = {
        CONF_ENABLE_SCHEDULING: True,
        CONF_ALLOWED_HOURS_START: "08:00",
        CONF_ALLOWED_HOURS_END: "22:00",
        CONF_BLOCKED_DAYS: [],
    }
    
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    
    # Test à 14h (dans la plage)
    current_time = datetime(2025, 10, 20, 14, 0, 0)  # Lundi 14h
    
    with patch("custom_components.smart_appliance_monitor.coordinator.datetime") as mock_dt:
        mock_dt.now.return_value = current_time
        
        allowed = coordinator._is_usage_allowed()
        assert allowed is True


@pytest.mark.asyncio
async def test_usage_blocked_outside_hours(mock_hass, mock_config_entry):
    """Test que l'utilisation est bloquée en dehors des heures autorisées."""
    mock_config_entry.options = {
        CONF_ENABLE_SCHEDULING: True,
        CONF_ALLOWED_HOURS_START: "08:00",
        CONF_ALLOWED_HOURS_END: "22:00",
        CONF_BLOCKED_DAYS: [],
    }
    
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    
    # Test à 23h (hors plage)
    current_time = datetime(2025, 10, 20, 23, 0, 0)
    
    with patch("custom_components.smart_appliance_monitor.coordinator.datetime") as mock_dt:
        mock_dt.now.return_value = current_time
        
        allowed = coordinator._is_usage_allowed()
        assert allowed is False


@pytest.mark.asyncio
async def test_usage_allowed_crossing_midnight(mock_hass, mock_config_entry):
    """Test que la plage horaire qui traverse minuit fonctionne."""
    mock_config_entry.options = {
        CONF_ENABLE_SCHEDULING: True,
        CONF_ALLOWED_HOURS_START: "22:00",
        CONF_ALLOWED_HOURS_END: "07:00",  # Traverse minuit
        CONF_BLOCKED_DAYS: [],
    }
    
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    
    # Test à 23h (autorisé)
    with patch("custom_components.smart_appliance_monitor.coordinator.datetime") as mock_dt:
        mock_dt.now.return_value = datetime(2025, 10, 20, 23, 0, 0)
        assert coordinator._is_usage_allowed() is True
    
    # Test à 6h (autorisé)
    with patch("custom_components.smart_appliance_monitor.coordinator.datetime") as mock_dt:
        mock_dt.now.return_value = datetime(2025, 10, 20, 6, 0, 0)
        assert coordinator._is_usage_allowed() is True
    
    # Test à 14h (bloqué)
    with patch("custom_components.smart_appliance_monitor.coordinator.datetime") as mock_dt:
        mock_dt.now.return_value = datetime(2025, 10, 20, 14, 0, 0)
        assert coordinator._is_usage_allowed() is False


@pytest.mark.asyncio
async def test_usage_blocked_on_blocked_day(mock_hass, mock_config_entry):
    """Test que l'utilisation est bloquée les jours bloqués."""
    mock_config_entry.options = {
        CONF_ENABLE_SCHEDULING: True,
        CONF_ALLOWED_HOURS_START: "00:00",
        CONF_ALLOWED_HOURS_END: "23:59",
        CONF_BLOCKED_DAYS: ["sunday"],
    }
    
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    
    # Test un dimanche (bloqué)
    sunday = datetime(2025, 10, 26, 14, 0, 0)  # Dimanche 26 octobre
    
    with patch("custom_components.smart_appliance_monitor.coordinator.datetime") as mock_dt:
        mock_dt.now.return_value = sunday
        
        allowed = coordinator._is_usage_allowed()
        assert allowed is False


@pytest.mark.asyncio
async def test_usage_allowed_on_non_blocked_day(mock_hass, mock_config_entry):
    """Test que l'utilisation est autorisée les jours non bloqués."""
    mock_config_entry.options = {
        CONF_ENABLE_SCHEDULING: True,
        CONF_ALLOWED_HOURS_START: "00:00",
        CONF_ALLOWED_HOURS_END: "23:59",
        CONF_BLOCKED_DAYS: ["sunday"],
    }
    
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    
    # Test un lundi (non bloqué)
    monday = datetime(2025, 10, 20, 14, 0, 0)  # Lundi 20 octobre
    
    with patch("custom_components.smart_appliance_monitor.coordinator.datetime") as mock_dt:
        mock_dt.now.return_value = monday
        
        allowed = coordinator._is_usage_allowed()
        assert allowed is True


@pytest.mark.asyncio
async def test_multiple_blocked_days(mock_hass, mock_config_entry):
    """Test que plusieurs jours peuvent être bloqués."""
    mock_config_entry.options = {
        CONF_ENABLE_SCHEDULING: True,
        CONF_ALLOWED_HOURS_START: "00:00",
        CONF_ALLOWED_HOURS_END: "23:59",
        CONF_BLOCKED_DAYS: ["saturday", "sunday"],
    }
    
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    
    # Test samedi (bloqué)
    saturday = datetime(2025, 10, 25, 14, 0, 0)
    with patch("custom_components.smart_appliance_monitor.coordinator.datetime") as mock_dt:
        mock_dt.now.return_value = saturday
        assert coordinator._is_usage_allowed() is False
    
    # Test dimanche (bloqué)
    sunday = datetime(2025, 10, 26, 14, 0, 0)
    with patch("custom_components.smart_appliance_monitor.coordinator.datetime") as mock_dt:
        mock_dt.now.return_value = sunday
        assert coordinator._is_usage_allowed() is False
    
    # Test vendredi (autorisé)
    friday = datetime(2025, 10, 24, 14, 0, 0)
    with patch("custom_components.smart_appliance_monitor.coordinator.datetime") as mock_dt:
        mock_dt.now.return_value = friday
        assert coordinator._is_usage_allowed() is True


@pytest.mark.asyncio
async def test_event_fired_when_usage_out_of_schedule(mock_hass, mock_config_entry):
    """Test qu'un événement est déclenché quand l'utilisation est hors horaire."""
    mock_config_entry.options = {
        CONF_ENABLE_SCHEDULING: True,
        CONF_ALLOWED_HOURS_START: "22:00",
        CONF_ALLOWED_HOURS_END: "07:00",
        CONF_BLOCKED_DAYS: [],
    }
    
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    coordinator.monitoring_enabled = True
    coordinator.data = {"state": "running"}
    
    # Mock des états - appareil en marche
    power_state = MagicMock()
    power_state.state = "100.0"
    energy_state = MagicMock()
    energy_state.state = "1.0"
    
    mock_hass.states.get.side_effect = lambda entity_id: (
        power_state if "power" in entity_id else energy_state
    )
    
    # Test à 14h (hors horaire)
    with patch("custom_components.smart_appliance_monitor.coordinator.datetime") as mock_dt:
        mock_dt.now.return_value = datetime(2025, 10, 20, 14, 0, 0)
        
        await coordinator._async_update_data()
    
    # Un événement doit être déclenché
    assert any(
        call[0][0] == EVENT_USAGE_OUT_OF_SCHEDULE 
        for call in mock_hass.bus.async_fire.call_args_list
    )


@pytest.mark.asyncio
async def test_no_event_when_usage_within_schedule(mock_hass, mock_config_entry):
    """Test qu'aucun événement n'est déclenché quand l'utilisation est autorisée."""
    mock_config_entry.options = {
        CONF_ENABLE_SCHEDULING: True,
        CONF_ALLOWED_HOURS_START: "08:00",
        CONF_ALLOWED_HOURS_END: "22:00",
        CONF_BLOCKED_DAYS: [],
    }
    
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    coordinator.monitoring_enabled = True
    coordinator.data = {"state": "running"}
    
    # Mock des états
    power_state = MagicMock()
    power_state.state = "100.0"
    energy_state = MagicMock()
    energy_state.state = "1.0"
    
    mock_hass.states.get.side_effect = lambda entity_id: (
        power_state if "power" in entity_id else energy_state
    )
    
    # Test à 14h (dans l'horaire)
    with patch("custom_components.smart_appliance_monitor.coordinator.datetime") as mock_dt:
        mock_dt.now.return_value = datetime(2025, 10, 20, 14, 0, 0)
        
        await coordinator._async_update_data()
    
    # Aucun événement ne doit être déclenché
    assert not any(
        call[0][0] == EVENT_USAGE_OUT_OF_SCHEDULE 
        for call in mock_hass.bus.async_fire.call_args_list
    )


@pytest.mark.asyncio
async def test_set_scheduling_enabled(mock_hass, mock_config_entry):
    """Test l'activation/désactivation de la planification."""
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    
    assert coordinator.scheduling_enabled is False
    
    coordinator.set_scheduling_enabled(True)
    assert coordinator.scheduling_enabled is True
    
    coordinator.set_scheduling_enabled(False)
    assert coordinator.scheduling_enabled is False


@pytest.mark.asyncio
async def test_scheduling_disabled_monitoring(mock_hass, mock_config_entry):
    """Test que la planification ne fonctionne pas si monitoring désactivé."""
    mock_config_entry.options = {
        CONF_ENABLE_SCHEDULING: True,
        CONF_ALLOWED_HOURS_START: "22:00",
        CONF_ALLOWED_HOURS_END: "07:00",
        CONF_BLOCKED_DAYS: [],
    }
    
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    coordinator.monitoring_enabled = False  # Désactivé
    coordinator.data = {"state": "running"}
    
    # Mock des états
    power_state = MagicMock()
    power_state.state = "100.0"
    energy_state = MagicMock()
    energy_state.state = "1.0"
    
    mock_hass.states.get.side_effect = lambda entity_id: (
        power_state if "power" in entity_id else energy_state
    )
    
    # Test à 14h (hors horaire)
    with patch("custom_components.smart_appliance_monitor.coordinator.datetime") as mock_dt:
        mock_dt.now.return_value = datetime(2025, 10, 20, 14, 0, 0)
        
        await coordinator._async_update_data()
    
    # Aucun événement ne doit être déclenché (monitoring off)
    assert not any(
        call[0][0] == EVENT_USAGE_OUT_OF_SCHEDULE 
        for call in mock_hass.bus.async_fire.call_args_list
    )


@pytest.mark.asyncio
async def test_scheduling_notification_mode(mock_hass, mock_config_entry):
    """Test que le mode notification envoie des alertes."""
    mock_config_entry.options = {
        CONF_ENABLE_SCHEDULING: True,
        CONF_ALLOWED_HOURS_START: "22:00",
        CONF_ALLOWED_HOURS_END: "07:00",
        CONF_BLOCKED_DAYS: [],
        CONF_SCHEDULING_MODE: SCHEDULING_MODE_NOTIFICATION,
    }
    
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    
    assert coordinator.scheduling_mode == SCHEDULING_MODE_NOTIFICATION


@pytest.mark.asyncio
async def test_scheduling_strict_mode(mock_hass, mock_config_entry):
    """Test que le mode strict est configuré."""
    mock_config_entry.options = {
        CONF_ENABLE_SCHEDULING: True,
        CONF_ALLOWED_HOURS_START: "22:00",
        CONF_ALLOWED_HOURS_END: "07:00",
        CONF_BLOCKED_DAYS: [],
        CONF_SCHEDULING_MODE: SCHEDULING_MODE_STRICT,
    }
    
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    
    assert coordinator.scheduling_mode == SCHEDULING_MODE_STRICT


@pytest.mark.asyncio
async def test_boundary_times(mock_hass, mock_config_entry):
    """Test les heures limites (début et fin exactes)."""
    mock_config_entry.options = {
        CONF_ENABLE_SCHEDULING: True,
        CONF_ALLOWED_HOURS_START: "08:00",
        CONF_ALLOWED_HOURS_END: "22:00",
        CONF_BLOCKED_DAYS: [],
    }
    
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    
    # Test à 08:00 exactement (autorisé)
    with patch("custom_components.smart_appliance_monitor.coordinator.datetime") as mock_dt:
        mock_dt.now.return_value = datetime(2025, 10, 20, 8, 0, 0)
        assert coordinator._is_usage_allowed() is True
    
    # Test à 22:00 exactement (autorisé)
    with patch("custom_components.smart_appliance_monitor.coordinator.datetime") as mock_dt:
        mock_dt.now.return_value = datetime(2025, 10, 20, 22, 0, 0)
        assert coordinator._is_usage_allowed() is True
    
    # Test à 07:59 (bloqué)
    with patch("custom_components.smart_appliance_monitor.coordinator.datetime") as mock_dt:
        mock_dt.now.return_value = datetime(2025, 10, 20, 7, 59, 0)
        assert coordinator._is_usage_allowed() is False
    
    # Test à 22:01 (bloqué)
    with patch("custom_components.smart_appliance_monitor.coordinator.datetime") as mock_dt:
        mock_dt.now.return_value = datetime(2025, 10, 20, 22, 1, 0)
        assert coordinator._is_usage_allowed() is False


@pytest.mark.asyncio
async def test_all_days_blocked(mock_hass, mock_config_entry):
    """Test que tous les jours peuvent être bloqués."""
    mock_config_entry.options = {
        CONF_ENABLE_SCHEDULING: True,
        CONF_ALLOWED_HOURS_START: "00:00",
        CONF_ALLOWED_HOURS_END: "23:59",
        CONF_BLOCKED_DAYS: ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"],
    }
    
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    
    # Test chaque jour de la semaine
    for day in range(24, 31):  # 24-30 octobre 2025 (lundi-dimanche)
        test_time = datetime(2025, 10, day, 12, 0, 0)
        with patch("custom_components.smart_appliance_monitor.coordinator.datetime") as mock_dt:
            mock_dt.now.return_value = test_time
            assert coordinator._is_usage_allowed() is False

