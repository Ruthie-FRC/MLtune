# Python-Java Communication Protocol

## Overview

MLtune uses NetworkTables for bidirectional communication between the Python tuner (running on driver station) and Java robot code (running on RoboRIO). This document describes the complete communication protocol.

## NetworkTables Structure

```
/Tuning/
├── BayesianTuner/              # Tuner control and status
│   ├── Heartbeat               # Python → Java: Timestamp for connection detection
│   ├── TunerEnabled            # Java ↔ Python: Enable/disable toggle
│   ├── TunerPaused             # Python → Java: Paused status
│   ├── TunerRuntimeStatus      # Python → Java: "ACTIVE", "DISABLED", "PAUSED"
│   ├── CurrentCoefficient      # Python → Java: Name of coefficient being tuned
│   ├── ShotCount               # Python → Java: Accumulated shots
│   ├── ShotThreshold           # Python → Java: Shots needed for optimization
│   ├── AutotuneEnabled         # Python → Java: Autotune mode status
│   ├── RunOptimization         # Java → Python: Manual optimization trigger button
│   ├── SkipToNextCoefficient   # Java → Python: Skip to next coefficient button
│   └── ...
├── DragCoefficient             # Java ↔ Python: Coefficient value
├── AirDensity                  # Java ↔ Python: Coefficient value
├── ProjectileMass              # Java ↔ Python: Coefficient value
├── ProjectileArea              # Java ↔ Python: Coefficient value
└── ... (other coefficients)

/FiringSolver/                  # Shot data and interlocks
├── ShotTimestamp               # Java → Python: When shot occurred
├── Hit                         # Java → Python: Shot result (true/false)
├── Distance                    # Java → Python: Distance to target (m)
├── TargetHeight                # Java → Python: Target height (m)
├── LaunchHeight                # Java → Python: Launch height (m)
├── DragCoefficient             # Java → Python: Drag coeff at shot time
├── AirDensity                  # Java → Python: Air density at shot time
├── ProjectileMass              # Java → Python: Mass at shot time
├── ProjectileArea              # Java → Python: Area at shot time
├── Solution/                   # Firing solution used
│   ├── pitchRadians            # Java → Python: Pitch angle
│   ├── exitVelocity            # Java → Python: Exit velocity (m/s)
│   └── yawRadians              # Java → Python: Yaw angle
└── Interlock/                  # Shot interlocks for safety
    ├── RequireShotLogged       # Python → Java: Enable shot logging interlock
    ├── RequireCoefficientsUpdated # Python → Java: Enable coeff update interlock
    ├── ShotLogged              # Python → Java: Shot has been logged (cleared by Java)
    └── CoefficientsUpdated     # Python → Java: Coeffs updated (cleared by Java)
```

## Communication Flow

### 1. Connection Detection

**Java → Python:**
- Java reads `/Tuning/BayesianTuner/Heartbeat` timestamp
- If `(currentTime - heartbeat) < 5.0` seconds, tuner is connected
- Java method: `TunerInterface.isTunerConnected()`

**Python → Java:**
- Python publishes current timestamp to `/Tuning/BayesianTuner/Heartbeat` every 1-2 seconds
- Python method: `NetworkTablesInterface.publish_heartbeat()`

### 2. Coefficient Tuning

**Java → Python (Read Coefficients):**
- Java uses `LoggedTunableNumber` which creates entries at `/Tuning/{CoeffName}`
- Example: `new LoggedTunableNumber("DragCoefficient", 0.47)` creates `/Tuning/DragCoefficient`
- Java reads updated values automatically through LoggedTunableNumber

**Python → Java (Write Coefficients):**
- Python writes optimized values to `/Tuning/{CoeffName}`
- Python method: `NetworkTablesInterface.write_coefficient(nt_key, value)`
- Rate limited to prevent RoboRIO overload (default: 10 Hz)

### 3. Shot Data Logging

**Java → Python:**
1. Java calculates firing solution (distance, angle, velocity)
2. Java shoots and detects result (hit/miss)
3. Java publishes complete shot data to `/FiringSolver/`
   - Shot result, solution used, current coefficient values
   - Java method: `FiringSolver.logShot(hit, distance, pitch, velocity, yaw)`
