import pygame
import src.utils.utils as utils
import static.colors as colors
import static.settings as settings
from src.interface.interface_element import InterfaceElement
from src.styles.styles import StatsPanelStyle
from src.interface.text import Text


class Stat:
    def __init__(self, title: str, value: str, pos: tuple, color: pygame.Color):
        self.title = title
        self.value = value
        self.pos = pos
        self.color = color
    
    def render(self, screen: pygame.display) -> None:
        Text(color=self.color).render(screen, self.title, self.pos)
        Text(color=self.color).render(screen, self.value, utils.add_twoples(self.pos, (0, settings.FONT_SIZE)))


class Stats(InterfaceElement):
    def __init__(self):
        style = StatsPanelStyle()
        pos = (settings.WINDOW_WIDTH-style.WIDTH, 0)
        InterfaceElement.__init__(self, style, pos)
        self.stats = []
    
    def render(self, screen: pygame.display) -> None:
        self.render_transparent(screen)
        self.render_border(screen)
        self._draw_stats(screen)
    
    def add_stat(self, title: str, value: str, color: pygame.Color=colors.BLACK) -> None:
        p = (self.pos[0]+10, 10+(2*settings.FONT_SIZE*len(self.stats)))
        self.stats.append(Stat(title, value, p, color))
    
    def clear(self) -> None:
        self.stats.clear()

    def _draw_stats(self, screen: pygame.display) -> None:
        s: Stat
        for s in self.stats:
            s.render(screen)
