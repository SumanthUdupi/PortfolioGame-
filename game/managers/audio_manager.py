import pygame
from config import *

class AudioManager:
    def __init__(self):
        pygame.mixer.init()
        self.master_volume = MASTER_VOLUME
        self.sfx_volume = SFX_VOLUME
        self.music_volume = MUSIC_VOLUME
        self.current_music = None

    def set_master_volume(self, volume):
        self.master_volume = max(0.0, min(1.0, volume))
        self._update_volumes()

    def set_sfx_volume(self, volume):
        self.sfx_volume = max(0.0, min(1.0, volume))
        self._update_volumes()

    def set_music_volume(self, volume):
        self.music_volume = max(0.0, min(1.0, volume))
        self._update_volumes()

    def _update_volumes(self):
        # Update all currently playing sounds
        pass  # Placeholder - would update active sounds

    def play_sound(self, sound_path, volume=1.0):
        # Placeholder: print text feedback instead of playing sound
        print(f"[AUDIO] Playing sound: {sound_path} at volume {volume * self.sfx_volume * self.master_volume}")
        # In real implementation: load and play sound with adjusted volume

    def play_music(self, music_path, loop=True):
        if self.current_music != music_path:
            self.current_music = music_path
            print(f"[AUDIO] Playing music: {music_path} at volume {self.music_volume * self.master_volume}")
            # In real implementation: load and play music with adjusted volume

    def stop_music(self):
        self.current_music = None
        print("[AUDIO] Music stopped")
        # In real implementation: pygame.mixer.music.stop()

    def pause_music(self):
        print("[AUDIO] Music paused")
        # In real implementation: pygame.mixer.music.pause()

    def resume_music(self):
        print("[AUDIO] Music resumed")
        # In real implementation: pygame.mixer.music.unpause()