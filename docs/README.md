# MLtune Documentation

## Quick Links

- [Getting Started](GETTING_STARTED.md) - Install and run
- [Usage Guide](USAGE.md) - Use the tuner
- [Robot Integration](INTEGRATION.md) - Add to your robot code
- [Contributing](CONTRIBUTING.md) - Develop and contribute

## What is this?

MLtune uses Bayesian optimization to automatically tune your robot's shooter parameters. You shoot, tell it if you hit or missed, and it figures out better coefficients. That's it.

## Requirements

- Python 3.8+
- Your robot running WPILib 2024+
- NetworkTables connection between your laptop and robot

## The 30 Second Version

```bash
# Clone and run
git clone https://github.com/Ruthie-FRC/MLtune.git
cd MLtune
scripts/START.sh  # or START.bat on Windows

# In another terminal, configure and tune
# See USAGE.md for details
```

That's it. See the guides for more details.
