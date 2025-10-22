"""Global configuration storage for Smart Appliance Monitor.

This module handles persistent global configuration that is shared across all appliances.
"""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.storage import Store

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

STORAGE_VERSION = 1
STORAGE_KEY = f"{DOMAIN}.global_config"


class GlobalConfigManager:
    """Manager for global configuration storage."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the global config manager.
        
        Args:
            hass: Home Assistant instance
        """
        self.hass = hass
        self._store = Store(hass, STORAGE_VERSION, STORAGE_KEY)
        self._config: dict[str, Any] = {}

    async def async_load(self) -> dict[str, Any]:
        """Load global configuration from storage.
        
        Returns:
            Global configuration dictionary
        """
        try:
            data = await self._store.async_load()
            if data is not None:
                self._config = data
                _LOGGER.debug("Global configuration loaded: %s", self._config)
            else:
                self._config = self._get_default_config()
                _LOGGER.debug("No stored config found, using defaults")
        except Exception as err:
            _LOGGER.error("Error loading global configuration: %s", err)
            self._config = self._get_default_config()
        
        return self._config

    async def async_save(self, config: dict[str, Any]) -> None:
        """Save global configuration to storage.
        
        Args:
            config: Configuration dictionary to save
        """
        try:
            self._config = config
            await self._store.async_save(config)
            _LOGGER.debug("Global configuration saved: %s", config)
        except Exception as err:
            _LOGGER.error("Error saving global configuration: %s", err)

    async def async_get(self, key: str, default: Any = None) -> Any:
        """Get a specific configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        if not self._config:
            await self.async_load()
        
        return self._config.get(key, default)

    async def async_set(self, key: str, value: Any) -> None:
        """Set a specific configuration value.
        
        Args:
            key: Configuration key
            value: Value to set
        """
        if not self._config:
            await self.async_load()
        
        self._config[key] = value
        await self.async_save(self._config)

    async def async_update(self, updates: dict[str, Any]) -> None:
        """Update multiple configuration values.
        
        Args:
            updates: Dictionary of key-value pairs to update
        """
        if not self._config:
            await self.async_load()
        
        self._config.update(updates)
        await self.async_save(self._config)

    def get_sync(self, key: str, default: Any = None) -> Any:
        """Get a configuration value synchronously (from cache).
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        return self._config.get(key, default)

    def _get_default_config(self) -> dict[str, Any]:
        """Get default global configuration.
        
        Returns:
            Default configuration dictionary
        """
        return {
            "ai_task_entity": None,
            "global_price_entity": None,
            "global_price_fixed": 0.2516,
            "enable_ai_analysis": False,
            "ai_analysis_trigger": "manual",
            "tariff_detection": {
                "detected_type": None,
                "peak_price": None,
                "offpeak_price": None,
                "transition_hours": [],
                "last_analysis": None,
            },
        }

    def get_currency(self) -> str:
        """Get configured currency from Home Assistant.
        
        Returns:
            Currency code (e.g., EUR, USD, GBP). Fallback to EUR if not configured.
        """
        return self.hass.config.currency or "EUR"
    
    def get_global_price_config(self) -> dict[str, Any]:
        """Get global price configuration.
        
        Returns:
            Dictionary with global_price_entity and global_price_fixed
        """
        return {
            "global_price_entity": self._config.get("global_price_entity"),
            "global_price_fixed": self._config.get("global_price_fixed", 0.2516),
        }
    
    async def async_update_tariff_detection(
        self, tariff_data: dict[str, Any]
    ) -> None:
        """Update tariff detection results.
        
        Args:
            tariff_data: Tariff detection results
        """
        if not self._config:
            await self.async_load()
        
        self._config["tariff_detection"] = tariff_data
        await self.async_save(self._config)
        _LOGGER.debug("Tariff detection updated: %s", tariff_data)

    @property
    def config(self) -> dict[str, Any]:
        """Get current configuration.
        
        Returns:
            Current configuration dictionary
        """
        return self._config

