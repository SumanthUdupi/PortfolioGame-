// game.js
// A Cozy Portfolio Game
// Uses Phaser 3 to create an interactive, explorable portfolio environment.

console.log("Cozy Portfolio Game Loaded");

// --- Global State ---
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

    create() {
        // Create a loading bar UI
        const width = this.cameras.main.width;
        const height = this.cameras.main.height;

        const progressBar = this.add.graphics();
        const progressBox = this.add.graphics();
        progressBox.fillStyle(0x8B4513, 0.8);
        progressBox.fillRect(width / 2 - 160, height / 2 - 25, 320, 50);

        const loadingText = this.add.text(width / 2, height / 2 - 50, 'Brewing Coffee...', {
            fontFamily: 'Caveat, cursive',
            fontSize: '28px',
            fill: '#4A2B00'
        }).setOrigin(0.5);

        // Simulate load with a tween
        this.tweens.addCounter({
            from: 0,
            to: 100,
            duration: 1500, // 1.5 seconds loading time
            onUpdate: (tween) => {
                const value = tween.getValue();
                progressBar.clear();
                progressBar.fillStyle(0xF5DEB3, 1);
                progressBar.fillRect(width / 2 - 150, height / 2 - 15, 300 * (value / 100), 30);
            },
            onComplete: () => {
                progressBar.destroy();
                progressBox.destroy();
                loadingText.destroy();
                this.scene.start('GameScene');
            }
        });
    }
}

// --- Game Scene ---
class GameScene extends Phaser.Scene {
    constructor() {
        super('GameScene');
        this.player = null;
        this.destination = null;
        this.zones = [];
        this.popups = [];
    }

    create() {
        // 1. World & Camera Setup
        this.cameras.main.setBackgroundColor('#E6D5B8'); // Soft beige/parchment
        const worldW = 2000;
        const worldH = 1500;
        this.physics.world.setBounds(0, 0, worldW, worldH);
        this.cameras.main.setBounds(0, 0, worldW, worldH);

        // 2. Environment (Procedural)
        this.createEnvironment(worldW, worldH);

        // 3. Create Zones (Interactive Areas)
        this.createZones(worldW, worldH);

        // 4. Player Setup
        this.createPlayer(worldW / 2, worldH / 2);

        // 5. UI & Achievements
        this.createUI();

        // 6. Input Handling
        this.input.on('pointerdown', (pointer) => {
            const worldPoint = this.cameras.main.getWorldPoint(pointer.x, pointer.y);
            this.destination.set(worldPoint.x, worldPoint.y);

            // Visual feedback for click
            this.createClickRipple(worldPoint.x, worldPoint.y);
        });

        // Camera Follow
        this.cameras.main.startFollow(this.player, true, 0.08, 0.08);
    }

    update() {
        // Movement Logic
        const distance = Phaser.Math.Distance.Between(this.player.x, this.player.y, this.destination.x, this.destination.y);

        if (distance > 10) {
            this.physics.accelerateToObject(this.player, this.destination, 400, 300, 300);
            // Flip player based on direction
            if (this.player.body.velocity.x < 0) this.player.setScale(-1, 1);
            else this.player.setScale(1, 1);
        } else {
            this.player.body.setVelocity(0, 0);
            this.player.body.setAcceleration(0, 0);
        }

        // Zone Interaction
        this.zones.forEach(zone => {
            const overlap = this.physics.overlap(this.player, zone.trigger);
            if (overlap) {
                if (!zone.isActive) {
                    zone.isActive = true;
                    this.showPopup(zone);
                    this.unlockAchievement(zone.key);
                }
            } else {
                if (zone.isActive) {
                    zone.isActive = false;
                    this.hidePopup(zone);
                }
            }
        });
    }

    // --- Creation Helpers ---

    createEnvironment(w, h) {
        // Draw Grass Tufts
        const grass = this.add.graphics();
        grass.fillStyle(0xCCD5AE, 1.0); // Soft green
        for (let i = 0; i < 300; i++) {
            const x = Phaser.Math.Between(0, w);
            const y = Phaser.Math.Between(0, h);
            grass.fillCircle(x, y, Phaser.Math.Between(4, 10));
        }

        // Draw Some Trees (Simple shapes)
        for (let i = 0; i < 20; i++) {
            this.drawTree(Phaser.Math.Between(0, w), Phaser.Math.Between(0, h));
        }

        // Title on the ground
        this.add.text(w/2, h/2 - 100, "Jules's Portfolio", {
            fontFamily: 'Caveat, cursive',
            fontSize: '48px',
            fill: '#8B4513'
        }).setOrigin(0.5).setAlpha(0.6);

        this.add.text(w/2, h/2 - 60, "(Click to walk & explore)", {
            fontFamily: 'Caveat, cursive',
            fontSize: '24px',
            fill: '#8B4513'
        }).setOrigin(0.5).setAlpha(0.6);
    }

