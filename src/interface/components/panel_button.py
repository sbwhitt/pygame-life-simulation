import pygame
import static.colors as colors
import static.settings as settings
import src.utils.utils as utils
from src.interface.interface_element import InterfaceElement
from src.styles.panel_styles import PanelButtonStyle


class PanelButton(InterfaceElement):
    def __init__(self, pos: tuple):
        style = PanelButtonStyle()
        InterfaceElement.__init__(self, style, pos)

    def render(self, screen: pygame.Surface, panel_open: bool) -> None:
        self.style.COLOR = colors.RED if panel_open else colors.GREEN
        if self.hovering():
            self.render_hover(screen)
        else:
            self.render_transparent(screen)
            self.render_border(screen)
