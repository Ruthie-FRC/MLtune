# MLtune

Automatic parameter tuning for FRC robots using Bayesian optimization.

## Overview

MLtune tunes robot parameters (shooter coefficients, PID gains, etc.) by learning from shot data. The system uses Bayesian optimization to efficiently explore the parameter space and find optimal values.

The tuner runs on your driver station laptop and communicates with the robot via NetworkTables. After each shot, you provide feedback (hit/miss), and the system updates its model to suggest better parameters.

## Installation

```bash
git clone https://github.com/Ruthie-FRC/MLtune.git
cd MLtune
scripts/START.sh  # or START.bat on Windows
```

The start script creates a virtual environment, installs dependencies, and launches both the GUI and web dashboard.

## Requirements

- Python 3.8 or newer
- WPILib 2024+ (for robot integration)
- NetworkTables connection between laptop and robot

## Documentation

All documentation is in the `docs/` folder:

- [Getting Started](docs/GETTING_STARTED.md) - Installation and setup
- [Usage Guide](docs/USAGE.md) - Configuration and operation
- [Robot Integration](docs/INTEGRATION.md) - Adding to robot code
- [Contributing](docs/CONTRIBUTING.md) - Development information
- [Repository Structure](docs/STRUCTURE.md) - Detailed navigation guide

### Component Documentation

- [mltune/](docs/mltune/) - Core tuning system
- [dashboard/](docs/dashboard/) - Web interface
- [java-integration/](docs/java-integration/) - Robot integration files
- [scripts/](docs/scripts/) - Launcher scripts

## Repository Structure

```
MLtune/
├── mltune/           # Core tuning system
├── dashboard/        # Web interface
├── java-integration/ # Robot code integration files
├── scripts/          # Launcher and utility scripts
└── docs/             # All documentation
    ├── mltune/           # mltune component docs
    ├── dashboard/        # dashboard component docs
    ├── java-integration/ # java integration docs
    └── scripts/          # scripts documentation
```

**📁 [See detailed structure guide →](docs/STRUCTURE.md)**

## License

GPL-3.0 - See LICENSE for details.

## Issues and Support

Report issues at https://github.com/Ruthie-FRC/MLtune/issues
