import pygame
import sys
import asyncio
import logging
from config import SCREEN_WIDTH, SCREEN_HEIGHT, CAPTION, FPS
from game.managers.scene_manager import SceneManager
from game.scenes.menu_scene import MenuScene
from game.scenes.game_scene import GameScene
from game.scenes.resume_scene import ResumeScene
from game.scenes.about_scene import AboutScene
from game.utils.event_bus import EventBus
from game.utils.logger import setup_logging

class Game:
    def __init__(self):
        setup_logging()
        self.logger = logging.getLogger("Game")
        self.logger.info("Initializing Game...")

        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(CAPTION)
        self.clock = pygame.time.Clock()
        self.running = True

        self.event_bus = EventBus() # REQ-TECH-02

        self.scene_manager = SceneManager(self.event_bus)
        self.scene_manager.add_scene("menu_scene", MenuScene(self))
        self.scene_manager.add_scene("game_scene", GameScene(self))
        self.scene_manager.add_scene("resume_scene", ResumeScene(self))
        self.scene_manager.add_scene("about_scene", AboutScene(self))
        self.scene_manager.set_scene("menu_scene")

    def handle_events(self):
        events = pygame.event.get()
        self.scene_manager.handle_events(events)
        for event in events:
            if event.type == pygame.QUIT:
                self.logger.info("Quit event received.")
                self.running = False

    def update(self):
        dt = self.clock.get_time() / 1000.0  # Delta time in seconds
        # REQ-TECH-03: Clamp dt to max 0.1s to prevent physics explosions
        if dt > 0.1:
            self.logger.warning(f"Lag spike detected. dt={dt} clamped to 0.1")
            dt = 0.1
        self.scene_manager.update(dt)

    def draw(self):
        self.scene_manager.draw(self.screen)
        pygame.display.flip()

    async def run(self):
        self.logger.info("Starting Game Loop...")
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
            await asyncio.sleep(0) # Required for pygbag / web assembly

        self.logger.info("Game Loop ended. Quitting.")
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    asyncio.run(game.run())
