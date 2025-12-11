class BaseScene:
    def __init__(self, game_manager):
        self.game_manager = game_manager

    def on_enter(self):
        pass

    def on_exit(self):
        pass

    def handle_event(self, event):
        pass

    def update(self, dt):
        pass

    def render(self, screen):
        pass