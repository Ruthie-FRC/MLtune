# Getting Started

## Install Python

You need Python 3.8 or newer. Check if you have it:

```bash
python3 --version  # Mac/Linux
python --version   # Windows
```

Don't have it? Get it from [python.org](https://python.org). On Windows, check "Add Python to PATH" during install.

## Get the Code

```bash
git clone https://github.com/Ruthie-FRC/MLtune.git
cd MLtune
```

Or download the ZIP from GitHub if you don't have git.

## Run It

**Windows:**
```bash
scripts\START.bat
```

**Mac/Linux:**
```bash
chmod +x scripts/START.sh
scripts/START.sh
```

The script creates a venv, installs dependencies, and launches both the GUI and web dashboard. First run takes a minute while it installs packages.

## What You Get

- **GUI window** - Shows connection status and logs
- **Web dashboard** - Open http://localhost:8050 in your browser
- **Auto-reconnect** - Handles robot reboots gracefully

## Configure Your Robot

Before tuning, you need to add our NetworkTables interface to your robot code. See [INTEGRATION.md](INTEGRATION.md).

## Verify It Works

1. Connect your laptop to the robot network
2. Run the start script
3. Check the GUI - should show "Connected" in green
4. Open the dashboard - should show live robot data

If something breaks, check that:
- Your robot is on and connected
- NetworkTables is running on the robot
- Your team number is correct in the config

## What's Next?

Read [USAGE.md](USAGE.md) to actually tune something.
