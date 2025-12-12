import pytmx
import pygame
from game.managers.asset_manager import AssetManager

class TileMapManager:
    def __init__(self):
        self.tmx_data = None
        self.map_layer = None
        self.asset_manager = AssetManager()

    def load_map(self, filename):
        # We need a full path to load with pytmx
        # Assuming maps are in assets/maps/ (need to check directory structure or assume)
        # The prompt says "render .tmx maps".
        import os
        map_path = os.path.join("assets", "maps", filename)

        try:
             self.tmx_data = pytmx.load_pygame(map_path)
        except Exception as e:
            print(f"Error loading map {map_path}: {e}")
            return

    def render(self, surface):
        if not self.tmx_data:
            return

        # Iterate over all layers
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmx_data.tilewidth,
                                            y * self.tmx_data.tileheight))
            elif isinstance(layer, pytmx.TiledObjectGroup):
                # We can handle objects here if needed
                pass
            elif isinstance(layer, pytmx.TiledImageLayer):
                if layer.image:
                     surface.blit(layer.image, (0, 0))

    def make_map_surface(self):
        if not self.tmx_data:
            return None

        temp_surface = pygame.Surface((self.tmx_data.width * self.tmx_data.tilewidth, self.tmx_data.height * self.tmx_data.tileheight))
        self.render(temp_surface)
        return temp_surface
