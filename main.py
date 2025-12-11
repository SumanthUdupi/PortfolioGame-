import pygame
import sys
from config import SCREEN_WIDTH, SCREEN_HEIGHT, CAPTION, FPS
from game.managers.asset_manager import AssetManager
from game.managers.input_manager import InputManager
from game.managers.scene_manager import SceneManager
from game.managers.audio_manager import AudioManager

# Import scenes later to avoid circular imports if needed,
# but best to do it inside methods or after class def if tightly coupled.
# For now, we will import them in the setup method.

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(CAPTION)
        self.clock = pygame.time.Clock()
        self.running = True

        self.asset_manager = AssetManager()
        self.input_manager = InputManager()
        self.scene_manager = SceneManager(self)
        self.audio_manager = AudioManager(self.asset_manager)

        self.score = 0
        self.high_score = 0

    def load_assets(self):
        # Load core assets
        self.asset_manager.load_image('player', 'player.png')
        self.asset_manager.load_image('enemy', 'enemy.png')
        self.asset_manager.load_image('bullet', 'bullet.png')
        self.asset_manager.load_sound('shoot', 'shoot.wav')
        self.asset_manager.load_sound('explosion', 'explosion.wav')

    def run(self):
        self.load_assets()

        # Initial Scene
        from game.scenes.title_scene import TitleScene
        self.scene_manager.change_scene(TitleScene(self.scene_manager))

        while self.running:
            dt = self.clock.tick(FPS) / 1000.0  # Delta time in seconds

            self.input_manager.update()
            if self.input_manager.quit_requested:
                self.running = False

            self.scene_manager.update(dt)
            self.scene_manager.draw(self.screen)

            pygame.display.flip()

        pygame.quit()
        sys.exit()

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
