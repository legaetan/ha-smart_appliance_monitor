# 🏠 Smart Appliance Monitor

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![GitHub Release](https://img.shields.io/github/release/yourusername/ha-smart_appliance_monitor.svg)](https://github.com/yourusername/ha-smart_appliance_monitor/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **⚠️ Projet en développement** - Cette intégration est actuellement en phase de concept et développement initial.

## 🎯 Vision

Une intégration HACS complète qui transforme n'importe quelle prise connectée en système de surveillance intelligent d'appareil électroménager, **sans configuration manuelle** !

## ✨ Fonctionnalités (Prévues)

- 🔌 **Surveillance automatique** - Détection intelligente des cycles de démarrage/arrêt
- 📊 **Statistiques détaillées** - Durée, consommation, coût par cycle
- 🤖 **Apprentissage automatique** - Calibration automatique des seuils
- 🔔 **Notifications enrichies** - Alertes avec statistiques et graphiques
- 📈 **Dashboard intégré** - Interface complète générée automatiquement
- 💰 **Suivi des coûts** - Calcul du coût par cycle et totaux journaliers/mensuels
- 🌍 **Multi-langue** - Support français et anglais (extensible)

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

- **[Concept complet](CONCEPT_INTEGRATION_HACS.md)** - Vision et fonctionnalités détaillées
- **[Spécifications techniques](SPECS_TECHNIQUES_INTEGRATION.md)** - Architecture et code
- **[Ressources développement](RESSOURCES_DEVELOPPEMENT.md)** - Guide pour contribuer
- **[Index complet](INDEX_COMPLET.md)** - Navigation dans la documentation

## 🛠️ État du Projet

### Phase Actuelle : Initialisation

- [x] Concept et spécifications
- [x] Documentation complète
- [ ] Structure du projet
- [ ] Intégration de base
- [ ] Config flow
- [ ] Entités (sensors, binary_sensors, etc.)
- [ ] Mode apprentissage
- [ ] Dashboard automatique
- [ ] Tests unitaires
- [ ] Publication HACS

### Roadmap

#### v0.1.0 - MVP (Prévu : T1 2026)
- Configuration via UI
- Détection cycle démarrage/arrêt
- Capteurs de base (état, durée, consommation, coût)
- Notifications simples

#### v0.5.0 - Fonctionnalités avancées (Prévu : T2 2026)
- Mode apprentissage automatique
- Profils d'appareils pré-configurés
- Dashboard automatique
- Statistiques avancées

#### v1.0.0 - Version production (Prévu : T3 2026)
- ML pour détection intelligente
- Intégration Energy Dashboard
- Multi-langue complet
- Documentation utilisateur complète

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

