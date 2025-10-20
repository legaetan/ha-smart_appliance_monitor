"""Tests pour la machine à états."""
from __future__ import annotations

from datetime import datetime, timedelta

import pytest

from custom_components.smart_appliance_monitor.state_machine import CycleStateMachine
from custom_components.smart_appliance_monitor.const import (
    EVENT_CYCLE_STARTED,
    EVENT_CYCLE_FINISHED,
    EVENT_ALERT_DURATION,
    STATE_IDLE,
    STATE_RUNNING,
    STATE_FINISHED,
)


@pytest.fixture
def state_machine():
    """Fixture pour créer une machine à états."""
    return CycleStateMachine(
        start_threshold=50,
        stop_threshold=5,
        start_delay=120,  # 2 minutes
        stop_delay=300,   # 5 minutes
        alert_duration=7200,  # 2 heures
    )


def test_initial_state(state_machine):
    """Test l'état initial de la machine."""
    assert state_machine.state == STATE_IDLE
    assert state_machine.current_cycle is None
    assert state_machine.last_cycle is None


def test_no_start_with_low_power(state_machine):
    """Test qu'un cycle ne démarre pas avec une puissance faible."""
    now = datetime(2025, 10, 20, 18, 30, 0)
    
    # Puissance faible
    event = state_machine.update(10, 0.0, now)
    
    assert event is None
    assert state_machine.state == STATE_IDLE
    assert state_machine.current_cycle is None


def test_start_requires_confirmation_delay(state_machine):
    """Test que le démarrage nécessite un délai de confirmation."""
    now = datetime(2025, 10, 20, 18, 30, 0)
    
    # Puissance élevée mais durée insuffisante
    event = state_machine.update(100, 0.0, now)
    assert event is None
    assert state_machine.state == STATE_IDLE
    
    # Après 1 minute (< 2 minutes requises)
    event = state_machine.update(100, 0.1, now + timedelta(seconds=60))
    assert event is None
    assert state_machine.state == STATE_IDLE
    
    # Après 2 minutes → démarrage confirmé
    event = state_machine.update(100, 0.2, now + timedelta(seconds=120))
    assert event == EVENT_CYCLE_STARTED
    assert state_machine.state == STATE_RUNNING
    assert state_machine.current_cycle is not None


def test_start_cancelled_if_power_drops(state_machine):
    """Test que le démarrage est annulé si la puissance redescend."""
    now = datetime(2025, 10, 20, 18, 30, 0)
    
    # Puissance élevée
    event = state_machine.update(100, 0.0, now)
    assert event is None
    assert state_machine._high_power_since is not None
    
    # Puissance qui redescend avant le délai
    event = state_machine.update(10, 0.0, now + timedelta(seconds=60))
    assert event is None
    assert state_machine.state == STATE_IDLE
    assert state_machine._high_power_since is None


def test_cycle_start_detection(state_machine):
    """Test la détection complète du démarrage d'un cycle."""
    now = datetime(2025, 10, 20, 18, 30, 0)
    
    # Démarrer un cycle
    state_machine.update(100, 1.0, now)
    event = state_machine.update(100, 1.1, now + timedelta(seconds=120))
    
    assert event == EVENT_CYCLE_STARTED
    assert state_machine.state == STATE_RUNNING
    assert state_machine.current_cycle["start_time"] == now + timedelta(seconds=120)
    assert state_machine.current_cycle["start_energy"] == 1.1
    assert state_machine.current_cycle["peak_power"] == 100


def test_peak_power_tracking(state_machine):
    """Test le suivi du pic de puissance pendant un cycle."""
    now = datetime(2025, 10, 20, 18, 30, 0)
    
    # Démarrer un cycle
    state_machine.update(100, 1.0, now)
    state_machine.update(100, 1.1, now + timedelta(seconds=120))
    
    assert state_machine.current_cycle["peak_power"] == 100
    
    # Puissance augmente
    state_machine.update(150, 1.2, now + timedelta(seconds=180))
    assert state_machine.current_cycle["peak_power"] == 150
    
    # Puissance redescend (le pic reste)
    state_machine.update(80, 1.3, now + timedelta(seconds=240))
    assert state_machine.current_cycle["peak_power"] == 150


def test_stop_requires_confirmation_delay(state_machine):
    """Test que l'arrêt nécessite un délai de confirmation."""
    now = datetime(2025, 10, 20, 18, 30, 0)
    
    # Démarrer un cycle
    state_machine.update(100, 1.0, now)
    state_machine.update(100, 1.1, now + timedelta(seconds=120))
    
    # Puissance faible mais durée insuffisante
    event = state_machine.update(3, 2.0, now + timedelta(minutes=10))
    assert event is None
    assert state_machine.state == STATE_RUNNING
    
    # Après 5 minutes → arrêt confirmé
    event = state_machine.update(3, 2.5, now + timedelta(minutes=15))
    assert event == EVENT_CYCLE_FINISHED
    assert state_machine.state == STATE_FINISHED


def test_stop_cancelled_if_power_rises(state_machine):
    """Test que l'arrêt est annulé si la puissance remonte."""
    now = datetime(2025, 10, 20, 18, 30, 0)
    
    # Démarrer un cycle
    state_machine.update(100, 1.0, now)
    state_machine.update(100, 1.1, now + timedelta(seconds=120))
    
    # Puissance faible
    state_machine.update(3, 2.0, now + timedelta(minutes=10))
    assert state_machine._low_power_since is not None
    
    # Puissance remonte avant le délai
    event = state_machine.update(100, 2.1, now + timedelta(minutes=12))
    assert event is None
    assert state_machine.state == STATE_RUNNING
    assert state_machine._low_power_since is None


