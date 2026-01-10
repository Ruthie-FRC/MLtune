#!/usr/bin/env python3
"""
MLTUNE Dashboard Launcher
Copyright (C) 2025 Ruthie-FRC

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

------------------------------------------------------

Entry point for running the MLtune dashboard.

Usage:
    python3 app.py
"""

import sys
import os
import webbrowser
import threading
import time

# Add the project root to the path so we can import from dashboard
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def open_browser():
    """Open browser after a short delay to ensure server is ready."""
    time.sleep(1.5)
    webbrowser.open('http://localhost:8050')

if __name__ == '__main__':
    # Import the dashboard app
    from dashboard.app import app, TUNER_AVAILABLE
    
    print("=" * 60)
    print("MLtune Dashboard Starting")
    print("=" * 60)
    print(f"Opening browser to: http://localhost:8050")
    print("=" * 60)
    print(f"Tuner integration: {'Available' if TUNER_AVAILABLE else 'Demo mode'}")
    print("=" * 60)
    
    # Open browser in background thread
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Use debug mode only in development, not in production
    debug_mode = os.environ.get('DASH_DEBUG', 'false').lower() == 'true'
    app.run(debug=debug_mode, host='0.0.0.0', port=8050)
