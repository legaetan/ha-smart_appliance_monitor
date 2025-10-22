# Smart Appliance Monitor v0.5.6 - French Language Support 🇫🇷

## 🌍 Nouveau : Support Bilingue pour les Cartes Custom

Cette release ajoute le **support complet du français** pour les cartes Lovelace custom ! Les cartes fonctionnent maintenant automatiquement avec les noms d'entités français et anglais.

## ✅ Ce qui a été ajouté

### Support Bilingue Automatique
- **Détection automatique de la langue** - Les cartes détectent si vous utilisez des entités françaises ou anglaises
- **Support du suffixe `_etat`** (français) en plus de `_state` (anglais)
- **Mapping automatique de toutes les entités** :
  - `duree_du_cycle` ↔ `cycle_duration`
  - `energie_du_cycle` ↔ `cycle_energy`
  - `cout_du_cycle` ↔ `cycle_cost`
  - `en_marche` ↔ `running`
  - `debranche` ↔ `unplugged`
  - `surveillance` ↔ `monitoring`
  - Et toutes les autres traductions
- **Aucune configuration nécessaire** - Tout fonctionne automatiquement !

## 🐛 Problème Résolu

### Avant v0.5.6
Les cartes affichaient "Entity not found" avec des entités françaises comme `sensor.lave_linge_etat`

### Après v0.5.6 ✅
Les cartes fonctionnent parfaitement avec :
- ✅ `sensor.lave_linge_etat` (français)
- ✅ `sensor.washing_machine_state` (anglais)

## 🚀 Comment Mettre à Jour

### Via HACS
1. Ouvrez **HACS** → **Intégrations**
2. Trouvez **Smart Appliance Monitor**
3. Cliquez sur **Update** pour installer v0.5.6
4. **Redémarrez Home Assistant**
5. **Videz le cache du navigateur** (Ctrl+Shift+R)

### Résultat
Les cartes custom fonctionneront immédiatement avec vos entités françaises !

## 📊 Exemple d'Utilisation

```yaml
# Fonctionne avec des entités françaises !
type: custom:smart-appliance-cycle-card
entity: sensor.lave_linge_etat

type: custom:smart-appliance-stats-card
entity: sensor.lave_vaisselle_etat
```

## 🔧 Détails Techniques

**Fichiers Modifiés:**
- `www/smart-appliance-cards/src/utils/helpers.js` - Mapping bilingue des entités
- `www/smart-appliance-cards/dist/*` - Cartes recompilées

**Rétrocompatibilité:** ✅ 100% compatible avec les installations anglaises existantes

**Changements Cassants:** ❌ Aucun

## 📝 Changelog Complet

Voir [CHANGELOG.md](CHANGELOG.md) pour tous les détails.

---

**Version**: 0.5.6  
**Date**: 21 octobre 2025  
**Téléchargement**: [smart_appliance_monitor-v0.5.6.zip](https://github.com/legaetan/ha-smart_appliance_monitor/releases/download/v0.5.6/smart_appliance_monitor-v0.5.6.zip)

