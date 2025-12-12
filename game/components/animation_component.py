import pygame

class AnimationComponent:
    def __init__(self, sprite_sheet, frame_width, frame_height):
        self.sprite_sheet = sprite_sheet
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.animations = {}
        self.current_animation = None
        self.current_frame_index = 0
        self.timer = 0
        self.frame_duration = 0.1 # Default duration per frame

    def add_animation(self, name, row_index, num_frames):
        frames = []
        for i in range(num_frames):
            x = i * self.frame_width
            y = row_index * self.frame_height
            rect = pygame.Rect(x, y, self.frame_width, self.frame_height)
            try:
                # Ensure the rect is within the sprite sheet
                if rect.right <= self.sprite_sheet.get_width() and rect.bottom <= self.sprite_sheet.get_height():
                     frames.append(self.sprite_sheet.subsurface(rect))
                else:
                    print(f"Warning: Frame {i} in animation {name} is out of bounds.")
            except ValueError as e:
                print(f"Error creating subsurface for animation {name}, frame {i}: {e}")

        if frames:
            self.animations[name] = frames

    def set_animation(self, name):
        if self.current_animation != name and name in self.animations:
            self.current_animation = name
            self.current_frame_index = 0
            self.timer = 0

    def update(self, dt):
        if self.current_animation:
            self.timer += dt
            if self.timer >= self.frame_duration:
                self.timer = 0
                frames = self.animations[self.current_animation]
                self.current_frame_index = (self.current_frame_index + 1) % len(frames)

    def get_current_frame(self):
        if self.current_animation:
            return self.animations[self.current_animation][self.current_frame_index]
        return None
