import pygame
from config import *

class InputManager:
    def __init__(self):
        self.keys_pressed = {}
        self.keys_held = {}
        self.mouse_pos = (0, 0)
        self.mouse_buttons = {}
        self.gamepad = None

        # Initialize gamepad if available
        if pygame.joystick.get_count() > 0:
            self.gamepad = pygame.joystick.Joystick(0)
            self.gamepad.init()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            self.keys_pressed[event.key] = True
            self.keys_held[event.key] = True
        elif event.type == pygame.KEYUP:
            self.keys_held[event.key] = False
        elif event.type == pygame.MOUSEMOTION:
            self.mouse_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.mouse_buttons[event.button] = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.mouse_buttons[event.button] = False

    def update(self, dt):
        # Clear pressed keys each frame
        self.keys_pressed.clear()
        self.mouse_buttons.clear()

    def is_key_pressed(self, key):
        return key in self.keys_pressed

    def is_key_held(self, key):
        return self.keys_held.get(key, False)

    def get_mouse_pos(self):
        return self.mouse_pos

    def is_mouse_button_pressed(self, button):
        return button in self.mouse_buttons

    def get_gamepad_axis(self, axis):
        if self.gamepad:
            return self.gamepad.get_axis(axis)
        return 0.0

    def is_gamepad_button_pressed(self, button):
        if self.gamepad:
            return self.gamepad.get_button(button)
        return False