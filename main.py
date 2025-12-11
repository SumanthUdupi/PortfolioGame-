import pygame
import sys
from config import *
from game.managers.game_manager import GameManager

def main():
    pygame.init()
    pygame.display.set_caption(TITLE)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    game_manager = GameManager()

    running = True
    dt = 0.0

    while running:
        dt = clock.tick(FPS) / 1000.0  # Convert to seconds

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game_manager.handle_event(event)

        game_manager.update(dt)
        game_manager.render(screen)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()