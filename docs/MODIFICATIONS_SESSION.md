# Modifications Session - Dashboard Refactoring & Energy Sync

**Date**: October 23, 2025  
**Version cible**: 0.9.1 ou 1.0.0

---

## 📋 Résumé des modifications

### 1. Dashboard - Refonte complète
- Nouveau système de templates réutilisables
- Dashboard principal avec 9 vues ultra-organisées
- 11 templates d'appareils mis à jour ou créés
- Documentation complète

### 2. Energy Dashboard Sync - Améliorations majeures
- Utilisation des sensors configurés (smart plug) au lieu des sensors SAM
- Matching intelligent avec fuzzy logic (accents, noms partiels, patterns)
- **Synchronisation globale des prix** depuis Energy Dashboard
- Rapport détaillé avec source de prix et appareils synchronisés

---

## 📁 Fichiers modifiés

### Core Integration

#### `custom_components/smart_appliance_monitor/__init__.py`
**Modifications**:
- Service `handle_sync_with_energy_dashboard()` refactorisé
- Ajout de la synchronisation globale des prix (une seule lecture pour tous les appareils)
- Rapport de notification enrichi avec informations de prix
- Lignes modifiées : 693-780

#### `custom_components/smart_appliance_monitor/energy.py`
**Modifications**:
- Nouvelle méthode `sync_price_from_energy_dashboard()` (lignes 289-378)
- Méthode `get_sync_status()` modifiée pour utiliser `coordinator.energy_sensor` (lignes 229-287)
- Nouvelle méthode `_find_device_by_name_fuzzy()` pour matching intelligent (lignes 380-455)
- Support des prix dynamiques (entités) et statiques

---

### Dashboard Templates

#### `dashboards/templates/_card_templates.yaml` ✨ NOUVEAU
**Contenu**: 11 templates de cartes réutilisables (465 lignes)
- `card_status_principal`
- `card_metrics_cycle`
- `card_power_graph`
- `card_controls`
- `card_stats_summary`
- `card_alerts`
- `card_ai_analysis`
- `card_energy_management`
- `card_scheduling`
- `card_custom_cycle`
- `card_custom_stats`

#### `dashboards/templates/sam-energy-dashboard.yaml` 🔄 REFONTE COMPLÈTE
**Modifications**: Réécriture complète (1911 lignes)
- 9 vues distinctes et organisées
- Intégration de tous les 9 appareils
- Utilisation des custom cards SAM
- Remplacement de `custom:bar-card` par `entities` native (ligne 301)
- Support complet de toutes les features (AI, anomalies, énergie, scheduling)

#### Templates d'appareils mis à jour

**`dashboards/templates/generic.yaml`** - Refactorisé avec templates
**`dashboards/templates/dishwasher.yaml`** - 10 sections, templates
**`dashboards/templates/washing_machine.yaml`** - 10 sections, templates
**`dashboards/templates/monitor.yaml`** - v1.0.0, 11 sections
**`dashboards/templates/nas.yaml`** - v1.0.0, 12 sections
**`dashboards/templates/printer_3d.yaml`** - v1.0.0, 12 sections
**`dashboards/templates/vmc.yaml`** - v1.0.0, 13 sections

#### Nouveaux templates créés ✨

**`dashboards/templates/water_heater.yaml`** - 10 sections
**`dashboards/templates/oven.yaml`** - 10 sections
**`dashboards/templates/dryer.yaml`** - 10 sections
**`dashboards/templates/desktop.yaml`** - 11 sections

#### `dashboards/README.md` 🔄 MIS À JOUR
**Modifications**: Documentation complète (729 lignes)
- Guide d'utilisation des templates
- Documentation des custom cards
- Structure des templates
- Guide de personnalisation
- Troubleshooting

---

### Documentation

#### `CHANGELOG.md` 📝 MIS À JOUR
**Modifications**: Nouvelle section `[Unreleased]` (lignes 8-59)
- Dashboard Enhancements (14 lignes)
- Energy Dashboard Integration (12 lignes)
- Changed (7 lignes)
- Fixed (3 lignes)

#### `docs/ENERGY_DASHBOARD_SYNC.md` ✨ NOUVEAU
**Contenu**: Documentation technique complète (350+ lignes)
- Overview et fonctionnement
- Device detection strategies (4 stratégies de matching)
- Global price synchronization
- Service usage et output attendu
- Technical implementation (code flow)
- Configuration requirements
- Troubleshooting guide
- API reference

---

## 🗑️ Fichiers supprimés

### `custom_components/smart_appliance_monitor/dashboards/` 🗑️ SUPPRIMÉ
**Raison**: Dossier obsolète, dashboards consolidés dans `/dashboards/templates/`
**Méthode**: `rm -rf custom_components/smart_appliance_monitor/dashboards/`

---

## 🔧 Fichiers à synchroniser vers HA

### Priorité 1 - Core (requis pour Energy Sync)
```
custom_components/smart_appliance_monitor/__init__.py
custom_components/smart_appliance_monitor/energy.py
```

### Priorité 2 - Dashboard (optionnel, pour tests dashboard)
```
dashboards/templates/_card_templates.yaml
dashboards/templates/sam-energy-dashboard.yaml
dashboards/templates/generic.yaml
dashboards/templates/dishwasher.yaml
dashboards/templates/washing_machine.yaml
dashboards/templates/water_heater.yaml
dashboards/templates/oven.yaml
dashboards/templates/dryer.yaml
dashboards/templates/desktop.yaml
dashboards/templates/monitor.yaml
dashboards/templates/nas.yaml
dashboards/templates/printer_3d.yaml
dashboards/templates/vmc.yaml
dashboards/README.md
```

