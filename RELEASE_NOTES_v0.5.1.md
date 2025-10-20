# Smart Appliance Monitor v0.5.1 - Release Notes

**Date de Release**: 20 octobre 2025

## 🎯 Focus de cette Version

Cette version **0.5.1** résout un problème critique : **la perte de données lors du redémarrage de Home Assistant**. Désormais, tous vos cycles en cours et vos statistiques sont automatiquement sauvegardés et restaurés.

## 🔒 Nouveauté Majeure : Persistance des États

### Le Problème Résolu

**Avant v0.5.1** :
- ❌ Un cycle de lave-linge en cours lors d'un redémarrage de HA était perdu
- ❌ Les statistiques de durée et d'énergie étaient incorrectes
- ❌ L'historique des cycles était réinitialisé
- ❌ Les utilisateurs perdaient leurs données lors de mises à jour ou redémarrages

**Avec v0.5.1** :
- ✅ Les cycles en cours continuent automatiquement après le redémarrage
- ✅ Les statistiques sont préservées et restent précises
- ✅ L'historique est sauvegardé pour la détection d'anomalies
- ✅ Aucune intervention manuelle nécessaire

### Comment ça Marche ?

Le système de persistance est **entièrement automatique** :

#### Sauvegarde Automatique
- ✅ **Au démarrage d'un cycle** : État initial sauvegardé
- ✅ **À la fin d'un cycle** : Statistiques complètes enregistrées
- ✅ **Toutes les 30 secondes** : Mise à jour pendant le cycle

#### Restauration Intelligente
- ✅ **Au démarrage de HA** : Tous les états sont restaurés
- ✅ **Validation des données** : Les statistiques obsolètes sont réinitialisées
  - Stats journalières d'un autre jour → Remises à zéro
  - Stats mensuelles d'un autre mois → Remises à zéro
  - Cycles en cours → Toujours restaurés

#### Emplacement de Stockage
```
/config/.storage/smart_appliance_monitor.<entry_id>.json
```

### Exemple Concret

#### Scénario : Lave-Linge + Redémarrage HA

1. **21:00** - Démarrage du lave-linge
   - 💾 Sauvegarde : Cycle démarré à 21:00, énergie initiale 1.234 kWh

2. **21:30** - Vous redémarrez Home Assistant (mise à jour, etc.)
   - 📂 Chargement automatique du fichier de sauvegarde
   - ♻️ Restauration : État `running`, cycle commencé à 21:00

3. **21:45** - Le lave-linge se termine
   - ✅ Détection correcte de la fin
   - 📊 **Durée calculée : 45 minutes** (depuis 21:00, pas depuis 21:30 !)
   - 💰 **Énergie et coût corrects**
   - 🔔 Notification avec les bonnes valeurs

### Ce qui est Sauvegardé

Le système préserve toutes les données importantes :

1. **État du Cycle**
   - État actuel (`idle`, `running`, `finished`)
   - Heure de démarrage
   - Énergie initiale
   - Puissance de pic

2. **Dernier Cycle Terminé**
   - Durée complète
   - Énergie consommée
   - Coût calculé

3. **Statistiques Journalières**
   - Date
   - Nombre de cycles
   - Énergie totale
   - Coût total

4. **Statistiques Mensuelles**
   - Année et mois
   - Énergie totale
   - Coût total

5. **Historique des Cycles**
   - 10 derniers cycles pour la détection d'anomalies

6. **Configuration**
   - Monitoring activé/désactivé
   - Notifications activées/désactivées

## 📁 Format de Stockage

Les données sont stockées en JSON :

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

## 🔧 Implémentation Technique

### Fichiers Créés

1. **`docs/PERSISTENCE.md`** (183 lignes)
   - Documentation technique complète
   - Format de stockage
   - Exemples d'utilisation
   - Maintenance

2. **`RESUME_PERSISTANCE.md`** (150 lignes)
   - Résumé d'implémentation en français
   - Problème et solution
   - Modifications apportées

3. **`tests/test_persistence.py`** (279 lignes)
   - Suite de tests complète (11 tests)
   - Tests de sérialisation/désérialisation
   - Tests de sauvegarde/restauration
   - Tests de validation des données

### Fichiers Modifiés

1. **`custom_components/smart_appliance_monitor/__init__.py`** (+4 lignes)
   - Appel de `restore_state()` au setup

2. **`custom_components/smart_appliance_monitor/coordinator.py`** (+186 lignes)
   - Système complet de persistance
   - Méthodes de sérialisation/désérialisation
   - Sauvegarde automatique dans les événements
   - Restauration avec validation

## ✅ Compatibilité et Migration

### Rétrocompatibilité

✅ **100% rétrocompatible** avec v0.5.0 :
- Aucune modification de configuration nécessaire
- Les configurations existantes fonctionnent immédiatement
- Première sauvegarde automatique lors du prochain cycle

### Migration

**Aucune action requise** de la part des utilisateurs :
1. Installez v0.5.1
2. Redémarrez Home Assistant
3. Le système commence automatiquement à sauvegarder

**Note** : Le premier redémarrage après installation ne restaurera rien (aucune sauvegarde existante), mais tous les redémarrages suivants bénéficieront de la persistance.

## 🎉 Bénéfices Utilisateur

### 1. Aucune Perte de Données
- Vos cycles ne sont plus interrompus par les redémarrages
- Les statistiques restent fiables et précises
- L'historique est préservé

