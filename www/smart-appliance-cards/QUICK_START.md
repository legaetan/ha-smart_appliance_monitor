# 🚀 Quick Start - Smart Appliance Cards

## Installation Rapide

### 1. Build

```bash
cd /workspace/www/smart-appliance-cards
npm install
npm run build
```

### 2. Copier vers Home Assistant

```bash
# Copier le dossier dist vers Home Assistant
cp -r dist /path/to/homeassistant/config/www/smart-appliance-cards/
```

### 3. Ajouter Resources dans HA

Settings → Dashboards → Resources → Add Resource

**Resource 1**:
- URL: `/local/smart-appliance-cards/dist/smart-appliance-cycle-card.js`
- Type: JavaScript Module

**Resource 2**:
- URL: `/local/smart-appliance-cards/dist/smart-appliance-stats-card.js`
- Type: JavaScript Module

### 4. Redémarrer HA et vider cache

- Redémarrer Home Assistant
- Vider cache navigateur (Ctrl+Shift+R)

---

## Utilisation Rapide

### Ajouter une carte

Dans un dashboard:
1. Edit Dashboard
2. Add Card
3. Chercher "Smart Appliance"

### Configuration minimale

```yaml
type: custom:smart-appliance-cycle-card
entity: sensor.washing_machine_state
```

```yaml
type: custom:smart-appliance-stats-card
entity: sensor.washing_machine_state
```

---

## Documentation Complète

- **README.md** - Guide utilisateur complet
- **BUILD_INSTRUCTIONS.md** - Instructions détaillées
- **DEVELOPMENT_SUMMARY.md** - Détails techniques
- **examples/** - Exemples de configuration

---

**Version**: 0.4.0  
**Date**: 20 octobre 2025  
**Statut**: ✅ Prêt à l'emploi
