# Tools - Scripts Utilitaires

Ce dossier contient les scripts utilitaires pour l'analyse et la maintenance de Smart Appliance Monitor.

## Scripts Disponibles

### 1. `analyze_appliances.py` - Analyse des seuils

Script d'analyse des appliances configurés pour déterminer les seuils optimaux.

**Utilisation:**
```bash
python3 tools/analyze_appliances.py
```

**Fonctionnalités:**
- Récupère toutes les appliances Smart Appliance Monitor configurées
- Analyse l'historique de puissance depuis le 20 octobre 2025
- Calcule les seuils optimaux (start/stop threshold) basés sur les données réelles
- Compare avec les seuils actuellement configurés
- Génère un rapport détaillé avec recommandations
- Ignore les appliances de type "other" (valeurs par défaut conservées)

**Sortie:**
- Rapport d'analyse dans la console
- Fichier `tools/analysis_results.json` avec les résultats détaillés

---

### 2. `update_thresholds.py` - Application des seuils optimisés

Script pour appliquer automatiquement les seuils optimisés aux appliances existantes via modification du fichier de configuration.

**Utilisation:**
```bash
python3 tools/update_thresholds.py
```

**Fonctionnalités:**
- Récupère toutes les appliances configurées
- Propose les nouveaux seuils optimisés pour chaque type d'appliance
- Demande confirmation avant chaque modification
- Met à jour le fichier `.storage/core.config_entries` via SSH
- Propose de redémarrer Home Assistant après les modifications

**Seuils appliqués:**
- **Lave Linge**: 100W / 20W (détection rapide: 60s / 120s)
- **Lave Vaisselle**: 150W / 50W (détection rapide: 60s / 120s)
- **Séche Linge**: 200W / 50W (détection rapide: 30s / 120s)
- **Imprimante 3D**: 30W / 10W (détection rapide: 60s / 120s)
- **Écran PC**: 40W / 5W (détection rapide: 30s / 60s)
- **Chauffe-Eau**: 1000W / 50W (détection rapide: 30s / 60s)
- **VMC**: 20W / 10W (détection rapide: 30s / 60s)

**Prérequis:**
- Accès SSH à Home Assistant configuré dans `.ha_config`
- Modules Python: `requests`, `json`, `subprocess`

---

## Prérequis Généraux

Les deux scripts nécessitent:
- Fichier `.ha_config` configuré avec HA_URL, HA_TOKEN et accès SSH
- Python 3.7+
- Modules: `requests`, `json`, `subprocess`, `datetime`, `statistics`

## Installation des dépendances

```bash
pip3 install requests
```

## Notes

- Les scripts utilisent SSH pour accéder au fichier de configuration Home Assistant
- `update_thresholds.py` modifie directement le fichier `.storage/core.config_entries`
- Un redémarrage de Home Assistant est nécessaire après modification des seuils
