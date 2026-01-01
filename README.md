# MLtune - Bayesian Optimization for FRC Shooters

MLtune is a machine learning-powered tuning system for FRC (FIRST Robotics Competition) shooters. It uses Bayesian optimization to automatically tune shooting coefficients based on real-time feedback from the robot.

## Features

- **Automated Coefficient Tuning**: Uses Bayesian optimization to find optimal shooting parameters
- **Web Dashboard**: Real-time browser-based control and monitoring interface
- **NetworkTables Integration**: Seamless communication with FRC robot code
- **7 Tunable Parameters**: Drag coefficient, gravity, shot height, target height, shooter angle, RPM, and exit velocity
- **Interactive Visualizations**: Track optimization progress with real-time graphs
- **Manual Override**: Fine-tune parameters manually when needed
- **Auto-Advance**: Automatically progress to next coefficient after achieving consistent accuracy

## Quick Start

### Windows
```batch
START.bat
```

### Mac/Linux
```bash
chmod +x START.sh
./START.sh
```

This will:
1. Create a virtual environment (if needed)
2. Install all dependencies
3. Launch both the tuner and dashboard

The dashboard will open automatically in your browser at `http://localhost:8050`

## Requirements

- Python 3.8 or newer
- NetworkTables (pynetworktables)
- Dash for web dashboard
- scikit-optimize for Bayesian optimization

## Project Structure

- `bayesopt/tuner/` - Core tuning engine
  - `tuner.py` - Main coordinator
  - `optimizer.py` - Bayesian optimization algorithms
  - `config.py` - Configuration system
- `dashboard/` - Web-based control interface
- `java-integration/` - Java robot code integration examples

## License

GNU General Public License v3.0 - See LICENSE file for details

Copyright (C) 2025 Ruthie-FRC
