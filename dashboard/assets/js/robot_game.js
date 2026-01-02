// Simple Robot Runner Game (Chrome dino style)
class RobotGame {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        if (!this.canvas) return;
        
        this.ctx = this.canvas.getContext('2d');
        this.isRunning = false;
        this.score = 0;
        this.gameSpeed = 3;
        
        // Robot properties
        this.robot = {
            x: 50,
            y: 150,
            width: 30,
            height: 30,
            jumping: false,
            velocityY: 0,
            gravity: 0.6
        };
        
        // Obstacles
        this.obstacles = [];
        this.frameCount = 0;
        
        // Bind keyboard
        document.addEventListener('keydown', (e) => {
            if (e.code === 'Space') {
                e.preventDefault();
                if (!this.isRunning) {
                    this.start();
                } else {
                    this.jump();
                }
            }
        });
    }
    
    start() {
        this.isRunning = true;
        this.score = 0;
        this.obstacles = [];
        this.robot.y = 150;
        this.robot.velocityY = 0;
        this.robot.jumping = false;
        this.gameLoop();
    }
    
    jump() {
        if (!this.robot.jumping) {
            this.robot.velocityY = -12;
            this.robot.jumping = true;
        }
    }
    
    update() {
        // Update robot
        this.robot.velocityY += this.robot.gravity;
        this.robot.y += this.robot.velocityY;
        
        // Ground collision
        if (this.robot.y > 150) {
            this.robot.y = 150;
            this.robot.velocityY = 0;
            this.robot.jumping = false;
        }
        
        // Create obstacles
        this.frameCount++;
        if (this.frameCount % 120 === 0) {
            this.obstacles.push({
                x: 800,
                y: 160,
                width: 20,
                height: 40
            });
        }
        
        // Update obstacles
        this.obstacles = this.obstacles.filter(obs => {
            obs.x -= this.gameSpeed;
            
            // Check collision
            if (this.checkCollision(this.robot, obs)) {
                this.isRunning = false;
                return false;
            }
            
            // Remove off-screen obstacles
            if (obs.x + obs.width < 0) {
                this.score += 10;
                return false;
            }
            
            return true;
        });
        
        // Increase difficulty
        if (this.frameCount % 300 === 0) {
            this.gameSpeed += 0.2;
        }
    }
    
    checkCollision(rect1, rect2) {
        return rect1.x < rect2.x + rect2.width &&
               rect1.x + rect1.width > rect2.x &&
               rect1.y < rect2.y + rect2.height &&
               rect1.y + rect1.height > rect2.y;
    }
    
    draw() {
        // Clear canvas
        this.ctx.fillStyle = getComputedStyle(document.documentElement)
            .getPropertyValue('--bg-secondary').trim();
        this.ctx.fillRect(0, 0, 800, 200);
        
        // Draw ground
        this.ctx.strokeStyle = getComputedStyle(document.documentElement)
            .getPropertyValue('--border-default').trim();
        this.ctx.lineWidth = 2;
        this.ctx.beginPath();
        this.ctx.moveTo(0, 180);
        this.ctx.lineTo(800, 180);
        this.ctx.stroke();
        
        // Draw robot (simple geometric shape)
        this.ctx.fillStyle = getComputedStyle(document.documentElement)
            .getPropertyValue('--accent-primary').trim();
        
        // Robot body
        this.ctx.fillRect(this.robot.x, this.robot.y, this.robot.width, this.robot.height);
        
        // Robot head
        this.ctx.fillRect(this.robot.x + 5, this.robot.y - 10, 20, 10);
        
        // Robot eyes
        this.ctx.fillStyle = '#ffffff';
        this.ctx.fillRect(this.robot.x + 8, this.robot.y - 7, 5, 5);
        this.ctx.fillRect(this.robot.x + 17, this.robot.y - 7, 5, 5);
        
        // Draw obstacles
        this.ctx.fillStyle = getComputedStyle(document.documentElement)
            .getPropertyValue('--danger').trim();
        this.obstacles.forEach(obs => {
            this.ctx.fillRect(obs.x, obs.y, obs.width, obs.height);
        });
        
        // Update score display
        const scoreDiv = document.getElementById('game-score');
        if (scoreDiv) {
            scoreDiv.textContent = 'Score: ' + this.score;
        }
        
        // Game over message
        if (!this.isRunning && this.score > 0) {
            this.ctx.fillStyle = getComputedStyle(document.documentElement)
                .getPropertyValue('--text-primary').trim();
            this.ctx.font = '24px var(--font-family)';
            this.ctx.textAlign = 'center';
            this.ctx.fillText('Game Over! Press SPACE to restart', 400, 100);
        }
    }
    
    gameLoop() {
        if (this.isRunning) {
            this.update();
        }
        this.draw();
        
        if (this.isRunning) {
            requestAnimationFrame(() => this.gameLoop());
        }
    }
}

// Initialize game when canvas is ready
window.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        if (document.getElementById('game-canvas')) {
            window.robotGame = new RobotGame('game-canvas');
        }
    }, 100);
});


