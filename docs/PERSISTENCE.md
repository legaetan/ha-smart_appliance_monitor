# Système de Persistance des Cycles

## Vue d'ensemble

Le système de persistance garantit que les cycles en cours et les statistiques ne sont **pas perdus lors du redémarrage de Home Assistant**. Toutes les données importantes sont sauvegardées automatiquement dans un fichier de stockage persistant.

## Données Sauvegardées

Le système sauvegarde les données suivantes :

### 1. État de la Machine à États
- **État actuel** : `idle`, `running`, ou `finished`
- **Cycle en cours** : informations sur le cycle actuellement en cours
  - Heure de démarrage
  - Énergie de départ
  - Puissance de pic
- **Dernier cycle** : statistiques du dernier cycle terminé
  - Heure de démarrage et de fin
  - Durée (en minutes)
  - Énergie consommée (kWh)

### 2. Statistiques
- **Statistiques journalières** :
  - Date
  - Nombre de cycles
  - Énergie totale consommée
  - Coût total
- **Statistiques mensuelles** :
  - Année et mois
  - Énergie totale consommée
  - Coût total

### 3. Historique des Cycles
- Historique des derniers cycles (pour la détection d'anomalies)
- Limité aux 10 derniers cycles

### 4. Configuration
- État de la surveillance (activé/désactivé)
- État des notifications (activé/désactivé)

## Fonctionnement

### Sauvegarde Automatique

L'état est sauvegardé automatiquement dans les cas suivants :

1. **Démarrage d'un cycle** : Sauvegarde immédiate lors du démarrage
2. **Fin d'un cycle** : Sauvegarde des statistiques et du dernier cycle
3. **Pendant un cycle** : Sauvegarde périodique toutes les 30 secondes (intervalle de mise à jour)

### Restauration au Démarrage

Lors du démarrage de Home Assistant :

1. Le coordinator est créé
2. L'état est restauré depuis le fichier de stockage
3. **Validation des données** :
   - Les statistiques journalières obsolètes (autre jour) sont réinitialisées
   - Les statistiques mensuelles obsolètes (autre mois) sont réinitialisées
   - Les cycles en cours sont restaurés tels quels

### Emplacement des Fichiers

Les données sont stockées dans le répertoire `.storage` de Home Assistant :

```
<config_dir>/.storage/smart_appliance_monitor.<entry_id>.json
```

Exemple :
```
/config/.storage/smart_appliance_monitor.a1b2c3d4e5f6.json
```

## Format de Stockage

Les données sont stockées au format JSON avec la structure suivante :

```json
{
  "state": "running",
  "current_cycle": {
    "start_time": "2025-10-20T21:00:00",
    "start_energy": 1.234,
    "peak_power": 150.5
  },
  "last_cycle": {
    "start_time": "2025-10-20T19:00:00",
    "end_time": "2025-10-20T20:30:00",
    "duration": 90.0,
    "energy": 1.5
  },
  "daily_stats": {
    "date": "2025-10-20",
    "cycles": 3,
    "total_energy": 4.5,
    "total_cost": 1.13
  },
  "monthly_stats": {
    "year": 2025,
    "month": 10,
    "total_energy": 45.0,
    "total_cost": 11.32
  },
  "cycle_history": [],
  "monitoring_enabled": true,
  "notifications_enabled": true
}
```

## Sérialisation des Données

### Dates et Heures
Les objets `datetime` Python sont convertis en chaînes ISO 8601 :
- `datetime(2025, 10, 20, 21, 0, 0)` → `"2025-10-20T21:00:00"`

### Dates
Les objets `date` Python sont convertis en chaînes ISO :
- `date(2025, 10, 20)` → `"2025-10-20"`

### Cycle
Les dictionnaires de cycle sont sérialisés avec conversion des timestamps.

## Gestion des Erreurs

Le système de persistance est conçu pour être **résilient** :

- **Échec de sauvegarde** : L'erreur est loggée mais n'interrompt pas le fonctionnement
- **Données corrompues** : L'intégration démarre avec les valeurs par défaut
- **Fichier manquant** : Première initialisation normale sans restauration

## Avantages

### 1. Continuité des Cycles
Un cycle de lave-linge en cours lors d'un redémarrage de HA continue d'être suivi correctement.

### 2. Statistiques Préservées
Les statistiques du jour et du mois sont conservées même après plusieurs redémarrages.

### 3. Détection d'Anomalies
L'historique des cycles est préservé, permettant une détection d'anomalies fiable.

### 4. Expérience Utilisateur
Aucune perte de données visible par l'utilisateur lors des redémarrages.

## Exemple d'Usage

### Scénario : Cycle de Lave-Linge Interrompu

1. **21:00** : Démarrage du lave-linge
   - Détection : Puissance > seuil pendant 2 minutes
   - État : `running`
   - Sauvegarde : Cycle en cours avec heure de démarrage

2. **21:30** : Redémarrage de Home Assistant
   - Lecture du fichier de stockage
   - Restauration : État `running` + cycle démarré à 21:00

3. **21:45** : Fin du lave-linge
   - Détection : Puissance < seuil pendant 5 minutes
   - Calcul : Durée = 45 minutes (depuis 21:00)
   - Sauvegarde : Dernier cycle avec statistiques complètes

4. **Résultat** : Aucune donnée perdue, cycle tracé correctement du début à la fin

## Maintenance

### Suppression Manuelle des Données

Pour réinitialiser complètement une intégration :

1. Arrêter Home Assistant
2. Supprimer le fichier : `.storage/smart_appliance_monitor.<entry_id>.json`
3. Redémarrer Home Assistant

### Sauvegarde des Données

Les fichiers `.storage/*.json` peuvent être sauvegardés avec votre configuration Home Assistant habituelle.

## Version

- **Version actuelle du stockage** : 1
- **Compatible depuis** : v0.5.0
