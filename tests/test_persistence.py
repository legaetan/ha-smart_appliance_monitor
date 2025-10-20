"""Tests pour la persistance de l'état."""
from __future__ import annotations

from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from custom_components.smart_appliance_monitor.coordinator import (
    SmartApplianceCoordinator,
)
from custom_components.smart_appliance_monitor.const import (
    STATE_IDLE,
    STATE_RUNNING,
    STATE_FINISHED,
)


@pytest.mark.asyncio
async def test_save_and_restore_state(mock_hass, mock_config_entry):
    """Test la sauvegarde et restauration de l'état."""
    # Créer le coordinator
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    
    # Simuler un cycle en cours
    coordinator.state_machine.state = STATE_RUNNING
    coordinator.state_machine.current_cycle = {
        "start_time": datetime.now(),
        "start_energy": 1.0,
        "peak_power": 150.0,
    }
    coordinator.state_machine.last_cycle = {
        "start_time": datetime(2025, 10, 20, 10, 0),
        "end_time": datetime(2025, 10, 20, 11, 30),
        "duration": 90.0,
        "energy": 1.5,
    }
    coordinator.daily_stats["cycles"] = 3
    coordinator.daily_stats["total_energy"] = 4.5
    
    # Sauvegarder l'état
    await coordinator._save_state()
    
    # Créer un nouveau coordinator (simuler un redémarrage)
    coordinator2 = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    
    # Restaurer l'état
    await coordinator2.restore_state()
    
    # Vérifier que l'état a été restauré
    assert coordinator2.state_machine.state == STATE_RUNNING
    assert coordinator2.state_machine.current_cycle is not None
    assert coordinator2.state_machine.current_cycle["start_energy"] == 1.0
    assert coordinator2.state_machine.current_cycle["peak_power"] == 150.0
    assert coordinator2.state_machine.last_cycle is not None
    assert coordinator2.state_machine.last_cycle["duration"] == 90.0
    assert coordinator2.daily_stats["cycles"] == 3
    assert coordinator2.daily_stats["total_energy"] == 4.5


@pytest.mark.asyncio
async def test_restore_state_no_saved_data(mock_hass, mock_config_entry):
    """Test la restauration sans données sauvegardées."""
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    
    # Tenter de restaurer sans données
    await coordinator.restore_state()
    
    # Vérifier les valeurs par défaut
    assert coordinator.state_machine.state == STATE_IDLE
    assert coordinator.state_machine.current_cycle is None
    assert coordinator.monitoring_enabled is True


@pytest.mark.asyncio
async def test_cycle_serialization(mock_hass, mock_config_entry):
    """Test la sérialisation/désérialisation d'un cycle."""
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    
    # Créer un cycle avec datetime
    cycle = {
        "start_time": datetime(2025, 10, 20, 10, 0, 0),
        "end_time": datetime(2025, 10, 20, 11, 30, 0),
        "duration": 90.0,
        "energy": 1.5,
        "peak_power": 200.0,
    }
    
    # Sérialiser
    serialized = coordinator._serialize_cycle(cycle)
    assert isinstance(serialized["start_time"], str)
    assert isinstance(serialized["end_time"], str)
    assert serialized["duration"] == 90.0
    
    # Désérialiser
    deserialized = coordinator._deserialize_cycle(serialized)
    assert isinstance(deserialized["start_time"], datetime)
    assert isinstance(deserialized["end_time"], datetime)
    assert deserialized["start_time"] == cycle["start_time"]
    assert deserialized["end_time"] == cycle["end_time"]
    assert deserialized["duration"] == 90.0


@pytest.mark.asyncio
async def test_stats_serialization(mock_hass, mock_config_entry):
    """Test la sérialisation/désérialisation des statistiques."""
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    
    from datetime import date
    
    # Créer des stats avec date
    stats = {
        "date": date(2025, 10, 20),
        "cycles": 5,
        "total_energy": 10.5,
        "total_cost": 2.64,
    }
    
    # Sérialiser
    serialized = coordinator._serialize_stats(stats)
    assert isinstance(serialized["date"], str)
    assert serialized["cycles"] == 5
    
    # Désérialiser
    deserialized = coordinator._deserialize_stats(serialized)
    assert isinstance(deserialized["date"], date)
    assert deserialized["date"] == stats["date"]
    assert deserialized["cycles"] == 5


