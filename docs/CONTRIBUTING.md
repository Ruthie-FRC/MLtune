# Contributing

## Development Setup

```bash
git clone https://github.com/FRC5892/MLtune.git
cd MLtune
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r MLtune/tuner/requirements.txt
pip install -r dashboard/requirements.txt
```

## Project Structure

```
MLtune/
├── MLtune/             # Main tuning application (Python)
│   ├── tuner/          # Core tuning system
│   │   ├── config.py   # Configuration loading
│   │   ├── tuner.py    # Main coordinator
│   │   ├── optimizer.py # Bayesian optimization
│   │   ├── nt_interface.py # NetworkTables communication
│   │   ├── gui.py      # Desktop GUI
│   │   ├── logger.py   # Logging utilities
│   │   ├── main.py     # Entry point
│   │   └── requirements.txt # Python dependencies
│   └── config/         # User configuration files
│       ├── COEFFICIENT_TUNING.py # Define parameters
│       └── TUNER_TOGGLES.ini # Behavior settings
├── dashboard/          # Web dashboard (Dash/Plotly)
│   ├── app.py          # Main dashboard application
│   ├── __main__.py     # Entry point
│   └── requirements.txt # Python dependencies
├── java-integration/   # Files to copy into robot code
│   ├── TunerInterface.java # Main interface
│   ├── LoggedTunableNumber.java # Tunable wrapper
│   ├── FiringSolutionSolver.java # Example implementation
│   └── Constants_Addition.java # Example constants
├── scripts/            # Launch and utility scripts
│   ├── START.sh / START.bat # Main launcher
│   ├── RUN_TUNER.sh / RUN_TUNER.bat # Alternative launcher
│   ├── CREATE_DESKTOP_SHORTCUT.bat # Windows shortcut creator
│   ├── activate_venv.sh / activate_venv.ps1 # Virtual environment auto-activation
│   └── tuner_daemon.py # Background daemon mode
└── docs/               # User and developer documentation
```

## Code Guidelines

- Maintain readability
- Match existing code style
- Document non-obvious functionality
- Avoid unnecessary complexity

## Testing

Automated tests are not currently implemented. Manual testing procedure:

- Execute changes in development environment
- Test with robot hardware when possible
- Verify GUI and dashboard functionality

## Documentation

Documentation should be:
- Concise and informative
- Technically accurate
- Free of unnecessary explanation

## Submitting Changes

1. Fork the repository
2. Implement changes
3. Test functionality
4. Submit pull request with clear description

## Architecture

### System Flow

1. `tuner.py` coordinates system operation
2. `nt_interface.py` manages robot communication
3. `optimizer.py` implements Bayesian optimization
4. `config.py` handles configuration loading
5. `gui.py` and `dashboard/` provide user interfaces

### Design Rationale

**Bayesian Optimization**
- Sample-efficient for robot tuning scenarios
- Handles measurement noise effectively
- No gradient information required

**scikit-optimize**
- Mature, well-tested implementation
- Straightforward API
- Adequate performance characteristics

**Separate GUI and Dashboard**
- GUI: Simple interface for operators
- Dashboard: Detailed interface for engineers

**NetworkTables**
- FRC standard protocol
- Native WPILib integration
- Low latency, real-time capable

## Potential Improvements

- Automated test suite
- Additional optimization algorithms
- Enhanced optimization history visualization
- Improved configuration validation
- Multi-robot support capability

## Development Tasks

### Run Tuner

```bash
python -m MLtune.tuner.gui
```

### Run Dashboard

```bash
python -m dashboard.app
```

### Test Without Robot

The system provides fallback behavior when NetworkTables is unavailable. Basic functionality can be tested without hardware.

### Add Coefficient

Modify `MLtune/config/COEFFICIENT_TUNING.py`:

```python
COEFFICIENTS = [
    {
        'name': 'coefficient_name',
        'bounds': (minimum, maximum),
        'initial': starting_value
    }
]
```

### Modify Optimization

See `MLtune/tuner/optimizer.py`. The `BayesianOptimizer` class wraps scikit-optimize. Alternative optimization approaches can be implemented by replacing this component.

## Support

For questions or issues, open a GitHub issue.
