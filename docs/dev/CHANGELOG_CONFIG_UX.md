# Améliorations de la configuration avancée

## Date : 20 octobre 2025

## Changements apportés

### Vue d'ensemble
L'écran de configuration avancée a été entièrement repensé pour améliorer l'expérience utilisateur. La configuration est maintenant divisée en plusieurs étapes logiques avec des unités plus intuitives.

---

## 🎯 Améliorations principales

### 1. Configuration en plusieurs étapes

Au lieu d'un seul écran avec 10 paramètres, la configuration est maintenant divisée en **4 étapes** :

#### **Étape 1 : Seuils de détection**
- Seuil de démarrage (W)
- Seuil d'arrêt (W)
- Descriptions avec exemples concrets selon le type d'appareil

#### **Étape 2 : Délais de détection et alertes**
- Délai de démarrage (en minutes au lieu de secondes)
- Délai d'arrêt (en minutes au lieu de secondes)
- Activation de l'alerte de durée
- Durée d'alerte (en heures au lieu de secondes)
- Toggle "Mode expert" pour accéder aux paramètres avancés

#### **Étape 3 : Notifications**
- Services de notification (multi-select simplifié)
- Types de notifications (multi-select simplifié)

#### **Étape 4 : Paramètres experts** (optionnel)
- Délai de détection débranché (en minutes)
- Nom du service de notification personnalisé
- Accessible uniquement si le mode expert est activé à l'étape 2

---

### 2. Unités de temps user-friendly

| Avant | Après |
|-------|-------|
| `start_delay: 120 secondes` | `start_delay: 2 minutes` |
| `stop_delay: 300 secondes` | `stop_delay: 5 minutes` |
| `alert_duration: 7200 secondes` | `alert_duration: 2 heures` |
| `unplugged_timeout: 300 secondes` | `unplugged_timeout: 5 minutes` |

**Plages de valeurs :**
- Délai de démarrage : 0.5 à 10 minutes (au lieu de 10 à 600 secondes)
- Délai d'arrêt : 0.5 à 30 minutes (au lieu de 10 à 1800 secondes)
- Durée d'alerte : 0.5 à 24 heures (au lieu de 1800 à 86400 secondes)
- Délai débranché : 1 à 60 minutes (au lieu de 60 à 3600 secondes)

---

### 3. Mode expert optionnel

Les paramètres avancés sont maintenant masqués par défaut :
- `unplugged_timeout` - Caché sauf si mode expert activé
- `custom_notify_service` - Caché sauf si mode expert activé

Avantages :
- Interface simplifiée pour les utilisateurs standard
- Pas de surcharge cognitive avec des options rarement utilisées
- Accessibles pour les power users via un simple toggle

---

### 4. Descriptions améliorées

Chaque paramètre a maintenant une description détaillée avec :
- Explications claires du comportement
- Exemples concrets adaptés au type d'appareil
- Plages de valeurs recommandées
- Valeurs par défaut indiquées

**Exemples de nouvelles descriptions :**

> **Seuil de démarrage** : Puissance minimale pour détecter le démarrage de l'appareil (ex: 100W pour un four, 10W pour un lave-linge)

> **Délai de démarrage** : Temps pendant lequel la puissance doit rester au-dessus du seuil avant de confirmer le démarrage (0,5-10 min)

---

## 🔧 Modifications techniques

### Fichiers modifiés

#### 1. `config_flow.py`
- Refactorisation complète de `SmartApplianceMonitorOptionsFlowHandler`
- Ajout de `self._options` pour persister les données entre étapes
- Nouvelle méthode : `async_step_init()` - Seuils de détection (étape 1)
- Nouvelle méthode : `async_step_delays()` - Délais et alertes (étape 2)
- Nouvelle méthode : `async_step_notifications()` - Notifications (étape 3)
- Nouvelle méthode : `async_step_expert()` - Paramètres experts (étape 4)
- Conversions automatiques minutes ↔ secondes et heures ↔ secondes
- Navigation conditionnelle : étape expert affichée uniquement si `expert_mode=True`

#### 2. `strings.json` (EN)
- Restructuration complète de la section `options.step`
- Ajout de 4 sections : `init`, `delays`, `notifications`, `expert`
- Mise à jour des labels avec les nouvelles unités
- Descriptions enrichies avec exemples et contexte

#### 3. `translations/fr.json` (FR)
- Traduction complète des 4 nouvelles étapes
- Cohérence terminologique assurée
- Descriptions détaillées en français avec exemples localisés

---

## 🔄 Rétrocompatibilité

**Les valeurs existantes sont automatiquement converties :**
- Les anciennes configurations en secondes sont lues correctement
- À l'affichage, les secondes sont converties en minutes/heures
- À la sauvegarde, les minutes/heures sont reconverties en secondes
- Aucune perte de données lors de la mise à jour

**Migration transparente :**
```python
# Ancien format (conservé en interne)
CONF_START_DELAY = 120  # secondes

# Affichage utilisateur
start_delay_minutes = 120 / 60 = 2.0  # minutes

# Sauvegarde après modification
CONF_START_DELAY = 2.0 * 60 = 120  # secondes
```

---

## 📊 Comparaison avant/après

