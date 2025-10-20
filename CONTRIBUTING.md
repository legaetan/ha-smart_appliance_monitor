# Contributing to Smart Appliance Monitor

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to the project.

## Development Setup

### Prerequisites

- Python 3.11 or higher
- Home Assistant 2024.1 or higher
- Git

### Getting Started

1. **Fork and Clone**

```bash
git clone https://github.com/yourusername/ha-smart_appliance_monitor.git
cd ha-smart_appliance_monitor
```

2. **Create Virtual Environment**

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

3. **Install Dependencies**

```bash
pip install -r requirements-dev.txt
```

4. **Link to Home Assistant** (for testing)

```bash
ln -s $(pwd)/custom_components/smart_appliance_monitor \
      /config/custom_components/smart_appliance_monitor
```

## Development Workflow

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Changes

- Write clear, documented code
- Follow existing code style
- Add tests for new functionality
- Update documentation as needed

### 3. Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=custom_components.smart_appliance_monitor --cov-report=html

# Run specific test file
pytest tests/test_state_machine.py

# Run specific test
pytest tests/test_state_machine.py::test_cycle_start_detection
```

### 4. Check Code Quality

```bash
# Linting
ruff check custom_components/ tests/

# Auto-fix linting issues
ruff check --fix custom_components/ tests/

# Formatting
black --check custom_components/ tests/

# Auto-format code
black custom_components/ tests/

# Type checking
mypy custom_components/smart_appliance_monitor/
```

### 5. Commit Changes

Use [Conventional Commits](https://www.conventionalcommits.org/) format:

```bash
git commit -m "feat: add new sensor for average cycle duration"
git commit -m "fix: correct energy calculation in state machine"
git commit -m "docs: update installation instructions"
```

**Commit Types:**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `test:` Test additions or modifications
- `refactor:` Code refactoring
- `chore:` Maintenance tasks

### 6. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub with:
- Clear description of changes
- Reference to related issues
- Screenshots (if UI changes)

## Code Style

### Python Style

- Follow [PEP 8](https://pep8.org/)
- Use Black for formatting (line length: 88)
- Use type hints for all functions
- Write docstrings for public functions

### Docstring Format

```python
def calculate_cost(energy: float, price: float) -> float:
    """Calculate the cost of energy consumption.
    
    Args:
        energy: Energy consumed in kWh
        price: Price per kWh in currency units
        
    Returns:
        Total cost in currency units
        
    Raises:
        ValueError: If energy or price is negative
    """
    if energy < 0 or price < 0:
        raise ValueError("Energy and price must be non-negative")
    
    return energy * price
```

### Home Assistant Conventions

- Use `_LOGGER` for logging
- Use `async` functions for I/O operations
- Follow Home Assistant's [coding standards](https://developers.home-assistant.io/docs/development_guidelines)
- Use `DataUpdateCoordinator` for data management
- Implement proper error handling

## Testing Guidelines

### Test Structure

- One test file per source file
- Group related tests in classes
- Use descriptive test names
- Use fixtures from `conftest.py`

### Test Example

```python
"""Tests for state machine."""
import pytest
from custom_components.smart_appliance_monitor.state_machine import CycleStateMachine


class TestCycleDetection:
    """Test cycle detection logic."""
    
    def test_cycle_starts_when_power_exceeds_threshold(self):
        """Test that cycle starts when power exceeds threshold for delay period."""
        machine = CycleStateMachine(
            start_threshold=50,
            stop_threshold=5,
            start_delay=120,
            stop_delay=300
        )
        
        # Power below threshold
        event = machine.update(30, 0.0)
        assert event is None
        assert machine.state == "idle"
        
        # Power above threshold but not long enough
        event = machine.update(60, 0.0)
        assert event is None
        assert machine.state == "idle"
        
        # Wait for delay period
        # ... (test continues)
```

### Test Coverage

- Aim for >90% code coverage
- Test happy paths and edge cases
- Test error conditions
- Mock external dependencies

## Documentation

### Update Documentation

When making changes, update relevant documentation:

- **README.md** - If adding major features
- **docs/wiki/** - If changing functionality
- **CHANGELOG.md** - All user-facing changes
- **Code comments** - Complex logic or algorithms

### Documentation Style

- Use clear, concise language
- Include code examples
- Add screenshots for UI changes
- Keep table of contents updated

## Pull Request Process

### Before Submitting

- [ ] All tests pass
- [ ] Code is formatted (Black)
- [ ] No linting errors (Ruff)
- [ ] Documentation is updated
- [ ] CHANGELOG.md is updated
- [ ] Commit messages follow convention

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
How to test these changes

## Checklist
- [ ] Tests pass
- [ ] Code formatted
- [ ] Documentation updated
- [ ] CHANGELOG updated
```

### Review Process

1. Maintainer reviews code
2. Automated tests run
3. Feedback addressed
4. Approved and merged

## Project Structure

```
ha-smart_appliance_monitor/
├── custom_components/
│   └── smart_appliance_monitor/
│       ├── __init__.py          # Integration entry point
│       ├── binary_sensor.py     # Binary sensor platform
│       ├── button.py            # Button platform
│       ├── config_flow.py       # UI configuration
│       ├── const.py             # Constants
│       ├── coordinator.py       # Data coordinator
│       ├── device.py            # Device utilities
│       ├── entity.py            # Base entity class
│       ├── manifest.json        # Integration metadata
│       ├── notify.py            # Notification system
│       ├── sensor.py            # Sensor platform
│       ├── services.yaml        # Service definitions
│       ├── state_machine.py     # Cycle detection logic
│       ├── strings.json         # English translations
│       ├── switch.py            # Switch platform
│       └── translations/
│           └── fr.json          # French translations
├── tests/                       # Unit tests
├── docs/                        # Documentation
├── .gitignore
├── pytest.ini
├── requirements-dev.txt
├── CONTRIBUTING.md              # This file
├── LICENSE
└── README.md
```

## Key Components

### State Machine (`state_machine.py`)
Handles cycle detection logic with configurable thresholds and delays.

### Coordinator (`coordinator.py`)
Manages data updates, events, and statistics using Home Assistant's `DataUpdateCoordinator`.

### Platforms
- `sensor.py` - 10 sensor entities
- `binary_sensor.py` - 2 binary sensor entities
- `switch.py` - 2 switch entities
- `button.py` - 1 button entity

### Configuration (`config_flow.py`)
Handles initial setup, reconfiguration, and options flow.

## Debugging

### Enable Debug Logging

Add to `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.smart_appliance_monitor: debug
```

### View Logs

```bash
tail -f /config/home-assistant.log | grep smart_appliance_monitor
```

### VS Code Debug Configuration

`.vscode/launch.json`:

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

## Resources

- [Home Assistant Developer Docs](https://developers.home-assistant.io/)
- [Integration Quality Scale](https://developers.home-assistant.io/docs/integration_quality_scale_index)
- [Config Flow Documentation](https://developers.home-assistant.io/docs/config_entries_config_flow_handler)
- [Entity Documentation](https://developers.home-assistant.io/docs/core/entity)

## Getting Help

- Check existing [issues](https://github.com/legaetan/ha-smart_appliance_monitor/issues)
- Ask in [discussions](https://github.com/legaetan/ha-smart_appliance_monitor/discussions)
- Join the [Home Assistant Discord](https://discord.gg/home-assistant)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

