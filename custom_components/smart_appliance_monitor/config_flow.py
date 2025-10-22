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
    CONF_ENABLE_AUTO_SHUTDOWN,
    CONF_AUTO_SHUTDOWN_DELAY,
    CONF_AUTO_SHUTDOWN_ENTITY,
    CONF_ENABLE_ENERGY_LIMITS,
    CONF_ENERGY_LIMIT_CYCLE,
    CONF_ENERGY_LIMIT_DAILY,
    CONF_ENERGY_LIMIT_MONTHLY,
    CONF_COST_BUDGET_MONTHLY,
    CONF_ENABLE_SCHEDULING,
    CONF_ALLOWED_HOURS_START,
    CONF_ALLOWED_HOURS_END,
    CONF_BLOCKED_DAYS,
    CONF_SCHEDULING_MODE,
    CONF_ENABLE_ANOMALY_DETECTION,
    APPLIANCE_TYPES,
    APPLIANCE_PROFILES,
    NOTIFICATION_SERVICES,
    NOTIFICATION_TYPES,
    SCHEDULING_MODE_NOTIFICATION,
    SCHEDULING_MODE_STRICT,
    DAYS_OF_WEEK,
    DEFAULT_PRICE_KWH,
    DEFAULT_START_THRESHOLD,
    DEFAULT_STOP_THRESHOLD,
    DEFAULT_START_DELAY,
    DEFAULT_STOP_DELAY,
    DEFAULT_ALERT_DURATION,
    DEFAULT_UNPLUGGED_TIMEOUT,
    DEFAULT_AUTO_SHUTDOWN_DELAY,
    DEFAULT_SCHEDULING_MODE,
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
                # Prix configuré globalement - voir service set_global_config
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={
                "price_info": "Energy price is now configured globally. Use the service 'smart_appliance_monitor.set_global_config' to configure pricing for all appliances."
            },
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
                # Prix configuré globalement - voir service set_global_config
            }
        )
        
        return self.async_show_form(
            step_id="reconfigure",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={
                "appliance_name": entry.data.get(CONF_APPLIANCE_NAME, ""),
                "price_info": "Energy price is now configured globally via set_global_config service."
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
        self._options = dict(config_entry.options)

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options - Step 1: Detection thresholds."""
        if user_input is not None:
            # Sauvegarder les options de cette étape
            self._options.update(user_input)
            # Passer à l'étape suivante
            return await self.async_step_delays()

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
            }
        )

        return self.async_show_form(
            step_id="init",
            data_schema=options_schema,
        )

    async def async_step_delays(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Step 2: Detection delays and alert duration."""
        if user_input is not None:
            # Convertir les minutes en secondes pour start_delay et stop_delay
            if "start_delay_minutes" in user_input:
                self._options[CONF_START_DELAY] = user_input["start_delay_minutes"] * 60
            if "stop_delay_minutes" in user_input:
                self._options[CONF_STOP_DELAY] = user_input["stop_delay_minutes"] * 60
            
            # Convertir les heures en secondes pour alert_duration
            if "alert_duration_hours" in user_input:
                self._options[CONF_ALERT_DURATION] = int(user_input["alert_duration_hours"] * 3600)
            
            # Sauvegarder enable_alert_duration, enable_anomaly_detection
            self._options[CONF_ENABLE_ALERT_DURATION] = user_input.get(CONF_ENABLE_ALERT_DURATION, False)
            self._options[CONF_ENABLE_ANOMALY_DETECTION] = user_input.get(CONF_ENABLE_ANOMALY_DETECTION, False)
            
            # Si mode avancé (energy/scheduling) activé
            if user_input.get("configure_advanced", False):
                return await self.async_step_energy_management()
            # Si mode expert activé, aller à l'étape expert
            elif user_input.get("expert_mode", False):
                self._options["expert_mode"] = True
                return await self.async_step_expert()
            else:
                self._options["expert_mode"] = False
                # Passer à l'étape notifications
                return await self.async_step_notifications()

        # Récupérer le profil de l'appareil pour les valeurs par défaut
        appliance_type = self.config_entry.data.get(CONF_APPLIANCE_TYPE, "other")
        profile = APPLIANCE_PROFILES.get(appliance_type, APPLIANCE_PROFILES["other"])

        # Convertir les secondes en minutes/heures pour l'affichage
        start_delay_minutes = self.config_entry.options.get(
            CONF_START_DELAY, profile["start_delay"]
        ) / 60
        stop_delay_minutes = self.config_entry.options.get(
            CONF_STOP_DELAY, profile["stop_delay"]
        ) / 60
        alert_duration_hours = self.config_entry.options.get(
            CONF_ALERT_DURATION, profile["alert_duration"]
        ) / 3600

        options_schema = vol.Schema(
            {
                vol.Optional(
                    "start_delay_minutes",
                    default=start_delay_minutes,
                ): vol.All(vol.Coerce(float), vol.Range(min=0.5, max=10)),
                vol.Optional(
                    "stop_delay_minutes",
                    default=stop_delay_minutes,
                ): vol.All(vol.Coerce(float), vol.Range(min=0.5, max=30)),
                vol.Optional(
                    CONF_ENABLE_ALERT_DURATION,
                    default=self.config_entry.options.get(
                        CONF_ENABLE_ALERT_DURATION, False
                    ),
                ): cv.boolean,
                vol.Optional(
                    "alert_duration_hours",
                    default=alert_duration_hours,
                ): vol.All(vol.Coerce(float), vol.Range(min=0.5, max=24)),
                vol.Optional(
                    CONF_ENABLE_ANOMALY_DETECTION,
                    default=self.config_entry.options.get(
                        CONF_ENABLE_ANOMALY_DETECTION, False
                    ),
                ): cv.boolean,
                vol.Optional(
                    "configure_advanced",
                    default=False,
                ): cv.boolean,
                vol.Optional(
                    "expert_mode",
                    default=False,
                ): cv.boolean,
            }
        )

        return self.async_show_form(
            step_id="delays",
            data_schema=options_schema,
        )

    async def async_step_notifications(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Step 3: Notification settings."""
        if user_input is not None:
            # Sauvegarder les options de notifications
            self._options[CONF_NOTIFICATION_SERVICES] = user_input.get(
                CONF_NOTIFICATION_SERVICES, DEFAULT_NOTIFICATION_SERVICES
            )
            self._options[CONF_NOTIFICATION_TYPES] = user_input.get(
                CONF_NOTIFICATION_TYPES, DEFAULT_NOTIFICATION_TYPES
            )
            
            # Nettoyer expert_mode de la configuration finale
            self._options.pop("expert_mode", None)
            
            # Créer l'entrée finale
            return self.async_create_entry(title="", data=self._options)

        options_schema = vol.Schema(
            {
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
                        translation_key="notification_service",
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
                        translation_key="notification_type",
                    )
                ),
            }
        )

        return self.async_show_form(
            step_id="notifications",
            data_schema=options_schema,
        )

    async def async_step_expert(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Step 4: Expert settings (optional)."""
        if user_input is not None:
            # Convertir les minutes en secondes pour unplugged_timeout
            if "unplugged_timeout_minutes" in user_input:
                self._options[CONF_UNPLUGGED_TIMEOUT] = user_input["unplugged_timeout_minutes"] * 60
            
            # Auto-shutdown
            self._options[CONF_ENABLE_AUTO_SHUTDOWN] = user_input.get(CONF_ENABLE_AUTO_SHUTDOWN, False)
            if "auto_shutdown_delay_minutes" in user_input:
                self._options[CONF_AUTO_SHUTDOWN_DELAY] = user_input["auto_shutdown_delay_minutes"] * 60
            self._options[CONF_AUTO_SHUTDOWN_ENTITY] = user_input.get(CONF_AUTO_SHUTDOWN_ENTITY, "")
            
            # Sauvegarder le service personnalisé
            self._options[CONF_CUSTOM_NOTIFY_SERVICE] = user_input.get(
                CONF_CUSTOM_NOTIFY_SERVICE, ""
            )
            
            # Passer à l'étape notifications
            return await self.async_step_notifications()

        # Convertir les secondes en minutes pour l'affichage
        unplugged_timeout_minutes = self.config_entry.options.get(
            CONF_UNPLUGGED_TIMEOUT, DEFAULT_UNPLUGGED_TIMEOUT
        ) / 60
        auto_shutdown_delay_minutes = self.config_entry.options.get(
            CONF_AUTO_SHUTDOWN_DELAY, DEFAULT_AUTO_SHUTDOWN_DELAY
        ) / 60

        options_schema = vol.Schema(
            {
                vol.Optional(
                    "unplugged_timeout_minutes",
                    default=unplugged_timeout_minutes,
                ): vol.All(vol.Coerce(float), vol.Range(min=1, max=60)),
                vol.Optional(
                    CONF_CUSTOM_NOTIFY_SERVICE,
                    default=self.config_entry.options.get(CONF_CUSTOM_NOTIFY_SERVICE, ""),
                ): str,
                vol.Optional(
                    CONF_ENABLE_AUTO_SHUTDOWN,
                    default=self.config_entry.options.get(CONF_ENABLE_AUTO_SHUTDOWN, False),
                ): cv.boolean,
                vol.Optional(
                    "auto_shutdown_delay_minutes",
                    default=auto_shutdown_delay_minutes,
                ): vol.All(vol.Coerce(float), vol.Range(min=5, max=60)),
                vol.Optional(
                    CONF_AUTO_SHUTDOWN_ENTITY,
                    default=self.config_entry.options.get(CONF_AUTO_SHUTDOWN_ENTITY, ""),
                ): selector.EntitySelector(
                    selector.EntitySelectorConfig(
                        domain=["switch", "light"],
                    )
                ),
            }
        )

        return self.async_show_form(
            step_id="expert",
            data_schema=options_schema,
        )

    async def async_step_energy_management(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Step: Energy Management (optional)."""
        if user_input is not None:
            # Sauvegarder les options de gestion énergétique
            self._options[CONF_ENABLE_ENERGY_LIMITS] = user_input.get(CONF_ENABLE_ENERGY_LIMITS, False)
            self._options[CONF_ENERGY_LIMIT_CYCLE] = user_input.get(CONF_ENERGY_LIMIT_CYCLE, 0)
            self._options[CONF_ENERGY_LIMIT_DAILY] = user_input.get(CONF_ENERGY_LIMIT_DAILY, 0)
            self._options[CONF_ENERGY_LIMIT_MONTHLY] = user_input.get(CONF_ENERGY_LIMIT_MONTHLY, 0)
            self._options[CONF_COST_BUDGET_MONTHLY] = user_input.get(CONF_COST_BUDGET_MONTHLY, 0)
            
            # Passer à l'étape scheduling
            return await self.async_step_scheduling()

        options_schema = vol.Schema(
            {
                vol.Optional(
                    CONF_ENABLE_ENERGY_LIMITS,
                    default=self.config_entry.options.get(CONF_ENABLE_ENERGY_LIMITS, False),
                ): cv.boolean,
                vol.Optional(
                    CONF_ENERGY_LIMIT_CYCLE,
                    default=self.config_entry.options.get(CONF_ENERGY_LIMIT_CYCLE, 0),
                ): vol.All(vol.Coerce(float), vol.Range(min=0, max=100)),
                vol.Optional(
                    CONF_ENERGY_LIMIT_DAILY,
                    default=self.config_entry.options.get(CONF_ENERGY_LIMIT_DAILY, 0),
                ): vol.All(vol.Coerce(float), vol.Range(min=0, max=500)),
                vol.Optional(
                    CONF_ENERGY_LIMIT_MONTHLY,
                    default=self.config_entry.options.get(CONF_ENERGY_LIMIT_MONTHLY, 0),
                ): vol.All(vol.Coerce(float), vol.Range(min=0, max=10000)),
                vol.Optional(
                    CONF_COST_BUDGET_MONTHLY,
                    default=self.config_entry.options.get(CONF_COST_BUDGET_MONTHLY, 0),
                ): vol.All(vol.Coerce(float), vol.Range(min=0, max=1000)),
            }
        )

        return self.async_show_form(
            step_id="energy_management",
            data_schema=options_schema,
        )

    async def async_step_scheduling(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Step: Scheduling (optional)."""
        if user_input is not None:
            # Sauvegarder les options de planification
            self._options[CONF_ENABLE_SCHEDULING] = user_input.get(CONF_ENABLE_SCHEDULING, False)
            self._options[CONF_ALLOWED_HOURS_START] = user_input.get(CONF_ALLOWED_HOURS_START, "00:00")
            self._options[CONF_ALLOWED_HOURS_END] = user_input.get(CONF_ALLOWED_HOURS_END, "23:59")
            self._options[CONF_BLOCKED_DAYS] = user_input.get(CONF_BLOCKED_DAYS, [])
            self._options[CONF_SCHEDULING_MODE] = user_input.get(CONF_SCHEDULING_MODE, DEFAULT_SCHEDULING_MODE)
            
            # Si mode expert était activé, aller à l'étape expert, sinon notifications
            if self._options.get("expert_mode", False):
                return await self.async_step_expert()
            else:
                return await self.async_step_notifications()

        options_schema = vol.Schema(
            {
                vol.Optional(
                    CONF_ENABLE_SCHEDULING,
                    default=self.config_entry.options.get(CONF_ENABLE_SCHEDULING, False),
                ): cv.boolean,
                vol.Optional(
                    CONF_ALLOWED_HOURS_START,
                    default=self.config_entry.options.get(CONF_ALLOWED_HOURS_START, "00:00"),
                ): str,
                vol.Optional(
                    CONF_ALLOWED_HOURS_END,
                    default=self.config_entry.options.get(CONF_ALLOWED_HOURS_END, "23:59"),
                ): str,
                vol.Optional(
                    CONF_BLOCKED_DAYS,
                    default=self.config_entry.options.get(CONF_BLOCKED_DAYS, []),
                ): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=DAYS_OF_WEEK,
                        multiple=True,
                        mode=selector.SelectSelectorMode.LIST,
                        translation_key="day_of_week",
                    )
                ),
                vol.Optional(
                    CONF_SCHEDULING_MODE,
                    default=self.config_entry.options.get(CONF_SCHEDULING_MODE, DEFAULT_SCHEDULING_MODE),
                ): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=[SCHEDULING_MODE_NOTIFICATION, SCHEDULING_MODE_STRICT],
                        translation_key="scheduling_mode",
                    )
                ),
            }
        )

        return self.async_show_form(
            step_id="scheduling",
            data_schema=options_schema,
        )

