"""Dashboard manager for Smart Appliance Monitor."""
from __future__ import annotations

import json
import logging
import os
import re
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml

from homeassistant.core import HomeAssistant
from homeassistant.components import frontend
from homeassistant.helpers import entity_registry as er

from .const import (
    DOMAIN,
    CONF_APPLIANCE_TYPE,
    APPLIANCE_TYPE_WASHING_MACHINE,
    APPLIANCE_TYPE_DISHWASHER,
    APPLIANCE_TYPE_DRYER,
    APPLIANCE_TYPE_WATER_HEATER,
    APPLIANCE_TYPE_OVEN,
    APPLIANCE_TYPE_MONITOR,
    APPLIANCE_TYPE_NAS,
    APPLIANCE_TYPE_PRINTER_3D,
    APPLIANCE_TYPE_VMC,
    APPLIANCE_TYPE_OTHER,
    SESSION_BASED_TYPES,
)
from .coordinator import SmartApplianceCoordinator
from .dashboard_config import DashboardConfigManager

_LOGGER = logging.getLogger(__name__)

DASHBOARD_URL_PATH = "smart-appliances"
DASHBOARD_TITLE = "Smart Appliances"
DASHBOARD_ICON = "mdi:lightning-bolt"

# Template mapping
TEMPLATE_MAP = {
    APPLIANCE_TYPE_WASHING_MACHINE: "washing_machine",
    APPLIANCE_TYPE_DISHWASHER: "dishwasher",
    APPLIANCE_TYPE_DRYER: "dryer",
    APPLIANCE_TYPE_WATER_HEATER: "water_heater",
    APPLIANCE_TYPE_OVEN: "oven",
    APPLIANCE_TYPE_MONITOR: "monitor",
    APPLIANCE_TYPE_NAS: "nas",
    APPLIANCE_TYPE_PRINTER_3D: "printer_3d",
    APPLIANCE_TYPE_VMC: "vmc",
    APPLIANCE_TYPE_OTHER: "generic",
}

# Icon mapping
ICON_MAP = {
    APPLIANCE_TYPE_WASHING_MACHINE: "mdi:washing-machine",
    APPLIANCE_TYPE_DISHWASHER: "mdi:dishwasher",
    APPLIANCE_TYPE_DRYER: "mdi:tumble-dryer",
    APPLIANCE_TYPE_WATER_HEATER: "mdi:water-boiler",
    APPLIANCE_TYPE_OVEN: "mdi:stove",
    APPLIANCE_TYPE_MONITOR: "mdi:monitor",
    APPLIANCE_TYPE_NAS: "mdi:nas",
    APPLIANCE_TYPE_PRINTER_3D: "mdi:printer-3d",
    APPLIANCE_TYPE_VMC: "mdi:fan",
    APPLIANCE_TYPE_OTHER: "mdi:power-plug",
}


