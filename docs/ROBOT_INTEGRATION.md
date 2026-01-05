# Robot Integration

## Overview

Copy Java files from `java-integration/` to your robot project for NetworkTables communication with the tuner.

## Required Files

**TunerInterface.java** - NetworkTables communication, reads tuner status and interlocks

**LoggedTunableNumber.java** - Wraps tunable parameters, publishes to NetworkTables

Example files: FiringSolutionSolver.java, Constants_Addition.java

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

Check tuner status or implement shooting interlocks:

```java
// In RobotContainer or subsystem
private TunerInterface tuner = TunerInterface.getInstance();

if (tuner.isTunerConnected()) {
    // Tuner running
}

if (tuner.canShoot()) {
    // Interlocks satisfied
}
```

### 4. Log Shot Results

Log shot results after each attempt. See `FiringSolutionSolver.java` for complete example:

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

The tuner:
- Reads shot data from NetworkTables
- Applies Bayesian optimization
- Publishes updated coefficient values to NetworkTables

## Example Implementation

See `FiringSolutionSolver.java` for complete example. Simplified version:

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

Interface classes handle NetworkTables interaction.

## Recommendations

- Test coefficient updates manually via NetworkTables first
- Verify shot detection works before enabling auto-tuning
- Start with wide parameter bounds
- Collect 10+ shots per coefficient minimum
- Back up working coefficients before tuning

## Troubleshooting

**Tuner disconnected:**
- Check NetworkTables operational
- Verify team number matches

**Coefficients not updating:**
- Set `TunerEnabled` to true in NetworkTables
- Check tuner logs
- Verify LoggedTunableNumber values read with `.get()`

**Shot data not received:**
- Verify `logShot()` is called
- Check dashboard for shot entries
- Review logs for errors