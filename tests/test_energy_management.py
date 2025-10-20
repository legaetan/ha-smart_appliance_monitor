"""Tests pour la fonctionnalité de gestion de l'énergie."""
from __future__ import annotations

from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from homeassistant.core import HomeAssistant

from custom_components.smart_appliance_monitor.coordinator import (
    SmartApplianceCoordinator,
)
from custom_components.smart_appliance_monitor.const import (
    CONF_ENABLE_ENERGY_LIMITS,
    CONF_ENERGY_LIMIT_CYCLE,
    CONF_ENERGY_LIMIT_DAILY,
    CONF_ENERGY_LIMIT_MONTHLY,
    CONF_COST_BUDGET_MONTHLY,
    EVENT_ENERGY_LIMIT_EXCEEDED,
    EVENT_BUDGET_EXCEEDED,
)


@pytest.mark.asyncio
async def test_energy_limits_disabled_by_default(mock_hass, mock_config_entry):
    """Test que les limites énergétiques sont désactivées par défaut."""
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    
    assert coordinator.energy_limits_enabled is False
    assert coordinator.energy_limit_cycle == 0
    assert coordinator.energy_limit_daily == 0
    assert coordinator.energy_limit_monthly == 0
    assert coordinator.cost_budget_monthly == 0


@pytest.mark.asyncio
async def test_energy_limits_enabled(mock_hass, mock_config_entry):
    """Test l'activation des limites énergétiques."""
    mock_config_entry.options = {
        CONF_ENABLE_ENERGY_LIMITS: True,
        CONF_ENERGY_LIMIT_CYCLE: 2.0,  # 2 kWh max par cycle
        CONF_ENERGY_LIMIT_DAILY: 5.0,  # 5 kWh max par jour
        CONF_ENERGY_LIMIT_MONTHLY: 50.0,  # 50 kWh max par mois
        CONF_COST_BUDGET_MONTHLY: 12.5,  # 12.5€ max par mois
    }
    
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    
    assert coordinator.energy_limits_enabled is True
    assert coordinator.energy_limit_cycle == 2.0
    assert coordinator.energy_limit_daily == 5.0
    assert coordinator.energy_limit_monthly == 50.0
    assert coordinator.cost_budget_monthly == 12.5


@pytest.mark.asyncio
async def test_cycle_energy_limit_not_exceeded(mock_hass, mock_config_entry):
    """Test qu'aucun événement n'est déclenché si la limite du cycle n'est pas dépassée."""
    mock_config_entry.options = {
        CONF_ENABLE_ENERGY_LIMITS: True,
        CONF_ENERGY_LIMIT_CYCLE: 2.0,
    }
    
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    coordinator.monitoring_enabled = True
    coordinator.data = {
        "current_cycle": {
            "energy": 1.5,  # En dessous de la limite
        }
    }
    
    # Mock des états
    power_state = MagicMock()
    power_state.state = "100.0"
    energy_state = MagicMock()
    energy_state.state = "1.5"
    
    mock_hass.states.get.side_effect = lambda entity_id: (
        power_state if "power" in entity_id else energy_state
    )
    
    # Mise à jour
    await coordinator._async_update_data()
    
    # Aucun événement ne doit être déclenché
    assert not any(
        call[0][0] == EVENT_ENERGY_LIMIT_EXCEEDED 
        for call in mock_hass.bus.async_fire.call_args_list
    )


