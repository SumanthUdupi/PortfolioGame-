import pygame
import sys
from config import SCREEN_WIDTH, SCREEN_HEIGHT, CAPTION, FPS
from game.managers.scene_manager import SceneManager
from game.scenes.menu_scene import MenuScene
from game.scenes.game_scene import GameScene

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(CAPTION)
        self.clock = pygame.time.Clock()
        self.running = True

        self.scene_manager = SceneManager()
        self.scene_manager.add_scene("menu_scene", MenuScene(self))
        self.scene_manager.add_scene("game_scene", GameScene(self))
        self.scene_manager.set_scene("menu_scene")

    def handle_events(self):
        events = pygame.event.get()
        self.scene_manager.handle_events(events)
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        dt = self.clock.get_time() / 1000.0  # Delta time in seconds
        self.scene_manager.update(dt)

    def draw(self):
        self.scene_manager.draw(self.screen)
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()