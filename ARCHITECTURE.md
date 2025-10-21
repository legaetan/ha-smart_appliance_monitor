# Architecture

This document describes the technical architecture and component design of Smart Appliance Monitor.

## Overview

Smart Appliance Monitor is built as a Home Assistant custom integration using a state machine architecture for reliable cycle detection. The system uses a coordinator pattern for data management and provides extensive entity coverage for monitoring and control.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Home Assistant                         │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────┴─────────────────────────────────┐
│              Smart Appliance Monitor Integration            │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │            DataUpdateCoordinator (30s poll)          │   │
│  │  - Fetches power/energy from sensors                 │   │
│  │  - Manages statistics (daily/monthly)                │   │
│  │  - Handles events and notifications                  │   │
│  └────────────────┬─────────────────────────────────────┘   │
│                   │                                         │
│  ┌────────────────┴─────────────────────────────────────┐   │
│  │              State Machine                           │   │
│  │  - Tracks appliance state (idle/running/finished)    │   │
│  │  - Detects cycle start/stop with thresholds          │   │
│  │  - Calculates cycle statistics                       │   │
│  │  - Emits events                                      │   │
│  └────────────────┬─────────────────────────────────────┘   │
│                   │                                         │
│         ┌─────────┴─────────┐                               │
│         │                   │                               │
│    ┌────▼─────┐       ┌─────▼──────┐                        │
│    │ Entities │       │  Notifier  │                        │
│    │  Update  │       │   System   │                        │
│    └──────────┘       └────────────┘                        │
│                                                             │
│  Entities (19 per appliance):                               │
│  • Sensors (10): state, duration, energy, cost, stats       │
│  • Binary Sensors (3): running, alert, unplugged            │
│  • Switches (6): monitoring, notifications, 4 notif types   │
│  • Buttons (1): reset stats                                 │
└─────────────────────────────────────────────────────────────┘
```

## Core Components

### State Machine (`state_machine.py`)

The state machine is the heart of cycle detection logic.

**States:**
- `idle` - Appliance is off or in standby
- `running` - Active cycle in progress
- `finished` - Cycle completed, waiting for acknowledgment

**Transitions:**
```
idle → running: Power > start_threshold for start_delay seconds
running → finished: Power < stop_threshold for stop_delay seconds
finished → idle: Automatic after next update or manual reset
```

**Key Features:**
- Configurable power thresholds (start/stop)
- Delay-based confirmation to avoid false positives
- Automatic statistics calculation (duration, energy, cost)
- Peak power tracking
- Event emission for state changes

**Configuration Parameters:**
- `start_threshold` (W) - Minimum power to detect start
- `stop_threshold` (W) - Maximum power to detect stop
- `start_delay` (s) - Confirmation time before cycle starts
- `stop_delay` (s) - Confirmation time before cycle stops
- `alert_duration` (s) - Time before duration alert triggers

### Data Coordinator (`coordinator.py`)

Manages all data updates and orchestrates component communication.

**Responsibilities:**
- Poll power/energy sensors every 30 seconds
- Update state machine with new readings
- Emit Home Assistant events for state changes
- Manage statistics (daily/monthly resets)
- Coordinate notifications
- Provide data to all entities

**Data Flow:**
1. Fetch power and energy from configured sensors
2. Update state machine with new values
3. Handle any events emitted by state machine
4. Update statistics trackers
5. Trigger notifications if needed
6. Broadcast updated data to entities

**Statistics Management:**
- Current cycle: duration, energy, cost (real-time)
- Last cycle: duration, energy, cost (persisted)
- Daily: cycle count, total cost (resets at midnight)
- Monthly: total cost (resets on 1st of month)

### Configuration Flow (`config_flow.py`)

Handles all user interaction for setup and configuration.

**Flows:**

1. **Initial Setup Flow** (`async_step_user`)
   - Appliance name and type selection
   - Power sensor selection
   - Energy sensor selection
   - Price configuration (fixed or entity-based)

2. **Reconfiguration Flow** (`async_step_reconfigure`)
   - Modify all base settings
   - Pre-filled with current values
   - Statistics preserved
   - Automatic integration reload

3. **Options Flow** (`async_step_init`)
   - Advanced threshold configuration
   - Delay adjustments
   - Alert settings
   - Uses appliance profile defaults

**Appliance Profiles:**
Pre-configured thresholds optimized per appliance type:

| Type            | Start (W) | Stop (W) | Start Delay (s) | Stop Delay (s) | Alert (s) |
|-----------------|-----------|----------|-----------------|----------------|-----------|
| Water Heater    | 1000      | 50       | 60              | 120            | 14400     |
| Oven            | 100       | 10       | 60              | 180            | 7200      |
| Dryer           | 100       | 10       | 60              | 180            | 7200      |
| Dishwasher      | 20        | 5        | 120             | 300            | 10800     |
| Washing Machine | 10        | 5        | 120             | 300            | 10800     |
| Coffee Maker    | 50        | 5        | 30              | 60             | 1800      |
| Monitor         | 30        | 5        | 60              | 120            | 28800     |
| NAS             | 50        | 20       | 180             | 300            | 21600     |
| 3D Printer      | 50        | 10       | 120             | 180            | 86400     |
| VMC             | 20        | 10       | 60              | 120            | 7200      |
| Other           | 50        | 5        | 120             | 300            | 7200      |

### Notification System (`notify.py`)

Handles all user notifications with multi-service support and granular control.

**Notification Types (v0.2.0):**

1. **Cycle/Session Started** (`NOTIF_TYPE_CYCLE_STARTED`)
   - Triggered when appliance begins cycle/session
   - Includes appliance name and type
   - Can be toggled individually via switch

2. **Cycle/Session Finished** (`NOTIF_TYPE_CYCLE_FINISHED`)
   - Triggered when cycle/session completes
   - Includes duration, energy consumption, cost
   - Can be toggled individually via switch

3. **Duration Alert** (`NOTIF_TYPE_ALERT_DURATION`)
   - Triggered when cycle/session exceeds expected duration
   - Includes current duration and threshold
   - Can be toggled individually via switch

4. **Unplugged Alert** (`NOTIF_TYPE_UNPLUGGED`) - **NEW in v0.2.0**
   - Triggered when appliance detected as disconnected
   - Includes time at zero power
   - Can be toggled individually via switch

**Multi-Service Delivery (v0.2.0):**
- **Mobile App**: Auto-detects available `mobile_app_*` services
- **Telegram**: Markdown formatting with inline buttons
- **Persistent Notification**: Fallback/alternative
- **Custom Service**: User-configurable service name
- Services configured in Options Flow
- Simultaneous delivery to multiple services

**Control Hierarchy:**
1. Master notifications switch (global enable/disable)
2. Configuration: Selected services and types (Options Flow)
3. Individual switches per notification type (quick toggle)

## Entity Architecture

### Base Entity (`entity.py`)

All entities inherit from `SmartApplianceEntity`:

```python
class SmartApplianceEntity(CoordinatorEntity):
    """Base class for all Smart Appliance Monitor entities."""
    
    def __init__(self, coordinator, entity_type):
        self.coordinator = coordinator
        self._attr_device_info = get_device_info(coordinator)
        self._attr_unique_id = f"{coordinator.entry.entry_id}_{entity_type}"