### Documentation (local only)
```
CHANGELOG.md
docs/ENERGY_DASHBOARD_SYNC.md
```

---

## ✅ Checklist de test

### Energy Dashboard Sync

- [ ] Synchroniser `__init__.py` et `energy.py` vers HA
- [ ] Redémarrer Home Assistant
- [ ] Ouvrir le dashboard SAM
- [ ] Cliquer sur "Synchroniser Energy Dashboard"
- [ ] Vérifier le rapport de notification:
  - [ ] Tous les appareils trouvés ("Synced: 9")
  - [ ] Prix global affiché (ex: "0.4500 €/kWh")
  - [ ] Source du prix affichée (ex: "`input_number.edf_price_kwh`")
  - [ ] "Applied to: All 9 appliances"
- [ ] Vérifier dans les logs HA:
  - [ ] Messages "Applied global price to 'XXX'"
  - [ ] Pas d'erreurs

### Dashboard Principal

- [ ] Synchroniser tous les fichiers dashboard vers HA
- [ ] Importer `sam-energy-dashboard.yaml` dans Lovelace
- [ ] Tester chaque onglet:
  - [ ] Onglet 1: Vue d'Ensemble (métriques, top consommateurs)
  - [ ] Onglet 2: Monitoring (états temps réel, graphiques)
  - [ ] Onglet 3: Détails Appareils (9 appareils avec custom cards)
  - [ ] Onglet 4: Énergie & Coûts (coûts, Energy Dashboard)
  - [ ] Onglet 5: Analyse IA (contrôles et résultats)
  - [ ] Onglet 6: Alertes & Anomalies (alertes, détection)
  - [ ] Onglet 7: Gestion Énergie (limites, budgets, scheduling)
  - [ ] Onglet 8: Contrôles Globaux (switches notifications)
  - [ ] Onglet 9: Export & Services (export, services avancés)

### Templates Individuels (optionnel)

- [ ] Tester template `dishwasher.yaml`
- [ ] Tester template `washing_machine.yaml`
- [ ] Tester template `water_heater.yaml`
- [ ] Tester template `oven.yaml`
- [ ] Tester template `dryer.yaml`
- [ ] Tester template `desktop.yaml`
- [ ] Tester template `monitor.yaml`
- [ ] Tester template `nas.yaml`
- [ ] Tester template `printer_3d.yaml`
- [ ] Tester template `vmc.yaml`

---

## 🚀 Commandes de synchronisation

### Sync rapide (Core seulement)
```bash
source .ha_config && rsync -avz \
  custom_components/smart_appliance_monitor/__init__.py \
  custom_components/smart_appliance_monitor/energy.py \
  $HA_SSH_USER@$HA_SSH_HOST:/config/custom_components/smart_appliance_monitor/
```

### Sync complet (Core + Dashboards)
```bash
source .ha_config && rsync -avz \
  --exclude='__pycache__' \
  --exclude='*.pyc' \
  custom_components/smart_appliance_monitor/ \
  $HA_SSH_USER@$HA_SSH_HOST:/config/custom_components/smart_appliance_monitor/

rsync -avz \
  dashboards/templates/ \
  $HA_SSH_USER@$HA_SSH_HOST:/config/dashboards/sam_templates/
```

### Redémarrer HA
```bash
source .ha_config && curl -X POST \
  -H "Authorization: Bearer $HA_TOKEN" \
  -H "Content-Type: application/json" \
  "$HA_URL/api/services/homeassistant/restart"
```

---

## 📊 Statistiques

### Lignes de code
- **Fichiers modifiés**: 18
- **Fichiers créés**: 6
- **Fichiers supprimés**: 7 (dossier obsolète)
- **Lignes ajoutées**: ~5000
- **Lignes modifiées**: ~200

### Fonctionnalités
- **Nouvelles features**: 2 (Energy Sync amélioré, Dashboard complet)
- **Templates créés**: 4 (water_heater, oven, dryer, desktop)
- **Templates mis à jour**: 7
- **Vues dashboard**: 9

---

## 📝 Notes importantes

### Energy Dashboard Sync
1. **Prix global** : Un seul prix pour toute la maison, pas par appareil
2. **Sensor configuré** : Utilise le sensor de la prise connectée, pas les sensors SAM
3. **Fuzzy matching** : 4 stratégies de matching pour trouver les appareils
4. **Lecture seule** : Ne modifie jamais `.storage/energy`

### Dashboard
1. **Templates réutilisables** : Toutes les cartes communes dans `_card_templates.yaml`
2. **Custom cards** : Nécessite les cartes SAM dans `www/smart-appliance-cards/`
3. **Compatibilité** : Pas de dépendances externes (bar-card retiré)
4. **9 appareils** : Lave-Linge, Lave-Vaisselle, Chauffe-Eau, Four, Sèche-Linge, Bambulab X1C, Écran PC, Bureau PC, VMC

---

## 🔜 Prochaines étapes

1. **Tests utilisateur** : Tester tous les onglets du dashboard
2. **Validation Energy Sync** : Confirmer que le prix se synchronise correctement
3. **Optimisations UI** : Ajuster les cartes selon feedback
4. **Release** : Préparer v0.9.1 ou v1.0.0
5. **Wiki** : Mettre à jour le wiki avec nouvelles features

---

**Auteur**: Assistant AI  
**Date de création**: 2025-10-23  
**Dernière mise à jour**: 2025-10-23