class DashboardManager:
    """Manager for Smart Appliances dashboard."""

    def __init__(self, hass: HomeAssistant, config_manager: DashboardConfigManager):
        """Initialize dashboard manager."""
        self.hass = hass
        self.config_manager = config_manager
        self._dashboard_exists = False
        self._custom_cards_available = {}
        self.dashboard_id = DASHBOARD_URL_PATH

    async def async_initialize(self):
        """Initialize the dashboard manager."""
        # Check for custom cards availability
        self._custom_cards_available = await self._async_check_custom_cards_available()
        _LOGGER.debug("Custom cards available: %s", self._custom_cards_available)

    async def _async_check_custom_cards_available(self) -> dict[str, bool]:
        """Check which custom cards are available."""
        available = {
            "smart_appliance_cycle_card": False,
            "smart_appliance_stats_card": False,
            "apexcharts_card": False,
        }

        try:
            # Check if custom cards directory exists
            www_path = Path(self.hass.config.path("www"))
            sam_cards_path = www_path / "smart-appliance-cards" / "dist"
            
            if sam_cards_path.exists():
                cycle_card = sam_cards_path / "smart-appliance-cycle-card.js"
                stats_card = sam_cards_path / "smart-appliance-stats-card.js"
                
                available["smart_appliance_cycle_card"] = cycle_card.exists()
                available["smart_appliance_stats_card"] = stats_card.exists()
                _LOGGER.debug("SAM custom cards found: cycle=%s, stats=%s",
                             available["smart_appliance_cycle_card"],
                             available["smart_appliance_stats_card"])

        except Exception as err:
            _LOGGER.debug("Error checking custom cards: %s", err)

        return available

    async def async_check_dashboard_exists(self) -> bool:
        """Check if dashboard YAML file exists (legacy compatibility)."""
        try:
            yaml_path = Path(self.hass.config.path("dashboards", "smart-appliances.yaml"))
            exists = yaml_path.exists()
            _LOGGER.debug("Dashboard YAML exists check: %s", exists)
            return exists
        except Exception as err:
            _LOGGER.debug("Error checking dashboard existence: %s", err)
            return False

    async def async_register_dashboard_if_exists(self) -> None:
        """Register dashboard if exists (legacy compatibility - YAML mode doesn't need registration)."""
        _LOGGER.debug("Dashboard registration not needed in YAML mode")

    async def async_create_or_update_dashboard(
        self, force_recreate: bool = False, output_path: str | None = None
    ) -> dict[str, Any]:
        """Generate the dashboard YAML file."""
        return await self.async_generate_yaml_file(output_path)

    async def async_generate_yaml_file(self, output_path: str | None = None) -> dict[str, Any]:
        """Generate the dashboard as a YAML file.
        
        Args:
            output_path: Custom output path (optional, defaults to config/dashboards/smart-appliances.yaml)
            
        Returns:
            dict with success status, path, and configuration instructions
        """
        try:
            # Build complete dashboard configuration
            dashboard_config = await self._async_build_dashboard_config()
            
            coordinators = self._get_all_coordinators()
            views_count = len(dashboard_config.get("views", []))
            
            _LOGGER.info("Generating dashboard YAML with %d views", views_count)

            # Determine output path
            if output_path:
                yaml_path = Path(output_path)
            else:
                yaml_path = Path(self.hass.config.path("dashboards", "smart-appliances.yaml"))
            
            # Create directory if needed
            yaml_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write YAML file
            await self.hass.async_add_executor_job(
                self._write_yaml_file,
                yaml_path,
                dashboard_config,
            )
            
            # Generate configuration instructions
            instructions = self._generate_config_instructions(yaml_path)
            
            _LOGGER.info("Dashboard YAML generated at %s", yaml_path)
            
            return {
                "success": True,
                "path": str(yaml_path),
                "views_count": views_count,
                "instructions": instructions,
                "message": f"Dashboard YAML generated with {views_count} views at {yaml_path}",
            }

        except Exception as err:
            _LOGGER.error("Error generating dashboard YAML: %s", err, exc_info=True)
            return {
                "success": False,
                "error": str(err),
            }

    def _write_yaml_file(self, path: Path, config: dict[str, Any]) -> None:
        """Write dashboard configuration to YAML file (synchronous for executor)."""
        import yaml
        
        with open(path, "w", encoding="utf-8") as f:
            # Add header comment
            f.write("# Smart Appliances Dashboard\n")
            f.write("# Generated by Smart Appliance Monitor integration\n")
            f.write(f"# Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("# Do not edit manually - regenerate via service call\n\n")
            
            # Write YAML
            yaml.dump(config, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        
        _LOGGER.info("Dashboard YAML file written to %s", path)
    
    def _generate_config_instructions(self, yaml_path: Path) -> str:
        """Generate configuration instructions for the user."""
        # Get relative path from HA config directory
        try:
            rel_path = yaml_path.relative_to(self.hass.config.path())
        except ValueError:
            rel_path = yaml_path
        
        instructions = f"""📋 Configuration requise dans configuration.yaml :

lovelace:
  mode: storage
  dashboards:
    smart-appliances:
      mode: yaml
      title: "Smart Appliances"
      icon: mdi:lightning-bolt
      filename: {rel_path}

Après avoir ajouté cette configuration :
1. Vérifiez la configuration (Outils Développeur > YAML > Vérifier la configuration)
2. Redémarrez Home Assistant
3. Le dashboard apparaîtra dans la sidebar avec l'icône ⚡

Le fichier a été créé à : {yaml_path}"""
        
        return instructions

    async def _async_register_dashboard(self) -> None:
        """Register the dashboard in Home Assistant's Lovelace system."""
        try:
            # Import storage helper
            from homeassistant.helpers.storage import Store
            
            # Load the lovelace_dashboards storage
            store = Store(self.hass, 1, "lovelace_dashboards")
            data = await store.async_load()
            
            if data is None:
                data = {"items": []}
            
            # Check if our dashboard is already registered
            dashboard_id = "smart_appliances"
            existing = next(
                (item for item in data.get("items", []) if item.get("id") == dashboard_id),
                None
            )
            
            if existing:
                _LOGGER.debug("Dashboard %s already registered", dashboard_id)
                # Dashboard already registered, just reload to refresh
                await self._async_reload_lovelace()
                return
            
            # Add our dashboard to the list
            dashboard_config = {
                "id": dashboard_id,
                "show_in_sidebar": True,
                "icon": DASHBOARD_ICON,
                "title": DASHBOARD_TITLE,
                "require_admin": False,
                "mode": "storage",
                "url_path": DASHBOARD_URL_PATH,
            }
            
            data.setdefault("items", []).append(dashboard_config)
            
            # Save the updated configuration
            await store.async_save(data)
            
            _LOGGER.info("Dashboard %s registered in Home Assistant dashboard list", DASHBOARD_URL_PATH)
            
            # Reload Lovelace to make the dashboard appear immediately
            await self._async_reload_lovelace()
            
        except Exception as err:
            _LOGGER.warning("Could not register dashboard: %s", err)
            # This is not critical - the dashboard will still work via direct URL

    async def _async_reload_lovelace(self) -> None:
        """Reload Lovelace configuration to refresh the dashboard list."""
        try:
            # Fire an event to reload Lovelace
            self.hass.bus.async_fire("lovelace_updated")
            _LOGGER.debug("Lovelace reload event fired")
        except Exception as err:
            _LOGGER.debug("Could not fire Lovelace reload event: %s", err)

    async def _async_build_dashboard_config(self) -> dict[str, Any]:
        """Build complete dashboard configuration."""
        config = await self.config_manager.async_get_config()

        # Get all coordinators
        coordinators = self._get_all_coordinators()

        # Build views
        views = []

        # 1. Overview view (always first)
        overview_view = await self._async_build_overview_view(coordinators)
        views.append(overview_view)

        # 2. Individual appliance views
        for coordinator in coordinators:
            appliance_id = self._get_appliance_id(coordinator)
            view_config = config.get_appliance_view_config(appliance_id)

            if view_config.get("enabled", True):
                _LOGGER.debug("Building view for %s", appliance_id)
                appliance_view = await self._async_build_appliance_view(
                    coordinator, view_config
                )
                if appliance_view:
                    views.append(appliance_view)

        # Build complete dashboard config
        dashboard_config = {
            "title": DASHBOARD_TITLE,
            "icon": DASHBOARD_ICON,
            "views": views,
        }

        return dashboard_config

    async def _async_build_overview_view(
        self, coordinators: list[SmartApplianceCoordinator]
    ) -> dict[str, Any]:
        """Build the overview view with dynamic cards."""
        config = await self.config_manager.async_get_config()
        use_custom_cards = config.global_settings.get("use_custom_cards", True)

        cards = []

        # 1. Global metrics card
        cards.append(self._build_global_metrics_card(coordinators))

        # 2. Energy consumption cards (Energy Dashboard style)
        if len(coordinators) > 0:
            cards.append(self._build_energy_consumption_today(coordinators))
            if self._custom_cards_available.get("apexcharts_card"):
                cards.append(self._build_energy_graph_7days(coordinators))
                cards.append(self._build_energy_distribution_donut(coordinators))
        
        # 3. Real-time monitoring
        cards.append(self._build_realtime_monitoring_card(coordinators, use_custom_cards))

        # 4. Top consumers
        if len(coordinators) > 0:
            cards.append(self._build_top_consumers_card(coordinators))

        # 5. Power graph
        if self._custom_cards_available.get("apexcharts_card") and len(coordinators) > 0:
            cards.append(self._build_power_graph_card(coordinators))
        elif len(coordinators) > 0:
            cards.append(self._build_power_graph_fallback(coordinators))

        return {
            "title": "Overview",
            "path": "overview",
            "icon": "mdi:home-lightning-bolt",
            "cards": cards,
        }

    def _build_global_metrics_card(self, coordinators: list[SmartApplianceCoordinator]) -> dict[str, Any]:
        """Build global metrics card."""
        entities = []
        
        for coord in coordinators:
            appliance_id = self._get_appliance_id(coord)
            entities.extend([
                f"sensor.{appliance_id}_state",
                f"sensor.{appliance_id}_total_energy_today",
                f"sensor.{appliance_id}_daily_cost",
            ])

        return {
            "type": "markdown",
            "content": f"""# ⚡ Smart Appliances Overview

**Appareils configurés**: {len(coordinators)}

Utilisez les onglets ci-dessus pour accéder aux détails de chaque appareil.""",
        }

    def _build_realtime_monitoring_card(
        self, coordinators: list[SmartApplianceCoordinator], use_custom_cards: bool
    ) -> dict[str, Any]:
        """Build real-time monitoring card using real configured power sensors."""
        if not coordinators:
            return {"type": "markdown", "content": "Aucun appareil configuré"}

        entities = []
        for coord in coordinators:
            appliance_type = coord.entry.data.get(CONF_APPLIANCE_TYPE, "other")
            icon = ICON_MAP.get(appliance_type, "mdi:power-plug")
            
            # Use the REAL configured power_sensor
            power_sensor = coord.entry.data.get("power_sensor")
            if power_sensor and self.hass.states.get(power_sensor):
                entities.append({
                    "entity": power_sensor,  # Real power sensor!
                    "name": coord.appliance_name,
                    "icon": icon,
                })

        return {
            "type": "entities",
            "title": "⚡ Monitoring Temps Réel",
            "entities": entities,
        }

    def _build_top_consumers_card(self, coordinators: list[SmartApplianceCoordinator]) -> dict[str, Any]:
        """Build top consumers card using real SAM-generated daily_energy entities."""
        entities = []
        entity_reg = er.async_get(self.hass)
        
        for coord in coordinators:
            # Find the real daily_energy entity from SAM
            sam_entities = er.async_entries_for_config_entry(entity_reg, coord.entry.entry_id)
            daily_energy = next(
                (e.entity_id for e in sam_entities if "_daily_energy" in e.entity_id or "_total_energy_today" in e.entity_id),
                None
            )
            if daily_energy and self.hass.states.get(daily_energy):
                entities.append(daily_energy)

        return {
            "type": "entities",
            "title": "🔝 Top Consommateurs (Aujourd'hui)",
            "entities": entities,
        }

    def _build_power_graph_card(self, coordinators: list[SmartApplianceCoordinator]) -> dict[str, Any]:
        """Build power graph with apexcharts using real configured power sensors."""
        series = []
        colors = ["#3498db", "#16a085", "#e67e22", "#f39c12", "#9b59b6", "#e74c3c", "#3daae4"]
        
        for idx, coord in enumerate(coordinators):
            # Use the REAL configured power_sensor
            power_sensor = coord.entry.data.get("power_sensor")
            if power_sensor and self.hass.states.get(power_sensor):
                series.append({
                    "entity": power_sensor,  # Real power sensor!
                    "name": coord.appliance_name,
                    "color": colors[idx % len(colors)],
                })

        return {
            "type": "custom:apexcharts-card",
            "header": {
                "show": True,
                "title": "📊 Puissances en Temps Réel (24h)",
                "show_states": True,
            },
            "graph_span": "24h",
            "series": series,
        }

    def _build_power_graph_fallback(self, coordinators: list[SmartApplianceCoordinator]) -> dict[str, Any]:
        """Build power graph fallback with history-graph using real configured power sensors."""
        entities = []
        for coord in coordinators:
            # Use the REAL configured power_sensor
            power_sensor = coord.entry.data.get("power_sensor")
            if power_sensor and self.hass.states.get(power_sensor):
                entities.append(power_sensor)

        return {
            "type": "history-graph",
            "title": "📊 Puissances (24h)",
            "entities": entities,
            "hours_to_show": 24,
        }

    def _build_energy_consumption_today(self, coordinators: list[SmartApplianceCoordinator]) -> dict[str, Any]:
        """Build energy consumption summary card for today (Energy Dashboard style)."""
        entity_reg = er.async_get(self.hass)
        
        # Calculate total energy today
        total_energy = 0.0
        total_cost = 0.0
        
        for coord in coordinators:
            # Get daily energy and cost from coordinator stats
            total_energy += coord.daily_stats.get("total_energy", 0)
            total_cost += coord.daily_stats.get("total_cost", 0)
        
        # Build entities list for display
        entities = []
        for coord in coordinators:
            sam_entities = er.async_entries_for_config_entry(entity_reg, coord.entry.entry_id)
            daily_energy = next(
                (e.entity_id for e in sam_entities if "_daily_energy" in e.entity_id or "_total_energy_today" in e.entity_id),
                None
            )
            if daily_energy and self.hass.states.get(daily_energy):
                entities.append(daily_energy)
        
        return {
            "type": "vertical-stack",
            "cards": [
                {
                    "type": "markdown",
                    "content": f"""## 📊 Consommation Aujourd'hui
                    
**Total**: {round(total_energy, 2)} kWh | {round(total_cost, 2)} €""",
                },
                {
                    "type": "horizontal-stack",
                    "cards": [
                        {
                            "type": "gauge",
                            "entity": entities[idx] if idx < len(entities) else "",
                            "name": coord.appliance_name,
                            "min": 0,
                            "max": 5,
                            "needle": True,
                            "severity": {
                                "green": 0,
                                "yellow": 3,
                                "red": 4,
                            },
                        } for idx, coord in enumerate(coordinators[:3])  # Max 3 gauges per row
                    ]
                } if len(coordinators) > 0 else {},
            ],
        }

    def _build_energy_graph_7days(self, coordinators: list[SmartApplianceCoordinator]) -> dict[str, Any]:
        """Build 7-day energy consumption graph (Energy Dashboard style)."""
        entity_reg = er.async_get(self.hass)
        series = []
        colors = ["#3498db", "#16a085", "#e67e22", "#f39c12", "#9b59b6", "#e74c3c", "#3daae4", "#95a5a6", "#34495e"]
        
        for idx, coord in enumerate(coordinators):
            sam_entities = er.async_entries_for_config_entry(entity_reg, coord.entry.entry_id)
            daily_energy = next(
                (e.entity_id for e in sam_entities if "_daily_energy" in e.entity_id or "_total_energy_today" in e.entity_id),
                None
            )
            if daily_energy and self.hass.states.get(daily_energy):
                series.append({
                    "entity": daily_energy,
                    "name": coord.appliance_name,
                    "color": colors[idx % len(colors)],
                    "type": "column",
                    "group_by": {
                        "func": "sum",
                        "duration": "1d",
                    },
                })
        
        return {
            "type": "custom:apexcharts-card",
            "header": {
                "show": True,
                "title": "📅 Consommation (7 derniers jours)",
                "show_states": True,
            },
            "graph_span": "7d",
            "span": {
                "end": "day",
            },
            "series": series,
        }

    def _build_energy_distribution_donut(self, coordinators: list[SmartApplianceCoordinator]) -> dict[str, Any]:
        """Build energy distribution donut chart (Energy Dashboard style)."""
        entity_reg = er.async_get(self.hass)
        series = []
        colors = ["#3498db", "#16a085", "#e67e22", "#f39c12", "#9b59b6", "#e74c3c", "#3daae4", "#95a5a6", "#34495e"]
        
        for idx, coord in enumerate(coordinators):
            sam_entities = er.async_entries_for_config_entry(entity_reg, coord.entry.entry_id)
            daily_energy = next(
                (e.entity_id for e in sam_entities if "_daily_energy" in e.entity_id or "_total_energy_today" in e.entity_id),
                None
            )
            if daily_energy and self.hass.states.get(daily_energy):
                series.append({
                    "entity": daily_energy,
                    "name": coord.appliance_name,
                    "color": colors[idx % len(colors)],
                })
        
        return {
            "type": "custom:apexcharts-card",
            "header": {
                "show": True,
                "title": "🥧 Répartition de la Consommation",
                "show_states": False,
            },
            "chart_type": "donut",
            "series": series,
        }

    async def _async_build_appliance_view(
        self, coordinator: SmartApplianceCoordinator, view_config: dict[str, Any]
    ) -> dict[str, Any] | None:
        """Build view for a specific appliance using real entities from coordinator."""
        try:
            appliance_id = self._get_appliance_id(coordinator)
            appliance_name = coordinator.appliance_name
            appliance_type = coordinator.entry.data.get(CONF_APPLIANCE_TYPE, "other")

            _LOGGER.debug("Building view for %s (type: %s)", appliance_id, appliance_type)

            # Get icon and color
            icon = ICON_MAP.get(appliance_type, "mdi:power-plug")
            
            # Determine session or cycle
            is_session_based = appliance_type in SESSION_BASED_TYPES
            cycle_or_session = "session" if is_session_based else "cycle"

            # Build cards directly using real entities from coordinator (no mapping!)
            cards = self._build_appliance_cards_direct(
                coordinator, appliance_name, cycle_or_session
            )

            return {
                "title": view_config.get("custom_name") or appliance_name,
                "path": appliance_id,
                "icon": icon,
                "cards": cards,
            }

        except Exception as err:
            _LOGGER.error(
                "Error building view for %s: %s",
                coordinator.appliance_name,
                err,
                exc_info=True,
            )

        return None

    def _build_appliance_cards_direct(
        self,
        coordinator: SmartApplianceCoordinator,
        appliance_name: str,
        cycle_or_session: str
    ) -> list[dict[str, Any]]:
        """Build cards for an appliance directly using real entities (no templates, no mapping)."""
        appliance_id = self._get_appliance_id(coordinator)
        cards = []
        
        # Get configured sensors from entry data
        power_sensor = coordinator.entry.data.get("power_sensor")
        energy_sensor = coordinator.entry.data.get("energy_sensor")
        
        # Get SAM-generated entities via entity registry
        entity_reg = er.async_get(self.hass)
        sam_entities = er.async_entries_for_config_entry(entity_reg, coordinator.entry.entry_id)
        
        # Helper to find entity by suffix
        def find_entity(suffix: str) -> str | None:
            """Find entity ending with suffix."""
            for entity in sam_entities:
                if entity.entity_id.endswith(suffix):
                    return entity.entity_id
            return None
        
        # Helper to add card safely
        def add_card(card_config: dict[str, Any]) -> None:
            """Add card if all entities exist."""
            try:
                # Validate all entities in the card
                entities_to_check = []
                if "entity" in card_config:
                    entities_to_check.append(card_config["entity"])
                if "entities" in card_config:
                    for ent in card_config["entities"]:
                        if isinstance(ent, dict) and "entity" in ent:
                            entities_to_check.append(ent["entity"])
                        elif isinstance(ent, str):
                            entities_to_check.append(ent)
                
                # Check all entities exist
                for ent_id in entities_to_check:
                    if not self.hass.states.get(ent_id):
                        _LOGGER.warning("Entity %s not found, skipping card", ent_id)
                        return
                
                cards.append(card_config)
            except Exception as err:
                _LOGGER.error("Error adding card: %s", err, exc_info=True)
        
        # 1. Status card with configured power sensor
        if power_sensor:
            add_card({
                "type": "gauge",
                "entity": power_sensor,
                "name": "Puissance Actuelle",
                "min": 0,
                "max": 3000,
                "severity": {"green": 0, "yellow": 500, "red": 2000}
            })
        
        # 2. State card
        state_entity = find_entity("_state")
        cycle_duration = find_entity("_cycle_duration") or find_entity("_session_duration")
        energy_per_cycle = find_entity("_energy_per_cycle") or find_entity("_energy_per_session")
        
        status_entities = []
        if state_entity:
            status_entities.append({"entity": state_entity, "name": "État"})
        if power_sensor:
            status_entities.append({"entity": power_sensor, "name": "Puissance"})
        if cycle_duration:
            status_entities.append({"entity": cycle_duration, "name": "Durée"})
        if energy_per_cycle:
            status_entities.append({"entity": energy_per_cycle, "name": "Énergie"})
        
        if status_entities:
            add_card({
                "type": "entities",
                "title": f"🔄 {appliance_name} - Status",
                "entities": status_entities
            })
        
        # 3. Today stats
        today_entities = []
        total_cycles = find_entity("_total_cycles_today") or find_entity("_total_sessions_today") or find_entity("_daily_cycles")
        total_energy = find_entity("_total_energy_today") or find_entity("_daily_energy")
        daily_cost = find_entity("_daily_cost")
        
        if total_cycles:
            today_entities.append({"entity": total_cycles})
        if total_energy:
            today_entities.append({"entity": total_energy})
        if daily_cost:
            today_entities.append({"entity": daily_cost})
        
        if today_entities:
            add_card({
                "type": "entities",
                "title": "📊 Aujourd'hui",
                "entities": today_entities
            })
        
        # 4. Monthly stats
        monthly_entities = []
        monthly_cycles = find_entity("_monthly_cycles") or find_entity("_monthly_sessions")
        monthly_energy = find_entity("_monthly_energy")
        monthly_cost = find_entity("_monthly_cost")
        
        if monthly_cycles:
            monthly_entities.append({"entity": monthly_cycles})
        if monthly_energy:
            monthly_entities.append({"entity": monthly_energy})
        if monthly_cost:
            monthly_entities.append({"entity": monthly_cost})
        
        if monthly_entities:
            add_card({
                "type": "entities",
                "title": "📅 Ce mois",
                "entities": monthly_entities
            })
        
        # 5. Current cycle/session
        current_entities = []
        cycle_energy = find_entity("_cycle_energy") or find_entity("_session_energy")
        cycle_cost = find_entity("_cycle_cost") or find_entity("_session_cost")
        
        if cycle_duration:
            current_entities.append({"entity": cycle_duration})
        if cycle_energy:
            current_entities.append({"entity": cycle_energy})
        if cycle_cost:
            current_entities.append({"entity": cycle_cost})
        
        if current_entities:
            add_card({
                "type": "entities",
                "title": f"⚡ {cycle_or_session.capitalize()} en cours",
                "entities": current_entities
            })
        
        # 6. Power history graph
        if power_sensor:
            add_card({
                "type": "history-graph",
                "title": "📈 Historique Puissance",
                "entities": [power_sensor],
                "hours_to_show": 24
            })
        
        # 7. Controls
        control_entities = []
        monitoring_switch = find_entity("_monitoring")
        notifications_switch = find_entity("_notifications")
        reset_button = find_entity("_reset_stats")
        
        if monitoring_switch:
            control_entities.append({"entity": monitoring_switch})
        if notifications_switch:
            control_entities.append({"entity": notifications_switch})
        if reset_button:
            control_entities.append({"entity": reset_button})
        
        if control_entities:
            add_card({
                "type": "entities",
                "title": "🎛️ Contrôles",
                "entities": control_entities
            })
        
        _LOGGER.debug("Built %d cards for %s", len(cards), appliance_id)
        return cards

    async def async_add_appliance_view(
        self, coordinator: SmartApplianceCoordinator
    ) -> dict[str, Any]:
        """Add a view for a new appliance."""
        appliance_id = self._get_appliance_id(coordinator)
        _LOGGER.info("Adding view for appliance: %s", appliance_id)

        # Regenerate dashboard YAML
        return await self.async_create_or_update_dashboard()

    async def async_remove_appliance_view(self, appliance_id: str) -> dict[str, Any]:
        """Remove a view for an appliance."""
        _LOGGER.info("Removing view for appliance: %s", appliance_id)

        # Remove from config
        await self.config_manager.async_remove_view_config(appliance_id)

        # Regenerate dashboard YAML
        return await self.async_create_or_update_dashboard()

    async def async_rebuild_dashboard(self) -> dict[str, Any]:
        """Rebuild the entire dashboard from scratch."""
        _LOGGER.info("Rebuilding dashboard...")
        return await self.async_create_or_update_dashboard(force_recreate=True)

    def _get_all_coordinators(self) -> list[SmartApplianceCoordinator]:
        """Get all SAM coordinators."""
        coordinators = []
        for entry in self.hass.config_entries.async_entries(DOMAIN):
            coordinator = self.hass.data[DOMAIN].get(entry.entry_id)
            if coordinator and isinstance(coordinator, SmartApplianceCoordinator):
                coordinators.append(coordinator)
        return coordinators

    def _get_appliance_id(self, coordinator: SmartApplianceCoordinator) -> str:
        """Get appliance ID for use in dashboard paths."""
        # Use Home Assistant's slugify to handle accents correctly
        from homeassistant.util import slugify
        return slugify(coordinator.appliance_name)
