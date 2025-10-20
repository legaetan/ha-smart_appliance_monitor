"""Système de notifications pour Smart Appliance Monitor."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.core import HomeAssistant

from .device import get_appliance_emoji

_LOGGER = logging.getLogger(__name__)


class SmartApplianceNotifier:
    """Gestionnaire de notifications pour un appareil."""

    def __init__(
        self,
        hass: HomeAssistant,
        appliance_name: str,
        appliance_type: str,
        notifications_enabled: bool = True,
    ) -> None:
        """Initialise le notifier.
        
        Args:
            hass: Instance Home Assistant
            appliance_name: Nom de l'appareil
            appliance_type: Type d'appareil
            notifications_enabled: Si les notifications sont activées
        """
        self.hass = hass
        self.appliance_name = appliance_name
        self.appliance_type = appliance_type
        self.notifications_enabled = notifications_enabled
    
    async def notify_cycle_started(self) -> None:
        """Envoie une notification lorsqu'un cycle démarre."""
        if not self.notifications_enabled:
            _LOGGER.debug("Notifications désactivées, notification de démarrage ignorée")
            return
        
        emoji = get_appliance_emoji(self.appliance_type)
        
        message = f"Le {self.appliance_name.lower()} vient de démarrer."
        
        await self._send_notification(
            title=f"{emoji} {self.appliance_name} démarré",
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
        if not self.notifications_enabled:
            _LOGGER.debug("Notifications désactivées, notification de fin ignorée")
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
        
        message = (
            f"Le {self.appliance_name.lower()} a terminé son cycle.\n\n"
            f"📊 Durée : {duration_str}\n"
            f"⚡ Consommation : {energy_str}\n"
            f"💰 Coût : {cost:.2f} €"
        )
        
        await self._send_notification(
            title=f"✅ {self.appliance_name} terminé",
            message=message,
            data={
                "notification_icon": "mdi:check-circle",
                "color": "#4CAF50",
                "tag": f"smart_appliance_{self.appliance_name.lower()}_finished",
                "actions": [
                    {
                        "action": f"VIEW_STATS_{self.appliance_name.upper()}",
                        "title": "Voir statistiques",
                    },
                    {
                        "action": "DISMISS",
                        "title": "OK",
                    },
                ],
            },
        )
        
        _LOGGER.info(
            "Notification de fin envoyée pour '%s' (durée: %.1f min, coût: %.2f €)",
            self.appliance_name,
            duration,
            cost,
        )
    
    async def notify_alert_duration(self, duration: float) -> None:
        """Envoie une alerte si le cycle dure trop longtemps.
        
        Args:
            duration: Durée actuelle du cycle en minutes
        """
        if not self.notifications_enabled:
            _LOGGER.debug("Notifications désactivées, alerte de durée ignorée")
            return
        
        emoji = get_appliance_emoji(self.appliance_type)
        
        # Formater la durée
        hours = int(duration / 60)
        minutes = int(duration % 60)
        duration_str = f"{hours}h{minutes:02d}"
        
        message = (
            f"⚠️ Le {self.appliance_name.lower()} fonctionne depuis {duration_str}.\n\n"
            f"Cela semble anormalement long. Vérifiez que tout va bien."
        )
        
        await self._send_notification(
            title=f"{emoji} Alerte durée - {self.appliance_name}",
            message=message,
            data={
                "notification_icon": "mdi:alert",
                "color": "#FF9800",
                "tag": f"smart_appliance_{self.appliance_name.lower()}_alert",
                "sticky": True,
                "actions": [
                    {
                        "action": f"STOP_{self.appliance_name.upper()}",
                        "title": "Arrêter la surveillance",
                    },
                    {
                        "action": "DISMISS",
                        "title": "Ignorer",
                    },
                ],
            },
        )
        
        _LOGGER.warning(
            "Alerte de durée envoyée pour '%s' (durée: %.1f min)",
            self.appliance_name,
            duration,
        )
    
    async def _send_notification(
        self,
        title: str,
        message: str,
        data: dict[str, Any] | None = None,
    ) -> None:
        """Envoie une notification via le service notify.
        
        Args:
            title: Titre de la notification
            message: Message de la notification
            data: Données supplémentaires pour la notification
        """
        if data is None:
            data = {}
        
        notification_data = {
            "title": title,
            "message": message,
            "data": data,
        }
        
        try:
            # Essayer d'abord avec notify.mobile_app (si configuré)
            if self.hass.services.has_service("notify", "mobile_app"):
                await self.hass.services.async_call(
                    "notify",
                    "mobile_app",
                    notification_data,
                )
            # Sinon utiliser notify.notify (notification persistante dans HA)
            else:
                await self.hass.services.async_call(
                    "notify",
                    "persistent_notification",
                    {
                        "title": title,
                        "message": message,
                    },
                )
        except Exception as err:
            _LOGGER.error(
                "Erreur lors de l'envoi de la notification pour '%s': %s",
                self.appliance_name,
                err,
            )
    
    def set_enabled(self, enabled: bool) -> None:
        """Active ou désactive les notifications.
        
        Args:
            enabled: True pour activer, False pour désactiver
        """
        self.notifications_enabled = enabled
        _LOGGER.debug(
            "Notifications %s pour '%s'",
            "activées" if enabled else "désactivées",
            self.appliance_name,
        )