@pytest.mark.asyncio
async def test_cycle_energy_limit_exceeded(mock_hass, mock_config_entry):
    """Test qu'un événement est déclenché si la limite du cycle est dépassée."""
    mock_config_entry.options = {
        CONF_ENABLE_ENERGY_LIMITS: True,
        CONF_ENERGY_LIMIT_CYCLE: 2.0,
    }
    
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    coordinator.monitoring_enabled = True
    coordinator.data = {
        "current_cycle": {
            "energy": 2.5,  # Dépasse la limite
        }
    }
    coordinator.daily_stats = {"total_energy": 2.5}
    coordinator.monthly_stats = {"total_energy": 2.5}
    
    # Mock des états
    power_state = MagicMock()
    power_state.state = "100.0"
    energy_state = MagicMock()
    energy_state.state = "2.5"
    
    mock_hass.states.get.side_effect = lambda entity_id: (
        power_state if "power" in entity_id else energy_state
    )
    
    # Mise à jour
    await coordinator._async_update_data()
    
    # Un événement doit être déclenché
    assert any(
        call[0][0] == EVENT_ENERGY_LIMIT_EXCEEDED 
        for call in mock_hass.bus.async_fire.call_args_list
    )


@pytest.mark.asyncio
async def test_daily_energy_limit_exceeded(mock_hass, mock_config_entry):
    """Test qu'un événement est déclenché si la limite journalière est dépassée."""
    mock_config_entry.options = {
        CONF_ENABLE_ENERGY_LIMITS: True,
        CONF_ENERGY_LIMIT_DAILY: 5.0,
    }
    
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    coordinator.monitoring_enabled = True
    coordinator.data = {"current_cycle": None}
    coordinator.daily_stats = {"total_energy": 5.5}  # Dépasse la limite
    coordinator.monthly_stats = {"total_energy": 5.5}
    
    # Mock des états
    power_state = MagicMock()
    power_state.state = "0.0"
    energy_state = MagicMock()
    energy_state.state = "5.5"
    
    mock_hass.states.get.side_effect = lambda entity_id: (
        power_state if "power" in entity_id else energy_state
    )
    
    # Mise à jour
    await coordinator._async_update_data()
    
    # Un événement doit être déclenché
    assert any(
        call[0][0] == EVENT_ENERGY_LIMIT_EXCEEDED 
        for call in mock_hass.bus.async_fire.call_args_list
    )


@pytest.mark.asyncio
async def test_monthly_energy_limit_exceeded(mock_hass, mock_config_entry):
    """Test qu'un événement est déclenché si la limite mensuelle est dépassée."""
    mock_config_entry.options = {
        CONF_ENABLE_ENERGY_LIMITS: True,
        CONF_ENERGY_LIMIT_MONTHLY: 50.0,
    }
    
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    coordinator.monitoring_enabled = True
    coordinator.data = {"current_cycle": None}
    coordinator.daily_stats = {"total_energy": 2.0}
    coordinator.monthly_stats = {"total_energy": 52.0}  # Dépasse la limite
    
    # Mock des états
    power_state = MagicMock()
    power_state.state = "0.0"
    energy_state = MagicMock()
    energy_state.state = "52.0"
    
    mock_hass.states.get.side_effect = lambda entity_id: (
        power_state if "power" in entity_id else energy_state
    )
    
    # Mise à jour
    await coordinator._async_update_data()
    
    # Un événement doit être déclenché
    assert any(
        call[0][0] == EVENT_ENERGY_LIMIT_EXCEEDED 
        for call in mock_hass.bus.async_fire.call_args_list
    )


@pytest.mark.asyncio
async def test_monthly_budget_exceeded(mock_hass, mock_config_entry):
    """Test qu'un événement est déclenché si le budget mensuel est dépassé."""
    mock_config_entry.options = {
        CONF_ENABLE_ENERGY_LIMITS: True,
        CONF_COST_BUDGET_MONTHLY: 10.0,
    }
    
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    coordinator.monitoring_enabled = True
    coordinator.data = {"current_cycle": None}
    coordinator.daily_stats = {"total_energy": 2.0}
    coordinator.monthly_stats = {
        "total_energy": 45.0,
        "total_cost": 11.3  # Dépasse le budget
    }
    
    # Mock des états
    power_state = MagicMock()
    power_state.state = "0.0"
    energy_state = MagicMock()
    energy_state.state = "45.0"
    
    mock_hass.states.get.side_effect = lambda entity_id: (
        power_state if "power" in entity_id else energy_state
    )
    
    # Mise à jour
    await coordinator._async_update_data()
    
    # Un événement budget doit être déclenché
    assert any(
        call[0][0] == EVENT_BUDGET_EXCEEDED 
        for call in mock_hass.bus.async_fire.call_args_list
    )


