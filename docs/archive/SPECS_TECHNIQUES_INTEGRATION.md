# 🔧 Spécifications Techniques - Smart Appliance Monitor

## 📋 Specifications for Developers

Ce document contient les spécifications techniques détaillées pour développer l'intégration HACS "Smart Appliance Monitor".

## 🎯 Objectif

Créer une intégration Home Assistant native pour surveiller automatiquement les appareils électroménagers via leurs prises connectées.

## 🏗️ Architecture

### Composants principaux

```python
custom_components/smart_appliance_monitor/
├── __init__.py              # Intégration principale
├── manifest.json            # Métadonnées HACS
├── config_flow.py           # Configuration via UI
├── coordinator.py           # DataUpdateCoordinator
├── const.py                 # Constantes globales
├── sensor.py                # Capteurs (état, conso, coût)
├── binary_sensor.py         # Capteurs binaires (running, alert)
├── button.py                # Boutons (reset stats)
├── switch.py                # Switches (enable/disable monitoring)
├── entity.py                # Classe de base des entités
├── device.py                # Gestion des devices
├── services.yaml            # Définition des services
├── strings.json             # Chaînes de l'UI (anglais)
└── translations/
    ├── en.json
    └── fr.json
```

## 📦 manifest.json

```json
{
  "domain": "smart_appliance_monitor",
  "name": "Smart Appliance Monitor",
  "codeowners": ["@yourusername"],
  "config_flow": true,
  "dependencies": ["recorder"],
  "documentation": "https://github.com/yourusername/smart-appliance-monitor",
  "iot_class": "local_polling",
  "issue_tracker": "https://github.com/yourusername/smart-appliance-monitor/issues",
  "requirements": ["scikit-learn>=1.3.0"],
  "version": "0.1.0"
}
```

## 🔄 Data Flow

```
┌──────────────────┐
│  Prise connectée │
│  (power sensor)  │
└────────┬─────────┘
         │ polling (30s)
         ▼
┌──────────────────┐
│  Coordinator     │◄──── Home Assistant Core
│  (Data Manager)  │
└────────┬─────────┘
         │ update
         ▼
┌──────────────────┐
│  State Machine   │
│  (Cycle Tracker) │
└────────┬─────────┘
         │ emit events
         ▼
┌──────────────────┐
│    Entities      │
│  (Sensors, etc.) │
└──────────────────┘
```

## 🔢 Entités créées

Pour chaque appareil configuré :

### Sensors

```python
# État actuel
sensor.{appliance_id}_state
  - states: "idle", "running", "finished"
  - attributes:
    - power: float  # Puissance actuelle (W)
    - duration: int  # Durée cycle en cours (min)
    - energy: float  # Énergie cycle en cours (kWh)

# Durée du cycle en cours
sensor.{appliance_id}_cycle_duration
  - unit: "min"
  - state: int

# Consommation du cycle en cours
sensor.{appliance_id}_cycle_energy
  - unit: "kWh"
  - state: float

# Coût du cycle en cours
sensor.{appliance_id}_cycle_cost
  - unit: "€" (ou autre devise)
  - state: float

# Statistiques du dernier cycle
sensor.{appliance_id}_last_cycle_duration
sensor.{appliance_id}_last_cycle_energy
sensor.{appliance_id}_last_cycle_cost

# Statistiques globales
sensor.{appliance_id}_daily_cycles
sensor.{appliance_id}_daily_cost
sensor.{appliance_id}_monthly_cost
```

### Binary Sensors

```python
binary_sensor.{appliance_id}_running
  - device_class: "running"
  - state: on/off

binary_sensor.{appliance_id}_alert_duration
  - device_class: "problem"
  - state: on/off
```

### Switches

```python
switch.{appliance_id}_monitoring
  - Activer/désactiver la surveillance

switch.{appliance_id}_notifications
  - Activer/désactiver les notifications
```

### Buttons

```python
button.{appliance_id}_reset_stats
  - Réinitialiser les statistiques
```

## 🔧 Configuration Flow

### Étape 1 : User Step

