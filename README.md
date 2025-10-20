# 🏠 Smart Appliance Monitor

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![GitHub Release](https://img.shields.io/github/release/yourusername/ha-smart_appliance_monitor.svg)](https://github.com/yourusername/ha-smart_appliance_monitor/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **✅ MVP Implémenté** - Le MVP est fonctionnel avec toutes les fonctionnalités de base !

## 🎯 Vision

Une intégration HACS complète qui transforme n'importe quelle prise connectée en système de surveillance intelligent d'appareil électroménager.

## ✨ Fonctionnalités Implémentées

### ✅ Disponible maintenant (v0.1.0)

- 🔌 **Surveillance automatique** - Détection des cycles de démarrage/arrêt avec seuils configurables
- 📊 **Statistiques complètes** - Durée, consommation, coût par cycle + historiques
- 🎛️ **Seuils optimisés par appareil** - Profils pré-configurés pour chaque type d'appareil
- 💰 **Prix dynamique** - Support des entités pour tarifs variables (HC/HP, Tempo)
- 🔧 **Reconfiguration flexible** - Modifier tous les paramètres sans perdre les statistiques
- 🔔 **Notifications intelligentes** - Alertes de début/fin de cycle et durée excessive
- 🌍 **Multi-langue** - Interface complète en français et anglais
- 🧪 **Tests unitaires** - Couverture complète du code

### 🚧 À venir

- 🤖 **Machine Learning** - Calibration automatique des seuils (Phase 2)
- 📈 **Dashboard intégré** - Interface générée automatiquement (Phase 2)
- 📉 **Graphiques** - Visualisations avancées dans les notifications (Phase 2)

## 🚀 Installation

### HACS (Recommandé - À venir)

1. Ouvrez HACS dans Home Assistant
2. Allez dans "Intégrations"
3. Cliquez sur "Explorer & télécharger des dépôts"
4. Recherchez "Smart Appliance Monitor"
5. Cliquez sur "Télécharger"
6. Redémarrez Home Assistant

### Installation Manuelle (Développement)

1. Clonez ce dépôt dans votre dossier `custom_components` :
```bash
cd /config/custom_components
git clone https://github.com/yourusername/ha-smart_appliance_monitor.git smart_appliance_monitor
```

2. Redémarrez Home Assistant

3. Ajoutez l'intégration via l'interface :
   - Paramètres → Appareils et services → Ajouter une intégration
   - Recherchez "Smart Appliance Monitor"

## 📱 Appareils Supportés

L'intégration peut surveiller tout appareil électroménager connecté via une prise intelligente avec capteur de puissance :

- 🔥 Four électrique
- 🍽️ Lave-vaisselle
- 🧺 Lave-linge
- 👕 Sèche-linge
- 💧 Chauffe-eau
- ☕ Machine à café
- 🍞 Grille-pain
- Et bien plus !

## 📚 Documentation

### Guides Utilisateur
- **[Guide de Reconfiguration](RECONFIGURE_GUIDE.md)** - Comment modifier les paramètres sans perdre les données
- **[Améliorations Récentes](IMPROVEMENTS.md)** - Prix dynamique et seuils adaptés

### Documentation Développeur
- **[Résumé d'implémentation](IMPLEMENTATION_SUMMARY.md)** - Architecture du MVP
- **[Guide de développement](DEVELOPMENT.md)** - Contribuer au projet
- **[Fichiers créés](FILES_CREATED.md)** - Liste complète des composants

### Documentation Complète
- **[Concept complet](CONCEPT_INTEGRATION_HACS.md)** - Vision et fonctionnalités détaillées
- **[Spécifications techniques](SPECS_TECHNIQUES_INTEGRATION.md)** - Architecture et code
- **[Ressources développement](RESSOURCES_DEVELOPPEMENT.md)** - Guide pour contribuer
- **[Index complet](INDEX_COMPLET.md)** - Navigation dans la documentation

## 🛠️ État du Projet

### Phase Actuelle : MVP Complet ✅

- [x] Concept et spécifications
- [x] Documentation complète
- [x] Structure du projet
- [x] Intégration de base avec coordinator
- [x] Config flow (création + reconfiguration)
- [x] State Machine pour détection de cycles
- [x] Entités complètes :
  - [x] Binary Sensors (running, alert_duration)
  - [x] Sensors (state, cycle_*, last_cycle_*, daily_*, monthly_cost)
  - [x] Buttons (reset_stats)
  - [x] Switches (monitoring, notifications)
- [x] Services personnalisés
- [x] Système de notifications
- [x] Tests unitaires complets
- [x] Prix dynamique via entité
- [x] Seuils optimisés par type d'appareil
- [x] Flux de reconfiguration
- [ ] Publication HACS
- [ ] Mode apprentissage ML
- [ ] Dashboard automatique

### Roadmap

#### ✅ v0.1.0 - MVP (Octobre 2025)
- ✅ Configuration via UI avec sélecteurs intelligents
- ✅ Détection cycle démarrage/arrêt avec machine à états
- ✅ 10 capteurs (état, cycle en cours, dernier cycle, statistiques)
- ✅ Notifications avec détails du cycle
- ✅ Services personnalisés (start_cycle, stop_monitoring, reset_stats)
- ✅ Prix dynamique via entité input_number/sensor
- ✅ Seuils adaptés par type d'appareil (7 profils)
- ✅ Flux de reconfiguration sans perte de données

#### 🚧 v0.2.0 - Améliorations (Prévu : Q1 2026)
- [ ] Publication sur HACS
- [ ] Intégration Energy Dashboard
- [ ] Support des automations avancées
- [ ] Export des données (CSV, JSON)
- [ ] Graphiques dans les notifications

#### 🔮 v0.5.0 - Machine Learning (Prévu : Q2 2026)
- [ ] Mode apprentissage automatique
- [ ] Détection intelligente des cycles
- [ ] Ajustement automatique des seuils
- [ ] Prédictions de durée/consommation

#### 🎯 v1.0.0 - Version production (Prévu : Q3 2026)
- [ ] Dashboard intégré automatique
- [ ] ML complet pour tous types d'appareils
- [ ] Multi-appareil avec groupes
- [ ] API complète pour intégrations tierces

## 🤝 Contribution

Les contributions sont les bienvenues ! Consultez le fichier [RESSOURCES_DEVELOPPEMENT.md](RESSOURCES_DEVELOPPEMENT.md) pour commencer.

### Environnement de Développement

```bash
# Cloner le dépôt
git clone https://github.com/yourusername/ha-smart_appliance_monitor.git
cd ha-smart_appliance_monitor

# Créer un lien symbolique dans votre instance HA de développement
ln -s $(pwd)/custom_components/smart_appliance_monitor /config/custom_components/

# Installer les dépendances de développement
pip install -r requirements-dev.txt

# Lancer les tests
pytest tests/
```

## 📝 Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 👤 Auteur

**Gaëtan (Lega)**

- 🌐 Home Assistant : https://home.lega.wtf
- 💬 Créé avec ❤️ pour la communauté Home Assistant

## 🙏 Remerciements

- La communauté Home Assistant
- Les mainteneurs de HACS
- Tous les contributeurs et testeurs

## 📞 Support

- 🐛 [Signaler un bug](https://github.com/yourusername/ha-smart_appliance_monitor/issues)
- 💡 [Proposer une fonctionnalité](https://github.com/yourusername/ha-smart_appliance_monitor/issues)
- 💬 [Discussions](https://github.com/yourusername/ha-smart_appliance_monitor/discussions)

---

**⭐ Si ce projet vous plaît, n'hésitez pas à lui donner une étoile sur GitHub !**

