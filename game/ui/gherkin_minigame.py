import pygame
import random
from config import *

class Block:
    def __init__(self, text, x, y, width, height, font):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.original_pos = (x, y)
        self.font = font
        self.is_dragging = False
        self.drag_offset = (0, 0)

    def draw(self, screen):
        color = (200, 200, 200) if not self.is_dragging else (220, 220, 220)
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)

        text_surface = self.font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

class GherkinMinigame:
    def __init__(self, game_manager, scenario_name, puzzle_data, on_complete, on_cancel=None):
        self.game_manager = game_manager
        self.scenario_name = scenario_name
        self.correct_order = puzzle_data
        self.on_complete = on_complete
        self.on_cancel = on_cancel
        self.font = pygame.font.Font(None, 24)

        if not self.correct_order:
             # Fallback or error handling
             self.correct_order = ["Error: Missing Data", "Error: Missing Data", "Error: Missing Data"]

        self.blocks = []
        self.slots = []

        self.setup_ui()

    def setup_ui(self):
        # Create slots
        start_y = 150
        slot_height = 50
        slot_width = 600
        padding = 20
        x = (SCREEN_WIDTH - slot_width) // 2

        for i, text in enumerate(["Given...", "When...", "Then..."]):
            y = start_y + i * (slot_height + padding)
            self.slots.append(pygame.Rect(x, y, slot_width, slot_height))

        # Create blocks (scrambled)
        scrambled_texts = self.correct_order.copy()
        while scrambled_texts == self.correct_order and len(scrambled_texts) > 1:
            random.shuffle(scrambled_texts)

        block_start_y = 400
        for i, text in enumerate(scrambled_texts):
            y = block_start_y + i * (slot_height + padding)
            # Center blocks initially at bottom
            self.blocks.append(Block(text, x, y, slot_width, slot_height, self.font))

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for block in self.blocks:
                    if block.rect.collidepoint(event.pos):
                        block.is_dragging = True
                        block.drag_offset = (block.rect.x - event.pos[0], block.rect.y - event.pos[1])
                        # Move to front
                        self.blocks.remove(block)
                        self.blocks.append(block)
                        break

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                for block in self.blocks:
                    if block.is_dragging:
                        block.is_dragging = False
                        self.snap_to_slot(block)
                        self.check_completion()

        elif event.type == pygame.MOUSEMOTION:
            for block in self.blocks:
                if block.is_dragging:
                    block.rect.x = event.pos[0] + block.drag_offset[0]
                    block.rect.y = event.pos[1] + block.drag_offset[1]

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.on_cancel:
                    self.on_cancel()

    def snap_to_slot(self, block):
        # Find closest slot
        best_slot = None
        min_dist = float('inf')

        for slot in self.slots:
            dist = (block.rect.centerx - slot.centerx)**2 + (block.rect.centery - slot.centery)**2
            if dist < min_dist:
                min_dist = dist
                best_slot = slot

        # If close enough to a slot, snap to it
        if best_slot and min_dist < 5000: # Threshold
            # Check if slot is occupied
            occupied = False
            for other in self.blocks:
                if other != block and other.rect.colliderect(best_slot):
                    occupied = True
                    break

            if not occupied:
                block.rect.topleft = best_slot.topleft
                return

    def check_completion(self):
        # Check if all slots are filled with correct blocks
        correct_count = 0
        for i, slot in enumerate(self.slots):
            # Safe access
            if i >= len(self.correct_order):
                break

            target_text = self.correct_order[i]
            for block in self.blocks:
                # Check if block is roughly in slot
                if abs(block.rect.x - slot.x) < 10 and abs(block.rect.y - slot.y) < 10:
                    if block.text == target_text:
                        correct_count += 1

        if correct_count == len(self.correct_order):
            self.on_complete()

    def update(self, dt):
        pass

    def draw(self, screen):
        # Draw overlay background
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(200)
        screen.blit(overlay, (0, 0))

        # Draw title
        title_surf = self.font.render(f"Construct Scenario: {self.scenario_name}", True, WHITE)
        screen.blit(title_surf, (20, 20))

        # Draw slots
        for i, slot in enumerate(self.slots):
            pygame.draw.rect(screen, (50, 50, 50), slot)
            pygame.draw.rect(screen, WHITE, slot, 2)
            # Label
            label = ["Given", "When", "Then"][i]
            label_surf = self.font.render(label, True, (150, 150, 150))
            screen.blit(label_surf, (slot.x - 60, slot.centery - 10))

        # Draw blocks
        for block in self.blocks:
            block.draw(screen)