@pytest.mark.asyncio
async def test_daily_stats_reset_on_new_day(mock_hass, mock_config_entry):
    """Test que les stats journalières obsolètes sont réinitialisées."""
    from datetime import date, timedelta
    
    # Créer le coordinator
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    
    # Simuler des stats d'hier
    yesterday = date.today() - timedelta(days=1)
    coordinator.daily_stats = {
        "date": yesterday,
        "cycles": 10,
        "total_energy": 20.0,
        "total_cost": 5.0,
    }
    
    # Sauvegarder
    await coordinator._save_state()
    
    # Créer un nouveau coordinator (simuler redémarrage)
    coordinator2 = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    
    # Restaurer
    await coordinator2.restore_state()
    
    # Vérifier que les stats ont été réinitialisées
    assert coordinator2.daily_stats["date"] == date.today()
    assert coordinator2.daily_stats["cycles"] == 0
    assert coordinator2.daily_stats["total_energy"] == 0.0


@pytest.mark.asyncio
async def test_monthly_stats_reset_on_new_month(mock_hass, mock_config_entry):
    """Test que les stats mensuelles obsolètes sont réinitialisées."""
    # Créer le coordinator
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    
    # Simuler des stats du mois dernier
    coordinator.monthly_stats = {
        "year": 2025,
        "month": 9,  # Septembre (on est en octobre)
        "total_energy": 100.0,
        "total_cost": 25.0,
    }
    
    # Sauvegarder
    await coordinator._save_state()
    
    # Créer un nouveau coordinator (simuler redémarrage)
    coordinator2 = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    
    # Restaurer
    await coordinator2.restore_state()
    
    # Vérifier que les stats ont été réinitialisées
    now = datetime.now()
    assert coordinator2.monthly_stats["year"] == now.year
    assert coordinator2.monthly_stats["month"] == now.month
    assert coordinator2.monthly_stats["total_energy"] == 0.0


@pytest.mark.asyncio
async def test_save_state_on_cycle_started(mock_hass, mock_config_entry):
    """Test que l'état est sauvegardé lors du démarrage d'un cycle."""
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    
    # Mock de _save_state pour vérifier qu'il est appelé
    with patch.object(coordinator, "_save_state", new=AsyncMock()) as mock_save:
        await coordinator._on_cycle_started()
        
        # Vérifier que _save_state a été appelé
        mock_save.assert_called_once()


@pytest.mark.asyncio
async def test_save_state_on_cycle_finished(mock_hass, mock_config_entry):
    """Test que l'état est sauvegardé lors de la fin d'un cycle."""
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    
    # Simuler un cycle terminé
    coordinator.state_machine.last_cycle = {
        "duration": 45.0,
        "energy": 1.2,
    }
    
    # Mock de _save_state pour vérifier qu'il est appelé
    with patch.object(coordinator, "_save_state", new=AsyncMock()) as mock_save:
        await coordinator._on_cycle_finished()
        
        # Vérifier que _save_state a été appelé
        mock_save.assert_called_once()


@pytest.mark.asyncio
async def test_periodic_save_during_running_cycle(mock_hass, mock_config_entry):
    """Test que l'état est sauvegardé périodiquement pendant un cycle en cours."""
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    
    # Simuler un cycle en cours
    coordinator.state_machine.state = STATE_RUNNING
    coordinator.state_machine.current_cycle = {
        "start_time": datetime.now(),
        "start_energy": 1.0,
        "peak_power": 150.0,
    }
    
    # Mock des capteurs
    power_state = MagicMock()
    power_state.state = "150.0"
    energy_state = MagicMock()
    energy_state.state = "2.0"
    
    mock_hass.states.get.side_effect = lambda entity_id: (
        power_state if "power" in entity_id else energy_state
    )
    
    # Mock de _save_state pour vérifier qu'il est appelé
    with patch.object(coordinator, "_save_state", new=AsyncMock()) as mock_save:
        await coordinator._async_update_data()
        
        # Vérifier que _save_state a été appelé (car état = RUNNING)
        mock_save.assert_called()


@pytest.mark.asyncio
async def test_no_periodic_save_when_idle(mock_hass, mock_config_entry):
    """Test que l'état n'est pas sauvegardé périodiquement si idle."""
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    
    # Vérifier que l'état est IDLE
    assert coordinator.state_machine.state == STATE_IDLE
    
    # Mock des capteurs
    power_state = MagicMock()
    power_state.state = "5.0"
    energy_state = MagicMock()
    energy_state.state = "10.0"
    
    mock_hass.states.get.side_effect = lambda entity_id: (
        power_state if "power" in entity_id else energy_state
    )
    
    # Mock de _save_state pour vérifier qu'il n'est PAS appelé
    with patch.object(coordinator, "_save_state", new=AsyncMock()) as mock_save:
        await coordinator._async_update_data()
        
        # Vérifier que _save_state n'a PAS été appelé (car état = IDLE)
        mock_save.assert_not_called()
