import pygame
from static.settings import Settings as settings
from src.interface.interface_element import InterfaceElement
from src.styles.styles import InfoBoxStyle
from src.interface.text import Text


class InfoBox(InterfaceElement):
    def __init__(self, pos: tuple, font_size: int):
        style = InfoBoxStyle()
        style.HEIGHT = font_size
        InterfaceElement.__init__(self, style, pos)
        self.text = Text(font_size=font_size)

    def render(self, screen: pygame.Surface, message: str) -> None:
        self.style.WIDTH = self.text.font.size(message)[0]
        self.render_transparent(screen)
        self.text.render(screen, message, self.pos)
