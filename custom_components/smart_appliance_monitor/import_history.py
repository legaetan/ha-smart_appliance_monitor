"""Historical Cycle Importer for Smart Appliance Monitor."""
from __future__ import annotations

import logging
from datetime import datetime, timedelta
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.components import recorder
from homeassistant.components.recorder import get_instance

from .const import DOMAIN
from .state_machine import CycleStateMachine

_LOGGER = logging.getLogger(__name__)


class HistoricalCycleImporter:
    """Import historical cycles from power sensor data."""

    def __init__(
        self,
        hass: HomeAssistant,
        appliance_id: str,
        appliance_name: str,
        appliance_type: str,
        power_sensor: str,
        energy_sensor: str,
        start_threshold: float,
        stop_threshold: float,
        start_delay: int,
        stop_delay: int,
        price_kwh: float,
    ):
        """Initialize the importer.
        
        Args:
            hass: Home Assistant instance
            appliance_id: Entry ID of the appliance
            appliance_name: Name of the appliance
            appliance_type: Type of appliance
            power_sensor: Power sensor entity ID
            energy_sensor: Energy sensor entity ID
            start_threshold: Power threshold to start cycle (W)
            stop_threshold: Power threshold to stop cycle (W)
            start_delay: Delay before confirming start (seconds)
            stop_delay: Delay before confirming stop (seconds)
            price_kwh: Price per kWh for cost calculation
        """
        self.hass = hass
        self.appliance_id = appliance_id
        self.appliance_name = appliance_name
        self.appliance_type = appliance_type
        self.power_sensor = power_sensor
        self.energy_sensor = energy_sensor
        self.start_threshold = start_threshold
        self.stop_threshold = stop_threshold
        self.start_delay = start_delay
        self.stop_delay = stop_delay
        self.price_kwh = price_kwh

    async def async_import_cycles(
        self,
        period_start: datetime | None = None,
        period_end: datetime | None = None,
        dry_run: bool = False,
        replace_existing: bool = False,
    ) -> dict[str, Any]:
        """Import historical cycles from power sensor data.
        
        Args:
            period_start: Start of the import period (default: 30 days ago)
            period_end: End of the import period (default: now)
            dry_run: If True, analyze without saving events
            replace_existing: If True, delete existing cycles in period before importing
            
        Returns:
            Dictionary with import results
        """
        # Default period: last 30 days
        if period_end is None:
            period_end = datetime.now()
        if period_start is None:
            period_start = period_end - timedelta(days=30)

        _LOGGER.info(
            "Starting historical cycle import for '%s' (%s to %s, dry_run=%s)",
            self.appliance_name,
            period_start.strftime("%Y-%m-%d"),
            period_end.strftime("%Y-%m-%d"),
            dry_run,
        )

        try:
            # Get power sensor history
            power_history = await self._async_get_sensor_history(
                self.power_sensor,
                period_start,
                period_end,
            )

            if not power_history:
                _LOGGER.warning(
                    "No power sensor history found for '%s' in the specified period",
                    self.appliance_name,
                )
                return {
                    "success": False,
                    "error": "No sensor history found",
                    "cycles_detected": 0,
                }

            # Get energy sensor history
            energy_history = await self._async_get_sensor_history(
                self.energy_sensor,
                period_start,
                period_end,
            )

            _LOGGER.debug(
                "Retrieved %d power states and %d energy states",
                len(power_history),
                len(energy_history),
            )

            # Detect cycles from power history
            cycles = self._detect_cycles_from_history(power_history, energy_history)

            _LOGGER.info(
                "Detected %d cycles for '%s' in period %s to %s",
                len(cycles),
                self.appliance_name,
                period_start.strftime("%Y-%m-%d"),
                period_end.strftime("%Y-%m-%d"),
            )

            # Calculate statistics by period
            stats_by_month = self._calculate_monthly_stats(cycles)

            # Save cycles as events (if not dry_run)
            if not dry_run and cycles:
                await self._async_save_cycles_as_events(
                    cycles, 
                    replace_existing,
                    period_start,
                    period_end,
                )
                action = "réimportés" if replace_existing else "importés"
                _LOGGER.info(
                    "%d cycles historiques %s pour '%s'",
                    len(cycles),
                    action,
                    self.appliance_name,
                )

            return {
                "success": True,
                "cycles_detected": len(cycles),
                "period_start": period_start.isoformat(),
                "period_end": period_end.isoformat(),
                "dry_run": dry_run,
                "stats_by_month": stats_by_month,
                "cycles": cycles if dry_run else None,  # Include cycles in dry_run
            }

        except Exception as err:
            _LOGGER.error(
                "Error importing historical cycles for '%s': %s",
                self.appliance_name,
                err,
            )
            return {
                "success": False,
                "error": str(err),
                "cycles_detected": 0,
            }

    async def _async_get_sensor_history(
        self,
        entity_id: str,
        start_time: datetime,
        end_time: datetime,
    ) -> list[tuple[datetime, float]]:
        """Get sensor history from Recorder.
        
        Args:
            entity_id: Entity ID of the sensor
            start_time: Start of the period
            end_time: End of the period
            
        Returns:
            List of (timestamp, value) tuples
        """
        from homeassistant.components.recorder import history

        recorder_instance = get_instance(self.hass)
        if recorder_instance is None:
            _LOGGER.error("Recorder not available")
            return []

        # Use history API instead of direct SQL queries
        def get_states() -> list[tuple[datetime, float]]:
            """Get states from history (sync method)."""
            # Get history for the entity
            history_states = history.get_significant_states(
                self.hass,
                start_time,
                end_time,
                entity_ids=[entity_id],
                significant_changes_only=False,
            )
            
            if entity_id not in history_states:
                _LOGGER.warning("No history found for entity '%s'", entity_id)
                return []
            
            states = []
            for state in history_states[entity_id]:
                try:
                    value = float(state.state)
                    states.append((state.last_updated, value))
                except (ValueError, TypeError, AttributeError):
                    # Skip invalid states
                    continue
            
            return states

        return await recorder_instance.async_add_executor_job(get_states)

    def _detect_cycles_from_history(
        self,
        power_history: list[tuple[datetime, float]],
        energy_history: list[tuple[datetime, float]],
    ) -> list[dict[str, Any]]:
        """Detect cycles from power sensor history.
        
        Args:
            power_history: List of (timestamp, power) tuples
            energy_history: List of (timestamp, energy) tuples
            
        Returns:
            List of detected cycles
        """
        cycles = []
        current_cycle = None
        above_threshold_since = None
        below_threshold_since = None

        # Create energy lookup dict for faster access
        energy_dict = {ts: val for ts, val in energy_history}

        for timestamp, power in power_history:
            # Check for cycle start
            if current_cycle is None:
                if power >= self.start_threshold:
                    if above_threshold_since is None:
                        above_threshold_since = timestamp
                    elif (timestamp - above_threshold_since).total_seconds() >= self.start_delay:
                        # Cycle started
                        energy_at_start = self._get_energy_at_time(energy_dict, timestamp)
                        current_cycle = {
                            "start_time": above_threshold_since,
                            "start_energy": energy_at_start,
                            "peak_power": power,
                        }
                        above_threshold_since = None
                        below_threshold_since = None
                else:
                    above_threshold_since = None

            # Check for cycle end
            else:
                # Update peak power
                if power > current_cycle["peak_power"]:
                    current_cycle["peak_power"] = power

                if power <= self.stop_threshold:
                    if below_threshold_since is None:
                        below_threshold_since = timestamp
                    elif (timestamp - below_threshold_since).total_seconds() >= self.stop_delay:
                        # Cycle ended
                        energy_at_end = self._get_energy_at_time(energy_dict, timestamp)
                        
                        # Calculate cycle metrics
                        duration_seconds = (timestamp - current_cycle["start_time"]).total_seconds()
                        duration_minutes = duration_seconds / 60
                        energy_consumed = energy_at_end - current_cycle["start_energy"]
                        cost = energy_consumed * self.price_kwh

                        # Only add valid cycles (positive duration and energy)
                        if duration_minutes > 0 and energy_consumed > 0:
                            cycles.append({
                                "start_time": current_cycle["start_time"].isoformat(),
                                "end_time": timestamp.isoformat(),
                                "duration": round(duration_minutes, 1),
                                "energy": round(energy_consumed, 3),
                                "cost": round(cost, 2),
                                "peak_power": round(current_cycle["peak_power"], 1),
                                "start_energy": round(current_cycle["start_energy"], 3),
                                "end_energy": round(energy_at_end, 3),
                            })

                        # Reset for next cycle
                        current_cycle = None
                        below_threshold_since = None
                        above_threshold_since = None
                else:
                    below_threshold_since = None

        return cycles

    def _get_energy_at_time(
        self,
        energy_dict: dict[datetime, float],
        target_time: datetime,
    ) -> float:
        """Get energy value at specific time (or closest).
        
        Args:
            energy_dict: Dictionary of timestamp -> energy
            target_time: Target timestamp
            
        Returns:
            Energy value at or near the target time
        """
        # Try exact match first
        if target_time in energy_dict:
            return energy_dict[target_time]

        # Find closest timestamp (within 5 minutes)
        closest_time = None
        closest_diff = timedelta(minutes=5)

        for ts in energy_dict:
            diff = abs(ts - target_time)
            if diff < closest_diff:
                closest_diff = diff
                closest_time = ts

        if closest_time:
            return energy_dict[closest_time]

        # Fallback to 0 if no close match
        return 0.0

    def _calculate_monthly_stats(
        self,
        cycles: list[dict[str, Any]],
    ) -> dict[str, dict[str, Any]]:
        """Calculate statistics by month.
        
        Args:
            cycles: List of detected cycles
            
        Returns:
            Dictionary of month -> statistics
        """
        stats_by_month = {}

        for cycle in cycles:
            start_time = datetime.fromisoformat(cycle["start_time"])
            month_key = start_time.strftime("%Y-%m")

            if month_key not in stats_by_month:
                stats_by_month[month_key] = {
                    "cycle_count": 0,
                    "total_energy": 0.0,
                    "total_cost": 0.0,
                }

            stats_by_month[month_key]["cycle_count"] += 1
            stats_by_month[month_key]["total_energy"] += cycle["energy"]
            stats_by_month[month_key]["total_cost"] += cycle["cost"]

        # Round values
        for month_stats in stats_by_month.values():
            month_stats["total_energy"] = round(month_stats["total_energy"], 3)
            month_stats["total_cost"] = round(month_stats["total_cost"], 2)

        return stats_by_month

    async def _async_save_cycles_as_events(
        self,
        cycles: list[dict[str, Any]],
        replace_existing: bool = False,
        period_start: datetime | None = None,
        period_end: datetime | None = None,
    ) -> None:
        """Save detected cycles as events in Recorder.
        
        Args:
            cycles: List of cycles to save
            replace_existing: If True, delete existing events in period first
            period_start: Start of the period (for deletion)
            period_end: End of the period (for deletion)
        """
        # If replace_existing, delete old events in the period first
        if replace_existing and period_start and period_end:
            deleted_count = await self._async_delete_events_in_period(
                period_start, period_end
            )
            if deleted_count > 0:
                _LOGGER.info(
                    "Deleted %d existing cycle events for '%s' in period %s to %s",
                    deleted_count,
                    self.appliance_name,
                    period_start.date(),
                    period_end.date(),
                )
        
        event_type = f"{DOMAIN}_cycle_finished"

        for cycle in cycles:
            # Fire event with historical timestamp
            event_data = {
                "appliance_name": self.appliance_name,
                "appliance_type": self.appliance_type,
                "appliance_id": self.appliance_id,
                "entry_id": self.appliance_id,
                "duration": cycle["duration"],
                "energy": cycle["energy"],
                "cost": cycle["cost"],
                "peak_power": cycle["peak_power"],
                "start_time": cycle["start_time"],
                "end_time": cycle["end_time"],
                "start_energy": cycle["start_energy"],
                "end_energy": cycle["end_energy"],
                "imported": True,  # Mark as imported
                "reimported": replace_existing,  # Mark if replacing
            }

            # Fire event (will be recorded by Recorder)
            # Note: The event will have current timestamp in Recorder,
            # but the cycle data includes the actual historical timestamps
            self.hass.bus.async_fire(event_type, event_data)

        _LOGGER.debug("Fired %d historical cycle events", len(cycles))

    async def _async_delete_events_in_period(
        self,
        period_start: datetime,
        period_end: datetime,
    ) -> int:
        """Delete cycle events in a given period from Recorder database.
        
        Args:
            period_start: Start of the period
            period_end: End of the period
            
        Returns:
            Number of events deleted
        """
        from homeassistant.components.recorder import get_instance
        
        recorder_instance = get_instance(self.hass)
        if recorder_instance is None:
            _LOGGER.error("Recorder not available")
            return 0
        
        def _delete_events() -> int:
            """Delete events in executor."""
            try:
                from sqlalchemy import text
                
                with recorder_instance.get_session() as session:
                    # Get event_type_id
                    event_type = f"{DOMAIN}_cycle_finished"
                    type_query = text(
                        "SELECT event_type_id FROM event_types WHERE event_type = :event_type"
                    )
                    type_result = session.execute(type_query, {"event_type": event_type})
                    type_row = type_result.first()
                    
                    if not type_row:
                        return 0
                    
                    event_type_id = type_row[0]
                    
                    # Get event IDs to delete for this appliance in the period
                    # We check the appliance_id in the event_data
                    find_query = text(
                        "SELECT e.event_id "
                        "FROM events e "
                        "JOIN event_data ed ON e.data_id = ed.data_id "
                        "WHERE e.event_type_id = :event_type_id "
                        "AND json_extract(ed.shared_data, '$.appliance_id') = :appliance_id "
                        "AND json_extract(ed.shared_data, '$.start_time') >= :period_start "
                        "AND json_extract(ed.shared_data, '$.start_time') <= :period_end"
                    )
                    
                    result = session.execute(
                        find_query,
                        {
                            "event_type_id": event_type_id,
                            "appliance_id": self.appliance_id,
                            "period_start": period_start.isoformat(),
                            "period_end": period_end.isoformat(),
                        }
                    )
                    
                    event_ids = [row[0] for row in result]
                    
                    if not event_ids:
                        return 0
                    
                    # Delete the events
                    # SQLite needs the list as a comma-separated string
                    ids_str = ",".join(str(id) for id in event_ids)
                    delete_query = text(f"DELETE FROM events WHERE event_id IN ({ids_str})")
                    session.execute(delete_query)
                    session.commit()
                    
                    return len(event_ids)
                    
            except Exception as err:
                _LOGGER.error("Error deleting events: %s", err)
                return 0
        
        return await recorder_instance.async_add_executor_job(_delete_events)


