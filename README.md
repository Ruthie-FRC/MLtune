# MLtune - Bayesian Optimization for FRC Shooters

MLtune is a machine learning-powered tuning system for FRC (FIRST Robotics Competition) shooters. It uses Bayesian optimization to automatically tune shooting coefficients based on real-time feedback from the robot.

## Platform Support

✅ **Windows** (Windows 10/11, VS Code)  
✅ **Chromebook** (Linux mode, VS Code)  
✅ **Mac** (macOS, VS Code)  
✅ **Linux** (Ubuntu, Debian, etc.)

## Features

- **Automated Coefficient Tuning**: Uses Bayesian optimization to find optimal shooting parameters
- **Web Dashboard**: Real-time browser-based control and monitoring interface
- **NetworkTables Integration**: Seamless communication with FRC robot code
- **7 Tunable Parameters**: Drag coefficient, gravity, shot height, target height, shooter angle, RPM, and exit velocity
- **Interactive Visualizations**: Track optimization progress with real-time graphs
- **Manual Override**: Fine-tune parameters manually when needed
- **Auto-Advance**: Automatically progress to next coefficient after achieving consistent accuracy

## Quick Start

### Windows (VS Code or Command Prompt)

1. Double-click `START.bat` or run:
   ```cmd
   START.bat
   ```

### Chromebook (Linux mode with VS Code)

1. Enable Linux (if not already enabled):
   - Settings → Advanced → Developers → Linux development environment → Turn on
2. Install Python 3.8+:
   ```bash
   sudo apt update
   sudo apt install python3 python3-venv python3-pip
   ```
3. Make the script executable and run:
   ```bash
   chmod +x START.sh
   ./START.sh
   ```

### Mac/Linux

```bash
chmod +x START.sh
./START.sh
```

### Using VS Code (All Platforms)

1. Open the project folder in VS Code
2. The terminal will automatically activate the Python virtual environment
3. Run the dashboard:
   ```bash
   python -m dashboard.app
   ```

The dashboard will open automatically in your browser at `http://localhost:8050`

## Installation

### Automatic (Recommended)

The `START.bat` (Windows) or `START.sh` (Mac/Linux/Chromebook) scripts handle everything automatically:
- Creates Python virtual environment
- Installs all dependencies
- Launches the dashboard

### Manual Installation

If you prefer to set up manually:

```bash
# Create virtual environment
python3 -m venv .venv

# Activate it
# On Windows:
.venv\Scripts\activate
# On Mac/Linux/Chromebook:
source .venv/bin/activate

# Install dependencies
pip install -r bayesopt/tuner/requirements.txt
pip install -r dashboard/requirements.txt

# Run dashboard
python -m dashboard.app
```

## Requirements

- **Python**: 3.8 or newer
- **NetworkTables**: pynetworktables (auto-installed)
- **Dash**: Web dashboard framework (auto-installed)
- **scikit-optimize**: Bayesian optimization (auto-installed)
- **Browser**: Any modern web browser (Chrome, Firefox, Edge, Safari)

### Chromebook-Specific Requirements

- Linux development environment enabled
- At least 4GB RAM recommended
- Python 3.8+ installed in Linux container

## Troubleshooting

### Chromebook Issues

**Problem**: Script won't run  
**Solution**: Make sure Linux is enabled and Python is installed:
```bash
sudo apt update && sudo apt install python3 python3-venv python3-pip
chmod +x START.sh
```

**Problem**: Permission denied  
**Solution**: Run with bash explicitly:
```bash
bash START.sh
```

### Windows Issues

**Problem**: Script won't run  
**Solution**: Make sure Python is installed and added to PATH. Download from [python.org](https://python.org)

**Problem**: Execution policy error (PowerShell)  
**Solution**: Run PowerShell as Administrator and execute:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### VS Code Issues

**Problem**: Python not detected  
**Solution**: 
1. Install Python extension for VS Code
2. Reload VS Code
3. Select Python interpreter: `Ctrl+Shift+P` → "Python: Select Interpreter" → Choose `.venv`

## Project Structure

```
MLtune/
├── bayesopt/tuner/         # Core tuning engine
│   ├── tuner.py           # Main coordinator
│   ├── optimizer.py       # Bayesian optimization algorithms
│   └── requirements.txt   # Python dependencies
├── dashboard/             # Web-based control interface
│   ├── app.py            # Dashboard application
│   ├── __main__.py       # Entry point
│   └── requirements.txt  # Dashboard dependencies
├── java-integration/      # Java robot code integration examples
├── .vscode/              # VS Code configuration
│   └── settings.json     # Cross-platform settings
├── START.bat             # Windows launcher
├── START.sh              # Mac/Linux/Chromebook launcher
└── README.md             # This file
```

## Development

### VS Code Setup (Automatic)

The project includes VS Code configuration that:
- Auto-detects your platform (Windows/Mac/Linux/Chromebook)
- Automatically activates the virtual environment
- Configures Python interpreter
- Sets up integrated terminal profiles

Just open the folder in VS Code and everything will work!

### GitHub Codespaces / Dev Containers

The project includes a `.devcontainer` configuration for cloud development:
- Works on any device with a browser
- No local installation required
- Automatically sets up environment

## License

GNU General Public License v3.0 - See LICENSE file for details

Copyright (C) 2025 Ruthie-FRC

## Support

For issues specific to:
- **Chromebook**: Check that Linux is properly enabled and Python 3.8+ is installed
- **Windows**: Ensure Python is in PATH and execution policies allow scripts
- **VS Code**: Install Python extension and reload window if needed

Happy tuning! 🎯🤖
