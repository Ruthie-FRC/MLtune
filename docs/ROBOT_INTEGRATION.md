# Robot Integration

## Overview

Integration requires copying Java files from the `java-integration/` directory into your robot project. These files provide the NetworkTables interface required for communication with the tuning system.

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

**Coefficients not updating:**
- Verify `TunerEnabled` is set to true
- Confirm `periodic()` is called in robot loop
- Check tuner application logs

**Shot data not received:**
- Verify `logShot()` calls are executed
- Check dashboard for recent shot entries
- Review driver station logs for errors