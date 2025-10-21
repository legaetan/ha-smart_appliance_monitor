"""Système de notifications avancé pour Smart Appliance Monitor."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.core import HomeAssistant

from .const import (
    NOTIF_SERVICE_MOBILE_APP,
    NOTIF_SERVICE_TELEGRAM,
    NOTIF_SERVICE_PERSISTENT,
    NOTIF_SERVICE_CUSTOM,
    NOTIF_TYPE_CYCLE_STARTED,
    NOTIF_TYPE_CYCLE_FINISHED,
    NOTIF_TYPE_ALERT_DURATION,
    NOTIF_TYPE_UNPLUGGED,
    NOTIF_TYPE_AUTO_SHUTDOWN,
    NOTIF_TYPE_ENERGY_LIMIT,
    NOTIF_TYPE_BUDGET,
    NOTIF_TYPE_SCHEDULE,
    NOTIF_TYPE_ANOMALY,
    NOTIF_TYPE_AI_ANALYSIS,
)
from .device import get_appliance_emoji

_LOGGER = logging.getLogger(__name__)


class SmartApplianceNotifier:
    """Gestionnaire de notifications avancé pour un appareil."""

    def __init__(
        self,
        hass: HomeAssistant,
        appliance_name: str,
        appliance_type: str,
        notification_services: list[str] | None = None,
        notification_types: list[str] | None = None,
        custom_service: str | None = None,
        notifications_enabled: bool = True,
    ) -> None:
        """Initialise le notifier.
        
        Args:
            hass: Instance Home Assistant
            appliance_name: Nom de l'appareil
            appliance_type: Type d'appareil
            notification_services: Liste des services de notification à utiliser
            notification_types: Liste des types de notifications actives
            custom_service: Nom du service personnalisé (si utilisé)
            notifications_enabled: Si les notifications sont activées globalement
        """
        self.hass = hass
        self.appliance_name = appliance_name
        self.appliance_type = appliance_type
        self.notifications_enabled = notifications_enabled
        
        # Services et types de notifications
        self.notification_services = notification_services or [NOTIF_SERVICE_MOBILE_APP, NOTIF_SERVICE_PERSISTENT]
        self.notification_types = notification_types or [
            NOTIF_TYPE_CYCLE_STARTED,
            NOTIF_TYPE_CYCLE_FINISHED,
            NOTIF_TYPE_ALERT_DURATION,
            NOTIF_TYPE_UNPLUGGED,
        ]
        self.custom_service = custom_service
        
        # État des switches individuels (initialisés à True, seront mis à jour par les switches)
        self.notification_type_switches = {
            NOTIF_TYPE_CYCLE_STARTED: True,
            NOTIF_TYPE_CYCLE_FINISHED: True,
            NOTIF_TYPE_ALERT_DURATION: True,
            NOTIF_TYPE_UNPLUGGED: True,
            NOTIF_TYPE_AUTO_SHUTDOWN: True,
            NOTIF_TYPE_ENERGY_LIMIT: True,
            NOTIF_TYPE_BUDGET: True,
            NOTIF_TYPE_SCHEDULE: True,
            NOTIF_TYPE_ANOMALY: True,
            NOTIF_TYPE_AI_ANALYSIS: True,
        }
    
    def set_enabled(self, enabled: bool) -> None:
        """Active ou désactive toutes les notifications globalement.
        
        Args:
            enabled: Si activé ou non
        """
        self.notifications_enabled = enabled
        _LOGGER.debug(
            "Notifications %s pour '%s'",
            "activées" if enabled else "désactivées",
            self.appliance_name,
        )
    
    def set_notification_type_enabled(self, notif_type: str, enabled: bool) -> None:
        """Active ou désactive un type de notification via switch.
        
        Args:
            notif_type: Type de notification
            enabled: Si activé ou non
        """
        self.notification_type_switches[notif_type] = enabled
        _LOGGER.debug(
            "Type de notification '%s' %s pour '%s'",
            notif_type,
            "activé" if enabled else "désactivé",
            self.appliance_name,
        )
    
    def _is_notification_type_enabled(self, notif_type: str) -> bool:
        """Vérifie si un type de notification est activé.
        
        Args:
            notif_type: Type de notification à vérifier
            
        Returns:
            True si le type est activé, False sinon
        """
        # Vérifier le switch global
        if not self.notifications_enabled:
            return False
        
        # Vérifier si le type est dans la liste configurée
        if notif_type not in self.notification_types:
            return False
        
        # Vérifier le switch individuel
        if not self.notification_type_switches.get(notif_type, True):
            return False
        
        return True
    
    async def notify_cycle_started(self) -> None:
        """Envoie une notification lorsqu'un cycle démarre."""
        if not self._is_notification_type_enabled(NOTIF_TYPE_CYCLE_STARTED):
            _LOGGER.debug("Notifications de démarrage désactivées pour '%s'", self.appliance_name)
            return
        
        emoji = get_appliance_emoji(self.appliance_type)
        title = f"{emoji} {self.appliance_name} démarré"
        message = f"Le {self.appliance_name.lower()} vient de démarrer."
        
        await self._send_notification(
            notif_type=NOTIF_TYPE_CYCLE_STARTED,
            title=title,
            message=message,
            data={
                "notification_icon": "mdi:play-circle",
                "color": "#2196F3",
                "tag": f"smart_appliance_{self.appliance_name.lower()}_started",
            },
        )
        
        _LOGGER.info("Notification de démarrage envoyée pour '%s'", self.appliance_name)
    
    async def notify_cycle_finished(
        self,
        duration: float,
        energy: float,
        cost: float,
    ) -> None:
        """Envoie une notification lorsqu'un cycle se termine.
        
        Args:
            duration: Durée du cycle en minutes
            energy: Énergie consommée en kWh
            cost: Coût en €
        """
        if not self._is_notification_type_enabled(NOTIF_TYPE_CYCLE_FINISHED):
            _LOGGER.debug("Notifications de fin désactivées pour '%s'", self.appliance_name)
            return
        
        emoji = get_appliance_emoji(self.appliance_type)
        
        # Formater la durée
        if duration < 60:
            duration_str = f"{int(duration)} min"
        else:
            hours = int(duration / 60)
            minutes = int(duration % 60)
            duration_str = f"{hours}h{minutes:02d}"
        
        # Formater l'énergie
        if energy < 1:
            energy_str = f"{int(energy * 1000)} Wh"
        else:
            energy_str = f"{energy:.2f} kWh"
        
        title = f"✅ {self.appliance_name} terminé"
        message = (
            f"Le {self.appliance_name.lower()} a terminé son cycle.\n\n"
            f"📊 Durée : {duration_str}\n"
            f"⚡ Consommation : {energy_str}\n"
            f"💰 Coût : {cost:.2f} €"
        )
        
        await self._send_notification(
            notif_type=NOTIF_TYPE_CYCLE_FINISHED,
            title=title,
            message=message,
            data={
                "notification_icon": "mdi:check-circle",
                "color": "#4CAF50",
                "tag": f"smart_appliance_{self.appliance_name.lower()}_finished",
                "duration": duration,
                "energy": energy,
                "cost": cost,
            },
        )
        
        _LOGGER.info(
            "Notification de fin envoyée pour '%s' (durée: %.1f min, coût: %.2f €)",
            self.appliance_name,
            duration,
            cost,
        )
    
    async def notify_alert_duration(self, duration: float, threshold: float) -> None:
        """Envoie une notification d'alerte de durée.
        
        Args:
            duration: Durée actuelle en minutes
            threshold: Seuil d'alerte en minutes
        """
        if not self._is_notification_type_enabled(NOTIF_TYPE_ALERT_DURATION):
            _LOGGER.debug("Notifications d'alerte désactivées pour '%s'", self.appliance_name)
            return
        
        emoji = get_appliance_emoji(self.appliance_type)
        
        title = f"⏰ {self.appliance_name} - Alerte durée"
        message = (
            f"Le {self.appliance_name.lower()} fonctionne depuis longtemps.\n\n"
            f"⏱️ Durée actuelle : {int(duration)} min\n"
            f"🔔 Seuil d'alerte : {int(threshold)} min"
        )
        
        await self._send_notification(
            notif_type=NOTIF_TYPE_ALERT_DURATION,
            title=title,
            message=message,
            data={
                "notification_icon": "mdi:timer-alert",
                "color": "#FF9800",
                "tag": f"smart_appliance_{self.appliance_name.lower()}_alert",
                "duration": duration,
                "threshold": threshold,
            },
        )
        
        _LOGGER.warning(
            "Notification d'alerte envoyée pour '%s' (durée: %.0f min)",
            self.appliance_name,
            duration,
        )
    
    async def notify_unplugged(self, time_at_zero: float) -> None:
        """Envoie une notification lorsque l'appareil est détecté comme débranché.
        
        Args:
            time_at_zero: Temps passé à 0W en secondes
        """
        if not self._is_notification_type_enabled(NOTIF_TYPE_UNPLUGGED):
            _LOGGER.debug("Notifications de débranchement désactivées pour '%s'", self.appliance_name)
            return
        
        emoji = get_appliance_emoji(self.appliance_type)
        
        time_minutes = int(time_at_zero / 60)
        
        title = f"🔌 {self.appliance_name} - Débranché"
        message = (
            f"Le {self.appliance_name.lower()} semble être débranché ou éteint.\n\n"
            f"⚠️ Aucune consommation détectée depuis {time_minutes} minutes.\n"
            f"Vérifiez l'alimentation de l'appareil."
        )
        
        await self._send_notification(
            notif_type=NOTIF_TYPE_UNPLUGGED,
            title=title,
            message=message,
            data={
                "notification_icon": "mdi:power-plug-off",
                "color": "#F44336",
                "tag": f"smart_appliance_{self.appliance_name.lower()}_unplugged",
                "time_at_zero": time_at_zero,
            },
        )
        
        _LOGGER.warning(
            "Notification de débranchement envoyée pour '%s' (0W depuis %.0f secondes)",
            self.appliance_name,
            time_at_zero,
        )
    
    async def notify_auto_shutdown(self, delay_minutes: float) -> None:
        """Envoie une notification lorsque l'extinction automatique se déclenche.
        
        Args:
            delay_minutes: Délai d'inactivité en minutes
        """
        if not self._is_notification_type_enabled(NOTIF_TYPE_AUTO_SHUTDOWN):
            _LOGGER.debug("Notifications d'auto-shutdown désactivées pour '%s'", self.appliance_name)
            return
        
        title = f"💤 {self.appliance_name} - Extinction automatique"
        message = (
            f"Le {self.appliance_name.lower()} a été éteint automatiquement.\n\n"
            f"⏱️ Inactif depuis {int(delay_minutes)} minutes."
        )
        
        await self._send_notification(
            notif_type=NOTIF_TYPE_AUTO_SHUTDOWN,
            title=title,
            message=message,
            data={
                "notification_icon": "mdi:power-sleep",
                "color": "#9C27B0",
                "tag": f"smart_appliance_{self.appliance_name.lower()}_shutdown",
                "delay_minutes": delay_minutes,
            },
        )
        
        _LOGGER.info("Notification d'extinction automatique envoyée pour '%s'", self.appliance_name)
    
    async def notify_energy_limit_exceeded(self, daily_energy: float, monthly_energy: float) -> None:
        """Envoie une notification lorsqu'une limite énergétique est dépassée.
        
        Args:
            daily_energy: Énergie journalière en kWh
            monthly_energy: Énergie mensuelle en kWh
        """
        if not self._is_notification_type_enabled(NOTIF_TYPE_ENERGY_LIMIT):
            _LOGGER.debug("Notifications de limite énergétique désactivées pour '%s'", self.appliance_name)
            return
        
        title = f"⚡ {self.appliance_name} - Limite énergétique"
        message = (
            f"Le {self.appliance_name.lower()} a dépassé une limite énergétique.\n\n"
            f"📊 Aujourd'hui : {daily_energy:.2f} kWh\n"
            f"📅 Ce mois : {monthly_energy:.2f} kWh"
        )
        
        await self._send_notification(
            notif_type=NOTIF_TYPE_ENERGY_LIMIT,
            title=title,
            message=message,
            data={
                "notification_icon": "mdi:gauge-full",
                "color": "#FF5722",
                "tag": f"smart_appliance_{self.appliance_name.lower()}_energy_limit",
                "daily_energy": daily_energy,
                "monthly_energy": monthly_energy,
            },
        )
        
        _LOGGER.warning("Notification de limite énergétique envoyée pour '%s'", self.appliance_name)
    
    async def notify_budget_exceeded(self, monthly_cost: float, budget: float) -> None:
        """Envoie une notification lorsque le budget mensuel est dépassé.
        
        Args:
            monthly_cost: Coût mensuel actuel en €
            budget: Budget mensuel configuré en €
        """
        if not self._is_notification_type_enabled(NOTIF_TYPE_BUDGET):
            _LOGGER.debug("Notifications de budget désactivées pour '%s'", self.appliance_name)
            return
        
        title = f"💰 {self.appliance_name} - Budget dépassé"
        message = (
            f"Le {self.appliance_name.lower()} a dépassé son budget mensuel.\n\n"
            f"💸 Coût actuel : {monthly_cost:.2f} €\n"
            f"🎯 Budget : {budget:.2f} €\n"
            f"📈 Dépassement : {monthly_cost - budget:.2f} €"
        )
        
        await self._send_notification(
            notif_type=NOTIF_TYPE_BUDGET,
            title=title,
            message=message,
            data={
                "notification_icon": "mdi:cash-remove",
                "color": "#F44336",
                "tag": f"smart_appliance_{self.appliance_name.lower()}_budget",
                "monthly_cost": monthly_cost,
                "budget": budget,
            },
        )
        
        _LOGGER.warning("Notification de budget dépassé envoyée pour '%s'", self.appliance_name)
    
    async def notify_usage_out_of_schedule(self, allowed_start: str, allowed_end: str) -> None:
        """Envoie une notification lorsque l'appareil est utilisé hors horaires.
        
        Args:
            allowed_start: Heure de début autorisée (HH:MM)
            allowed_end: Heure de fin autorisée (HH:MM)
        """
        if not self._is_notification_type_enabled(NOTIF_TYPE_SCHEDULE):
            _LOGGER.debug("Notifications de planification désactivées pour '%s'", self.appliance_name)
            return
        
        title = f"🕐 {self.appliance_name} - Hors horaire"
        message = (
            f"Le {self.appliance_name.lower()} est utilisé en dehors des horaires autorisés.\n\n"
            f"⏰ Plage autorisée : {allowed_start} - {allowed_end}"
        )
        
        await self._send_notification(
            notif_type=NOTIF_TYPE_SCHEDULE,
            title=title,
            message=message,
            data={
                "notification_icon": "mdi:calendar-remove",
                "color": "#FF9800",
                "tag": f"smart_appliance_{self.appliance_name.lower()}_schedule",
                "allowed_start": allowed_start,
                "allowed_end": allowed_end,
            },
        )
        
        _LOGGER.warning("Notification hors horaire envoyée pour '%s'", self.appliance_name)
    
    async def notify_anomaly_detected(self, score: float) -> None:
        """Envoie une notification lorsqu'une anomalie est détectée.
        
        Args:
            score: Score d'anomalie (0-100)
        """
        if not self._is_notification_type_enabled(NOTIF_TYPE_ANOMALY):
            _LOGGER.debug("Notifications d'anomalie désactivées pour '%s'", self.appliance_name)
            return
        
        title = f"⚠️ {self.appliance_name} - Anomalie détectée"
        message = (
            f"Une anomalie a été détectée sur le {self.appliance_name.lower()}.\n\n"
            f"📊 Score d'anomalie : {score:.1f}/100\n"
            f"Vérifiez le fonctionnement de l'appareil."
        )
        
        await self._send_notification(
            notif_type=NOTIF_TYPE_ANOMALY,
            title=title,
            message=message,
            data={
                "notification_icon": "mdi:alert-circle",
                "color": "#E91E63",
                "tag": f"smart_appliance_{self.appliance_name.lower()}_anomaly",
                "anomaly_score": score,
            },
        )
        
        _LOGGER.warning("Notification d'anomalie envoyée pour '%s' (score: %.1f)", self.appliance_name, score)
    
    async def notify_ai_analysis(self, result: dict[str, Any]) -> None:
        """Send notification for AI analysis results.
        
        Args:
            result: AI analysis results dictionary
        """
        if not self._is_notification_type_enabled(NOTIF_TYPE_AI_ANALYSIS):
            _LOGGER.debug("AI analysis notifications disabled for '%s'", self.appliance_name)
            return
        
        status = result.get("status", "unknown")
        summary = result.get("summary", "Analysis completed")
        recommendations = result.get("recommendations", [])
        savings_kwh = result.get("energy_savings_kwh", 0)
        savings_eur = result.get("energy_savings_eur", 0)
        
        # Icon based on status
        if status == "optimized":
            icon = "mdi:brain-check"
            status_emoji = "✅"
            color = "#4CAF50"
        elif status == "needs_improvement":
            icon = "mdi:brain-alert"
            status_emoji = "⚠️"
            color = "#FF9800"
        else:
            icon = "mdi:brain"
            status_emoji = "ℹ️"
            color = "#2196F3"
        
        title = f"🤖 AI Analysis - {self.appliance_name}"
        
        # Build message
        message_parts = [
            f"{status_emoji} Status: {status.replace('_', ' ').title()}",
            "",
            f"📝 {summary}",
        ]
        
        if savings_kwh > 0 or savings_eur > 0:
            message_parts.append("")
            message_parts.append("💡 Potential Savings:")
            if savings_kwh > 0:
                message_parts.append(f"  • Energy: {savings_kwh:.2f} kWh")
            if savings_eur > 0:
                message_parts.append(f"  • Cost: {savings_eur:.2f} €")
        
        if recommendations:
            message_parts.append("")
            message_parts.append("📋 Top Recommendations:")
            for i, rec in enumerate(recommendations[:3], 1):  # Top 3 only
                message_parts.append(f"  {i}. {rec}")
        
        message = "\n".join(message_parts)
        
        await self._send_notification(
            notif_type=NOTIF_TYPE_AI_ANALYSIS,
            title=title,
            message=message,
            data={
                "notification_icon": icon,
                "color": color,
                "tag": f"smart_appliance_{self.appliance_name.lower()}_ai_analysis",
                "status": status,
                "savings_kwh": savings_kwh,
                "savings_eur": savings_eur,
                "actions": [
                    {
                        "action": "VIEW_DETAILS",
                        "title": "View Details",
                    },
                    {
                        "action": "REANALYZE",
                        "title": "Re-analyze",
                    },
                ],
            },
        )
        
        _LOGGER.info("AI analysis notification sent for '%s' (status: %s)", self.appliance_name, status)
    
    async def _send_notification(
        self,
        notif_type: str,
        title: str,
        message: str,
        data: dict[str, Any],
    ) -> None:
        """Envoie une notification via tous les services configurés.
        
        Args:
            notif_type: Type de notification
            title: Titre de la notification
            message: Message de la notification
            data: Données additionnelles
        """
        # Envoyer vers chaque service configuré
        for service in self.notification_services:
            try:
                if service == NOTIF_SERVICE_MOBILE_APP:
                    await self._send_mobile_app(title, message, data)
                elif service == NOTIF_SERVICE_TELEGRAM:
                    await self._send_telegram(title, message, data)
                elif service == NOTIF_SERVICE_PERSISTENT:
                    await self._send_persistent(title, message)
                elif service == NOTIF_SERVICE_CUSTOM and self.custom_service:
                    await self._send_custom(title, message, data)
            except Exception as err:
                _LOGGER.error(
                    "Erreur lors de l'envoi de la notification via %s: %s",
                    service,
                    err,
                )
    
    async def _send_mobile_app(
        self,
        title: str,
        message: str,
        data: dict[str, Any],
    ) -> None:
        """Envoie une notification via mobile_app.
        
        Args:
            title: Titre
            message: Message
            data: Données additionnelles
        """
        # Essayer de trouver un service mobile_app disponible
        services = self.hass.services.async_services()
        notify_services = services.get("notify", {})
        
        # Chercher les services mobile_app_*
        mobile_services = [
            service_name
            for service_name in notify_services.keys()
            if service_name.startswith("mobile_app_")
        ]
        
        if not mobile_services:
            _LOGGER.warning("Aucun service mobile_app trouvé")
            return
        
        # Utiliser le premier service mobile trouvé
        service_name = mobile_services[0]
        
        await self.hass.services.async_call(
            "notify",
            service_name,
            {
                "title": title,
                "message": message,
                "data": data,
            },
        )
        
        _LOGGER.debug("Notification envoyée via %s", service_name)
    
    async def _send_telegram(
        self,
        title: str,
        message: str,
        data: dict[str, Any],
    ) -> None:
        """Envoie une notification via Telegram.
        
        Args:
            title: Titre
            message: Message
            data: Données additionnelles
        """
        # Vérifier si le service telegram_bot existe
        if not self.hass.services.has_service("telegram_bot", "send_message"):
            _LOGGER.warning("Service telegram_bot.send_message non disponible")
            return
        
        # Formatter en markdown pour Telegram
        formatted_message = f"*{title}*\n\n{message}"
        
        await self.hass.services.async_call(
            "telegram_bot",
            "send_message",
            {
                "message": formatted_message,
                "parse_mode": "markdown",
            },
        )
        
        _LOGGER.debug("Notification envoyée via Telegram")
    
    async def _send_persistent(self, title: str, message: str) -> None:
        """Envoie une notification persistante.
        
        Args:
            title: Titre
            message: Message
        """
        await self.hass.services.async_call(
            "persistent_notification",
            "create",
            {
                "title": title,
                "message": message,
                "notification_id": f"smart_appliance_{self.appliance_name.lower()}",
            },
        )
        
        _LOGGER.debug("Notification persistante créée")
    
    async def _send_custom(
        self,
        title: str,
        message: str,
        data: dict[str, Any],
    ) -> None:
        """Envoie une notification via un service personnalisé.
        
        Args:
            title: Titre
            message: Message
            data: Données additionnelles
        """
        if not self.custom_service:
            return
        
        # Extraire domaine et service
        if "." in self.custom_service:
            domain, service = self.custom_service.split(".", 1)
        else:
            domain = "notify"
            service = self.custom_service
        
        # Vérifier si le service existe
        if not self.hass.services.has_service(domain, service):
            _LOGGER.warning(
                "Service personnalisé %s.%s non disponible",
                domain,
                service,
            )
            return
        
        await self.hass.services.async_call(
            domain,
            service,
            {
                "title": title,
                "message": message,
                "data": data,
            },
        )
        
        _LOGGER.debug("Notification envoyée via %s.%s", domain, service)
