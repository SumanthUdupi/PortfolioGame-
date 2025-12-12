import pygame
from config import *

# Define Audio Constants here or in config.py. Putting here for module cohesion.
MUSIC_TRACKS = {
    1: "zone1_corporate_synth.mp3",
    2: "zone2_techno_server.mp3",
    3: "zone3_lofi_study.mp3",
    "menu": "menu_theme.mp3"
}

AMBIENT_TRACKS = {
    1: "ambient_office.ogg",
    2: "ambient_server_hum.ogg",
    3: "ambient_rain.ogg",
}

SOUNDS = {
    "hover": "ui_blip.wav",
    "click": "ui_click.wav",
    "typing": "keyboard_type.wav",
    "gherkin_complete": "gherkin_complete.wav",
    "api_validated": "api_validated.wav"
}

class AudioManager:
    def __init__(self, asset_manager):
        # Initialize mixer if not already done.
        # Ideally, this should be done in Game class, but safe to call multiple times.
        if not pygame.mixer.get_init():
            try:
                pygame.mixer.init()
            except pygame.error as e:
                print(f"[AUDIO] Failed to initialize mixer: {e}")

        self.asset_manager = asset_manager

        # Volume settings (0.0 to 1.0)
        self.master_volume = 1.0
        self.sfx_volume = 1.0
        self.music_volume = 1.0

        self.current_music = None
        self.current_ambient = None

        # Reserve a channel for ambient sound so it doesn't get interrupted by SFX
        # Channel 0: Ambient
        # Channel 1-7: SFX
        try:
            pygame.mixer.set_reserved(1)
            self.ambient_channel = pygame.mixer.Channel(0)
        except pygame.error:
            self.ambient_channel = None
            print("[AUDIO] Warning: Could not reserve ambient channel.")

    def set_master_volume(self, volume):
        self.master_volume = max(0.0, min(1.0, volume))
        self._update_volumes()

    def set_sfx_volume(self, volume):
        self.sfx_volume = max(0.0, min(1.0, volume))
        # No direct way to update all playing SFX unless we track them,
        # but subsequent plays will use new volume.
        # Ambient channel volume update:
        if self.ambient_channel:
            self.ambient_channel.set_volume(self.sfx_volume * self.master_volume)

    def set_music_volume(self, volume):
        self.music_volume = max(0.0, min(1.0, volume))
        try:
            pygame.mixer.music.set_volume(self.music_volume * self.master_volume)
        except pygame.error:
            pass

    def _update_volumes(self):
        self.set_music_volume(self.music_volume)
        self.set_sfx_volume(self.sfx_volume)

    def play_sound(self, sound_name_or_path, volume=1.0):
        # Allow passing key from SOUNDS dict or direct path
        path = SOUNDS.get(sound_name_or_path, sound_name_or_path)

        sound = self.asset_manager.load_sound(path)
        if sound:
            final_volume = volume * self.sfx_volume * self.master_volume
            sound.set_volume(final_volume)
            sound.play()
            return sound
        else:
            # print(f"[AUDIO] Sound not found: {path}") # Reduce spam if missing
            pass
        return None

    def play_ui_sound(self, sound_type):
        """Plays UI sounds like 'hover' or 'click'."""
        self.play_sound(sound_type)

    def play_typing_sound(self):
        """Plays a typing sound. Could be randomized in future."""
        # Random pitch variation could be added here for realism
        self.play_sound("typing", volume=0.5)

    def play_spatial_sound(self, sound_name, source_pos, listener_pos, max_dist=500):
        """
        Plays a sound with volume adjusted by distance.
        source_pos: (x, y) tuple or object with x,y
        listener_pos: (x, y) tuple or object with x,y
        """
        # Calculate distance
        dx = source_pos[0] - listener_pos[0]
        dy = source_pos[1] - listener_pos[1]
        dist = (dx*dx + dy*dy)**0.5

        if dist > max_dist:
            return # Too far

        # Linear attenuation
        # Volume = 1.0 at 0 dist, 0.0 at max_dist
        attenuation = 1.0 - (dist / max_dist)
        attenuation = max(0.0, min(1.0, attenuation))

        self.play_sound(sound_name, volume=attenuation)

    def play_music(self, track_key_or_path, fade_ms=1000, loop=True):
        """
        Crossfades to new music track.
        track_key_or_path: Key in MUSIC_TRACKS or file path.
        """
        path = MUSIC_TRACKS.get(track_key_or_path, track_key_or_path)

        if self.current_music == path:
            return # Already playing

        self.current_music = path

        # Ensure path is relative to asset manager base or handled by mixer
        # AssetManager doesn't give full path for music usually, it expects loading via pygame.mixer.music.load
        # We need to construct full path or rely on AssetManager helper if we add one.
        # But AssetManager.base_path is private-ish.
        # Let's construct path similar to AssetManager.

        import os
        full_path = os.path.join(self.asset_manager.base_path, 'sounds', 'music', path)

        # Verify file exists to avoid crashing mixer
        if not os.path.exists(full_path):
            print(f"[AUDIO] Music file not found: {full_path}")
            return

        try:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.fadeout(fade_ms)
                # Note: fadeout is blocking? No, it's non-blocking in SDL usually, but load() might stop it.
                # To do proper crossfade with music, we need to queue the next one?
                # pygame.mixer.music.queue() puts it after current one finishes.
                # But we want to interrupt and crossfade.
                # Pygame music channel doesn't support true crossfade (mixing two music streams).
                # We can only fade out then start new one.
                # We'll just load and play which stops previous one. To make it smoother, we might need a delay or accept hard cut/fast fade.
                # Actually, simply calling play() will stop the previous one.
                # If we want fade out first, we can't block here.
                # Standard pattern: just play with fadein. The old one stops abruptly.
                # To improve: define a custom event to trigger play after fadeout? Too complex for now.
                # We'll stick to: Start new one with fadein.
                pass

            pygame.mixer.music.load(full_path)
            pygame.mixer.music.set_volume(self.music_volume * self.master_volume)
            pygame.mixer.music.play(-1 if loop else 0, fade_ms=fade_ms)

        except pygame.error as e:
            print(f"[AUDIO] Error playing music {full_path}: {e}")

    def start_ambient(self, zone_id):
        """Plays ambient sound loop on dedicated channel."""
        if not self.ambient_channel:
            return

        track = AMBIENT_TRACKS.get(zone_id)
        if not track:
            self.ambient_channel.stop()
            self.current_ambient = None
            return

        if self.current_ambient == track:
            return

        self.current_ambient = track
        sound = self.asset_manager.load_sound(track) # Assume ambients are in sounds/sfx or sounds/ ?
        # Requirement says "background noise layer separate from music".
        # AssetManager.load_sound looks in 'sounds/'. We might need to specify subfolder if track string doesn't have it.
        # Let's assume track strings in constants include subfolder if needed e.g., "ambient/office.ogg"

        if sound:
            self.ambient_channel.play(sound, loops=-1, fade_ms=1000)
            self.ambient_channel.set_volume(self.sfx_volume * self.master_volume)
        else:
             self.ambient_channel.stop()

    def set_ambient_volume(self, volume_scale):
        """Sets the volume of the ambient channel (0.0 to 1.0)"""
        if self.ambient_channel:
            final_volume = volume_scale * self.sfx_volume * self.master_volume
            self.ambient_channel.set_volume(final_volume)
