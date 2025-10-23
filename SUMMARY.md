# Résumé - Ajout du Profil Climatisation et Analyse des Appliances

**Date**: 23 octobre 2025

## ✅ Modifications Effectuées

### 1. Nouveau Profil "air_conditioner" (Climatisation)

**Fichiers modifiés:**
- `custom_components/smart_appliance_monitor/const.py`
- `custom_components/smart_appliance_monitor/strings.json` 
- `custom_components/smart_appliance_monitor/translations/fr.json`

**Profil créé:**
```python
APPLIANCE_TYPE_AIR_CONDITIONER = "air_conditioner"

APPLIANCE_PROFILES = {
    "air_conditioner": {
        "start_threshold": 50,      # Démarrage compresseur
        "stop_threshold": 20,       # Arrêt compresseur (veille ~12W)
        "start_delay": 120,         # 2 minutes
        "stop_delay": 300,          # 5 minutes (cycles du compresseur)
        "alert_duration": 43200,    # 12 heures
    },
}
```

**Traductions ajoutées:**
- English: "Air Conditioner"
- Français: "Climatisation"

---

## 📊 Analyse des Appliances (20-23 octobre 2025)

### Appliances analysées avec recommandations:

| Appliance | Type | Actuels | Recommandés | Statut |
|-----------|------|---------|-------------|--------|
| **Lave Linge** | washing_machine | 10W / 10W | 580W / 45W | ⚠️ À ajuster |
| **Lave Vaisselle** | dishwasher | 20W / 5W | 580W / 100W | ⚠️ À ajuster |
| **Séche Linge** | dryer | 50W / 15W | 620W / 310W | ⚠️ À ajuster |
| **Bambulab X1C** | printer_3d | 50W / 10W | 20W / 5W | ⚠️ À ajuster |
| **Ecran PC** | monitor | 50W / 5W | 130W / 105W | ⚠️ À ajuster |
| **Chauffe-Eau** | water_heater | 1000W / 50W | - | ✅ Seuils OK (ignorer algo) |
| **Four** | oven | 100W / 10W | - | ℹ️ Pas assez utilisé |
| **VMC** | vmc | 10W / 3W | - | ℹ️ Pas assez utilisé |
| **Bureau PC** | other | N/A | - | ⏭️ Ignoré (type other) |
| **Clim** | other | N/A | - | ⏭️ Ignoré (type other) |

**Note:** Les appliances de type "other" gardent les valeurs par défaut comme demandé.

---

## 🚀 Prochaines Étapes

### Option A: Application Automatique (Recommandé) ✨

Utiliser le script pour appliquer automatiquement les seuils optimisés:

```bash
python3 tools/update_thresholds.py
```

Le script va:
1. Afficher les seuils actuels vs optimisés pour chaque appliance
2. Demander confirmation avant chaque modification
3. Mettre à jour automatiquement les configurations
4. Proposer de redémarrer Home Assistant

**Avantage:** Rapide et fiable, applique tous les changements en quelques secondes!

---

### Option B: Application Manuelle

#### 1. Synchroniser et Redémarrer HA

```bash
# Syncthing (automatique si configuré) ou:
source .ha_config
rsync -avz -e "ssh -i $HA_SSH_ID_RSA" \
  custom_components/smart_appliance_monitor/ \
  $HA_SSH_USER@$HA_SSH_HOST:/config/custom_components/smart_appliance_monitor/

# Redémarrer HA
curl -X POST -H "Authorization: Bearer $HA_TOKEN" \
  -H "Content-Type: application/json" \
  "$HA_URL/api/services/homeassistant/restart"
```

##### 2. Configurer la Climatisation

1. Aller dans **Settings → Devices & Services → Smart Appliance Monitor**
2. Trouver l'appliance **"Clim"**
3. Cliquer sur **Reconfigure**
4. Changer le type: **Other → Climatisation**
5. Les seuils optimaux (50W / 20W) seront automatiquement appliqués

#### 3. Ajuster les Autres Appliances (Optionnel)

Pour les appliances avec des seuils incorrects (Lave Linge, Lave Vaisselle, etc.):
1. Aller dans **Settings → Devices & Services → Smart Appliance Monitor**
2. Cliquer sur l'appliance → **Configure → Advanced Configuration**
3. Appliquer les seuils recommandés ci-dessus

---

## 📁 Structure des Fichiers

### Nouveaux fichiers:
```
tools/
├── analyze_appliances.py      # Script d'analyse des appliances
├── update_thresholds.py        # Script d'application automatique des seuils ✨
├── analysis_results.json       # Résultats de l'analyse (20-23 oct)
└── README.md                   # Documentation des scripts
```

### Fichiers modifiés:
```
custom_components/smart_appliance_monitor/
├── const.py                    # Ajout profil air_conditioner
├── strings.json                # Traduction EN
└── translations/fr.json        # Traduction FR
```

---

## 🔧 Scripts Utilitaires

### 1. Analyse des seuils

Le script `tools/analyze_appliances.py` peut être réutilisé pour analyser les seuils des appliances:

```bash
cd /home/legaetan/syncthing_lega.wtf_stacks/HA/ha-smart_appliance_monitor
python3 tools/analyze_appliances.py
```

**Fonctionnalités:**
- Analyse l'historique de puissance de toutes les appliances
- Calcule les seuils optimaux basés sur les données réelles
- Compare avec les seuils actuels
- Ignore les appliances "other" (valeurs par défaut conservées)
- Génère un rapport avec recommandations

### 2. Application automatique des seuils ✨

Le script `tools/update_thresholds.py` applique automatiquement les seuils optimisés:

```bash
python3 tools/update_thresholds.py
```

**Fonctionnalités:**
- Affiche les seuils actuels vs optimisés
- Demande confirmation avant chaque modification
- Met à jour automatiquement via SSH
- Propose de redémarrer Home Assistant
- **Gain de temps énorme!**

---

## 📝 Notes Importantes

1. **Profil Climatisation**: Les seuils 50W/20W sont optimaux pour détecter les cycles du compresseur sans faux positifs.

2. **Appliances "other"**: Le Bureau PC et la Clim gardent les valeurs par défaut car ils sont configurés comme "other". Pour la Clim, il faut la reconfigurer en type "Climatisation".

3. **Chauffe-Eau**: Les seuils actuels (1000W/50W) sont corrects malgré les recommandations de l'algorithme (0W/0W sont fausses).

4. **Lave Linge/Vaisselle**: Les seuils actuels (10W/10W et 20W/5W) sont trop bas et causent beaucoup de faux positifs. Les seuils recommandés (580W/45W et 580W/100W) sont plus appropriés.

---

**Résumé créé le**: 23 octobre 2025  
**Outils utilisés**: `analyze_appliances.py`

