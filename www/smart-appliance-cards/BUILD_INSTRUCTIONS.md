# Instructions de Build - Smart Appliance Cards

## 🎯 Objectif

Ce document explique comment compiler les cartes pour la production et les installer dans Home Assistant.

## 📋 Prérequis

- Node.js v16+ et npm installés
- Accès au serveur Home Assistant
- Droits d'écriture dans `/config/www/`

## 🔨 Étapes de Build

### 1. Installation des Dépendances

```bash
cd /workspace/www/smart-appliance-cards
npm install
```

**Attendu**: Installation de toutes les dépendances (lit, rollup, babel, etc.)

### 2. Build de Production

```bash
npm run build
```

**Résultat**: Création des fichiers compilés dans `dist/`:
- `dist/smart-appliance-cycle-card.js` (~50KB minifié)
- `dist/smart-appliance-stats-card.js` (~50KB minifié)

### 3. Vérification du Build

Vérifier que les fichiers existent:
```bash
ls -lh dist/
```

Devrait afficher:
```
smart-appliance-cycle-card.js
smart-appliance-stats-card.js
```

### 4. Test de Syntaxe (Optionnel)

```bash
npm run lint
```

Corrige automatiquement les erreurs:
```bash
npm run format
```

## 📦 Installation dans Home Assistant

### Option A: Installation Locale (Développement)

Si Home Assistant est sur la même machine:

```bash
# Créer le dossier de destination
mkdir -p /path/to/homeassistant/config/www/smart-appliance-cards/dist

# Copier les fichiers compilés
cp dist/*.js /path/to/homeassistant/config/www/smart-appliance-cards/dist/

# Copier aussi les exemples (optionnel)
cp -r examples /path/to/homeassistant/config/www/smart-appliance-cards/
```

### Option B: Installation Distante (Serveur)

Si Home Assistant est sur un serveur distant:

```bash
# Via SCP
scp -r dist/*.js user@homeassistant:/config/www/smart-appliance-cards/dist/

# Via SFTP
sftp user@homeassistant
> cd /config/www
> mkdir smart-appliance-cards
> cd smart-appliance-cards
> mkdir dist
> cd dist
> put dist/*.js
> bye
```

### Option C: Via Samba/SMB (Plus Simple)

1. Ouvrir le partage réseau Home Assistant
2. Naviguer vers `config/www/`
3. Créer le dossier `smart-appliance-cards/dist/`
4. Copier manuellement les fichiers `.js`

## 🔧 Configuration dans Home Assistant

### 1. Ajouter les Resources

Dans Home Assistant:

1. **Settings** → **Dashboards**
2. Menu **⋮** → **Resources**
3. Clic **+ Add Resource**

**Première Resource - Cycle Card**:
- URL: `/local/smart-appliance-cards/dist/smart-appliance-cycle-card.js`
- Resource type: **JavaScript Module**

**Deuxième Resource - Stats Card**:
- URL: `/local/smart-appliance-cards/dist/smart-appliance-stats-card.js`
- Resource type: **JavaScript Module**

### 2. Redémarrer Home Assistant

**Important**: Redémarrer HA après avoir ajouté les resources.

```bash
# Via interface
Settings → System → Restart

# Ou via CLI
ha core restart
```

### 3. Vider le Cache du Navigateur

Sur chaque navigateur/appareil:
- **Windows/Linux**: Ctrl + Shift + R
- **Mac**: Cmd + Shift + R
- **Mobile**: Vider le cache de l'app Companion

## ✅ Vérification de l'Installation

### Test 1: Console JavaScript

Ouvrir la console (F12) dans le navigateur et vérifier:

```javascript
// Devrait afficher les infos de version
// "SMART-APPLIANCE-CYCLE-CARD v0.4.0"
// "SMART-APPLIANCE-STATS-CARD v0.4.0"
```

### Test 2: Ajouter une Carte

1. Aller sur un dashboard
2. Clic **Edit Dashboard**
3. Clic **+ Add Card**
4. Chercher "Smart Appliance"

**Attendu**: Voir apparaître:
- Smart Appliance Cycle Card
- Smart Appliance Stats Card

### Test 3: Configuration Basique

Ajouter une carte avec config minimale:

