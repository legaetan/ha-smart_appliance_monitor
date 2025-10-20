"""Tests pour le système de notifications."""
from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from custom_components.smart_appliance_monitor.notify import SmartApplianceNotifier


@pytest.fixture
def notifier(mock_hass):
    """Fixture pour créer un notifier."""
    return SmartApplianceNotifier(
        hass=mock_hass,
        appliance_name="Four",
        appliance_type="oven",
        notifications_enabled=True,
    )


def test_notifier_init(notifier):
    """Test l'initialisation du notifier."""
    assert notifier.appliance_name == "Four"
    assert notifier.appliance_type == "oven"
    assert notifier.notifications_enabled is True


@pytest.mark.asyncio
async def test_notify_cycle_started(notifier):
    """Test la notification de démarrage de cycle."""
    notifier.hass.services.has_service = MagicMock(return_value=True)
    notifier.hass.services.async_call = AsyncMock()
    
    await notifier.notify_cycle_started()
    
    # Vérifier que le service a été appelé
    notifier.hass.services.async_call.assert_called_once()
    call_args = notifier.hass.services.async_call.call_args
    
    assert call_args[0][0] == "notify"
    assert call_args[0][1] == "mobile_app"
    assert "Four démarré" in call_args[0][2]["title"]
    assert "démarrer" in call_args[0][2]["message"].lower()


@pytest.mark.asyncio
async def test_notify_cycle_started_disabled(notifier):
    """Test que la notification n'est pas envoyée si désactivée."""
    notifier.notifications_enabled = False
    notifier.hass.services.async_call = AsyncMock()
    
    await notifier.notify_cycle_started()
    
    # Vérifier que le service n'a pas été appelé
    notifier.hass.services.async_call.assert_not_called()


@pytest.mark.asyncio
async def test_notify_cycle_finished(notifier):
    """Test la notification de fin de cycle."""
    notifier.hass.services.has_service = MagicMock(return_value=True)
    notifier.hass.services.async_call = AsyncMock()
    
    await notifier.notify_cycle_finished(
        duration=45.5,  # 45.5 minutes
        energy=1.234,   # 1.234 kWh
        cost=0.31,      # 0.31 €
    )
    
    # Vérifier que le service a été appelé
    notifier.hass.services.async_call.assert_called_once()
    call_args = notifier.hass.services.async_call.call_args
    
    assert call_args[0][0] == "notify"
    assert "terminé" in call_args[0][2]["title"].lower()
    
    message = call_args[0][2]["message"]
    assert "45 min" in message
    assert "1.23 kWh" in message
    assert "0.31 €" in message


@pytest.mark.asyncio
async def test_notify_cycle_finished_long_duration(notifier):
    """Test la notification avec une longue durée."""
    notifier.hass.services.has_service = MagicMock(return_value=True)
    notifier.hass.services.async_call = AsyncMock()
    
    await notifier.notify_cycle_finished(
        duration=135.0,  # 2h15
        energy=2.5,
        cost=0.63,
    )
    
    call_args = notifier.hass.services.async_call.call_args
    message = call_args[0][2]["message"]
    
    assert "2h15" in message


@pytest.mark.asyncio
async def test_notify_alert_duration(notifier):
    """Test la notification d'alerte de durée."""
    notifier.hass.services.has_service = MagicMock(return_value=True)
    notifier.hass.services.async_call = AsyncMock()
    
    await notifier.notify_alert_duration(duration=135.0)  # 2h15
    
    # Vérifier que le service a été appelé
    notifier.hass.services.async_call.assert_called_once()
    call_args = notifier.hass.services.async_call.call_args
    
    assert call_args[0][0] == "notify"
    assert "Alerte" in call_args[0][2]["title"]
    
    message = call_args[0][2]["message"]
    assert "2h15" in message
    assert "anormalement" in message.lower()


@pytest.mark.asyncio
async def test_notify_fallback_to_persistent(notifier):
    """Test le fallback vers persistent_notification si mobile_app n'existe pas."""
    notifier.hass.services.has_service = MagicMock(return_value=False)
    notifier.hass.services.async_call = AsyncMock()
    
    await notifier.notify_cycle_started()
    
    # Vérifier que persistent_notification a été utilisé
    notifier.hass.services.async_call.assert_called_once()
    call_args = notifier.hass.services.async_call.call_args
    
    assert call_args[0][0] == "notify"
    assert call_args[0][1] == "persistent_notification"


@pytest.mark.asyncio
async def test_notify_handles_errors(notifier):
    """Test que les erreurs de notification sont gérées."""
    notifier.hass.services.has_service = MagicMock(return_value=True)
    notifier.hass.services.async_call = AsyncMock(
        side_effect=Exception("Service non disponible")
    )
    
    # Ne doit pas lever d'exception
    await notifier.notify_cycle_started()


def test_set_enabled(notifier):
    """Test l'activation/désactivation des notifications."""
    assert notifier.notifications_enabled is True
    
    notifier.set_enabled(False)
    assert notifier.notifications_enabled is False
    
    notifier.set_enabled(True)
    assert notifier.notifications_enabled is True

