# Usage Guide

## Config Files

Everything's in `src/mltune/config/`:

**COEFFICIENT_TUNING.py** - Define what you're tuning:
```python
COEFFICIENTS = [
    {
        'name': 'k1',
        'bounds': (0.0, 1.0),
        'initial': 0.5
    },
    # ... more coefficients
]
```

**TUNER_TOGGLES.ini** - Control behavior:
```ini
[tuning]
autotune_enabled = False          # Auto-optimize after each shot
auto_advance_on_success = False   # Auto-advance to next coefficient
shot_threshold = 10               # Shots needed before optimizing

[network]
team_number = 1234
server_ip = 10.12.34.2
```

## Basic Workflow

1. Start the tuner (see GETTING_STARTED.md)
2. Enable tuning via dashboard toggle
3. Shoot and provide hit/miss feedback
4. Press "Optimize" when you have enough data
5. Check if the new coefficients work better
6. Move to next coefficient when satisfied

## Manual vs Auto Mode

**Manual mode** (recommended):
- You control when to optimize
- You control when to advance to next coefficient
- Set both toggles to `False` in config

**Auto mode**:
- Optimizes automatically after N shots
- Advances automatically on success
- Set toggles to `True` in config

## Hotkeys

The tuner registers global hotkeys (may need admin/root):

- `Ctrl+Alt+R` - Run optimization
- `Ctrl+Alt+N` - Next coefficient
- `Ctrl+Alt+S` - Start/stop tuning

If hotkeys don't work, just use the dashboard or GUI buttons.

## Dashboard

Open http://localhost:8050 for the web interface. You can:

- Toggle tuning on/off
- View current coefficient values
- See optimization history
- Run optimization manually
- Skip to next coefficient
- View logs and shot data

The dashboard auto-updates when the robot sends new data.

## Common Issues

**"Disconnected" status:**
- Check robot is on
- Verify team number in config
- Make sure you're on the robot network

**Hotkeys not working:**
- Run with admin/sudo
- Or just use the dashboard instead
- The `keyboard` library can be finicky

**Import errors:**
- Make sure you ran the start script
- If not, manually install: `pip install -r src/mltune/tuner/requirements.txt`

**Optimization takes forever:**
- Lower your shot threshold
- Check that shot data is actually being logged
- View logs to see what's happening

## Tips

- Start with wide bounds, narrow them down after initial tuning
- More shots = better optimization, but diminishing returns after ~20
- Watch the logs - they tell you everything that's happening
- The dashboard is more reliable than hotkeys on most systems
- Back up your tuned coefficients before resetting

## Logs

Logs go to `tuner_logs/` with timestamps. Check them if something seems wrong.
