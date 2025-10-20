# Guide de test - Configuration avancée améliorée

## 🧪 Tests à effectuer

### Test 1 : Nouvelle configuration
**Objectif** : Vérifier le flux complet pour un nouvel appareil

1. Aller dans Paramètres → Appareils et services
2. Trouver "Smart Appliance Monitor" 
3. Cliquer sur un appareil existant
4. Cliquer sur "CONFIGURER"

**Résultat attendu :**
- ✅ Écran 1 "Seuils de détection" s'affiche avec 2 champs seulement
- ✅ Descriptions claires avec exemples
- ✅ Valeurs pré-remplies selon le profil de l'appareil

---

### Test 2 : Navigation entre les étapes
**Objectif** : Vérifier le flux de navigation

1. Sur l'écran 1 (Seuils), modifier les valeurs
2. Cliquer sur "Soumettre"
3. Vérifier l'écran 2 (Délais) s'affiche
4. Noter les valeurs affichées (doivent être en minutes/heures)
5. Ne pas activer "Mode expert"
6. Cliquer sur "Soumettre"
7. Vérifier l'écran 3 (Notifications) s'affiche
8. Sélectionner des services et types
9. Cliquer sur "Soumettre"

**Résultat attendu :**
- ✅ Navigation fluide entre les 3 étapes (pas 4 car mode expert désactivé)
- ✅ Les valeurs de l'étape 1 sont conservées
- ✅ Délais affichés en minutes (ex: 2 au lieu de 120)
- ✅ Durée d'alerte affichée en heures (ex: 2 au lieu de 7200)
- ✅ Configuration sauvegardée à la fin

---

### Test 3 : Mode expert
**Objectif** : Vérifier l'accès aux paramètres avancés

1. Modifier la configuration d'un appareil
2. Aller jusqu'à l'écran 2 (Délais)
3. Cocher "Activer le mode expert"
4. Cliquer sur "Soumettre"

**Résultat attendu :**
- ✅ Écran 4 "Paramètres experts" s'affiche
- ✅ Champ "Délai débranché" en minutes (ex: 5)
- ✅ Champ "Service personnalisé" disponible
- ✅ Après soumission, passe à l'écran Notifications

---

### Test 4 : Conversion des unités
**Objectif** : Vérifier la rétrocompatibilité

1. Avant le test, noter les valeurs actuelles via Developer Tools → États
   - Chercher `start_delay`, `stop_delay`, `alert_duration` de votre appareil
   - Ces valeurs doivent être en secondes (ex: 120, 300, 7200)

2. Modifier la configuration de l'appareil

3. Vérifier l'écran 2 (Délais) :
   - `start_delay: 120s` → doit afficher `2` minutes
   - `stop_delay: 300s` → doit afficher `5` minutes
   - `alert_duration: 7200s` → doit afficher `2` heures

4. Modifier une valeur (ex: mettre 3 minutes pour start_delay)

5. Terminer la configuration

6. Vérifier via Developer Tools que la valeur est bien stockée en secondes :
   - `start_delay` doit maintenant être `180` (3 × 60)

**Résultat attendu :**
- ✅ Anciennes valeurs en secondes correctement converties à l'affichage
- ✅ Nouvelles valeurs correctement reconverties en secondes au stockage
- ✅ Aucune perte de précision

---

### Test 5 : Traductions françaises
**Objectif** : Vérifier l'interface en français

1. S'assurer que Home Assistant est en français (Profil → Langue)
2. Ouvrir la configuration d'un appareil

**Résultat attendu :**
- ✅ Écran 1 : "Seuils de détection"
- ✅ Écran 2 : "Délais de détection et alertes"
- ✅ Écran 3 : "Notifications"
- ✅ Écran 4 : "Paramètres experts"
- ✅ Descriptions en français claires et naturelles
- ✅ Exemples pertinents (ex: "four" au lieu de "oven")

---

### Test 6 : Validation des valeurs
**Objectif** : Vérifier les limites des champs

1. Modifier la configuration
2. Sur l'écran 2 (Délais), essayer des valeurs hors limites :
   - Délai de démarrage : essayer 0.1 min (trop petit) ou 15 min (trop grand)
   - Durée d'alerte : essayer 0.1 h (trop petit) ou 30 h (trop grand)

**Résultat attendu :**
- ✅ Erreur si valeur < minimum (0.5 min pour délais, 0.5h pour alerte)
- ✅ Erreur si valeur > maximum (10 min pour start, 30 min pour stop, 24h pour alerte)
- ✅ Message d'erreur clair

