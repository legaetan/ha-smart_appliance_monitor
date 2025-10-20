# Guide de Reconfiguration - Smart Appliance Monitor

## 🔧 Nouvelle Fonctionnalité : Reconfigurer sans perdre les données

Vous pouvez maintenant **modifier tous les paramètres** de votre intégration Smart Appliance Monitor sans avoir à la supprimer et la recréer. Les statistiques sont conservées ! 🎉

## 📍 Comment accéder à la reconfiguration ?

### Étape 1 : Aller dans les paramètres de l'intégration

1. Allez dans **Paramètres** → **Appareils & Services**
2. Cliquez sur **Smart Appliance Monitor**
3. Cliquez sur votre appareil (ex: "Chauffe-Eau")
4. Vous verrez maintenant un bouton **"Reconfigurer"**

![Bouton Reconfigurer](https://via.placeholder.com/600x100?text=Bouton+Reconfigurer)

### Étape 2 : Modifier les paramètres

Vous pouvez maintenant modifier :

| Paramètre | Description | Exemple d'utilisation |
|-----------|-------------|----------------------|
| **Nom de l'appareil** | Renommer votre appareil | "Chauffe-Eau" → "Ballon d'eau chaude" |
| **Type d'appareil** | Changer le type | "Other" → "Water Heater" (applique les bons seuils) |
| **Capteur de puissance** | Changer le capteur | Si vous avez changé de prise connectée |
| **Capteur d'énergie** | Changer le capteur | Si vous avez changé de prise connectée |
| **Entité du prix** | Ajouter/modifier une entité | Passer d'un prix fixe à dynamique |
| **Prix du kWh** | Modifier le prix fixe | Mettre à jour le tarif |

### Étape 3 : Valider

1. Cliquez sur **"Valider"**
2. L'intégration se recharge automatiquement
3. **Tous vos historiques et statistiques sont conservés** ✅

---

## 🎯 Cas d'usage pratiques

### 1. Changer le type d'appareil pour optimiser les seuils

**Problème** : Vous aviez configuré votre chauffe-eau comme "Autre" avec les seuils par défaut (50W), mais il déclenche à 1500W.

**Solution** :
1. Reconfigurer l'appareil
2. Changer le type vers **"Chauffe-eau"**
3. Les seuils passent automatiquement à **1000W de démarrage**
4. Les statistiques précédentes sont conservées

---

### 2. Passer d'un prix fixe à un prix dynamique

**Problème** : Vous avez configuré un prix fixe de 0.2516 €/kWh, mais vous voulez maintenant utiliser une entité `input_number` pour les heures creuses/pleines.

**Solution** :
1. Créez votre `input_number.electricity_price` dans Home Assistant
2. Reconfigurer l'intégration
3. Sélectionnez l'entité dans **"Entité du prix"**
4. Les futurs coûts seront calculés avec le prix dynamique

---

### 3. Changer de prise connectée

**Problème** : Votre prise Sonoff a lâché, vous l'avez remplacée par une Shelly. Les entités ont changé.

**Solution** :
1. Reconfigurer l'appareil
2. Sélectionnez les nouveaux capteurs :
   - `sensor.shelly_power` au lieu de `sensor.sonoff_power`
   - `sensor.shelly_energy` au lieu de `sensor.sonoff_energy`
3. La surveillance reprend avec les nouveaux capteurs

---

### 4. Renommer un appareil

**Problème** : Vous avez nommé votre appareil "Four" mais vous voulez être plus précis.

**Solution** :
1. Reconfigurer
2. Renommer : "Four" → "Four Encastrable Cuisine"
3. Le titre de l'intégration et toutes les entités sont mis à jour

---

## ⚙️ Différence entre Reconfiguration et Configuration Avancée

| Fonction | Reconfiguration | Configuration Avancée |
|----------|----------------|----------------------|
| **Accès** | Bouton "Reconfigurer" | Bouton "Configurer" |
| **Nom de l'appareil** | ✅ Oui | ❌ Non |
| **Type d'appareil** | ✅ Oui | ❌ Non |
| **Capteurs** | ✅ Oui | ❌ Non |
| **Entité du prix** | ✅ Oui | ❌ Non |
| **Prix fixe** | ✅ Oui | ❌ Non |
| **Seuils (W)** | ❌ Non* | ✅ Oui |
| **Délais (s)** | ❌ Non* | ✅ Oui |
| **Alertes** | ❌ Non* | ✅ Oui |

*Si vous changez le type d'appareil, les seuils se réadaptent automatiquement dans la Configuration Avancée.

---

## 💡 Conseils

### Quand utiliser la reconfiguration ?

✅ **Utilisez la reconfiguration pour :**
- Changer le type d'appareil
- Passer au prix dynamique
- Remplacer une prise défectueuse
- Corriger une erreur de configuration initiale

❌ **N'utilisez PAS la reconfiguration pour :**
- Ajuster les seuils de puissance → Utilisez "Configuration Avancée"
- Modifier les délais → Utilisez "Configuration Avancée"
- Activer/désactiver les alertes → Utilisez "Configuration Avancée"

### Les statistiques sont-elles vraiment conservées ?

**OUI !** La reconfiguration ne touche **QUE** aux paramètres de base (data). Les statistiques sont stockées séparément :

- ✅ Dernier cycle conservé
- ✅ Nombre de cycles du jour conservé
- ✅ Coûts journaliers/mensuels conservés
- ✅ Historique dans le coordinateur conservé

**Seule exception** : Si vous changez le `entry_id` (en supprimant/recréant), vous perdez tout.

---

## 🔍 Que se passe-t-il en coulisses ?

1. **Validation** : Les nouveaux capteurs sont vérifiés
2. **Mise à jour** : Les données de configuration (`entry.data`) sont mises à jour
3. **Rechargement** : L'intégration est rechargée avec `async_reload()`
4. **Confirmation** : Message "Reconfiguration réussie !"

Le `coordinator` est recréé avec les nouveaux paramètres, mais récupère les statistiques existantes.

---

## 🐛 Dépannage

### Le bouton "Reconfigurer" n'apparaît pas

**Cause** : Votre version de Home Assistant est trop ancienne.

**Solution** : Mettez à jour Home Assistant vers une version ≥ 2023.4

### Les seuils ne s'adaptent pas automatiquement

**Comportement normal** : Les seuils de la Configuration Avancée ne sont pas modifiés automatiquement pour éviter de perdre vos ajustements personnalisés.

**Solution** :
1. Notez que les nouveaux profils sont disponibles
2. Allez dans "Configuration Avancée"
3. Les valeurs par défaut affichées correspondent au nouveau type
4. Ajustez manuellement si nécessaire

### L'intégration ne se recharge pas

**Cause** : Erreur dans la configuration des capteurs.

**Solution** :
1. Vérifiez que les entités existent : `sensor.xxx_power` et `sensor.xxx_energy`
2. Consultez les logs : **Paramètres** → **Système** → **Logs**
3. Cherchez `smart_appliance_monitor`

---

## 📚 En savoir plus

- [Guide d'installation](README.md)
- [Configuration avancée](IMPLEMENTATION_SUMMARY.md)
- [Améliorations récentes](IMPROVEMENTS.md)

---

**Profitez de cette nouvelle flexibilité pour optimiser votre surveillance sans perdre vos données !** 🚀

