"""Tests pour le coordinator."""
from __future__ import annotations

from datetime import timedelta
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from homeassistant.helpers.update_coordinator import UpdateFailed

from custom_components.smart_appliance_monitor.coordinator import (
    SmartApplianceCoordinator,
)
from custom_components.smart_appliance_monitor.const import (
    EVENT_CYCLE_STARTED,
    EVENT_CYCLE_FINISHED,
    EVENT_ALERT_DURATION,
    STATE_IDLE,
    STATE_RUNNING,
)


@pytest.mark.asyncio
async def test_coordinator_init(mock_hass, mock_config_entry):
    """Test l'initialisation du coordinator."""
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    
    assert coordinator.appliance_name == "Four"
    assert coordinator.appliance_type == "oven"
    assert coordinator.power_sensor == "sensor.prise_four_power"
    assert coordinator.energy_sensor == "sensor.prise_four_energy"
    assert coordinator.price_kwh == 0.2516
    assert coordinator.monitoring_enabled is True
    assert coordinator.notifications_enabled is True
    assert coordinator.state_machine is not None


@pytest.mark.asyncio
async def test_update_data_success(mock_hass, mock_config_entry):
    """Test la mise à jour des données avec succès."""
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    
    # Mock des états des capteurs
    power_state = MagicMock()
    power_state.state = "10.5"
    energy_state = MagicMock()
    energy_state.state = "1.234"
    
    mock_hass.states.get.side_effect = lambda entity_id: (
        power_state if "power" in entity_id else energy_state
    )
    
    # Mise à jour
    data = await coordinator._async_update_data()
    
    assert data["power"] == 10.5
    assert data["energy"] == 1.234
    assert data["state"] == STATE_IDLE
    assert data["monitoring_enabled"] is True
    assert data["notifications_enabled"] is True


@pytest.mark.asyncio
async def test_update_data_missing_power_sensor(mock_hass, mock_config_entry):
    """Test que l'update échoue si le capteur de puissance est manquant."""
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    
    # Mock : capteur de puissance non disponible
    mock_hass.states.get.return_value = None
    
    with pytest.raises(UpdateFailed) as exc_info:
        await coordinator._async_update_data()
    
    assert "non disponible" in str(exc_info.value).lower()


@pytest.mark.asyncio
async def test_update_data_invalid_power_value(mock_hass, mock_config_entry):
    """Test que les valeurs invalides sont gérées."""
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    
    # Mock des états avec valeur invalide
    power_state = MagicMock()
    power_state.state = "unavailable"
    energy_state = MagicMock()
    energy_state.state = "1.234"
    
    mock_hass.states.get.side_effect = lambda entity_id: (
        power_state if "power" in entity_id else energy_state
    )
    
    # Mise à jour (devrait utiliser 0.0 par défaut)
    data = await coordinator._async_update_data()
    
    assert data["power"] == 0.0
    assert data["energy"] == 1.234


@pytest.mark.asyncio
async def test_monitoring_disabled(mock_hass, mock_config_entry):
    """Test que la machine à états n'est pas mise à jour si la surveillance est désactivée."""
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    coordinator.monitoring_enabled = False
    
    # Mock des états
    power_state = MagicMock()
    power_state.state = "100"
    energy_state = MagicMock()
    energy_state.state = "1.0"
    
    mock_hass.states.get.side_effect = lambda entity_id: (
        power_state if "power" in entity_id else energy_state
    )
    
    # Mock de la machine à états
    with patch.object(coordinator.state_machine, "update") as mock_update:
        await coordinator._async_update_data()
        
        # La machine à états ne doit pas être mise à jour
        mock_update.assert_not_called()


@pytest.mark.asyncio
async def test_event_cycle_started(mock_hass, mock_config_entry):
    """Test que l'événement cycle_started est émis correctement."""
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    
    # Simuler un événement cycle_started
    await coordinator._handle_event(EVENT_CYCLE_STARTED)
    
    # Vérifier que l'événement a été émis
    mock_hass.bus.async_fire.assert_called_once()
    call_args = mock_hass.bus.async_fire.call_args
    assert call_args[0][0] == "smart_appliance_monitor_cycle_started"
    assert call_args[0][1]["appliance_name"] == "Four"


