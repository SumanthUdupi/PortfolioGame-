import pygame
import os
import random
import wave
import math
import struct

# Colors
NEON_BLUE = (0, 255, 255)
NEON_RED = (255, 0, 100)
NEON_GREEN = (50, 255, 50)
NEON_YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TRANSPARENT = (0, 0, 0, 0)

def create_glow_surf(radius, color):
    surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    for r in range(radius, 0, -2):
        alpha = int(255 * (r / radius) ** 3) # Fading out
        pygame.draw.circle(surf, (*color, 10), (radius, radius), r)
    pygame.draw.circle(surf, color, (radius, radius), radius // 2)
    return surf

def create_player_sprite():
    size = 64
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    # Triangle ship
    points = [(32, 10), (10, 54), (32, 45), (54, 54)]
    pygame.draw.polygon(surf, NEON_BLUE, points, 2)
    # Glow
    pygame.draw.polygon(surf, (*NEON_BLUE, 50), points, 0)
    return surf

def create_enemy_sprite():
    size = 48
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    # Hexagonish
    points = [(24, 5), (43, 15), (43, 33), (24, 43), (5, 33), (5, 15)]
    pygame.draw.polygon(surf, NEON_RED, points, 2)
    pygame.draw.line(surf, NEON_RED, (15, 20), (33, 20), 2)
    return surf

def create_projectile_sprite():
    size = 16
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.circle(surf, NEON_YELLOW, (8, 8), 6)
    return surf

def create_star_background(width, height, num_stars=100):
    surf = pygame.Surface((width, height))
    surf.fill(BLACK)
    for _ in range(num_stars):
        x = random.randint(0, width)
        y = random.randint(0, height)
        brightness = random.randint(50, 255)
        surf.set_at((x, y), (brightness, brightness, brightness))
    return surf

def generate_sound(filename, duration, freq_start, freq_end, volume=0.5):
    sample_rate = 44100
    n_samples = int(sample_rate * duration)

    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)

        for i in range(n_samples):
            t = i / sample_rate
            # Linear frequency slide
            freq = freq_start + (freq_end - freq_start) * (i / n_samples)
            value = int(32767.0 * volume * math.sin(2.0 * math.pi * freq * t))
            data = struct.pack('<h', value)
            wav_file.writeframesraw(data)

def main():
    pygame.init()

    # Paths
    assets_dir = os.path.join(os.path.dirname(__file__), '..', 'assets')
    sprites_dir = os.path.join(assets_dir, 'sprites')
    sounds_dir = os.path.join(assets_dir, 'sounds')

    os.makedirs(sprites_dir, exist_ok=True)
    os.makedirs(sounds_dir, exist_ok=True)

    # Generate Sprites
    print("Generating sprites...")
    pygame.image.save(create_player_sprite(), os.path.join(sprites_dir, 'player.png'))
    pygame.image.save(create_enemy_sprite(), os.path.join(sprites_dir, 'enemy.png'))
    pygame.image.save(create_projectile_sprite(), os.path.join(sprites_dir, 'bullet.png'))

    # Generate Sounds
    print("Generating sounds...")
    # Shoot: High to low fast
    generate_sound(os.path.join(sounds_dir, 'shoot.wav'), 0.1, 880, 220, 0.3)
    # Explosion: Noise-like (approximated with erratic sine for simplicity without numpy)
    # Actually, let's just make a low rumble
    generate_sound(os.path.join(sounds_dir, 'explosion.wav'), 0.3, 100, 50, 0.5)

    print("Assets generated successfully!")
    pygame.quit()

if __name__ == "__main__":
    main()
