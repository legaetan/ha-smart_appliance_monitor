# Smart Appliance Monitor v0.5.0 - Release Notes

**Date de Release**: 21 octobre 2025

## 🎉 Nouveautés Majeures

Cette version **0.5.0** transforme Smart Appliance Monitor d'un simple tracker de cycles en un **système complet de gestion énergétique** avec des fonctionnalités avancées d'automatisation et d'analyse.

### ✨ Extinction Automatique (Auto-Shutdown)

Économisez de l'énergie en éteignant automatiquement vos appareils après une période d'inactivité.

- **Configuration flexible** : Délai de 5 à 60 minutes
- **Contrôle par switch** : `switch.{appliance}_auto_shutdown`
- **Service manuel** : `force_shutdown` pour tests
- **Notifications** : Alerte avant extinction

**Cas d'usage** :
- Moniteur qui s'éteint après 30 min d'inactivité
- Imprimante 3D qui se coupe après impression
- Cafetière qui se désactive après 1h

### 💰 Gestion Avancée de l'Énergie

Contrôlez votre consommation avec des **limites configurables** et un **suivi budgétaire**.

**4 types de limites** :
- **Par cycle** : Limite d'énergie pour un seul cycle (ex: 2 kWh max)
- **Journalière** : Limite quotidienne (ex: 5 kWh/jour)
- **Mensuelle** : Limite mensuelle (ex: 50 kWh/mois)
- **Budget mensuel** : Limite de coût (ex: 10€/mois)

**Nouvelles entités** :
- `binary_sensor.{appliance}_energy_limit_exceeded` - Toute limite dépassée
- `binary_sensor.{appliance}_budget_exceeded` - Budget dépassé
- `sensor.{appliance}_daily_energy` - Consommation journalière (kWh)
- `sensor.{appliance}_monthly_energy` - Consommation mensuelle (kWh)
- `switch.{appliance}_energy_limits` - Activation du monitoring

**Notifications automatiques** lors du dépassement des limites.

### ⏰ Planification d'Utilisation (Scheduling)

Optimisez vos coûts énergétiques en définissant **quand** vos appareils peuvent être utilisés.

**Fonctionnalités** :
- **Plages horaires** : Ex: 22h-7h (heures creuses)
- **Jours bloqués** : Ex: pas de lessive le dimanche
- **Mode notification** : Alerte si utilisation hors horaires
- **Mode strict** : Blocage réel (à venir)

**Nouvelle entité** :
- `binary_sensor.{appliance}_usage_allowed` - Utilisation autorisée maintenant ?
- `switch.{appliance}_scheduling` - Activation de la planification

**Cas d'usage** :
- Lave-linge uniquement en heures creuses (économies)
- Lave-vaisselle silencieux (pas la nuit)
- Production solaire (10h-16h)

### 🤖 Détection d'Anomalies

**Intelligence artificielle** pour détecter les comportements inhabituels et les potentiels problèmes.

**Détections** :
- **Cycle trop court** : <50% de la durée moyenne
- **Cycle trop long** : >200% de la durée moyenne
- **Consommation anormale** : ±50% par rapport à la moyenne
- **Basé sur l'historique** : Analyse des 10 derniers cycles

**Nouvelles entités** :
- `sensor.{appliance}_anomaly_score` - Score d'anomalie 0-100%
- `binary_sensor.{appliance}_anomaly_detected` - Anomalie détectée

**Notifications** en cas de détection d'anomalie.

**Exemples d'anomalies** :
- Lave-linge bloqué 3h au lieu de 1h30 → Problème de vidange
- Lave-vaisselle 3 kWh au lieu de 1.2 kWh → Résistance défectueuse
- Cycle fini en 15 min au lieu de 45 min → Interruption utilisateur

### 📊 Export de Données

Exportez vos statistiques pour **analyse externe**, **sauvegarde** ou **reporting**.

**Formats disponibles** :
- **CSV** : Compatible Excel, Google Sheets, LibreOffice
- **JSON** : Données structurées pour APIs et scripts

