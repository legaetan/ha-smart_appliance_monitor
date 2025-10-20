"""Tests pour la fonctionnalité de détection d'anomalies."""
from __future__ import annotations

from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from homeassistant.core import HomeAssistant

from custom_components.smart_appliance_monitor.coordinator import (
    SmartApplianceCoordinator,
)
from custom_components.smart_appliance_monitor.const import (
    CONF_ENABLE_ANOMALY_DETECTION,
    EVENT_ANOMALY_DETECTED,
)


@pytest.mark.asyncio
async def test_anomaly_detection_disabled_by_default(mock_hass, mock_config_entry):
    """Test que la détection d'anomalies est désactivée par défaut."""
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    
    assert coordinator.anomaly_detection_enabled is False
    assert coordinator._cycle_history == []
    assert coordinator._max_history_size == 10


@pytest.mark.asyncio
async def test_anomaly_detection_enabled(mock_hass, mock_config_entry):
    """Test l'activation de la détection d'anomalies."""
    mock_config_entry.options = {
        CONF_ENABLE_ANOMALY_DETECTION: True,
    }
    
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    
    assert coordinator.anomaly_detection_enabled is True


@pytest.mark.asyncio
async def test_cycle_history_added_on_cycle_finish(mock_hass, mock_config_entry):
    """Test que les cycles sont ajoutés à l'historique."""
    mock_config_entry.options = {
        CONF_ENABLE_ANOMALY_DETECTION: True,
    }
    
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    coordinator.monitoring_enabled = True
    
    # Simuler la fin d'un cycle
    cycle_data = {
        "start_time": datetime.now() - timedelta(minutes=60),
        "end_time": datetime.now(),
        "duration": 60.0,
        "energy": 1.5,
        "cost": 0.38,
        "peak_power": 1850,
    }
    
    coordinator._on_cycle_finished(cycle_data)
    
    assert len(coordinator._cycle_history) == 1
    assert coordinator._cycle_history[0]["duration"] == 60.0
    assert coordinator._cycle_history[0]["energy"] == 1.5


@pytest.mark.asyncio
async def test_cycle_history_limited_to_max_size(mock_hass, mock_config_entry):
    """Test que l'historique ne dépasse pas la taille maximale."""
    mock_config_entry.options = {
        CONF_ENABLE_ANOMALY_DETECTION: True,
    }
    
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    coordinator.monitoring_enabled = True
    
    # Ajouter 15 cycles (max = 10)
    for i in range(15):
        cycle_data = {
            "start_time": datetime.now() - timedelta(minutes=60),
            "end_time": datetime.now(),
            "duration": 60.0 + i,
            "energy": 1.5,
            "cost": 0.38,
            "peak_power": 1850,
        }
        coordinator._on_cycle_finished(cycle_data)
    
    # Doit contenir seulement les 10 derniers
    assert len(coordinator._cycle_history) == 10
    # Le premier élément doit être le cycle 5 (indices 5-14)
    assert coordinator._cycle_history[0]["duration"] == 65.0


@pytest.mark.asyncio
async def test_no_anomaly_with_insufficient_history(mock_hass, mock_config_entry):
    """Test qu'aucune anomalie n'est détectée avec moins de 3 cycles."""
    mock_config_entry.options = {
        CONF_ENABLE_ANOMALY_DETECTION: True,
    }
    
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    coordinator.monitoring_enabled = True
    coordinator.data = {"current_cycle": None}
    
    # Ajouter seulement 2 cycles
    for i in range(2):
        cycle_data = {
            "start_time": datetime.now() - timedelta(minutes=60),
            "end_time": datetime.now(),
            "duration": 60.0,
            "energy": 1.5,
            "cost": 0.38,
            "peak_power": 1850,
        }
        coordinator._cycle_history.append(cycle_data)
    
    # Mock des états
    power_state = MagicMock()
    power_state.state = "0.0"
    energy_state = MagicMock()
    energy_state.state = "3.0"
    
    mock_hass.states.get.side_effect = lambda entity_id: (
        power_state if "power" in entity_id else energy_state
    )
    
    # Mise à jour
    await coordinator._async_update_data()
    
    # Aucun événement d'anomalie ne doit être déclenché
    assert not any(
        call[0][0] == EVENT_ANOMALY_DETECTED 
        for call in mock_hass.bus.async_fire.call_args_list
    )


