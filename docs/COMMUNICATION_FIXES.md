# Python-Java Communication Fixes

## Summary of Changes

This document summarizes all the fixes made to ensure proper Python-Java communication in MLtune.

## Issues Fixed

### 1. Missing Constant in Java
**Problem**: `FiringSolutionSolver.java` referenced `kDefaultMaxExitVelocity` but it wasn't defined in `Constants_Addition.java`.

**Fix**: Added the missing constant:
```java
public static final double kDefaultMaxExitVelocity = 25.0;
```

**File**: `java-integration/Constants_Addition.java`

---

### 2. No Heartbeat Mechanism
**Problem**: Java's `TunerInterface.isTunerConnected()` checks for a heartbeat timestamp, but Python wasn't publishing it.

**Fix**: Added `publish_heartbeat()` method to Python:
```python
def publish_heartbeat(self):
    """Publish timestamp for Java connection detection."""
    tuner_table.putNumber("Heartbeat", time.time())
```

**File**: `MLtune/tuner/nt_interface.py`

**Usage**: Call `nt.publish_heartbeat()` every 1-2 seconds in main loop.

---

### 3. Missing Shot Logged Signal
**Problem**: Java provides `clearShotLoggedFlag()` for interlocks, but Python had no corresponding `signal_shot_logged()` method.

**Fix**: Added `signal_shot_logged()` method to Python:
```python
def signal_shot_logged(self):
    """Signal that shot has been logged (clears interlock)."""
    interlock_table.putBoolean("ShotLogged", True)
```

**File**: `MLtune/tuner/nt_interface.py`

**Usage**: Call after successfully logging shot data.

---

### 4. NetworkTables Path Mismatch
**Problem**: Python configuration used paths like `/Tuning/FiringSolver/DragCoefficient` but Java creates `/Tuning/DragCoefficient`.

**Fix**: Updated Python configuration to use simple coefficient names:
```python
# Before
"nt_key": "/Tuning/FiringSolver/DragCoefficient"

# After
"nt_key": "DragCoefficient"
```

Python's `write_coefficient()` uses `self.tuning_table` which is already set to `/Tuning`, so it correctly writes to `/Tuning/DragCoefficient`.

**File**: `MLtune/config/COEFFICIENT_TUNING.py`

---

## Documentation Added

### 1. Communication Protocol Documentation
**File**: `docs/PYTHON_JAVA_COMMUNICATION.md`

Complete specification of:
- NetworkTables structure
- Communication flows (connection, coefficients, shots, optimization, interlocks)
- Java integration guide
- Python integration guide
- Troubleshooting

### 2. Integration Test Script
**File**: `scripts/test_integration.py`

Automated tests for:
- ✅ NetworkTables connection
- ✅ Heartbeat publishing
- ✅ Coefficient read/write paths
- ✅ Interlock signals
- ✅ Status publishing
- ⚠️  Shot data reading (requires Java side)

**Usage**: `python scripts/test_integration.py`

### 3. Minimal Python Example
**File**: `scripts/minimal_tuner_example.py`

Shows basic tuner implementation:
- Connect to NetworkTables
- Publish heartbeat
- Monitor shot data
- Write coefficient updates
- Handle dashboard controls

**Usage**: `python scripts/minimal_tuner_example.py`

### 4. Minimal Java Example
**File**: `java-integration/MinimalShooterExample.java`

Shows basic robot integration:
- Create tunable coefficients with `LoggedTunableNumber`
- Check tuner status with `TunerInterface`
- Log shots with all required data
- Use interlocks (optional)

### 5. Updated Documentation
**Files**: 
- `README.md` - Added quick start guide
- `docs/ROBOT_INTEGRATION.md` - Added testing section and better troubleshooting

---

## Verification Checklist

To verify the fixes work correctly:

### Python Side
- [x] `publish_heartbeat()` method exists
- [x] `signal_shot_logged()` method exists
- [x] `signal_coefficients_updated()` method exists
- [x] Coefficient paths use simple names (e.g., "DragCoefficient")
- [x] Integration test script works

### Java Side
- [x] `kDefaultMaxExitVelocity` constant defined
- [x] `TunerInterface.isTunerConnected()` checks heartbeat
- [x] `TunerInterface.clearShotLoggedFlag()` exists
- [x] `LoggedTunableNumber` creates paths at `/Tuning/{name}`
- [x] Minimal example compiles

### Documentation
- [x] Communication protocol documented
- [x] Integration examples provided (Python and Java)
- [x] Testing guide included
- [x] Troubleshooting updated
- [x] README has quick start

---

## Testing the Integration

### 1. Run Integration Test
```bash
cd MLtune
python scripts/test_integration.py
```

