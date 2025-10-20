# Plan de Développement - Smart Appliance Cards

**Version**: 0.4.0  
**Date**: Octobre 2025  
**Statut**: Planification terminée - Prêt pour le développement

## Vue d'Ensemble

Ce document décrit le plan de développement complet des deux cartes Lovelace personnalisées pour Smart Appliance Monitor:

1. **smart-appliance-cycle-card** - Carte d'affichage du cycle en cours
2. **smart-appliance-stats-card** - Carte de statistiques complètes

## Objectifs

- ✅ Créer des cartes visuellement attractives et modernes
- ✅ Utiliser lit-element pour la compatibilité avec Home Assistant
- ✅ Supporter la terminologie adaptative (cycle/session)
- ✅ Fournir des éditeurs de configuration visuels
- ✅ Optimiser les performances et la réactivité
- ✅ Assurer la compatibilité mobile et desktop
- ✅ Documentation complète en français et anglais

## Architecture Technique

### Stack Technologique

- **Framework**: [lit-element](https://lit.dev/) v3.x
- **Langage**: JavaScript ES2021+ (TypeScript optionnel)
- **Build**: Rollup.js avec plugins Babel
- **Styles**: CSS3 avec CSS Variables pour le theming
- **Charts**: Chart.js v4.x ou ApexCharts
- **Icons**: Material Design Icons (mdi:*)

### Structure des Fichiers

```
www/smart-appliance-cards/
├── README.md                          # Documentation utilisateur
├── DEVELOPMENT_PLAN.md                # Ce document
├── package.json                       # Dépendances npm
├── rollup.config.js                   # Configuration build
├── src/
│   ├── cards/
│   │   ├── smart-appliance-cycle-card.js      # Carte cycle
│   │   ├── smart-appliance-stats-card.js      # Carte stats
│   │   ├── cycle-card-editor.js               # Éditeur cycle
│   │   └── stats-card-editor.js               # Éditeur stats
│   ├── components/
│   │   ├── cycle-status.js                    # Composant statut animé
│   │   ├── power-graph.js                     # Mini graphique
│   │   ├── action-buttons.js                  # Boutons d'action
│   │   ├── stats-tabs.js                      # Onglets statistiques
│   │   └── trend-indicator.js                 # Indicateur de tendance
│   ├── utils/
│   │   ├── helpers.js                         # Fonctions utilitaires
│   │   ├── formatters.js                      # Formatage des valeurs
│   │   └── constants.js                       # Constantes
│   └── styles/
│       ├── cycle-card-styles.js               # Styles carte cycle
│       ├── stats-card-styles.js               # Styles carte stats
│       └── common-styles.js                   # Styles communs
├── dist/
│   ├── smart-appliance-cycle-card.js          # Build final cycle
│   └── smart-appliance-stats-card.js          # Build final stats
└── examples/
    ├── cycle-card-basic.yaml                  # Exemple basique cycle
    ├── cycle-card-advanced.yaml               # Exemple avancé cycle
    ├── stats-card-basic.yaml                  # Exemple basique stats
    └── stats-card-advanced.yaml               # Exemple avancé stats
```

## Carte 1: smart-appliance-cycle-card

### Fonctionnalités

#### Affichage du Statut (Priorité Haute)
- **Indicateur visuel circulaire** avec animation
  - État `idle`: Gris avec icône d'appareil
  - État `running`: Vert avec animation de rotation/pulse
  - État `finished`: Bleu avec icône de checkmark
- **Support terminologie adaptative**: "Cycle" vs "Session" selon le type d'appareil
- **Transitions fluides** entre les états

#### Informations en Temps Réel (Priorité Haute)
- **Durée actuelle**: Format HH:MM:SS avec mise à jour en direct
- **Énergie consommée**: Format X.XX kWh avec icône éclair
- **Coût estimé**: Format X.XX € avec symbole monétaire
- **Puissance actuelle**: Format XXX W (optionnel, configurable)

#### Mini Graphique de Puissance (Priorité Moyenne)
- **Graphique en ligne** des 30 dernières minutes
- **Zone colorée** sous la courbe
- **Marqueurs de seuils**: Start threshold et stop threshold
- **Échelle automatique** avec valeurs min/max
- **Responsive**: Adapté à la largeur de la carte

#### Boutons d'Action (Priorité Moyenne)
- **Arrêter la surveillance**: Appel service `stop_monitoring`
- **Réinitialiser les stats**: Appel service `reset_statistics`
- **Démarrer un cycle manuellement**: Appel service `start_cycle`
- **Icônes claires** avec tooltips

#### États Spéciaux (Priorité Haute)
- **Alerte durée**: Bordure orange + icône si cycle > durée attendue
- **Appareil débranché**: Bordure rouge + message si unplugged
- **Pas de surveillance**: Message informatif si monitoring désactivé

### Configuration

```yaml
type: custom:smart-appliance-cycle-card
entity: sensor.washing_machine_state
name: Machine à Laver  # Optionnel, auto-détecté
show_power_graph: true  # Défaut: true
show_action_buttons: true  # Défaut: true
show_current_power: false  # Défaut: false
graph_hours: 0.5  # Défaut: 0.5 (30 min)
theme: auto  # auto/light/dark
```

### Éditeur Visuel

Interface de configuration avec:
- Sélecteur d'entité (sensor.xxx_state)
- Toggle pour afficher/masquer le graphique
- Toggle pour afficher/masquer les boutons
- Toggle pour afficher/masquer la puissance actuelle
- Slider pour la durée du graphique (15min - 2h)
- Sélecteur de thème (auto/light/dark)

## Carte 2: smart-appliance-stats-card

### Fonctionnalités

#### Interface à Onglets (Priorité Haute)
- **3 onglets**: Aujourd'hui / Semaine / Mois
- **Navigation fluide** avec animation de transition
- **Indicateur actif** sous l'onglet sélectionné
- **Mémorisation** de l'onglet sélectionné dans le state

#### Vue "Aujourd'hui" (Priorité Haute)
- **Nombre de cycles**: Badge avec chiffre
- **Énergie totale**: XX.X kWh avec graphique en barre
- **Coût total**: XX.XX € avec icône monétaire
- **Durée moyenne**: HH:MM par cycle
- **Comparaison hier**: Indicateurs ↑ ↓ → avec pourcentage

#### Vue "Semaine" (Priorité Moyenne)
- **Graphique en barres**: Énergie par jour (7 derniers jours)
- **Nombre total de cycles**: Nombre
- **Coût total**: Avec comparaison semaine précédente
- **Jour le plus actif**: Nom du jour + nombre de cycles
- **Tendance**: Indicateur visuel (hausse/baisse/stable)

#### Vue "Mois" (Priorité Moyenne)
- **Graphique en ligne**: Énergie par semaine (4 dernières semaines)
- **Nombre total de cycles**: Nombre
- **Coût total**: Avec comparaison mois précédent
- **Projection fin de mois**: Estimation basée sur la moyenne
- **Record mensuel**: Jour avec le plus de cycles

#### Indicateurs de Tendance (Priorité Moyenne)
- **Flèches colorées**: 
  - ↑ Rouge: Augmentation > 10%
  - ↓ Vert: Diminution > 10%
  - → Gris: Stable (±10%)
- **Pourcentage de variation**: +X% ou -X%
- **Label explicite**: "vs hier", "vs semaine dernière", etc.

#### Métriques d'Efficacité (Priorité Basse)
- **Coût moyen par cycle**: XX.XX €
- **Énergie moyenne par cycle**: X.XX kWh
- **Durée moyenne**: HH:MM
- **Meilleure heure**: Heure avec tarif le plus bas utilisée

### Configuration

```yaml
type: custom:smart-appliance-stats-card
entity: sensor.washing_machine_state
name: Statistiques Machine  # Optionnel
default_tab: today  # today/week/month
show_trends: true  # Défaut: true
show_efficiency: true  # Défaut: true
chart_type: bar  # bar/line
theme: auto  # auto/light/dark
```

### Éditeur Visuel

Interface de configuration avec:
- Sélecteur d'entité principale
- Sélecteur d'onglet par défaut
- Toggle pour afficher/masquer les tendances
- Toggle pour afficher/masquer les métriques d'efficacité
- Sélecteur de type de graphique (barres/ligne)
- Sélecteur de thème

## Composants Réutilisables

### 1. CycleStatus Component
```javascript
// Affichage visuel du statut avec animation
class CycleStatus extends LitElement {
  static properties = {
    state: { type: String },
    animated: { type: Boolean }
  };
}
```

### 2. PowerGraph Component
```javascript
// Mini graphique de consommation
class PowerGraph extends LitElement {
  static properties = {
    data: { type: Array },
    hours: { type: Number },
    thresholds: { type: Object }
  };
}
```

### 3. ActionButtons Component
```javascript
// Boutons d'action avec tooltips
class ActionButtons extends LitElement {
  static properties = {
    entity: { type: String },
    buttons: { type: Array }
  };
}
```

### 4. StatsTabs Component
```javascript
// Interface à onglets pour statistiques
class StatsTabs extends LitElement {
  static properties = {
    tabs: { type: Array },
    activeTab: { type: String }
  };
}
```

### 5. TrendIndicator Component
```javascript
// Indicateur de tendance avec flèche et pourcentage
class TrendIndicator extends LitElement {
  static properties = {
    current: { type: Number },
    previous: { type: Number },
    label: { type: String }
  };
}
```

## Utilitaires

### helpers.js
```javascript
// Récupération d'entités liées
export function getRelatedEntities(hass, mainEntity) {
  // Retourne toutes les entités de l'appareil
}

// Calcul de statistiques
export function calculateStats(history, period) {
  // Retourne {count, total_energy, total_cost, avg_duration}
}

// Détection du type d'appareil
export function getApplianceType(entity) {
  // Retourne le type (washing_machine, dishwasher, etc.)
}
```

### formatters.js
```javascript
// Formatage de durée
export function formatDuration(seconds) {
  // Retourne "2h 30m" ou "45m 30s"
}

// Formatage d'énergie
export function formatEnergy(kwh) {
  // Retourne "2.34 kWh"
}

// Formatage de coût
export function formatCost(value, currency = '€') {
  // Retourne "1.23 €"
}

// Formatage de pourcentage
export function formatPercent(value) {
  // Retourne "+15%" ou "-8%"
}
```

### constants.js
```javascript
// États possibles
export const STATES = {
  IDLE: 'idle',
  RUNNING: 'running',
  FINISHED: 'finished'
};

// Couleurs par état
export const STATE_COLORS = {
  idle: '#9e9e9e',
  running: '#4caf50',
  finished: '#2196f3'
};

// Types d'appareils et terminologie
export const APPLIANCE_TERMINOLOGY = {
  washing_machine: 'cycle',
  dishwasher: 'cycle',
  dryer: 'cycle',
  monitor: 'session',
  nas: 'session',
  // ...
};
```

## Styles et Theming

### Système de Thème

Utilisation des CSS Variables de Home Assistant:
```css
:host {
  --primary-color: var(--primary-color);
  --text-primary-color: var(--primary-text-color);
  --card-background-color: var(--card-background-color);
  --divider-color: var(--divider-color);
  --state-idle-color: var(--state-inactive-color);
  --state-running-color: var(--state-active-color);
  --state-finished-color: var(--state-finished-color, #2196F3);
}
```

### Responsive Design

- **Desktop** (> 768px): Largeur complète, 2 colonnes si possible
- **Tablet** (768px - 480px): 1 colonne, éléments empilés
- **Mobile** (< 480px): Compact, boutons réduits, texte plus petit

### Animations

- **État running**: Animation `pulse` 2s infinite
- **Transition d'état**: `transition: all 0.3s ease`
- **Changement d'onglet**: `slide-in` avec fade
- **Graphiques**: Animation d'apparition progressive

## Configuration du Build

### package.json
```json
{
  "name": "smart-appliance-cards",
  "version": "0.4.0",
  "description": "Custom Lovelace cards for Smart Appliance Monitor",
  "main": "dist/smart-appliance-cycle-card.js",
  "scripts": {
    "build": "rollup -c",
    "watch": "rollup -c -w",
    "lint": "eslint src/**/*.js",
    "format": "prettier --write src/**/*.js"
  },
  "dependencies": {
    "lit": "^3.0.0",
    "chart.js": "^4.4.0"
  },
  "devDependencies": {
    "@babel/core": "^7.23.0",
    "@babel/preset-env": "^7.23.0",
    "@rollup/plugin-babel": "^6.0.0",
    "@rollup/plugin-node-resolve": "^15.2.0",
    "@rollup/plugin-terser": "^0.4.4",
    "eslint": "^8.52.0",
    "prettier": "^3.0.0",
    "rollup": "^4.0.0"
  },
  "keywords": ["home-assistant", "lovelace", "custom-card"],
  "author": "Smart Appliance Monitor Team",
  "license": "MIT"
}
```

### rollup.config.js
```javascript
import babel from '@rollup/plugin-babel';
import resolve from '@rollup/plugin-node-resolve';
import terser from '@rollup/plugin-terser';

const production = !process.env.ROLLUP_WATCH;

export default [
  {
    input: 'src/cards/smart-appliance-cycle-card.js',
    output: {
      file: 'dist/smart-appliance-cycle-card.js',
      format: 'es',
      sourcemap: !production
    },
    plugins: [
      resolve(),
      babel({ babelHelpers: 'bundled' }),
      production && terser()
    ]
  },
  {
    input: 'src/cards/smart-appliance-stats-card.js',
    output: {
      file: 'dist/smart-appliance-stats-card.js',
      format: 'es',
      sourcemap: !production
    },
    plugins: [
      resolve(),
      babel({ babelHelpers: 'bundled' }),
      production && terser()
    ]
  }
];
```

## Tests

### Tests Manuels

1. **Tests fonctionnels** dans Home Assistant
   - Installation des cartes
   - Configuration via UI
   - Vérification de chaque fonctionnalité
   - Test sur différents appareils

2. **Tests de compatibilité**
   - Chrome/Edge (Desktop + Mobile)
   - Firefox (Desktop + Mobile)
   - Safari (iOS + macOS)
   - Home Assistant Companion App (iOS + Android)

3. **Tests de performance**
   - Temps de chargement initial
   - Utilisation mémoire
   - Fluidité des animations
   - Rafraîchissement des données

### Checklist de Validation

- [ ] La carte s'affiche correctement au premier chargement
- [ ] L'éditeur visuel fonctionne et sauvegarde la config
- [ ] Les entités sont correctement détectées
- [ ] Les états changent en temps réel
- [ ] Les animations sont fluides (60 fps)
- [ ] Le thème s'adapte (light/dark)
- [ ] Les boutons d'action fonctionnent
- [ ] Les graphiques s'affichent correctement
- [ ] La carte est responsive (mobile/desktop)
- [ ] Pas d'erreurs dans la console
- [ ] Les traductions fonctionnent (EN/FR)

## Documentation

### README.md (Mise à jour)

Sections à ajouter/mettre à jour:
- ✅ Installation via HACS (instructions détaillées)
- ✅ Installation manuelle (copie de fichiers)
- ✅ Configuration YAML complète
- ✅ Exemples avec captures d'écran
- ✅ Options avancées
- ✅ Troubleshooting
- ✅ FAQ

### Exemples YAML

Créer des exemples pour chaque cas d'usage:
- Configuration minimale
- Configuration complète
- Multi-appareils
- Personnalisation avancée

### Captures d'Écran

Fournir des captures pour:
- Carte cycle (idle/running/finished)
- Carte stats (chaque onglet)
- Éditeurs visuels
- Thème light/dark
- Responsive mobile

## Roadmap de Développement

### Phase 1: Setup (1-2 jours)
- [x] Analyser les besoins
- [ ] Créer la structure de fichiers
- [ ] Configurer package.json et rollup
- [ ] Créer les fichiers de base

### Phase 2: Cycle Card (3-4 jours)
- [ ] Structure lit-element
- [ ] Affichage du statut animé
- [ ] Informations en temps réel
- [ ] Mini graphique de puissance
- [ ] Boutons d'action
- [ ] Éditeur de configuration
- [ ] Tests et ajustements

### Phase 3: Stats Card (3-4 jours)
- [ ] Structure lit-element
- [ ] Interface à onglets
- [ ] Vue "Aujourd'hui"
- [ ] Vue "Semaine"
- [ ] Vue "Mois"
- [ ] Indicateurs de tendance
- [ ] Éditeur de configuration
- [ ] Tests et ajustements

### Phase 4: Polish & Testing (2-3 jours)
- [ ] Optimisation des performances
- [ ] Responsive design
- [ ] Animations fluides
- [ ] Tests multi-navigateurs
- [ ] Documentation
- [ ] Exemples YAML

### Phase 5: Release (1 jour)
- [ ] Build de production
- [ ] Minification
- [ ] Création du package HACS
- [ ] Documentation finale
- [ ] Annonce de release

**Durée estimée totale**: 10-14 jours de développement actif

## Critères de Succès

### Fonctionnels
- ✅ Les 2 cartes sont opérationnelles
- ✅ Toutes les fonctionnalités planifiées sont implémentées
- ✅ Les éditeurs visuels fonctionnent parfaitement
- ✅ Compatibilité avec tous les types d'appareils
- ✅ Support de la terminologie adaptative

### Techniques
- ✅ Code propre et maintenable
- ✅ Performance optimale (< 100ms render)
- ✅ Build < 50KB par carte (minifié)
- ✅ 0 erreurs console en production
- ✅ Compatible HA 2024.1+

### Documentation
- ✅ README complet avec exemples
- ✅ Commentaires dans le code
- ✅ Exemples YAML fonctionnels
- ✅ Guide de troubleshooting
- ✅ Screenshots/GIFs de démo

### Qualité Utilisateur
- ✅ Interface intuitive sans formation
- ✅ Feedback visuel immédiat
- ✅ Erreurs explicites et utiles
- ✅ Responsive parfait mobile/desktop
- ✅ Thème adaptatif light/dark

## Dépendances Externes

### Requises
- Home Assistant 2024.1+
- Navigateur moderne (ES2021+)
- Smart Appliance Monitor v0.3.0+

### Optionnelles
- HACS (pour installation facile)
- Custom cards (Mushroom, Button Card) pour dashboards complets

## Problèmes Connus et Solutions

### Problème 1: Rafraîchissement des Graphiques
**Symptôme**: Les graphiques ne se mettent pas à jour en temps réel  
**Solution**: Utiliser `hass.connection.subscribeMessage` pour les updates

### Problème 2: Performance avec Beaucoup de Données
**Symptôme**: Lenteur avec historique de plusieurs mois  
**Solution**: Limiter les requêtes d'historique, utiliser la pagination

### Problème 3: Thème Non Respecté
**Symptôme**: Les couleurs ne suivent pas le thème HA  
**Solution**: Utiliser systématiquement les CSS Variables de HA

## Références

### Documentation Home Assistant
- [Lovelace Custom Cards](https://developers.home-assistant.io/docs/frontend/custom-ui/lovelace-custom-card/)
- [lit-element Guide](https://lit.dev/docs/)
- [Frontend Data](https://developers.home-assistant.io/docs/frontend/data/)

### Exemples de Cartes
- [Mushroom Cards](https://github.com/piitaya/lovelace-mushroom) - Inspiration UI
- [Mini Graph Card](https://github.com/kalkih/mini-graph-card) - Graphiques
- [Button Card](https://github.com/custom-cards/button-card) - Configuration

### Outils de Développement
- [Card Tools](https://github.com/thomasloven/lovelace-card-tools) - Helpers
- [Lit Analyzer](https://www.npmjs.com/package/lit-analyzer) - Validation
- [HA Frontend](https://github.com/home-assistant/frontend) - Code source référence

## Notes de Version

### v0.4.0 (Planifié)
- ✅ Première release des custom cards
- ✅ smart-appliance-cycle-card
- ✅ smart-appliance-stats-card
- ✅ Éditeurs visuels complets
- ✅ Support HACS

### v0.4.1 (Futur)
- [ ] Mode compact pour mobile
- [ ] Thèmes personnalisables
- [ ] Export de données CSV
- [ ] Graphiques interactifs (zoom, pan)

### v0.5.0 (Futur)
- [ ] Prédictions ML affichées
- [ ] Comparaisons multi-appareils
- [ ] Widget pour app companion
- [ ] Notifications push depuis la carte

---

**Document créé le**: 20 octobre 2025  
**Dernière mise à jour**: 20 octobre 2025  
**Auteur**: Smart Appliance Monitor Team  
**Statut**: ✅ Planification complète - Prêt pour développement
