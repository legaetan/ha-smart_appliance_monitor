"""Coordinator pour Smart Appliance Monitor."""
from __future__ import annotations

import logging
from datetime import timedelta, datetime
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.helpers.storage import Store

from .const import (
    DOMAIN,
    CONF_APPLIANCE_NAME,
    CONF_APPLIANCE_TYPE,
    CONF_POWER_SENSOR,
    CONF_ENERGY_SENSOR,
    CONF_PRICE_KWH,
    CONF_PRICE_ENTITY,
    CONF_START_THRESHOLD,
    CONF_STOP_THRESHOLD,
    CONF_START_DELAY,
    CONF_STOP_DELAY,
    CONF_ENABLE_ALERT_DURATION,
    CONF_ALERT_DURATION,
    CONF_UNPLUGGED_TIMEOUT,
    CONF_NOTIFICATION_SERVICES,
    CONF_NOTIFICATION_TYPES,
    CONF_CUSTOM_NOTIFY_SERVICE,
    CONF_ENABLE_AUTO_SHUTDOWN,
    CONF_AUTO_SHUTDOWN_DELAY,
    CONF_AUTO_SHUTDOWN_ENTITY,
    CONF_ENABLE_ENERGY_LIMITS,
    CONF_ENERGY_LIMIT_CYCLE,
    CONF_ENERGY_LIMIT_DAILY,
    CONF_ENERGY_LIMIT_MONTHLY,
    CONF_COST_BUDGET_MONTHLY,
    CONF_ENABLE_SCHEDULING,
    CONF_ALLOWED_HOURS_START,
    CONF_ALLOWED_HOURS_END,
    CONF_BLOCKED_DAYS,
    CONF_SCHEDULING_MODE,
    CONF_ENABLE_ANOMALY_DETECTION,
    APPLIANCE_PROFILES,
    DEFAULT_START_THRESHOLD,
    DEFAULT_STOP_THRESHOLD,
    DEFAULT_START_DELAY,
    DEFAULT_STOP_DELAY,
    DEFAULT_ALERT_DURATION,
    DEFAULT_UNPLUGGED_TIMEOUT,
    DEFAULT_AUTO_SHUTDOWN_DELAY,
    DEFAULT_SCHEDULING_MODE,
    DEFAULT_PRICE_KWH,
    DEFAULT_NOTIFICATION_SERVICES,
    DEFAULT_NOTIFICATION_TYPES,
    SCHEDULING_MODE_STRICT,
    STATE_IDLE,
    STATE_RUNNING,
    EVENT_CYCLE_STARTED,
    EVENT_CYCLE_FINISHED,
    EVENT_ALERT_DURATION,
    EVENT_UNPLUGGED,
    EVENT_AUTO_SHUTDOWN,
    EVENT_ENERGY_LIMIT_EXCEEDED,
    EVENT_BUDGET_EXCEEDED,
    EVENT_USAGE_OUT_OF_SCHEDULE,
    EVENT_ANOMALY_DETECTED,
    EVENT_AI_ANALYSIS_COMPLETED,
    EVENT_AI_ANALYSIS_FAILED,
    AI_TRIGGER_AUTO_CYCLE_END,
    STATE_ANALYZING,
)
from .state_machine import CycleStateMachine
from .notify import SmartApplianceNotifier

_LOGGER = logging.getLogger(__name__)