Expected output:
```
✓ PASS - Connection
✓ PASS - Heartbeat
✓ PASS - Coefficient Paths
✓ PASS - Interlock Signals
✓ PASS - Status Publishing
⚠ PASS - Shot Data Reading (no data if Java not running)
```

### 2. Test with Robot
1. Deploy Java code with tuning mode enabled
2. Start Python tuner: `python scripts/minimal_tuner_example.py`
3. Verify Java sees connection: `TunerInterface.isTunerConnected()` returns true
4. Fire a shot from robot
5. Verify Python receives shot data
6. Verify coefficient updates work

### 3. Manual Verification
Use OutlineViewer to inspect NetworkTables:
- `/Tuning/BayesianTuner/Heartbeat` updates every second
- `/Tuning/DragCoefficient` (and other coefficients) readable/writable
- `/FiringSolver/ShotTimestamp` updates when shots occur
- `/FiringSolver/Interlock/ShotLogged` toggles correctly

---

## Next Steps for Users

1. **Copy Java files** to robot project:
   - `TunerInterface.java`
   - `LoggedTunableNumber.java`
   - (Optional) `MinimalShooterExample.java` as reference

2. **Replace constants** with `LoggedTunableNumber`:
   ```java
   private static LoggedTunableNumber coeff = 
       new LoggedTunableNumber("CoeffName", defaultValue);
   ```

3. **Log shots** after each firing:
   ```java
   solver.logShot(hit, distance, pitch, velocity, yaw);
   ```

4. **Configure Python** in `MLtune/config/COEFFICIENT_TUNING.py`:
   - Set coefficient ranges
   - Set tuning order
   - Configure autotune settings

5. **Run tuner** on driver station:
   ```bash
   python scripts/minimal_tuner_example.py
   ```

6. **Verify** using integration test:
   ```bash
   python scripts/test_integration.py
   ```

---

## Key Changes by File

| File | Changes |
|------|---------|
| `java-integration/Constants_Addition.java` | Added `kDefaultMaxExitVelocity` constant |
| `MLtune/tuner/nt_interface.py` | Added `publish_heartbeat()` and `signal_shot_logged()` |
| `MLtune/config/COEFFICIENT_TUNING.py` | Fixed NetworkTables paths for all coefficients |
| `docs/PYTHON_JAVA_COMMUNICATION.md` | New: Complete protocol documentation |
| `scripts/test_integration.py` | New: Automated integration tests |
| `scripts/minimal_tuner_example.py` | New: Minimal Python example |
| `java-integration/MinimalShooterExample.java` | New: Minimal Java example |
| `docs/ROBOT_INTEGRATION.md` | Updated: Added testing section and examples |
| `README.md` | Updated: Added quick start and documentation links |

---

## Communication Flow (After Fixes)

```
┌──────────────────────────────────────────┐
│         Python Tuner (Driver Station)    │
│                                          │
│  1. Connect to NetworkTables            │
│  2. Publish heartbeat every second ━━━━━╋━━━> Java checks timestamp
│  3. Write coefficients to /Tuning/X ━━━━╋━━━> Java LoggedTunableNumber reads
│  4. Read shot data from /FiringSolver/ <╋━━━━ Java publishes after each shot
│  5. Signal shot logged ━━━━━━━━━━━━━━━━╋━━━> Java clears interlock
│  6. Signal coefficients updated ━━━━━━━━╋━━━> Java clears interlock
│                                          │
└──────────────────────────────────────────┘
           ▲                           │
           │      NetworkTables        │
           │      (bidirectional)      │
           │                           ▼
┌──────────────────────────────────────────┐
│         Java Robot Code (RoboRIO)        │
│                                          │
│  1. LoggedTunableNumber syncs with NT   │
│  2. Calculate firing solution           │
│  3. Execute shot                        │
│  4. Publish shot data ━━━━━━━━━━━━━━━━>│
│  5. Check tuner connected (heartbeat)   │
│  6. Check interlocks before shooting    │
│                                          │
└──────────────────────────────────────────┘
```

---

## Conclusion

All necessary fixes have been implemented to ensure proper Python-Java communication:

✅ **Java can detect** if Python tuner is connected (heartbeat)
✅ **Python can read** coefficients from Java
✅ **Python can write** updated coefficients to Java
✅ **Java can publish** shot data for Python to collect
✅ **Python can read** shot data from Java
✅ **Interlocks work** bidirectionally for coordination
✅ **Paths match** between Python and Java
✅ **Examples provided** for both sides
✅ **Tests available** to verify integration
✅ **Documentation complete** with protocol details

The Python and Java components can now communicate properly and as intended.
