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
        }
    
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
