import pygame
from config import KEY_BINDINGS

class InputManager:
    def __init__(self):
        self.keys_pressed = {}
        self.mouse_pos = (0, 0)
        self.mouse_buttons = [False, False, False]
        self.quit_requested = False

        # Gamepad initialization
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
        else:
            self.joystick = None

    def update(self):
        self.keys_pressed = pygame.key.get_pressed()
        self.mouse_pos = pygame.mouse.get_pos()
        self.mouse_buttons = pygame.mouse.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_requested = True

    def is_action_pressed(self, action_name):
        """
        Checks if the action (e.g., 'left', 'shoot') is triggered by
        Keyboard or Gamepad.
        """
        # Keyboard check
        keys = KEY_BINDINGS.get(action_name, [])
        for key in keys:
            if self.keys_pressed[key]:
                return True

        # Mouse check for shooting
        if action_name == 'shoot' and self.mouse_buttons[0]:
            return True

        # Gamepad check
        if self.joystick:
            if action_name == 'left':
                return self.joystick.get_axis(0) < -0.5
            elif action_name == 'right':
                return self.joystick.get_axis(0) > 0.5
            elif action_name == 'up':
                return self.joystick.get_axis(1) < -0.5
            elif action_name == 'down':
                return self.joystick.get_axis(1) > 0.5
            elif action_name in ['shoot', 'confirm']:
                return self.joystick.get_button(0) # Button 0 (A/Cross)

        return False