```python
# config_flow.py
class SmartApplianceMonitorConfigFlow(config_entries.ConfigFlow):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        
        if user_input is not None:
            # Validation
            power_sensor = user_input[CONF_POWER_SENSOR]
            if not await self._validate_sensor(power_sensor):
                errors["base"] = "invalid_sensor"
            else:
                # Créer l'entrée
                return self.async_create_entry(
                    title=user_input[CONF_NAME],
                    data=user_input
                )
        
        # Schéma du formulaire
        data_schema = vol.Schema({
            vol.Required(CONF_NAME): str,
            vol.Required(CONF_APPLIANCE_TYPE): vol.In(APPLIANCE_TYPES),
            vol.Required(CONF_POWER_SENSOR): selector.EntitySelector(
                selector.EntitySelectorConfig(
                    domain="sensor",
                    device_class="power"
                )
            ),
            vol.Required(CONF_ENERGY_SENSOR): selector.EntitySelector(
                selector.EntitySelectorConfig(
                    domain="sensor",
                    device_class="energy"
                )
            ),
            vol.Optional(CONF_PRICE_KWH, default=0.2516): cv.positive_float,
        })
        
        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors
        )
```

### Étape 2 : Options Flow (configuration avancée)

```python
async def async_step_init(self, user_input=None):
    """Manage options."""
    if user_input is not None:
        return self.async_create_entry(title="", data=user_input)
    
    options_schema = vol.Schema({
        vol.Optional(
            CONF_START_THRESHOLD,
            default=self.config_entry.options.get(CONF_START_THRESHOLD, 50)
        ): vol.All(vol.Coerce(int), vol.Range(min=1, max=5000)),
        
        vol.Optional(
            CONF_STOP_THRESHOLD,
            default=self.config_entry.options.get(CONF_STOP_THRESHOLD, 5)
        ): vol.All(vol.Coerce(int), vol.Range(min=1, max=100)),
        
        vol.Optional(
            CONF_START_DELAY,
            default=self.config_entry.options.get(CONF_START_DELAY, 120)
        ): vol.All(vol.Coerce(int), vol.Range(min=10, max=600)),
        
        vol.Optional(
            CONF_STOP_DELAY,
            default=self.config_entry.options.get(CONF_STOP_DELAY, 300)
        ): vol.All(vol.Coerce(int), vol.Range(min=10, max=1800)),
        
        vol.Optional(
            CONF_ENABLE_ALERT_DURATION,
            default=self.config_entry.options.get(CONF_ENABLE_ALERT_DURATION, False)
        ): cv.boolean,
        
        vol.Optional(
            CONF_ALERT_DURATION,
            default=self.config_entry.options.get(CONF_ALERT_DURATION, 7200)
        ): vol.All(vol.Coerce(int), vol.Range(min=1800, max=21600)),
    })
    
    return self.async_show_form(
        step_id="init",
        data_schema=options_schema
    )
```

## 🔄 Coordinator

```python
# coordinator.py
class SmartApplianceCoordinator(DataUpdateCoordinator):
    """Coordonne les mises à jour de données."""
    
    def __init__(self, hass, entry):
        """Initialize."""
        self.entry = entry
        self.power_sensor = entry.data[CONF_POWER_SENSOR]
        self.energy_sensor = entry.data[CONF_ENERGY_SENSOR]
        
        # Machine à états
        self.state_machine = CycleStateMachine(
            start_threshold=entry.options.get(CONF_START_THRESHOLD, 50),
            stop_threshold=entry.options.get(CONF_STOP_THRESHOLD, 5),
            start_delay=entry.options.get(CONF_START_DELAY, 120),
            stop_delay=entry.options.get(CONF_STOP_DELAY, 300),
        )
        
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=30),
        )
    
    async def _async_update_data(self):
        """Récupère les dernières données."""
        try:
            # Récupération de la puissance
            power_state = self.hass.states.get(self.power_sensor)
            power = float(power_state.state) if power_state else 0
            
            # Récupération de l'énergie
            energy_state = self.hass.states.get(self.energy_sensor)
            energy = float(energy_state.state) if energy_state else 0
            
            # Mise à jour de la machine à états
            event = self.state_machine.update(power, energy)
            
            # Émettre les événements si nécessaire
            if event:
                self._handle_event(event)
            
            return {
                "power": power,
                "energy": energy,
                "state": self.state_machine.state,
                "cycle_data": self.state_machine.current_cycle,
            }
            
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}")
    
    def _handle_event(self, event):
        """Gère les événements de la machine à états."""
        if event == EVENT_CYCLE_STARTED:
            self._notify_cycle_started()
        elif event == EVENT_CYCLE_FINISHED:
            self._notify_cycle_finished()
        elif event == EVENT_ALERT_DURATION:
            self._notify_alert_duration()
```