```

**Provides:**
- Automatic device linkage
- Coordinator integration
- Unique ID generation
- Availability tracking

### Sensors (`sensor.py`)

10 sensor entities per appliance:

**Current Cycle Sensors:**
- `state` - Current state (idle/running/finished)
- `cycle_duration` - Duration in minutes
- `cycle_energy` - Energy in kWh
- `cycle_cost` - Cost in currency

**Last Cycle Sensors:**
- `last_cycle_duration` - Previous cycle duration
- `last_cycle_energy` - Previous cycle energy
- `last_cycle_cost` - Previous cycle cost

**Statistics Sensors:**
- `daily_cycles` - Count of cycles today
- `daily_cost` - Total cost today
- `monthly_cost` - Total cost this month

**Features:**
- Appropriate device classes (`duration`, `energy`, `monetary`)
- State classes (`measurement`, `total`)
- Unit of measurement
- Suggested display precision

### Binary Sensors (`binary_sensor.py`)

3 binary sensor entities per appliance:

**Running Sensor:**
- `ON` when appliance is running
- `OFF` when idle or finished
- Device class: `running`

**Alert Duration Sensor:**
- `ON` when cycle exceeds expected duration
- `OFF` otherwise
- Device class: `problem`
- Only created if alert duration is enabled in options

**Unplugged Sensor:**
- `ON` when appliance is detected as unplugged/disconnected
- `OFF` otherwise
- Device class: `problem`
- Detects when power = 0W for configurable timeout (default: 5 minutes)
- Extra attributes: `time_at_zero_power`, `unplugged_timeout`, `detection_progress`

### Switches (`switch.py`)

6 switch entities per appliance:

**Monitoring Switch:**
- Enable/disable cycle detection
- Persists across restarts
- Updates coordinator monitoring state

**Notifications Switch:**
- Enable/disable all notifications (master switch)
- Independent of monitoring
- Updates notifier state

**Notification Type Switches (4):**
- `notification_cycle_started` - Toggle start notifications
- `notification_cycle_finished` - Toggle completion notifications
- `notification_alert_duration` - Toggle duration alerts
- `notification_unplugged` - Toggle unplugged alerts
- Work in conjunction with master notifications switch
- Allow granular control without changing configuration
- All enabled by default

### Buttons (`button.py`)

1 button entity per appliance:

**Reset Statistics Button:**
- Clears all statistics
- Resets daily/monthly counters
- Fires reset event
- Logs action

## Services

Three custom services for programmatic control:

### `smart_appliance_monitor.start_cycle`

Manually trigger cycle start (useful for testing or manual tracking).

**Parameters:**
- `device_id` - Target appliance device

**Use Case:** Start tracking when automatic detection isn't suitable.

### `smart_appliance_monitor.stop_monitoring`

Disable monitoring for specific appliance.

**Parameters:**
- `device_id` - Target appliance device

**Use Case:** Temporarily stop tracking without removing integration.

### `smart_appliance_monitor.reset_statistics`

Reset all statistics for specific appliance.

**Parameters:**
- `device_id` - Target appliance device

**Use Case:** Clear history after appliance replacement or major changes.

## Data Flow

### Update Cycle (Every 30 seconds)

```
1. Coordinator._async_update_data() triggered
   ↓
