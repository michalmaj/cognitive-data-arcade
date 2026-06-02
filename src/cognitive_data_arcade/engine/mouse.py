from __future__ import annotations
import pygame


def hit(rect: pygame.Rect, pos: tuple[int, int]) -> bool:
    return rect.collidepoint(pos)
