# Getting Started

## Prerequisites

Python 3.8 or newer is required. Verify your installation:

```bash
python3 --version  # Mac/Linux
python --version   # Windows
```

If Python is not installed, download it from [python.org](https://python.org). Windows users should enable "Add Python to PATH" during installation.

## Installation

Clone the repository:

```bash
git clone https://github.com/Ruthie-FRC/MLtune.git
cd MLtune
```

Alternatively, download the repository as a ZIP file from GitHub.

## Running the Application

Execute the appropriate start script for your platform:

**Windows:**
```bash
scripts\START.bat
```

**Mac/Linux:**
```bash
chmod +x scripts/START.sh
scripts/START.sh
```

The start script performs the following:
- Creates a Python virtual environment
- Installs required dependencies
- Launches the GUI application
- Starts the web dashboard (http://localhost:8050)

Initial startup takes approximately one minute while dependencies install. Subsequent launches are immediate.

## Robot Configuration

Before tuning, integrate the NetworkTables interface into your robot code. See [INTEGRATION.md](INTEGRATION.md) for instructions.

## Verification

After launching the application:

1. Connect your laptop to the robot's network
2. Check the GUI window for "Connected" status
3. Open http://localhost:8050 to access the web dashboard
4. Verify live robot data appears in the dashboard

If connection fails:
- Verify the robot is powered on and NetworkTables is running
- Check that the team number in the configuration matches your robot
- Ensure your laptop is connected to the correct network

## Next Steps

Refer to [USAGE.md](USAGE.md) for configuration and tuning procedures.