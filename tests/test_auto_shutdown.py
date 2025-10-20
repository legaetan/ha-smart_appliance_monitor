"""Tests pour la fonctionnalité d'extinction automatique."""
from __future__ import annotations

from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from homeassistant.core import HomeAssistant

from custom_components.smart_appliance_monitor.coordinator import (
    SmartApplianceCoordinator,
)
from custom_components.smart_appliance_monitor.const import (
    CONF_ENABLE_AUTO_SHUTDOWN,
    CONF_AUTO_SHUTDOWN_DELAY,
    CONF_AUTO_SHUTDOWN_ENTITY,
    DEFAULT_AUTO_SHUTDOWN_DELAY,
    EVENT_AUTO_SHUTDOWN,
    STATE_IDLE,
)


@pytest.mark.asyncio
async def test_auto_shutdown_disabled_by_default(mock_hass, mock_config_entry):
    """Test que l'extinction automatique est désactivée par défaut."""
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    
    assert coordinator.auto_shutdown_enabled is False
    assert coordinator.auto_shutdown_delay == DEFAULT_AUTO_SHUTDOWN_DELAY
    assert coordinator.auto_shutdown_entity is None


@pytest.mark.asyncio
async def test_auto_shutdown_enabled(mock_hass, mock_config_entry):
    """Test l'activation de l'extinction automatique."""
    mock_config_entry.options = {
        CONF_ENABLE_AUTO_SHUTDOWN: True,
        CONF_AUTO_SHUTDOWN_DELAY: 30,
        CONF_AUTO_SHUTDOWN_ENTITY: "switch.monitor_plug",
    }
    
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    
    assert coordinator.auto_shutdown_enabled is True
    assert coordinator.auto_shutdown_delay == 30
    assert coordinator.auto_shutdown_entity == "switch.monitor_plug"


@pytest.mark.asyncio
async def test_auto_shutdown_timer_starts_on_idle(mock_hass, mock_config_entry):
    """Test que le timer démarre quand l'appareil devient idle."""
    mock_config_entry.options = {
        CONF_ENABLE_AUTO_SHUTDOWN: True,
        CONF_AUTO_SHUTDOWN_DELAY: 5,
        CONF_AUTO_SHUTDOWN_ENTITY: "switch.monitor_plug",
    }
    
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    coordinator.monitoring_enabled = True
    
    # Mock des états
    power_state = MagicMock()
    power_state.state = "0.0"
    energy_state = MagicMock()
    energy_state.state = "0.0"
    
    mock_hass.states.get.side_effect = lambda entity_id: (
        power_state if "power" in entity_id else energy_state
    )
    
    # Mock du temps
    start_time = datetime(2025, 10, 20, 18, 0, 0)
    
    with patch("custom_components.smart_appliance_monitor.coordinator.datetime") as mock_dt:
        mock_dt.now.return_value = start_time
        
        # Première mise à jour (idle)
        await coordinator._async_update_data()
        
        assert coordinator._auto_shutdown_timer is not None
        assert coordinator._auto_shutdown_timer == start_time


@pytest.mark.asyncio
async def test_auto_shutdown_triggers_after_delay(mock_hass, mock_config_entry):
    """Test que l'extinction se déclenche après le délai."""
    mock_config_entry.options = {
        CONF_ENABLE_AUTO_SHUTDOWN: True,
        CONF_AUTO_SHUTDOWN_DELAY: 5,  # 5 minutes
        CONF_AUTO_SHUTDOWN_ENTITY: "switch.monitor_plug",
    }
    
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    coordinator.monitoring_enabled = True
    
    # Mock des états
    power_state = MagicMock()
    power_state.state = "0.0"
    energy_state = MagicMock()
    energy_state.state = "0.0"
    
    mock_hass.states.get.side_effect = lambda entity_id: (
        power_state if "power" in entity_id else energy_state
    )
    
    # Mock des services
    mock_hass.services = MagicMock()
    mock_hass.services.async_call = AsyncMock()
    
    start_time = datetime(2025, 10, 20, 18, 0, 0)
    after_delay = start_time + timedelta(minutes=6)  # 6 minutes après
    
    with patch("custom_components.smart_appliance_monitor.coordinator.datetime") as mock_dt:
        # Premier update : démarre le timer
        mock_dt.now.return_value = start_time
        await coordinator._async_update_data()
        
        # Deuxième update : 6 minutes plus tard
        mock_dt.now.return_value = after_delay
        await coordinator._async_update_data()
        
        # Vérifier que homeassistant.turn_off a été appelé
        mock_hass.services.async_call.assert_called_once_with(
            "homeassistant",
            "turn_off",
            {"entity_id": "switch.monitor_plug"},
        )


@pytest.mark.asyncio
async def test_auto_shutdown_reset_on_running(mock_hass, mock_config_entry):
    """Test que le timer est réinitialisé quand l'appareil redémarre."""
    mock_config_entry.options = {
        CONF_ENABLE_AUTO_SHUTDOWN: True,
        CONF_AUTO_SHUTDOWN_DELAY: 5,
        CONF_AUTO_SHUTDOWN_ENTITY: "switch.monitor_plug",
    }
    
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    coordinator.monitoring_enabled = True
    coordinator._auto_shutdown_timer = datetime(2025, 10, 20, 18, 0, 0)
    
    # Mock des états - appareil en marche
    power_state = MagicMock()
    power_state.state = "100.0"  # En marche
    energy_state = MagicMock()
    energy_state.state = "1.0"
    
    mock_hass.states.get.side_effect = lambda entity_id: (
        power_state if "power" in entity_id else energy_state
    )
    
    # Mise à jour
    await coordinator._async_update_data()
    
    # Timer doit être réinitialisé
    assert coordinator._auto_shutdown_timer is None