4. Java updates `ShotTimestamp` to signal new data

**Python → Java:**
1. Python monitors `ShotTimestamp` for changes
2. When new timestamp detected, Python reads all shot data
3. Python method: `NetworkTablesInterface.read_shot_data()` returns `ShotData` object
4. Python adds shot to optimization dataset

### 4. Optimization Triggering

**Manual Mode (autotune disabled):**
- Java: Driver presses `RunOptimization` button on dashboard
- Python: Reads button state with `read_run_optimization_button()`
- Python: Runs optimization when button pressed
- Python: Resets button to false after reading

**Automatic Mode (autotune enabled):**
- Python: Automatically triggers when `ShotCount >= ShotThreshold`
- Python: Updates `ShotCount` as shots accumulate
- Java: Can monitor progress via `TunerInterface.getShotCount()`

### 5. Shooting Interlocks (Optional Safety Feature)

Interlocks ensure the robot waits for the tuner before shooting.

**Shot Logging Interlock:**
1. Python enables: `write_interlock_settings(require_shot_logged=True, ...)`
2. Java checks: `TunerInterface.isShootingAllowed()` returns false
3. Java clears flag before shot: `clearShotLoggedFlag()` sets `ShotLogged=false`
4. Java shoots
5. Python logs shot
6. Python signals: `signal_shot_logged()` sets `ShotLogged=true`
7. Java can shoot again

**Coefficient Update Interlock:**
1. Python enables: `write_interlock_settings(..., require_coefficients_updated=True)`
2. Python optimizes and writes new coefficients
3. Python signals: `signal_coefficients_updated()` sets `CoefficientsUpdated=true`
4. Java checks: `TunerInterface.isShootingAllowed()` now returns true
5. Java clears flag after reading: `clearCoefficientsUpdatedFlag()`

### 6. Status and Monitoring

**Python → Java:**
- Tuner status: `write_tuner_enabled_status(enabled, paused)`
- Autotune info: `write_autotune_status(enabled, shot_count, threshold)`
- Current coefficient: `write_current_coefficient_info(name, autotune, threshold, auto_advance)`

**Java → Python:**
- Runtime enable/disable: Java reads/writes `TunerEnabled` toggle
- Python monitors: `read_tuner_enabled_toggle()`

## Java Integration (Required Files)

### 1. LoggedTunableNumber.java
- Location: `src/main/java/frc/robot/util/LoggedTunableNumber.java`
- Purpose: Wraps coefficient values with NetworkTables integration
- Usage:
```java
private static LoggedTunableNumber dragCoeff = 
    new LoggedTunableNumber("DragCoefficient", 0.47);

double value = dragCoeff.get();  // Read current value (from NT or default)
```

### 2. TunerInterface.java
- Location: `src/main/java/frc/robot/util/TunerInterface.java`
- Purpose: Check tuner connection and status
- Usage:
```java
TunerInterface tuner = TunerInterface.getInstance();

if (tuner.isTunerConnected()) {
    // Tuner is running
}

if (tuner.isShootingAllowed()) {
    // Safe to shoot (interlocks satisfied)
}

String currentCoeff = tuner.getCurrentCoefficient();
int shotCount = tuner.getShotCount();
```

### 3. FiringSolutionSolver.java (Example)
- Location: `src/main/java/frc/robot/subsystems/FiringSolutionSolver.java`
- Purpose: Example implementation showing how to log shots
- Usage:
```java
FiringSolver solver = new FiringSolver();

// Calculate solution
FiringSolution solution = solver.calculate(distance, targetHeight, launchHeight);

// Execute shot
shooter.shoot(solution.getPitchRadians(), solution.getExitVelocityMps());

// After shot completes, log the result
boolean hit = detectHit();
solver.logShot(hit, distance, solution.getPitchRadians(), 
               solution.getExitVelocityMps(), solution.getYawRadians(),
               targetHeight, launchHeight);
```

## Python Integration

