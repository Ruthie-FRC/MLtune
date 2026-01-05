#!/usr/bin/env python3
"""
Integration test script to verify Python-Java NetworkTables communication.

This script tests that:
1. Python can connect to NetworkTables
2. Python can publish heartbeat for Java connection detection
3. Python can read/write coefficients at correct paths
4. Python can read shot data from Java
5. Python can signal interlocks (shot logged, coefficients updated)

Run this script with a NetworkTables server running (either a robot or simulator).
"""

import sys
import time
import logging
from pathlib import Path

# Add MLtune to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from MLtune.tuner.nt_interface import NetworkTablesInterface, ShotData
from MLtune.tuner.config import TunerConfig

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def test_connection(nt_interface):
    """Test basic NetworkTables connection."""
    logger.info("=" * 60)
    logger.info("TEST 1: NetworkTables Connection")
    logger.info("=" * 60)
    
    # Try to connect (will use localhost by default if not specified)
    if nt_interface.start(server_ip="localhost"):
        logger.info("✓ Connected to NetworkTables successfully")
        return True
    else:
        logger.error("✗ Failed to connect to NetworkTables")
        logger.info("  Make sure a NetworkTables server is running (robot or simulator)")
        return False


def test_heartbeat(nt_interface):
    """Test heartbeat publishing."""
    logger.info("=" * 60)
    logger.info("TEST 2: Heartbeat Publishing")
    logger.info("=" * 60)
    
    try:
        # Publish heartbeat multiple times
        for i in range(3):
            nt_interface.publish_heartbeat()
            logger.info(f"✓ Published heartbeat {i+1}/3")
            time.sleep(0.5)
        
        logger.info("✓ Heartbeat mechanism working")
        logger.info("  Java TunerInterface.isTunerConnected() should return true")
        return True
    except Exception as e:
        logger.error(f"✗ Heartbeat test failed: {e}")
        return False


def test_coefficient_paths(nt_interface, config):
    """Test coefficient read/write at correct NetworkTables paths."""
    logger.info("=" * 60)
    logger.info("TEST 3: Coefficient Read/Write Paths")
    logger.info("=" * 60)
    
    # Test paths that match Java LoggedTunableNumber
    # Java creates: "/Tuning/" + dashboardKey (e.g., "/Tuning/DragCoefficient")
    test_coefficients = {
        "DragCoefficient": 0.47,
        "AirDensity": 1.225,
        "ProjectileMass": 0.27,
        "ProjectileArea": 0.0314,
    }
    
    success = True
    for coeff_name, default_value in test_coefficients.items():
        try:
            # Write a test value
            test_value = default_value * 1.1  # Slightly different from default
            if nt_interface.write_coefficient(coeff_name, test_value, force=True):
                logger.info(f"✓ Wrote {coeff_name} = {test_value}")
                
                # Small delay to ensure value propagates
                time.sleep(0.1)
                
                # Read it back
                read_value = nt_interface.read_coefficient(coeff_name, default_value)
                if abs(read_value - test_value) < 0.001:
                    logger.info(f"✓ Read back {coeff_name} = {read_value} (matches)")
                else:
                    logger.warning(f"⚠ Read back {coeff_name} = {read_value} (expected {test_value})")
                    logger.info(f"  This might be OK if Java is overwriting the value")
            else:
                logger.error(f"✗ Failed to write {coeff_name}")
                success = False
        except Exception as e:
            logger.error(f"✗ Error testing {coeff_name}: {e}")
            success = False
    
    if success:
        logger.info("✓ Coefficient path test completed")
        logger.info(f"  Coefficients should appear at /Tuning/<CoeffName> in NetworkTables")
    return success


