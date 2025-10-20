"""Config flow for Smart Appliance Monitor integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers import selector

from .const import (
    DOMAIN,
    CONF_APPLIANCE_NAME,
    CONF_APPLIANCE_TYPE,
    CONF_POWER_SENSOR,
    CONF_ENERGY_SENSOR,
    CONF_PRICE_KWH,
    CONF_PRICE_ENTITY,
    CONF_START_THRESHOLD,
    CONF_STOP_THRESHOLD,
    CONF_START_DELAY,
    CONF_STOP_DELAY,
    CONF_ENABLE_ALERT_DURATION,
    CONF_ALERT_DURATION,
    CONF_UNPLUGGED_TIMEOUT,
    CONF_NOTIFICATION_SERVICES,
    CONF_NOTIFICATION_TYPES,
    CONF_CUSTOM_NOTIFY_SERVICE,
    APPLIANCE_TYPES,
    APPLIANCE_PROFILES,
    NOTIFICATION_SERVICES,
    NOTIFICATION_TYPES,
    DEFAULT_PRICE_KWH,
    DEFAULT_START_THRESHOLD,
    DEFAULT_STOP_THRESHOLD,
    DEFAULT_START_DELAY,
    DEFAULT_STOP_DELAY,
    DEFAULT_ALERT_DURATION,
    DEFAULT_UNPLUGGED_TIMEOUT,
    DEFAULT_NOTIFICATION_SERVICES,
    DEFAULT_NOTIFICATION_TYPES,
)

_LOGGER = logging.getLogger(__name__)


class SmartApplianceMonitorConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Smart Appliance Monitor."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            # Validate the input
            power_sensor = user_input[CONF_POWER_SENSOR]
            
            # Check if sensor exists
            if not self.hass.states.get(power_sensor):
                errors["base"] = "invalid_sensor"
            else:
                # Create the config entry
                return self.async_create_entry(
                    title=user_input[CONF_APPLIANCE_NAME],
                    data=user_input,
                )

        # Build the config schema
        data_schema = vol.Schema(
            {
                vol.Required(CONF_APPLIANCE_NAME): str,
                vol.Required(CONF_APPLIANCE_TYPE): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=APPLIANCE_TYPES,
                        translation_key="appliance_type",
                    )
                ),
                vol.Required(CONF_POWER_SENSOR): selector.EntitySelector(
                    selector.EntitySelectorConfig(
                        domain="sensor",
                    )
                ),
                vol.Required(CONF_ENERGY_SENSOR): selector.EntitySelector(
                    selector.EntitySelectorConfig(
                        domain="sensor",
                    )
                ),
                vol.Optional(CONF_PRICE_ENTITY): selector.EntitySelector(
                    selector.EntitySelectorConfig(
                        domain=["sensor", "input_number"],
                    )
                ),
                vol.Optional(CONF_PRICE_KWH, default=DEFAULT_PRICE_KWH): cv.positive_float,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )

    async def async_step_reconfigure(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle reconfiguration of the integration."""
        errors: dict[str, str] = {}
        
        # Récupérer l'entrée de configuration actuelle
        entry = self.hass.config_entries.async_get_entry(self.context["entry_id"])
        
        if user_input is not None:
            # Valider les capteurs
            power_sensor = user_input[CONF_POWER_SENSOR]
            if not self.hass.states.get(power_sensor):
                errors["base"] = "invalid_sensor"
            else:
                # Mettre à jour la configuration
                self.hass.config_entries.async_update_entry(
                    entry,
                    data=user_input,
                    title=user_input[CONF_APPLIANCE_NAME],
                )
                # Recharger l'intégration
                await self.hass.config_entries.async_reload(entry.entry_id)
                return self.async_abort(reason="reconfigure_successful")
        
        # Pré-remplir avec les valeurs actuelles
        data_schema = vol.Schema(
            {
                vol.Required(
                    CONF_APPLIANCE_NAME,
                    default=entry.data.get(CONF_APPLIANCE_NAME)
                ): str,
                vol.Required(
                    CONF_APPLIANCE_TYPE,
                    default=entry.data.get(CONF_APPLIANCE_TYPE)
                ): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=APPLIANCE_TYPES,
                        translation_key="appliance_type",
                    )
                ),
                vol.Required(
                    CONF_POWER_SENSOR,
                    default=entry.data.get(CONF_POWER_SENSOR)
                ): selector.EntitySelector(
                    selector.EntitySelectorConfig(
                        domain="sensor",
                    )
                ),
                vol.Required(
                    CONF_ENERGY_SENSOR,
                    default=entry.data.get(CONF_ENERGY_SENSOR)
                ): selector.EntitySelector(
                    selector.EntitySelectorConfig(
                        domain="sensor",
                    )
                ),
                vol.Optional(
                    CONF_PRICE_ENTITY,
                    default=entry.data.get(CONF_PRICE_ENTITY)
                ): selector.EntitySelector(
                    selector.EntitySelectorConfig(
                        domain=["sensor", "input_number"],
                    )
                ),
                vol.Optional(
                    CONF_PRICE_KWH,
                    default=entry.data.get(CONF_PRICE_KWH, DEFAULT_PRICE_KWH)
                ): cv.positive_float,
            }
        )
        
        return self.async_show_form(
            step_id="reconfigure",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={
                "appliance_name": entry.data.get(CONF_APPLIANCE_NAME, "")
            },
        )

    @staticmethod
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Get the options flow for this handler."""
        return SmartApplianceMonitorOptionsFlowHandler(config_entry)


class SmartApplianceMonitorOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow for Smart Appliance Monitor."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        # Récupérer le profil de l'appareil pour les valeurs par défaut
        appliance_type = self.config_entry.data.get(CONF_APPLIANCE_TYPE, "other")
        profile = APPLIANCE_PROFILES.get(appliance_type, APPLIANCE_PROFILES["other"])

        options_schema = vol.Schema(
            {
                vol.Optional(
                    CONF_START_THRESHOLD,
                    default=self.config_entry.options.get(
                        CONF_START_THRESHOLD, profile["start_threshold"]
                    ),
                ): vol.All(vol.Coerce(int), vol.Range(min=1, max=5000)),
                vol.Optional(
                    CONF_STOP_THRESHOLD,
                    default=self.config_entry.options.get(
                        CONF_STOP_THRESHOLD, profile["stop_threshold"]
                    ),
                ): vol.All(vol.Coerce(int), vol.Range(min=1, max=100)),
                vol.Optional(
                    CONF_START_DELAY,
                    default=self.config_entry.options.get(
                        CONF_START_DELAY, profile["start_delay"]
                    ),
                ): vol.All(vol.Coerce(int), vol.Range(min=10, max=600)),
                vol.Optional(
                    CONF_STOP_DELAY,
                    default=self.config_entry.options.get(
                        CONF_STOP_DELAY, profile["stop_delay"]
                    ),
                ): vol.All(vol.Coerce(int), vol.Range(min=10, max=1800)),
                vol.Optional(
                    CONF_ENABLE_ALERT_DURATION,
                    default=self.config_entry.options.get(
                        CONF_ENABLE_ALERT_DURATION, False
                    ),
                ): cv.boolean,
                vol.Optional(
                    CONF_ALERT_DURATION,
                    default=self.config_entry.options.get(
                        CONF_ALERT_DURATION, profile["alert_duration"]
                    ),
                ): vol.All(vol.Coerce(int), vol.Range(min=1800, max=21600)),
                vol.Optional(
                    CONF_UNPLUGGED_TIMEOUT,
                    default=self.config_entry.options.get(
                        CONF_UNPLUGGED_TIMEOUT, DEFAULT_UNPLUGGED_TIMEOUT
                    ),
                ): vol.All(vol.Coerce(int), vol.Range(min=60, max=3600)),
                vol.Optional(
                    CONF_NOTIFICATION_SERVICES,
                    default=self.config_entry.options.get(
                        CONF_NOTIFICATION_SERVICES, DEFAULT_NOTIFICATION_SERVICES
                    ),
                ): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=NOTIFICATION_SERVICES,
                        multiple=True,
                        mode=selector.SelectSelectorMode.LIST,
                    )
                ),
                vol.Optional(
                    CONF_NOTIFICATION_TYPES,
                    default=self.config_entry.options.get(
                        CONF_NOTIFICATION_TYPES, DEFAULT_NOTIFICATION_TYPES
                    ),
                ): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=NOTIFICATION_TYPES,
                        multiple=True,
                        mode=selector.SelectSelectorMode.LIST,
                    )
                ),
                vol.Optional(
                    CONF_CUSTOM_NOTIFY_SERVICE,
                    default=self.config_entry.options.get(CONF_CUSTOM_NOTIFY_SERVICE, ""),
                ): str,
            }
        )

        return self.async_show_form(
            step_id="init",
            data_schema=options_schema,
        )

