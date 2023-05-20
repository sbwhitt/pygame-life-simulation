import pygame
import random
import static.settings as settings


def add_twoples(t1: tuple, t2: tuple) -> tuple:
    '''Returns sum of two element tuples'''
    return (t1[0] + t2[0], t1[1] + t2[1]) if len(t1) == len(t2) == 2 else None

def subtract_twoples(t1: tuple, t2: tuple) -> tuple:
    '''Returns sum of two element tuples'''
    return (t1[0] - t2[0], t1[1] - t2[1]) if len(t1) == len(t2) == 2 else None

def multiply_twople_by_constant(t1: tuple, const: int) -> tuple:
    '''Returns two element tuple with all elements multiplied by given constant'''
    return (t1[0] * const, t1[1] * const) if len(t1) == 2 else None

def get_random_color(start: int=-1, end: int=-1) -> pygame.Color:
    '''Returns random pygame color between given values or 10, 245 by default'''
    if (start > 0 and end > 0) and (start <= 255 and end <= 255):
        return pygame.Color(
            random.randint(start, end),
            random.randint(start, end),
            random.randint(start, end)
        )
    else:
        return pygame.Color(
            random.randint(10, 245),
            random.randint(10, 245),
            random.randint(10, 245)
        )

def get_tile_pos(t1: tuple, offset: tuple=None, top_left: bool=False, top_right: bool=False, bottom_left: bool=False, bottom_right: bool=False) -> tuple:
    '''
    Returns the tile start coordinates for the position given plus an optional offset.
    Returns top left point by default
    '''
    loc = add_twoples(t1, offset) if offset else t1
    if top_left:
        return (loc[0]-(loc[0] % settings.ENT_WIDTH), loc[1]-(loc[1] % settings.ENT_WIDTH))
    if top_right:
        return (loc[0]+(loc[0] % settings.ENT_WIDTH), loc[1]-(loc[1] % settings.ENT_WIDTH))
    if bottom_left:
        return (loc[0]-(loc[0] % settings.ENT_WIDTH), loc[1]+(loc[1] % settings.ENT_WIDTH))
    if bottom_right:
        return (loc[0]+(loc[0] % settings.ENT_WIDTH), loc[1]+(loc[1] % settings.ENT_WIDTH))
    return (loc[0]-(loc[0] % settings.ENT_WIDTH), loc[1]-(loc[1] % settings.ENT_WIDTH))

def get_rect_from_twoples(t1: tuple, t2: tuple, offset: tuple=None) -> pygame.rect.Rect:
    '''Returns a pygame rect with top left and bottom right corners t1 and/or t2'''
    # [t1, t2, (t1[0], t2[1]), (t2[0], t1[1])]
    left = t1[0] if t1[0] < t2[0] else t2[0]
    top = t1[1] if t1[1] < t2[1] else t2[1]
    width = abs(t1[0] - t2[0])
    height = abs(t1[1] - t2[1])
    return pygame.rect.Rect(left, top, width, height)
