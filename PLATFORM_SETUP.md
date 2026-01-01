# Platform-Specific Setup Guide

This guide provides detailed setup instructions for each supported platform.

## Windows Setup

### Prerequisites
1. **Python 3.8 or newer**: Download from [python.org](https://python.org)
   - ✅ Check "Add Python to PATH" during installation
   - Verify: Open Command Prompt and run `python --version`

2. **VS Code** (optional but recommended): Download from [code.visualstudio.com](https://code.visualstudio.com)

### Quick Start
1. Double-click `START.bat` in the project folder
2. The script will automatically:
   - Create a Python virtual environment
   - Install all dependencies
   - Launch the dashboard
3. Your browser will open to `http://localhost:8050`

### VS Code Setup
1. Open the project folder in VS Code
2. Install the Python extension (if prompted)
3. Open a new terminal (Ctrl+`)
4. The virtual environment will activate automatically
5. Press F5 to run the dashboard with debugging

### Troubleshooting
- **"Python not found"**: Reinstall Python and check "Add to PATH"
- **Execution policy error**: Run PowerShell as admin:
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```

---

## Chromebook Setup (Linux Mode)

### Prerequisites
1. **Enable Linux**: Settings → Advanced → Developers → Turn on Linux
2. **Install Python**:
   ```bash
   sudo apt update
   sudo apt install python3 python3-venv python3-pip git
   ```
3. **VS Code** (optional): Install from Linux apps or download .deb from [code.visualstudio.com](https://code.visualstudio.com)

### Quick Start
1. Open Terminal (Linux)
2. Navigate to project:
   ```bash
   cd /path/to/MLtune
   ```
3. Make script executable:
   ```bash
   chmod +x START.sh
   ```
4. Run the launcher:
   ```bash
   ./START.sh
   ```
5. Open browser to `http://localhost:8050`

### VS Code Setup
1. Open Terminal in VS Code (Ctrl+`)
2. The virtual environment activates automatically
3. Press F5 to run with debugging

### Chromebook-Specific Tips
- **Performance**: Close unnecessary tabs for better performance
- **Storage**: Linux container has limited storage (check available space)
- **Network**: Dashboard runs locally, no internet needed once installed
- **Browser**: Use Chrome (built-in) for best compatibility

### Troubleshooting
- **"Permission denied"**: Run `chmod +x START.sh` first
- **Python not found**: Run the apt install commands above
- **Out of space**: Increase Linux container size in Settings
- **Can't access localhost**: Use `127.0.0.1:8050` instead

---

## Mac Setup

### Prerequisites
1. **Python 3.8+**: Usually pre-installed, or use:
   ```bash
   brew install python3
   ```
2. **VS Code** (optional): Download from [code.visualstudio.com](https://code.visualstudio.com)

### Quick Start
1. Open Terminal
2. Navigate to project:
   ```bash
   cd /path/to/MLtune
   ```
3. Make script executable:
   ```bash
   chmod +x START.sh
   ```
4. Run:
   ```bash
   ./START.sh
   ```

### VS Code Setup
Same as Linux/Chromebook above.

---

## VS Code Extensions (All Platforms)

### Recommended
- **Python** (ms-python.python) - Essential for Python development
- **Pylance** (ms-python.vscode-pylance) - Enhanced Python IntelliSense

### Optional
- **Python Debugger** - Advanced debugging features
- **GitLens** - Enhanced Git integration
- **Error Lens** - Inline error highlighting

Install via: `Ctrl+Shift+X` → Search → Install

---

## Common Issues & Solutions

### All Platforms

**Dashboard won't start**
1. Check Python version: `python --version` (or `python3 --version`)
2. Recreate virtual environment:
   ```bash
   rm -rf .venv
   # Then run START.bat or START.sh again
   ```

**Browser doesn't open automatically**
- Manually navigate to: `http://localhost:8050`

**Port 8050 already in use**
- Close other applications using port 8050
- Or edit `dashboard/__main__.py` to use a different port

### Platform-Specific

**Windows: "Script is not digitally signed"**
```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unrestricted
```

**Chromebook: "No space left on device"**
- Increase Linux storage: Settings → Linux → Disk size
- Clean up: `sudo apt clean && sudo apt autoremove`

**Mac: "Command not found: python"**
- Use `python3` instead of `python`
- Or create alias: `alias python=python3`

---

## Getting Help

1. Check this guide first
2. Review README.md in project root
3. Check VS Code's Python extension output
4. Verify virtual environment is activated (you should see `(.venv)` in terminal)

---

**Last Updated**: January 2026
