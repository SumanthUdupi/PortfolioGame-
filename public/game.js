// game.js
// This will be our main game file where Phaser.js logic resides.

console.log("game.js loaded");

// Global state for achievements (could be stored in local storage for persistence)
const achievements = {
    aboutMeViewed: false,
    projectsViewed: false,
    skillsViewed: false,
    contactViewed: false
};

// --- Preloader Scene ---
class PreloaderScene extends Phaser.Scene {
    constructor() {
        super('PreloaderScene');
    }

    preload() {
        // Display a loading bar or text
        let loadingText = this.add.text(this.scale.width / 2, this.scale.height / 2, 'Loading...', { 
            fontSize: '32px', 
            fill: '#4A2B00', 
            fontFamily: 'Caveat, cursive' 
        }).setOrigin(0.5);

        // Load placeholder assets (a very short silent audio for now)
        // In a real game, you would load actual audio files.
        const silentAudioData = 'data:audio/wav;base64,UklGRiQAAABXQVZFZm10IBAAAAABAAEARKwAAIhYAQACABAAZGF0YQAAAAAA'; // A very short silent WAV
        this.load.audio('background_music', silentAudioData);
        this.load.audio('click_sfx', silentAudioData);
        this.load.audio('achievement_sfx', silentAudioData);


        // Simulate loading other assets
        for (let i = 0; i < 500; i++) {
            this.load.image('dummy' + i, 'data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs=');
        }

        this.load.on('progress', (value) => {
            loadingText.setText('Loading: ' + Math.round(value * 100) + '%');
        });

        this.load.on('complete', () => {
            loadingText.setText('Loading Complete!');
        });
    }

    create() {
        // Transition to the GameScene after a short delay
        this.time.delayedCall(500, () => {
            this.scene.start('GameScene');
        });
    }
}

// --- Game Scene ---
class GameScene extends Phaser.Scene {
    constructor() {
        super('GameScene');
        this.player = null;
        this.destination = null;

        this.aboutMeContent = null;
        this.projectsContent = null;
        this.skillsContent = null;
        this.contactContent = null;

        this.aboutMeRect = null;
        this.projectsRect = null;
        this.skillsRect = null;
        this.contactRect = null;

        this.achievementPanel = null; // UI element for achievements
        this.bgMusic = null; // Declare bgMusic here
    }

    preload() {
        // No assets to preload in this scene directly for now.
        // All major assets will be preloaded in PreloaderScene.
    }

