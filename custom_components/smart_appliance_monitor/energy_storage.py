"""Energy Storage File Reader for Smart Appliance Monitor.

This module provides read-only access to Home Assistant's .storage/energy file
to synchronize with the native Energy Dashboard.
"""
from __future__ import annotations

import asyncio
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError

_LOGGER = logging.getLogger(__name__)

ENERGY_STORAGE_FILE = ".storage/energy"
CACHE_DURATION = timedelta(minutes=5)


class EnergyStorageError(HomeAssistantError):
    """Exception raised when energy storage file cannot be read."""


class EnergyStorageReader:
    """Read and parse Home Assistant's energy storage file."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the energy storage reader.
        
        Args:
            hass: Home Assistant instance
        """
        self.hass = hass
        self._cache: dict[str, Any] | None = None
        self._cache_time: datetime | None = None
        self._lock = asyncio.Lock()

    @property
    def storage_path(self) -> Path:
        """Get the path to the energy storage file.
        
        Returns:
            Path to .storage/energy file
        """
        return Path(self.hass.config.path(ENERGY_STORAGE_FILE))

    async def async_read_energy_config(
        self, force_refresh: bool = False
    ) -> dict[str, Any]:
        """Read the energy configuration from storage file.
        
        Args:
            force_refresh: Force refresh of cache
            
        Returns:
            Dictionary with energy configuration
            
        Raises:
            EnergyStorageError: If file cannot be read or parsed
        """
        async with self._lock:
            # Check cache validity
            if not force_refresh and self._is_cache_valid():
                _LOGGER.debug("Using cached energy configuration")
                return self._cache.copy()

            try:
                config = await self._read_file()
                self._cache = config
                self._cache_time = datetime.now()
                return config.copy()
            except Exception as err:
                _LOGGER.error("Failed to read energy storage file: %s", err)
                raise EnergyStorageError(f"Cannot read energy storage: {err}") from err

    def _is_cache_valid(self) -> bool:
        """Check if cache is still valid.
        
        Returns:
            True if cache exists and is not expired
        """
        if self._cache is None or self._cache_time is None:
            return False
        
        age = datetime.now() - self._cache_time
        return age < CACHE_DURATION

    async def _read_file(self) -> dict[str, Any]:
        """Read and parse the energy storage file.
        
        Returns:
            Parsed JSON content
            
        Raises:
            EnergyStorageError: If file doesn't exist or is invalid
        """
        if not self.storage_path.exists():
            raise EnergyStorageError(
                f"Energy storage file not found at {self.storage_path}"
            )

        try:
            content = await self.hass.async_add_executor_job(
                self._read_file_sync
            )
            return content
        except json.JSONDecodeError as err:
            raise EnergyStorageError(
                f"Invalid JSON in energy storage file: {err}"
            ) from err

    def _read_file_sync(self) -> dict[str, Any]:
        """Synchronous file reading (runs in executor).
        
        Returns:
            Parsed JSON content
        """
        with open(self.storage_path, "r", encoding="utf-8") as file:
            return json.load(file)

    async def get_energy_sources(self) -> list[dict[str, Any]]:
        """Get configured energy sources.
        
        Returns:
            List of energy sources (grid, solar, battery, gas)
        """
        config = await self.async_read_energy_config()
        return config.get("data", {}).get("energy_sources", [])

    async def get_device_consumption(self) -> list[dict[str, Any]]:
        """Get configured device consumption entries.
        
        Returns:
            List of devices with their consumption sensors
        """
        config = await self.async_read_energy_config()
        return config.get("data", {}).get("device_consumption", [])

    async def find_device_by_sensor(
        self, sensor_entity_id: str
    ) -> dict[str, Any] | None:
        """Find a device configuration by its energy sensor.
        
        Args:
            sensor_entity_id: Entity ID of the energy sensor
            
        Returns:
            Device configuration dict or None if not found
        """
        devices = await self.get_device_consumption()
        for device in devices:
            if device.get("stat_consumption") == sensor_entity_id:
                return device
        return None

    async def is_sensor_in_dashboard(self, sensor_entity_id: str) -> bool:
        """Check if a sensor is configured in Energy Dashboard.
        
        Args:
            sensor_entity_id: Entity ID to check
            
        Returns:
            True if sensor is in the dashboard
        """
        device = await self.find_device_by_sensor(sensor_entity_id)
        return device is not None

    async def get_total_grid_consumption_sensor(self) -> str | None:
        """Get the main grid consumption sensor.
        
        Returns:
            Entity ID of the main grid sensor or None
        """
        sources = await self.get_energy_sources()
        for source in sources:
            if source.get("type") == "grid":
                flow_from = source.get("flow_from", [])
                if flow_from:
                    return flow_from[0].get("stat_energy_from")
        return None

    async def get_devices_included_in_stat(
        self, parent_sensor: str
    ) -> list[dict[str, Any]]:
        """Get all devices included in a parent sensor.
        
        Args:
            parent_sensor: Parent sensor entity ID
            
        Returns:
            List of devices that are sub-components of the parent
        """
        devices = await self.get_device_consumption()
        included = []
        for device in devices:
            if device.get("included_in_stat") == parent_sensor:
                included.append(device)
        return included

    async def get_sync_report(
        self, sam_devices: list[dict[str, Any]]
    ) -> dict[str, Any]:
        """Generate synchronization report between SAM and Energy Dashboard.
        
        Args:
            sam_devices: List of SAM configured devices with their sensors
            
        Returns:
            Report with sync status and recommendations
        """
        dashboard_devices = await self.get_device_consumption()
        
        # Build sets for comparison
        dashboard_sensors = {d.get("stat_consumption") for d in dashboard_devices}
        sam_sensors = {d.get("energy_sensor") for d in sam_devices}
        
        # Find matches and mismatches
        synced = []
        not_in_dashboard = []
        
        for device in sam_devices:
            sensor = device.get("energy_sensor")
            if sensor in dashboard_sensors:
                synced.append(device)
            else:
                not_in_dashboard.append(device)
        
        # Find dashboard devices that could use SAM
        potential_sam_devices = []
        for device in dashboard_devices:
            sensor = device.get("stat_consumption")
            if sensor not in sam_sensors:
                # Check if it ends with _energy (common pattern)
                if sensor and sensor.endswith("_energy"):
                    potential_sam_devices.append(device)
        
        return {
            "synced_devices": synced,
            "not_in_dashboard": not_in_dashboard,
            "potential_sam_devices": potential_sam_devices,
            "total_sam_devices": len(sam_devices),
            "total_dashboard_devices": len(dashboard_devices),
            "sync_percentage": (
                len(synced) / len(sam_devices) * 100 if sam_devices else 0
            ),
        }

    def invalidate_cache(self) -> None:
        """Invalidate the cache to force refresh on next read."""
        self._cache = None
        self._cache_time = None
        _LOGGER.debug("Energy storage cache invalidated")

