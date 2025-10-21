# Release Notes - Smart Appliance Monitor

Ce dossier contient les notes de version détaillées pour chaque release de Smart Appliance Monitor.

## 📋 Index des Versions

### Version 0.5.x - Features Avancées & Corrections

- **[v0.5.6](RELEASE_NOTES_v0.5.6.md)** - 21 octobre 2025 - Support Bilingue (Français) 🇫🇷
  - Support français/anglais pour les custom cards
  - Détection automatique de la langue
  - Mapping bilingue des entités

- **[v0.5.5](RELEASE_NOTES_v0.5.5.md)** - 21 octobre 2025 - Corrections Critiques
  - Correction API StaticPathConfig
  - Ajout méthode `set_enabled()` manquante
  - Restauration d'état fonctionnelle

- **[v0.5.4](RELEASE_NOTES_v0.5.4.md)** - 21 octobre 2025 - Correction API
  - Migration vers `async_register_static_paths`
  - Correction compatibilité Home Assistant

- **[v0.5.3](RELEASE_NOTES_v0.5.3.md)** - 21 octobre 2025 - Installation Automatique
  - Cartes custom automatiquement installées via HACS
  - Enregistrement automatique des ressources frontend
  - Intégration HACS complète

- **[v0.5.2](RELEASE_NOTES_v0.5.2.md)** - 21 octobre 2025 - Frontend Resources
  - Première tentative d'installation automatique des cartes
  - Améliorations de la documentation

- **[v0.5.1](RELEASE_NOTES_v0.5.1.md)** - 20 octobre 2025 - State Persistence
  - Persistance des cycles et statistiques
  - Restauration automatique après redémarrage HA
  - Validation intelligente des données

### Version 0.5.0 - Advanced Features (20 octobre 2025)

Voir [CHANGELOG.md](../../CHANGELOG.md) pour la version complète 0.5.0 incluant :
- Energy Dashboard integration
- Data export (CSV/JSON)
- Auto-shutdown
- Energy Management
- Usage Scheduling
- Anomaly Detection

### Versions Antérieures

Pour les versions 0.1.0 à 0.4.x, consultez le [CHANGELOG.md](../../CHANGELOG.md) complet.

---

## 📚 Ressources Associées

- **CHANGELOG** : [CHANGELOG.md](../../CHANGELOG.md) - Historique complet des versions
- **IDEAS** : [IDEAS.md](../IDEAS.md) - Fonctionnalités futures et roadmap
- **GitHub Releases** : [Releases](https://github.com/legaetan/ha-smart_appliance_monitor/releases)

---

## 🔖 Convention de Versioning

Ce projet suit le [Semantic Versioning](https://semver.org/):
- **MAJOR** (x.0.0) - Breaking changes
- **MINOR** (0.x.0) - New features (backward compatible)
- **PATCH** (0.0.x) - Bug fixes (backward compatible)

---

**Dernière version** : v0.5.6  
**Date** : 21 octobre 2025

