# Guide de développement - Smart Appliance Monitor

## Configuration de l'environnement

### Prérequis

- Python 3.11 ou supérieur
- Home Assistant 2024.1 ou supérieur
- Git

### Installation

```bash
# Cloner le dépôt
cd /config/___dev
git clone <votre-repo> ha-smart_appliance_monitor

# Créer un environnement virtuel
python3 -m venv venv
source venv/bin/activate  # Sur Linux/Mac
# ou
venv\Scripts\activate  # Sur Windows

# Installer les dépendances de développement
pip install -r requirements-dev.txt
```

### Installation dans Home Assistant (développement)

```bash
# Créer un lien symbolique vers custom_components
ln -s /config/___dev/ha-smart_appliance_monitor/custom_components/smart_appliance_monitor \
      /config/custom_components/smart_appliance_monitor

# Redémarrer Home Assistant
ha core restart
```

## Tests

### Exécuter tous les tests

```bash
pytest
```

### Exécuter des tests spécifiques

```bash
# Tests d'un seul fichier
pytest tests/test_state_machine.py

# Tests d'une seule fonction
pytest tests/test_state_machine.py::test_cycle_start_detection

# Tests avec verbosité
pytest -v

# Tests avec couverture
pytest --cov=custom_components.smart_appliance_monitor --cov-report=html
```

### Tests marqués

```bash
# Seulement les tests unitaires
pytest -m unit

# Seulement les tests d'intégration
pytest -m integration

# Exclure les tests lents
pytest -m "not slow"
```

## Linting et formatage

### Ruff (linting)

```bash
# Vérifier le code
ruff check custom_components/ tests/

# Corriger automatiquement
ruff check --fix custom_components/ tests/
```

### Black (formatage)

```bash
# Vérifier le formatage
black --check custom_components/ tests/

# Formater automatiquement
black custom_components/ tests/
```

### MyPy (type checking)

```bash
mypy custom_components/smart_appliance_monitor/
```

## Structure du projet

```
ha-smart_appliance_monitor/
├── custom_components/
│   └── smart_appliance_monitor/
│       ├── __init__.py              # Point d'entrée
│       ├── binary_sensor.py         # Capteurs binaires
│       ├── button.py                # Boutons
│       ├── config_flow.py           # Configuration UI
│       ├── const.py                 # Constantes
│       ├── coordinator.py           # Coordinator
│       ├── device.py                # Device info
│       ├── entity.py                # Classe de base entité
│       ├── manifest.json            # Métadonnées
│       ├── notify.py                # Notifications
│       ├── sensor.py                # Capteurs
│       ├── services.yaml            # Services
│       ├── state_machine.py         # Machine à états
│       ├── strings.json             # Traductions (EN)
│       ├── switch.py                # Switches
│       └── translations/
│           └── fr.json              # Traductions (FR)
├── tests/
│   ├── conftest.py                  # Configuration tests
│   ├── test_binary_sensor.py
│   ├── test_button.py
│   ├── test_coordinator.py
│   ├── test_notify.py
│   ├── test_sensor.py
│   ├── test_services.py
│   ├── test_state_machine.py
│   └── test_switch.py
├── DOC/                             # Documentation
├── .gitignore
├── pytest.ini                       # Configuration pytest
├── requirements-dev.txt             # Dépendances dev
├── DEVELOPMENT.md                   # Ce fichier
└── README.md                        # README principal
```

## Workflow de développement

### 1. Créer une branche

```bash
git checkout -b feature/ma-nouvelle-fonctionnalite
```

### 2. Développer et tester

```bash
# Faire vos modifications
# Écrire les tests
pytest tests/test_mon_module.py

# Vérifier le linting
ruff check .
black --check .
```

### 3. Commit

```bash
git add .
git commit -m "feat: description de la fonctionnalité"
```

### 4. Push et Pull Request

```bash
git push origin feature/ma-nouvelle-fonctionnalite
# Créer une PR sur GitHub
```

## Conventions de code

### Style

- Suivre PEP 8
- Utiliser Black pour le formatage
- Utiliser les type hints
- Documenter les fonctions avec des docstrings

### Exemple de docstring

```python
def ma_fonction(param1: str, param2: int) -> bool:
    """Description courte de la fonction.
    
    Description longue si nécessaire.
    
    Args:
        param1: Description du paramètre 1
        param2: Description du paramètre 2
        
    Returns:
        Description du retour
        
    Raises:
        ValueError: Quand param2 est négatif
    """
    if param2 < 0:
        raise ValueError("param2 doit être positif")
    
    return param1 == "test"
```

### Commits

Utiliser la convention Conventional Commits :

- `feat:` Nouvelle fonctionnalité
- `fix:` Correction de bug
- `docs:` Documentation
- `test:` Tests
- `refactor:` Refactoring
- `chore:` Tâches de maintenance

## Debugging

### Logs

Les logs sont dans `/config/home-assistant.log` ou visibles via :

```bash
tail -f /config/home-assistant.log | grep smart_appliance_monitor
```

### Niveau de logs

Ajouter dans `configuration.yaml` :

```yaml
logger:
  default: info
  logs:
    custom_components.smart_appliance_monitor: debug
```

### Debugging avec VS Code

Configuration `.vscode/launch.json` :

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Tests",
      "type": "python",
      "request": "launch",
      "module": "pytest",
      "args": ["-v"],
      "console": "integratedTerminal"
    }
  ]
}
```

## Documentation

### Mettre à jour la documentation

- README principal : `README.md`
- Documentation technique : `DOC/`
- Traductions : `custom_components/smart_appliance_monitor/translations/`

### Générer la documentation

```bash
# TODO: Ajouter sphinx ou mkdocs
```

## Ressources

### Home Assistant

- [Developer Documentation](https://developers.home-assistant.io/)
- [Integration Quality Scale](https://developers.home-assistant.io/docs/integration_quality_scale_index)
- [Config Flow](https://developers.home-assistant.io/docs/config_entries_config_flow_handler)

### Intégrations de référence

- [PowerCalc](https://github.com/bramstroker/homeassistant-powercalc)
- [Adaptive Lighting](https://github.com/basnijholt/adaptive-lighting)

### Communauté

- [Home Assistant Community](https://community.home-assistant.io/)
- [Discord](https://discord.gg/home-assistant)

## Support

Pour toute question ou problème :

1. Consulter la documentation dans `DOC/`
2. Vérifier les issues existantes sur GitHub
3. Créer une nouvelle issue si nécessaire