@pytest.mark.asyncio
async def test_anomaly_detected_cycle_too_long(mock_hass, mock_config_entry):
    """Test qu'une anomalie est détectée quand le cycle est trop long."""
    mock_config_entry.options = {
        CONF_ENABLE_ANOMALY_DETECTION: True,
    }
    
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    coordinator.monitoring_enabled = True
    
    # Ajouter 5 cycles normaux (60 min chacun)
    for i in range(5):
        cycle_data = {
            "start_time": datetime.now() - timedelta(minutes=60),
            "end_time": datetime.now(),
            "duration": 60.0,
            "energy": 1.5,
            "cost": 0.38,
            "peak_power": 1850,
        }
        coordinator._cycle_history.append(cycle_data)
    
    # Ajouter un cycle anormal (180 min = 3x la moyenne)
    coordinator.data = {
        "current_cycle": {
            "start_time": datetime.now() - timedelta(minutes=180),
            "duration": 180.0,
            "energy": 4.5,
        }
    }
    
    # Mock des états
    power_state = MagicMock()
    power_state.state = "100.0"
    energy_state = MagicMock()
    energy_state.state = "4.5"
    
    mock_hass.states.get.side_effect = lambda entity_id: (
        power_state if "power" in entity_id else energy_state
    )
    
    # Mise à jour
    await coordinator._async_update_data()
    
    # Un événement d'anomalie doit être déclenché
    assert any(
        call[0][0] == EVENT_ANOMALY_DETECTED 
        for call in mock_hass.bus.async_fire.call_args_list
    )


@pytest.mark.asyncio
async def test_anomaly_detected_cycle_too_short(mock_hass, mock_config_entry):
    """Test qu'une anomalie est détectée quand le cycle est trop court."""
    mock_config_entry.options = {
        CONF_ENABLE_ANOMALY_DETECTION: True,
    }
    
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    coordinator.monitoring_enabled = True
    
    # Ajouter 5 cycles normaux (60 min chacun)
    for i in range(5):
        cycle_data = {
            "start_time": datetime.now() - timedelta(minutes=60),
            "end_time": datetime.now(),
            "duration": 60.0,
            "energy": 1.5,
            "cost": 0.38,
            "peak_power": 1850,
        }
        coordinator._cycle_history.append(cycle_data)
    
    # Ajouter un cycle anormal (20 min = 1/3 de la moyenne)
    coordinator.data = {
        "current_cycle": {
            "start_time": datetime.now() - timedelta(minutes=20),
            "duration": 20.0,
            "energy": 0.5,
        }
    }
    
    # Mock des états
    power_state = MagicMock()
    power_state.state = "100.0"
    energy_state = MagicMock()
    energy_state.state = "0.5"
    
    mock_hass.states.get.side_effect = lambda entity_id: (
        power_state if "power" in entity_id else energy_state
    )
    
    # Mise à jour
    await coordinator._async_update_data()
    
    # Un événement d'anomalie doit être déclenché
    assert any(
        call[0][0] == EVENT_ANOMALY_DETECTED 
        for call in mock_hass.bus.async_fire.call_args_list
    )


@pytest.mark.asyncio
async def test_anomaly_detected_energy_too_high(mock_hass, mock_config_entry):
    """Test qu'une anomalie est détectée quand la consommation est trop élevée."""
    mock_config_entry.options = {
        CONF_ENABLE_ANOMALY_DETECTION: True,
    }
    
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    coordinator.monitoring_enabled = True
    
    # Ajouter 5 cycles normaux (1.5 kWh chacun)
    for i in range(5):
        cycle_data = {
            "start_time": datetime.now() - timedelta(minutes=60),
            "end_time": datetime.now(),
            "duration": 60.0,
            "energy": 1.5,
            "cost": 0.38,
            "peak_power": 1850,
        }
        coordinator._cycle_history.append(cycle_data)
    
    # Ajouter un cycle anormal (3.5 kWh = 2.3x la moyenne)
    coordinator.data = {
        "current_cycle": {
            "start_time": datetime.now() - timedelta(minutes=60),
            "duration": 60.0,
            "energy": 3.5,
        }
    }
    
    # Mock des états
    power_state = MagicMock()
    power_state.state = "100.0"
    energy_state = MagicMock()
    energy_state.state = "3.5"
    
    mock_hass.states.get.side_effect = lambda entity_id: (
        power_state if "power" in entity_id else energy_state
    )
    
    # Mise à jour
    await coordinator._async_update_data()
    
    # Un événement d'anomalie doit être déclenché
    assert any(
        call[0][0] == EVENT_ANOMALY_DETECTED 
        for call in mock_hass.bus.async_fire.call_args_list
    )


