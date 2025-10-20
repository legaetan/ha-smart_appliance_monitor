"""Coordinator pour Smart Appliance Monitor."""
from __future__ import annotations

import logging
from datetime import timedelta, datetime
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    DOMAIN,
    CONF_APPLIANCE_NAME,
    CONF_APPLIANCE_TYPE,
    CONF_POWER_SENSOR,
    CONF_ENERGY_SENSOR,
    CONF_PRICE_KWH,
    CONF_START_THRESHOLD,
    CONF_STOP_THRESHOLD,
    CONF_START_DELAY,
    CONF_STOP_DELAY,
    CONF_ENABLE_ALERT_DURATION,
    CONF_ALERT_DURATION,
    DEFAULT_START_THRESHOLD,
    DEFAULT_STOP_THRESHOLD,
    DEFAULT_START_DELAY,
    DEFAULT_STOP_DELAY,
    DEFAULT_ALERT_DURATION,
    EVENT_CYCLE_STARTED,
    EVENT_CYCLE_FINISHED,
    EVENT_ALERT_DURATION,
)
from .state_machine import CycleStateMachine
from .notify import SmartApplianceNotifier

_LOGGER = logging.getLogger(__name__)

UPDATE_INTERVAL = timedelta(seconds=30)


class SmartApplianceCoordinator(DataUpdateCoordinator):
    """Coordonne les mises à jour de données pour un appareil."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialise le coordinator.
        
        Args:
            hass: Instance Home Assistant
            entry: Config entry de l'intégration
        """
        self.entry = entry
        self.appliance_name = entry.data[CONF_APPLIANCE_NAME]
        self.appliance_type = entry.data[CONF_APPLIANCE_TYPE]
        self.power_sensor = entry.data[CONF_POWER_SENSOR]
        self.energy_sensor = entry.data[CONF_ENERGY_SENSOR]
        self.price_kwh = entry.data[CONF_PRICE_KWH]
        
        # Récupération des options (avec valeurs par défaut)
        self.start_threshold = entry.options.get(
            CONF_START_THRESHOLD, DEFAULT_START_THRESHOLD
        )
        self.stop_threshold = entry.options.get(
            CONF_STOP_THRESHOLD, DEFAULT_STOP_THRESHOLD
        )
        self.start_delay = entry.options.get(CONF_START_DELAY, DEFAULT_START_DELAY)
        self.stop_delay = entry.options.get(CONF_STOP_DELAY, DEFAULT_STOP_DELAY)
        
        enable_alert = entry.options.get(CONF_ENABLE_ALERT_DURATION, False)
        alert_duration = entry.options.get(CONF_ALERT_DURATION, DEFAULT_ALERT_DURATION)
        
        # Machine à états
        self.state_machine = CycleStateMachine(
            start_threshold=self.start_threshold,
            stop_threshold=self.stop_threshold,
            start_delay=self.start_delay,
            stop_delay=self.stop_delay,
            alert_duration=alert_duration if enable_alert else None,
        )
        
        # Statistiques journalières et mensuelles
        self.daily_stats: dict[str, Any] = self._init_daily_stats()
        self.monthly_stats: dict[str, Any] = self._init_monthly_stats()
        
        # Switches d'activation
        self.monitoring_enabled = True
        self.notifications_enabled = True
        
        # Système de notifications
        self.notifier = SmartApplianceNotifier(
            hass=hass,
            appliance_name=self.appliance_name,
            appliance_type=self.appliance_type,
            notifications_enabled=self.notifications_enabled,
        )
        
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_{entry.entry_id}",
            update_interval=UPDATE_INTERVAL,
        )
        
        _LOGGER.info(
            "Coordinator initialisé pour '%s' (type: %s)",
            self.appliance_name,
            self.appliance_type,
        )
    
    def _init_daily_stats(self) -> dict[str, Any]:
        """Initialise les statistiques journalières."""
        return {
            "date": datetime.now().date(),
            "cycles": 0,
            "total_energy": 0.0,
            "total_cost": 0.0,
        }
    
    def _init_monthly_stats(self) -> dict[str, Any]:
        """Initialise les statistiques mensuelles."""
        now = datetime.now()
        return {
            "year": now.year,
            "month": now.month,
            "total_cost": 0.0,
        }
    
    async def _async_update_data(self) -> dict[str, Any]:
        """Récupère les dernières données des capteurs.
        
        Returns:
            Dictionnaire contenant l'état actuel de l'appareil
            
        Raises:
            UpdateFailed: Si la récupération des données échoue
        """
        try:
            # Récupération de la puissance
            power_state = self.hass.states.get(self.power_sensor)
            if power_state is None:
                raise UpdateFailed(f"Capteur de puissance '{self.power_sensor}' non disponible")
            
            try:
                power = float(power_state.state)
            except (ValueError, TypeError):
                _LOGGER.warning(
                    "Valeur de puissance invalide: %s. Utilisation de 0.",
                    power_state.state,
                )
                power = 0.0
            
            # Récupération de l'énergie
            energy_state = self.hass.states.get(self.energy_sensor)
            if energy_state is None:
                raise UpdateFailed(f"Capteur d'énergie '{self.energy_sensor}' non disponible")
            
            try:
                energy = float(energy_state.state)
            except (ValueError, TypeError):
                _LOGGER.warning(
                    "Valeur d'énergie invalide: %s. Utilisation de 0.",
                    energy_state.state,
                )
                energy = 0.0
            
            # Mise à jour de la machine à états (seulement si la surveillance est activée)
            event = None
            if self.monitoring_enabled:
                event = self.state_machine.update(power, energy)
                
                # Gestion des événements
                if event:
                    await self._handle_event(event)
            
            # Mise à jour des statistiques journalières/mensuelles
            self._update_statistics()
            
            # Construction des données de retour
            data = {
                "power": power,
                "energy": energy,
                "state": self.state_machine.state,
                "current_cycle": self.state_machine.current_cycle,
                "last_cycle": self.state_machine.last_cycle,
                "daily_stats": self.daily_stats,
                "monthly_stats": self.monthly_stats,
                "monitoring_enabled": self.monitoring_enabled,
                "notifications_enabled": self.notifications_enabled,
            }
            
            return data
            
        except UpdateFailed:
            raise
        except Exception as err:
            raise UpdateFailed(f"Erreur lors de la mise à jour des données: {err}") from err
    
    async def _handle_event(self, event: str) -> None:
        """Gère les événements émis par la machine à états.
        
        Args:
            event: Nom de l'événement (EVENT_CYCLE_STARTED, etc.)
        """
        _LOGGER.info("Événement reçu: %s", event)
        
        if event == EVENT_CYCLE_STARTED:
            await self._on_cycle_started()
        elif event == EVENT_CYCLE_FINISHED:
            await self._on_cycle_finished()
        elif event == EVENT_ALERT_DURATION:
            await self._on_alert_duration()
    
    async def _on_cycle_started(self) -> None:
        """Appelé lorsqu'un cycle démarre."""
        _LOGGER.info("Cycle démarré pour '%s'", self.appliance_name)
        
        # Émettre un événement Home Assistant
        self.hass.bus.async_fire(
            f"{DOMAIN}_cycle_started",
            {
                "appliance_name": self.appliance_name,
                "appliance_type": self.appliance_type,
                "entry_id": self.entry.entry_id,
            },
        )
        
        # Envoyer une notification
        await self.notifier.notify_cycle_started()
    
    async def _on_cycle_finished(self) -> None:
        """Appelé lorsqu'un cycle se termine."""
        if self.state_machine.last_cycle is None:
            return
        
        cycle = self.state_machine.last_cycle
        duration = cycle.get("duration", 0)
        energy = cycle.get("energy", 0)
        cost = energy * self.price_kwh
        
        _LOGGER.info(
            "Cycle terminé pour '%s' - Durée: %.1f min, Énergie: %.3f kWh, Coût: %.2f €",
            self.appliance_name,
            duration,
            energy,
            cost,
        )
        
        # Mise à jour des statistiques
        self.daily_stats["cycles"] += 1
        self.daily_stats["total_energy"] += energy
        self.daily_stats["total_cost"] += cost
        self.monthly_stats["total_cost"] += cost
        
        # Émission d'un événement
        self.hass.bus.async_fire(
            f"{DOMAIN}_cycle_finished",
            {
                "appliance_name": self.appliance_name,
                "appliance_type": self.appliance_type,
                "entry_id": self.entry.entry_id,
                "duration": duration,
                "energy": energy,
                "cost": round(cost, 2),
            },
        )
        
        # Envoyer une notification
        await self.notifier.notify_cycle_finished(
            duration=duration,
            energy=energy,
            cost=cost,
        )
    
    async def _on_alert_duration(self) -> None:
        """Appelé lorsqu'une alerte de durée est déclenchée."""
        _LOGGER.warning("Alerte de durée pour '%s'", self.appliance_name)
        
        # Émission d'un événement
        self.hass.bus.async_fire(
            f"{DOMAIN}_alert_duration",
            {
                "appliance_name": self.appliance_name,
                "appliance_type": self.appliance_type,
                "entry_id": self.entry.entry_id,
            },
        )
        
        # Envoyer une notification d'alerte
        duration = self.state_machine.get_cycle_duration()
        await self.notifier.notify_alert_duration(duration=duration)
    
    def _update_statistics(self) -> None:
        """Met à jour les statistiques journalières et mensuelles."""
        now = datetime.now()
        
        # Réinitialisation des stats journalières si nouvelle journée
        if now.date() != self.daily_stats["date"]:
            _LOGGER.debug("Nouvelle journée détectée, réinitialisation des stats journalières")
            self.daily_stats = self._init_daily_stats()
        
        # Réinitialisation des stats mensuelles si nouveau mois
        if now.year != self.monthly_stats["year"] or now.month != self.monthly_stats["month"]:
            _LOGGER.debug("Nouveau mois détecté, réinitialisation des stats mensuelles")
            self.monthly_stats = self._init_monthly_stats()
    
    def reset_statistics(self) -> None:
        """Réinitialise toutes les statistiques."""
        _LOGGER.info("Réinitialisation des statistiques pour '%s'", self.appliance_name)
        self.state_machine.reset_statistics()
        self.daily_stats = self._init_daily_stats()
        self.monthly_stats = self._init_monthly_stats()
    
    def set_monitoring_enabled(self, enabled: bool) -> None:
        """Active ou désactive la surveillance.
        
        Args:
            enabled: True pour activer, False pour désactiver
        """
        _LOGGER.info(
            "Surveillance %s pour '%s'",
            "activée" if enabled else "désactivée",
            self.appliance_name,
        )
        self.monitoring_enabled = enabled
    
    def set_notifications_enabled(self, enabled: bool) -> None:
        """Active ou désactive les notifications.
        
        Args:
            enabled: True pour activer, False pour désactiver
        """
        _LOGGER.info(
            "Notifications %s pour '%s'",
            "activées" if enabled else "désactivées",
            self.appliance_name,
        )
        self.notifications_enabled = enabled
        self.notifier.set_enabled(enabled)

