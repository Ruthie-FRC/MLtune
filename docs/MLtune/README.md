# MLtune Core Application

Main tuning application using Bayesian optimization.

## What's Here

- `tuner/` - Core tuning logic and algorithms
- `config/` - Configuration files

## Configuration

Edit these files to configure tuning:

- `config/COEFFICIENT_TUNING.py` - Define parameters to tune
- `config/TUNER_TOGGLES.ini` - Control tuning behavior

## Key Files

- `tuner/tuner.py` - Main coordinator
- `tuner/optimizer.py` - Bayesian optimization
- `tuner/nt_interface.py` - Robot communication
- `tuner/gui.py` - Desktop GUI

See [../USAGE.md](../USAGE.md) for usage information.