@pytest.mark.asyncio
async def test_anomaly_detected_energy_too_low(mock_hass, mock_config_entry):
    """Test qu'une anomalie est détectée quand la consommation est trop faible."""
    mock_config_entry.options = {
        CONF_ENABLE_ANOMALY_DETECTION: True,
    }
    
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    coordinator.monitoring_enabled = True
    
    # Ajouter 5 cycles normaux (1.5 kWh chacun)
    for i in range(5):
        cycle_data = {
            "start_time": datetime.now() - timedelta(minutes=60),
            "end_time": datetime.now(),
            "duration": 60.0,
            "energy": 1.5,
            "cost": 0.38,
            "peak_power": 1850,
        }
        coordinator._cycle_history.append(cycle_data)
    
    # Ajouter un cycle anormal (0.5 kWh = 1/3 de la moyenne)
    coordinator.data = {
        "current_cycle": {
            "start_time": datetime.now() - timedelta(minutes=60),
            "duration": 60.0,
            "energy": 0.5,
        }
    }
    
    # Mock des états
    power_state = MagicMock()
    power_state.state = "100.0"
    energy_state = MagicMock()
    energy_state.state = "0.5"
    
    mock_hass.states.get.side_effect = lambda entity_id: (
        power_state if "power" in entity_id else energy_state
    )
    
    # Mise à jour
    await coordinator._async_update_data()
    
    # Un événement d'anomalie doit être déclenché
    assert any(
        call[0][0] == EVENT_ANOMALY_DETECTED 
        for call in mock_hass.bus.async_fire.call_args_list
    )


@pytest.mark.asyncio
async def test_no_anomaly_within_normal_range(mock_hass, mock_config_entry):
    """Test qu'aucune anomalie n'est détectée pour des cycles normaux."""
    mock_config_entry.options = {
        CONF_ENABLE_ANOMALY_DETECTION: True,
    }
    
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    coordinator.monitoring_enabled = True
    
    # Ajouter 5 cycles normaux
    for i in range(5):
        cycle_data = {
            "start_time": datetime.now() - timedelta(minutes=60),
            "end_time": datetime.now(),
            "duration": 60.0,
            "energy": 1.5,
            "cost": 0.38,
            "peak_power": 1850,
        }
        coordinator._cycle_history.append(cycle_data)
    
    # Ajouter un cycle normal (légèrement différent mais dans la plage)
    coordinator.data = {
        "current_cycle": {
            "start_time": datetime.now() - timedelta(minutes=65),
            "duration": 65.0,  # +8% (dans les 50%)
            "energy": 1.6,     # +7% (dans les 50%)
        }
    }
    
    # Mock des états
    power_state = MagicMock()
    power_state.state = "100.0"
    energy_state = MagicMock()
    energy_state.state = "1.6"
    
    mock_hass.states.get.side_effect = lambda entity_id: (
        power_state if "power" in entity_id else energy_state
    )
    
    # Mise à jour
    await coordinator._async_update_data()
    
    # Aucun événement d'anomalie ne doit être déclenché
    assert not any(
        call[0][0] == EVENT_ANOMALY_DETECTED 
        for call in mock_hass.bus.async_fire.call_args_list
    )


@pytest.mark.asyncio
async def test_get_anomaly_score(mock_hass, mock_config_entry):
    """Test le calcul du score d'anomalie."""
    mock_config_entry.options = {
        CONF_ENABLE_ANOMALY_DETECTION: True,
    }
    
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    
    # Ajouter 5 cycles normaux (60 min, 1.5 kWh)
    for i in range(5):
        cycle_data = {
            "start_time": datetime.now() - timedelta(minutes=60),
            "end_time": datetime.now(),
            "duration": 60.0,
            "energy": 1.5,
            "cost": 0.38,
            "peak_power": 1850,
        }
        coordinator._cycle_history.append(cycle_data)
    
    # Cycle normal
    coordinator.data = {
        "current_cycle": {
            "start_time": datetime.now() - timedelta(minutes=60),
            "duration": 60.0,
            "energy": 1.5,
        }
    }
    score_normal = coordinator.get_anomaly_score()
    assert score_normal == 0.0  # Aucune anomalie
    
    # Cycle anormal (3x durée, 2x énergie)
    coordinator.data = {
        "current_cycle": {
            "start_time": datetime.now() - timedelta(minutes=180),
            "duration": 180.0,
            "energy": 3.0,
        }
    }
    score_anomaly = coordinator.get_anomaly_score()
    assert score_anomaly > 50.0  # Score élevé


