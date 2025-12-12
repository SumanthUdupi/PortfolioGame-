import pygame
from game.entities.entity import Entity
from game.managers.input_manager import InputManager
from game.components.animation_component import AnimationComponent
from config import BLACK, WHITE

class Player(Entity):
    def __init__(self, x, y, width, height, asset_key=None, image=None):
        # Pass None as asset_key to Entity init to avoid default scaling of the spritesheet
        # We will handle the image setting via animation component
        super().__init__(x, y, width, height, image=image)
        self.speed = 200 # pixels per second
        self.input_manager = InputManager() # Singleton instance

        self.animation = None

        if asset_key:
            spritesheet = self.asset_manager.get_image(asset_key)
            if not spritesheet:
                 spritesheet = self.asset_manager.load_image(asset_key)

            if spritesheet:
                sheet_width = spritesheet.get_width()
                sheet_height = spritesheet.get_height()

                # Assume 4 rows
                frame_h = sheet_height // 4
                # Assume 4 columns (frames)
                frame_w = sheet_width // 4

                self.animation = AnimationComponent(spritesheet, frame_w, frame_h)
                self.animation.add_animation("down", 0, 4)
                self.animation.add_animation("left", 1, 4)
                self.animation.add_animation("right", 2, 4)
                self.animation.add_animation("up", 3, 4)
                self.animation.set_animation("down")

                # Set initial image
                current_frame = self.animation.get_current_frame()
                if current_frame:
                    self.image = pygame.transform.scale(current_frame, (self.width, self.height))


    def update(self, dt, velocity_override=None):
        if velocity_override:
            self.velocity = pygame.math.Vector2(velocity_override)
        else:
            self.velocity.x = 0
            self.velocity.y = 0

            if self.input_manager.is_key_held(pygame.K_LEFT) or self.input_manager.is_key_held(pygame.K_a):
                self.velocity.x = -1
            if self.input_manager.is_key_held(pygame.K_RIGHT) or self.input_manager.is_key_held(pygame.K_d):
                self.velocity.x = 1
            if self.input_manager.is_key_held(pygame.K_UP) or self.input_manager.is_key_held(pygame.K_w):
                self.velocity.y = -1
            if self.input_manager.is_key_held(pygame.K_DOWN) or self.input_manager.is_key_held(pygame.K_s):
                self.velocity.y = 1

            # Normalize diagonal movement
            if self.velocity.length() > 0:
                self.velocity.normalize_ip()

        # Update animation based on direction
        if self.velocity.length() > 0:
            if self.animation:
                if self.velocity.y > 0:
                    self.animation.set_animation("down")
                elif self.velocity.y < 0:
                    self.animation.set_animation("up")
                elif self.velocity.x > 0:
                    self.animation.set_animation("right")
                elif self.velocity.x < 0:
                    self.animation.set_animation("left")

        # Animation update
        if self.animation:
            self.animation.update(dt)
            current_frame = self.animation.get_current_frame()
            if current_frame:
                 self.image = pygame.transform.scale(current_frame, (self.width, self.height))

            # Idle frame logic (REQ-VISUAL-04: Idle frame when velocity == 0)
            if self.velocity.length() == 0:
                 # Reset to first frame of current animation or specific idle animation?
                 # Requirement says "Idle frame when velocity == 0". Usually frame 0 is idle.
                 self.animation.current_frame_index = 0
                 # We need to update image immediately
                 current_frame = self.animation.get_current_frame()
                 if current_frame:
                      self.image = pygame.transform.scale(current_frame, (self.width, self.height))

        super().update(dt) # Call parent's update for position change

    def draw(self, screen):
        super().draw(screen)
