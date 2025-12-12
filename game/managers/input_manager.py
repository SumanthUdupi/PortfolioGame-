import pygame

class InputManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(InputManager, cls).__new__(cls)
            cls._instance.keyboard_state = {}
            cls._instance.prev_keyboard_state = {}
            cls._instance.mouse_pos = (0, 0)
            cls._instance.mouse_buttons = (0, 0, 0) # left, middle, right
            cls._instance.prev_mouse_buttons = (0, 0, 0)
        return cls._instance

    def update(self):
        self.prev_keyboard_state = self.keyboard_state
        self.keyboard_state = pygame.key.get_pressed()

        self.prev_mouse_buttons = self.mouse_buttons
        self.mouse_buttons = pygame.mouse.get_pressed()
        self.mouse_pos = pygame.mouse.get_pos()

    def is_key_pressed(self, key):
        return self.keyboard_state[key] and not self.prev_keyboard_state[key]

    def is_key_held(self, key):
        return self.keyboard_state[key]

    def is_key_released(self, key):
        return not self.keyboard_state[key] and self.prev_keyboard_state[key]

    def get_mouse_pos(self):
        return self.mouse_pos

    def is_mouse_button_pressed(self, button):
        return self.mouse_buttons[button] and not self.prev_mouse_buttons[button]

    def is_mouse_button_held(self, button):
        return self.mouse_buttons[button]

    def is_mouse_button_released(self, button):
        return not self.mouse_buttons[button] and self.prev_mouse_buttons[button]