def test_cycle_end_detection(state_machine):
    """Test la détection complète de l'arrêt d'un cycle."""
    now = datetime(2025, 10, 20, 18, 30, 0)
    
    # Démarrer un cycle
    state_machine.update(100, 1.0, now)
    state_machine.update(100, 1.1, now + timedelta(seconds=120))
    
    # Terminer le cycle
    state_machine.update(3, 2.0, now + timedelta(minutes=10))
    event = state_machine.update(3, 2.5, now + timedelta(minutes=15))
    
    assert event == EVENT_CYCLE_FINISHED
    assert state_machine.state == STATE_FINISHED
    assert state_machine.last_cycle is not None
    
    # Vérifier les statistiques calculées
    last_cycle = state_machine.last_cycle
    assert "duration" in last_cycle
    assert "energy" in last_cycle
    assert last_cycle["duration"] == pytest.approx(13.0, abs=0.1)  # 15 - 2 = 13 min
    assert last_cycle["energy"] == pytest.approx(1.4, abs=0.01)  # 2.5 - 1.1 = 1.4 kWh


def test_alert_duration(state_machine):
    """Test l'alerte de durée excessive."""
    now = datetime(2025, 10, 20, 18, 30, 0)
    
    # Démarrer un cycle
    state_machine.update(100, 1.0, now)
    state_machine.update(100, 1.1, now + timedelta(seconds=120))
    
    # Avant l'alerte (< 2h)
    event = state_machine.update(100, 2.0, now + timedelta(hours=1))
    assert event is None
    
    # Après 2h → alerte déclenchée
    event = state_machine.update(100, 3.0, now + timedelta(hours=2, seconds=120))
    assert event == EVENT_ALERT_DURATION
    assert state_machine.state == STATE_RUNNING
    
    # L'alerte ne doit se déclencher qu'une seule fois
    event = state_machine.update(100, 3.5, now + timedelta(hours=3))
    assert event is None


def test_alert_duration_disabled(state_machine):
    """Test qu'aucune alerte n'est déclenchée si désactivée."""
    # Créer une machine sans alerte
    sm = CycleStateMachine(
        start_threshold=50,
        stop_threshold=5,
        start_delay=120,
        stop_delay=300,
        alert_duration=None,  # Désactivé
    )
    
    now = datetime(2025, 10, 20, 18, 30, 0)
    
    # Démarrer un cycle
    sm.update(100, 1.0, now)
    sm.update(100, 1.1, now + timedelta(seconds=120))
    
    # Après 5 heures (bien au-delà de 2h)
    event = sm.update(100, 5.0, now + timedelta(hours=5))
    assert event is None  # Pas d'alerte


def test_finished_to_idle_transition(state_machine):
    """Test la transition de FINISHED vers IDLE après 10 minutes."""
    now = datetime(2025, 10, 20, 18, 30, 0)
    
    # Démarrer et terminer un cycle
    state_machine.update(100, 1.0, now)
    state_machine.update(100, 1.1, now + timedelta(seconds=120))
    state_machine.update(3, 2.0, now + timedelta(minutes=10))
    state_machine.update(3, 2.5, now + timedelta(minutes=15))
    
    assert state_machine.state == STATE_FINISHED
    
    # Après 5 minutes (< 10 minutes)
    event = state_machine.update(3, 2.5, now + timedelta(minutes=20))
    assert event is None
    assert state_machine.state == STATE_FINISHED
    
    # Après 10 minutes → retour à IDLE
    event = state_machine.update(3, 2.5, now + timedelta(minutes=25))
    assert event is None
    assert state_machine.state == STATE_IDLE
    assert state_machine.current_cycle is None
    assert state_machine.last_cycle is not None  # Conservé


def test_get_cycle_duration(state_machine):
    """Test le calcul de la durée du cycle en cours."""
    now = datetime(2025, 10, 20, 18, 30, 0)
    
    # Pas de cycle en cours
    assert state_machine.get_cycle_duration(now) == 0.0
    
    # Démarrer un cycle
    state_machine.update(100, 1.0, now)
    state_machine.update(100, 1.1, now + timedelta(seconds=120))
    
    # Après 10 minutes
    duration = state_machine.get_cycle_duration(now + timedelta(minutes=12))
    assert duration == pytest.approx(10.0, abs=0.1)


def test_get_cycle_energy(state_machine):
    """Test le calcul de l'énergie du cycle en cours."""
    now = datetime(2025, 10, 20, 18, 30, 0)
    
    # Pas de cycle en cours
    assert state_machine.get_cycle_energy(1.0) == 0.0
    
    # Démarrer un cycle
    state_machine.update(100, 1.0, now)
    state_machine.update(100, 1.1, now + timedelta(seconds=120))
    
    # Énergie consommée
    energy = state_machine.get_cycle_energy(2.5)
    assert energy == pytest.approx(1.4, abs=0.01)  # 2.5 - 1.1


def test_reset_statistics(state_machine):
    """Test la réinitialisation des statistiques."""
    now = datetime(2025, 10, 20, 18, 30, 0)
    
    # Créer un historique
    state_machine.update(100, 1.0, now)
    state_machine.update(100, 1.1, now + timedelta(seconds=120))
    state_machine.update(3, 2.0, now + timedelta(minutes=10))
    state_machine.update(3, 2.5, now + timedelta(minutes=15))
    
    assert state_machine.last_cycle is not None
    
    # Réinitialiser
    state_machine.reset_statistics()
    
    assert state_machine.last_cycle is None

