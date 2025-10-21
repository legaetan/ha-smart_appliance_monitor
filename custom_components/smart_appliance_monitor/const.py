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
CONF_UNPLUGGED_TIMEOUT = "unplugged_timeout"

# Notification Configuration
CONF_NOTIFICATION_SERVICES = "notification_services"
CONF_NOTIFICATION_TYPES = "notification_types"
CONF_CUSTOM_NOTIFY_SERVICE = "custom_notify_service"

# Auto-Shutdown Configuration
CONF_ENABLE_AUTO_SHUTDOWN = "enable_auto_shutdown"
CONF_AUTO_SHUTDOWN_DELAY = "auto_shutdown_delay"
CONF_AUTO_SHUTDOWN_ENTITY = "auto_shutdown_entity"

# Energy Management Configuration
CONF_ENABLE_ENERGY_LIMITS = "enable_energy_limits"
CONF_ENERGY_LIMIT_CYCLE = "energy_limit_cycle"
CONF_ENERGY_LIMIT_DAILY = "energy_limit_daily"
CONF_ENERGY_LIMIT_MONTHLY = "energy_limit_monthly"
CONF_COST_BUDGET_MONTHLY = "cost_budget_monthly"

# Scheduling Configuration
CONF_ENABLE_SCHEDULING = "enable_scheduling"
CONF_ALLOWED_HOURS_START = "allowed_hours_start"
CONF_ALLOWED_HOURS_END = "allowed_hours_end"
CONF_BLOCKED_DAYS = "blocked_days"
CONF_SCHEDULING_MODE = "scheduling_mode"

# Anomaly Detection Configuration
CONF_ENABLE_ANOMALY_DETECTION = "enable_anomaly_detection"

# Energy Dashboard Integration
CONF_ENABLE_ENERGY_DASHBOARD_SYNC = "enable_energy_dashboard_sync"

# Appliance Types
APPLIANCE_TYPE_OVEN = "oven"
APPLIANCE_TYPE_DISHWASHER = "dishwasher"
APPLIANCE_TYPE_WASHING_MACHINE = "washing_machine"
APPLIANCE_TYPE_DRYER = "dryer"
APPLIANCE_TYPE_WATER_HEATER = "water_heater"
APPLIANCE_TYPE_COFFEE_MAKER = "coffee_maker"
APPLIANCE_TYPE_MONITOR = "monitor"
APPLIANCE_TYPE_NAS = "nas"
APPLIANCE_TYPE_PRINTER_3D = "printer_3d"
APPLIANCE_TYPE_VMC = "vmc"
APPLIANCE_TYPE_OTHER = "other"

APPLIANCE_TYPES = [
    APPLIANCE_TYPE_OVEN,
    APPLIANCE_TYPE_DISHWASHER,
    APPLIANCE_TYPE_WASHING_MACHINE,
    APPLIANCE_TYPE_DRYER,
    APPLIANCE_TYPE_WATER_HEATER,
    APPLIANCE_TYPE_COFFEE_MAKER,
    APPLIANCE_TYPE_MONITOR,
    APPLIANCE_TYPE_NAS,
    APPLIANCE_TYPE_PRINTER_3D,
    APPLIANCE_TYPE_VMC,
    APPLIANCE_TYPE_OTHER,
]

# Types utilisant la terminologie "session" au lieu de "cycle"
SESSION_BASED_TYPES = [APPLIANCE_TYPE_MONITOR, APPLIANCE_TYPE_NAS, APPLIANCE_TYPE_VMC]

# States
STATE_IDLE = "idle"
STATE_RUNNING = "running"
STATE_FINISHED = "finished"

# Events
EVENT_CYCLE_STARTED = "cycle_started"
EVENT_CYCLE_FINISHED = "cycle_finished"
EVENT_ALERT_DURATION = "alert_duration"
EVENT_UNPLUGGED = "unplugged"
EVENT_AUTO_SHUTDOWN = "auto_shutdown"
EVENT_ENERGY_LIMIT_EXCEEDED = "energy_limit_exceeded"
EVENT_BUDGET_EXCEEDED = "budget_exceeded"
EVENT_USAGE_OUT_OF_SCHEDULE = "usage_out_of_schedule"
EVENT_ANOMALY_DETECTED = "anomaly_detected"
EVENT_ENERGY_DASHBOARD_SYNCED = "energy_dashboard_synced"

# Notification Types
NOTIF_TYPE_CYCLE_STARTED = "cycle_started"
NOTIF_TYPE_CYCLE_FINISHED = "cycle_finished"
NOTIF_TYPE_ALERT_DURATION = "alert_duration"
NOTIF_TYPE_UNPLUGGED = "unplugged"
NOTIF_TYPE_AUTO_SHUTDOWN = "auto_shutdown"
NOTIF_TYPE_ENERGY_LIMIT = "energy_limit"
NOTIF_TYPE_BUDGET = "budget"
NOTIF_TYPE_SCHEDULE = "schedule"
NOTIF_TYPE_ANOMALY = "anomaly"

