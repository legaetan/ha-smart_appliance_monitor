"""Custom Energy Dashboard backend for Smart Appliance Monitor.

This module provides advanced energy analytics and data aggregation for custom dashboards.
"""
from __future__ import annotations

import logging
from datetime import datetime, timedelta
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.components.recorder import get_instance, history
from homeassistant.helpers import entity_registry as er
import homeassistant.util.dt as dt_util

from .const import DOMAIN
from .coordinator import SmartApplianceCoordinator
from .energy_storage import EnergyStorageReader, EnergyStorageError

_LOGGER = logging.getLogger(__name__)


class CustomEnergyDashboard:
    """Custom Energy Dashboard with advanced analytics."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the custom energy dashboard.
        
        Args:
            hass: Home Assistant instance
        """
        self.hass = hass
        self.storage_reader = EnergyStorageReader(hass)

    async def get_period_data(
        self,
        start: datetime,
        end: datetime,
        devices: list[str] | None = None,
    ) -> dict[str, Any]:
        """Get energy data for a specific period.
        
        Args:
            start: Period start datetime
            end: Period end datetime
            devices: Optional list of device names to filter
            
        Returns:
            Energy data for the period
        """
        # Get all SAM coordinators
        coordinators = self._get_coordinators(devices)
        
        period_data = {
            "period": {
                "start": start.isoformat(),
                "end": end.isoformat(),
                "duration_hours": (end - start).total_seconds() / 3600,
            },
            "devices": [],
            "totals": {
                "energy_kwh": 0.0,
                "cost": 0.0,
                "cycles": 0,
            },
        }
        
        for coord in coordinators:
            # For current day, use coordinator stats
            if start.date() == datetime.now().date():
                device_data = {
                    "name": coord.appliance_name,
                    "type": coord.appliance_type,
                    "energy_kwh": round(coord.daily_stats.get("total_energy", 0), 3),
                    "cost": round(coord.daily_stats.get("total_cost", 0), 2),
                    "cycles": coord.daily_stats.get("cycles", 0),
                }
            else:
                # For historical data, would need to query recorder
                # For now, return zeros (would be implemented in full version)
                device_data = {
                    "name": coord.appliance_name,
                    "type": coord.appliance_type,
                    "energy_kwh": 0.0,
                    "cost": 0.0,
                    "cycles": 0,
                }
            
            period_data["devices"].append(device_data)
            period_data["totals"]["energy_kwh"] += device_data["energy_kwh"]
            period_data["totals"]["cost"] += device_data["cost"]
            period_data["totals"]["cycles"] += device_data["cycles"]
        
        # Round totals
        period_data["totals"]["energy_kwh"] = round(period_data["totals"]["energy_kwh"], 3)
        period_data["totals"]["cost"] = round(period_data["totals"]["cost"], 2)
        
        return period_data

    async def get_devices_breakdown(
        self,
        devices: list[str] | None = None,
    ) -> dict[str, Any]:
        """Get energy breakdown by device.
        
        Args:
            devices: Optional list of device names to filter
            
        Returns:
            Breakdown of energy consumption by device
        """
        coordinators = self._get_coordinators(devices)
        
        breakdown = {
            "devices": [],
            "total_energy_kwh": 0.0,
            "total_cost": 0.0,
        }
        
        for coord in coordinators:
            daily_energy = coord.daily_stats.get("total_energy", 0)
            daily_cost = coord.daily_stats.get("total_cost", 0)
            
            device_data = {
                "name": coord.appliance_name,
                "type": coord.appliance_type,
                "daily": {
                    "energy_kwh": round(daily_energy, 3),
                    "cost": round(daily_cost, 2),
                    "cycles": coord.daily_stats.get("cycles", 0),
                },
                "monthly": {
                    "energy_kwh": round(coord.monthly_stats.get("total_energy", 0), 3),
                    "cost": round(coord.monthly_stats.get("total_cost", 0), 2),
                },
            }
            
            breakdown["devices"].append(device_data)
            breakdown["total_energy_kwh"] += daily_energy
            breakdown["total_cost"] += daily_cost
        
        # Calculate percentages
        for device in breakdown["devices"]:
            if breakdown["total_energy_kwh"] > 0:
                device["percentage"] = round(
                    device["daily"]["energy_kwh"] / breakdown["total_energy_kwh"] * 100, 1
                )
            else:
                device["percentage"] = 0.0
        
        # Sort by energy consumption (highest first)
        breakdown["devices"].sort(key=lambda x: x["daily"]["energy_kwh"], reverse=True)
        
        # Round totals
        breakdown["total_energy_kwh"] = round(breakdown["total_energy_kwh"], 3)
        breakdown["total_cost"] = round(breakdown["total_cost"], 2)
        
        return breakdown

    async def get_comparison_data(
        self,
        current_start: datetime,
        current_end: datetime,
        previous_start: datetime,
        previous_end: datetime,
        devices: list[str] | None = None,
    ) -> dict[str, Any]:
        """Get comparison data between two periods.
        
        Args:
            current_start: Current period start
            current_end: Current period end
            previous_start: Previous period start
            previous_end: Previous period end
            devices: Optional list of device names to filter
            
        Returns:
            Comparison data between periods
        """
        current_data = await self.get_period_data(current_start, current_end, devices)
        previous_data = await self.get_period_data(previous_start, previous_end, devices)
        
        # Calculate differences
        energy_diff = current_data["totals"]["energy_kwh"] - previous_data["totals"]["energy_kwh"]
        cost_diff = current_data["totals"]["cost"] - previous_data["totals"]["cost"]
        
        # Calculate percentage changes
        if previous_data["totals"]["energy_kwh"] > 0:
            energy_change_pct = (energy_diff / previous_data["totals"]["energy_kwh"]) * 100
        else:
            energy_change_pct = 0.0 if energy_diff == 0 else 100.0
        
        if previous_data["totals"]["cost"] > 0:
            cost_change_pct = (cost_diff / previous_data["totals"]["cost"]) * 100
        else:
            cost_change_pct = 0.0 if cost_diff == 0 else 100.0
        
        comparison = {
            "current": current_data,
            "previous": previous_data,
            "comparison": {
                "energy_diff_kwh": round(energy_diff, 3),
                "energy_change_pct": round(energy_change_pct, 1),
                "cost_diff": round(cost_diff, 2),
                "cost_change_pct": round(cost_change_pct, 1),
            },
        }
        
        return comparison

    async def get_daily_timeline(
        self,
        date: datetime | None = None,
        devices: list[str] | None = None,
    ) -> dict[str, Any]:
        """Get hourly energy consumption timeline for a day.
        
        Args:
            date: Date to get timeline for (defaults to today)
            devices: Optional list of device names to filter
            
        Returns:
            Hourly breakdown of energy consumption
        """
        if date is None:
            date = datetime.now()
        
        start = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=1)
        
        # Initialize hourly data structure
        timeline = {
            "date": start.date().isoformat(),
            "hourly": [{"hour": h, "energy_kwh": 0.0, "cost": 0.0} for h in range(24)],
            "devices": {},
        }
        
        coordinators = self._get_coordinators(devices)
        
        # For current implementation, we don't have hourly granularity
        # This would require historical data from recorder
        # Placeholder implementation
        for coord in coordinators:
            timeline["devices"][coord.appliance_name] = {
                "type": coord.appliance_type,
                "total_energy_kwh": round(coord.daily_stats.get("total_energy", 0), 3),
                "total_cost": round(coord.daily_stats.get("total_cost", 0), 2),
            }
        
        return timeline

    async def get_top_consumers(
        self,
        period: str = "daily",
        limit: int = 5,
    ) -> list[dict[str, Any]]:
        """Get top energy consumers.
        
        Args:
            period: Period to analyze ("daily" or "monthly")
            limit: Number of top consumers to return
            
        Returns:
            List of top consumers
        """
        coordinators = self._get_coordinators()
        
        consumers = []
        for coord in coordinators:
            if period == "daily":
                energy = coord.daily_stats.get("total_energy", 0)
                cost = coord.daily_stats.get("total_cost", 0)
            else:  # monthly
                energy = coord.monthly_stats.get("total_energy", 0)
                cost = coord.monthly_stats.get("total_cost", 0)
            
            consumers.append({
                "name": coord.appliance_name,
                "type": coord.appliance_type,
                "energy_kwh": round(energy, 3),
                "cost": round(cost, 2),
            })
        
        # Sort by energy consumption
        consumers.sort(key=lambda x: x["energy_kwh"], reverse=True)
        
        # Return top N
        return consumers[:limit]

    async def get_energy_efficiency_score(
        self,
        devices: list[str] | None = None,
    ) -> dict[str, Any]:
        """Calculate energy efficiency scores for devices.
        
        Args:
            devices: Optional list of device names to filter
            
        Returns:
            Efficiency scores and recommendations
        """
        coordinators = self._get_coordinators(devices)
        
        scores = {
            "overall_score": 0.0,
            "devices": [],
            "recommendations": [],
        }
        
        total_score = 0.0
        device_count = 0
        
        for coord in coordinators:
            # Calculate a simple efficiency score based on:
            # - Energy consumption relative to appliance type
            # - Number of cycles
            # - Anomaly score (if available)
            
            daily_energy = coord.daily_stats.get("total_energy", 0)
            cycles = coord.daily_stats.get("cycles", 0)
            
            # Energy per cycle (lower is better)
            if cycles > 0:
                energy_per_cycle = daily_energy / cycles
            else:
                energy_per_cycle = daily_energy
            
            # Simple scoring (0-100, higher is better)
            # This is a placeholder - real implementation would be more sophisticated
            score = max(0, min(100, 100 - (energy_per_cycle * 10)))
            
            device_score = {
                "name": coord.appliance_name,
                "type": coord.appliance_type,
                "score": round(score, 1),
                "energy_kwh": round(daily_energy, 3),
                "cycles": cycles,
                "energy_per_cycle": round(energy_per_cycle, 3) if cycles > 0 else None,
            }
            
            scores["devices"].append(device_score)
            total_score += score
            device_count += 1
            
            # Generate recommendations
            if score < 50:
                scores["recommendations"].append({
                    "device": coord.appliance_name,
                    "severity": "high",
                    "message": f"{coord.appliance_name} has low efficiency score. Consider checking for issues.",
                })
        
        # Calculate overall score
        if device_count > 0:
            scores["overall_score"] = round(total_score / device_count, 1)
        
        # Sort devices by score (lowest first)
        scores["devices"].sort(key=lambda x: x["score"])
        
        return scores

    def _get_coordinators(
        self,
        devices: list[str] | None = None,
    ) -> list[SmartApplianceCoordinator]:
        """Get SAM coordinators, optionally filtered by device names.
        
        Args:
            devices: Optional list of device names to filter
            
        Returns:
            List of coordinators
        """
        all_coordinators = [
            coord for coord in self.hass.data.get(DOMAIN, {}).values()
            if isinstance(coord, SmartApplianceCoordinator)
        ]
        
        if devices:
            return [
                coord for coord in all_coordinators
                if coord.appliance_name in devices
            ]
        
        return all_coordinators

    async def get_dashboard_summary(self) -> dict[str, Any]:
        """Get complete dashboard summary with all key metrics.
        
        Returns:
            Complete dashboard summary
        """
        breakdown = await self.get_devices_breakdown()
        top_consumers = await self.get_top_consumers(limit=3)
        efficiency = await self.get_energy_efficiency_score()
        
        # Get today vs yesterday comparison
        now = datetime.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = now
        yesterday_start = today_start - timedelta(days=1)
        yesterday_end = today_start
        
        comparison = await self.get_comparison_data(
            today_start, today_end,
            yesterday_start, yesterday_end
        )
        
        summary = {
            "timestamp": now.isoformat(),
            "total_devices": len(breakdown["devices"]),
            "today": {
                "energy_kwh": breakdown["total_energy_kwh"],
                "cost": breakdown["total_cost"],
            },
            "vs_yesterday": {
                "energy_diff_kwh": comparison["comparison"]["energy_diff_kwh"],
                "energy_change_pct": comparison["comparison"]["energy_change_pct"],
            },
            "top_consumers": top_consumers,
            "efficiency_score": efficiency["overall_score"],
            "recommendations": efficiency["recommendations"],
        }
        
        return summary

    async def export_for_ai_analysis(
        self,
        period: str = "today",
        compare_previous: bool = False,
    ) -> dict[str, Any]:
        """Export energy dashboard data for AI analysis.
        
        Args:
            period: Analysis period (today/yesterday/week/month)
            compare_previous: Include comparison with previous period
            
        Returns:
            Structured data optimized for AI analysis
        """
        now = datetime.now()
        
        # Determine period boundaries
        if period == "today":
            start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end = now
            prev_start = start - timedelta(days=1)
            prev_end = start
        elif period == "yesterday":
            start = (now - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
            end = now.replace(hour=0, minute=0, second=0, microsecond=0)
            prev_start = start - timedelta(days=1)
            prev_end = start
        elif period == "week":
            start = (now - timedelta(days=7)).replace(hour=0, minute=0, second=0, microsecond=0)
            end = now
            prev_start = start - timedelta(days=7)
            prev_end = start
        elif period == "month":
            start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            end = now
            # Previous month
            if start.month == 1:
                prev_start = start.replace(year=start.year - 1, month=12)
            else:
                prev_start = start.replace(month=start.month - 1)
            prev_end = start
        else:
            # Default to today
            start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end = now
            prev_start = start - timedelta(days=1)
            prev_end = start
        
        # Get current period data
        current_data = await self.get_period_data(start, end)
        breakdown = await self.get_devices_breakdown()
        top_consumers = await self.get_top_consumers(limit=5)
        efficiency = await self.get_energy_efficiency_score()
        
        export_data = {
            "period": {
                "name": period,
                "start": start.isoformat(),
                "end": end.isoformat(),
                "duration_hours": (end - start).total_seconds() / 3600,
            },
            "overview": {
                "total_devices": len(breakdown["devices"]),
                "total_energy_kwh": round(current_data["totals"]["energy_kwh"], 3),
                "total_cost_eur": round(current_data["totals"]["cost"], 2),
                "total_cycles": current_data["totals"]["cycles"],
                "efficiency_score": efficiency["overall_score"],
            },
            "devices": [],
            "top_consumers": top_consumers,
            "efficiency_metrics": efficiency,
        }
        
        # Add detailed device information
        for device in breakdown["devices"]:
            device_info = {
                "name": device["name"],
                "type": device["type"],
                "daily_energy_kwh": device["daily"]["energy_kwh"],
                "daily_cost_eur": device["daily"]["cost"],
                "daily_cycles": device["daily"]["cycles"],
                "monthly_energy_kwh": device["monthly"]["energy_kwh"],
                "monthly_cost_eur": device["monthly"]["cost"],
                "percentage_of_total": device.get("percentage", 0),
            }
            export_data["devices"].append(device_info)
        
        # Add comparison if requested
        if compare_previous:
            comparison = await self.get_comparison_data(
                start, end, prev_start, prev_end
            )
            export_data["comparison"] = {
                "previous_period": {
                    "start": prev_start.isoformat(),
                    "end": prev_end.isoformat(),
                    "energy_kwh": round(comparison["previous"]["totals"]["energy_kwh"], 3),
                    "cost_eur": round(comparison["previous"]["totals"]["cost"], 2),
                },
                "changes": {
                    "energy_diff_kwh": comparison["comparison"]["energy_diff_kwh"],
                    "energy_change_pct": comparison["comparison"]["energy_change_pct"],
                    "cost_diff_eur": comparison["comparison"]["cost_diff"],
                    "cost_change_pct": comparison["comparison"]["cost_change_pct"],
                },
            }
        
        # Add pricing information
        coordinators = self._get_coordinators()
        if coordinators:
            # Get average price from first coordinator
            avg_price = coordinators[0].price_kwh
            export_data["pricing"] = {
                "average_price_kwh_eur": round(avg_price, 4),
                "currency": "EUR",
            }
        
        export_data["export_metadata"] = {
            "timestamp": now.isoformat(),
            "comparison_included": compare_previous,
        }
        
        return export_data