@pytest.mark.asyncio
async def test_energy_limit_notification_once(mock_hass, mock_config_entry):
    """Test que la notification n'est envoyée qu'une fois par période."""
    mock_config_entry.options = {
        CONF_ENABLE_ENERGY_LIMITS: True,
        CONF_ENERGY_LIMIT_DAILY: 5.0,
    }
    
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    coordinator.monitoring_enabled = True
    coordinator.data = {"current_cycle": None}
    coordinator.daily_stats = {"total_energy": 5.5}
    coordinator.monthly_stats = {"total_energy": 5.5}
    
    # Mock des états
    power_state = MagicMock()
    power_state.state = "0.0"
    energy_state = MagicMock()
    energy_state.state = "5.5"
    
    mock_hass.states.get.side_effect = lambda entity_id: (
        power_state if "power" in entity_id else energy_state
    )
    
    # Première mise à jour - événement déclenché
    await coordinator._async_update_data()
    first_call_count = len([
        call for call in mock_hass.bus.async_fire.call_args_list
        if call[0][0] == EVENT_ENERGY_LIMIT_EXCEEDED
    ])
    
    # Reset du mock
    mock_hass.bus.async_fire.reset_mock()
    
    # Deuxième mise à jour - pas de nouvel événement
    await coordinator._async_update_data()
    second_call_count = len([
        call for call in mock_hass.bus.async_fire.call_args_list
        if call[0][0] == EVENT_ENERGY_LIMIT_EXCEEDED
    ])
    
    assert first_call_count > 0
    assert second_call_count == 0


@pytest.mark.asyncio
async def test_budget_notification_once(mock_hass, mock_config_entry):
    """Test que la notification budget n'est envoyée qu'une fois par mois."""
    mock_config_entry.options = {
        CONF_ENABLE_ENERGY_LIMITS: True,
        CONF_COST_BUDGET_MONTHLY: 10.0,
    }
    
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    coordinator.monitoring_enabled = True
    coordinator.data = {"current_cycle": None}
    coordinator.daily_stats = {"total_energy": 2.0}
    coordinator.monthly_stats = {
        "total_energy": 45.0,
        "total_cost": 11.3
    }
    
    # Mock des états
    power_state = MagicMock()
    power_state.state = "0.0"
    energy_state = MagicMock()
    energy_state.state = "45.0"
    
    mock_hass.states.get.side_effect = lambda entity_id: (
        power_state if "power" in entity_id else energy_state
    )
    
    # Première mise à jour
    await coordinator._async_update_data()
    first_call_count = len([
        call for call in mock_hass.bus.async_fire.call_args_list
        if call[0][0] == EVENT_BUDGET_EXCEEDED
    ])
    
    # Reset du mock
    mock_hass.bus.async_fire.reset_mock()
    
    # Deuxième mise à jour
    await coordinator._async_update_data()
    second_call_count = len([
        call for call in mock_hass.bus.async_fire.call_args_list
        if call[0][0] == EVENT_BUDGET_EXCEEDED
    ])
    
    assert first_call_count > 0
    assert second_call_count == 0


@pytest.mark.asyncio
async def test_set_energy_limits_enabled(mock_hass, mock_config_entry):
    """Test l'activation/désactivation du monitoring des limites."""
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    
    assert coordinator.energy_limits_enabled is False
    
    coordinator.set_energy_limits_enabled(True)
    assert coordinator.energy_limits_enabled is True
    
    coordinator.set_energy_limits_enabled(False)
    assert coordinator.energy_limits_enabled is False


