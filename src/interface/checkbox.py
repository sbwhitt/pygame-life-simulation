import pygame
import src.utils.utils as utils
import static.colors as colors
import static.settings as settings
from src.interface.interface_element import InterfaceElement
from src.styles.styles import CheckboxStyle


class Checkbox(InterfaceElement):
    def __init__(self, pos: tuple):
        style = CheckboxStyle()
        InterfaceElement.__init__(self, style, pos)

    def render(self, screen: pygame.Surface) -> None:
        self.render_opaque(screen)
        self.render_border(screen)
