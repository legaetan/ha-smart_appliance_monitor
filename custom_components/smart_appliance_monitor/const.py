"""Constants for the Smart Appliance Monitor integration."""

# Domain
DOMAIN = "smart_appliance_monitor"

# Configuration
CONF_APPLIANCE_NAME = "appliance_name"
CONF_APPLIANCE_TYPE = "appliance_type"
CONF_POWER_SENSOR = "power_sensor"
CONF_ENERGY_SENSOR = "energy_sensor"
CONF_PRICE_KWH = "price_kwh"
CONF_PRICE_ENTITY = "price_entity"  # Nouvelle option: entité pour le prix

# Advanced Configuration
CONF_START_THRESHOLD = "start_threshold"
CONF_STOP_THRESHOLD = "stop_threshold"
CONF_START_DELAY = "start_delay"
CONF_STOP_DELAY = "stop_delay"
CONF_ENABLE_ALERT_DURATION = "enable_alert_duration"
CONF_ALERT_DURATION = "alert_duration"

# Appliance Types
APPLIANCE_TYPE_OVEN = "oven"
APPLIANCE_TYPE_DISHWASHER = "dishwasher"
APPLIANCE_TYPE_WASHING_MACHINE = "washing_machine"
APPLIANCE_TYPE_DRYER = "dryer"
APPLIANCE_TYPE_WATER_HEATER = "water_heater"
APPLIANCE_TYPE_COFFEE_MAKER = "coffee_maker"
APPLIANCE_TYPE_OTHER = "other"

APPLIANCE_TYPES = [
    APPLIANCE_TYPE_OVEN,
    APPLIANCE_TYPE_DISHWASHER,
    APPLIANCE_TYPE_WASHING_MACHINE,
    APPLIANCE_TYPE_DRYER,
    APPLIANCE_TYPE_WATER_HEATER,
    APPLIANCE_TYPE_COFFEE_MAKER,
    APPLIANCE_TYPE_OTHER,
]

# States
STATE_IDLE = "idle"
STATE_RUNNING = "running"
STATE_FINISHED = "finished"

# Events
EVENT_CYCLE_STARTED = "cycle_started"
EVENT_CYCLE_FINISHED = "cycle_finished"
EVENT_ALERT_DURATION = "alert_duration"

# Sensor Types
SENSOR_STATE = "state"
SENSOR_CYCLE_DURATION = "cycle_duration"
SENSOR_CYCLE_ENERGY = "cycle_energy"
SENSOR_CYCLE_COST = "cycle_cost"
SENSOR_LAST_CYCLE_DURATION = "last_cycle_duration"
SENSOR_LAST_CYCLE_ENERGY = "last_cycle_energy"
SENSOR_LAST_CYCLE_COST = "last_cycle_cost"
SENSOR_DAILY_CYCLES = "daily_cycles"
SENSOR_DAILY_COST = "daily_cost"
SENSOR_MONTHLY_COST = "monthly_cost"

# Default Values
DEFAULT_PRICE_KWH = 0.2516
DEFAULT_START_THRESHOLD = 50
DEFAULT_STOP_THRESHOLD = 5
DEFAULT_START_DELAY = 120
DEFAULT_STOP_DELAY = 300
DEFAULT_ALERT_DURATION = 7200

# Profils d'appareils avec seuils optimisés
APPLIANCE_PROFILES = {
    APPLIANCE_TYPE_OVEN: {
        "start_threshold": 100,  # Four: puissance élevée
        "stop_threshold": 10,
        "start_delay": 60,  # Démarrage rapide
        "stop_delay": 180,  # Arrêt lent (refroidissement)
        "alert_duration": 7200,  # 2h
    },
    APPLIANCE_TYPE_DISHWASHER: {
        "start_threshold": 20,  # Lave-vaisselle: puissance variable
        "stop_threshold": 5,
        "start_delay": 120,
        "stop_delay": 300,
        "alert_duration": 10800,  # 3h
    },
    APPLIANCE_TYPE_WASHING_MACHINE: {
        "start_threshold": 10,  # Lave-linge: puissance variable
        "stop_threshold": 5,
        "start_delay": 120,
        "stop_delay": 300,
        "alert_duration": 10800,  # 3h
    },
    APPLIANCE_TYPE_DRYER: {
        "start_threshold": 100,  # Sèche-linge: puissance élevée
        "stop_threshold": 10,
        "start_delay": 60,
        "stop_delay": 180,
        "alert_duration": 7200,  # 2h
    },
    APPLIANCE_TYPE_WATER_HEATER: {
        "start_threshold": 1000,  # Chauffe-eau: très haute puissance
        "stop_threshold": 50,
        "start_delay": 60,
        "stop_delay": 120,
        "alert_duration": 14400,  # 4h
    },
    APPLIANCE_TYPE_COFFEE_MAKER: {
        "start_threshold": 50,  # Machine à café: puissance moyenne
        "stop_threshold": 5,
        "start_delay": 30,  # Très rapide
        "stop_delay": 60,  # Très rapide
        "alert_duration": 1800,  # 30min
    },
    APPLIANCE_TYPE_OTHER: {
        "start_threshold": DEFAULT_START_THRESHOLD,
        "stop_threshold": DEFAULT_STOP_THRESHOLD,
        "start_delay": DEFAULT_START_DELAY,
        "stop_delay": DEFAULT_STOP_DELAY,
        "alert_duration": DEFAULT_ALERT_DURATION,
    },
}