2. Fetch power from sensor (hass.states.get)
   ↓
3. Fetch energy from sensor (hass.states.get)
   ↓
4. state_machine.update(power, energy)
   ↓
5. Event emitted? (cycle_started, cycle_finished, alert_duration)
   ↓
6. Handle event:
   - Update statistics
   - Log information
   - Trigger notification
   ↓
7. Return updated data to entities
   ↓
8. Entities update their states
```

### Event Handling

```
Event: cycle_started
  → coordinator._on_cycle_started()
    → Log cycle start
    → Update statistics
    → notifier.notify_cycle_started()

Event: cycle_finished
  → coordinator._on_cycle_finished()
    → Calculate final statistics
    → Log cycle completion
    → Update last_cycle data
    → Increment daily counter
    → notifier.notify_cycle_finished()

Event: alert_duration
  → coordinator._on_alert_duration()
    → Log alert
    → notifier.notify_alert_duration()
```

## File Structure

```
custom_components/smart_appliance_monitor/
├── __init__.py              # Entry point, service registration
├── binary_sensor.py         # Binary sensor platform (124 lines)
├── button.py                # Button platform (80 lines)
├── config_flow.py           # Configuration UI (256 lines)
├── const.py                 # Constants and profiles (124 lines)
├── coordinator.py           # Data coordinator (389 lines)
├── device.py                # Device utilities (70 lines)
├── entity.py                # Base entity class (50 lines)
├── manifest.json            # Integration metadata
├── notify.py                # Notification system (230 lines)
├── sensor.py                # Sensor platform (395 lines)
├── services.yaml            # Service definitions (51 lines)
├── state_machine.py         # Cycle detection (260 lines)
├── strings.json             # English translations
├── switch.py                # Switch platform (128 lines)
└── translations/
    └── fr.json              # French translations