## 🤖 State Machine

```python
# state_machine.py
class CycleStateMachine:
    """Machine à états pour suivre les cycles."""
    
    STATE_IDLE = "idle"
    STATE_RUNNING = "running"
    STATE_FINISHED = "finished"
    
    def __init__(self, start_threshold, stop_threshold, start_delay, stop_delay):
        self.start_threshold = start_threshold
        self.stop_threshold = stop_threshold
        self.start_delay = start_delay
        self.stop_delay = stop_delay
        
        self.state = self.STATE_IDLE
        self.current_cycle = None
        
        self._high_power_since = None
        self._low_power_since = None
    
    def update(self, power: float, energy: float) -> str | None:
        """Met à jour l'état et retourne un événement si nécessaire."""
        now = time.time()
        event = None
        
        # Détection du démarrage
        if self.state == self.STATE_IDLE:
            if power > self.start_threshold:
                if self._high_power_since is None:
                    self._high_power_since = now
                elif now - self._high_power_since >= self.start_delay:
                    # Démarrage confirmé !
                    self.state = self.STATE_RUNNING
                    self.current_cycle = {
                        "start_time": datetime.now(),
                        "start_energy": energy,
                        "peak_power": power,
                    }
                    event = EVENT_CYCLE_STARTED
                    self._high_power_since = None
            else:
                self._high_power_since = None
        
        # Détection de l'arrêt
        elif self.state == self.STATE_RUNNING:
            # Mise à jour du pic
            if power > self.current_cycle["peak_power"]:
                self.current_cycle["peak_power"] = power
            
            if power < self.stop_threshold:
                if self._low_power_since is None:
                    self._low_power_since = now
                elif now - self._low_power_since >= self.stop_delay:
                    # Arrêt confirmé !
                    self.state = self.STATE_FINISHED
                    self.current_cycle.update({
                        "end_time": datetime.now(),
                        "end_energy": energy,
                    })
                    event = EVENT_CYCLE_FINISHED
                    self._low_power_since = None
            else:
                self._low_power_since = None
        
        # État "finished" → retour à "idle"
        elif self.state == self.STATE_FINISHED:
            # Après 10 minutes, retour à idle
            if now - self.current_cycle["end_time"].timestamp() >= 600:
                self.state = self.STATE_IDLE
                self.current_cycle = None
        
        return event
```

## 📊 Sensors

```python
# sensor.py
class SmartApplianceSensor(CoordinatorEntity, SensorEntity):
    """Représente un capteur de l'appareil."""
    
    def __init__(self, coordinator, sensor_type):
        """Initialize."""
        super().__init__(coordinator)
        self._sensor_type = sensor_type
        self._attr_name = f"{coordinator.entry.data[CONF_NAME]} {SENSOR_TYPES[sensor_type]['name']}"
        self._attr_unique_id = f"{coordinator.entry.entry_id}_{sensor_type}"
        self._attr_device_class = SENSOR_TYPES[sensor_type].get("device_class")
        self._attr_native_unit_of_measurement = SENSOR_TYPES[sensor_type].get("unit")
    
    @property
    def native_value(self):
        """Return the state of the sensor."""
        if self._sensor_type == SENSOR_STATE:
            return self.coordinator.data["state"]
        
        elif self._sensor_type == SENSOR_CYCLE_DURATION:
            cycle = self.coordinator.data["cycle_data"]
            if cycle and "start_time" in cycle:
                duration = (datetime.now() - cycle["start_time"]).total_seconds() / 60
                return round(duration)
            return 0
        
        elif self._sensor_type == SENSOR_CYCLE_ENERGY:
            cycle = self.coordinator.data["cycle_data"]
            if cycle and "start_energy" in cycle:
                energy_kwh = self.coordinator.data["energy"] - cycle["start_energy"]
                return round(energy_kwh * 1000)  # Convertir en Wh
            return 0
        
        # ... autres types de capteurs

# Définition des types de capteurs
SENSOR_TYPES = {
    SENSOR_STATE: {
        "name": "State",
        "device_class": SensorDeviceClass.ENUM,
        "options": ["idle", "running", "finished"],
    },
    SENSOR_CYCLE_DURATION: {
        "name": "Cycle Duration",
        "unit": "min",
        "device_class": SensorDeviceClass.DURATION,
    },
    SENSOR_CYCLE_ENERGY: {
        "name": "Cycle Energy",
        "unit": "Wh",
        "device_class": SensorDeviceClass.ENERGY,
    },
    SENSOR_CYCLE_COST: {
        "name": "Cycle Cost",
        "unit": "€",
        "device_class": SensorDeviceClass.MONETARY,
    },
}
```

