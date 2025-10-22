"""Cycle History Manager for Smart Appliance Monitor."""
from __future__ import annotations

import logging
from datetime import datetime, timedelta
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.components import recorder
from homeassistant.components.recorder import get_instance, history

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class CycleHistoryManager:
    """Manage cycle history using Home Assistant Recorder."""

    def __init__(self, hass: HomeAssistant, appliance_id: str, appliance_name: str):
        """Initialize the history manager.
        
        Args:
            hass: Home Assistant instance
            appliance_id: Entry ID of the appliance
            appliance_name: Name of the appliance
        """
        self.hass = hass
        self.appliance_id = appliance_id
        self.appliance_name = appliance_name
        self._event_type = f"{DOMAIN}_cycle_finished"

    async def async_get_cycles(
        self,
        period_start: datetime | None = None,
        period_end: datetime | None = None,
        min_duration: float | None = None,
        max_duration: float | None = None,
        min_energy: float | None = None,
        max_energy: float | None = None,
        limit: int | None = None,
    ) -> list[dict[str, Any]]:
        """Retrieve cycles from Recorder with filters.
        
        Args:
            period_start: Start of the period (default: 30 days ago)
            period_end: End of the period (default: now)
            min_duration: Minimum cycle duration in minutes
            max_duration: Maximum cycle duration in minutes
            min_energy: Minimum energy consumption in kWh
            max_energy: Maximum energy consumption in kWh
            limit: Maximum number of results to return
            
        Returns:
            List of cycles matching the criteria
        """
        # Default period: last 30 days
        if period_end is None:
            period_end = datetime.now()
        if period_start is None:
            period_start = period_end - timedelta(days=30)

        _LOGGER.debug(
            "Querying cycle history for '%s' from %s to %s",
            self.appliance_name,
            period_start,
            period_end,
        )

        try:
            # Get recorder instance
            recorder_instance = get_instance(self.hass)
            if recorder_instance is None:
                _LOGGER.error("Recorder not available")
                return []

            # Query events from Recorder
            events = await recorder_instance.async_add_executor_job(
                self._get_events_from_recorder,
                period_start,
                period_end,
            )

            if not events:
                _LOGGER.debug("No cycle events found in period")
                return []

            _LOGGER.debug("Found %d events in Recorder", len(events))

            # Filter events by appliance_id
            cycles = []
            for event in events:
                event_data = event.data
                
                # Check if this event belongs to this appliance
                if event_data.get("appliance_id") != self.appliance_id:
                    continue

                # Extract cycle data
                cycle = {
                    "timestamp": event.time_fired,
                    "appliance_name": event_data.get("appliance_name"),
                    "appliance_type": event_data.get("appliance_type"),
                    "duration": event_data.get("duration", 0),
                    "energy": event_data.get("energy", 0),
                    "cost": event_data.get("cost", 0),
                    "peak_power": event_data.get("peak_power", 0),
                    "start_time": event_data.get("start_time"),
                    "end_time": event_data.get("end_time"),
                    "start_energy": event_data.get("start_energy", 0),
                    "end_energy": event_data.get("end_energy", 0),
                }

                # Apply filters
                if min_duration is not None and cycle["duration"] < min_duration:
                    continue
                if max_duration is not None and cycle["duration"] > max_duration:
                    continue
                if min_energy is not None and cycle["energy"] < min_energy:
                    continue
                if max_energy is not None and cycle["energy"] > max_energy:
                    continue

                cycles.append(cycle)

            # Sort by timestamp (most recent first)
            cycles.sort(key=lambda x: x["timestamp"], reverse=True)

            # Apply limit
            if limit is not None and limit > 0:
                cycles = cycles[:limit]

            _LOGGER.info(
                "Retrieved %d cycles for '%s' (period: %s to %s)",
                len(cycles),
                self.appliance_name,
                period_start.strftime("%Y-%m-%d"),
                period_end.strftime("%Y-%m-%d"),
            )

            return cycles

        except Exception as err:
            _LOGGER.error(
                "Error retrieving cycle history for '%s': %s",
                self.appliance_name,
                err,
            )
            return []

    def _get_events_from_recorder(
        self,
        start_time: datetime,
        end_time: datetime,
    ) -> list:
        """Get events from Recorder (sync method for executor).
        
        Args:
            start_time: Start of the period
            end_time: End of the period
            
        Returns:
            List of events (as dicts)
        """
        recorder_instance = get_instance(self.hass)
        if recorder_instance is None:
            return []

        # Query events using lower-level API
        try:
            _LOGGER.debug(
                "Querying events: type=%s, start=%s, end=%s",
                self._event_type,
                start_time,
                end_time,
            )
            
            # Use raw SQL queries for compatibility with all HA versions
            from sqlalchemy import text
            import json
            
            with recorder_instance.get_session() as session:
                # First get the event_type_id
                type_query = text(
                    "SELECT event_type_id FROM event_types WHERE event_type = :event_type"
                )
                type_result = session.execute(type_query, {"event_type": self._event_type})
                type_row = type_result.first()
                
                if not type_row:
                    _LOGGER.info("Event type '%s' not found in database", self._event_type)
                    return []
                
                event_type_id = type_row[0]
                
                # Now query events using event_type_id and time_fired_ts
                stmt = text(
                    "SELECT ed.shared_data, e.time_fired_ts "
                    "FROM events e "
                    "JOIN event_data ed ON e.data_id = ed.data_id "
                    "WHERE e.event_type_id = :event_type_id "
                    "AND e.time_fired_ts >= :start_time "
                    "AND e.time_fired_ts <= :end_time "
                    "ORDER BY e.time_fired_ts DESC"
                )
                result = session.execute(
                    stmt,
                    {
                        "event_type_id": event_type_id,
                        "start_time": start_time.timestamp(),
                        "end_time": end_time.timestamp(),
                    }
                )
                
                events = []
                for row in result:
                    try:
                        event_data = json.loads(row[0]) if isinstance(row[0], str) else row[0]
                        # Create a simple event object
                        events.append(type('Event', (), {
                            'data': event_data,
                            'time_fired': datetime.fromtimestamp(row[1])
                        })())
                    except Exception as e:
                        _LOGGER.debug("Error parsing event data: %s", e)
                        continue
                
                _LOGGER.info(
                    "Found %d events of type '%s' in Recorder",
                    len(events),
                    self._event_type,
                )
                return events
                
        except Exception as err:
            _LOGGER.error("Error querying events: %s", err)
            return []

    async def async_get_cycle_statistics(
        self,
        period_start: datetime | None = None,
        period_end: datetime | None = None,
    ) -> dict[str, Any]:
        """Get aggregated statistics for cycles in a period.
        
        Args:
            period_start: Start of the period
            period_end: End of the period
            
        Returns:
            Dictionary with statistics
        """
        cycles = await self.async_get_cycles(
            period_start=period_start,
            period_end=period_end,
        )

        if not cycles:
            return {
                "period_start": period_start.isoformat() if period_start else None,
                "period_end": period_end.isoformat() if period_end else None,
                "cycle_count": 0,
                "total_energy": 0,
                "total_cost": 0,
                "avg_duration": 0,
                "avg_energy": 0,
                "avg_cost": 0,
                "max_energy": 0,
                "min_energy": 0,
            }

        total_energy = sum(c["energy"] for c in cycles)
        total_cost = sum(c["cost"] for c in cycles)
        total_duration = sum(c["duration"] for c in cycles)

        return {
            "period_start": period_start.isoformat() if period_start else None,
            "period_end": period_end.isoformat() if period_end else None,
            "cycle_count": len(cycles),
            "total_energy": round(total_energy, 3),
            "total_cost": round(total_cost, 2),
            "avg_duration": round(total_duration / len(cycles), 1) if cycles else 0,
            "avg_energy": round(total_energy / len(cycles), 3) if cycles else 0,
            "avg_cost": round(total_cost / len(cycles), 2) if cycles else 0,
            "max_energy": round(max(c["energy"] for c in cycles), 3) if cycles else 0,
            "min_energy": round(min(c["energy"] for c in cycles), 3) if cycles else 0,
        }