**Services** :
- `smart_appliance_monitor.export_to_csv`
- `smart_appliance_monitor.export_to_json`

**Données exportées** :
- Cycle en cours et dernier cycle
- Statistiques journalières et mensuelles
- Historique des cycles (pour anomalies)
- Configuration de l'appareil

**Cas d'usage** :
- Backup hebdomadaire automatique
- Analyse Excel mensuelle
- Intégration InfluxDB/Grafana
- Upload vers cloud (Dropbox, etc.)

### ⚡ Intégration Energy Dashboard

Les capteurs d'énergie sont désormais **100% compatibles** avec le tableau de bord Énergie natif de Home Assistant.

**Capteurs compatibles** :
- `sensor.{appliance}_daily_energy`
- `sensor.{appliance}_monthly_energy`
- `sensor.{appliance}_daily_cost`
- `sensor.{appliance}_monthly_cost`

**Ajoutez facilement** vos appareils pour visualiser leur contribution à votre consommation totale.

## 📈 Statistiques

### Entités Créées

**Avant v0.5.0** : 19 entités par appareil  
**v0.5.0** : **30 entités par appareil** (+11)

**Détail** :
- **13 Sensors** (+3) : state, cycle_*, last_cycle_*, daily_*, monthly_*, anomaly_score
- **7 Binary Sensors** (+4) : running, alert_duration, unplugged, energy_limit, budget, usage_allowed, anomaly
- **9 Switches** (+3) : monitoring, notifications, notify_*, auto_shutdown, energy_limits, scheduling
- **1 Button** : reset_statistics

### Services

**3 nouveaux services** :
1. `export_to_csv` - Export CSV
2. `export_to_json` - Export JSON
3. `force_shutdown` - Force l'extinction (tests)

## 🔧 Configuration

### Flow de Configuration

Le flux de configuration a été étendu avec **3 nouveaux steps optionnels** :

**Step 3** : **Energy Management** (optionnel)
- Activer les limites énergétiques
- Configurer limites par cycle, journalières, mensuelles
- Définir budget mensuel

**Step 4** : **Scheduling** (optionnel)
- Activer la planification
- Définir plages horaires autorisées
- Bloquer des jours spécifiques
- Choisir mode (notification/strict)

**Step 5** : **Expert Settings** (amélioré)
- Activer extinction automatique
- Configurer délai d'inactivité
- Sélectionner entité à contrôler

### Rétrocompatibilité

✅ **100% rétrocompatible** : Les configurations existantes continuent de fonctionner sans modification.

Les nouvelles fonctionnalités sont **optionnelles** et **désactivées par défaut**.

## 📚 Documentation

### Nouveau Wiki

**4 nouvelles pages complètes** :
1. **[Advanced Features](wiki/Advanced-Features)** - Vue d'ensemble (60+ exemples)
2. **[Energy Management](wiki/Energy-Management)** - Guide complet gestion énergie
3. **[Scheduling](wiki/Scheduling)** - Guide planification avec cas d'usage
4. **[Data Export](wiki/Data-Export)** - Export et intégrations externes

**Pages mises à jour** :
- [Home](wiki/Home) - Version 0.5.0, nouvelles features
- [Features](wiki/Features) - Mise à jour du comptage d'entités
- [Configuration](wiki/Configuration) - Nouveaux steps

### Changelog Complet

Voir [CHANGELOG.md](CHANGELOG.md) pour tous les détails techniques.

## 🚀 Installation

### Nouveaux Utilisateurs

1. Téléchargez `smart_appliance_monitor-0.5.0.zip`
2. Décompressez dans `/config/custom_components/`
3. Redémarrez Home Assistant
4. Ajoutez l'intégration via UI

### Mise à Jour

**Depuis v0.4.x** :

1. Remplacez le contenu de `/config/custom_components/smart_appliance_monitor/`
2. Redémarrez Home Assistant
3. Vos configurations existantes sont préservées
4. Accédez aux nouvelles fonctionnalités via **Options** (⚙️ sur chaque appareil)

