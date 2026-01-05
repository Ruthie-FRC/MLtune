// Example showing how to integrate MLtune into your robot code
// This demonstrates the minimal integration needed for Python-Java communication

package frc.robot.examples;

import edu.wpi.first.wpilibj.Timer;
import edu.wpi.first.wpilibj2.command.SubsystemBase;
import frc.robot.util.TunerInterface;
import frc.robot.util.LoggedTunableNumber;

/**
 * Minimal example showing how to integrate MLtune into a shooter subsystem.
 * 
 * This example demonstrates:
 * 1. Creating tunable coefficients with LoggedTunableNumber
 * 2. Using TunerInterface to check tuner status
 * 3. Logging shot data for the Python tuner
 * 4. Using interlocks to coordinate with the tuner (optional)
 * 
 * Integration steps:
 * 1. Copy TunerInterface.java and LoggedTunableNumber.java to your project
 * 2. Replace static constants with LoggedTunableNumber instances
 * 3. Call TunerInterface methods to check tuner status
 * 4. Log every shot with all relevant data
 */
public class MinimalShooterExample extends SubsystemBase {
    
    // ========== TUNABLE COEFFICIENTS ==========
    // Replace your static final constants with LoggedTunableNumber
    // These automatically sync with NetworkTables when tuningMode is enabled
    
    // Before: private static final double DRAG_COEFFICIENT = 0.47;
    // After:
    private static final LoggedTunableNumber dragCoefficient = 
        new LoggedTunableNumber("DragCoefficient", 0.47);
    
    private static final LoggedTunableNumber airDensity = 
        new LoggedTunableNumber("AirDensity", 1.225);
    
    private static final LoggedTunableNumber velocityIterations = 
        new LoggedTunableNumber("VelocityIterations", 20);
    
    // ========== TUNER INTERFACE ==========
    // Singleton interface to check tuner connection and status
    private final TunerInterface tunerInterface;
    
    // ========== SHOT TRACKING ==========
    // NetworkTables publishers for shot data
    private final edu.wpi.first.networktables.NetworkTable shotTable;
    private final edu.wpi.first.networktables.DoublePublisher shotTimestampPub;
    private final edu.wpi.first.networktables.BooleanPublisher hitPub;
    private final edu.wpi.first.networktables.DoublePublisher distancePub;
    private final edu.wpi.first.networktables.DoublePublisher dragCoeffPub;
    private final edu.wpi.first.networktables.DoublePublisher airDensityPub;
    
    // Solution subtable
    private final edu.wpi.first.networktables.DoublePublisher pitchPub;
    private final edu.wpi.first.networktables.DoublePublisher velocityPub;
    private final edu.wpi.first.networktables.DoublePublisher yawPub;
    
    public MinimalShooterExample() {
        // Get tuner interface singleton
        tunerInterface = TunerInterface.getInstance();
        
        // Set up NetworkTables publishers for shot data
        var ntInstance = edu.wpi.first.networktables.NetworkTableInstance.getDefault();
        shotTable = ntInstance.getTable("FiringSolver");
        var solutionTable = shotTable.getSubTable("Solution");
        
        shotTimestampPub = shotTable.getDoubleTopic("ShotTimestamp").publish();
        hitPub = shotTable.getBooleanTopic("Hit").publish();
        distancePub = shotTable.getDoubleTopic("Distance").publish();
        dragCoeffPub = shotTable.getDoubleTopic("DragCoefficient").publish();
        airDensityPub = shotTable.getDoubleTopic("AirDensity").publish();
        
        pitchPub = solutionTable.getDoubleTopic("pitchRadians").publish();
        velocityPub = solutionTable.getDoubleTopic("exitVelocity").publish();
        yawPub = solutionTable.getDoubleTopic("yawRadians").publish();
    }
    
    @Override
    public void periodic() {
        // Optional: Check if tuner is connected
        if (tunerInterface.isTunerConnected()) {
            // Tuner is running - you could display this on dashboard
        }
        
        // Optional: Check current tuning status
        String currentCoeff = tunerInterface.getCurrentCoefficient();
        int shotCount = tunerInterface.getShotCount();
        // Display this info to drivers if desired
    }
    
