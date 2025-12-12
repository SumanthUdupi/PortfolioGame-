class SceneManager:
    def __init__(self):
        self.scenes = {}
        self.active_scene = None

    def add_scene(self, name, scene):
        self.scenes[name] = scene

    def set_scene(self, name):
        if name in self.scenes:
            if self.active_scene:
                self.active_scene.exit()
            self.active_scene = self.scenes[name]
            self.active_scene.enter()
        else:
            print(f"Warning: Scene '{name}' not found.")

    def handle_events(self, events):
        if self.active_scene:
            self.active_scene.handle_events(events)

    def update(self, dt):
        if self.active_scene:
            self.active_scene.update(dt)

    def draw(self, screen):
        if self.active_scene:
            self.active_scene.draw(screen)