### Avant (écran unique)
```
┌─────────────────────────────────────┐
│  Configuration avancée              │
├─────────────────────────────────────┤
│ Seuil de démarrage (W): 50          │
│ Seuil d'arrêt (W): 5                │
│ Délai de démarrage (s): 120         │
│ Délai d'arrêt (s): 300              │
│ Activer alerte: ☐                   │
│ Durée d'alerte (s): 7200            │
│ Délai débranché (s): 300            │
│ Services notif: [...]               │
│ Types notif: [...]                  │
│ Service custom: ___________         │
│                                     │
│           [  Valider  ]             │
└─────────────────────────────────────┘
```

### Après (4 écrans)

**Écran 1 : Seuils**
```
┌─────────────────────────────────────┐
│  Seuils de détection                │
├─────────────────────────────────────┤
│ Configurez les seuils de puissance  │
│ pour détecter le démarrage et       │
│ l'arrêt de votre appareil.          │
│                                     │
│ Seuil de démarrage (W): 50          │
│ ℹ Puissance minimale pour détecter  │
│   le démarrage (ex: 100W pour four) │
│                                     │
│ Seuil d'arrêt (W): 5                │
│ ℹ Puissance maximale pour détecter  │
│   l'arrêt (ex: 10W pour four)       │
│                                     │
│           [  Suivant  ]             │
└─────────────────────────────────────┘
```

**Écran 2 : Délais**
```
┌─────────────────────────────────────┐
│  Délais de détection et alertes     │
├─────────────────────────────────────┤
│ Configurez combien de temps la      │
│ puissance doit rester stable.       │
│                                     │
│ Délai de démarrage: 2 min           │
│ ℹ Temps au-dessus du seuil (0,5-10) │
│                                     │
│ Délai d'arrêt: 5 min                │
│ ℹ Temps en-dessous du seuil (0,5-30)│
│                                     │
│ Activer alerte de durée: ☐          │
│ Durée d'alerte: 2 heures            │
│                                     │
│ Mode expert: ☐                      │
│                                     │
│           [  Suivant  ]             │
└─────────────────────────────────────┘
```

**Écran 3 : Notifications**
```
┌─────────────────────────────────────┐
│  Notifications                      │
├─────────────────────────────────────┤
│ Choisissez les services et          │
│ événements de notification.         │
│                                     │
│ Services de notification:           │
│ ☑ Application mobile                │
│ ☐ Telegram                          │
│ ☑ Notification persistante          │
│ ☐ Service personnalisé              │
│                                     │
│ Types de notifications:             │
│ ☑ Cycle démarré                     │
│ ☑ Cycle terminé                     │
│ ☑ Alerte de durée                   │
│ ☑ Débranché                         │
│                                     │
│           [  Valider  ]             │
└─────────────────────────────────────┘
```

**Écran 4 : Expert** (optionnel)
```
┌─────────────────────────────────────┐
│  ⚙️ Paramètres experts              │
├─────────────────────────────────────┤
│ Configuration avancée pour          │
│ utilisateurs expérimentés.          │
│                                     │
│ Délai débranché: 5 min              │
│ ℹ Durée à 0W avant détection        │
│   (1-60 min, défaut: 5 min)         │
│                                     │
│ Service personnalisé: _________     │
│ ℹ Nom complet (ex: notify.custom)   │
│                                     │
│           [  Suivant  ]             │
└─────────────────────────────────────┘
```

---

## ✅ Avantages pour l'utilisateur

1. **Clarté** : Chaque écran se concentre sur un aspect spécifique
2. **Simplicité** : Unités naturelles (min/h au lieu de secondes)
3. **Guidage** : Descriptions détaillées avec exemples concrets
4. **Flexibilité** : Mode expert optionnel pour ne pas surcharger
5. **Progression logique** : Navigation naturelle entre les étapes
6. **Sécurité** : Rétrocompatibilité totale avec les configs existantes

---

## 🚀 Tests recommandés

1. **Nouvelle configuration** : Créer un nouvel appareil et parcourir les 4 étapes
2. **Modification existante** : Éditer un appareil existant (vérifier conversion des unités)
3. **Mode expert** : Activer/désactiver le mode expert et vérifier le flux
4. **Sauvegarde** : Confirmer que les valeurs sont bien sauvegardées en secondes
5. **Traductions** : Tester en français et en anglais

---

## 📝 Notes de développement

- Les valeurs sont toujours stockées en **secondes** en interne pour la compatibilité
- La conversion se fait uniquement à l'**affichage** et à la **saisie**
- Le flag `expert_mode` n'est **pas persisté** dans la configuration finale
- Les `translation_key` sont utilisés pour les sélecteurs multi-choix
- La validation des ranges est maintenue pour éviter les valeurs incorrectes

---

## 🔍 Pour aller plus loin

### Améliorations futures possibles
- Ajouter des sliders visuels pour les seuils de puissance
- Prévisualisation des profils par type d'appareil
- Wizarding avec détection automatique des seuils optimaux
- Graphique de consommation en temps réel pendant la config
- Suggestions intelligentes basées sur l'historique

---

**Implémenté par :** Claude AI  
**Date :** 20 octobre 2025  
**Version :** 0.3.0 (proposition)