@pytest.mark.asyncio
async def test_auto_shutdown_event_fired(mock_hass, mock_config_entry):
    """Test qu'un événement est déclenché lors de l'extinction."""
    mock_config_entry.options = {
        CONF_ENABLE_AUTO_SHUTDOWN: True,
        CONF_AUTO_SHUTDOWN_DELAY: 5,
        CONF_AUTO_SHUTDOWN_ENTITY: "switch.monitor_plug",
    }
    
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    coordinator.monitoring_enabled = True
    
    # Mock des services
    mock_hass.services = MagicMock()
    mock_hass.services.async_call = AsyncMock()
    
    # Appel direct de la méthode d'extinction
    await coordinator._on_auto_shutdown()
    
    # Vérifier que l'événement a été déclenché
    assert mock_hass.bus.async_fire.called
    call_args = mock_hass.bus.async_fire.call_args_list
    
    # Trouver l'appel avec EVENT_AUTO_SHUTDOWN
    event_fired = False
    for call in call_args:
        if call[0][0] == EVENT_AUTO_SHUTDOWN:
            event_fired = True
            break
    
    assert event_fired


@pytest.mark.asyncio
async def test_auto_shutdown_no_entity_configured(mock_hass, mock_config_entry):
    """Test que rien ne se passe si aucune entité n'est configurée."""
    mock_config_entry.options = {
        CONF_ENABLE_AUTO_SHUTDOWN: True,
        CONF_AUTO_SHUTDOWN_DELAY: 5,
        CONF_AUTO_SHUTDOWN_ENTITY: None,  # Pas d'entité
    }
    
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    coordinator.monitoring_enabled = True
    
    # Mock des services
    mock_hass.services = MagicMock()
    mock_hass.services.async_call = AsyncMock()
    
    # Appel direct de la méthode d'extinction
    await coordinator._on_auto_shutdown()
    
    # Aucun service ne doit être appelé
    mock_hass.services.async_call.assert_not_called()


@pytest.mark.asyncio
async def test_set_auto_shutdown_enabled(mock_hass, mock_config_entry):
    """Test l'activation/désactivation du monitoring auto-shutdown."""
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    
    assert coordinator.auto_shutdown_enabled is False
    
    coordinator.set_auto_shutdown_enabled(True)
    assert coordinator.auto_shutdown_enabled is True
    
    coordinator.set_auto_shutdown_enabled(False)
    assert coordinator.auto_shutdown_enabled is False


@pytest.mark.asyncio
async def test_auto_shutdown_timer_persists_across_updates(mock_hass, mock_config_entry):
    """Test que le timer persiste entre les mises à jour tant que idle."""
    mock_config_entry.options = {
        CONF_ENABLE_AUTO_SHUTDOWN: True,
        CONF_AUTO_SHUTDOWN_DELAY: 10,
        CONF_AUTO_SHUTDOWN_ENTITY: "switch.monitor_plug",
    }
    
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    coordinator.monitoring_enabled = True
    
    # Mock des états - toujours idle
    power_state = MagicMock()
    power_state.state = "0.0"
    energy_state = MagicMock()
    energy_state.state = "0.0"
    
    mock_hass.states.get.side_effect = lambda entity_id: (
        power_state if "power" in entity_id else energy_state
    )
    
    start_time = datetime(2025, 10, 20, 18, 0, 0)
    
    with patch("custom_components.smart_appliance_monitor.coordinator.datetime") as mock_dt:
        # Premier update
        mock_dt.now.return_value = start_time
        await coordinator._async_update_data()
        timer1 = coordinator._auto_shutdown_timer
        
        # Deuxième update (2 minutes après)
        mock_dt.now.return_value = start_time + timedelta(minutes=2)
        await coordinator._async_update_data()
        timer2 = coordinator._auto_shutdown_timer
        
        # Le timer doit être le même (pas réinitialisé)
        assert timer1 == timer2


@pytest.mark.asyncio
async def test_auto_shutdown_disabled_monitoring(mock_hass, mock_config_entry):
    """Test que l'auto-shutdown ne fonctionne pas si monitoring désactivé."""
    mock_config_entry.options = {
        CONF_ENABLE_AUTO_SHUTDOWN: True,
        CONF_AUTO_SHUTDOWN_DELAY: 5,
        CONF_AUTO_SHUTDOWN_ENTITY: "switch.monitor_plug",
    }
    
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    coordinator.monitoring_enabled = False  # Désactivé
    
    # Mock des états
    power_state = MagicMock()
    power_state.state = "0.0"
    energy_state = MagicMock()
    energy_state.state = "0.0"
    
    mock_hass.states.get.side_effect = lambda entity_id: (
        power_state if "power" in entity_id else energy_state
    )
    
    # Mise à jour
    await coordinator._async_update_data()
    
    # Le timer ne doit pas démarrer
    assert coordinator._auto_shutdown_timer is None