@pytest.mark.asyncio
async def test_anomaly_detection_disabled_monitoring(mock_hass, mock_config_entry):
    """Test que la détection d'anomalies ne fonctionne pas si monitoring désactivé."""
    mock_config_entry.options = {
        CONF_ENABLE_ANOMALY_DETECTION: True,
    }
    
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    coordinator.monitoring_enabled = False  # Désactivé
    
    # Ajouter cycles et cycle anormal
    for i in range(5):
        cycle_data = {
            "start_time": datetime.now() - timedelta(minutes=60),
            "end_time": datetime.now(),
            "duration": 60.0,
            "energy": 1.5,
            "cost": 0.38,
            "peak_power": 1850,
        }
        coordinator._cycle_history.append(cycle_data)
    
    coordinator.data = {
        "current_cycle": {
            "start_time": datetime.now() - timedelta(minutes=180),
            "duration": 180.0,
            "energy": 4.5,
        }
    }
    
    # Mock des états
    power_state = MagicMock()
    power_state.state = "100.0"
    energy_state = MagicMock()
    energy_state.state = "4.5"
    
    mock_hass.states.get.side_effect = lambda entity_id: (
        power_state if "power" in entity_id else energy_state
    )
    
    # Mise à jour
    await coordinator._async_update_data()
    
    # Aucun événement ne doit être déclenché (monitoring off)
    assert not any(
        call[0][0] == EVENT_ANOMALY_DETECTED 
        for call in mock_hass.bus.async_fire.call_args_list
    )


@pytest.mark.asyncio
async def test_anomaly_score_zero_without_history(mock_hass, mock_config_entry):
    """Test que le score d'anomalie est 0 sans historique."""
    mock_config_entry.options = {
        CONF_ENABLE_ANOMALY_DETECTION: True,
    }
    
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    coordinator.data = {
        "current_cycle": {
            "start_time": datetime.now() - timedelta(minutes=180),
            "duration": 180.0,
            "energy": 10.0,
        }
    }
    
    score = coordinator.get_anomaly_score()
    assert score == 0.0  # Pas d'historique = pas d'anomalie


@pytest.mark.asyncio
async def test_multiple_anomaly_types(mock_hass, mock_config_entry):
    """Test qu'une anomalie avec plusieurs facteurs est détectée."""
    mock_config_entry.options = {
        CONF_ENABLE_ANOMALY_DETECTION: True,
    }
    
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    coordinator.monitoring_enabled = True
    
    # Ajouter 5 cycles normaux
    for i in range(5):
        cycle_data = {
            "start_time": datetime.now() - timedelta(minutes=60),
            "end_time": datetime.now(),
            "duration": 60.0,
            "energy": 1.5,
            "cost": 0.38,
            "peak_power": 1850,
        }
        coordinator._cycle_history.append(cycle_data)
    
    # Cycle anormal : trop long ET trop énergivore
    coordinator.data = {
        "current_cycle": {
            "start_time": datetime.now() - timedelta(minutes=200),
            "duration": 200.0,  # 3.3x la moyenne
            "energy": 5.0,      # 3.3x la moyenne
        }
    }
    
    # Mock des états
    power_state = MagicMock()
    power_state.state = "100.0"
    energy_state = MagicMock()
    energy_state.state = "5.0"
    
    mock_hass.states.get.side_effect = lambda entity_id: (
        power_state if "power" in entity_id else energy_state
    )
    
    # Mise à jour
    await coordinator._async_update_data()
    
    # Un événement d'anomalie doit être déclenché
    assert any(
        call[0][0] == EVENT_ANOMALY_DETECTED 
        for call in mock_hass.bus.async_fire.call_args_list
    )
    
    # Le score doit être élevé (plusieurs facteurs)
    score = coordinator.get_anomaly_score()
    assert score > 70.0