    create() {
        // Play background music
        this.bgMusic = this.sound.add('background_music', { loop: true, volume: 0.5 });
        this.bgMusic.play();

        // Set a cozy background color
        this.cameras.main.setBackgroundColor('#D2B48C'); // Tan/light brown for a warm feel

        // Define world bounds, making it larger than the camera view for exploration
        const worldWidth = this.scale.width * 3; // 3 times the camera width
        const worldHeight = this.scale.height * 3; // 3 times the camera height
        this.physics.world.setBounds(0, 0, worldWidth, worldHeight);

        // Add placeholder text for the scene (centered in the larger world)
        this.add.text(worldWidth / 2, worldHeight / 2, 'Welcome to My Cozy Portfolio!', { 
            fontSize: '48px', 
            fill: '#4A2B00', // Dark brown for text
            fontFamily: 'Caveat, cursive' // Use the loaded font
        }).setOrigin(0.5);

        this.add.text(worldWidth / 2, worldHeight / 2 + 60, 'Click to explore!', { 
            fontSize: '24px', 
            fill: '#4A2B00',
            fontFamily: 'Caveat, cursive'
        }).setOrigin(0.5);

        // --- Portfolio Sections ---
        const sectionWidth = 300;
        const sectionHeight = 200;
        const sectionTextStyle = { fontSize: '32px', fill: '#FFFFFF', fontFamily: 'Caveat, cursive' };
        const contentTextStyle = { 
            fontSize: '20px', 
            fill: '#4A2B00', 
            fontFamily: 'Caveat, cursive',
            wordWrap: { width: 400, useAdvancedWrap: true }
        };

        // Helper function to create interactive sections
        const createSection = (x, y, label, content, color) => {
            const rect = this.add.rectangle(x, y, sectionWidth, sectionHeight, color)
                .setOrigin(0.5)
                .setInteractive()
                .on('pointerover', () => rect.setScale(1.05)) // Subtle scale on hover
                .on('pointerout', () => rect.setScale(1)); // Reset scale
            this.physics.add.existing(rect, true);
            this.add.text(x, y, label, sectionTextStyle).setOrigin(0.5);
            const contentText = this.add.text(x, y + 150, content, contentTextStyle).setOrigin(0.5).setVisible(false).setScale(0.8).setAlpha(0); // Initial state for animation
            return { rect, contentText };
        };

        const about = createSection(worldWidth * 0.25, worldHeight * 0.25, 'About Me', 'This is where I tell you about myself!', 0x8B4513);
        this.aboutMeRect = about.rect;
        this.aboutMeContent = about.contentText;

        const projects = createSection(worldWidth * 0.75, worldHeight * 0.25, 'Projects', 'Check out my awesome projects here!', 0x5F9EA0);
        this.projectsRect = projects.rect;
        this.projectsContent = projects.contentText;

        const skills = createSection(worldWidth * 0.25, worldHeight * 0.75, 'Skills', 'These are the things I\'m good at!', 0x6B8E23);
        this.skillsRect = skills.rect;
        this.skillsContent = skills.contentText;

        const contact = createSection(worldWidth * 0.75, worldHeight * 0.75, 'Contact', 'Get in touch with me!', 0xD2691E);
        this.contactRect = contact.rect;
        this.contactContent = contact.contentText;
        // --- End Portfolio Sections ---

        // Create a simple player character (a circle with an outline)
        const playerGraphics = this.add.graphics({ x: worldWidth / 2, y: worldHeight / 2 });
        playerGraphics.lineStyle(4, 0x4A2B00, 1); // Dark brown outline
        playerGraphics.fillStyle(0xFFD700, 1); // Gold fill for a warm touch
        playerGraphics.fillCircle(0, 0, 16); // Draw a circle
        playerGraphics.strokeCircle(0, 0, 16); // Draw the outline
        this.player = this.physics.add.existing(playerGraphics); // Add physics to the graphics object
        this.player.body.setCollideWorldBounds(true);
        this.player.body.setCircle(16); // Set the physics body to match the circle
        this.player.setOrigin(0.5);
        this.player.body.setDrag(500); // Add some drag to make movement feel smoother
        this.player.setScale(1); // Initialize scale for animation
        
        // Initialize destination to player's current position
        this.destination = new Phaser.Math.Vector2(this.player.x, this.player.y);

        // Camera follows the player
        this.cameras.main.startFollow(this.player);
        this.cameras.main.setBounds(0, 0, worldWidth, worldHeight);

        // Input for point-and-click movement
        this.input.on('pointerdown', function (pointer) {
            // Get world coordinates of the click
            const worldPoint = this.cameras.main.getWorldPoint(pointer.x, pointer.y);
            this.destination.x = worldPoint.x;
            this.destination.y = worldPoint.y;
            this.sound.play('click_sfx', { volume: 0.1 }); // Play click sound
            
            // Player scale animation on click
            this.tweens.add({
                targets: this.player,
                scaleX: 1.1,
                scaleY: 1.1,
                duration: 100,
                yoyo: true,
                ease: 'Power1'
            });
        }, this);

        // Overlap handling functions
        this.showContentWithAnimation = (contentObject) => {
            if (!contentObject.visible) {
                contentObject.setVisible(true);
                this.tweens.add({
                    targets: contentObject,
                    alpha: 1,
                    scaleX: 1,
                    scaleY: 1,
                    duration: 300,
                    ease: 'Power2'
                });
            }
        };

        this.hideContentWithAnimation = (contentObject) => {
            if (contentObject.visible) {
                this.tweens.add({
                    targets: contentObject,
                    alpha: 0,
                    scaleX: 0.8,
                    scaleY: 0.8,
                    duration: 300,
                    ease: 'Power2',
                    onComplete: () => contentObject.setVisible(false)
                });
            }
        };

        // --- Achievement System ---
        const achievementTextStyle = { 
            fontSize: '20px', 
            fill: '#FFFFFF', 
            fontFamily: 'Caveat, cursive',
            backgroundColor: '#8B4513', // Cozy background for pop-up
            padding: { x: 10, y: 5 }
        };

        this.showAchievement = (text) => {
            this.sound.play('achievement_sfx', { volume: 0.2 }); // Play achievement sound
            const achievementPopUp = this.add.text(this.cameras.main.worldView.centerX, this.cameras.main.worldView.centerY - 100, text, achievementTextStyle)
                .setOrigin(0.5)
                .setScrollFactor(0) // Fixed to camera
                .setAlpha(0)
                .setScale(0.8);
            
            this.tweens.add({
                targets: achievementPopUp,
                alpha: 1,
                y: '-=50', // Move up slightly
                scaleX: 1,
                scaleY: 1,
                ease: 'Power1',
                duration: 500,
                onComplete: () => {
                    this.time.delayedCall(2000, () => {
                        this.tweens.add({
                            targets: achievementPopUp,
                            alpha: 0,
                            y: '-=20',
                            scaleX: 0.8,
                            scaleY: 0.8,
                            ease: 'Power1',
                            duration: 500,
                            onComplete: () => achievementPopUp.destroy()
                        });
                    });
                }
            });
        };

        // Persistent achievement display panel (top-right corner)
        this.achievementPanel = this.add.text(this.scale.width - 20, 20, 'Achievements:', { 
            fontSize: '18px', 
            fill: '#4A2B00', 
            fontFamily: 'Caveat, cursive',
            backgroundColor: '#F5DEB3', // Wheat color for panel
            padding: { x: 10, y: 5 }
        }).setOrigin(1, 0) // Anchor to top-right
          .setScrollFactor(0) // Fixed to camera
          .setDepth(100); // Ensure it's on top

        this.updateAchievementPanel = () => {
            let panelText = 'Achievements:\n';
            if (achievements.aboutMeViewed) panelText += '- About Me (Viewed)\n';
            if (achievements.projectsViewed) panelText += '- Projects (Viewed)\n';
            if (achievements.skillsViewed) panelText += '- Skills (Viewed)\n';
            if (achievements.contactViewed) panelText += '- Contact (Viewed)\n';
            if (panelText === 'Achievements:\n') panelText += 'None yet... explore!';
            this.achievementPanel.setText(panelText);
        };
        this.updateAchievementPanel(); // Initial update

        // Overlap management for content and achievements
        this.manageSectionInteraction = (player, rect, contentObject, achievementKey, achievementName) => {
            if (this.physics.overlap(player, rect)) {
                this.showContentWithAnimation(contentObject);
                if (!achievements[achievementKey]) {
                    achievements[achievementKey] = true;
                    this.showAchievement(`Achievement Unlocked: ${achievementName}!`);
                    this.updateAchievementPanel();
                }
            } else {
                this.hideContentWithAnimation(contentObject);
            }
        };
    }

