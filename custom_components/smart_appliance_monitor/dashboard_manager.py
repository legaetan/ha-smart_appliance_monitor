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
    APPLIANCE_TYPE_AIR_CONDITIONER,
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
    APPLIANCE_TYPE_AIR_CONDITIONER: "air_conditioner",
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
    APPLIANCE_TYPE_AIR_CONDITIONER: "mdi:air-conditioner",
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

        # 2. Cost overview grid - NEW: Compact view of all appliances with costs
        if len(coordinators) > 0:
            cards.append(self._build_appliances_cost_grid_card(coordinators))

        # 3. Energy consumption cards (Energy Dashboard style)
        if len(coordinators) > 0:
            cards.append(self._build_energy_consumption_today(coordinators))
            if self._custom_cards_available.get("apexcharts_card"):
                cards.append(self._build_energy_graph_7days(coordinators))
                cards.append(self._build_energy_distribution_donut(coordinators))
        
        # 4. Real-time monitoring
        cards.append(self._build_realtime_monitoring_card(coordinators, use_custom_cards))

        # 5. Top consumers
        if len(coordinators) > 0:
            cards.append(self._build_top_consumers_card(coordinators))

        # 6. Power graph
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
    
    def _get_cost_color(self, cost: float) -> str:
        """Get color for cost bar based on amount."""
        if cost < 1.0:
            return "#2ecc71"  # Green
        elif cost < 5.0:
            return "#f39c12"  # Orange
        else:
            return "#e74c3c"  # Red
    
    def _build_appliances_cost_grid_card(
        self, coordinators: list[SmartApplianceCoordinator]
    ) -> dict[str, Any]:
        """Build cost overview table card with graphical elements."""
        if not coordinators:
            return None
        
        # Collect data from all coordinators
        appliances_data = []
        max_daily_cost = 0.01  # Minimum to avoid division by zero
        max_monthly_cost = 0.01
        
        for coord in coordinators:
            appliance_type = coord.entry.data.get(CONF_APPLIANCE_TYPE, "other")
            icon = ICON_MAP.get(appliance_type, "mdi:power-plug")
            
            daily_cost = coord.daily_stats.get("total_cost", 0)
            monthly_cost = coord.monthly_stats.get("total_cost", 0)
            daily_cycles = coord.daily_stats.get("cycle_count", 0)
            monthly_cycles = coord.monthly_stats.get("cycle_count", 0)
            
            max_daily_cost = max(max_daily_cost, daily_cost)
            max_monthly_cost = max(max_monthly_cost, monthly_cost)
            
            appliances_data.append({
                "name": coord.appliance_name,
                "icon": icon,
                "state": coord.state_machine.state,
                "daily_cycles": daily_cycles,
                "monthly_cycles": monthly_cycles,
                "daily_cost": daily_cost,
                "monthly_cost": monthly_cost,
                "currency": coord.currency,
            })
        
        # Sort by monthly cost descending
        appliances_data.sort(key=lambda x: x["monthly_cost"], reverse=True)
        
        # Generate HTML table rows
        rows = []
        for data in appliances_data:
            # Calculate bar widths
            daily_bar_width = (data["daily_cost"] / max_daily_cost * 100) if max_daily_cost > 0 else 0
            monthly_bar_width = (data["monthly_cost"] / max_monthly_cost * 100) if max_monthly_cost > 0 else 0
            
            # Determine bar colors
            daily_bar_color = self._get_cost_color(data["daily_cost"])
            monthly_bar_color = self._get_cost_color(data["monthly_cost"])
            
            # State badge
            state_class = f"status-{data['state']}"
            state_label = data['state'].capitalize()
            
            row_html = f"""
        <tr>
          <td>
            <div style="display: flex; align-items: center; gap: 8px;">
              <span class="appliance-icon">{data['icon']}</span>
              <strong>{data['name']}</strong>
            </div>
          </td>
          <td><span class="status-badge {state_class}">{state_label}</span></td>
          <td style="text-align: center;"><strong>{data['daily_cycles']}</strong></td>
          <td style="text-align: center;"><strong>{data['monthly_cycles']}</strong></td>
          <td>
            <div class="metric-value">{data['daily_cost']:.2f} {data['currency']}</div>
            <div class="cost-bar" style="width: {daily_bar_width:.0f}%; background: {daily_bar_color};"></div>
          </td>
          <td>
            <div class="metric-value">{data['monthly_cost']:.2f} {data['currency']}</div>
            <div class="cost-bar" style="width: {monthly_bar_width:.0f}%; background: {monthly_bar_color};"></div>
          </td>
        </tr>
            """
            rows.append(row_html)
        
        # Build complete markdown with CSS
        table_html = "\n".join(rows)
        content = f"""<style>
.cost-overview-table {{
  width: 100%;
  border-collapse: collapse;
  margin-top: 16px;
  font-size: 0.95em;
}}
.cost-overview-table th {{
  background: var(--primary-color);
  color: white;
  padding: 14px 12px;
  text-align: left;
  font-weight: 600;
  font-size: 0.9em;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}}
.cost-overview-table td {{
  padding: 14px 12px;
  border-bottom: 1px solid var(--divider-color);
  vertical-align: middle;
}}
.cost-overview-table tr:hover {{
  background: var(--table-row-background-hover-color, rgba(var(--rgb-primary-color), 0.05));
}}
.cost-overview-table tr:last-child td {{
  border-bottom: none;
}}
.appliance-icon {{
  font-size: 1.8em;
}}
.status-badge {{
  display: inline-block;
  padding: 6px 12px;
  border-radius: 14px;
  font-size: 0.8em;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}}
.status-idle {{
  background: #95a5a6;
  color: white;
}}
.status-running {{
  background: #3498db;
  color: white;
  animation: pulse 2s ease-in-out infinite;
}}
.status-finished {{
  background: #2ecc71;
  color: white;
}}
.status-analyzing {{
  background: #9b59b6;
  color: white;
}}
@keyframes pulse {{
  0%, 100% {{ opacity: 1; }}
  50% {{ opacity: 0.7; }}
}}
.cost-bar {{
  height: 8px;
  background: var(--primary-color);
  border-radius: 4px;
  margin-top: 6px;
  transition: width 0.3s ease;
}}
.metric-value {{
  font-size: 1.15em;
  font-weight: 700;
  color: var(--primary-text-color);
}}
</style>

<table class="cost-overview-table">
  <thead>
    <tr>
      <th>🏠 Appareil</th>
      <th>📊 État</th>
      <th style="text-align: center;">🔄 Cycles Aujourd'hui</th>
      <th style="text-align: center;">📅 Cycles Mois</th>
      <th>💰 Coût Aujourd'hui</th>
      <th>💰 Coût Mensuel</th>
    </tr>
  </thead>
  <tbody>
{table_html}
  </tbody>
</table>
"""
        
        return {
            "type": "markdown",
            "title": "💰 Vue d'Ensemble des Coûts",
            "content": content,
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

    def _build_appliances_cost_grid_card(self, coordinators: list[SmartApplianceCoordinator]) -> dict[str, Any]:
        """Build compact cost overview card for all appliances."""
        if not coordinators:
            return {"type": "markdown", "content": "Aucun appareil configuré"}

        entities = []
        
        for coord in coordinators:
            appliance_id = self._get_appliance_id(coord)
            appliance_type = coord.entry.data.get(CONF_APPLIANCE_TYPE, "other")
            icon = ICON_MAP.get(appliance_type, "mdi:power-plug")
            
            # Add header/separator for each appliance
            entities.append({
                "type": "section",
                "label": coord.appliance_name,
            })
            
            # State sensor
            state_entity = f"sensor.{appliance_id}_state"
            if self.hass.states.get(state_entity):
                entities.append({
                    "entity": state_entity,
                    "name": "État",
                    "icon": icon,
                })
            
            # Daily cycles
            daily_cycles_entity = f"sensor.{appliance_id}_daily_cycles"
            if self.hass.states.get(daily_cycles_entity):
                entities.append({
                    "entity": daily_cycles_entity,
                    "name": "Cycles aujourd'hui",
                    "icon": "mdi:refresh",
                })
            
            # Daily cost
            daily_cost_entity = f"sensor.{appliance_id}_daily_cost"
            if self.hass.states.get(daily_cost_entity):
                entities.append({
                    "entity": daily_cost_entity,
                    "name": "Coût aujourd'hui",
                })
            
            # Monthly cost
            monthly_cost_entity = f"sensor.{appliance_id}_monthly_cost"
            if self.hass.states.get(monthly_cost_entity):
                entities.append({
                    "entity": monthly_cost_entity,
                    "name": "Coût mensuel",
                })

        return {
            "type": "entities",
            "title": "💰 Vue d'ensemble des Coûts",
            "entities": entities,
            "state_color": True,
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
            
            # Merge dashboard sections from entry.options if present
            entry_sections = coordinator.entry.options.get("dashboard_sections_visible", {})
            if entry_sections:
                # Merge entry options with view config
                if "sections_visible" not in view_config:
                    view_config["sections_visible"] = {}
                view_config["sections_visible"].update(entry_sections)

            # Build cards directly using real entities from coordinator (no mapping!)
            cards = self._build_appliance_cards_direct(
                coordinator, appliance_name, cycle_or_session, view_config
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

    def _build_statistics_advanced_card(
        self,
        coordinator: SmartApplianceCoordinator,
        appliance_name: str,
        cycle_or_session: str,
        find_entity: callable,
    ) -> dict[str, Any] | None:
        """Build advanced statistics card with frequency, averages, and trends."""
        # Calculate advanced metrics from coordinator data
        daily_stats = coordinator.daily_stats or {}
        monthly_stats = coordinator.monthly_stats or {}

        # Resolve cycle counters (support both legacy and new keys)
        total_cycles_today = daily_stats.get("cycles", daily_stats.get("cycle_count", 0))
        total_cycles_month = monthly_stats.get("cycles", monthly_stats.get("cycle_count", 0))

        # If monthly cycles not tracked, approximate from history for current month
        try:
            if not total_cycles_month and hasattr(coordinator, "_cycle_history"):
                from datetime import datetime as _dt
                total_cycles_month = sum(
                    1
                    for c in coordinator._cycle_history
                    if isinstance(c.get("timestamp"), _dt)
                    and c["timestamp"].year == _dt.now().year
                    and c["timestamp"].month == _dt.now().month
                )
        except Exception:
            pass

        # Calculate frequency (cycles per day based on monthly average)
        days_in_month = 30  # Approximation
        freq_per_day = round(total_cycles_month / days_in_month, 1) if total_cycles_month > 0 else 0
        freq_per_week = round(freq_per_day * 7, 1)

        # Average duration/energy/cost for today
        # Prefer values from stats; otherwise compute from cycle history
        avg_duration_sec = daily_stats.get("avg_duration", 0)
        avg_energy = daily_stats.get("avg_energy", 0)
        avg_cost = daily_stats.get("avg_cost", 0)

        if (not avg_duration_sec) or (not avg_energy and total_cycles_today) or (not avg_cost and total_cycles_today):
            try:
                from datetime import datetime as _dt
                today = _dt.now().date()
                durations_min = []
                energies_kwh = []
                costs = []
                if hasattr(coordinator, "_cycle_history"):
                    for c in coordinator._cycle_history:
                        ts = c.get("timestamp")
                        if isinstance(ts, _dt) and ts.date() == today:
                            # History stores duration in minutes and energy in kWh
                            if "duration" in c:
                                durations_min.append(float(c.get("duration", 0)))
                            if "energy" in c:
                                energies_kwh.append(float(c.get("energy", 0)))
                            if "energy" in c:
                                costs.append(float(c.get("energy", 0)) * coordinator.price_kwh)
                n = len(durations_min)
                if n > 0:
                    avg_duration_sec = sum(durations_min) / n * 60
                if total_cycles_today:
                    # If totals exist, use them; otherwise compute from history
                    if daily_stats.get("total_energy") is not None:
                        avg_energy = daily_stats.get("total_energy", 0) / max(1, total_cycles_today)
                    elif energies_kwh:
                        avg_energy = sum(energies_kwh) / n
                    if daily_stats.get("total_cost") is not None:
                        avg_cost = daily_stats.get("total_cost", 0) / max(1, total_cycles_today)
                    elif costs:
                        avg_cost = sum(costs) / n
            except Exception:
                pass

        avg_duration_min = round(avg_duration_sec / 60, 0) if avg_duration_sec > 0 else 0

        # Total usage time today/month (hours)
        total_usage_today_h = 0.0
        total_usage_month_h = 0.0
        try:
            if daily_stats.get("total_duration"):
                total_usage_today_h = round(daily_stats.get("total_duration", 0) / 3600, 1)
            else:
                # Fallback: compute from history
                from datetime import datetime as _dt
                today = _dt.now().date()
                total_usage_today_h = round(
                    sum((c.get("duration", 0) for c in getattr(coordinator, "_cycle_history", []) if isinstance(c.get("timestamp"), _dt) and c["timestamp"].date() == today)) / 60,
                    1,
                )
            if monthly_stats.get("total_duration"):
                total_usage_month_h = round(monthly_stats.get("total_duration", 0) / 3600, 1)
            else:
                from datetime import datetime as _dt
                now = _dt.now()
                total_usage_month_h = round(
                    sum((c.get("duration", 0) for c in getattr(coordinator, "_cycle_history", []) if isinstance(c.get("timestamp"), _dt) and c["timestamp"].year == now.year and c["timestamp"].month == now.month)) / 60,
                    1,
                )
        except Exception:
            pass

        # Build markdown content
        content = f"""## 📊 Statistiques Avancées

**Fréquence d'utilisation:**
- Aujourd'hui: {total_cycles_today} {cycle_or_session}(s)
- Ce mois: {total_cycles_month} {cycle_or_session}(s)
- Moyenne: {freq_per_day} {cycle_or_session}/jour | {freq_per_week} {cycle_or_session}/semaine

**Moyennes par {cycle_or_session}:**
- Durée: {avg_duration_min} min
- Énergie: {round(avg_energy, 2)} kWh
- Coût: {round(avg_cost, 2)} {coordinator.currency}

**Temps d'utilisation:**
- Aujourd'hui: {total_usage_today_h} h
- Ce mois: {total_usage_month_h} h
"""
        
        return {
            "type": "markdown",
            "title": "📊 Statistiques Avancées",
            "content": content,
        }

    def _build_ai_actions_card(
        self,
        coordinator: SmartApplianceCoordinator,
        appliance_id: str,
        find_entity: callable,
    ) -> dict[str, Any] | None:
        """Build AI actions card with service buttons and last analysis display."""
        state_entity = find_entity("_state")
        if not state_entity:
            return None
        
        # Check if AI analysis entity exists
        ai_analysis_entity = find_entity("_ai_analysis")
        
        cards = [
            {
                "type": "markdown",
                "content": "## 🤖 Actions IA"
            },
            {
                "type": "entities",
                "title": "Analyses Disponibles",
                "entities": [
                    {
                        "type": "button",
                        "name": "🔍 Analyser les Cycles (Complet)",
                        "tap_action": {
                            "action": "call-service",
                            "service": "smart_appliance_monitor.analyze_cycles",
                            "service_data": {
                                "entity_id": state_entity,
                                "analysis_type": "all",
                                "cycle_count": 10,
                            },
                        },
                    },
                    {
                        "type": "button",
                        "name": "💡 Obtenir Recommandations",
                        "tap_action": {
                            "action": "call-service",
                            "service": "smart_appliance_monitor.analyze_cycles",
                            "service_data": {
                                "entity_id": state_entity,
                                "analysis_type": "recommendations",
                                "cycle_count": 10,
                            },
                        },
                    },
                    {
                        "type": "button",
                        "name": "📈 Analyser Patterns",
                        "tap_action": {
                            "action": "call-service",
                            "service": "smart_appliance_monitor.analyze_cycles",
                            "service_data": {
                                "entity_id": state_entity,
                                "analysis_type": "pattern",
                                "cycle_count": 10,
                            },
                        },
                    },
                ],
            },
        ]
        
        # Add last analysis display if entity exists
        if ai_analysis_entity and self.hass.states.get(ai_analysis_entity):
            cards.append({
                "type": "entities",
                "title": "📝 Dernière Analyse IA",
                "entities": [
                    {
                        "entity": ai_analysis_entity,
                        "type": "attribute",
                        "attribute": "summary",
                        "name": "Résumé",
                    },
                    {
                        "entity": ai_analysis_entity,
                        "type": "attribute",
                        "attribute": "status",
                        "name": "Statut",
                    },
                    {
                        "entity": ai_analysis_entity,
                        "type": "attribute",
                        "attribute": "last_analysis_date",
                        "name": "Analysé le",
                    },
                ],
            })
        else:
            cards.append({
                "type": "markdown",
                "content": "ℹ️ *Configuration IA requise via service `set_global_config`*",
            })
        
        return {
            "type": "vertical-stack",
            "cards": cards,
        }

    def _build_services_card(
        self,
        coordinator: SmartApplianceCoordinator,
        appliance_id: str,
        find_entity: callable,
    ) -> dict[str, Any] | None:
        """Build services card with all available actions."""
        state_entity = find_entity("_state")
        if not state_entity:
            return None
        
        entities = [
            {
                "type": "button",
                "name": "📤 Exporter en CSV",
                "tap_action": {
                    "action": "call-service",
                    "service": "smart_appliance_monitor.export_to_csv",
                    "service_data": {
                        "entity_id": state_entity,
                    },
                },
            },
            {
                "type": "button",
                "name": "📤 Exporter en JSON",
                "tap_action": {
                    "action": "call-service",
                    "service": "smart_appliance_monitor.export_to_json",
                    "service_data": {
                        "entity_id": state_entity,
                    },
                },
            },
            {
                "type": "button",
                "name": "🔄 Sync Energy Dashboard",
                "tap_action": {
                    "action": "call-service",
                    "service": "smart_appliance_monitor.sync_with_energy_dashboard",
                    "service_data": {
                        "entity_id": state_entity,
                    },
                },
            },
            {
                "type": "button",
                "name": "📜 Obtenir Historique",
                "tap_action": {
                    "action": "call-service",
                    "service": "smart_appliance_monitor.get_cycle_history",
                    "service_data": {
                        "entity_id": state_entity,
                    },
                },
            },
            {
                "type": "button",
                "name": "📥 Importer Historique",
                "tap_action": {
                    "action": "call-service",
                    "service": "smart_appliance_monitor.import_historical_cycles",
                    "service_data": {
                        "entity_id": state_entity,
                        "dry_run": True,
                    },
                },
            },
        ]
        
        # Add auto-shutdown button if enabled
        if coordinator.entry.options.get("enable_auto_shutdown", False):
            entities.append({
                "type": "button",
                "name": "⚡ Force Shutdown",
                "tap_action": {
                    "action": "call-service",
                    "service": "smart_appliance_monitor.force_shutdown",
                    "service_data": {
                        "entity_id": state_entity,
                    },
                },
            })
        
        return {
            "type": "entities",
            "title": "🛠️ Services & Actions",
            "entities": entities,
        }

    def _build_appliance_cards_direct(
        self,
        coordinator: SmartApplianceCoordinator,
        appliance_name: str,
        cycle_or_session: str,
        view_config: dict[str, Any]
    ) -> list[dict[str, Any]]:
        """Build cards for an appliance directly using real entities (no templates, no mapping)."""
        appliance_id = self._get_appliance_id(coordinator)
        cards = []
        
        # Get sections visibility configuration
        from .dashboard_config import DEFAULT_APPLIANCE_SECTIONS
        sections_visible = view_config.get("sections_visible", DEFAULT_APPLIANCE_SECTIONS)
        
        _LOGGER.info("Building cards for appliance: %s (type: %s, cycle_or_session: %s)", 
                     appliance_name, coordinator.entry.data.get(CONF_APPLIANCE_TYPE), cycle_or_session)
        
        # Get configured sensors from entry data
        power_sensor = coordinator.entry.data.get("power_sensor")
        energy_sensor = coordinator.entry.data.get("energy_sensor")
        
        _LOGGER.info("Configured sensors - power: %s, energy: %s", power_sensor, energy_sensor)
        
        # Get SAM-generated entities via entity registry
        entity_reg = er.async_get(self.hass)
        sam_entities = er.async_entries_for_config_entry(entity_reg, coordinator.entry.entry_id)
        
        _LOGGER.info("Found %d SAM entities for %s: %s", 
                     len(sam_entities), appliance_name, 
                     [e.entity_id for e in sam_entities])
        
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
                        _LOGGER.warning("Entity %s not found for %s, skipping card: %s", 
                                       ent_id, appliance_name, card_config.get("title", "Unknown"))
                        return
                
                cards.append(card_config)
                _LOGGER.debug("Added card: %s with %d entities", 
                             card_config.get("title", card_config.get("type")), len(entities_to_check))
            except Exception as err:
                _LOGGER.error("Error adding card for %s: %s", appliance_name, err, exc_info=True)
        
        # 1. Status card with configured power sensor
        if sections_visible.get("status", True) and power_sensor:
            add_card({
                "type": "gauge",
                "entity": power_sensor,
                "name": "Puissance Actuelle",
                "min": 0,
                "max": 3000,
                "severity": {"green": 0, "yellow": 500, "red": 2000}
            })
        
        # 2. State card (basic status)
        if sections_visible.get("status", True):
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
        
        # 3. Today stats (basic statistics)
        if sections_visible.get("statistics_basic", True):
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
        
        # 4. Monthly stats (basic statistics)
        if sections_visible.get("statistics_basic", True):
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
        
        # 5. Advanced statistics card (NEW)
        if sections_visible.get("statistics_advanced", True):
            adv_stats_card = self._build_statistics_advanced_card(
                coordinator, appliance_name, cycle_or_session, find_entity
            )
            if adv_stats_card:
                cards.append(adv_stats_card)
        
        # 6. Current cycle/session
        if sections_visible.get("current_cycle", True):
            current_entities = []
            cycle_duration = find_entity("_cycle_duration") or find_entity("_session_duration")
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
        
        # 7. Power history graph
        if sections_visible.get("power_graph", True) and power_sensor:
            add_card({
                "type": "history-graph",
                "title": "📈 Historique Puissance",
                "entities": [power_sensor],
                "hours_to_show": 24
            })
        
        # 8. AI Actions card (NEW)
        if sections_visible.get("ai_actions", True):
            ai_card = self._build_ai_actions_card(coordinator, appliance_id, find_entity)
            if ai_card:
                cards.append(ai_card)
        
        # 9. Services card (NEW)
        if sections_visible.get("services", True):
            services_card = self._build_services_card(coordinator, appliance_id, find_entity)
            if services_card:
                cards.append(services_card)
        
        # 10. Controls
        if sections_visible.get("controls", True):
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
        
        _LOGGER.info("✅ Built %d cards for %s", len(cards), appliance_name)
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
