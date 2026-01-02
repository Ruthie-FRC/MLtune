# Robot Integration

## Overview

Copy the Java files from `java/` into your robot project. These provide the NetworkTables interface that the tuner needs.

## Files You Need

**TunerInterface.java** - Main interface class
- Handles NetworkTables communication
- Logs shot data (distance, angle, hit/miss)
- Receives updated coefficients from tuner

**LoggedTunableNumber.java** - Wrapper for tunable values
- Makes any number tunable via NetworkTables
- Logs value changes automatically
- Drop-in replacement for constants

The other files are examples - use them if they match your setup, ignore otherwise.

## Basic Integration

### 1. Add the Files

Put `TunerInterface.java` and `LoggedTunableNumber.java` in your robot code package, e.g.:
```
src/main/java/frc/robot/tuning/
```

### 2. Replace Your Constants

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

// Use .get() to read values
double value = k1.get();
```

### 3. Initialize the Tuner Interface

In your `RobotContainer` or main `Robot` class:

```java
private TunerInterface tuner;

public RobotContainer() {
    tuner = new TunerInterface();
    // ... rest of your init code
}
```

### 4. Log Shot Data

After each shot, call:

```java
tuner.logShot(distance, angle, didHit);
```

Where:
- `distance` - Distance to target in meters
- `angle` - Angle to target in degrees
- `didHit` - `true` if scored, `false` if missed

### 5. Periodic Updates

In `robotPeriodic()`:

```java
@Override
public void robotPeriodic() {
    tuner.periodic();  // Updates coefficients from NetworkTables
}
```

## That's It

The tuner will:
- Read your shot data via NetworkTables
- Optimize coefficients using Bayesian optimization
- Push updated values back to the robot
- Log everything for review

## Example: Shooter Subsystem

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
        // Calculate and shoot
        double velocity = calculateVelocity(distance, angle);
        setVelocity(velocity);
        
        // Wait for shot to complete...
        
        // Log the result
        boolean hit = checkIfScored();  // Your detection logic
        tuner.logShot(distance, angle, hit);
    }
    
    private double calculateVelocity(double distance, double angle) {
        // Use the tunable coefficients
        return kV.get() * distance + kS.get();
    }
}
```

## NetworkTables Structure

The tuner uses these NT keys:

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

You don't need to touch these directly - the interface handles it.

## Tips

- Test with manual coefficient changes first (via NetworkTables or dashboard)
- Make sure your hit detection is reliable before auto-tuning
- Start with wide bounds in the tuner config
- Log at least 10 shots per coefficient for good results
- Back up coefficients that work before experimenting

## Troubleshooting

**Tuner shows disconnected:**
- Check NetworkTables is running
- Verify team number matches in both robot and tuner config

**Coefficients not updating:**
- Check `TunerEnabled` is true
- Make sure `periodic()` is being called
- Look at the tuner logs

**Shot data not received:**
- Verify you're calling `logShot()`
- Check the dashboard shows recent shots
- Look for errors in driver station logs
