"""Module d'intégration Energy Dashboard pour Smart Appliance Monitor."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components import sensor
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import UnitOfEnergy
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er

from .const import DOMAIN
from .coordinator import SmartApplianceCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_energy_sensors(
    hass: HomeAssistant,
    coordinator: SmartApplianceCoordinator,
) -> None:
    """Configure les sensors pour qu'ils soient compatibles avec Energy Dashboard.
    
    Args:
        hass: Instance Home Assistant
        coordinator: Coordinator de l'appareil
    """
    entity_reg = er.async_get(hass)
    
    # Sensors d'énergie à configurer pour Energy Dashboard
    energy_sensors = [
        f"sensor.{coordinator.appliance_name.lower().replace(' ', '_')}_cycle_energy",
        f"sensor.{coordinator.appliance_name.lower().replace(' ', '_')}_daily_energy",
        f"sensor.{coordinator.appliance_name.lower().replace(' ', '_')}_monthly_energy",
    ]
    
    for entity_id in energy_sensors:
        entity = entity_reg.async_get(entity_id)
        if entity:
            _LOGGER.debug("Sensor énergie configuré pour Energy Dashboard: %s", entity_id)
        else:
            _LOGGER.warning("Sensor introuvable: %s", entity_id)


def is_energy_sensor_compatible(entity_id: str) -> bool:
    """Vérifie si un sensor est compatible avec Energy Dashboard.
    
    Args:
        entity_id: ID de l'entité à vérifier
        
    Returns:
        True si compatible, False sinon
    """
    return (
        entity_id.endswith("_energy") or
        entity_id.endswith("_daily_energy") or
        entity_id.endswith("_monthly_energy")
    )


async def async_get_energy_data(
    coordinator: SmartApplianceCoordinator,
) -> dict[str, Any]:
    """Récupère les données énergétiques de l'appareil.
    
    Args:
        coordinator: Coordinator de l'appareil
        
    Returns:
        Dictionnaire avec les données énergétiques
    """
    # Cycle en cours
    current_cycle_energy = 0.0
    if coordinator.state_machine.current_cycle:
        current_cycle_energy = coordinator.state_machine.current_cycle.get("energy", 0)
    
    # Dernier cycle
    last_cycle_energy = 0.0
    if coordinator.state_machine.last_cycle:
        last_cycle_energy = coordinator.state_machine.last_cycle.get("energy", 0)
    
    return {
        "current_cycle_energy_kwh": round(current_cycle_energy, 3),
        "last_cycle_energy_kwh": round(last_cycle_energy, 3),
        "daily_energy_kwh": round(coordinator.daily_stats.get("total_energy", 0), 3),
        "monthly_energy_kwh": round(coordinator.monthly_stats.get("total_energy", 0), 3),
        "daily_cost_eur": round(coordinator.daily_stats.get("total_cost", 0), 2),
        "monthly_cost_eur": round(coordinator.monthly_stats.get("total_cost", 0), 2),
        "price_kwh": coordinator.price_kwh,
    }


async def async_add_to_energy_dashboard(
    hass: HomeAssistant,
    coordinator: SmartApplianceCoordinator,
) -> dict[str, str]:
    """Fournit les informations nécessaires pour ajouter l'appareil au Energy Dashboard.
    
    Args:
        hass: Instance Home Assistant
        coordinator: Coordinator de l'appareil
        
    Returns:
        Dictionnaire avec les entity_ids et instructions
    """
    appliance_name_slug = coordinator.appliance_name.lower().replace(' ', '_')
    
    return {
        "appliance_name": coordinator.appliance_name,
        "appliance_type": coordinator.appliance_type,
        "energy_sensors": {
            "cycle_energy": f"sensor.{appliance_name_slug}_cycle_energy",
            "daily_energy": f"sensor.{appliance_name_slug}_daily_energy",
            "monthly_energy": f"sensor.{appliance_name_slug}_monthly_energy",
        },
        "cost_sensors": {
            "daily_cost": f"sensor.{appliance_name_slug}_daily_cost",
            "monthly_cost": f"sensor.{appliance_name_slug}_monthly_cost",
        },
        "instructions": {
            "fr": (
                "Pour ajouter cet appareil au Energy Dashboard:\n"
                "1. Allez dans Configuration > Tableaux de bord > Énergie\n"
                f"2. Cliquez sur 'Ajouter une consommation'\n"
                f"3. Sélectionnez le sensor: sensor.{appliance_name_slug}_daily_energy\n"
                "4. Le coût sera automatiquement calculé si vous avez configuré un prix"
            ),
            "en": (
                "To add this appliance to Energy Dashboard:\n"
                "1. Go to Configuration > Dashboards > Energy\n"
                f"2. Click 'Add Consumption'\n"
                f"3. Select sensor: sensor.{appliance_name_slug}_daily_energy\n"
                "4. Cost will be automatically calculated if you configured a price"
            ),
        },
    }


class EnergyDashboardHelper:
    """Helper class pour l'intégration Energy Dashboard."""
    
    def __init__(self, hass: HomeAssistant, coordinator: SmartApplianceCoordinator) -> None:
        """Initialise le helper.
        
        Args:
            hass: Instance Home Assistant
            coordinator: Coordinator de l'appareil
        """
        self.hass = hass
        self.coordinator = coordinator
    
    async def get_consumption_stats(self) -> dict[str, Any]:
        """Récupère les statistiques de consommation pour Energy Dashboard.
        
        Returns:
            Statistiques formatées pour Energy Dashboard
        """
        return {
            "daily": {
                "energy_kwh": round(self.coordinator.daily_stats.get("total_energy", 0), 3),
                "cost_eur": round(self.coordinator.daily_stats.get("total_cost", 0), 2),
                "cycles": self.coordinator.daily_stats.get("cycles", 0),
            },
            "monthly": {
                "energy_kwh": round(self.coordinator.monthly_stats.get("total_energy", 0), 3),
                "cost_eur": round(self.coordinator.monthly_stats.get("total_cost", 0), 2),
            },
            "current_price_kwh": self.coordinator.price_kwh,
        }
    
    def is_configured_for_energy_dashboard(self) -> bool:
        """Vérifie si l'appareil est correctement configuré pour Energy Dashboard.
        
        Returns:
            True si configuré, False sinon
        """
        # Vérifier que les sensors nécessaires existent
        appliance_name_slug = self.coordinator.appliance_name.lower().replace(' ', '_')
        required_sensors = [
            f"sensor.{appliance_name_slug}_daily_energy",
            f"sensor.{appliance_name_slug}_monthly_energy",
        ]
        
        entity_reg = er.async_get(self.hass)
        for entity_id in required_sensors:
            if not entity_reg.async_get(entity_id):
                return False
        
        return True
    
    async def get_energy_dashboard_config(self) -> dict[str, Any]:
        """Génère la configuration suggérée pour Energy Dashboard.
        
        Returns:
            Configuration Energy Dashboard
        """
        appliance_name_slug = self.coordinator.appliance_name.lower().replace(' ', '_')
        
        return {
            "type": "individual_device",
            "name": self.coordinator.appliance_name,
            "stat_energy_from": f"sensor.{appliance_name_slug}_daily_energy",
            "stat_cost": f"sensor.{appliance_name_slug}_daily_cost",
            "device_consumption": True,
            "unit_of_measurement": UnitOfEnergy.KILO_WATT_HOUR,
        }

