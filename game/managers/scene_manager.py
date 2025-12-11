class SceneManager:
    def __init__(self):
        self.scenes = {}
        self.current_scene = None

    def add_scene(self, name, scene):
        self.scenes[name] = scene

    def set_scene(self, name):
        if name in self.scenes:
            if self.current_scene:
                self.current_scene.on_exit()
            self.current_scene = self.scenes[name]
            self.current_scene.on_enter()

    def handle_event(self, event):
        if self.current_scene:
            self.current_scene.handle_event(event)

    def update(self, dt):
        if self.current_scene:
            self.current_scene.update(dt)

    def render(self, screen):
        if self.current_scene:
            self.current_scene.render(screen)