```yaml
type: custom:smart-appliance-cycle-card
entity: sensor.washing_machine_state
```

**Attendu**: La carte s'affiche sans erreur

## 🐛 Dépannage

### Erreur: "Custom element doesn't exist"

**Cause**: Resources pas chargées

**Solution**:
1. Vérifier l'URL dans Resources
2. Vérifier que les fichiers existent
3. Redémarrer HA
4. Vider cache navigateur

### Erreur: "Entity not found"

**Cause**: Entity ID incorrect

**Solution**:
1. Vérifier dans Developer Tools → States
2. L'entity doit être `sensor.xxx_state`
3. Smart Appliance Monitor doit être installé

### Carte Vide ou Erreur de Rendu

**Cause**: Erreur JavaScript

**Solution**:
1. Ouvrir console navigateur (F12)
2. Regarder les erreurs en rouge
3. Vérifier la version de lit (doit être 3.x)

### Styles Incorrects

**Cause**: Thème HA non chargé

**Solution**:
1. Vérifier que le thème HA est actif
2. Essayer theme: 'light' ou 'dark' dans la config
3. Vider cache navigateur

## 🚀 Mode Développement

Pour développer et tester en temps réel:

### 1. Mode Watch

```bash
npm run watch
```

Laisse le terminal ouvert. Les fichiers sont recompilés automatiquement à chaque modification.

### 2. Lien Symbolique (Linux/Mac)

Au lieu de copier, créer un lien:

```bash
ln -s /workspace/www/smart-appliance-cards/dist /path/to/homeassistant/config/www/smart-appliance-cards/dist
```

**Avantage**: Les modifications sont immédiatement disponibles après rebuild.

### 3. Cycle de Développement

1. Modifier le code dans `src/`
2. Le build watch recompile automatiquement
3. Rafraîchir le navigateur (Ctrl+Shift+R)
4. Tester les changements

## 📊 Structure des Fichiers Compilés

```
dist/
├── smart-appliance-cycle-card.js      # Carte cycle compilée + minifiée
└── smart-appliance-stats-card.js      # Carte stats compilée + minifiée
```

Chaque fichier contient:
- Le code de la carte principale
- L'éditeur de configuration
- Tous les utilitaires (helpers, formatters, constants)
- Les styles CSS
- Dépendance lit-element embarquée

**Taille**: ~40-60 KB par fichier (minifié)

## 🔍 Vérification de la Qualité

### Vérifier la Minification

```bash
# Les fichiers doivent être compacts (pas de commentaires, code minifié)
head -n 5 dist/smart-appliance-cycle-card.js
```

### Vérifier les Imports

```bash
# Tous les imports doivent être résolus (pas de chemins relatifs)
grep "import.*from" dist/*.js
```

**Attendu**: Aucun résultat (les imports sont bundlés)

## 📝 Checklist Avant Release

- [ ] `npm install` exécuté sans erreur
- [ ] `npm run build` exécuté avec succès
- [ ] Fichiers `dist/*.js` créés
- [ ] Taille des fichiers < 100KB chacun
- [ ] Aucune erreur de lint
- [ ] Tests manuels dans HA réussis
- [ ] Documentation à jour
- [ ] Exemples YAML testés

## 🎉 Prochaines Étapes

Une fois le build vérifié:

1. **Tester** toutes les fonctionnalités
2. **Corriger** les bugs éventuels
3. **Optimiser** si nécessaire
4. **Documenter** les problèmes connus
5. **Préparer** la release v0.4.0

## 💡 Conseils

### Performance

- Les cartes utilisent un update interval de 1s (running) ou 30s (idle)
- Limiter le nombre de cartes par dashboard (max 10)
- Utiliser le mode compact sur mobile

### Compatibilité

- Home Assistant 2024.1+
- Navigateurs modernes (Chrome 90+, Firefox 88+, Safari 14+)
- Mobile: iOS 14+, Android 10+

### Personnalisation

- Tous les thèmes HA sont supportés
- Les CSS Variables peuvent être overridées
- Voir `src/styles/common-styles.js` pour les variables

---

**Dernière mise à jour**: 20 octobre 2025  
**Version**: 0.4.0  
**Auteur**: Smart Appliance Monitor Team
