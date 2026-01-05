# MLtune

Bayesian optimization tuner for FRC robot parameters. Automatically tunes shooter coefficients and other parameters based on performance data collected during practice or competition.

## Quick Start

### 1. Install and Run

**Windows:**
```bash
scripts\START.bat
```

**Mac/Linux:**
```bash
scripts/START.sh
```

Creates virtual environment, installs dependencies, starts tuner and dashboard.

### 2. Integrate with Robot

Copy files from `java-integration/` to your robot project. Replace constants with `LoggedTunableNumber` and publish shot data to NetworkTables:

```java
private LoggedTunableNumber kV = new LoggedTunableNumber("Shooter/kV", 0.12);

public void logShot(boolean hit, double distance, double pitch, double velocity, double yaw) {
    // Publish to NetworkTables - see FiringSolutionSolver.java
}
```

### 3. Run

1. Connect to robot network
2. Open dashboard: http://localhost:8050
3. Enable tuning, take shots
4. System optimizes parameters based on results

## Features

- Bayesian optimization (scikit-optimize)
- Real-time parameter tuning during practice/competition
- Web dashboard (Dash/Plotly) for monitoring and control
- NetworkTables communication with robot
- Desktop GUI and web interface

## Documentation

- [Getting Started](docs/GETTING_STARTED.md) - Installation and setup
- [Usage Guide](docs/USAGE.md) - Configuration and operation
- [Robot Integration](docs/ROBOT_INTEGRATION.md) - Robot code integration
- [Repository Structure](docs/REPO_STRUCTURE.md) - Codebase navigation
- [Contributing](docs/CONTRIBUTING.md) - Development guide

## Requirements

- Python 3.8+
- FRC robot with NetworkTables
- Network connection to robot

## Operation

1. Robot logs shot data (distance, angle, hit/miss) to NetworkTables
2. Tuner applies Bayesian optimization to collected data
3. Updated coefficients published to NetworkTables
4. Robot reads new values from LoggedTunableNumber instances

## Repository Structure

```
MLtune/
├── MLtune/           # Core Python tuning system
├── dashboard/        # Web monitoring interface
├── java-integration/ # Robot code integration files
├── scripts/          # Launch scripts
└── docs/             # Documentation
```

## License

GNU General Public License v3.0 - see [LICENSE](LICENSE).
