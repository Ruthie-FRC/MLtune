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

### 3. Check Tuner Status (Optional)

If you need to check tuner status or implement shooting interlocks:

```java
// In RobotContainer or subsystem
private TunerInterface tuner = TunerInterface.getInstance();

// Check if tuner is connected
if (tuner.isTunerConnected()) {
    // Tuner is running
}

// Check if shooting is allowed based on interlocks
if (tuner.canShoot()) {
    // Safe to shoot
}
```

### 4. Log Shot Results

In your shooter or firing solution subsystem, log shot results after each attempt. See `FiringSolutionSolver.java` for a complete example:

```java
public void logShot(boolean hit, double distanceMeters, 
                   double pitchRadians, double exitVelocityMps, 
                   double yawRadians) {
    // Publish to NetworkTables for tuner
    m_shotTimestampPub.set(Timer.getFPGATimestamp());
    m_hitPub.set(hit);
    m_distancePub.set(distanceMeters);
    m_pitchPub.set(pitchRadians);
    m_velocityPub.set(exitVelocityMps);
    m_yawPub.set(yawRadians);
    // Also publish current coefficient values
}
```

## System Behavior

The tuner performs the following operations:
- Reads shot data from NetworkTables
- Applies Bayesian optimization to determine optimal coefficients
- Publishes updated values to NetworkTables
- Maintains logs for analysis

## Example Implementation

See `FiringSolutionSolver.java` for a complete example. Here's a simplified version:

```java
public class Shooter extends SubsystemBase {
    private static LoggedTunableNumber kV = 
        new LoggedTunableNumber("Shooter/kV", 0.12);
    private static LoggedTunableNumber kS = 
        new LoggedTunableNumber("Shooter/kS", 0.5);
    
    // NetworkTables publishers for shot data
    private final BooleanPublisher m_hitPub;
    private final DoublePublisher m_distancePub;
    // ... other publishers
    
    public Shooter() {
        NetworkTable shotTable = NetworkTableInstance.getDefault().getTable("Shooter");
        m_hitPub = shotTable.getBooleanTopic("Hit").publish();
        m_distancePub = shotTable.getDoubleTopic("Distance").publish();
        // Initialize other publishers
    }
    
    public void shoot(double distance, double angle) {
        double velocity = calculateVelocity(distance, angle);
        setVelocity(velocity);
        
        // Wait for shot completion...
        
        boolean hit = checkIfScored();
        logShot(hit, distance, angle, velocity);
    }
    
    private void logShot(boolean hit, double distance, double angle, double velocity) {
        m_hitPub.set(hit);
        m_distancePub.set(distance);
        // Publish other shot data to NetworkTables
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
- Verify `TunerEnabled` is set to true in NetworkTables
- Check tuner application logs
- Ensure LoggedTunableNumber values are being read with `.get()`

**Shot data not received:**
- Verify `logShot()` calls are executed
- Check dashboard for recent shot entries
- Review driver station logs for errors