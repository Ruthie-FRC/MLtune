# Scripts

Launch and utility scripts for MLtune.

## Main Launchers

**START.sh / START.bat**
- Main launcher (use this)
- Creates venv, installs deps, runs GUI + dashboard
- Windows: `START.bat`
- Mac/Linux: `START.sh`

**RUN_TUNER.sh / RUN_TUNER.bat**
- Alternative launcher for daemon mode

## Utility Scripts

**CREATE_DESKTOP_SHORTCUT.bat** (Windows)
- Creates desktop shortcut to launcher

**activate_venv.sh / activate_venv.ps1**
- Auto-activate venv when entering directory
- Optional - for development workflow

**tuner_daemon.py**
- Background daemon mode
- Auto-starts tuning on robot connection