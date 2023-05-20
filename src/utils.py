import pygame
import random

def add_coords(c1: tuple, c2: tuple) -> tuple:
    '''Returns sum of two element tuples'''
    return (c1[0] + c2[0], c1[1] + c2[1]) if len(c1) == len(c2) == 2 else None

def multiply_coord_by_constant(coord: tuple, const: int) -> tuple:
    '''Returns two element tuple with all elements multiplied by given constant'''
    return (coord[0] * const, coord[1] * const) if len(coord) == 2 else None

def get_random_color() -> pygame.Color:
    '''Returns random pygame color between values 10, 245'''
    return pygame.Color(
        random.randint(10, 245),
        random.randint(10, 245),
        random.randint(10, 245)
    )
