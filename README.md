# MLtune

**Automated Bayesian optimization tuner for FRC robot shooting systems**

MLtune uses machine learning to automatically tune firing solution coefficients like drag coefficient, air density, and solver parameters. It communicates with your robot via NetworkTables, collecting shot data and publishing optimized coefficient values.

## Features

- 🎯 **Automated Coefficient Tuning**: Uses Bayesian optimization to find optimal values
- 🔄 **Real-time Communication**: Bidirectional NetworkTables integration with Java robot code
- 📊 **Dashboard Control**: Manual and automatic tuning modes with live status
- 🔒 **Safety Interlocks**: Optional shot coordination to prevent race conditions
- 📈 **Progress Tracking**: Monitor optimization progress and shot statistics
- 🛡️ **RoboRIO Protection**: Rate limiting prevents network overload

## Quick Start

### Python Side (Driver Station)

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the minimal tuner example:**
   ```bash
   python scripts/minimal_tuner_example.py
   ```

### Java Side (Robot)

1. **Copy required files to your robot project:**
   - `java-integration/TunerInterface.java` → `src/main/java/frc/robot/util/`
   - `java-integration/LoggedTunableNumber.java` → `src/main/java/frc/robot/util/`

2. **Replace static constants with LoggedTunableNumber:**
   ```java
   // Before
   private static final double DRAG_COEFFICIENT = 0.47;
   
   // After
   private static LoggedTunableNumber dragCoefficient = 
       new LoggedTunableNumber("DragCoefficient", 0.47);
   
   // Use with .get()
   double drag = dragCoefficient.get();
   ```

3. **Log shots after firing:**
   ```java
   firingSolver.logShot(hit, distance, pitch, velocity, yaw);
   ```

**See [MinimalShooterExample.java](java-integration/MinimalShooterExample.java) for complete example.**

## Documentation

- **[Robot Integration](docs/ROBOT_INTEGRATION.md)** - How to integrate with your robot code
- **[Python-Java Communication](docs/PYTHON_JAVA_COMMUNICATION.md)** - Complete protocol documentation
- **[Getting Started](docs/GETTING_STARTED.md)** - Installation and setup
- **[Usage Guide](docs/USAGE.md)** - How to use the tuner

## Testing Integration

Verify Python-Java communication:

```bash
python scripts/test_integration.py
```

## Contributing

See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.
