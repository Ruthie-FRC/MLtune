# Robot Integration

## Overview

Integration requires copying Java files from the `java-integration/` directory into your robot project. These files provide the NetworkTables interface required for communication with the tuning system.

**For detailed communication protocol, see: [PYTHON_JAVA_COMMUNICATION.md](PYTHON_JAVA_COMMUNICATION.md)**

## Quick Start

See **[MinimalShooterExample.java](../java-integration/MinimalShooterExample.java)** for a complete, annotated example showing the integration pattern.

See **[minimal_tuner_example.py](../scripts/minimal_tuner_example.py)** for a Python-side example.

## Required Files

**TunerInterface.java**
- Manages NetworkTables communication
- Logs shot data (distance, angle, hit/miss)
- Receives coefficient updates from tuner

**LoggedTunableNumber.java**
- Wrapper class for tunable parameters
- Provides NetworkTables integration
- Logs value changes automatically

Additional files (FiringSolutionSolver.java, Constants_Addition.java) are example implementations.

## Integration Steps

### 1. Add Files to Project

Place `TunerInterface.java` and `LoggedTunableNumber.java` in your robot code package:
```
src/main/java-integration/frc/robot/tuning/
```

### 2. Replace Static Constants

**Before:**
```java
private static final double K1 = 0.5;
private static final double K2 = 1.0;
```

**After:**
```java
private static LoggedTunableNumber k1 = 
    new LoggedTunableNumber("k1", 0.5);
private static LoggedTunableNumber k2 = 
    new LoggedTunableNumber("k2", 1.0);

// Access values using get()
double value = k1.get();
```

### 3. Initialize Tuner Interface

In `RobotContainer` or `Robot` class:

```java
private TunerInterface tuner;

public RobotContainer() {
    tuner = new TunerInterface();
    // Additional initialization...
}
```

### 4. Log Shot Results

After each shot attempt:

```java
tuner.logShot(distance, angle, didHit);
```

Parameters:
- `distance` - Distance to target (meters)
- `angle` - Angle to target (degrees)
- `didHit` - Boolean indicating shot success

### 5. Periodic Updates

In `robotPeriodic()`:

```java
@Override
public void robotPeriodic() {
    tuner.periodic();
}
```

## System Behavior

The tuner performs the following operations:
- Reads shot data from NetworkTables
- Applies Bayesian optimization to determine optimal coefficients
- Publishes updated values to NetworkTables
- Maintains logs for analysis

## Example Implementation

```java
public class Shooter extends SubsystemBase {
    private static LoggedTunableNumber kV = 
        new LoggedTunableNumber("Shooter/kV", 0.12);
    private static LoggedTunableNumber kS = 
        new LoggedTunableNumber("Shooter/kS", 0.5);
    
    private TunerInterface tuner;
    
    public Shooter() {
        tuner = TunerInterface.getInstance();
    }
    
    public void shoot(double distance, double angle) {
        double velocity = calculateVelocity(distance, angle);
        setVelocity(velocity);
        
        // Wait for shot completion...
        
        boolean hit = checkIfScored();
        tuner.logShot(distance, angle, hit);
    }
    
    private double calculateVelocity(double distance, double angle) {
        return kV.get() * distance + kS.get();
    }
}
```

## NetworkTables Structure

The system uses the following NetworkTables hierarchy:

```
/Tuning/BayesianTuner/
  ├── TunerEnabled (boolean)
  ├── Coefficients/
  │   ├── k1 (double)
  │   ├── k2 (double)
  │   └── ...
  └── ShotData/
      ├── Distance (double)
      ├── Angle (double)
      ├── Hit (boolean)
      └── ShotLogged (boolean)
```

The interface classes handle NetworkTables interaction automatically.

## Testing the Integration

### 1. Test NetworkTables Communication

Run the integration test script to verify Python-Java communication:

```bash
cd MLtune
python scripts/test_integration.py
```

This tests:
- NetworkTables connection
- Heartbeat mechanism
- Coefficient read/write paths
- Interlock signaling
- Status publishing

### 2. Manual Testing

**Test coefficient updates:**
1. Start your robot code with tuning mode enabled
2. Use NetworkTables viewer (e.g., OutlineViewer) to manually change a coefficient value at `/Tuning/DragCoefficient`
3. Verify the robot code picks up the new value

**Test shot logging:**
1. Start the minimal Python tuner: `python scripts/minimal_tuner_example.py`
2. Trigger a shot from the robot
3. Verify the Python tuner receives and logs the shot data

**Test connection detection:**
1. Start robot code
2. Start Python tuner
3. Check that `TunerInterface.isTunerConnected()` returns `true` in Java
4. Stop Python tuner
5. Verify `isTunerConnected()` returns `false` after ~5 seconds

## Recommendations

- Test coefficient updates manually via NetworkTables before enabling automatic tuning
- Verify shot detection reliability before automated optimization
- Use wide parameter bounds initially in tuner configuration
- Collect minimum 10 shots per coefficient for meaningful optimization
- Preserve working coefficients before experimental tuning sessions

## Troubleshooting

**Tuner shows disconnected:**
- Verify NetworkTables is operational
- Check team number matches in robot and tuner configurations
- Ensure Python tuner is calling `publish_heartbeat()` regularly (every 1-2 seconds)
- Check firewall settings aren't blocking NetworkTables port (1735)

**Coefficients not updating:**
- Verify `TunerEnabled` is set to true
- Confirm `periodic()` is called in robot loop
- Check tuner application logs
- Verify coefficient names match between Java and Python (case-sensitive)
- Use OutlineViewer to inspect NetworkTables structure and verify paths

**Shot data not received:**
- Verify `logShot()` calls are executed after each shot
- Check that `ShotTimestamp` is being updated in NetworkTables
- Ensure all required shot data fields are being published
- Review driver station logs for errors
- Check Python tuner is monitoring the correct table (`/FiringSolver/`)

**Java can't read coefficient updates from Python:**
- Verify paths match: Java uses `/Tuning/{CoeffName}`, Python writes to same path
- Check that `Constants.tuningMode` is `true` in Java
- Ensure LoggedTunableNumber is calling `.get()` to read current value
- Use OutlineViewer to verify values are actually being written

**Python can't read shot data from Java:**
- Verify Java is publishing to `/FiringSolver/` table
- Check that `ShotTimestamp` is being updated (triggers Python to read)
- Ensure all required fields are published (Hit, Distance, Solution/pitchRadians, etc.)
- Check Python logs for any read errors or validation failures

For detailed communication protocol, see [PYTHON_JAVA_COMMUNICATION.md](PYTHON_JAVA_COMMUNICATION.md)