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
from .energy_storage import EnergyStorageReader, EnergyStorageError

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


class EnergyDashboardSync:
    """Synchronization handler between SAM and Energy Dashboard."""
    
    def __init__(
        self,
        hass: HomeAssistant,
        coordinator: SmartApplianceCoordinator,
    ) -> None:
        """Initialize the sync handler.
        
        Args:
            hass: Home Assistant instance
            coordinator: Appliance coordinator
        """
        self.hass = hass
        self.coordinator = coordinator
        self.storage_reader = EnergyStorageReader(hass)
    
    async def get_sync_status(self) -> dict[str, Any]:
        """Get synchronization status for this appliance.
        
        Returns:
            Dict with sync status and details
        """
        appliance_name_slug = self.coordinator.appliance_name.lower().replace(' ', '_')
        daily_energy_sensor = f"sensor.{appliance_name_slug}_daily_energy"
        
        try:
            # Check if sensor is in Energy Dashboard
            device_config = await self.storage_reader.find_device_by_sensor(
                daily_energy_sensor
            )
            
            if device_config:
                status = "synced"
                message = f"Appliance '{self.coordinator.appliance_name}' is configured in Energy Dashboard"
                
                # Check if it's included in another stat
                parent_stat = device_config.get("included_in_stat")
                if parent_stat:
                    message += f" (included in {parent_stat})"
                
            else:
                status = "not_configured"
                message = f"Appliance '{self.coordinator.appliance_name}' is NOT in Energy Dashboard"
            
            return {
                "status": status,
                "message": message,
                "appliance_name": self.coordinator.appliance_name,
                "energy_sensor": daily_energy_sensor,
                "dashboard_config": device_config,
            }
            
        except EnergyStorageError as err:
            _LOGGER.warning("Cannot read energy storage: %s", err)
            return {
                "status": "error",
                "message": f"Cannot read Energy Dashboard configuration: {err}",
                "appliance_name": self.coordinator.appliance_name,
                "energy_sensor": daily_energy_sensor,
                "dashboard_config": None,
            }
    
    async def suggest_energy_config(self) -> dict[str, Any]:
        """Generate suggested configuration for Energy Dashboard.
        
        Returns:
            Configuration ready to be added to Energy Dashboard
        """
        appliance_name_slug = self.coordinator.appliance_name.lower().replace(' ', '_')
        
        config = {
            "stat_consumption": f"sensor.{appliance_name_slug}_daily_energy",
            "name": self.coordinator.appliance_name,
        }
        
        # Try to find a parent sensor if this is a sub-device
        # For example, if bureau_energy exists and contains this device
        try:
            devices = await self.storage_reader.get_device_consumption()
            
            # Look for potential parent sensors
            # This is a heuristic: check if there's a sensor that might be a parent
            # based on naming (e.g., "bureau_energy" for "lumiere_bureau_energy")
            potential_parents = []
            for device in devices:
                parent_sensor = device.get("stat_consumption", "")
                # Extract base name (remove sensor. prefix)
                if parent_sensor.startswith("sensor."):
                    parent_base = parent_sensor.replace("sensor.", "").replace("_energy", "")
                    appliance_base = appliance_name_slug.replace("_energy", "")
                    
                    # Check if appliance name contains parent name
                    if parent_base in appliance_base and parent_base != appliance_base:
                        potential_parents.append(parent_sensor)
            
            if potential_parents:
                # Suggest the first potential parent
                config["included_in_stat"] = potential_parents[0]
                _LOGGER.info(
                    "Suggested parent sensor for %s: %s",
                    self.coordinator.appliance_name,
                    potential_parents[0]
                )
        
        except EnergyStorageError:
            pass  # No parent suggestion if can't read storage
        
        return config
    
    async def find_similar_devices(self) -> list[dict[str, Any]]:
        """Find devices in Energy Dashboard that could use SAM monitoring.
        
        Returns:
            List of similar devices that are candidates for SAM
        """
        try:
            devices = await self.storage_reader.get_device_consumption()
            similar = []
            
            for device in devices:
                sensor = device.get("stat_consumption", "")
                name = device.get("name", "")
                
                # Skip if this is already a SAM device
                # SAM sensors typically follow pattern: sensor.{name}_daily_energy
                if not sensor or not sensor.endswith("_energy"):
                    continue
                
                # Extract potential appliance name
                # sensor.refrigerateur_energie -> refrigerateur
                base_name = sensor.replace("sensor.", "").replace("_energie", "").replace("_energy", "")
                
                # This device could benefit from SAM monitoring
                similar.append({
                    "sensor": sensor,
                    "name": name or base_name.replace("_", " ").title(),
                    "dashboard_config": device,
                    "suggestion": f"Consider adding '{name or base_name}' to Smart Appliance Monitor",
                })
            
            return similar
            
        except EnergyStorageError as err:
            _LOGGER.warning("Cannot find similar devices: %s", err)
            return []
    
    async def generate_sync_report(self) -> dict[str, Any]:
        """Generate comprehensive sync report.
        
        Returns:
            Complete sync report with status and recommendations
        """
        sync_status = await self.get_sync_status()
        suggested_config = await self.suggest_energy_config()
        similar_devices = await self.find_similar_devices()
        
        return {
            "appliance": {
                "name": self.coordinator.appliance_name,
                "type": self.coordinator.appliance_type,
            },
            "sync_status": sync_status,
            "suggested_config": suggested_config,
            "similar_devices": similar_devices,
            "instructions": await self._get_instructions(sync_status["status"]),
        }
    
    async def _get_instructions(self, status: str) -> dict[str, str]:
        """Get user instructions based on sync status.
        
        Args:
            status: Current sync status
            
        Returns:
            Instructions in English and French
        """
        appliance_name_slug = self.coordinator.appliance_name.lower().replace(' ', '_')
        sensor = f"sensor.{appliance_name_slug}_daily_energy"
        
        if status == "synced":
            return {
                "en": f"✅ {self.coordinator.appliance_name} is already configured in Energy Dashboard.",
                "fr": f"✅ {self.coordinator.appliance_name} est déjà configuré dans le tableau de bord Énergie.",
            }
        elif status == "not_configured":
            return {
                "en": (
                    f"⚠️ {self.coordinator.appliance_name} is NOT in Energy Dashboard.\n\n"
                    "To add it:\n"
                    "1. Go to Settings → Dashboards → Energy\n"
                    "2. Click 'Add Consumption'\n"
                    f"3. Select sensor: {sensor}\n"
                    "4. Save\n\n"
                    f"Or use the service: smart_appliance_monitor.export_energy_config"
                ),
                "fr": (
                    f"⚠️ {self.coordinator.appliance_name} n'est PAS dans le tableau de bord Énergie.\n\n"
                    "Pour l'ajouter :\n"
                    "1. Allez dans Paramètres → Tableaux de bord → Énergie\n"
                    "2. Cliquez sur 'Ajouter une consommation'\n"
                    f"3. Sélectionnez le capteur : {sensor}\n"
                    "4. Enregistrez\n\n"
                    f"Ou utilisez le service : smart_appliance_monitor.export_energy_config"
                ),
            }
        else:  # error
            return {
                "en": "❌ Cannot read Energy Dashboard configuration. Check your Home Assistant setup.",
                "fr": "❌ Impossible de lire la configuration du tableau de bord Énergie. Vérifiez votre installation Home Assistant.",
            }

