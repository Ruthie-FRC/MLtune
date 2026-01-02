# MLtune

Bayesian optimization for FRC robot parameter tuning. Tune shooter coefficients (or anything else) automatically using machine learning.

## What It Does

You take shots. You tell it if you hit or missed. It figures out better coefficients. Repeat until your shooter is dialed in.

Uses Bayesian optimization because it's sample-efficient and handles noisy data well - perfect for robot tuning where test time is limited.

## Quick Start

```bash
git clone https://github.com/Ruthie-FRC/MLtune.git
cd MLtune

# Run (creates venv, installs deps, launches GUI + dashboard)
scripts/START.sh  # Mac/Linux
scripts\START.bat  # Windows
```

First run takes a minute to install packages. Subsequent runs are instant.

## Features

- **Bayesian optimization** - Smart, sample-efficient tuning
- **NetworkTables integration** - Works with standard WPILib
- **GUI + web dashboard** - Desktop window and http://localhost:8050
- **Auto-reconnect** - Handles robot reboots gracefully
- **Hotkeys** - Quick controls (when they work)
- **Logging** - Everything is logged for review

## Requirements

- Python 3.8+
- WPILib 2024+ on your robot
- NetworkTables connection

## Docs

- [Getting Started](docs/GETTING_STARTED.md) - Install and run
- [Usage Guide](docs/USAGE.md) - Configure and tune
- [Robot Integration](docs/INTEGRATION.md) - Add to your robot code
- [Contributing](docs/CONTRIBUTING.md) - Development guide

## Structure

```
MLtune/
├── src/
│   ├── mltune/       # Core tuning system
│   └── dashboard/    # Web dashboard
├── java/             # Robot integration files
├── scripts/          # Launch scripts
└── docs/             # Documentation
```

## License

GPL-3.0 - see LICENSE

## Support

Open an issue if something breaks or doesn't make sense.

---

Built for FRC by Ruthie-FRC