---

### Test 7 : Valeurs décimales
**Objectif** : Vérifier le support des fractions

1. Modifier la configuration
2. Sur l'écran 2, entrer :
   - Délai de démarrage : `1.5` minutes
   - Délai d'arrêt : `2.5` minutes
   - Durée d'alerte : `1.5` heures

3. Terminer la configuration

4. Vérifier dans Developer Tools :
   - `start_delay` doit être `90` secondes (1.5 × 60)
   - `stop_delay` doit être `150` secondes (2.5 × 60)
   - `alert_duration` doit être `5400` secondes (1.5 × 3600)

**Résultat attendu :**
- ✅ Valeurs décimales acceptées
- ✅ Conversion correcte avec décimales
- ✅ Précision conservée

---

### Test 8 : Annulation en cours de configuration
**Objectif** : Vérifier le comportement si on ferme pendant la config

1. Modifier la configuration
2. Sur l'écran 1, changer les seuils
3. Cliquer sur "Soumettre" pour aller à l'écran 2
4. Sur l'écran 2, fermer la fenêtre sans soumettre

5. Rouvrir la configuration

**Résultat attendu :**
- ✅ Les modifications de l'écran 1 ne sont PAS sauvegardées
- ✅ Les anciennes valeurs sont toujours présentes
- ✅ Pas d'état incohérent

---

## 🐛 Problèmes potentiels à surveiller

### Problème 1 : Valeurs non converties
**Symptôme** : Les délais s'affichent en secondes au lieu de minutes  
**Cause probable** : Division non appliquée dans `async_step_delays`  
**Vérification** : Ligne 277-285 de config_flow.py

### Problème 2 : Erreur de sauvegarde
**Symptôme** : Erreur lors de la validation finale  
**Cause probable** : Clés temporaires (`start_delay_minutes`) non converties  
**Vérification** : Lignes 250-258 de config_flow.py

### Problème 3 : Mode expert toujours actif
**Symptôme** : Écran expert s'affiche même si non coché  
**Cause probable** : `expert_mode` non nettoyé ou mal testé  
**Vérification** : Lignes 264-270 et 333 de config_flow.py

### Problème 4 : Traductions manquantes
**Symptôme** : Textes en anglais dans l'interface française  
**Cause probable** : Clés de traduction mal définies  
**Vérification** : Comparer strings.json et fr.json ligne par ligne

---

## ✅ Checklist de validation complète

Avant de considérer la feature comme prête :

- [ ] Test 1 : Nouvelle configuration ✓
- [ ] Test 2 : Navigation entre étapes ✓
- [ ] Test 3 : Mode expert activé ✓
- [ ] Test 4 : Conversion des unités ✓
- [ ] Test 5 : Interface française ✓
- [ ] Test 6 : Validation des limites ✓
- [ ] Test 7 : Valeurs décimales ✓
- [ ] Test 8 : Annulation ✓
- [ ] Aucune erreur dans les logs Home Assistant
- [ ] Aucune erreur de linter Python
- [ ] JSON valides (strings.json et fr.json)
- [ ] Documentation à jour (README.md si nécessaire)

---

## 🔧 Commandes utiles pour tester

```bash
# Redémarrer Home Assistant après modification
ha core restart

# Vérifier les logs en temps réel
tail -f /config/home-assistant.log | grep smart_appliance

# Valider la syntaxe Python
python3 -m py_compile /config/custom_components/smart_appliance_monitor/config_flow.py

# Valider les JSON
python3 -m json.tool /config/custom_components/smart_appliance_monitor/strings.json
python3 -m json.tool /config/custom_components/smart_appliance_monitor/translations/fr.json

# Voir la configuration stockée d'un appareil
# Aller dans Developer Tools → États
# Chercher : binary_sensor.XXX_running (remplacer XXX par nom appareil)
# Cliquer sur l'entité → Attributs → config
```

---

## 📸 Captures d'écran recommandées

Pour documentation :
1. Écran 1 - Seuils (montrer exemples dans descriptions)
2. Écran 2 - Délais avec toggle mode expert
3. Écran 3 - Notifications avec multi-select
4. Écran 4 - Paramètres experts (si activé)
5. Vue avant/après dans Developer Tools (valeurs en secondes vs affichage)

---

**Bonne chance pour les tests ! 🚀**