@pytest.mark.asyncio
async def test_energy_limits_disabled_monitoring(mock_hass, mock_config_entry):
    """Test que les limites ne sont pas vérifiées si monitoring désactivé."""
    mock_config_entry.options = {
        CONF_ENABLE_ENERGY_LIMITS: True,
        CONF_ENERGY_LIMIT_DAILY: 5.0,
    }
    
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    coordinator.monitoring_enabled = False  # Désactivé
    coordinator.data = {"current_cycle": None}
    coordinator.daily_stats = {"total_energy": 10.0}  # Bien au-dessus de la limite
    
    # Mock des états
    power_state = MagicMock()
    power_state.state = "0.0"
    energy_state = MagicMock()
    energy_state.state = "10.0"
    
    mock_hass.states.get.side_effect = lambda entity_id: (
        power_state if "power" in entity_id else energy_state
    )
    
    # Mise à jour
    await coordinator._async_update_data()
    
    # Aucun événement ne doit être déclenché
    assert not any(
        call[0][0] == EVENT_ENERGY_LIMIT_EXCEEDED 
        for call in mock_hass.bus.async_fire.call_args_list
    )


@pytest.mark.asyncio
async def test_zero_limit_means_disabled(mock_hass, mock_config_entry):
    """Test qu'une limite à 0 signifie désactivée."""
    mock_config_entry.options = {
        CONF_ENABLE_ENERGY_LIMITS: True,
        CONF_ENERGY_LIMIT_DAILY: 0,  # Limite désactivée
    }
    
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    coordinator.monitoring_enabled = True
    coordinator.data = {"current_cycle": None}
    coordinator.daily_stats = {"total_energy": 1000.0}  # Très élevé
    coordinator.monthly_stats = {"total_energy": 1000.0}
    
    # Mock des états
    power_state = MagicMock()
    power_state.state = "0.0"
    energy_state = MagicMock()
    energy_state.state = "1000.0"
    
    mock_hass.states.get.side_effect = lambda entity_id: (
        power_state if "power" in entity_id else energy_state
    )
    
    # Mise à jour
    await coordinator._async_update_data()
    
    # Aucun événement ne doit être déclenché (limite = 0)
    assert not any(
        call[0][0] == EVENT_ENERGY_LIMIT_EXCEEDED 
        for call in mock_hass.bus.async_fire.call_args_list
    )


@pytest.mark.asyncio
async def test_multiple_limits_exceeded(mock_hass, mock_config_entry):
    """Test que plusieurs limites peuvent être dépassées simultanément."""
    mock_config_entry.options = {
        CONF_ENABLE_ENERGY_LIMITS: True,
        CONF_ENERGY_LIMIT_DAILY: 5.0,
        CONF_ENERGY_LIMIT_MONTHLY: 40.0,
        CONF_COST_BUDGET_MONTHLY: 10.0,
    }
    
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    coordinator.monitoring_enabled = True
    coordinator.data = {"current_cycle": None}
    coordinator.daily_stats = {"total_energy": 6.0}  # Dépasse daily
    coordinator.monthly_stats = {
        "total_energy": 45.0,  # Dépasse monthly
        "total_cost": 11.3  # Dépasse budget
    }
    
    # Mock des états
    power_state = MagicMock()
    power_state.state = "0.0"
    energy_state = MagicMock()
    energy_state.state = "45.0"
    
    mock_hass.states.get.side_effect = lambda entity_id: (
        power_state if "power" in entity_id else energy_state
    )
    
    # Mise à jour
    await coordinator._async_update_data()
    
    # Les deux types d'événements doivent être déclenchés
    event_types = [call[0][0] for call in mock_hass.bus.async_fire.call_args_list]
    
    assert EVENT_ENERGY_LIMIT_EXCEEDED in event_types
    assert EVENT_BUDGET_EXCEEDED in event_types

