"""Tests pour les buttons."""
from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from custom_components.smart_appliance_monitor.button import (
    SmartApplianceResetStatsButton,
)


@pytest.fixture
def reset_button(mock_hass, mock_config_entry):
    """Fixture pour créer un bouton reset."""
    from custom_components.smart_appliance_monitor.coordinator import SmartApplianceCoordinator
    
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    return SmartApplianceResetStatsButton(coordinator)


def test_reset_button_init(reset_button):
    """Test l'initialisation du bouton reset."""
    assert reset_button.entity_type == "reset_stats"
    assert reset_button._attr_name == "Réinitialiser les statistiques"
    assert reset_button.unique_id.endswith("_reset_stats")
    assert reset_button.icon == "mdi:refresh"


@pytest.mark.asyncio
async def test_reset_button_press(reset_button):
    """Test l'appui sur le bouton reset."""
    # Mock des méthodes du coordinator
    reset_button.coordinator.reset_statistics = MagicMock()
    reset_button.coordinator.async_request_refresh = AsyncMock()
    
    # Appuyer sur le bouton
    await reset_button.async_press()
    
    # Vérifier que les méthodes ont été appelées
    reset_button.coordinator.reset_statistics.assert_called_once()
    reset_button.coordinator.async_request_refresh.assert_called_once()


@pytest.mark.asyncio
async def test_reset_button_emits_event(reset_button):
    """Test que le bouton émet un événement lors de l'appui."""
    # Mock des méthodes
    reset_button.coordinator.reset_statistics = MagicMock()
    reset_button.coordinator.async_request_refresh = AsyncMock()
    
    # Appuyer sur le bouton
    await reset_button.async_press()
    
    # Vérifier que l'événement a été émis
    reset_button.hass.bus.async_fire.assert_called_once()
    call_args = reset_button.hass.bus.async_fire.call_args
    assert call_args[0][0] == "smart_appliance_monitor_stats_reset"
    assert call_args[0][1]["appliance_name"] == "Four"
    assert "entry_id" in call_args[0][1]