### 2. Meilleure Expérience
- Transparence totale : vous ne remarquez aucune différence
- Fiabilité accrue : vos données sont toujours là
- Confiance : plus de crainte de redémarrer HA

### 3. Détection d'Anomalies Fiable
- L'historique des cycles est préservé
- L'analyse ML reste pertinente
- Les patterns sont correctement identifiés

### 4. Statistiques Précises
- Durées calculées depuis le vrai début du cycle
- Énergie et coûts exacts
- Notifications avec les bonnes valeurs

## 📊 Performance

Le système de persistance est optimisé :

- ⚡ **Sauvegarde asynchrone** : Non bloquante, n'impacte pas les performances
- ⚡ **Fichiers légers** : < 5 Ko typiquement par appareil
- ⚡ **Impact minimal** : Sauvegarde toutes les 30s seulement si cycle en cours
- ⚡ **Restauration rapide** : Chargement instantané au démarrage

## 🔍 Gestion des Erreurs

Le système est **résilient** :

- **Fichier corrompu** : L'intégration démarre avec valeurs par défaut
- **Fichier manquant** : Première initialisation normale
- **Échec de sauvegarde** : Erreur loggée, fonctionnement continue
- **Échec de restauration** : Démarrage propre sans données restaurées

## 📚 Documentation

### Documentation Technique

- **[docs/PERSISTENCE.md](docs/PERSISTENCE.md)** - Documentation complète du système
  - Vue d'ensemble
  - Format de stockage
  - Fonctionnement détaillé
  - Exemples d'usage
  - Maintenance

### Documentation Utilisateur (Wiki)

- Mise à jour du wiki avec informations de persistance
- Section "State Persistence" dans Features Guide
- Mentions dans Home page

## 🚀 Installation et Mise à Jour

### Nouveaux Utilisateurs

1. Téléchargez `smart_appliance_monitor-0.5.1.zip`
2. Décompressez dans `/config/custom_components/`
3. Redémarrez Home Assistant
4. Configurez vos appareils via l'interface

### Mise à Jour depuis v0.5.0

1. Remplacez le contenu de `/config/custom_components/smart_appliance_monitor/`
2. Redémarrez Home Assistant
3. ✅ Vos configurations sont préservées
4. ✅ La persistance commence automatiquement

### Mise à Jour depuis v0.4.x ou antérieur

1. Installez v0.5.1
2. Redémarrez Home Assistant
3. Vos appareils continuent de fonctionner
4. Accédez aux nouvelles fonctionnalités v0.5.0 via **Options** si désiré

## 🐛 Corrections de Bugs

Cette version corrige :
- ❌ **Perte de cycles en cours** lors de redémarrage HA → ✅ Résolu
- ❌ **Durées incorrectes** après redémarrage → ✅ Résolu
- ❌ **Statistiques réinitialisées** lors de redémarrage → ✅ Résolu
- ❌ **Historique perdu** pour détection d'anomalies → ✅ Résolu

## ⚠️ Breaking Changes

**Aucun breaking change** dans cette version !

Toutes les configurations existantes continuent de fonctionner sans modification.

## 🔮 Prochaines Étapes

### Version 0.6.0 (Prévue Q4 2025)

- **Custom Cards** : Cartes Lovelace dédiées
- **Mode strict** : Blocage physique avec scheduling
- **Graphiques avancés** : Historique de consommation
- **Multi-tarifs** : Support tarifs HP/HC automatiques

## 💡 Exemples d'Utilisation

### Cas d'Usage 1 : Maintenance HA

```
Avant v0.5.1 :
- Lave-linge démarre à 21:00
- Mise à jour HA à 21:30
- Cycle perdu, statistiques fausses ❌

Avec v0.5.1 :
- Lave-linge démarre à 21:00
- Mise à jour HA à 21:30
- Cycle continue, données exactes ✅
```

### Cas d'Usage 2 : Redémarrage Imprévu

```
Avant v0.5.1 :
- Imprimante 3D en cours (8h d'impression)
- Coupure électrique brève
- HA redémarre, impression tracking perdu ❌

Avec v0.5.1 :
- Imprimante 3D en cours (8h d'impression)
- Coupure électrique brève
- HA redémarre, impression tracking restauré ✅
```

### Cas d'Usage 3 : Statistiques Mensuelles

```
Avant v0.5.1 :
- 15 cycles ce mois, 25€
- Redémarrage HA
- Statistiques mensuelles perdues ❌

Avec v0.5.1 :
- 15 cycles ce mois, 25€
- Redémarrage HA
- Statistiques mensuelles préservées ✅
```

## 🙏 Remerciements

Merci à tous les utilisateurs qui ont signalé ce problème et aidé à identifier les cas d'usage critiques.

## 📞 Support

- **Issues** : [GitHub Issues](https://github.com/legaetan/ha-smart_appliance_monitor/issues)
- **Discussions** : [GitHub Discussions](https://github.com/legaetan/ha-smart_appliance_monitor/discussions)
- **Wiki** : [Documentation Complète](https://github.com/legaetan/ha-smart_appliance_monitor/wiki)

## 📥 Téléchargement

- **Archive ZIP** : `smart_appliance_monitor-0.5.1.zip`
- **Taille** : 60 KB
- **Checksum SHA256** : `a040c5b0ff758ff78d368a6c727806f3e017277368efea676bb359b3f0740512`

---

**Version** : 0.5.1  
**Date** : 20 octobre 2025  
**Compatibilité** : Home Assistant 2023.x+  
**Licence** : MIT

**Changelog complet** : [CHANGELOG.md](CHANGELOG.md)

