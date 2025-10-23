"""Dashboard configuration management for Smart Appliance Monitor."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.storage import Store

_LOGGER = logging.getLogger(__name__)

STORAGE_KEY = "smart_appliance_monitor.dashboard_config"
STORAGE_VERSION = 1

DEFAULT_COLOR_SCHEME = {
    "primary": "#3498db",
    "secondary": "#16a085",
    "accent": "#e74c3c",
}

DEFAULT_GLOBAL_SETTINGS = {
    "use_custom_cards": True,
    "theme": "default",
    "color_scheme": DEFAULT_COLOR_SCHEME,
    "auto_update": True,
}

DEFAULT_OVERVIEW_CONFIG = {
    "sections_visible": {
        "metrics": True,
        "monitoring": True,
        "energy_costs": True,
        "ai_analysis": True,
        "alerts": True,
        "energy_management": True,
        "controls": True,
        "export": True,
        "details": False,  # Désactivé par défaut (lourd)
    },
    "appliances_order": [],
}

DEFAULT_APPLIANCE_SECTIONS = {
    "status": True,                    # Gauge puissance + état
    "statistics_basic": True,          # Stats aujourd'hui/mois (existing)
    "statistics_advanced": True,       # Stats enrichies (fréquence, moyennes, tendances)
    "current_cycle": True,             # Cycle en cours
    "power_graph": True,               # Graphique historique puissance
    "controls": True,                  # Switches monitoring/notifications + reset
    "ai_actions": True,                # Carte IA avec services et dernière analyse
    "services": True,                  # Services complets (export, sync, etc.)
    "energy_management": False,        # Gestion énergie (si activé)
    "scheduling": False,               # Planification (si activé)
    "anomaly_detection": False,        # Détection anomalies (si activé)
    "alerts": False,                   # Alertes
}


class DashboardConfig:
    """Dashboard configuration data class."""

    def __init__(self, data: dict[str, Any] | None = None):
        """Initialize dashboard configuration."""
        if data is None:
            data = {}

        self.dashboard_id = data.get("dashboard_id", "smart_appliances")
        self.global_settings = data.get("global_settings", DEFAULT_GLOBAL_SETTINGS.copy())
        self.overview_config = data.get("overview_config", DEFAULT_OVERVIEW_CONFIG.copy())
        self.appliance_views = data.get("appliance_views", {})

        # Ensure all required keys exist
        self._ensure_defaults()

    def _ensure_defaults(self) -> None:
        """Ensure all default keys exist in configuration."""
        # Global settings
        for key, value in DEFAULT_GLOBAL_SETTINGS.items():
            if key not in self.global_settings:
                self.global_settings[key] = value

        # Color scheme
        if "color_scheme" not in self.global_settings:
            self.global_settings["color_scheme"] = DEFAULT_COLOR_SCHEME.copy()
        else:
            for key, value in DEFAULT_COLOR_SCHEME.items():
                if key not in self.global_settings["color_scheme"]:
                    self.global_settings["color_scheme"][key] = value

        # Overview config
        for key, value in DEFAULT_OVERVIEW_CONFIG.items():
            if key not in self.overview_config:
                self.overview_config[key] = value

        # Overview sections
        if "sections_visible" not in self.overview_config:
            self.overview_config["sections_visible"] = DEFAULT_OVERVIEW_CONFIG["sections_visible"].copy()

    def to_dict(self) -> dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            "dashboard_id": self.dashboard_id,
            "global_settings": self.global_settings,
            "overview_config": self.overview_config,
            "appliance_views": self.appliance_views,
        }

    def get_appliance_view_config(self, appliance_id: str) -> dict[str, Any]:
        """Get configuration for a specific appliance view."""
        if appliance_id in self.appliance_views:
            return self.appliance_views[appliance_id]

        # Return default configuration
        return {
            "enabled": True,
            "template": "generic",
            "sections_visible": DEFAULT_APPLIANCE_SECTIONS.copy(),
            "color": DEFAULT_COLOR_SCHEME["primary"],
            "custom_name": None,
        }

    def update_appliance_view(self, appliance_id: str, config: dict[str, Any]) -> None:
        """Update configuration for a specific appliance view."""
        if appliance_id not in self.appliance_views:
            self.appliance_views[appliance_id] = self.get_appliance_view_config(appliance_id)

        # Merge configuration
        self.appliance_views[appliance_id].update(config)

    def remove_appliance_view(self, appliance_id: str) -> None:
        """Remove configuration for a specific appliance view."""
        if appliance_id in self.appliance_views:
            del self.appliance_views[appliance_id]


class DashboardConfigManager:
    """Manager for dashboard configuration."""

    def __init__(self, hass: HomeAssistant):
        """Initialize configuration manager."""
        self.hass = hass
        self._store = Store(hass, STORAGE_VERSION, STORAGE_KEY)
        self._config: DashboardConfig | None = None

    async def async_load(self) -> DashboardConfig:
        """Load configuration from storage."""
        if self._config is not None:
            return self._config

        data = await self._store.async_load()
        self._config = DashboardConfig(data)

        _LOGGER.debug("Dashboard configuration loaded")
        return self._config

    async def async_save(self, config: DashboardConfig | None = None) -> None:
        """Save configuration to storage."""
        if config is not None:
            self._config = config

        if self._config is None:
            _LOGGER.warning("No configuration to save")
            return

        await self._store.async_save(self._config.to_dict())
        _LOGGER.debug("Dashboard configuration saved")

    async def async_get_config(self) -> DashboardConfig:
        """Get current configuration."""
        if self._config is None:
            return await self.async_load()
        return self._config

    async def async_update_global_settings(self, settings: dict[str, Any]) -> None:
        """Update global settings."""
        config = await self.async_get_config()
        config.global_settings.update(settings)
        await self.async_save()

    async def async_update_overview_config(self, overview_config: dict[str, Any]) -> None:
        """Update overview configuration."""
        config = await self.async_get_config()
        config.overview_config.update(overview_config)
        await self.async_save()

    async def async_update_view_config(
        self, appliance_id: str, view_config: dict[str, Any]
    ) -> None:
        """Update configuration for a specific appliance view."""
        config = await self.async_get_config()
        config.update_appliance_view(appliance_id, view_config)
        await self.async_save()

    async def async_remove_view_config(self, appliance_id: str) -> None:
        """Remove configuration for a specific appliance view."""
        config = await self.async_get_config()
        config.remove_appliance_view(appliance_id)
        await self.async_save()

    async def async_reset_to_defaults(self) -> None:
        """Reset configuration to defaults."""
        self._config = DashboardConfig()
        await self.async_save()
        _LOGGER.info("Dashboard configuration reset to defaults")

    async def async_migrate_config(self, old_version: int, new_version: int) -> None:
        """Migrate configuration from old version to new version."""
        _LOGGER.info(
            "Migrating dashboard configuration from version %d to %d",
            old_version,
            new_version,
        )
        # Add migration logic here if needed in future versions

