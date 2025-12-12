from typing import Dict, Any, Optional
from game.utils.event_bus import EventBus
import logging

class SceneManager:
    def __init__(self, event_bus: Optional[EventBus] = None):
        self.scenes: Dict[str, Any] = {}
        self.active_scene: Any = None
        self.event_bus = event_bus
        self.logger = logging.getLogger("SceneManager")

    def add_scene(self, name: str, scene: Any) -> None:
        self.scenes[name] = scene

    def set_scene(self, name: str) -> None:
        if name in self.scenes:
            if self.active_scene:
                self.active_scene.exit()
            self.active_scene = self.scenes[name]
            self.active_scene.enter()
            self.logger.info(f"Switched to scene: {name}")
        else:
            self.logger.warning(f"Warning: Scene '{name}' not found.")

    def handle_events(self, events: Any) -> None:
        if self.active_scene:
            self.active_scene.handle_events(events)

    def update(self, dt: float) -> None:
        if self.active_scene:
            self.active_scene.update(dt)

    def draw(self, screen: Any) -> None:
        if self.active_scene:
            self.active_scene.draw(screen)