UPDATE_INTERVAL = timedelta(seconds=30)
STORAGE_VERSION = 1
STORAGE_KEY = "smart_appliance_monitor.{entry_id}"


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
        
        # Prix : entité ou valeur fixe
        self.price_entity = entry.data.get(CONF_PRICE_ENTITY)
        self.price_kwh_fixed = entry.data.get(CONF_PRICE_KWH, DEFAULT_PRICE_KWH)
        
        # Récupérer le profil de l'appareil
        profile = APPLIANCE_PROFILES.get(
            self.appliance_type, APPLIANCE_PROFILES["other"]
        )
        
        # Récupération des options (avec valeurs par défaut du profil)
        self.start_threshold = entry.options.get(
            CONF_START_THRESHOLD, profile["start_threshold"]
        )
        self.stop_threshold = entry.options.get(
            CONF_STOP_THRESHOLD, profile["stop_threshold"]
        )
        self.start_delay = entry.options.get(
            CONF_START_DELAY, profile["start_delay"]
        )
        self.stop_delay = entry.options.get(
            CONF_STOP_DELAY, profile["stop_delay"]
        )
        
        enable_alert = entry.options.get(CONF_ENABLE_ALERT_DURATION, False)
        alert_duration = entry.options.get(
            CONF_ALERT_DURATION, profile["alert_duration"]
        )
        unplugged_timeout = entry.options.get(
            CONF_UNPLUGGED_TIMEOUT, DEFAULT_UNPLUGGED_TIMEOUT
        )
        
        # Machine à états
        self.state_machine = CycleStateMachine(
            start_threshold=self.start_threshold,
            stop_threshold=self.stop_threshold,
            start_delay=self.start_delay,
            stop_delay=self.stop_delay,
            alert_duration=alert_duration if enable_alert else None,
            unplugged_timeout=unplugged_timeout,
        )
        
        # Statistiques journalières et mensuelles
        self.daily_stats: dict[str, Any] = self._init_daily_stats()
        self.monthly_stats: dict[str, Any] = self._init_monthly_stats()
        
        # Switches d'activation
        self.monitoring_enabled = True
        self.notifications_enabled = True
        
        # Options de notification
        notification_services = entry.options.get(
            CONF_NOTIFICATION_SERVICES, DEFAULT_NOTIFICATION_SERVICES
        )
        notification_types = entry.options.get(
            CONF_NOTIFICATION_TYPES, DEFAULT_NOTIFICATION_TYPES
        )
        custom_service = entry.options.get(CONF_CUSTOM_NOTIFY_SERVICE)
        
        # Système de notifications
        self.notifier = SmartApplianceNotifier(
            hass=hass,
            appliance_name=self.appliance_name,
            appliance_type=self.appliance_type,
            notification_services=notification_services,
            notification_types=notification_types,
            custom_service=custom_service,
            notifications_enabled=self.notifications_enabled,
        )
        
        # Auto-shutdown
        self.auto_shutdown_enabled = entry.options.get(CONF_ENABLE_AUTO_SHUTDOWN, False)
        self.auto_shutdown_delay = entry.options.get(CONF_AUTO_SHUTDOWN_DELAY, DEFAULT_AUTO_SHUTDOWN_DELAY)
        self.auto_shutdown_entity = entry.options.get(CONF_AUTO_SHUTDOWN_ENTITY, "")
        self._auto_shutdown_timer: datetime | None = None
        
        # Energy limits
        self.energy_limits_enabled = entry.options.get(CONF_ENABLE_ENERGY_LIMITS, False)
        self.energy_limit_cycle = entry.options.get(CONF_ENERGY_LIMIT_CYCLE, 0)
        self.energy_limit_daily = entry.options.get(CONF_ENERGY_LIMIT_DAILY, 0)
        self.energy_limit_monthly = entry.options.get(CONF_ENERGY_LIMIT_MONTHLY, 0)
        self.cost_budget_monthly = entry.options.get(CONF_COST_BUDGET_MONTHLY, 0)
        self._energy_limit_cycle_notified = False
        self._energy_limit_daily_notified = False
        self._energy_limit_monthly_notified = False
        self._budget_monthly_notified = False
        
        # Scheduling
        self.scheduling_enabled = entry.options.get(CONF_ENABLE_SCHEDULING, False)
        self.allowed_hours_start = entry.options.get(CONF_ALLOWED_HOURS_START, "00:00")
        self.allowed_hours_end = entry.options.get(CONF_ALLOWED_HOURS_END, "23:59")
        self.blocked_days = entry.options.get(CONF_BLOCKED_DAYS, [])
        self.scheduling_mode = entry.options.get(CONF_SCHEDULING_MODE, DEFAULT_SCHEDULING_MODE)
        
        # Anomaly detection
        self.anomaly_detection_enabled = entry.options.get(CONF_ENABLE_ANOMALY_DETECTION, False)
        self._cycle_history: list[dict[str, Any]] = []
        self._max_history_size = 30
        
        # AI Analysis
        self.ai_analysis_enabled = False  # Will be loaded from global config
        self.ai_analysis_trigger = "manual"  # Will be loaded from global config
        self.ai_task_entity: str | None = None  # Will be loaded from global config
        self.last_ai_analysis_result: dict[str, Any] | None = None
        
        # Storage pour la persistance
        storage_key = STORAGE_KEY.format(entry_id=entry.entry_id)
        self._store = Store(hass, STORAGE_VERSION, storage_key)
        
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
            "total_energy": 0.0,
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
                
                # Vérifications supplémentaires
                await self._check_auto_shutdown()
                await self._check_energy_limits()
                await self._check_scheduling()
                await self._check_anomaly_detection()
            
            # Mise à jour des statistiques journalières/mensuelles
            self._update_statistics()
            
            # Sauvegarde périodique de l'état (uniquement si un cycle est en cours)
            if self.state_machine.state == STATE_RUNNING:
                await self._save_state()
            
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
        elif event == EVENT_UNPLUGGED:
            await self._on_unplugged()
        elif event == EVENT_AUTO_SHUTDOWN:
            await self._on_auto_shutdown()
        elif event == EVENT_ENERGY_LIMIT_EXCEEDED:
            await self._on_energy_limit_exceeded()
        elif event == EVENT_BUDGET_EXCEEDED:
            await self._on_budget_exceeded()
        elif event == EVENT_USAGE_OUT_OF_SCHEDULE:
            await self._on_usage_out_of_schedule()
        elif event == EVENT_ANOMALY_DETECTED:
            await self._on_anomaly_detected()
    
    async def _on_cycle_started(self) -> None:
        """Appelé lorsqu'un cycle démarre."""
        _LOGGER.info("Cycle démarré pour '%s'", self.appliance_name)
        
        # Sauvegarder l'état
        await self._save_state()
        
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
        
        # Récupérer le prix actuel
        price_kwh = self._get_current_price()
        cost = energy * price_kwh
        
        _LOGGER.info(
            "Cycle terminé pour '%s' - Durée: %.1f min, Énergie: %.3f kWh, Coût: %.2f €",
            self.appliance_name,
            duration,
            energy,
            cost,
        )
        
        # Mise à jour des statistiques (avec validation pour éviter valeurs négatives)
        self.daily_stats["cycles"] += 1
        
        # Validation : si l'énergie du cycle est négative, c'est une erreur de données
        if energy < 0:
            _LOGGER.warning(
                "Énergie de cycle négative détectée (%.3f kWh) pour '%s'. "
                "Cela indique probablement un reset du compteur. Cycle ignoré dans les stats.",
                energy,
                self.appliance_name,
            )
        else:
            self.daily_stats["total_energy"] += energy
            self.daily_stats["total_cost"] += cost
            self.monthly_stats["total_energy"] += energy
            self.monthly_stats["total_cost"] += cost
        
        # Validation finale : si les totaux sont négatifs, réinitialiser
        if self.daily_stats["total_energy"] < 0:
            _LOGGER.error(
                "Total d'énergie quotidienne négatif détecté (%.3f kWh) pour '%s'. "
                "Réinitialisation des statistiques quotidiennes.",
                self.daily_stats["total_energy"],
                self.appliance_name,
            )
            self.daily_stats["total_energy"] = max(0, energy)
            self.daily_stats["total_cost"] = max(0, cost)
        
        if self.monthly_stats["total_energy"] < 0:
            _LOGGER.error(
                "Total d'énergie mensuelle négatif détecté (%.3f kWh) pour '%s'. "
                "Réinitialisation des statistiques mensuelles.",
                self.monthly_stats["total_energy"],
                self.appliance_name,
            )
            self.monthly_stats["total_energy"] = max(0, energy)
            self.monthly_stats["total_cost"] = max(0, cost)
        
        # Ajouter à l'historique des cycles (toujours, pas seulement pour la détection d'anomalies)
        self._cycle_history.append({
            "duration": duration,
            "energy": energy,
            "cost": cost,
            "timestamp": datetime.now(),
        })
        # Limiter la taille de l'historique
        if len(self._cycle_history) > self._max_history_size:
            self._cycle_history.pop(0)
        
        # Réinitialiser le timer d'auto-shutdown
        self._auto_shutdown_timer = None
        
        # Réinitialiser le flag de limite cycle
        self._energy_limit_cycle_notified = False
        
        # Émission d'un événement enrichi pour stockage Recorder
        self.hass.bus.async_fire(
            f"{DOMAIN}_cycle_finished",
            {
                "appliance_name": self.appliance_name,
                "appliance_type": self.appliance_type,
                "appliance_id": self.entry.entry_id,
                "entry_id": self.entry.entry_id,
                "duration": duration,
                "energy": energy,
                "cost": round(cost, 2),
                "peak_power": cycle.get("peak_power", 0),
                "start_time": cycle.get("start_time").isoformat() if cycle.get("start_time") else None,
                "end_time": cycle.get("end_time").isoformat() if cycle.get("end_time") else None,
                "start_energy": cycle.get("start_energy", 0),
                "end_energy": cycle.get("end_energy", 0),
            },
        )
        
        # Envoyer une notification
        await self.notifier.notify_cycle_finished(
            duration=duration,
            energy=energy,
            cost=cost,
        )
        
        # Trigger AI analysis if enabled and configured for auto-trigger on cycle end
        if (
            self.ai_analysis_enabled
            and self.ai_analysis_trigger == AI_TRIGGER_AUTO_CYCLE_END
            and self.ai_task_entity
        ):
            _LOGGER.debug(
                "Auto-triggering AI analysis for '%s' after cycle finished",
                self.appliance_name,
            )
            # Run analysis in background (don't block cycle finish)
            self.hass.async_create_task(
                self.async_trigger_ai_analysis()
            )
        
        # Sauvegarder l'état
        await self._save_state()
    
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
        threshold = self.state_machine.alert_duration / 60 if self.state_machine.alert_duration else 0
        await self.notifier.notify_alert_duration(duration=duration, threshold=threshold)
    
    async def _on_unplugged(self) -> None:
        """Appelé lorsque l'appareil est détecté comme débranché."""
        _LOGGER.warning("Appareil débranché détecté pour '%s'", self.appliance_name)
        
        # Émission d'un événement
        time_at_zero = self.state_machine.get_time_at_zero_power()
        self.hass.bus.async_fire(
            f"{DOMAIN}_unplugged",
            {
                "appliance_name": self.appliance_name,
                "appliance_type": self.appliance_type,
                "entry_id": self.entry.entry_id,
                "time_at_zero": time_at_zero,
            },
        )
        
        # Envoyer une notification
        await self.notifier.notify_unplugged(time_at_zero=time_at_zero)
    
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
    
    async def set_monitoring_enabled(self, enabled: bool) -> None:
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
        await self._save_state()
    
    async def set_notifications_enabled(self, enabled: bool) -> None:
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
        await self._save_state()
    
    def set_auto_shutdown_enabled(self, enabled: bool) -> None:
        """Active ou désactive l'extinction automatique."""
        self.auto_shutdown_enabled = enabled
        if not enabled:
            self._auto_shutdown_timer = None
    
    def set_energy_limits_enabled(self, enabled: bool) -> None:
        """Active ou désactive les limites énergétiques."""
        self.energy_limits_enabled = enabled
        if not enabled:
            self._energy_limit_cycle_notified = False
            self._energy_limit_daily_notified = False
            self._energy_limit_monthly_notified = False
            self._budget_monthly_notified = False
    
    def set_scheduling_enabled(self, enabled: bool) -> None:
        """Active ou désactive la planification."""
        self.scheduling_enabled = enabled
    
    async def set_ai_analysis_enabled(self, enabled: bool) -> None:
        """Enable or disable AI analysis.
        
        Args:
            enabled: True to enable, False to disable
        """
        _LOGGER.info(
            "AI analysis %s for '%s'",
            "enabled" if enabled else "disabled",
            self.appliance_name,
        )
        self.ai_analysis_enabled = enabled
        await self._save_state()
    
    async def load_global_ai_config(self) -> None:
        """Load AI configuration from global config."""
        global_config = self.hass.data.get(DOMAIN, {}).get("global_config")
        if not global_config:
            _LOGGER.debug("No global config found for AI analysis")
            return
        
        # Load AI Task entity
        self.ai_task_entity = global_config.get_sync("ai_task_entity")
        
        # Load AI analysis trigger
        self.ai_analysis_trigger = global_config.get_sync("ai_analysis_trigger", "manual")
        
        _LOGGER.debug(
            "Global AI config loaded for '%s': entity=%s, trigger=%s",
            self.appliance_name,
            self.ai_task_entity,
            self.ai_analysis_trigger,
        )
    
    async def async_trigger_ai_analysis(
        self,
        analysis_type: str = "all",
        cycle_count: int = 10,
    ) -> dict[str, Any] | None:
        """Trigger AI analysis for this appliance.
        
        Args:
            analysis_type: Type of analysis to perform
            cycle_count: Number of cycles to analyze
            
        Returns:
            Analysis results or None if failed
        """
        from .ai_client import SmartApplianceAIClient
        from .export import SmartApplianceDataExporter
        
        if not self.ai_task_entity:
            _LOGGER.warning(
                "Cannot trigger AI analysis for '%s': no AI Task entity configured",
                self.appliance_name,
            )
            return None
        
        try:
            _LOGGER.info(
                "Triggering AI analysis for '%s' (type: %s, cycles: %d)",
                self.appliance_name,
                analysis_type,
                cycle_count,
            )

            # Reset previous analysis result and notify sensor update
            self.last_ai_analysis_result = {
                "status": STATE_ANALYZING,
                "timestamp": datetime.now().isoformat(),
            }
            self.async_update_listeners()
            
            # Export data for AI analysis
            exporter = SmartApplianceDataExporter(self)
            export_data = exporter.export_for_ai_analysis(cycle_count=cycle_count)
            
            # Add cycle count to export data
            export_data["cycle_count_analyzed"] = cycle_count
            
            # Create AI client and analyze
            ai_client = SmartApplianceAIClient(self.hass, self.ai_task_entity)
            result = await ai_client.async_analyze_cycle_data(
                appliance_name=self.appliance_name,
                appliance_type=self.appliance_type,
                data=export_data,
                analysis_type=analysis_type,
            )
            
            # Store result
            result["cycle_count_analyzed"] = cycle_count
            self.last_ai_analysis_result = result
            
            # Save state immediately to persist the analysis result
            await self._save_state()
            
            # Fire event
            self.hass.bus.fire(
                f"{DOMAIN}_{EVENT_AI_ANALYSIS_COMPLETED}",
                {
                    "appliance_name": self.appliance_name,
                    "analysis_type": analysis_type,
                    "status": result.get("status"),
                },
            )
            
            _LOGGER.info(
                "AI analysis completed for '%s': status=%s",
                self.appliance_name,
                result.get("status"),
            )
            
            return result
            
        except Exception as err:
            _LOGGER.error(
                "AI analysis failed for '%s': %s",
                self.appliance_name,
                err,
            )
            
            # Fire error event
            self.hass.bus.fire(
                f"{DOMAIN}_{EVENT_AI_ANALYSIS_FAILED}",
                {
                    "appliance_name": self.appliance_name,
                    "error": str(err),
                },
            )
            
            return None
    
    async def _check_auto_shutdown(self) -> None:
        """Vérifie si l'appareil doit être éteint automatiquement."""
        if not self.auto_shutdown_enabled or not self.auto_shutdown_entity:
            return
        
        # Si appareil en idle, démarrer/vérifier le timer
        if self.state_machine.state == "idle":
            if self._auto_shutdown_timer is None:
                self._auto_shutdown_timer = datetime.now()
            else:
                elapsed = (datetime.now() - self._auto_shutdown_timer).total_seconds()
                if elapsed >= self.auto_shutdown_delay:
                    await self._on_auto_shutdown()
        else:
            # Réinitialiser le timer si l'appareil n'est pas idle
            self._auto_shutdown_timer = None
    
    async def _check_energy_limits(self) -> None:
        """Vérifie les limites énergétiques."""
        if not self.energy_limits_enabled:
            return
        
        # Vérifier limite du cycle en cours
        if self.energy_limit_cycle > 0 and self.state_machine.current_cycle:
            cycle_energy = self.state_machine.current_cycle.get("energy", 0)
            if cycle_energy > self.energy_limit_cycle and not self._energy_limit_cycle_notified:
                self._energy_limit_cycle_notified = True
                await self._handle_event(EVENT_ENERGY_LIMIT_EXCEEDED)
        
        # Vérifier limite journalière
        if self.energy_limit_daily > 0:
            if self.daily_stats["total_energy"] > self.energy_limit_daily and not self._energy_limit_daily_notified:
                self._energy_limit_daily_notified = True
                await self._handle_event(EVENT_ENERGY_LIMIT_EXCEEDED)
        
        # Vérifier limite mensuelle
        if self.energy_limit_monthly > 0:
            if self.monthly_stats["total_energy"] > self.energy_limit_monthly and not self._energy_limit_monthly_notified:
                self._energy_limit_monthly_notified = True
                await self._handle_event(EVENT_ENERGY_LIMIT_EXCEEDED)
        
        # Vérifier budget mensuel
        if self.cost_budget_monthly > 0:
            if self.monthly_stats["total_cost"] > self.cost_budget_monthly and not self._budget_monthly_notified:
                self._budget_monthly_notified = True
                await self._handle_event(EVENT_BUDGET_EXCEEDED)
    
    async def _check_scheduling(self) -> None:
        """Vérifie si l'utilisation est autorisée selon la planification."""
        if not self.scheduling_enabled:
            return
        
        if not self._is_usage_allowed():
            # Si l'appareil est en cours d'utilisation hors des horaires
            if self.state_machine.state == "running":
                await self._handle_event(EVENT_USAGE_OUT_OF_SCHEDULE)
    
    async def _check_anomaly_detection(self) -> None:
        """Vérifie s'il y a des anomalies dans le cycle en cours."""
        if not self.anomaly_detection_enabled or len(self._cycle_history) < 3:
            return
        
        # Vérifier seulement pendant un cycle
        if self.state_machine.state != "running" or not self.state_machine.current_cycle:
            return
        
        current_cycle = self.state_machine.current_cycle
        current_duration = current_cycle.get("duration", 0)
        current_energy = current_cycle.get("energy", 0)
        
        # Calculer moyennes de l'historique
        avg_duration = sum(c["duration"] for c in self._cycle_history) / len(self._cycle_history)
        avg_energy = sum(c["energy"] for c in self._cycle_history) / len(self._cycle_history)
        
        # Détecter anomalies
        anomaly_detected = False
        
        # Cycle trop long (>200% de la moyenne)
        if current_duration > avg_duration * 2:
            anomaly_detected = True
            _LOGGER.warning("Anomalie détectée: Cycle trop long (%.1f min vs %.1f min en moyenne)", 
                          current_duration, avg_duration)
        
        # Consommation anormale (>150% de la moyenne)
        if current_energy > avg_energy * 1.5:
            anomaly_detected = True
            _LOGGER.warning("Anomalie détectée: Consommation élevée (%.3f kWh vs %.3f kWh en moyenne)", 
                          current_energy, avg_energy)
        
        if anomaly_detected:
            await self._handle_event(EVENT_ANOMALY_DETECTED)
    
    def _is_usage_allowed(self) -> bool:
        """Vérifie si l'utilisation est autorisée selon la planification."""
        now = datetime.now()
        
        # Vérifier jour bloqué
        day_names = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        current_day = day_names[now.weekday()]
        if current_day in self.blocked_days:
            return False
        
        # Vérifier horaires
        current_time = now.time()
        try:
            start_time = datetime.strptime(self.allowed_hours_start, "%H:%M").time()
            end_time = datetime.strptime(self.allowed_hours_end, "%H:%M").time()
            
            if start_time <= end_time:
                # Plage normale (ex: 08:00 - 22:00)
                return start_time <= current_time <= end_time
            else:
                # Plage traversant minuit (ex: 22:00 - 07:00)
                return current_time >= start_time or current_time <= end_time
        except ValueError:
            _LOGGER.error("Format d'heure invalide: %s - %s", self.allowed_hours_start, self.allowed_hours_end)
            return True
    
    def get_anomaly_score(self) -> float:
        """Calcule un score d'anomalie (0-100)."""
        if not self.anomaly_detection_enabled or len(self._cycle_history) < 3:
            return 0
        
        if self.state_machine.state != "running" or not self.state_machine.current_cycle:
            return 0
        
        current_cycle = self.state_machine.current_cycle
        current_duration = current_cycle.get("duration", 0)
        current_energy = current_cycle.get("energy", 0)
        
        # Calculer moyennes
        avg_duration = sum(c["duration"] for c in self._cycle_history) / len(self._cycle_history)
        avg_energy = sum(c["energy"] for c in self._cycle_history) / len(self._cycle_history)
        
        # Calculer les écarts en pourcentage
        duration_deviation = abs(current_duration - avg_duration) / avg_duration if avg_duration > 0 else 0
        energy_deviation = abs(current_energy - avg_energy) / avg_energy if avg_energy > 0 else 0
        
        # Score basé sur les écarts (max 100)
        score = min(100, (duration_deviation + energy_deviation) * 50)
        return round(score, 1)
    
    async def _on_auto_shutdown(self) -> None:
        """Appelé lorsque l'extinction automatique se déclenche."""
        _LOGGER.info("Extinction automatique pour '%s'", self.appliance_name)
        
        # Éteindre l'appareil
        try:
            await self.hass.services.async_call(
                "homeassistant",
                "turn_off",
                {"entity_id": self.auto_shutdown_entity},
                blocking=True,
            )
            
            # Émettre un événement
            self.hass.bus.async_fire(
                f"{DOMAIN}_auto_shutdown",
                {
                    "appliance_name": self.appliance_name,
                    "appliance_type": self.appliance_type,
                    "entry_id": self.entry.entry_id,
                    "entity_id": self.auto_shutdown_entity,
                },
            )
            
            # Notification
            await self.notifier.notify_auto_shutdown(self.auto_shutdown_delay / 60)
            
        except Exception as err:
            _LOGGER.error("Erreur lors de l'extinction automatique: %s", err)
        
        # Réinitialiser le timer
        self._auto_shutdown_timer = None
    
    async def _on_energy_limit_exceeded(self) -> None:
        """Appelé lorsqu'une limite énergétique est dépassée."""
        _LOGGER.warning("Limite énergétique dépassée pour '%s'", self.appliance_name)
        
        # Émettre un événement
        self.hass.bus.async_fire(
            f"{DOMAIN}_energy_limit_exceeded",
            {
                "appliance_name": self.appliance_name,
                "appliance_type": self.appliance_type,
                "entry_id": self.entry.entry_id,
                "daily_energy": self.daily_stats["total_energy"],
                "monthly_energy": self.monthly_stats["total_energy"],
            },
        )
        
        # Notification
        await self.notifier.notify_energy_limit_exceeded(
            daily_energy=self.daily_stats["total_energy"],
            monthly_energy=self.monthly_stats["total_energy"],
        )
    
    async def _on_budget_exceeded(self) -> None:
        """Appelé lorsque le budget mensuel est dépassé."""
        _LOGGER.warning("Budget mensuel dépassé pour '%s'", self.appliance_name)
        
        # Émettre un événement
        self.hass.bus.async_fire(
            f"{DOMAIN}_budget_exceeded",
            {
                "appliance_name": self.appliance_name,
                "appliance_type": self.appliance_type,
                "entry_id": self.entry.entry_id,
                "monthly_cost": self.monthly_stats["total_cost"],
                "budget": self.cost_budget_monthly,
            },
        )
        
        # Notification
        await self.notifier.notify_budget_exceeded(
            monthly_cost=self.monthly_stats["total_cost"],
            budget=self.cost_budget_monthly,
        )
    
    async def _on_usage_out_of_schedule(self) -> None:
        """Appelé lorsque l'appareil est utilisé hors des horaires autorisés."""
        _LOGGER.warning("Utilisation hors horaire pour '%s'", self.appliance_name)
        
        # Émettre un événement
        self.hass.bus.async_fire(
            f"{DOMAIN}_usage_out_of_schedule",
            {
                "appliance_name": self.appliance_name,
                "appliance_type": self.appliance_type,
                "entry_id": self.entry.entry_id,
            },
        )
        
        # Notification
        await self.notifier.notify_usage_out_of_schedule(
            allowed_start=self.allowed_hours_start,
            allowed_end=self.allowed_hours_end,
        )
    
    async def _on_anomaly_detected(self) -> None:
        """Appelé lorsqu'une anomalie est détectée."""
        _LOGGER.warning("Anomalie détectée pour '%s'", self.appliance_name)
        
        score = self.get_anomaly_score()
        
        # Émettre un événement
        self.hass.bus.async_fire(
            f"{DOMAIN}_anomaly_detected",
            {
                "appliance_name": self.appliance_name,
                "appliance_type": self.appliance_type,
                "entry_id": self.entry.entry_id,
                "anomaly_score": score,
            },
        )
        
        # Notification
        await self.notifier.notify_anomaly_detected(score=score)
    
    def _get_current_price(self) -> float:
        """Récupère le prix actuel du kWh.
        
        Si une entité est configurée, utilise sa valeur.
        Sinon, utilise la valeur fixe configurée.
        
        Returns:
            Prix du kWh en €
        """
        if self.price_entity:
            # Récupérer la valeur depuis l'entité
            price_state = self.hass.states.get(self.price_entity)
            if price_state and price_state.state not in ["unavailable", "unknown"]:
                try:
                    return float(price_state.state)
                except (ValueError, TypeError):
                    _LOGGER.warning(
                        "Impossible de lire le prix depuis %s, utilisation de la valeur fixe",
                        self.price_entity,
                    )
        
        # Valeur fixe par défaut
        return self.price_kwh_fixed
    
    @property
    def price_kwh(self) -> float:
        """Propriété pour accéder au prix actuel."""
        return self._get_current_price()
    
    async def _save_state(self) -> None:
        """Sauvegarde l'état actuel dans le stockage persistant."""
        try:
            # Préparer les données à sauvegarder
            data = {
                "state": self.state_machine.state,
                "current_cycle": self._serialize_cycle(self.state_machine.current_cycle),
                "last_cycle": self._serialize_cycle(self.state_machine.last_cycle),
                "daily_stats": self._serialize_stats(self.daily_stats),
                "monthly_stats": self.monthly_stats,
                "cycle_history": [
                    self._serialize_cycle(cycle) for cycle in self._cycle_history
                ],
                "monitoring_enabled": self.monitoring_enabled,
                "notifications_enabled": self.notifications_enabled,
                "ai_analysis_enabled": self.ai_analysis_enabled,
                "last_ai_analysis_result": self.last_ai_analysis_result,
            }
            
            await self._store.async_save(data)
            _LOGGER.debug("État sauvegardé pour '%s'", self.appliance_name)
            
        except Exception as err:
            _LOGGER.error(
                "Erreur lors de la sauvegarde de l'état pour '%s': %s",
                self.appliance_name,
                err,
            )
    
    async def restore_state(self) -> None:
        """Restaure l'état depuis le stockage persistant."""
        try:
            data = await self._store.async_load()
            
            if data is None:
                _LOGGER.debug(
                    "Aucun état sauvegardé trouvé pour '%s'",
                    self.appliance_name,
                )
                return
            
            # Restaurer l'état de la machine à états
            self.state_machine.state = data.get("state", STATE_IDLE)
            self.state_machine.current_cycle = self._deserialize_cycle(
                data.get("current_cycle")
            )
            self.state_machine.last_cycle = self._deserialize_cycle(
                data.get("last_cycle")
            )
            
            # Restaurer les statistiques journalières
            saved_daily_stats = data.get("daily_stats")
            if saved_daily_stats:
                # Vérifier si c'est toujours le même jour
                saved_date = datetime.fromisoformat(saved_daily_stats["date"]).date()
                if saved_date == datetime.now().date():
                    self.daily_stats = self._deserialize_stats(saved_daily_stats)
                    # Validation : corriger les valeurs négatives
                    if self.daily_stats.get("total_energy", 0) < 0:
                        _LOGGER.warning(
                            "Énergie quotidienne négative détectée lors de la restauration "
                            "(%.3f kWh) pour '%s'. Réinitialisation à 0.",
                            self.daily_stats["total_energy"],
                            self.appliance_name,
                        )
                        self.daily_stats["total_energy"] = 0.0
                        self.daily_stats["total_cost"] = 0.0
                else:
                    _LOGGER.debug(
                        "Stats journalières obsolètes (date: %s), réinitialisation",
                        saved_date,
                    )
            
            # Restaurer les statistiques mensuelles
            saved_monthly_stats = data.get("monthly_stats")
            if saved_monthly_stats:
                # Vérifier si c'est toujours le même mois
                now = datetime.now()
                if (
                    saved_monthly_stats["year"] == now.year
                    and saved_monthly_stats["month"] == now.month
                ):
                    self.monthly_stats = saved_monthly_stats
                    # Validation : corriger les valeurs négatives
                    if self.monthly_stats.get("total_energy", 0) < 0:
                        _LOGGER.warning(
                            "Énergie mensuelle négative détectée lors de la restauration "
                            "(%.3f kWh) pour '%s'. Réinitialisation à 0.",
                            self.monthly_stats["total_energy"],
                            self.appliance_name,
                        )
                        self.monthly_stats["total_energy"] = 0.0
                        self.monthly_stats["total_cost"] = 0.0
                else:
                    _LOGGER.debug(
                        "Stats mensuelles obsolètes (mois: %s/%s), réinitialisation",
                        saved_monthly_stats["month"],
                        saved_monthly_stats["year"],
                    )
            
            # Restaurer l'historique des cycles
            saved_history = data.get("cycle_history", [])
            self._cycle_history = [
                self._deserialize_cycle(cycle) for cycle in saved_history
            ]
            
            # Restaurer les switches
            self.monitoring_enabled = data.get("monitoring_enabled", True)
            self.notifications_enabled = data.get("notifications_enabled", True)
            self.ai_analysis_enabled = data.get("ai_analysis_enabled", False)
            self.notifier.set_enabled(self.notifications_enabled)
            
            # Restaurer les résultats d'analyse AI
            self.last_ai_analysis_result = data.get("last_ai_analysis_result", None)
            
            _LOGGER.info(
                "État restauré pour '%s' - État: %s, Cycle en cours: %s",
                self.appliance_name,
                self.state_machine.state,
                "Oui" if self.state_machine.current_cycle else "Non",
            )
            
        except Exception as err:
            _LOGGER.error(
                "Erreur lors de la restauration de l'état pour '%s': %s",
                self.appliance_name,
                err,
            )
    
    def _serialize_cycle(self, cycle: dict[str, Any] | None) -> dict[str, Any] | None:
        """Sérialise un cycle pour le stockage JSON."""
        if cycle is None:
            return None
        
        serialized = cycle.copy()
        
        # Convertir les datetime en ISO format
        for key in ["start_time", "end_time", "timestamp"]:
            if key in serialized and isinstance(serialized[key], datetime):
                serialized[key] = serialized[key].isoformat()
        
        return serialized
    
    def _deserialize_cycle(self, cycle: dict[str, Any] | None) -> dict[str, Any] | None:
        """Désérialise un cycle depuis le stockage JSON."""
        if cycle is None:
            return None
        
        deserialized = cycle.copy()
        
        # Convertir les chaînes ISO en datetime
        for key in ["start_time", "end_time", "timestamp"]:
            if key in deserialized and isinstance(deserialized[key], str):
                try:
                    deserialized[key] = datetime.fromisoformat(deserialized[key])
                except (ValueError, TypeError):
                    _LOGGER.warning(
                        "Impossible de désérialiser la date '%s': %s",
                        key,
                        deserialized[key],
                    )
        
        return deserialized
    
    def _serialize_stats(self, stats: dict[str, Any]) -> dict[str, Any]:
        """Sérialise les statistiques pour le stockage JSON."""
        serialized = stats.copy()
        
        # Convertir la date en ISO format
        if "date" in serialized:
            serialized["date"] = serialized["date"].isoformat()
        
        return serialized
    
    def _deserialize_stats(self, stats: dict[str, Any]) -> dict[str, Any]:
        """Désérialise les statistiques depuis le stockage JSON."""
        deserialized = stats.copy()
        
        # Convertir la chaîne ISO en date
        if "date" in deserialized and isinstance(deserialized["date"], str):
            try:
                deserialized["date"] = datetime.fromisoformat(
                    deserialized["date"]
                ).date()
            except (ValueError, TypeError):
                _LOGGER.warning(
                    "Impossible de désérialiser la date: %s",
                    deserialized["date"],
                )
                deserialized["date"] = datetime.now().date()
        
        return deserialized