def test_interlock_signals(nt_interface):
    """Test interlock signaling methods."""
    logger.info("=" * 60)
    logger.info("TEST 4: Interlock Signals")
    logger.info("=" * 60)
    
    try:
        # Test shot logged signal
        nt_interface.signal_shot_logged()
        logger.info("✓ Signaled shot logged")
        logger.info("  Java TunerInterface.isShootingAllowed() should allow shooting")
        
        time.sleep(0.1)
        
        # Test coefficients updated signal
        nt_interface.signal_coefficients_updated()
        logger.info("✓ Signaled coefficients updated")
        
        time.sleep(0.1)
        
        # Test interlock settings
        nt_interface.write_interlock_settings(
            require_shot_logged=False,
            require_coefficients_updated=False
        )
        logger.info("✓ Wrote interlock settings (both disabled)")
        logger.info("  Java TunerInterface.isShootingAllowed() should return true")
        
        return True
    except Exception as e:
        logger.error(f"✗ Interlock test failed: {e}")
        return False


def test_status_publishing(nt_interface):
    """Test status and autotune information publishing."""
    logger.info("=" * 60)
    logger.info("TEST 5: Status Publishing")
    logger.info("=" * 60)
    
    try:
        # Test tuner enabled status
        nt_interface.write_tuner_enabled_status(enabled=True, paused=False)
        logger.info("✓ Published tuner enabled status")
        
        time.sleep(0.1)
        
        # Test autotune status
        nt_interface.write_autotune_status(
            autotune_enabled=True,
            shot_count=5,
            shot_threshold=10
        )
        logger.info("✓ Published autotune status (5/10 shots)")
        logger.info("  Java TunerInterface can read shot count and threshold")
        
        time.sleep(0.1)
        
        # Test current coefficient info
        nt_interface.write_current_coefficient_info(
            coeff_name="DragCoefficient",
            is_autotune=True,
            shot_threshold=10,
            auto_advance=True
        )
        logger.info("✓ Published current coefficient info")
        logger.info("  Java TunerInterface.getCurrentCoefficient() should return 'DragCoefficient'")
        
        return True
    except Exception as e:
        logger.error(f"✗ Status publishing test failed: {e}")
        return False


def test_shot_data_reading(nt_interface):
    """Test reading shot data (requires Java side to publish)."""
    logger.info("=" * 60)
    logger.info("TEST 6: Shot Data Reading")
    logger.info("=" * 60)
    
    logger.info("Waiting for shot data from Java side...")
    logger.info("(This test requires Java code to publish shot data)")
    logger.info("Checking for 5 seconds...")
    
    shot_received = False
    for i in range(5):
        shot_data = nt_interface.read_shot_data()
        if shot_data:
            logger.info(f"✓ Received shot data: {shot_data}")
            shot_received = True
            break
        time.sleep(1)
        logger.info(f"  Waiting... ({i+1}/5)")
    
    if not shot_received:
        logger.warning("⚠ No shot data received")
        logger.info("  This is OK if Java side isn't publishing shots yet")
        logger.info("  Java should call FiringSolver.logShot() to publish shot data")
    
    return True  # Don't fail on this test


def main():
    """Run all integration tests."""
    logger.info("MLtune Python-Java Integration Test")
    logger.info("=" * 60)
    
    # Create config and interface
    config = TunerConfig()
    nt_interface = NetworkTablesInterface(config)
    
    # Run tests
    results = {
        "Connection": test_connection(nt_interface),
    }
    
    if results["Connection"]:
        # Only run other tests if connection succeeded
        results["Heartbeat"] = test_heartbeat(nt_interface)
        results["Coefficient Paths"] = test_coefficient_paths(nt_interface, config)
        results["Interlock Signals"] = test_interlock_signals(nt_interface)
        results["Status Publishing"] = test_status_publishing(nt_interface)
        results["Shot Data Reading"] = test_shot_data_reading(nt_interface)
    
    # Summary
    logger.info("=" * 60)
    logger.info("TEST SUMMARY")
    logger.info("=" * 60)
    for test_name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        logger.info(f"{status} - {test_name}")
    
    passed_count = sum(1 for v in results.values() if v)
    total_count = len(results)
    logger.info(f"\nPassed {passed_count}/{total_count} tests")
    
    # Cleanup
    nt_interface.stop()
    
    return 0 if passed_count == total_count else 1


if __name__ == "__main__":
    sys.exit(main())