    drawTree(x, y) {
        const tree = this.add.container(x, y);
        const trunk = this.add.graphics();
        trunk.fillStyle(0x8B4513, 1);
        trunk.fillRect(-10, 0, 20, 60); // Trunk

        const leaves = this.add.graphics();
        leaves.fillStyle(0x6B8E23, 1);
        leaves.fillCircle(0, -20, 40); // Leaves
        leaves.fillStyle(0x556B2F, 0.8);
        leaves.fillCircle(-20, -10, 30);
        leaves.fillCircle(20, -10, 30);

        tree.add([trunk, leaves]);
        tree.setDepth(y); // Simple depth sorting
    }

    createZones(w, h) {
        // Define our 4 main areas
        const locations = [
            {
                key: 'about', title: 'About Me', x: w * 0.2, y: h * 0.2,
                color: 0xE9967A,
                draw: this.drawHouse.bind(this),
                content: "Hi! I'm Jules, a passionate developer.\nI love building cozy, interactive web experiences.\nMy goal is to make software feel human."
            },
            {
                key: 'projects', title: 'Projects', x: w * 0.8, y: h * 0.2,
                color: 0x8FBC8F,
                draw: this.drawGallery.bind(this),
                content: "1. Cozy Portfolio (You are here!)\n2. Neon Space Shooter (Python/Pygame)\n3. Procedural Art Gen\n\nCheck my GitHub for more!"
            },
            {
                key: 'skills', title: 'Skills', x: w * 0.2, y: h * 0.8,
                color: 0xADD8E6,
                draw: this.drawGarden.bind(this),
                content: "Languages: JS, Python, HTML/CSS\nTools: React, Phaser, Git\nSpecialty: Creative Coding & Game Dev"
            },
            {
                key: 'contact', title: 'Contact', x: w * 0.8, y: h * 0.8,
                color: 0xF08080,
                draw: this.drawMailbox.bind(this),
                content: "Let's work together!\nEmail: jules@example.com\nTwitter: @jules_dev\nGitHub: github.com/jules"
            }
        ];

        locations.forEach(loc => {
            // Draw the visual landmark
            const visual = loc.draw(loc.x, loc.y);

            // Create a trigger zone (invisible circle)
            const trigger = this.add.circle(loc.x, loc.y + 40, 100, 0xffffff, 0); // Invisible
            this.physics.add.existing(trigger, true); // Static body

            // Store ref
            this.zones.push({
                key: loc.key,
                trigger: trigger,
                title: loc.title,
                content: loc.content,
                isActive: false,
                x: loc.x,
                y: loc.y
            });

            // Label
            this.add.text(loc.x, loc.y + 80, loc.title, {
                fontFamily: 'Caveat, cursive',
                fontSize: '24px',
                fill: '#4A2B00'
            }).setOrigin(0.5);
        });
    }

    drawHouse(x, y) {
        const house = this.add.container(x, y);
        const g = this.add.graphics();

        // Base
        g.fillStyle(0xF5F5DC, 1);
        g.fillRect(-50, -50, 100, 80);
        // Roof
        g.fillStyle(0xA0522D, 1);
        g.fillTriangle(-60, -50, 60, -50, 0, -110);
        // Door
        g.fillStyle(0x8B4513, 1);
        g.fillRect(-15, -10, 30, 40);
        
        house.add(g);
        house.setDepth(y);
        return house;
    }

    drawGallery(x, y) {
        const gallery = this.add.container(x, y);
        const g = this.add.graphics();

        // Easel legs
        g.lineStyle(4, 0x8B4513);
        g.lineBetween(-30, 20, 0, -40);
        g.lineBetween(30, 20, 0, -40);
        g.lineBetween(0, 20, 0, -10);

        // Canvas
        g.fillStyle(0xFFFFFF, 1);
        g.fillRect(-25, -30, 50, 40);
        g.lineStyle(2, 0x000000, 0.2);
        g.strokeRect(-25, -30, 50, 40);

        gallery.add(g);
        gallery.setDepth(y);
        return gallery;
    }

    drawGarden(x, y) {
        const garden = this.add.container(x, y);
        const g = this.add.graphics();

        // Flower bed
        g.fillStyle(0x8B4513, 1);
        g.fillEllipse(0, 10, 80, 40);

        // Flowers
        const colors = [0xFF69B4, 0xFFD700, 0x87CEEB];
        [-20, 0, 20].forEach((ox, i) => {
            g.fillStyle(0x228B22, 1);
            g.fillRect(ox - 2, -20, 4, 30); // Stem
            g.fillStyle(colors[i], 1);
            g.fillCircle(ox, -20, 8); // Petals
        });

        garden.add(g);
        garden.setDepth(y);
        return garden;
    }

    drawMailbox(x, y) {
        const mb = this.add.container(x, y);
        const g = this.add.graphics();

        // Post
        g.fillStyle(0x8B4513, 1);
        g.fillRect(-5, -10, 10, 40);

        // Box
        g.fillStyle(0xCD5C5C, 1); // Indian Red
        g.fillRoundedRect(-20, -35, 40, 25, 5);

        // Flag
        g.fillStyle(0xFFD700, 1);
        g.fillRect(15, -45, 5, 20);

        mb.add(g);
        mb.setDepth(y);
        return mb;
    }

