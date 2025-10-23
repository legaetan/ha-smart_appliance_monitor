# Dashboard Templates - Smart Appliance Monitor

Documentation complète du système de dashboards pour Smart Appliance Monitor.

**Version**: 1.0.0  
**Dernière mise à jour**: Octobre 2025

---

## 📋 Table des Matières

- [Vue d'ensemble](#vue-densemble)
- [Architecture du système](#architecture-du-système)
- [Templates disponibles](#templates-disponibles)
- [Dashboard SAM principal](#dashboard-sam-principal)
- [Cartes génériques](#cartes-génériques)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Personnalisation](#personnalisation)
- [Entités disponibles](#entités-disponibles)
- [Services](#services)
- [Dépannage](#dépannage)

---

## Vue d'ensemble

Ce dossier contient un système complet de dashboards pour Smart Appliance Monitor, comprenant :

### 🎯 Composants principaux :

1. **Templates individuels par type d'appareil** (11 templates)
2. **Dashboard SAM principal** avec 9 vues thématiques
3. **Système de cartes génériques** réutilisables
4. **Intégration Energy Dashboard** Home Assistant

### ✨ Fonctionnalités :

- **Surveillance en temps réel** des cycles et sessions
- **Analyse IA** des patterns de consommation
- **Détection d'anomalies** avec scores et alertes
- **Gestion énergétique** (limites, budgets, planification)
- **Export de données** (CSV/JSON)
- **Statistiques complètes** (jour/semaine/mois)
- **Cartes custom modernes** avec graphiques interactifs

---

## Architecture du système

```
dashboards/
├── templates/
│   ├── _card_templates.yaml          # Cartes génériques réutilisables
│   ├── sam-energy-dashboard.yaml     # Dashboard principal (9 vues)
│   │
│   ├── generic.yaml                  # Template universel
│   │
│   ├── dishwasher.yaml               # Lave-vaisselle (cycles 2-4h)
│   ├── washing_machine.yaml          # Lave-linge (cycles 1-3h)
│   ├── dryer.yaml                    # Sèche-linge (cycles 1-3h)
│   ├── water_heater.yaml             # Chauffe-eau (cycles longs)
│   ├── oven.yaml                     # Four (cycles courts)
│   │
│   ├── monitor.yaml                  # Écran (sessions)
│   ├── desktop.yaml                  # PC Bureau (sessions)
│   ├── nas.yaml                      # NAS (activité intensive)
│   ├── printer_3d.yaml               # Imprimante 3D (impressions longues)
│   └── vmc.yaml                      # VMC (mode boost)
│
└── README.md                         # Ce fichier
```

---

## Templates disponibles

### 📦 Templates par Type d'Appareil

| Template | Type | Durée typique | Sections | Version |
|----------|------|---------------|----------|---------|
| **generic.yaml** | Universel | Variable | 10 | v1.0.0 |
| **dishwasher.yaml** | Cycles | 2-4h | 10 | v1.0.0 |
| **washing_machine.yaml** | Cycles | 1-3h | 10 | v1.0.0 |
| **dryer.yaml** | Cycles | 1-3h | 10 | v1.0.0 |
| **water_heater.yaml** | Cycles | 2-6h | 10 | v1.0.0 |
| **oven.yaml** | Cycles | 30min-3h | 10 | v1.0.0 |
| **monitor.yaml** | Sessions | Variable | 11 | v1.0.0 |
| **desktop.yaml** | Sessions | Variable | 11 | v1.0.0 |
| **nas.yaml** | Sessions | Variable | 12 | v1.0.0 |
| **printer_3d.yaml** | Cycles | Jusqu'à 24h+ | 12 | v1.0.0 |
| **vmc.yaml** | Sessions | Variable | 13 | v1.0.0 |

### 🔧 Sections communes à tous les templates :

1. **Status Overview** - Carte custom avec état en temps réel
2. **Statistics** - Carte custom avec onglets (Aujourd'hui/Semaine/Mois)
3. **Current Cycle/Session** - Gauge durée + métriques énergie/coût
4. **Power Consumption** - Graphique 24h de consommation
5. **Controls** - Switches monitoring et notifications
6. **Energy Management** - Limites et budgets
7. **Scheduling** - Planification des usages
8. **AI Analysis** - Analyse IA avec boutons et résultats
9. **Anomaly Detection** - Scores et détection d'anomalies
10. **Alerts** - Alertes conditionnelles actives

---

## Dashboard SAM principal

**Fichier** : `sam-energy-dashboard.yaml`  
**Version** : 2.0.0  
**Taille** : 1923 lignes  
**Type** : Dashboard multi-vues ultra-organisé

### 🎨 Les 9 Vues :

#### 1️⃣ **Vue d'Ensemble** (`/lovelace/sam-energy/home`)

- Métriques totales (appareils actifs, coûts jour/mois)
- Grid des 9 appareils avec navigation
- Top consommateurs du jour (bar-chart)
- Alertes actives en temps réel
- Bouton sync Energy Dashboard

#### 2️⃣ **Monitoring** (`/lovelace/sam-energy/monitoring`)

- État de tous les appareils
- Cycles/sessions en cours
- Graphique multi-courbes des puissances (24h)
- Monitoring temps réel avec ApexCharts

#### 3️⃣ **Détails Appareils** (`/lovelace/sam-energy/details`)

- Section par appareil avec :
  - Custom cycle card (graphique + actions)
  - Custom stats card (onglets détaillés)
- Vue complète pour les 9 appareils

#### 4️⃣ **Énergie & Coûts** (`/lovelace/sam-energy/energy`)

- Graphiques consommation par appareil (7j)
- Graphiques coûts quotidiens et mensuels
- Projections de coût mensuel
- Classement des consommateurs
- Budget tracking avec gauges
- Bouton sync Energy Dashboard

#### 5️⃣ **Analyse IA** (`/lovelace/sam-energy/ai`)

- Configuration globale IA
- Activation IA par appareil
- Boutons d'analyse (Pattern/Recommandations/Complète)
- Résultats d'analyse en Markdown
- Économies potentielles (kWh + €)

#### 6️⃣ **Alertes & Anomalies** (`/lovelace/sam-energy/alerts`)

- Alertes actives :
  - Alertes durée
  - Appareils débranchés
  - Limites énergie dépassées
  - Budgets dépassés
- Anomalies détectées
- Gauges scores d'anomalies
- Historique scores (7j)
- État planification (usage autorisé)

#### 7️⃣ **Gestion Énergétique** (`/lovelace/sam-energy/energy-management`)

- Activation limites énergie par appareil
- Gauges consommation vs limites
- Configuration scheduling
- Switches auto-shutdown
- Graphique tendances mensuelles

#### 8️⃣ **Contrôles Globaux** (`/lovelace/sam-energy/controls`)

- Switches monitoring (tous)
- Switches notifications master
- Notifications détaillées par type :
  - Cycle démarré
  - Cycle terminé
  - Alerte durée
  - Appareil débranché
- Boutons reset stats

#### 9️⃣ **Export & Services** (`/lovelace/sam-energy/export`)

- Export CSV par appareil
- Export JSON par appareil
- Services avancés :
  - Sync Energy Dashboard
  - Détection système tarifaire
  - Obtenir données énergie
  - Analyse Energy Dashboard globale
- Documentation historique cycles

---

## Cartes génériques

**Fichier** : `_card_templates.yaml`  
**Version** : 1.0.0

### 📦 9 Cartes réutilisables :

#### 1. **card_status_principal**
Carte Mushroom template avec :
- Status (idle/running/finished/analyzing)
- Icône colorée dynamique
- Badges d'alerte (anomalies, durée, débranché)
- Durée en cours

#### 2. **card_metrics_cycle**
Métriques du cycle actuel :
- Gauge durée avec seuils
- Statistiques énergie
- Statistiques coût

#### 3. **card_power_graph**
Graphique Mini-Graph-Card :
- Consommation 24h
- Animé avec fill fade
- Points par heure configurables

#### 4. **card_controls**
Contrôles complets :
- Switch monitoring
- Switch notifications master
- 4 switches notifications détaillées
- Bouton reset stats

#### 5. **card_stats_summary**
Résumé statistiques :
- Dernier cycle (durée/énergie/coût)
- Cycles/sessions du jour
- Coûts jour/mois

#### 6. **card_alerts**
Alertes conditionnelles :
- Durée anormale
- Appareil débranché
- Anomalie détectée

#### 7. **card_ai_analysis**
Analyse IA :
- Boutons Pattern/Recommendations/Complète
- État analyse
- Résultats markdown
- Économies potentielles

#### 8. **card_energy_management**
Gestion énergie :
- Switches limites/auto-shutdown
- Gauges énergie jour/mois
- Alertes limites

#### 9. **card_scheduling**
Planification :
- Switch scheduling
- Status usage autorisé
- Plages horaires

### 🔧 Variables de personnalisation :

```yaml
{APPLIANCE_ID}        # ID de l'appareil (ex: lave_linge)
{APPLIANCE_NAME}      # Nom affiché (ex: "Lave-Linge")
{ICON}                # Icône MDI (ex: mdi:washing-machine)
{SESSION_OR_CYCLE}    # "cycle" ou "session"
{MAX_DURATION}        # Durée max en minutes
{POWER_COLOR}         # Couleur graphique (ex: '#3498db')
```

---

## Installation

### Prérequis

#### Cartes Custom (via HACS) :

✅ **Obligatoires** :
- [Mini Graph Card](https://github.com/kalkih/mini-graph-card)
- [Mushroom Cards](https://github.com/piitaya/lovelace-mushroom)
- [ApexCharts Card](https://github.com/RomRider/apexcharts-card)
- [Bar Card](https://github.com/custom-cards/bar-card)
- [Auto Entities](https://github.com/thomasloven/lovelace-auto-entities)

🎨 **Recommandées** :
- `smart-appliance-cycle-card` (fournie dans `www/smart-appliance-cards/`)
- `smart-appliance-stats-card` (fournie dans `www/smart-appliance-cards/`)

### Installation des cartes custom SAM :

```bash
# Copier les cartes custom dans www/
cp -r custom_components/smart_appliance_monitor/www/smart-appliance-cards/ /config/www/

# Aller dans Home Assistant : Configuration → Dashboards → Resources
# Ajouter :
#   URL: /local/smart-appliance-cards/smart-appliance-cycle-card.js
#   Type: JavaScript Module
#   URL: /local/smart-appliance-cards/smart-appliance-stats-card.js
#   Type: JavaScript Module

# Redémarrer Home Assistant
```

---

## Utilisation

### 📘 Option 1 : Dashboard SAM complet

**Méthode la plus simple** - Dashboard tout-en-un avec 9 vues.

1. Aller dans **Configuration** → **Dashboards**
2. Cliquer **+ Ajouter un Dashboard**
3. Nom : `Energy (SAM)`
4. Icône : `mdi:lightning-bolt`
5. Copier le contenu de `sam-energy-dashboard.yaml`
6. **Remplacer les IDs d'appareils** :
   - `lave_linge`, `lave_vaisselle`, etc. → vos IDs réels

### 📗 Option 2 : Templates individuels

Pour créer un dashboard par appareil :

1. Choisir le template approprié (ex: `washing_machine.yaml`)
2. Copier le contenu dans un nouveau dashboard
3. **Remplacer toutes les variables** :

```yaml
# Exemple pour un lave-linge :
{APPLIANCE_ID}    → lave_linge
{APPLIANCE_NAME}  → "Lave-Linge"
{ICON}            → mdi:washing-machine
```

### 📙 Option 3 : Cartes individuelles

Pour ajouter une carte spécifique à un dashboard existant :

1. Ouvrir `_card_templates.yaml`
2. Copier la carte souhaitée (ex: `card_status_principal`)
3. Remplacer les variables `{APPLIANCE_ID}`, `{APPLIANCE_NAME}`, etc.
4. Coller dans votre dashboard

### 🔄 Service de création automatique

```yaml
service: smart_appliance_monitor.create_dashboard
data:
  entity_id: sensor.lave_linge_state
  use_custom_cards: true
```

---

## Personnalisation

### 🎨 Modifier les couleurs

```yaml
# Dans les graphiques
color: '#3498db'  # Bleu
color: '#16a085'  # Vert teal
color: '#e67e22'  # Orange
color: '#f39c12'  # Jaune
color: '#9b59b6'  # Violet
color: '#e74c3c'  # Rouge
```

### ⏱️ Adapter les seuils de durée

```yaml
# Dans les gauges
severity:
  green: 0      # Normal
  yellow: 90    # Attention (minutes)
  red: 150      # Critique (minutes)
min: 0
max: 180        # Durée maximum (minutes)
```

### 📊 Modifier les graphiques

```yaml
# Mini-graph-card
hours_to_show: 24         # Durée affichée
points_per_hour: 4        # Précision
line_width: 2             # Épaisseur ligne
animate: true             # Animations

# ApexCharts
graph_span: 7d            # 7 jours
all_series_config:
  type: line              # line, column, area
  stroke_width: 2
  curve: smooth           # smooth, straight, stepline
```

### 🖼️ Changer les icônes

Icônes disponibles sur [Material Design Icons](https://pictogrammers.com/library/mdi/)

```yaml
icon: mdi:washing-machine   # Lave-linge
icon: mdi:dishwasher        # Lave-vaisselle
icon: mdi:tumble-dryer      # Sèche-linge
icon: mdi:water-boiler      # Chauffe-eau
icon: mdi:stove             # Four
icon: mdi:printer-3d        # Imprimante 3D
icon: mdi:monitor           # Écran
icon: mdi:desktop-tower     # PC
icon: mdi:fan               # VMC
```

---

## Entités disponibles

### 📊 Sensors (par appareil)

#### État et cycle actuel :
- `sensor.{id}_state` - État (idle/running/finished/analyzing)
- `sensor.{id}_cycle_duration` - Durée cycle actuel (min)
- `sensor.{id}_cycle_energy` - Énergie cycle actuel (kWh)
- `sensor.{id}_cycle_cost` - Coût cycle actuel (€)

#### Dernier cycle :
- `sensor.{id}_last_cycle_duration` - Durée dernier cycle (min)
- `sensor.{id}_last_cycle_energy` - Énergie dernier cycle (kWh)
- `sensor.{id}_last_cycle_cost` - Coût dernier cycle (€)

#### Statistiques quotidiennes :
- `sensor.{id}_daily_cycles` - Nombre de cycles du jour
- `sensor.{id}_daily_energy` - Énergie consommée du jour (kWh)
- `sensor.{id}_daily_cost` - Coût du jour (€)

#### Statistiques mensuelles :
- `sensor.{id}_monthly_cycles` - Nombre de cycles du mois
- `sensor.{id}_monthly_energy` - Énergie consommée du mois (kWh)
- `sensor.{id}_monthly_cost` - Coût du mois (€)

#### Analyse avancée :
- `sensor.{id}_anomaly_score` - Score d'anomalie (0-100)
- `sensor.{id}_ai_analysis` - Résultats analyse IA
  - Attributs : `summary`, `recommendations`, `energy_savings_kwh`, `energy_savings_eur`

#### Puissance :
- `sensor.{id}_power` - Puissance instantanée (W)

### 🔘 Binary Sensors (par appareil)

- `binary_sensor.{id}_running` - Appareil en marche
- `binary_sensor.{id}_alert_duration` - Alerte durée anormale
- `binary_sensor.{id}_unplugged` - Appareil débranché
- `binary_sensor.{id}_energy_limit_exceeded` - Limite énergie dépassée
- `binary_sensor.{id}_budget_exceeded` - Budget dépassé
- `binary_sensor.{id}_usage_allowed` - Usage autorisé (scheduling)
- `binary_sensor.{id}_anomaly_detected` - Anomalie détectée

### 🎛️ Switches (par appareil)

#### Surveillance :
- `switch.{id}_monitoring` - Surveillance automatique active

#### Notifications :
- `switch.{id}_notifications` - Notifications master
- `switch.{id}_notification_cycle_started` - Notif démarrage cycle
- `switch.{id}_notification_cycle_finished` - Notif fin cycle
- `switch.{id}_notification_alert_duration` - Notif durée anormale
- `switch.{id}_notification_unplugged` - Notif débranché

#### Gestion énergie :
- `switch.{id}_energy_limits` - Limites énergétiques actives
- `switch.{id}_auto_shutdown` - Arrêt automatique
- `switch.{id}_scheduling` - Planification horaire

#### IA :
- `switch.{id}_ai_analysis` - Analyse IA automatique

### 🔘 Buttons (par appareil)

- `button.{id}_reset_stats` - Réinitialiser statistiques

### 🌐 Entités globales

- `select.smart_appliance_monitor_ai_task` - Tâche IA sélectionnée
- `select.smart_appliance_monitor_price_entity` - Entité prix énergie

---

## Services

### 📊 Analyse IA

#### Analyser les cycles d'un appareil
```yaml
service: smart_appliance_monitor.analyze_cycles
data:
  entity_id: sensor.lave_linge_state
  analysis_type: all                # pattern, recommendations, comparative, all
  cycle_count: 10                   # Nombre de cycles à analyser
```

#### Analyser l'Energy Dashboard global
```yaml
service: smart_appliance_monitor.analyze_energy_dashboard
data:
  days: 7                           # Nombre de jours
```

### 💾 Export de données

#### Export CSV
```yaml
service: smart_appliance_monitor.export_to_csv
data:
  entity_id: sensor.lave_linge_state
  # Fichier créé dans /config/www/sam-exports/
```

#### Export JSON
```yaml
service: smart_appliance_monitor.export_to_json
data:
  entity_id: sensor.lave_linge_state
```

### 🔄 Energy Dashboard

#### Synchroniser avec Energy Dashboard
```yaml
service: smart_appliance_monitor.sync_with_energy_dashboard
```

#### Obtenir données énergie
```yaml
service: smart_appliance_monitor.get_energy_data
data:
  period: today                     # today, week, month, year
```

### 📜 Historique

#### Obtenir historique des cycles
```yaml
service: smart_appliance_monitor.get_cycle_history
data:
  entity_id: sensor.lave_linge_state
  days: 7
```

### ⚙️ Configuration

#### Détecter système tarifaire
```yaml
service: smart_appliance_monitor.detect_tariff_system
```

#### Configurer globalement
```yaml
service: smart_appliance_monitor.set_global_config
data:
  ai_task: conversation.openai_gpt4
  price_entity: sensor.electricity_price
```

---

## Dépannage

### ❌ Problèmes courants

#### Les cartes ne s'affichent pas

**Causes possibles** :
- Entités inexistantes ou mal nommées
- Cartes custom non installées
- Erreurs de syntaxe YAML

**Solutions** :
1. Vérifier les noms d'entités dans **Outils de développement** → **États**
2. Installer les cartes custom via HACS
3. Valider le YAML avec un validateur en ligne
4. Vider le cache du navigateur (Ctrl+Shift+R)

#### Les graphiques sont vides

**Causes** :
- Pas assez de données historiques
- Capteur power non configuré
- Recorder mal configuré

**Solutions** :
1. Attendre que des données soient collectées (30s minimum)
2. Vérifier que le capteur power existe et fonctionne
3. Vérifier la configuration du recorder dans `configuration.yaml`

#### Erreur "Entity not available"

**Causes** :
- Appareil non configuré dans SAM
- Entité désactivée
- Monitoring désactivé

**Solutions** :
1. Vérifier la configuration de l'appareil dans SAM
2. Réactiver l'entité dans **Configuration** → **Entités**
3. Activer le switch monitoring

#### Les notifications ne fonctionnent pas

**Causes** :
- Notifications désactivées
- Service de notification non configuré

**Solutions** :
1. Activer `switch.{id}_notifications`
2. Activer les switches de notifications spécifiques
3. Configurer un service de notification dans HA

#### L'analyse IA ne fonctionne pas

**Causes** :
- Tâche IA non configurée
- Pas assez de cycles historiques
- API IA indisponible

**Solutions** :
1. Configurer `select.smart_appliance_monitor_ai_task`
2. Attendre d'avoir au moins 5 cycles
3. Vérifier la configuration de l'API IA (OpenAI, Claude, Ollama)

### 🔍 Debug

#### Activer les logs détaillés

Ajouter dans `configuration.yaml` :

```yaml
logger:
  default: info
  logs:
    custom_components.smart_appliance_monitor: debug
```

#### Tester les services

Aller dans **Outils de développement** → **Services** et tester manuellement chaque service.

---

## 📚 Ressources

### Documentation

- [Wiki Smart Appliance Monitor](https://github.com/legaetan/ha-smart_appliance_monitor/wiki)
- [Home Assistant Dashboards](https://www.home-assistant.io/dashboards/)
- [Lovelace YAML Mode](https://www.home-assistant.io/lovelace/yaml-mode/)

### Cartes Custom

- [HACS](https://hacs.xyz/) - Home Assistant Community Store
- [Mini Graph Card](https://github.com/kalkih/mini-graph-card)
- [Mushroom Cards](https://github.com/piitaya/lovelace-mushroom)
- [ApexCharts Card](https://github.com/RomRider/apexcharts-card)
- [Bar Card](https://github.com/custom-cards/bar-card)
- [Auto Entities](https://github.com/thomasloven/lovelace-auto-entities)

### Icônes

- [Material Design Icons](https://pictogrammers.com/library/mdi/)

---

## 🤝 Support

Pour toute question ou problème :

1. Consulter le [Wiki](https://github.com/legaetan/ha-smart_appliance_monitor/wiki)
2. Vérifier les [Issues](https://github.com/legaetan/ha-smart_appliance_monitor/issues)
3. Créer une nouvelle issue si nécessaire

---

## 📝 Changelog

### Version 1.0.0 (Octobre 2025)

**Refonte complète du système de dashboards** :

- ✨ Nouveau dashboard SAM avec 9 vues thématiques
- ✨ 11 templates individuels (7 mis à jour + 4 nouveaux)
- ✨ Système de cartes génériques réutilisables
- ✨ Intégration complète Energy Dashboard
- ✨ Support cartes custom (cycle-card, stats-card)
- ✨ Section AI Analysis dans tous les templates
- ✨ Section Anomaly Detection avec scores
- ✨ Section Energy Management complète
- ✨ Section Scheduling pour tous les appareils
- 📊 Graphiques ApexCharts pour analyses avancées
- 📊 Projections de coûts mensuels
- 🎨 Design moderne avec Mushroom Cards
- 📱 Optimisé mobile et desktop

**Nouveaux templates** :
- `water_heater.yaml` - Chauffe-eau
- `oven.yaml` - Four
- `dryer.yaml` - Sèche-linge
- `desktop.yaml` - PC Bureau

**Templates mis à jour** :
- `generic.yaml` - v1.0.0 (10 sections)
- `dishwasher.yaml` - v1.0.0 (10 sections)
- `washing_machine.yaml` - v1.0.0 (10 sections)
- `monitor.yaml` - v1.0.0 (11 sections)
- `nas.yaml` - v1.0.0 (12 sections)
- `printer_3d.yaml` - v1.0.0 (12 sections)
- `vmc.yaml` - v1.0.0 (13 sections)

---

**Made with ❤️ for Home Assistant**
