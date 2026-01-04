# MLtune

**Machine Learning-based Parameter Tuning for FRC Robots**

MLtune uses Bayesian optimization to automatically tune robot parameters (like shooter coefficients) based on real-world performance data. Instead of manually tweaking values, the system learns optimal parameters from shot attempts during practice or competition.

## Quick Start

### 1. Install and Run

**Windows:**
```bash
scripts\START.bat
```

**Mac/Linux:**
```bash
chmod +x scripts/START.sh
scripts/START.sh
```

The launcher will automatically set up a virtual environment, install dependencies, and start both the tuner and web dashboard.

### 2. Integrate with Robot

Copy the Java files from `java-integration/` to your robot project and add logging for shot attempts:

```java
// In your robot code
private TunerInterface tuner = new TunerInterface();

// Replace static constants with tunable values
private LoggedTunableNumber kV = new LoggedTunableNumber("Shooter/kV", 0.12);

// Log each shot attempt
tuner.logShot(distance, angle, didHit);
```

### 3. Tune Parameters

1. Connect to your robot's network
2. Open the dashboard at http://localhost:8050
3. Enable tuning and take shots
4. Let the system optimize parameters automatically

## Features

- **Bayesian Optimization** - Sample-efficient ML algorithm that learns from each shot
- **Real-time Tuning** - Optimizes parameters during practice or competition
- **Web Dashboard** - Monitor performance, view history, and control tuning
- **NetworkTables Integration** - Seamless communication with FRC robot code
- **Multiple Interfaces** - Desktop GUI and web dashboard for different use cases

## Documentation

- **[Getting Started](docs/GETTING_STARTED.md)** - Detailed installation and setup
- **[Usage Guide](docs/USAGE.md)** - Configuration and operation instructions
- **[Robot Integration](docs/ROBOT_INTEGRATION.md)** - How to integrate with your robot code
- **[Repository Structure](docs/REPO_STRUCTURE.md)** - Navigate the codebase
- **[Contributing](docs/CONTRIBUTING.md)** - Development and contribution guide

## System Requirements

- Python 3.8 or newer
- FRC robot with NetworkTables support
- Network connection to robot (wired or wireless)

## How It Works

1. **Data Collection** - Robot logs shot attempts (distance, angle, hit/miss) via NetworkTables
2. **Optimization** - Bayesian optimizer analyzes data and suggests improved parameters
3. **Update** - New coefficients are sent back to the robot automatically
4. **Repeat** - Process continues, learning and improving over time

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

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Support

For questions, issues, or feature requests, please open a GitHub issue.