@pytest.mark.asyncio
async def test_event_cycle_finished(mock_hass, mock_config_entry):
    """Test que l'événement cycle_finished est émis avec les bonnes stats."""
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    
    # Simuler un cycle terminé
    coordinator.state_machine.last_cycle = {
        "duration": 45.0,
        "energy": 1.2,
    }
    
    await coordinator._handle_event(EVENT_CYCLE_FINISHED)
    
    # Vérifier que l'événement a été émis
    mock_hass.bus.async_fire.assert_called_once()
    call_args = mock_hass.bus.async_fire.call_args
    assert call_args[0][0] == "smart_appliance_monitor_cycle_finished"
    assert call_args[0][1]["duration"] == 45.0
    assert call_args[0][1]["energy"] == 1.2
    assert call_args[0][1]["cost"] == pytest.approx(0.30, abs=0.01)  # 1.2 * 0.2516
    
    # Vérifier que les stats ont été mises à jour
    assert coordinator.daily_stats["cycles"] == 1
    assert coordinator.daily_stats["total_energy"] == 1.2
    assert coordinator.daily_stats["total_cost"] == pytest.approx(0.30, abs=0.01)


@pytest.mark.asyncio
async def test_event_alert_duration(mock_hass, mock_config_entry):
    """Test que l'événement alert_duration est émis."""
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    
    await coordinator._handle_event(EVENT_ALERT_DURATION)
    
    # Vérifier que l'événement a été émis
    mock_hass.bus.async_fire.assert_called_once()
    call_args = mock_hass.bus.async_fire.call_args
    assert call_args[0][0] == "smart_appliance_monitor_alert_duration"


@pytest.mark.asyncio
async def test_daily_stats_reset(mock_hass, mock_config_entry):
    """Test que les stats journalières se réinitialisent."""
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    
    # Définir des stats pour hier
    from datetime import date, timedelta
    yesterday = date.today() - timedelta(days=1)
    coordinator.daily_stats = {
        "date": yesterday,
        "cycles": 5,
        "total_energy": 10.0,
        "total_cost": 2.52,
    }
    
    # Mock des états
    power_state = MagicMock()
    power_state.state = "10"
    energy_state = MagicMock()
    energy_state.state = "1.0"
    
    mock_hass.states.get.side_effect = lambda entity_id: (
        power_state if "power" in entity_id else energy_state
    )
    
    # Mise à jour (devrait réinitialiser les stats)
    await coordinator._async_update_data()
    
    assert coordinator.daily_stats["date"] == date.today()
    assert coordinator.daily_stats["cycles"] == 0
    assert coordinator.daily_stats["total_energy"] == 0.0
    assert coordinator.daily_stats["total_cost"] == 0.0


@pytest.mark.asyncio
async def test_reset_statistics(mock_hass, mock_config_entry):
    """Test la réinitialisation complète des statistiques."""
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    
    # Définir des stats
    coordinator.daily_stats["cycles"] = 5
    coordinator.monthly_stats["total_cost"] = 10.0
    coordinator.state_machine.last_cycle = {"duration": 45}
    
    # Réinitialiser
    coordinator.reset_statistics()
    
    assert coordinator.daily_stats["cycles"] == 0
    assert coordinator.monthly_stats["total_cost"] == 0.0
    assert coordinator.state_machine.last_cycle is None


@pytest.mark.asyncio
async def test_set_monitoring_enabled(mock_hass, mock_config_entry):
    """Test l'activation/désactivation de la surveillance."""
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    
    assert coordinator.monitoring_enabled is True
    
    coordinator.set_monitoring_enabled(False)
    assert coordinator.monitoring_enabled is False
    
    coordinator.set_monitoring_enabled(True)
    assert coordinator.monitoring_enabled is True


@pytest.mark.asyncio
async def test_set_notifications_enabled(mock_hass, mock_config_entry):
    """Test l'activation/désactivation des notifications."""
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    
    assert coordinator.notifications_enabled is True
    
    coordinator.set_notifications_enabled(False)
    assert coordinator.notifications_enabled is False
    
    coordinator.set_notifications_enabled(True)
    assert coordinator.notifications_enabled is True

