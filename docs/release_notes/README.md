# Release Notes - Smart Appliance Monitor

Ce dossier contient les notes de version détaillées pour chaque release de Smart Appliance Monitor.

## 📋 Index des Versions

### Version 0.8.x - Cycle History System 📊

- **[v0.8.1](RELEASE_NOTES_v0.8.1.md)** - 22 octobre 2025 - Documentation Update 📚
  - **CORRECTIONS** : Audit complet de la documentation
  - Correction des versions obsolètes dans wiki et README
  - Correction du comptage d'entités (32→33)
  - Nouvelle page wiki Cycle-History.md (540+ lignes)
  - Documentation complète des services v0.8.0
  - Mise à jour de tous les liens et références

- **[v0.8.0](RELEASE_NOTES_v0.8.0.md)** - 22 octobre 2025 - Cycle History System 🎉
  - **NOUVELLE FONCTIONNALITÉ** : Système d'historique persistant des cycles
  - Service `get_cycle_history` pour requêtes avec filtres avancés
  - Service `import_historical_cycles` pour reconstruction de cycles passés
  - Stockage hybride : 30 cycles en mémoire + illimité dans Recorder
  - Enregistrement automatique dans la base de données HA
  - Support mode `replace_existing` pour nettoyage et réimport
  - Requêtes SQL optimisées pour Recorder moderne
  - Documentation complète avec exemples et avertissements

### Version 0.7.x - AI Analysis 🤖

- **[v0.7.4](RELEASE_NOTES_v0.7.4.md)** - 21 octobre 2025 - Negative Energy Values Fix 🚨
  - **CRITIQUE** : Correction des valeurs d'énergie négatives (-4551 kWh → 0 kWh)
  - Cause : Reset des capteurs ESPHome créant des énergies de cycle négatives
  - Validation multi-niveaux pour détecter et ignorer les énergies négatives
  - Auto-récupération des statistiques corrompues au redémarrage
  - Logging détaillé pour le debugging des problèmes de données
  - Analyse IA maintenant fonctionnelle avec données valides

- **[v0.7.3](RELEASE_NOTES_v0.7.3.md)** - 21 octobre 2025 - AI Analysis Bug Fixes 🐛
  - **CRITIQUE** : Correction du parsing des réponses IA (recommendations et insights vides)
  - Passage de JSON strict à parsing Markdown
  - Correction du matching coordinator pour noms d'appareils avec underscores
  - Amélioration des prompts IA avec structure Markdown explicite
  - Ajout de logs debug détaillés pour le suivi des réponses IA
  - Correction clé de réponse : `response["text"]` → `response["data"]`

- **[v0.7.2](RELEASE_NOTES_v0.7.2.md)** - 21 octobre 2025 - Bug Fixes & Documentation 🐛
  - **CRITIQUE** : Correction du bug d'enregistrement des services AI
  - Tous les 13 services maintenant disponibles après mise à jour
  - Documentation wiki complète pour les fonctionnalités AI (500+ lignes)
  - Sidebar wiki mise à jour avec section "Energy & AI"
  - Liens wiki vérifiés et corrigés
  - Guide de migration depuis v0.6.0, v0.7.0, et v0.7.1

- **[v0.7.1](RELEASE_NOTES_v0.7.1.md)** - 21 octobre 2025 - Historical Release Notes Recovery 📚
  - Récupération de toutes les release notes historiques (v0.2.0 à v0.5.0)
  - Système de documentation permanent établi
  - Organisation complète des releases passées
  - Workflow de release mis à jour

- **[v0.7.0](RELEASE_NOTES_v0.7.0.md)** - 21 octobre 2025 - AI-Powered Cycle Analysis 🤖
  - Analyse IA des cycles d'appareils via Home Assistant AI Tasks
  - Support OpenAI, Claude, Ollama, et autres providers IA
  - Trois types d'analyse : Pattern, Comparative, Recommendations
  - Analyse globale du tableau de bord énergétique
  - Nouveaux services : `configure_ai`, `analyze_cycles`, `analyze_energy_dashboard`
  - Nouveaux capteurs et switches d'analyse IA
  - Guide de test complet (TESTING_AI.md)
  - Documentation bilingue (EN/FR)

### Version 0.6.x - Energy Dashboard Integration ⚡

- **[v0.6.0](RELEASE_NOTES_v0.6.0.md)** - 21 octobre 2025 - Energy Dashboard Integration Suite
  - Lecteur de fichier `.storage/energy` (read-only)
  - Synchronisation automatique avec Energy Dashboard
  - Services de sync et export de configuration
  - Custom Energy Dashboard avec analytics avancées
  - Comparaisons multi-périodes
  - Template de dashboard personnalisé

### Version 0.5.x - Advanced Features & Fixes ⚡

- **[v0.5.7](RELEASE_NOTES_v0.5.7.md)** - 21 octobre 2025 - Documentation & Roadmap 📚
  - Nouveau fichier IDEAS.md centralisé (297 lignes)
  - 3 nouvelles idées majeures ajoutées
  - Release notes organisées dans dossier dédié
  - Documentation épurée et professionnelle

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

- **[v0.5.0](RELEASE_NOTES_v0.5.0.md)** - 21 octobre 2025 - Advanced Features Release 🚀
  - Auto-shutdown automatique après cycles
  - Energy Management avec limites et budget
  - Usage Scheduling (heures autorisées, jours bloqués)
  - Anomaly Detection intelligente
  - Data Export (CSV/JSON)
  - Energy Dashboard Integration
  - 10 nouvelles entités par appareil (30 total)

### Version 0.4.x - Configuration UX Improvements 🎨

- **[v0.4.1](RELEASE_NOTES_v0.4.1.md)** - 20 octobre 2025 - Bundled Dashboard Templates
  - Templates inclus directement dans l'intégration
  - 7 templates pour chaque type d'appareil
  - Résolution automatique et génération immédiate
  - Customization facile

- **[v0.4.0](RELEASE_NOTES_v0.4.0.md)** - 20 octobre 2025 - Enhanced Configuration UX
  - Configuration multi-étapes (4 étapes)
  - Unités naturelles (minutes/heures au lieu de secondes)
  - Mode Expert pour options avancées
  - Descriptions améliorées et aide contextuelle

### Version 0.3.x - Dashboard System 📊

- **[v0.3.0](RELEASE_NOTES_v0.3.0.md)** - 20 octobre 2025 - Dashboard Templates
  - Système de templates dashboard complet
  - 7 templates pré-configurés par type d'appareil
  - Service `generate_dashboard_yaml` automatique
  - Support Mushroom Cards et Mini Graph Card
  - 6 sections par dashboard (status, cycle, power, controls, stats, alerts)

### Version 0.2.x - Initial Release 🎉

- **[v0.2.0](RELEASE_NOTES_v0.2.0.md)** - 20 octobre 2025 - Initial Public Release
  - Première release publique
  - Détection automatique de cycles
  - 14 entités par appareil
  - Configuration Flow UI complète
  - Système de notifications (Telegram, Mobile App, Persistent)
  - Support multi-langue (EN/FR)

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

**Dernière version** : v0.8.1  
**Date** : 22 octobre 2025

