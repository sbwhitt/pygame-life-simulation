import pygame
import random
import static.settings as settings


def add_twoples(t1: tuple, t2: tuple) -> tuple:
    '''Returns sum of two element tuples'''
    return (t1[0] + t2[0], t1[1] + t2[1]) if len(t1) == len(t2) == 2 else None

def subtract_twoples(t1: tuple, t2: tuple) -> tuple:
    '''Returns difference of two element tuples'''
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

def get_color_transparent(color: pygame.Color, transparency: int) -> pygame.Color:
    '''Returns given color with transparency value applied'''
    if not (transparency >= 0 and transparency <= 255): return color
    return pygame.Color(color.r, color.g, color.b, transparency)

def get_tile_pos(t1: tuple, offset: tuple=None, top: bool=False, left: bool=False, bottom: bool=False, right: bool=False) -> tuple:
    '''
    Returns the tile start coordinates for the position given plus an optional offset.
    Returns top left point by default
    '''
    loc = add_twoples(t1, offset) if offset else t1
    if top and left:
        return (loc[0]-(loc[0] % settings.ENT_WIDTH), loc[1]-(loc[1] % settings.ENT_WIDTH))
    if top and right:
        return (loc[0]+settings.ENT_WIDTH-(loc[0] % settings.ENT_WIDTH), loc[1]-(loc[1] % settings.ENT_WIDTH))
    if bottom and left:
        return (loc[0]-(loc[0] % settings.ENT_WIDTH), loc[1]+settings.ENT_WIDTH-(loc[1] % settings.ENT_WIDTH))
    if bottom and right:
        return (loc[0]+settings.ENT_WIDTH-(loc[0] % settings.ENT_WIDTH), loc[1]+settings.ENT_WIDTH-(loc[1] % settings.ENT_WIDTH))
    return (loc[0]-(loc[0] % settings.ENT_WIDTH), loc[1]-(loc[1] % settings.ENT_WIDTH))

def get_rect_from_twoples(t1: tuple, t2: tuple) -> pygame.rect.Rect:
    '''Returns a pygame rect with top left and bottom right corners t1 and/or t2'''
    # [t1, t2, (t1[0], t2[1]), (t2[0], t1[1])]
    t1_tile_pos = get_tile_pos(t1, top=(t1[1] <= t2[1]), left=(t1[0] <= t2[0]), bottom=(t1[1] >= t2[1]), right=(t1[0] >= t2[0]))
    t2_tile_pos = get_tile_pos(t2, top=(t2[1] <= t1[1]), left=(t2[0] <= t1[0]), bottom=(t2[1] >= t1[1]), right=(t2[0] >= t1[0]))
    left = t1_tile_pos[0] if t1_tile_pos[0] < t2_tile_pos[0] else t2_tile_pos[0]
    top = t1_tile_pos[1] if t1_tile_pos[1] < t2_tile_pos[1] else t2_tile_pos[1]
    width = abs(t1_tile_pos[0] - t2_tile_pos[0])
    height = abs(t1_tile_pos[1] - t2_tile_pos[1])
    return pygame.rect.Rect(left, top, width, height)

def get_rect_outline(rect: pygame.rect.Rect, offset: tuple=(0, 0)) -> list[tuple]:
    '''Returns pygame rect vertices minus offset for rendering outline'''
    return [
        subtract_twoples(rect.topleft, offset),
        subtract_twoples(rect.topright, offset),
        subtract_twoples(rect.bottomright, offset),
        subtract_twoples(rect.bottomleft, offset)
    ]

def within_rect(pos: tuple, rect: pygame.rect.Rect) -> bool:
    '''Returns whether or not the given position is within the given rect boundaries'''
    return (pos[0] >= rect.left and
            pos[0] <= rect.right and
            pos[1] >= rect.top and
            pos[1] <= rect.bottom)

# source: https://stackoverflow.com/questions/6339057/draw-a-transparent-rectangles-and-polygons-in-pygame
def draw_rect_alpha(surface, color, rect, border_radius=-1):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect(), border_radius=border_radius)
    surface.blit(shape_surf, rect)
