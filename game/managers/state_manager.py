from typing import List, Optional, Dict, Any

# It's better to use a forward reference for type hinting classes
# that might cause circular imports, like BaseScene.
# from game.scenes.base_scene import BaseScene 

class StateManager:
    """
    Manages a stack of game states (scenes) and the transitions between them.
    This allows for scenes to be pushed on top of each other (e.g., a pause menu
    over the game) and popped off to return to the previous state.
    """
    def __init__(self, initial_scene: 'BaseScene' = None):
        """
        Initializes the StateManager.

        Args:
            initial_scene (BaseScene, optional): The first scene to add to the stack.
                                                 Defaults to None.
        """
        self.scenes: List['BaseScene'] = []
        if initial_scene:
            self.push_scene(initial_scene)

    def get_active_scene(self) -> Optional['BaseScene']:
        """Returns the scene currently at the top of the stack."""
        return self.scenes[-1] if self.scenes else None

    def handle_events(self, events, pressed_keys):
        """Passes events to the active scene to be handled."""
        active_scene = self.get_active_scene()
        if active_scene:
            active_scene.handle_events(events, pressed_keys)

    def update(self, dt: float):
        """
        Updates the active scene and checks if it's requesting a state change.
        
        Args:
            dt (float): The time delta since the last frame.
        """
        active_scene = self.get_active_scene()
        if active_scene:
            active_scene.update(dt)
            # If the scene has set a next_scene, it means it wants to transition.
            if active_scene.next_scene is not None:
                self.change_scene(active_scene.next_scene)


    def draw(self, screen: 'pygame.Surface'):
        """Tells the active scene to draw itself to the screen."""
        active_scene = self.get_active_scene()
        if active_scene:
            active_scene.draw(screen)

    def push_scene(self, new_scene: 'BaseScene', **kwargs: Any):
        """

        Pauses the current scene and adds a new one to the top of the stack.

        Args:
            new_scene (BaseScene): The new scene to activate.
            **kwargs: Keyword arguments to pass to the new scene's on_enter method.
        """
        if self.scenes:
            self.get_active_scene().on_exit()
        new_scene.manager = self  # Give scene a reference to the manager
        self.scenes.append(new_scene)
        new_scene.on_enter(**kwargs)

    def pop_scene(self):
        """
        Removes the current scene from the stack and resumes the one below it.
        """
        if self.scenes:
            old_scene = self.scenes.pop()
            old_scene.on_exit()
        if self.scenes:
            # Pass any potential results from the popped scene to the new active scene
            self.get_active_scene().on_enter()

    def change_scene(self, new_scene: 'BaseScene', **kwargs: Any):
        """
        Removes all current scenes from the stack and starts a new one.

        Args:
            new_scene (BaseScene): The new scene to start.
            **kwargs: Keyword arguments to pass to the new scene's on_enter method.
        """
        while self.scenes:
            self.scenes.pop().on_exit()
        self.push_scene(new_scene, **kwargs)