### Starting the Tuner
```python
from MLtune.tuner.nt_interface import NetworkTablesInterface
from MLtune.tuner.config import TunerConfig

config = TunerConfig()
nt = NetworkTablesInterface(config)

# Connect to robot
if nt.start(server_ip="10.TE.AM.2"):  # Replace with your team number
    print("Connected to robot")
    
    # Publish heartbeat periodically
    while True:
        nt.publish_heartbeat()
        
        # Read shot data
        shot = nt.read_shot_data()
        if shot:
            print(f"New shot: hit={shot.hit}, distance={shot.distance}")
            nt.signal_shot_logged()  # Signal we logged it
        
        time.sleep(1)
```

## Rate Limiting

To prevent overloading the RoboRIO, the Python tuner implements rate limiting:

- **Write rate limit**: Default 10 Hz (configurable via `MAX_NT_WRITE_RATE_HZ`)
- **Read rate limit**: Default 20 Hz (configurable via `MAX_NT_READ_RATE_HZ`)
- **Heartbeat rate limit**: Minimum 0.5 seconds between heartbeats (internal)
- **Connection retry delay**: 5 seconds between connection attempts

### Configuration

Rate limits can be configured in `MLtune/config/COEFFICIENT_TUNING.py`:

```python
# RoboRIO Protection - Rate limits for NetworkTables
MAX_WRITE_RATE_HZ = 5.0    # Max coefficient updates per second
MAX_READ_RATE_HZ = 20.0    # Max shot data reads per second
BATCH_WRITES = True        # Batch multiple writes together
```

Or set them directly in your TunerConfig:
```python
config = TunerConfig()
config.MAX_NT_WRITE_RATE_HZ = 5.0  # Slower for older RoboRIOs
config.MAX_NT_READ_RATE_HZ = 10.0  # Reduce if seeing network congestion
```

Bypass rate limiting with `write_coefficient(key, value, force=True)` if needed.

## Testing Communication

Run the integration test script to verify communication:

```bash
python scripts/test_integration.py
```

This tests:
1. NetworkTables connection
2. Heartbeat publishing
3. Coefficient read/write paths
4. Interlock signaling
5. Status publishing
6. Shot data reading

## Troubleshooting

### Tuner shows disconnected in Java
- Check that Python tuner is running
- Verify `publish_heartbeat()` is being called regularly
- Check NetworkTables connection (firewall, team number)

### Coefficients not updating in Java
- Verify tuner is writing to correct path: `/Tuning/{CoeffName}`
- Check that Java `Constants.tuningMode` is `true`
- Verify Java is calling `.get()` on LoggedTunableNumber

### Shot data not received by Python
- Check Java is calling `logShot()` after each shot
- Verify Java is updating `ShotTimestamp`
- Check Python is monitoring correct table: `/FiringSolver/`

### Interlocks blocking shots
- Check interlock settings: `RequireShotLogged`, `RequireCoefficientsUpdated`
- Verify Python is calling `signal_shot_logged()` and `signal_coefficients_updated()`
- Check Java is calling `clearShotLoggedFlag()` and `clearCoefficientsUpdatedFlag()`

## Example Complete Workflow

1. **Initialization:**
   - Java: Start robot code with tuning mode enabled
   - Python: Start tuner and connect to robot NetworkTables
   - Python: Publish heartbeat every second

2. **Shot Cycle:**
   - Java: Calculate firing solution using current coefficients
   - Java: Check `isShootingAllowed()` (if using interlocks)
   - Java: Clear `ShotLogged` flag
   - Java: Execute shot
   - Java: Detect hit/miss result
   - Java: Call `logShot()` with all data
   - Python: Detect new `ShotTimestamp`
   - Python: Read and validate shot data
   - Python: Add to optimization dataset
   - Python: Call `signal_shot_logged()`
   - Python: Increment shot count

3. **Optimization:**
   - Python: Check if `ShotCount >= ShotThreshold` (autotune) or button pressed (manual)
   - Python: Run Bayesian optimization
   - Python: Write updated coefficients to NetworkTables
   - Python: Call `signal_coefficients_updated()`
   - Java: LoggedTunableNumber automatically picks up new values
   - Java: Next shot uses updated coefficients

4. **Monitoring:**
   - Java: Check `getCurrentCoefficient()` to see what's being tuned
   - Java: Check `getShotCount()` to see progress
   - Java: Check `isTunerConnected()` to verify tuner is running
