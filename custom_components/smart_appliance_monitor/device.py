"""Gestion des devices pour Smart Appliance Monitor."""
from __future__ import annotations

from homeassistant.helpers.entity import DeviceInfo

from .const import DOMAIN


def get_device_info(entry_id: str, appliance_name: str, appliance_type: str) -> DeviceInfo:
    """Retourne les informations du device pour un appareil.
    
    Args:
        entry_id: ID de la config entry
        appliance_name: Nom de l'appareil
        appliance_type: Type d'appareil
        
    Returns:
        DeviceInfo configuré pour l'appareil
    """
    return DeviceInfo(
        identifiers={(DOMAIN, entry_id)},
        name=appliance_name,
        manufacturer="Smart Appliance Monitor",
        model=appliance_type.replace("_", " ").title(),
        sw_version="0.1.0",
        configuration_url=f"homeassistant://config/integrations/integration/{DOMAIN}",
    )


def get_appliance_icon(appliance_type: str) -> str:
    """Retourne l'icône appropriée pour un type d'appareil.
    
    Args:
        appliance_type: Type d'appareil
        
    Returns:
        Nom de l'icône MDI
    """
    icons = {
        "oven": "mdi:stove",
        "dishwasher": "mdi:dishwasher",
        "washing_machine": "mdi:washing-machine",
        "dryer": "mdi:tumble-dryer",
        "water_heater": "mdi:water-boiler",
        "coffee_maker": "mdi:coffee-maker",
        "other": "mdi:power-plug",
    }
    return icons.get(appliance_type, "mdi:power-plug")


def get_appliance_emoji(appliance_type: str) -> str:
    """Retourne l'emoji approprié pour un type d'appareil.
    
    Args:
        appliance_type: Type d'appareil
        
    Returns:
        Emoji représentant l'appareil
    """
    emojis = {
        "oven": "🔥",
        "dishwasher": "🍽️",
        "washing_machine": "🧺",
        "dryer": "👕",
        "water_heater": "💧",
        "coffee_maker": "☕",
        "other": "🔌",
    }
    return emojis.get(appliance_type, "🔌")

