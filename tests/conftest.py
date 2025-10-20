"""Configuration commune pour les tests."""
from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime

import pytest
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from custom_components.smart_appliance_monitor.const import (
    DOMAIN,
    CONF_APPLIANCE_NAME,
    CONF_APPLIANCE_TYPE,
    CONF_POWER_SENSOR,
    CONF_ENERGY_SENSOR,
    CONF_PRICE_KWH,
    APPLIANCE_TYPE_OVEN,
)


@pytest.fixture
def mock_config_entry() -> ConfigEntry:
    """Fixture pour créer une config entry de test."""
    return ConfigEntry(
        version=1,
        minor_version=0,
        domain=DOMAIN,
        title="Test Four",
        data={
            CONF_APPLIANCE_NAME: "Four",
            CONF_APPLIANCE_TYPE: APPLIANCE_TYPE_OVEN,
            CONF_POWER_SENSOR: "sensor.prise_four_power",
            CONF_ENERGY_SENSOR: "sensor.prise_four_energy",
            CONF_PRICE_KWH: 0.2516,
        },
        options={},
        source="user",
        entry_id="test_entry_id",
        unique_id="test_unique_id",
    )


@pytest.fixture
def mock_hass() -> HomeAssistant:
    """Fixture pour créer un mock de Home Assistant."""
    hass = MagicMock(spec=HomeAssistant)
    hass.states = MagicMock()
    hass.bus = MagicMock()
    hass.bus.async_fire = AsyncMock()
    hass.data = {}
    return hass


@pytest.fixture
def fixed_datetime():
    """Fixture pour fixer la date/heure dans les tests."""
    fixed_time = datetime(2025, 10, 20, 18, 30, 0)
    
    with patch("custom_components.smart_appliance_monitor.state_machine.datetime") as mock_dt:
        mock_dt.now.return_value = fixed_time
        yield fixed_time