# Notification Services
NOTIF_SERVICE_MOBILE_APP = "mobile_app"
NOTIF_SERVICE_TELEGRAM = "telegram"
NOTIF_SERVICE_PERSISTENT = "persistent_notification"
NOTIF_SERVICE_CUSTOM = "custom"

NOTIFICATION_SERVICES = [
    NOTIF_SERVICE_MOBILE_APP,
    NOTIF_SERVICE_TELEGRAM,
    NOTIF_SERVICE_PERSISTENT,
    NOTIF_SERVICE_CUSTOM,
]

NOTIFICATION_TYPES = [
    NOTIF_TYPE_CYCLE_STARTED,
    NOTIF_TYPE_CYCLE_FINISHED,
    NOTIF_TYPE_ALERT_DURATION,
    NOTIF_TYPE_UNPLUGGED,
    NOTIF_TYPE_AUTO_SHUTDOWN,
    NOTIF_TYPE_ENERGY_LIMIT,
    NOTIF_TYPE_BUDGET,
    NOTIF_TYPE_SCHEDULE,
    NOTIF_TYPE_ANOMALY,
]

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
SENSOR_DAILY_ENERGY = "daily_energy"
SENSOR_MONTHLY_COST = "monthly_cost"
SENSOR_MONTHLY_ENERGY = "monthly_energy"
SENSOR_ANOMALY_SCORE = "anomaly_score"

# Default Values
DEFAULT_PRICE_KWH = 0.2516
DEFAULT_START_THRESHOLD = 50
DEFAULT_STOP_THRESHOLD = 5
DEFAULT_START_DELAY = 120
DEFAULT_STOP_DELAY = 300
DEFAULT_ALERT_DURATION = 7200
DEFAULT_UNPLUGGED_TIMEOUT = 300  # 5 minutes
DEFAULT_AUTO_SHUTDOWN_DELAY = 1800  # 30 minutes
DEFAULT_SCHEDULING_MODE = "notification_only"  # or "strict_block"
DEFAULT_NOTIFICATION_SERVICES = [NOTIF_SERVICE_MOBILE_APP, NOTIF_SERVICE_PERSISTENT]
DEFAULT_NOTIFICATION_TYPES = [
    NOTIF_TYPE_CYCLE_STARTED,
    NOTIF_TYPE_CYCLE_FINISHED,
    NOTIF_TYPE_ALERT_DURATION,
    NOTIF_TYPE_UNPLUGGED,
]

# Scheduling Modes
SCHEDULING_MODE_NOTIFICATION = "notification_only"
SCHEDULING_MODE_STRICT = "strict_block"

# Days of Week
DAYS_OF_WEEK = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

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
    APPLIANCE_TYPE_MONITOR: {
        "start_threshold": 30,  # Écran: détection allumage
        "stop_threshold": 5,  # Mode veille/éteint
        "start_delay": 60,
        "stop_delay": 120,
        "alert_duration": 28800,  # 8h - sessions longues
    },
    APPLIANCE_TYPE_NAS: {
        "start_threshold": 50,  # Activité intensive (baseline ~30W)
        "stop_threshold": 20,  # Retour à idle ou arrêt
        "start_delay": 180,  # Confirmer début backup/transfert
        "stop_delay": 300,  # Fin d'activité confirmée
        "alert_duration": 21600,  # 6h pour backups longs
    },
    APPLIANCE_TYPE_PRINTER_3D: {
        "start_threshold": 50,  # Imprimante 3D: démarrage impression
        "stop_threshold": 10,  # Certaines gardent ventilo actif
        "start_delay": 120,
        "stop_delay": 180,
        "alert_duration": 86400,  # 24h - impressions très longues
    },
    APPLIANCE_TYPE_VMC: {
        "start_threshold": 20,  # VMC: passage en mode boost
        "stop_threshold": 10,  # Retour mode normal/arrêt
        "start_delay": 60,
        "stop_delay": 120,
        "alert_duration": 7200,  # 2h pour un boost long
    },
    APPLIANCE_TYPE_OTHER: {
        "start_threshold": DEFAULT_START_THRESHOLD,
        "stop_threshold": DEFAULT_STOP_THRESHOLD,
        "start_delay": DEFAULT_START_DELAY,
        "stop_delay": DEFAULT_STOP_DELAY,
        "alert_duration": DEFAULT_ALERT_DURATION,
    },
}

