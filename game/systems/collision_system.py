import pygame

class CollisionSystem:
    @staticmethod
    def check_collision(entity1, entity2):
        """Check bounding box collision between two entities"""
        return entity1.rect.colliderect(entity2.rect)

    @staticmethod
    def check_point_collision(point, entity):
        """Check if a point collides with an entity"""
        return entity.rect.collidepoint(point)

    @staticmethod
    def resolve_collision(entity1, entity2):
        """Basic collision resolution - push entities apart"""
        # Calculate overlap
        overlap_x = min(entity1.x + entity1.width - entity2.x, entity2.x + entity2.width - entity1.x)
        overlap_y = min(entity1.y + entity1.height - entity2.y, entity2.y + entity2.height - entity1.y)

        if overlap_x < overlap_y:
            # Resolve horizontally
            if entity1.x < entity2.x:
                entity1.x -= overlap_x / 2
                entity2.x += overlap_x / 2
            else:
                entity1.x += overlap_x / 2
                entity2.x -= overlap_x / 2
        else:
            # Resolve vertically
            if entity1.y < entity2.y:
                entity1.y -= overlap_y / 2
                entity2.y += overlap_y / 2
            else:
                entity1.y += overlap_y / 2
                entity2.y -= overlap_y / 2