    update() {
        // Move player towards destination
        const distance = Phaser.Math.Distance.Between(this.player.x, this.player.y, this.destination.x, this.destination.y);

        if (distance > 5) { // If player is not at destination (with a small tolerance)
            this.physics.accelerateToObject(this.player, this.destination, 300, 300, 300); // Adjust acceleration as needed
        } else {
            this.player.body.setVelocity(0, 0); // Stop player when destination is reached
            this.player.x = this.destination.x;
            this.player.y = this.destination.y;
        }

        // Manage content visibility and achievements based on player overlap with sections
        this.manageSectionInteraction(this.player, this.aboutMeRect, this.aboutMeContent, 'aboutMeViewed', 'A Glimpse Into Me');
        this.manageSectionInteraction(this.player, this.projectsRect, this.projectsContent, 'projectsViewed', 'Project Explorer');
        this.manageSectionInteraction(this.player, this.skillsRect, this.skillsContent, 'skillsViewed', 'Skill Seeker');
        this.manageSectionInteraction(this.player, this.contactRect, this.contactContent, 'contactViewed', 'Reach Out');
    }
}

// Phaser configuration
const gameConfig = {
    type: Phaser.AUTO,
    scale: {
        mode: Phaser.Scale.FIT, // Fit to screen, maintaining aspect ratio
        autoCenter: Phaser.Scale.CENTER_BOTH, // Center the game canvas
        width: 1280, // Base width for design
        height: 720, // Base height for design
    },
    parent: 'game-container', // ID of the div to put the game canvas in
    physics: {
        default: 'arcade',
        arcade: {
            debug: false
        }
    },
    scene: [PreloaderScene, GameScene] // List of scenes in the game
};

// Initialize the game
const game = new Phaser.Game(gameConfig);
