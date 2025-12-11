class SceneManager:
    def __init__(self, game):
        self.game = game
        self.current_scene = None

    def change_scene(self, new_scene):
        if self.current_scene:
            self.current_scene.exit()
        self.current_scene = new_scene
        self.current_scene.enter()

    def update(self, dt):
        if self.current_scene:
            self.current_scene.update(dt)

    def draw(self, screen):
        if self.current_scene:
            self.current_scene.draw(screen)

class Scene:
    def __init__(self, manager):
        self.manager = manager
        self.game = manager.game

    def enter(self):
        pass

    def exit(self):
        pass

    def update(self, dt):
        pass

    def draw(self, screen):
        pass
