import pygame

class Entity:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.components = {}

    def add_component(self, component_type, component):
        self.components[component_type] = component

    def get_component(self, component_type):
        return self.components.get(component_type)

    def has_component(self, component_type):
        return component_type in self.components

    def update(self, dt):
        for component in self.components.values():
            if hasattr(component, 'update'):
                component.update(dt)

    def render(self, screen, camera_x=0, camera_y=0):
        for component in self.components.values():
            if hasattr(component, 'render'):
                component.render(screen, self.x - camera_x, self.y - camera_y)

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)