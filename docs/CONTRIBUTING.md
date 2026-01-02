# Contributing

## Setup

```bash
git clone https://github.com/Ruthie-FRC/MLtune.git
cd MLtune
python3 -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r src/mltune/tuner/requirements.txt
pip install -r src/dashboard/requirements.txt
```

## Project Structure

```
src/
├── mltune/
│   ├── tuner/          # Core tuning logic
│   │   ├── config.py   # Config loading
│   │   ├── tuner.py    # Main coordinator
│   │   ├── optimizer.py # Bayesian optimization
│   │   ├── nt_interface.py # NetworkTables
│   │   └── gui.py      # Desktop GUI
│   └── config/         # User config files
└── dashboard/          # Web dashboard (Dash/Plotly)
```

## Making Changes

### Code Style

We don't enforce strict style rules, but:
- Keep it readable
- Match surrounding code
- Add docstrings for non-obvious functions
- Don't over-engineer

### Testing

We don't have automated tests yet (PRs welcome). For now:
- Actually run your changes
- Test with a real robot if possible
- Check both GUI and dashboard work

### Documentation

Keep docs concise and useful. Assume competence - nobody wants hand-holding.

## Pull Requests

1. Fork the repo
2. Make your changes
3. Test them
4. Open a PR with a clear description

We'll review and merge if it makes sense.

## Architecture Notes

### Tuner Flow

1. `tuner.py` coordinates everything
2. `nt_interface.py` handles robot communication
3. `optimizer.py` does the Bayesian optimization math
4. `config.py` loads user settings
5. `gui.py` and `dashboard/` provide interfaces

### Key Design Decisions

**Why Bayesian optimization?**
- Sample-efficient (important for robot tuning)
- Handles noisy data well
- No gradients needed

**Why scikit-optimize?**
- Stable, well-tested
- Easy to use
- Good enough performance

**Why separate GUI and dashboard?**
- GUI for drivers (simple, always-on)
- Dashboard for engineers (detailed, optional)

**Why NetworkTables?**
- Standard in FRC
- Works out of the box with WPILib
- Real-time, low latency

### What Could Be Better

- Add automated tests
- Support for more optimization algorithms
- Better visualization of optimization history
- Config validation and helpful error messages
- Multi-robot support

Feel free to work on any of these.

## Common Dev Tasks

### Run the tuner locally

```bash
python -m src.mltune.tuner.gui
```

### Run the dashboard locally

```bash
python -m src.dashboard.app
```

### Test without a robot

The system falls back to a simulated mode if NetworkTables isn't available. You can test basic functionality without hardware.

### Add a new coefficient

Edit `src/mltune/config/COEFFICIENT_TUNING.py`:

```python
COEFFICIENTS = [
    {
        'name': 'your_coeff',
        'bounds': (min_value, max_value),
        'initial': starting_value
    }
]
```

### Modify the optimization algorithm

Look in `src/mltune/tuner/optimizer.py`. The `BayesianOptimizer` class wraps scikit-optimize. Swap it out if you want a different approach.

## Questions?

Open an issue. We'll help.
