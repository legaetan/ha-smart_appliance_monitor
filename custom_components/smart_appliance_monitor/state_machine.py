"""Machine à états pour suivre les cycles d'appareils électroménagers."""
from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

from .const import (
    EVENT_CYCLE_STARTED,
    EVENT_CYCLE_FINISHED,
    EVENT_ALERT_DURATION,
    STATE_IDLE,
    STATE_RUNNING,
    STATE_FINISHED,
)

_LOGGER = logging.getLogger(__name__)


class CycleStateMachine:
    """Machine à états pour suivre les cycles d'un appareil."""

    def __init__(
        self,
        start_threshold: int,
        stop_threshold: int,
        start_delay: int,
        stop_delay: int,
        alert_duration: int | None = None,
    ) -> None:
        """Initialise la machine à états.
        
        Args:
            start_threshold: Seuil de puissance pour détecter un démarrage (W)
            stop_threshold: Seuil de puissance pour détecter un arrêt (W)
            start_delay: Délai de confirmation du démarrage (secondes)
            stop_delay: Délai de confirmation de l'arrêt (secondes)
            alert_duration: Durée maximale avant alerte (secondes, optionnel)
        """
        self.start_threshold = start_threshold
        self.stop_threshold = stop_threshold
        self.start_delay = start_delay
        self.stop_delay = stop_delay
        self.alert_duration = alert_duration
        
        self.state = STATE_IDLE
        self.current_cycle: dict[str, Any] | None = None
        self.last_cycle: dict[str, Any] | None = None
        
        self._high_power_since: datetime | None = None
        self._low_power_since: datetime | None = None
        self._alert_triggered = False
    
    def update(self, power: float, energy: float, now: datetime | None = None) -> str | None:
        """Met à jour l'état de la machine et retourne un événement si nécessaire.
        
        Args:
            power: Puissance actuelle (W)
            energy: Énergie totale consommée (kWh)
            now: Datetime actuel (optionnel, pour les tests)
            
        Returns:
            Nom de l'événement si un changement d'état se produit, None sinon
        """
        if now is None:
            now = datetime.now()
        
        event = None
        
        # État IDLE : détection du démarrage
        if self.state == STATE_IDLE:
            event = self._handle_idle_state(power, energy, now)
        
        # État RUNNING : surveillance du cycle et détection de l'arrêt
        elif self.state == STATE_RUNNING:
            event = self._handle_running_state(power, energy, now)
        
        # État FINISHED : transition automatique vers IDLE après un délai
        elif self.state == STATE_FINISHED:
            event = self._handle_finished_state(now)
        
        return event
    
    def _handle_idle_state(
        self, power: float, energy: float, now: datetime
    ) -> str | None:
        """Gère l'état IDLE et détecte le démarrage."""
        if power > self.start_threshold:
            if self._high_power_since is None:
                self._high_power_since = now
                _LOGGER.debug(
                    "Puissance élevée détectée : %.1fW > %dW. Début du délai de confirmation.",
                    power,
                    self.start_threshold,
                )
            else:
                elapsed = (now - self._high_power_since).total_seconds()
                if elapsed >= self.start_delay:
                    # Démarrage confirmé !
                    self.state = STATE_RUNNING
                    self.current_cycle = {
                        "start_time": now,
                        "start_energy": energy,
                        "peak_power": power,
                    }
                    self._high_power_since = None
                    self._alert_triggered = False
                    _LOGGER.info(
                        "Cycle démarré (puissance: %.1fW, énergie initiale: %.3f kWh)",
                        power,
                        energy,
                    )
                    return EVENT_CYCLE_STARTED
        else:
            # Réinitialisation si la puissance redescend
            if self._high_power_since is not None:
                _LOGGER.debug(
                    "Puissance redescendue avant confirmation : %.1fW. Réinitialisation.",
                    power,
                )
            self._high_power_since = None
        
        return None
    
    def _handle_running_state(
        self, power: float, energy: float, now: datetime
    ) -> str | None:
        """Gère l'état RUNNING et détecte l'arrêt ou les alertes."""
        if self.current_cycle is None:
            _LOGGER.error("État RUNNING mais current_cycle est None. Réinitialisation.")
            self.state = STATE_IDLE
            return None
        
        # Mise à jour du pic de puissance
        if power > self.current_cycle["peak_power"]:
            self.current_cycle["peak_power"] = power
        
        # Vérification de l'alerte de durée
        if (
            self.alert_duration is not None
            and not self._alert_triggered
        ):
            elapsed = (now - self.current_cycle["start_time"]).total_seconds()
            if elapsed >= self.alert_duration:
                self._alert_triggered = True
                _LOGGER.warning(
                    "Alerte : cycle en cours depuis %.0f min (seuil: %.0f min)",
                    elapsed / 60,
                    self.alert_duration / 60,
                )
                return EVENT_ALERT_DURATION
        
        # Détection de l'arrêt
        if power < self.stop_threshold:
            if self._low_power_since is None:
                self._low_power_since = now
                _LOGGER.debug(
                    "Puissance faible détectée : %.1fW < %dW. Début du délai de confirmation.",
                    power,
                    self.stop_threshold,
                )
            else:
                elapsed = (now - self._low_power_since).total_seconds()
                if elapsed >= self.stop_delay:
                    # Arrêt confirmé !
                    self.state = STATE_FINISHED
                    self.current_cycle["end_time"] = now
                    self.current_cycle["end_energy"] = energy
                    
                    # Calcul des statistiques
                    duration = (
                        self.current_cycle["end_time"] - self.current_cycle["start_time"]
                    ).total_seconds() / 60  # en minutes
                    energy_used = (
                        self.current_cycle["end_energy"] - self.current_cycle["start_energy"]
                    )
                    
                    self.current_cycle["duration"] = round(duration, 1)
                    self.current_cycle["energy"] = round(energy_used, 3)
                    
                    self.last_cycle = self.current_cycle.copy()
                    self._low_power_since = None
                    
                    _LOGGER.info(
                        "Cycle terminé (durée: %.1f min, énergie: %.3f kWh)",
                        duration,
                        energy_used,
                    )
                    return EVENT_CYCLE_FINISHED
        else:
            # Réinitialisation si la puissance remonte
            if self._low_power_since is not None:
                _LOGGER.debug(
                    "Puissance remontée avant confirmation : %.1fW. Réinitialisation.",
                    power,
                )
            self._low_power_since = None
        
        return None
    
    def _handle_finished_state(self, now: datetime) -> str | None:
        """Gère l'état FINISHED et transition vers IDLE."""
        if self.current_cycle is None:
            self.state = STATE_IDLE
            return None
        
        # Après 10 minutes, retour à IDLE
        elapsed = (now - self.current_cycle["end_time"]).total_seconds()
        if elapsed >= 600:  # 10 minutes
            _LOGGER.debug("Transition de FINISHED vers IDLE après 10 minutes")
            self.current_cycle = None
            self.state = STATE_IDLE
        
        return None
    
    def get_cycle_duration(self, now: datetime | None = None) -> float:
        """Retourne la durée du cycle en cours en minutes.
        
        Args:
            now: Datetime actuel (optionnel, pour les tests)
            
        Returns:
            Durée en minutes, 0 si pas de cycle en cours
        """
        if self.current_cycle is None or "start_time" not in self.current_cycle:
            return 0.0
        
        if now is None:
            now = datetime.now()
        
        duration = (now - self.current_cycle["start_time"]).total_seconds() / 60
        return round(duration, 1)
    
    def get_cycle_energy(self, current_energy: float) -> float:
        """Retourne l'énergie consommée pendant le cycle en cours.
        
        Args:
            current_energy: Énergie totale actuelle (kWh)
            
        Returns:
            Énergie du cycle en kWh, 0 si pas de cycle en cours
        """
        if self.current_cycle is None or "start_energy" not in self.current_cycle:
            return 0.0
        
        energy = current_energy - self.current_cycle["start_energy"]
        return round(energy, 3)
    
    def reset_statistics(self) -> None:
        """Réinitialise les statistiques du dernier cycle."""
        _LOGGER.info("Réinitialisation des statistiques")
        self.last_cycle = None

