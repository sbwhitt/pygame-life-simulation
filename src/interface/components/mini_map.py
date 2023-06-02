import pygame
import static.colors as colors
import static.settings as settings
import src.utils.utils as utils
from src.interface.interface_element import InterfaceElement
from src.styles.panel_styles import MiniMapStyle
from src.styles.panel_styles import MiniMapCursorStyle
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
    
    def render(self, screen: pygame.Surface, boundary: pygame.Rect) -> None:
        self.rect = self.build_rect()
        lines = utils.get_rect_outline(self.rect)
        border = lines
        for i in range(len(lines)):
            l = lines[i]
            if l[0] < boundary.left: border[i] = (boundary.left, border[i][1])
            elif l[0] > boundary.right: border[i] = (boundary.right, border[i][1])
            if l[1] < boundary.top: border[i] = (border[i][0], boundary.top)
            elif l[1] > boundary.bottom: border[i] = (border[i][0], boundary.bottom)
        pygame.draw.lines(screen, colors.BLACK, True, border)



class MiniMap(InterfaceElement):
    def __init__(self, window: Window):
        style = MiniMapStyle()
        InterfaceElement.__init__(self, style, (window.width-style.WIDTH, window.height-style.HEIGHT))
        self.window = window
        self.map_ratio = self._calculate_map_ratio()
        self.small_ent_size = settings.ENT_WIDTH * self.map_ratio
        self.cursor = MiniMapCursor(
            int(self.window.width * self.map_ratio),
            int(self.window.height * self.map_ratio),
            utils.add_twoples(self.pos, (2, 2)))

    def render(self, screen: pygame.Surface, entities: list[Entity]) -> None:
        if self.hovering():
            self.style.BORDER_WIDTH = 3
        else:
            self.style.BORDER_WIDTH = 2
        self.render_border(screen)
        self._render_small_entities(screen, entities)
        self._render_cursor(screen)

    def handle_click(self, pos: tuple) -> None:
        new_off = self._calculate_window_offset(pos)
        self.window.set_offset(new_off)

    def zoom_in(self, speed: int) -> None:
        new_w = int(self.cursor.style.WIDTH / speed)
        new_h = int(self.cursor.style.HEIGHT / speed)
        self.cursor.style.WIDTH = new_w
        self.cursor.style.HEIGHT = new_h

    def zoom_out(self, speed: int) -> None:
        new_w = self.cursor.style.WIDTH * speed
        new_h = self.cursor.style.HEIGHT * speed
        self.cursor.style.WIDTH = new_w
        self.cursor.style.HEIGHT = new_h

    # helpers

    def _render_cursor(self, screen: pygame.Surface) -> None:
        ratio = self._calculate_map_ratio()
        x_adj, y_adj = int(self.window.offset[0] * ratio), int(self.window.offset[1] * ratio)
        self.cursor.update(utils.add_twoples(self.pos, (x_adj, y_adj)))
        self.cursor.render(screen, self.rect)

    def _render_small_entities(self, screen: pygame.Surface, entities: list[Entity]) -> None:
        ratio = self._calculate_map_ratio()
        for e in entities:
            copy = e.rect.copy()
            adj_left_top = utils.add_twoples(
                utils.add_twoples(
                    self.pos,
                    (copy.left * ratio, copy.top * ratio)
                ),
                (2, 2)
            )
            copy.update(adj_left_top, (self.small_ent_size, self.small_ent_size))
            if e.dna.diseased and settings.IN_GAME_SETTINGS["MARK_DISEASED"]:
                pygame.draw.rect(screen, colors.BLACK,
                                 copy, border_radius=0)
            else:
                pygame.draw.rect(screen, e.dna.color, 
                                 copy, border_radius=0)

    def _calculate_window_offset(self, pos: tuple) -> tuple:
        ratio = self._calculate_map_ratio()
        p = utils.subtract_twoples(pos, self.pos)
        pos_adj = (int(p[0]/ratio), int(p[1]/ratio))
        return utils.subtract_twoples(pos_adj, (int(self.window.width/2), int(self.window.height/2)))

    def _calculate_map_ratio(self) -> float:
        return (self.style.WIDTH / settings.WORLD_SIZE)