**Depuis v0.3.x ou antérieur** :

⚠️ Voir [Migration Guide](wiki/Migration) pour instructions spécifiques.

## 💡 Exemples d'Utilisation

### Économies d'Énergie

```yaml
# Lave-linge uniquement en heures creuses
enable_scheduling: true
allowed_hours_start: "22:00"
allowed_hours_end: "07:00"

# Budget mensuel de 10€
enable_energy_limits: true
cost_budget_monthly: 10.0
```

### Monitoring Avancé

```yaml
# Détection d'anomalies
enable_anomaly_detection: true

# Extinction auto du moniteur après 30 min
enable_auto_shutdown: true
auto_shutdown_delay: 30
auto_shutdown_entity: switch.monitor_plug
```

### Analyse et Reporting

```yaml
# Export automatique chaque semaine
automation:
  - alias: "Weekly Data Export"
    trigger:
      - platform: time
        at: "00:00:00"
    condition:
      - condition: time
        weekday: sun
    action:
      - service: smart_appliance_monitor.export_to_csv
        data:
          entity_id: sensor.washing_machine_state
          file_path: "/config/exports/washing_machine_{{ now().strftime('%Y%m%d') }}.csv"
```

## 🔍 Changements Techniques

### Nouveaux Fichiers

- `custom_components/smart_appliance_monitor/export.py` - Module d'export
- `custom_components/smart_appliance_monitor/energy.py` - Aide Energy Dashboard

### Fichiers Modifiés

**Modifications majeures** :
- `const.py` - 50+ nouvelles constantes
- `coordinator.py` - Logique toutes nouvelles features
- `config_flow.py` - 3 nouveaux steps de configuration
- `switch.py` - 3 nouveaux switches
- `binary_sensor.py` - 4 nouveaux binary sensors
- `sensor.py` - 3 nouveaux sensors
- `notify.py` - 5 nouveaux types de notifications
- `services.yaml` - 3 nouveaux services

## 🐛 Corrections

- Amélioration de la détection d'unplugged
- Meilleure gestion des resets de statistiques mensuelles
- Optimisation des vérifications toutes les 30s

## ⚠️ Breaking Changes

**Aucun breaking change** dans cette version !

Toutes les configurations existantes continuent de fonctionner sans modification.

## 📝 Notes de Migration

### Activation des Nouvelles Features

Pour activer les nouvelles fonctionnalités sur un appareil existant :

1. Allez dans **Paramètres** → **Appareils et Services**
2. Trouvez **Smart Appliance Monitor**
3. Cliquez sur **Configurer** (⚙️) à côté de votre appareil
4. Naviguez dans les steps pour activer les features désirées
5. Sauvegardez

**Aucune perte de données** : Toutes vos statistiques et historiques sont préservés.

## 🔮 Prochaines Étapes

### Version 0.6.0 (Prévue Q4 2025)

- **Custom Cards** : Cartes Lovelace dédiées
- **Mode strict** : Blocage physique avec scheduling
- **Graphiques avancés** : Historique de consommation
- **Multi-tarifs** : Support tarifs HP/HC automatiques

## 🙏 Remerciements

Merci à tous les testeurs et contributeurs qui ont aidé à façonner cette version majeure !

## 📞 Support

- **Issues** : [GitHub Issues](https://github.com/legaetan/ha-smart_appliance_monitor/issues)
- **Discussions** : [GitHub Discussions](https://github.com/legaetan/ha-smart_appliance_monitor/discussions)
- **Wiki** : [Documentation Complète](https://github.com/legaetan/ha-smart_appliance_monitor/wiki)

## 📥 Téléchargement

- **Archive ZIP** : `smart_appliance_monitor-0.5.0.zip` (73 KB)
- **Checksum SHA256** : `b7a93818994126738d9e2788a32a9f33f842c6c38b2c63d211579f3f6f0f5b72`

---

**Version** : 0.5.0  
**Date** : 21 octobre 2025  
**Compatibilité** : Home Assistant 2023.x+  
**Licence** : MIT

