"""Module d'export de données pour Smart Appliance Monitor."""
from __future__ import annotations

import csv
import json
import logging
from datetime import datetime
from io import StringIO
from pathlib import Path
from typing import Any

from homeassistant.core import HomeAssistant

from .coordinator import SmartApplianceCoordinator

_LOGGER = logging.getLogger(__name__)


class SmartApplianceDataExporter:
    """Gestionnaire d'export de données pour un appareil."""

    def __init__(self, coordinator: SmartApplianceCoordinator) -> None:
        """Initialise l'exporteur.
        
        Args:
            coordinator: Coordinator de l'appareil
        """
        self.coordinator = coordinator
        self.hass = coordinator.hass
        self.appliance_name = coordinator.appliance_name

    def export_to_csv(self, file_path: str | None = None) -> str:
        """Exporte les données en format CSV.
        
        Args:
            file_path: Chemin du fichier de sortie (optionnel)
            
        Returns:
            Contenu CSV en string
        """
        output = StringIO()
        writer = csv.writer(output)
        
        # En-têtes
        writer.writerow([
            "Timestamp",
            "Appliance",
            "Type",
            "State",
            "Power (W)",
            "Energy (kWh)",
            "Cost (EUR)",
            "Duration (min)",
        ])
        
        # Cycle en cours
        if self.coordinator.state_machine.current_cycle:
            cycle = self.coordinator.state_machine.current_cycle
            writer.writerow([
                cycle.get("start_time", ""),
                self.appliance_name,
                self.coordinator.appliance_type,
                "running",
                self.coordinator.data.get("power", 0),
                round(cycle.get("energy", 0), 3),
                round(cycle.get("energy", 0) * self.coordinator.price_kwh, 2),
                round(cycle.get("duration", 0), 1),
            ])
        
        # Dernier cycle
        if self.coordinator.state_machine.last_cycle:
            cycle = self.coordinator.state_machine.last_cycle
            writer.writerow([
                cycle.get("end_time", ""),
                self.appliance_name,
                self.coordinator.appliance_type,
                "finished",
                0,
                round(cycle.get("energy", 0), 3),
                round(cycle.get("energy", 0) * self.coordinator.price_kwh, 2),
                round(cycle.get("duration", 0), 1),
            ])
        
        # Statistiques journalières
        daily = self.coordinator.daily_stats
        writer.writerow([])
        writer.writerow(["Daily Statistics", "", "", "", "", "", "", ""])
        writer.writerow([
            daily.get("date", ""),
            self.appliance_name,
            "daily_summary",
            "",
            "",
            round(daily.get("total_energy", 0), 3),
            round(daily.get("total_cost", 0), 2),
            "",
        ])
        writer.writerow([
            "Cycles",
            daily.get("cycles", 0),
            "", "", "", "", "", ""
        ])
        
        # Statistiques mensuelles
        monthly = self.coordinator.monthly_stats
        writer.writerow([])
        writer.writerow(["Monthly Statistics", "", "", "", "", "", "", ""])
        writer.writerow([
            f"{monthly.get('year', '')}-{monthly.get('month', '')}",
            self.appliance_name,
            "monthly_summary",
            "",
            "",
            round(monthly.get("total_energy", 0), 3),
            round(monthly.get("total_cost", 0), 2),
            "",
        ])
        
        csv_content = output.getvalue()
        output.close()
        
        # Écrire dans un fichier si demandé
        if file_path:
            try:
                Path(file_path).write_text(csv_content, encoding="utf-8")
                _LOGGER.info("Données exportées en CSV vers %s", file_path)
            except Exception as err:
                _LOGGER.error("Erreur lors de l'écriture du fichier CSV: %s", err)
        
        return csv_content

    def export_to_json(self, file_path: str | None = None) -> str:
        """Exporte les données en format JSON.
        
        Args:
            file_path: Chemin du fichier de sortie (optionnel)
            
        Returns:
            Contenu JSON en string
        """
        data = {
            "export_date": datetime.now().isoformat(),
            "appliance": {
                "name": self.appliance_name,
                "type": self.coordinator.appliance_type,
            },
            "configuration": {
                "start_threshold": self.coordinator.start_threshold,
                "stop_threshold": self.coordinator.stop_threshold,
                "start_delay": self.coordinator.start_delay,
                "stop_delay": self.coordinator.stop_delay,
                "price_kwh": self.coordinator.price_kwh,
            },
            "current_state": {
                "state": self.coordinator.state_machine.state,
                "power": self.coordinator.data.get("power", 0),
                "monitoring_enabled": self.coordinator.monitoring_enabled,
            },
            "current_cycle": None,
            "last_cycle": None,
            "daily_stats": {
                "date": str(self.coordinator.daily_stats.get("date", "")),
                "cycles": self.coordinator.daily_stats.get("cycles", 0),
                "total_energy_kwh": round(self.coordinator.daily_stats.get("total_energy", 0), 3),
                "total_cost_eur": round(self.coordinator.daily_stats.get("total_cost", 0), 2),
            },
            "monthly_stats": {
                "year": self.coordinator.monthly_stats.get("year", 0),
                "month": self.coordinator.monthly_stats.get("month", 0),
                "total_energy_kwh": round(self.coordinator.monthly_stats.get("total_energy", 0), 3),
                "total_cost_eur": round(self.coordinator.monthly_stats.get("total_cost", 0), 2),
            },
        }
        
        # Ajouter le cycle en cours
        if self.coordinator.state_machine.current_cycle:
            cycle = self.coordinator.state_machine.current_cycle
            data["current_cycle"] = {
                "start_time": cycle.get("start_time", "").isoformat() if cycle.get("start_time") else None,
                "duration_minutes": round(cycle.get("duration", 0), 1),
                "energy_kwh": round(cycle.get("energy", 0), 3),
                "peak_power_w": cycle.get("peak_power", 0),
            }
        
        # Ajouter le dernier cycle
        if self.coordinator.state_machine.last_cycle:
            cycle = self.coordinator.state_machine.last_cycle
            data["last_cycle"] = {
                "start_time": cycle.get("start_time", "").isoformat() if cycle.get("start_time") else None,
                "end_time": cycle.get("end_time", "").isoformat() if cycle.get("end_time") else None,
                "duration_minutes": round(cycle.get("duration", 0), 1),
                "energy_kwh": round(cycle.get("energy", 0), 3),
                "peak_power_w": cycle.get("peak_power", 0),
            }
        
        # Ajouter l'historique des cycles pour l'anomaly detection
        if self.coordinator.anomaly_detection_enabled and self.coordinator._cycle_history:
            data["cycle_history"] = [
                {
                    "timestamp": cycle["timestamp"].isoformat(),
                    "duration_minutes": round(cycle["duration"], 1),
                    "energy_kwh": round(cycle["energy"], 3),
                    "cost_eur": round(cycle["cost"], 2),
                }
                for cycle in self.coordinator._cycle_history
            ]
        
        json_content = json.dumps(data, indent=2, ensure_ascii=False)
        
        # Écrire dans un fichier si demandé
        if file_path:
            try:
                Path(file_path).write_text(json_content, encoding="utf-8")
                _LOGGER.info("Données exportées en JSON vers %s", file_path)
            except Exception as err:
                _LOGGER.error("Erreur lors de l'écriture du fichier JSON: %s", err)
        
        return json_content

    def get_export_summary(self) -> dict[str, Any]:
        """Retourne un résumé des données disponibles pour l'export.
        
        Returns:
            Dictionnaire avec le résumé
        """
        return {
            "appliance_name": self.appliance_name,
            "has_current_cycle": self.coordinator.state_machine.current_cycle is not None,
            "has_last_cycle": self.coordinator.state_machine.last_cycle is not None,
            "daily_cycles": self.coordinator.daily_stats.get("cycles", 0),
            "history_size": len(self.coordinator._cycle_history) if self.coordinator.anomaly_detection_enabled else 0,
            "export_formats": ["csv", "json"],
        }

    def export_for_ai_analysis(self, cycle_count: int = 10) -> dict[str, Any]:
        """Export data optimized for AI analysis.
        
        Args:
            cycle_count: Number of historical cycles to include
            
        Returns:
            Structured data optimized for AI prompts
        """
        from datetime import datetime
        from statistics import mean, stdev
        
        # Gather cycle history
        cycle_history = []
        if self.coordinator.anomaly_detection_enabled and self.coordinator._cycle_history:
            # Get the most recent cycles
            recent_cycles = self.coordinator._cycle_history[-cycle_count:]
            
            for cycle in recent_cycles:
                cycle_history.append({
                    "timestamp": cycle["timestamp"].isoformat() if hasattr(cycle["timestamp"], "isoformat") else str(cycle["timestamp"]),
                    "duration_minutes": round(cycle["duration"], 1),
                    "energy_kwh": round(cycle["energy"], 3),
                    "cost_eur": round(cycle["cost"], 2),
                    "hour_of_day": cycle["timestamp"].hour if hasattr(cycle["timestamp"], "hour") else 0,
                    "day_of_week": cycle["timestamp"].strftime("%A") if hasattr(cycle["timestamp"], "strftime") else "Unknown",
                })
        
        # Calculate statistics if we have history
        statistics = {}
        if cycle_history:
            durations = [c["duration_minutes"] for c in cycle_history]
            energies = [c["energy_kwh"] for c in cycle_history]
            costs = [c["cost_eur"] for c in cycle_history]
            
            statistics = {
                "duration": {
                    "mean": round(mean(durations), 1) if durations else 0,
                    "min": round(min(durations), 1) if durations else 0,
                    "max": round(max(durations), 1) if durations else 0,
                    "stdev": round(stdev(durations), 1) if len(durations) > 1 else 0,
                },
                "energy": {
                    "mean": round(mean(energies), 3) if energies else 0,
                    "min": round(min(energies), 3) if energies else 0,
                    "max": round(max(energies), 3) if energies else 0,
                    "stdev": round(stdev(energies), 3) if len(energies) > 1 else 0,
                },
                "cost": {
                    "mean": round(mean(costs), 2) if costs else 0,
                    "min": round(min(costs), 2) if costs else 0,
                    "max": round(max(costs), 2) if costs else 0,
                    "stdev": round(stdev(costs), 2) if len(costs) > 1 else 0,
                },
            }
            
            # Analyze temporal patterns
            hours = [c["hour_of_day"] for c in cycle_history]
            days = [c["day_of_week"] for c in cycle_history]
            
            # Most common usage hours
            hour_counts = {}
            for hour in hours:
                hour_counts[hour] = hour_counts.get(hour, 0) + 1
            
            # Most common usage days
            day_counts = {}
            for day in days:
                day_counts[day] = day_counts.get(day, 0) + 1
            
            statistics["patterns"] = {
                "most_common_hours": sorted(hour_counts.items(), key=lambda x: x[1], reverse=True)[:3],
                "most_common_days": sorted(day_counts.items(), key=lambda x: x[1], reverse=True)[:3],
            }
        
        # Build complete export
        export_data = {
            "appliance": {
                "name": self.appliance_name,
                "type": self.coordinator.appliance_type,
            },
            "configuration": {
                "start_threshold_w": self.coordinator.start_threshold,
                "stop_threshold_w": self.coordinator.stop_threshold,
                "start_delay_s": self.coordinator.start_delay,
                "stop_delay_s": self.coordinator.stop_delay,
                "price_kwh_eur": self.coordinator.price_kwh,
            },
            "current_state": {
                "state": self.coordinator.state_machine.state,
                "power_w": self.coordinator.data.get("power", 0),
                "monitoring_enabled": self.coordinator.monitoring_enabled,
            },
            "current_cycle": None,
            "last_cycle": None,
            "cycle_history": cycle_history,
            "statistics": statistics,
            "daily_summary": {
                "date": str(self.coordinator.daily_stats.get("date", "")),
                "cycles": self.coordinator.daily_stats.get("cycles", 0),
                "total_energy_kwh": round(self.coordinator.daily_stats.get("total_energy", 0), 3),
                "total_cost_eur": round(self.coordinator.daily_stats.get("total_cost", 0), 2),
            },
            "monthly_summary": {
                "year": self.coordinator.monthly_stats.get("year", 0),
                "month": self.coordinator.monthly_stats.get("month", 0),
                "total_energy_kwh": round(self.coordinator.monthly_stats.get("total_energy", 0), 3),
                "total_cost_eur": round(self.coordinator.monthly_stats.get("total_cost", 0), 2),
            },
            "export_metadata": {
                "timestamp": datetime.now().isoformat(),
                "cycle_count": len(cycle_history),
            },
        }
        
        # Add current cycle if exists
        if self.coordinator.state_machine.current_cycle:
            cycle = self.coordinator.state_machine.current_cycle
            export_data["current_cycle"] = {
                "start_time": cycle.get("start_time", "").isoformat() if cycle.get("start_time") else None,
                "duration_minutes": round(cycle.get("duration", 0), 1),
                "energy_kwh": round(cycle.get("energy", 0), 3),
                "peak_power_w": cycle.get("peak_power", 0),
            }
        
        # Add last cycle if exists
        if self.coordinator.state_machine.last_cycle:
            cycle = self.coordinator.state_machine.last_cycle
            export_data["last_cycle"] = {
                "start_time": cycle.get("start_time", "").isoformat() if cycle.get("start_time") else None,
                "end_time": cycle.get("end_time", "").isoformat() if cycle.get("end_time") else None,
                "duration_minutes": round(cycle.get("duration", 0), 1),
                "energy_kwh": round(cycle.get("energy", 0), 3),
                "peak_power_w": cycle.get("peak_power", 0),
                "cost_eur": round(cycle.get("energy", 0) * self.coordinator.price_kwh, 2),
            }
        
        return export_data

    def export_cycles_history_csv(self, cycle_count: int = 50) -> str:
        """Export cycle history in CSV format for tabular analysis.
        
        Args:
            cycle_count: Number of cycles to export
            
        Returns:
            CSV content as string
        """
        output = StringIO()
        writer = csv.writer(output)
        
        # Headers
        writer.writerow([
            "Timestamp",
            "Date",
            "Time",
            "Day of Week",
            "Duration (min)",
            "Energy (kWh)",
            "Cost (EUR)",
            "Hour",
        ])
        
        # Export cycle history if available
        if self.coordinator.anomaly_detection_enabled and self.coordinator._cycle_history:
            recent_cycles = self.coordinator._cycle_history[-cycle_count:]
            
            for cycle in recent_cycles:
                timestamp = cycle["timestamp"]
                writer.writerow([
                    timestamp.isoformat() if hasattr(timestamp, "isoformat") else str(timestamp),
                    timestamp.strftime("%Y-%m-%d") if hasattr(timestamp, "strftime") else "",
                    timestamp.strftime("%H:%M:%S") if hasattr(timestamp, "strftime") else "",
                    timestamp.strftime("%A") if hasattr(timestamp, "strftime") else "",
                    round(cycle["duration"], 1),
                    round(cycle["energy"], 3),
                    round(cycle["cost"], 2),
                    timestamp.hour if hasattr(timestamp, "hour") else 0,
                ])
        
        csv_content = output.getvalue()
        output.close()
        
        return csv_content

