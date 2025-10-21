# Smart Appliance Monitor - Documentation Update (21 octobre 2025)

## 📚 Mise à Jour Majeure de la Documentation

Cette release marque une **réorganisation complète de la documentation** et l'ajout de **3 nouvelles idées majeures** pour l'avenir du projet.

## ✅ Réorganisation Complète de la Documentation

### Nouveau Fichier Central : `docs/IDEAS.md`
- **251 lignes** d'idées et fonctionnalités futures consolidées
- Organisation par **6 thèmes** : UI, ML, Energy, Integrations, Architecture, Advanced
- Sous-organisation par **priorité** : Court terme / Moyen terme / Long terme
- **Matrice de priorité** avec impact et effort estimés

### Release Notes Organisées
- Nouveau dossier `docs/release_notes/` avec index
- 6 fichiers de release notes déplacés et indexés (v0.5.1 à v0.5.6)
- Meilleure découvrabilité et organisation

### Documentation Épurée
- **README.md** : Suppression roadmap → Référence à IDEAS.md
- **ARCHITECTURE.md** : Focus sur l'architecture actuelle
- **Custom Cards README** : Roadmap consolidée
- **Wiki** : Références "(future feature)" remplacées par liens IDEAS.md

## 🆕 Trois Nouvelles Idées Majeures

### 1. Energy Storage File Integration
**Priorité** : Moyen terme | **Impact** : Élevé

- Lecture automatique du fichier `.storage/energy` de Home Assistant
- Récupération des configurations :
  - `energy_sources` - Sources d'énergie
  - `device_consumption` - Appareils suivis
  - `included_in_stat` - Statut d'inclusion
- Synchronisation automatique avec Energy Dashboard
- Détection et import des appareils déjà configurés

### 2. Custom Energy Dashboard
**Priorité** : Moyen terme | **Impact** : Élevé

Dashboard personnalisé inspiré du Energy Dashboard natif avec plus de contrôle :
- Périodes personnalisables (jour/semaine/mois/année/custom)
- Filtres avancés par appareil, type, pièce
- Vues et layouts flexibles
- Comparaisons multi-périodes
- Export des données et rapports
- Compatible avec l'intégration Energy Storage File

### 3. Automatic Appliance Detection 🔥
**Priorité** : Moyen terme | **Impact** : Très élevé

**Détection intelligente d'appareils non configurés** :

**Analyse des écarts de consommation** :
- Comparaison `energy_sources` (total) vs `device_consumption` (suivis)
- Détection automatique des pics non attribués
- Calcul de puissance moyenne sur période glissante
- Analyse de durée et pattern

**Reconnaissance intelligente** :
- Matching avec `APPLIANCE_PROFILES` basé sur :
  - Puissance moyenne du pic
  - Durée d'utilisation
  - Pattern de consommation
- Support : grille-pain, micro-ondes, plaques induction, etc.

**Proposition automatique** :
- Suggestion de création avec type détecté
- Pré-configuration des seuils d'après observations
- Notification pour validation utilisateur

**Historique et apprentissage** :
- Log des appareils détectés non configurés
- Statistiques sur consommation non suivie
- Amélioration continue du matching

## 📊 Matrice de Priorité Mise à Jour

| Priorité | Feature | Impact |
|----------|---------|--------|
| 🔴 Haute | Graphiques temps réel | Élevé |
| 🔴 Haute | Strict block mode | Élevé |
| 🟡 Moyenne | Energy Storage File | Élevé |
| 🟡 Moyenne | **Automatic Appliance Detection 🆕** | **Très élevé** |
| 🟡 Moyenne | Custom Energy Dashboard | Élevé |
| 🟡 Moyenne | ML Auto-calibration | Élevé |

## 🎯 Bénéfices

**Pour les Utilisateurs** :
- Vision claire des fonctionnalités futures
- Possibilité de voter et contribuer aux idées
- Documentation mieux organisée et plus accessible

**Pour le Projet** :
- Roadmap centralisée et maintenue
- Meilleure planification du développement
- Documentation épurée et professionnelle

## 📚 Fichiers Modifiés

### Nouveaux Fichiers
- `docs/IDEAS.md` (297 lignes)
- `docs/release_notes/README.md`

### Fichiers Nettoyés
- `README.md` - Roadmap supprimée
- `ARCHITECTURE.md` - Future enhancements consolidées
- `custom_components/.../www/smart-appliance-cards/README.md`
- `custom_components/.../www/smart-appliance-cards/PROJECT_STATUS.txt`
- `docs/wiki-github/Advanced-Features.md`
- `docs/wiki-github/Scheduling.md`
- `docs/wiki-github/Dashboards.md`
- `docs/wiki-github/Advanced-Notifications.md`

## 🔗 Liens Utiles

- **IDEAS.md** : [docs/IDEAS.md](docs/IDEAS.md)
- **Release Notes** : [docs/release_notes/](docs/release_notes/)
- **CHANGELOG** : [CHANGELOG.md](CHANGELOG.md)

---

**Type** : Documentation  
**Version intégration** : v0.5.6 (inchangée)  
**Date** : 21 octobre 2025

## 💡 Contribuer aux Idées

Vous avez des suggestions pour ces nouvelles fonctionnalités ? Participez aux discussions sur [GitHub](https://github.com/legaetan/ha-smart_appliance_monitor/discussions) !

