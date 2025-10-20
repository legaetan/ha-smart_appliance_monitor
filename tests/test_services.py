"""Tests pour les services."""
from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from custom_components.smart_appliance_monitor import (
    async_setup_services,
    _get_coordinator_from_entity_id,
)
from custom_components.smart_appliance_monitor.const import DOMAIN, STATE_RUNNING


@pytest.mark.asyncio
async def test_setup_services(mock_hass):
    """Test l'enregistrement des services."""
    # Mock du service register
    mock_hass.services = MagicMock()
    mock_hass.services.async_register = MagicMock()
    
    await async_setup_services(mock_hass)
    
    # Vérifier que les 3 services ont été enregistrés
    assert mock_hass.services.async_register.call_count == 3
    
    # Vérifier les noms des services
    calls = [call[0] for call in mock_hass.services.async_register.call_args_list]
    service_names = [call[1] for call in calls]
    
    assert "start_cycle" in service_names
    assert "stop_monitoring" in service_names
    assert "reset_statistics" in service_names


@pytest.mark.asyncio
async def test_service_start_cycle(mock_hass, mock_config_entry):
    """Test le service start_cycle."""
    from custom_components.smart_appliance_monitor.coordinator import SmartApplianceCoordinator
    
    # Créer un coordinator
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    coordinator.data = {"power": 100.0, "energy": 1.0}
    coordinator._handle_event = AsyncMock()
    coordinator.async_request_refresh = AsyncMock()
    
    mock_hass.data[DOMAIN] = {mock_config_entry.entry_id: coordinator}
    
    # Mock du service call
    call = MagicMock()
    call.data = {"entity_id": f"sensor.{mock_config_entry.entry_id}_state"}
    
    # Enregistrer les services
    await async_setup_services(mock_hass)
    
    # Récupérer le handler du service
    start_cycle_handler = None
    for call_args in mock_hass.services.async_register.call_args_list:
        if call_args[0][1] == "start_cycle":
            start_cycle_handler = call_args[0][2]
            break
    
    assert start_cycle_handler is not None
    
    # Appeler le service
    await start_cycle_handler(call)
    
    # Vérifier que le cycle a été démarré
    assert coordinator.state_machine.state == STATE_RUNNING
    assert coordinator.state_machine.current_cycle is not None
    coordinator._handle_event.assert_called_once()
    coordinator.async_request_refresh.assert_called_once()


@pytest.mark.asyncio
async def test_service_stop_monitoring(mock_hass, mock_config_entry):
    """Test le service stop_monitoring."""
    from custom_components.smart_appliance_monitor.coordinator import SmartApplianceCoordinator
    
    # Créer un coordinator
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    coordinator.set_monitoring_enabled = MagicMock()
    coordinator.async_request_refresh = AsyncMock()
    
    mock_hass.data[DOMAIN] = {mock_config_entry.entry_id: coordinator}
    
    # Mock du service call
    call = MagicMock()
    call.data = {"entity_id": f"sensor.{mock_config_entry.entry_id}_state"}
    
    # Enregistrer les services
    await async_setup_services(mock_hass)
    
    # Récupérer le handler du service
    stop_monitoring_handler = None
    for call_args in mock_hass.services.async_register.call_args_list:
        if call_args[0][1] == "stop_monitoring":
            stop_monitoring_handler = call_args[0][2]
            break
    
    assert stop_monitoring_handler is not None
    
    # Appeler le service
    await stop_monitoring_handler(call)
    
    # Vérifier que la surveillance a été désactivée
    coordinator.set_monitoring_enabled.assert_called_once_with(False)
    coordinator.async_request_refresh.assert_called_once()


@pytest.mark.asyncio
async def test_service_reset_statistics(mock_hass, mock_config_entry):
    """Test le service reset_statistics."""
    from custom_components.smart_appliance_monitor.coordinator import SmartApplianceCoordinator
    
    # Créer un coordinator
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    coordinator.reset_statistics = MagicMock()
    coordinator.async_request_refresh = AsyncMock()
    
    mock_hass.data[DOMAIN] = {mock_config_entry.entry_id: coordinator}
    
    # Mock du service call
    call = MagicMock()
    call.data = {"entity_id": f"sensor.{mock_config_entry.entry_id}_state"}
    
    # Enregistrer les services
    await async_setup_services(mock_hass)
    
    # Récupérer le handler du service
    reset_statistics_handler = None
    for call_args in mock_hass.services.async_register.call_args_list:
        if call_args[0][1] == "reset_statistics":
            reset_statistics_handler = call_args[0][2]
            break
    
    assert reset_statistics_handler is not None
    
    # Appeler le service
    await reset_statistics_handler(call)
    
    # Vérifier que les statistiques ont été réinitialisées
    coordinator.reset_statistics.assert_called_once()
    coordinator.async_request_refresh.assert_called_once()


def test_get_coordinator_from_entity_id(mock_hass, mock_config_entry):
    """Test la fonction _get_coordinator_from_entity_id."""
    from custom_components.smart_appliance_monitor.coordinator import SmartApplianceCoordinator
    
    # Créer un coordinator
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    mock_hass.data[DOMAIN] = {mock_config_entry.entry_id: coordinator}
    
    # Tester avec un entity_id valide
    entity_id = f"sensor.{mock_config_entry.entry_id}_state"
    result = _get_coordinator_from_entity_id(mock_hass, entity_id)
    
    assert result is not None
    assert result == coordinator


def test_get_coordinator_from_entity_id_not_found(mock_hass):
    """Test _get_coordinator_from_entity_id quand l'entité n'existe pas."""
    mock_hass.data[DOMAIN] = {}
    
    result = _get_coordinator_from_entity_id(mock_hass, "sensor.unknown_entity")
    
    assert result is None