```

## Key Design Decisions

### Why State Machine?

- **Reliability**: Explicit state transitions prevent ambiguity
- **Testability**: Easy to unit test all state transitions
- **Maintainability**: Clear logic flow for future enhancements
- **Predictability**: Deterministic behavior

### Why Coordinator Pattern?

- **Efficiency**: Single data fetch for multiple entities
- **Consistency**: All entities see same data snapshot
- **Home Assistant Best Practice**: Recommended pattern
- **Error Handling**: Centralized error management

### Why Delay-Based Detection?

- **Avoid False Positives**: Power fluctuations don't trigger cycles
- **Reliability**: Confirms sustained power changes
- **Configurability**: Users can adjust for their appliances
- **Robustness**: Handles noisy sensor data

### Why Appliance Profiles?

- **User Experience**: Sensible defaults out of the box
- **Flexibility**: Users can still customize if needed
- **Accuracy**: Tuned for common appliance behaviors
- **Scalability**: Easy to add new appliance types

## Statistics

### Codebase (v0.2.0)
- **Python Files**: 12 production files
- **Lines of Code**: ~3,500+ lines (was ~2,500)
- **Test Files**: 9 test files
- **Test Cases**: 75+ unit tests
- **Code Coverage**: ~95%

### Entities Per Appliance (v0.2.0)
- Sensors: 10 (adaptive naming based on appliance type)
- Binary Sensors: 3 (running, alert_duration, unplugged)
- Switches: 6 (monitoring, notifications, 4 notification type switches)
- Buttons: 1 (reset statistics)
- **Total**: 19 entities (was 15 in v0.1.0)

### Appliance Types Supported
- **Total**: 11 appliance types
  - Cycle-based (7): Oven, Dishwasher, Washing Machine, Dryer, Water Heater, Coffee Maker, 3D Printer
  - Session-based (3): Monitor, NAS, VMC
  - Generic: Other

### Notification Services Supported
- Mobile App (auto-detection)
- Telegram
- Persistent Notification
- Custom service (user-configurable)

## Testing Strategy

### Unit Tests
- One test file per component
- Mock Home Assistant core
- Test all state transitions
- Test error conditions
- Test edge cases

### Test Coverage
- State Machine: 15 tests (100% coverage)
- Coordinator: 13 tests
- Sensors: 13 tests
- Binary Sensors: 10 tests
- Switches: 8 tests
- Notifications: 8 tests
- Services: 5 tests
- Buttons: 3 tests

### Fixtures (`conftest.py`)
- Mock `hass` instance
- Mock config entry
- Mock coordinator
- Common test utilities

## Performance Considerations

### Optimization Strategies
- **30-second polling**: Balance between responsiveness and load
- **Efficient state checks**: Minimal computation per update
- **Smart caching**: Price data cached until changed
- **Lazy evaluation**: Statistics calculated only when needed

### Resource Usage
- **Memory**: Minimal (basic statistics only)
- **CPU**: Low (simple arithmetic operations)
- **Network**: None (local sensor polling)
- **Storage**: Minimal (persisted in config entry)

## Scalability Considerations
- Current design supports unlimited appliances
- No shared state between appliances
- Independent coordinators per appliance
- Stateless services

---

## Future Architecture Enhancements

For planned architecture improvements and future enhancements, see [IDEAS.md](docs/IDEAS.md).

---

**Version**: 0.1.0  
**Last Updated**: October 2025

