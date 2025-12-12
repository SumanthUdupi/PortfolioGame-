import pygame
import pytest
from game.entities.entity import Entity
from game.managers.input_manager import InputManager

# Initialize Pygame for tests that require it
pygame.init()
pygame.display.set_mode((1, 1)) # Create a dummy screen for pygame.display calls

@pytest.fixture
def dummy_entity():
    # A simple entity for testing
    return Entity(x=0, y=0, width=10, height=10)

def test_entity_initialization(dummy_entity):
    assert dummy_entity.rect.x == 0
    assert dummy_entity.rect.y == 0
    assert dummy_entity.rect.width == 10
    assert dummy_entity.rect.height == 10
    assert dummy_entity.speed == 0

def test_entity_movement(dummy_entity):
    dummy_entity.speed = 100
    dummy_entity.velocity.x = 1
    dummy_entity.velocity.y = 0
    dummy_entity.update(1) # Simulate 1 second pass
    assert dummy_entity.rect.x == 100
    assert dummy_entity.rect.y == 0

    dummy_entity.velocity.x = 0
    dummy_entity.velocity.y = 1
    dummy_entity.update(0.5) # Simulate 0.5 second pass
    assert dummy_entity.rect.x == 100
    assert dummy_entity.rect.y == 50

# Test for InputManager (requires careful mocking or special handling for pygame.key.get_pressed())
# For now, let's just ensure it can be instantiated without error
def test_input_manager_instantiation():
    input_manager = InputManager()
    assert input_manager is not None
