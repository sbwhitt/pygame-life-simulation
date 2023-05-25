import pygame
import static.colors as colors
import static.settings as settings
import src.utils.utils as utils
from src.interface.interface_element import InterfaceElement
from src.styles.styles import MiniMapStyle
from src.styles.styles import MiniMapCursorStyle
from src.interface.window import Window
from src.entities.entity import Entity


class MiniMapCursor(InterfaceElement):
    def __init__(self, width: int, height: int, pos: tuple):
        InterfaceElement.__init__(self, MiniMapCursorStyle(), pos)
        self.style.WIDTH = width
        self.style.HEIGHT = height
        self.pos = pos
    
    def update(self, pos: tuple) -> None:
        self.pos = pos
    
    def render(self, screen: pygame.display) -> None:
        self.render_border(screen)


class MiniMap(InterfaceElement):
    def __init__(self, screen: pygame.display, window: Window):
        style = MiniMapStyle()
        InterfaceElement.__init__(self, style, (window.width-style.WIDTH, window.height-style.HEIGHT))
        self.screen = screen
        self.window = window
        self.map_ratio = (self.style.WIDTH / settings.WORLD_SIZE)
        self.cursor = MiniMapCursor(
            int(self.window.width * self.map_ratio),
            int(self.window.height * self.map_ratio),
            utils.add_twoples(self.pos, (2, 2)))

    def render(self, screen: pygame.display, entities: list[Entity]) -> None:
        # self.render_transparent(screen)
        self.render_border(screen)
        self._render_small_entities(screen, entities)
        self._render_cursor(screen)
    
    def _render_cursor(self, screen: pygame.display) -> None:
        offset_x_adj = int(self.window.offset[0] * self.map_ratio)
        offset_y_adj = int(self.window.offset[1] * self.map_ratio)
        self.cursor.update(utils.add_twoples(self.pos, (offset_x_adj, offset_y_adj)))
        self.cursor.render(screen)
    
    def _render_small_entities(self, screen: pygame.display, entities: list[Entity]) -> None:
        for e in entities:
            copy = e.rect.copy()
            adj_left_top = utils.add_twoples(
                utils.add_twoples(
                    self.pos,
                    (copy.left * self.map_ratio, copy.top * self.map_ratio)
                ),
                (2, 2)
            )
            copy.update(adj_left_top, (copy.width * self.map_ratio, copy.height * self.map_ratio))
            if e.dna.diseased and settings.IN_GAME_SETTINGS["MARK_DISEASED"]:
                pygame.draw.rect(screen, colors.BLACK,
                                 copy, border_radius=0)
            else:
                pygame.draw.rect(self.screen, e.dna.color, 
                                 copy, border_radius=0)
