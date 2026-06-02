import pygame
import pytest
from cognitive_data_arcade.engine.mouse import hit

pygame.init()


def test_hit_inside():
    rect = pygame.Rect(10, 10, 100, 50)
    assert hit(rect, (50, 30))


def test_hit_outside():
    rect = pygame.Rect(10, 10, 100, 50)
    assert not hit(rect, (200, 200))


def test_hit_edge():
    rect = pygame.Rect(10, 10, 100, 50)
    assert hit(rect, (10, 10))


def test_hit_just_outside():
    rect = pygame.Rect(10, 10, 100, 50)
    assert not hit(rect, (110, 60))