    /**
     * Example shooting method showing the integration pattern.
     * 
     * This demonstrates:
     * 1. Using tunable coefficients with .get()
     * 2. Checking shooting interlocks (optional)
     * 3. Logging shot data for the tuner
     */
    public void shootAtTarget(double distanceMeters) {
        // ========== 1. CALCULATE SOLUTION ==========
        // Use tunable coefficients with .get() to access current values
        double drag = dragCoefficient.get();
        double density = airDensity.get();
        int iterations = (int) velocityIterations.get();
        
        // Your existing firing solution calculation
        // This is simplified - use your actual solver
        double pitchRadians = calculatePitch(distanceMeters, drag, density, iterations);
        double exitVelocityMps = calculateVelocity(distanceMeters, drag, density);
        double yawRadians = 0.0;  // For 2D case
        
        // ========== 2. CHECK INTERLOCKS (OPTIONAL) ==========
        // If you enabled interlocks, check before shooting
        // This ensures tuner has processed the previous shot
        if (!tunerInterface.isShootingAllowed()) {
            System.out.println("Shot blocked by tuner interlock");
            return;  // Wait for tuner to clear interlock
        }
        
        // Clear the shot logged flag BEFORE shooting
        // The tuner will set it back to true after logging the shot
        tunerInterface.clearShotLoggedFlag();
        
        // ========== 3. EXECUTE SHOT ==========
        // Your code to actually shoot
        setShooterAngle(pitchRadians);
        setShooterVelocity(exitVelocityMps);
        shoot();
        
        // Wait for shot to complete
        Timer.delay(0.5);  // Adjust based on your shot time
        
        // ========== 4. DETECT RESULT ==========
        // Your code to detect if shot hit or missed
        // This could use vision, sensors, or driver input
        boolean hit = detectShotResult();
        
        // ========== 5. LOG SHOT DATA ==========
        // CRITICAL: Log EVERY shot with ALL relevant data
        // The tuner needs this to optimize coefficients
        logShotData(
            hit, 
            distanceMeters, 
            pitchRadians, 
            exitVelocityMps, 
            yawRadians,
            drag,  // Current coefficient values at shot time
            density
        );
    }
    
    /**
     * Log shot data to NetworkTables for the Python tuner.
     * 
     * This publishes all the information the tuner needs:
     * - Shot result (hit/miss)
     * - Firing solution used (distance, angle, velocity)
     * - Coefficient values at the time of the shot
     * 
     * The Python tuner monitors ShotTimestamp to detect new shots.
     */
    private void logShotData(
            boolean hit,
            double distanceMeters,
            double pitchRadians,
            double exitVelocityMps,
            double yawRadians,
            double dragCoeffUsed,
            double airDensityUsed) {
        
        // Update timestamp LAST - this signals new shot to Python
        shotTimestampPub.set(Timer.getFPGATimestamp());
        
        // Shot result
        hitPub.set(hit);
        
        // Target parameters
        distancePub.set(distanceMeters);
        
        // Solution used
        pitchPub.set(pitchRadians);
        velocityPub.set(exitVelocityMps);
        yawPub.set(yawRadians);
        
        // Coefficient values at shot time (IMPORTANT!)
        // The tuner needs to know which coefficient values were used
        dragCoeffPub.set(dragCoeffUsed);
        airDensityPub.set(airDensityUsed);
        
        System.out.println(String.format(
            "Shot logged: hit=%s, dist=%.2fm, pitch=%.3frad, vel=%.2fm/s",
            hit, distanceMeters, pitchRadians, exitVelocityMps
        ));
    }
    
    // ========== PLACEHOLDER METHODS ==========
    // Replace these with your actual implementation
    
    private double calculatePitch(double distance, double drag, double density, int iterations) {
        // Your pitch calculation logic
        return 0.4;  // Placeholder
    }
    
    private double calculateVelocity(double distance, double drag, double density) {
        // Your velocity calculation logic
        return 15.0;  // Placeholder
    }
    
    private void setShooterAngle(double radians) {
        // Your angle control code
    }
    
    private void setShooterVelocity(double mps) {
        // Your velocity control code
    }
    
    private void shoot() {
        // Your shooting trigger code
    }
    
    private boolean detectShotResult() {
        // Your hit detection code
        // Could use vision, beam breaks, driver input, etc.
        return false;  // Placeholder
    }
}