    createPlayer(x, y) {
        // Draw a cute character (Procedural)
        const p = this.add.container(x, y);
        const g = this.add.graphics();

        // Shadow
        g.fillStyle(0x000000, 0.2);
        g.fillEllipse(0, 15, 30, 10);

        // Body (Ghost/Blob shape)
        g.fillStyle(0xFFFFFF, 1);
        g.fillCircle(0, 0, 20);
        g.fillRect(-20, 0, 40, 15);
        g.fillCircle(-10, 15, 8);
        g.fillCircle(10, 15, 8);
        g.fillCircle(0, 15, 8);

        // Eyes
        g.fillStyle(0x000000, 1);
        g.fillCircle(-8, 0, 3);
        g.fillCircle(8, 0, 3);

        // Blush
        g.fillStyle(0xFFB6C1, 0.6);
        g.fillCircle(-12, 5, 4);
        g.fillCircle(12, 5, 4);

        p.add(g);

        // Add physics
        this.physics.add.existing(p);
        p.body.setCircle(20);
        p.body.setOffset(-20, -20);
        p.body.setDrag(500);
        p.body.setCollideWorldBounds(true);

        this.player = p;
        this.destination = new Phaser.Math.Vector2(x, y);

        // Idle animation
        this.tweens.add({
            targets: p,
            y: '+=5',
            duration: 1500,
            yoyo: true,
            repeat: -1,
            ease: 'Sine.easeInOut'
        });
    }

    createClickRipple(x, y) {
        const ripple = this.add.circle(x, y, 5, 0xFFFFFF, 0.5);
        this.tweens.add({
            targets: ripple,
            scale: 5,
            alpha: 0,
            duration: 500,
            onComplete: () => ripple.destroy()
        });
    }

    // --- UI & Interaction ---

    createUI() {
        // Achievements Panel (Top Right)
        this.achText = this.add.text(this.scale.width - 20, 20, 'Achievements: 0/4', {
            fontFamily: 'Caveat, cursive',
            fontSize: '24px',
            fill: '#4A2B00',
            backgroundColor: '#F5DEB3',
            padding: { x: 10, y: 5 },
            align: 'right'
        }).setOrigin(1, 0).setScrollFactor(0).setDepth(100);
    }

    showPopup(zone) {
        // Create a popup container
        const width = 400;
        const height = 250;
        const x = this.cameras.main.width / 2;
        const y = this.cameras.main.height - height / 2 - 50;

        const container = this.add.container(x, y).setScrollFactor(0).setDepth(200);

        // Background
        const bg = this.add.graphics();
        bg.fillStyle(0xFFFAF0, 0.95);
        bg.lineStyle(4, 0x8B4513, 1);
        bg.fillRoundedRect(-width/2, -height/2, width, height, 15);
        bg.strokeRoundedRect(-width/2, -height/2, width, height, 15);

        // Content
        const title = this.add.text(0, -height/2 + 30, zone.title, {
            fontFamily: 'Caveat, cursive',
            fontSize: '36px',
            fill: '#8B4513',
            fontStyle: 'bold'
        }).setOrigin(0.5);

        const content = this.add.text(0, 10, zone.content, {
            fontFamily: 'Caveat, cursive',
            fontSize: '24px',
            fill: '#4A2B00',
            align: 'center',
            wordWrap: { width: width - 40 }
        }).setOrigin(0.5);

        const hint = this.add.text(0, height/2 - 20, "(Move away to close)", {
            fontFamily: 'Caveat, cursive',
            fontSize: '16px',
            fill: '#A0522D'
        }).setOrigin(0.5);

        container.add([bg, title, content, hint]);
        container.setScale(0);

        this.tweens.add({
            targets: container,
            scale: 1,
            duration: 400,
            ease: 'Back.out'
        });

        // Store active popup
        this.currentPopup = container;
    }

    hidePopup() {
        if (this.currentPopup) {
            const p = this.currentPopup;
            this.currentPopup = null;
            this.tweens.add({
                targets: p,
                scale: 0,
                duration: 300,
                ease: 'Back.in',
                onComplete: () => p.destroy()
            });
        }
    }

    unlockAchievement(key) {
        if (!achievements[key + 'Viewed']) {
            achievements[key + 'Viewed'] = true;

            // Update UI
            const count = Object.values(achievements).filter(v => v).length;
            this.achText.setText(`Achievements: ${count}/4`);

            // Flash effect
            this.cameras.main.flash(500, 255, 255, 200);
        }
    }
}

// --- Configuration ---
const config = {
    type: Phaser.AUTO,
    scale: {
        mode: Phaser.Scale.FIT,
        autoCenter: Phaser.Scale.CENTER_BOTH,
        width: 1280,
        height: 720
    },
    backgroundColor: '#E6D5B8',
    parent: 'game-container',
    physics: {
        default: 'arcade',
        arcade: {
            debug: false,
            gravity: { y: 0 }
        }
    },
    scene: [PreloaderScene, GameScene]
};

const game = new Phaser.Game(config);
