import pygame

class UIPanel:
    def __init__(self, x, y, width, height, asset_manager):
        self.rect = pygame.Rect(x, y, width, height)
        # Assuming asset_manager has a 'panel_9slice.png' or similar.
        # Since I don't have it, I'll generate a placeholder if missing or implement a basic draw.
        # But REQ-VISUAL-08 specifically asks for 9-slice.

        self.patch_size = 10 # Corner size
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.asset_manager = asset_manager

        # Try to load panel asset, else draw rounded rect
        self.panel_asset = self.asset_manager.get_image("ui/panel_9slice.png")
        if not self.panel_asset:
             # Try load
             self.panel_asset = self.asset_manager.load_image("ui/panel_9slice.png")

        self.redraw()

    def redraw(self):
        self.image.fill((0,0,0,0))
        if self.panel_asset:
            self.draw_9slice(self.image, self.rect.width, self.rect.height)
        else:
            # Fallback: Rounded rect with border
            pygame.draw.rect(self.image, (50, 50, 50, 200), (0, 0, self.rect.width, self.rect.height), 0, 10)
            pygame.draw.rect(self.image, (200, 200, 200), (0, 0, self.rect.width, self.rect.height), 2, 10)

    def draw_9slice(self, surface, width, height):
        # Implementation of 9-slice scaling
        # Assuming panel_asset is 3x3 patches
        w = self.panel_asset.get_width()
        h = self.panel_asset.get_height()
        cw = w // 3 # Corner width
        ch = h // 3 # Corner height

        # Corners
        # Top-Left
        surface.blit(self.panel_asset, (0, 0), (0, 0, cw, ch))
        # Top-Right
        surface.blit(self.panel_asset, (width - cw, 0), (w - cw, 0, cw, ch))
        # Bottom-Left
        surface.blit(self.panel_asset, (0, height - ch), (0, h - ch, cw, ch))
        # Bottom-Right
        surface.blit(self.panel_asset, (width - cw, height - ch), (w - cw, h - ch, cw, ch))

        # Edges
        # Top
        top_edge = pygame.transform.scale(self.panel_asset.subsurface((cw, 0, cw, ch)), (width - 2*cw, ch))
        surface.blit(top_edge, (cw, 0))
        # Bottom
        bottom_edge = pygame.transform.scale(self.panel_asset.subsurface((cw, h - ch, cw, ch)), (width - 2*cw, ch))
        surface.blit(bottom_edge, (cw, height - ch))
        # Left
        left_edge = pygame.transform.scale(self.panel_asset.subsurface((0, ch, cw, ch)), (cw, height - 2*ch))
        surface.blit(left_edge, (0, ch))
        # Right
        right_edge = pygame.transform.scale(self.panel_asset.subsurface((w - cw, ch, cw, ch)), (cw, height - 2*ch))
        surface.blit(right_edge, (width - cw, ch))

        # Center
        center = pygame.transform.scale(self.panel_asset.subsurface((cw, ch, cw, ch)), (width - 2*cw, height - 2*ch))
        surface.blit(center, (cw, ch))

    def draw(self, screen):
        screen.blit(self.image, self.rect)
