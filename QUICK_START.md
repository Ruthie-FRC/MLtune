# Quick Start Reference Card

## Launch Commands

### Windows
```cmd
START.bat
```

### Mac / Linux / Chromebook
```bash
./START.sh
```

### VS Code (All Platforms)
Press `F5` or run:
```bash
python -m dashboard.app
```

## Access Dashboard
Open browser to: **http://localhost:8050**

## VS Code Shortcuts
- `F5` - Start with debugging
- `Ctrl+C` - Stop dashboard
- `Ctrl+~` - Toggle terminal
- `Ctrl+Shift+P` - Command palette

## First-Time Setup

### Windows
1. Install Python from python.org (check "Add to PATH")
2. Run `START.bat`

### Chromebook
1. Enable Linux in Settings
2. Install Python: `sudo apt install python3 python3-venv`
3. Run `chmod +x START.sh && ./START.sh`

### Mac
1. Run `chmod +x START.sh && ./START.sh`

## Troubleshooting Quick Fixes

| Problem | Solution |
|---------|----------|
| Python not found | Install Python 3.8+ and add to PATH |
| Permission denied | Run `chmod +x START.sh` (Mac/Linux/Chromebook) |
| Port in use | Close other apps or change port in code |
| VS Code can't find Python | Select interpreter: `Ctrl+Shift+P` → Python: Select Interpreter |

## Need More Help?
See `PLATFORM_SETUP.md` for detailed platform-specific instructions.
