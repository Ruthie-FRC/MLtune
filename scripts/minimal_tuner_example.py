#!/usr/bin/env python3
"""
Minimal Python tuner example showing NetworkTables communication.

This example demonstrates the basic integration pattern for the MLtune tuner.
It shows how to:
1. Connect to NetworkTables
2. Publish heartbeat for connection detection
3. Monitor shot data
4. Write coefficient updates
5. Signal interlocks

This is a simplified version - the actual tuner has more features like
Bayesian optimization, autotune modes, and dashboard controls.
"""

import sys
import time
import logging
from pathlib import Path

# Add MLtune to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from MLtune.tuner.nt_interface import NetworkTablesInterface
from MLtune.tuner.config import TunerConfig

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main tuner loop."""
    # Configuration
    config = TunerConfig()
    
    # Create NetworkTables interface
    nt = NetworkTablesInterface(config)
    
    # Connect to robot (use "localhost" for simulation, "10.TE.AM.2" for real robot)
    logger.info("Connecting to NetworkTables...")
    server_ip = "localhost"  # Change to your robot's IP
    
    if not nt.start(server_ip=server_ip):
        logger.error("Failed to connect to NetworkTables")
        logger.info("Make sure robot code or simulator is running")
        return 1
    
    logger.info("Connected to NetworkTables successfully")
    logger.info("Starting tuner loop (Press Ctrl+C to stop)...")
    
    # Track shots
    shot_count = 0
    shot_threshold = 10
    
    try:
        while True:
            # 1. Publish heartbeat (every loop iteration is fine, rate limited internally)
            nt.publish_heartbeat()
            
            # 2. Publish status
            nt.write_tuner_enabled_status(enabled=True, paused=False)
            nt.write_autotune_status(
                autotune_enabled=False,  # Manual mode for this example
                shot_count=shot_count,
                shot_threshold=shot_threshold
            )
            
            # 3. Check for shot data
            shot_data = nt.read_shot_data()
            if shot_data:
                shot_count += 1
                logger.info(f"Shot #{shot_count}: hit={shot_data.hit}, "
                          f"distance={shot_data.distance:.2f}m, "
                          f"angle={shot_data.angle:.3f}rad, "
                          f"velocity={shot_data.velocity:.2f}m/s")
                logger.info(f"  Coefficients at shot time: drag={shot_data.drag_coefficient:.6f}, "
                          f"air_density={shot_data.air_density:.3f}")
                
                # Signal that we logged the shot (for interlocks)
                nt.signal_shot_logged()
                
                # In a real tuner, you would add this shot to your optimization dataset
                # and run optimization when enough shots are collected
            
            # 4. Check if manual optimization was triggered
            if nt.read_run_optimization_button():
                logger.info("Manual optimization triggered!")
                logger.info(f"Collected {shot_count} shots so far")
                
                # In a real tuner, this is where you would run Bayesian optimization
                # For this example, we'll just write a dummy coefficient update
                
                # Example: Update drag coefficient
                new_drag_coeff = 0.48  # In reality, this comes from optimization
                logger.info(f"Writing updated DragCoefficient: {new_drag_coeff}")
                
                if nt.write_coefficient("DragCoefficient", new_drag_coeff, force=True):
                    logger.info("✓ Coefficient update sent to robot")
                    nt.signal_coefficients_updated()
                else:
                    logger.error("✗ Failed to write coefficient")
            
            # 5. Check if tuner was disabled from dashboard
            changed, enabled = nt.read_tuner_enabled_toggle()
            if changed:
                if enabled:
                    logger.info("Tuner ENABLED from dashboard")
                else:
                    logger.info("Tuner DISABLED from dashboard")
                    logger.info("Pausing tuner activity...")
            
            # Small delay
            time.sleep(0.5)
            
    except KeyboardInterrupt:
        logger.info("\nStopping tuner...")
    finally:
        # Cleanup
        nt.stop()
        logger.info("Tuner stopped")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