## 🔔 Notifications

```python
# notify.py
class SmartApplianceNotifier:
    """Gère les notifications."""
    
    def __init__(self, hass, config_entry):
        self.hass = hass
        self.config_entry = config_entry
    
    async def notify_cycle_started(self, appliance_name, icon):
        """Envoie une notification de démarrage."""
        await self.hass.services.async_call(
            "notify",
            "mobile_app",
            {
                "title": f"{icon} {appliance_name} démarré",
                "message": f"Le {appliance_name.lower()} vient d'être allumé.",
                "data": {
                    "notification_icon": self._get_icon(appliance_name),
                    "color": self._get_color(appliance_name),
                }
            }
        )
    
    async def notify_cycle_finished(self, appliance_name, stats):
        """Envoie une notification de fin avec statistiques."""
        message = (
            f"Le {appliance_name.lower()} a terminé.\n\n"
            f"Durée : {stats['duration']} min\n"
            f"Consommation : {stats['energy']} Wh\n"
            f"Coût : {stats['cost']} €"
        )
        
        await self.hass.services.async_call(
            "notify",
            "mobile_app",
            {
                "title": f"✅ {appliance_name} terminé",
                "message": message,
                "data": {
                    "notification_icon": self._get_icon(appliance_name, "off"),
                    "color": "#4CAF50",
                    "actions": [
                        {"action": "view_stats", "title": "Voir statistiques"},
                        {"action": "dismiss", "title": "OK"},
                    ]
                }
            }
        )
```

## 🧪 Tests

```python
# tests/test_state_machine.py
import pytest
from custom_components.smart_appliance_monitor.state_machine import CycleStateMachine

def test_cycle_start_detection():
    """Test la détection du démarrage."""
    sm = CycleStateMachine(
        start_threshold=50,
        stop_threshold=5,
        start_delay=120,
        stop_delay=300
    )
    
    # Puissance faible → pas de démarrage
    event = sm.update(10, 0)
    assert event is None
    assert sm.state == CycleStateMachine.STATE_IDLE
    
    # Puissance élevée → en attente
    event = sm.update(100, 0)
    assert event is None
    
    # Après 2 minutes → démarrage confirmé
    # (simuler le temps avec un mock)
    ...
```

## 📦 Déploiement

### Installation en développement

```bash
# Cloner le repo
git clone https://github.com/yourusername/smart-appliance-monitor.git

# Lien symbolique dans custom_components
cd /config
ln -s /path/to/smart-appliance-monitor/custom_components/smart_appliance_monitor custom_components/

# Redémarrer Home Assistant
```

### Publication sur HACS

1. Tag de release : `v0.1.0`
2. Créer `hacs.json` :
```json
{
  "name": "Smart Appliance Monitor",
  "render_readme": true,
  "domains": ["sensor", "binary_sensor", "button", "switch"]
}
```

3. Soumettre une PR à HACS : https://github.com/hacs/default

## 📝 TODO

- [ ] Implémenter le mode apprentissage
- [ ] Ajouter le support multi-devises
- [ ] Créer des graphiques de consommation
- [ ] Intégration Energy Dashboard
- [ ] Support de Google Home/Alexa
- [ ] Export de données (CSV, JSON)
- [ ] Dashboard Lovelace personnalisé
- [ ] Tests unitaires complets
- [ ] Tests d'intégration
- [ ] Documentation utilisateur

---

**Ce document est en cours de développement.**  
Contributions bienvenues ! 🤝

