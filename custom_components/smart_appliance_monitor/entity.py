"""Classe de base pour les entités Smart Appliance Monitor."""
from __future__ import annotations

from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, CONF_APPLIANCE_NAME, CONF_APPLIANCE_TYPE
from .coordinator import SmartApplianceCoordinator


class SmartApplianceEntity(CoordinatorEntity[SmartApplianceCoordinator]):
    """Classe de base pour toutes les entités Smart Appliance Monitor."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: SmartApplianceCoordinator,
        entity_type: str,
    ) -> None:
        """Initialise l'entité.
        
        Args:
            coordinator: Le coordinator de l'appareil
            entity_type: Type d'entité (ex: "state", "running", etc.)
        """
        super().__init__(coordinator)
        
        self.entity_type = entity_type
        self._attr_unique_id = f"{coordinator.entry.entry_id}_{entity_type}"
        
        # Set English name BEFORE translation_key to force English entity_id
        # The entity_id will be: sensor.{appliance_slug}_{entity_type}
        # The UI will still show translated names via translation_key in child classes
        self._attr_name = entity_type.replace("_", " ").capitalize()
        
        # Device info pour regrouper toutes les entités
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.entry.entry_id)},
            name=coordinator.appliance_name,
            manufacturer="Smart Appliance Monitor",
            model=coordinator.appliance_type.replace("_", " ").title(),
            sw_version="0.1.0",
            configuration_url=f"homeassistant://config/integrations/integration/{DOMAIN}",
        )
    
    @property
    def available(self) -> bool:
        """Retourne si l'entité est disponible.
        
        L'entité est disponible si le coordinator a des données.
        """
        return self.coordinator.last_update_success

