import pygame
import src.utils.utils as utils
import static.colors as colors
import static.settings as settings
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


class Stats:
    def __init__(self, width):
        self.width = width
        self.stats = []
    
    def add_stat(self, title: str, value: str, color: pygame.Color=colors.BLACK) -> None:
        self.stats.append(Stat(title, value, (self.width+10, 2*settings.FONT_SIZE*len(self.stats)), color))

    def draw_stats(self, screen: pygame.display) -> None:
        s: Stat
        for s in self.stats:
            s.render(screen)
    
    def clear(self) -> None:
        self.stats.clear()
