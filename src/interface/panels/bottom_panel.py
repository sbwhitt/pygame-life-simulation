import pygame
import src.utils.utils as utils
import static.colors as colors
import static.settings as settings
from src.interface.interface_element import InterfaceElement
from src.styles.panel_styles import BottomPanelStyle
from src.styles.panel_styles import BottomPanelOptionStyle
from src.interface.panels.panel_button import PanelButton
from src.styles.panel_styles import PanelButtonStyle


# placeholder class
class BottomPanelOption(InterfaceElement):
    def __init__(self, pos: tuple, color: pygame.Color):
        style = BottomPanelOptionStyle()
        style.COLOR = color
        InterfaceElement.__init__(self, style, pos)


class BottomPanel(InterfaceElement):
    def __init__(self):
        style = BottomPanelStyle()
        pos = (0, settings.WINDOW_HEIGHT - style.HEIGHT)
        InterfaceElement.__init__(self, style, pos)
        self.panel_button = PanelButton((0, settings.WINDOW_HEIGHT - PanelButtonStyle.HEIGHT))
        self.panel_open = False
        self.children = [BottomPanelOption(self.pos, colors.RED)]

    def render(self, screen: pygame.display) -> None:
        if self.panel_open:
            self.render_transparent(screen)
            self.render_border(screen)
            c: BottomPanelOption
            for c in self.children:
                c.render(screen)
        self.panel_button.render(screen, self.panel_open)
    
    def handle_click(self, button: int) -> None:
        if self.panel_button.hovering():
            if button == settings.LEFT_CLICK:
                self.toggle_panel()

    def toggle_panel(self) -> None:
        self.panel_open = not self.panel_open
        if self.panel_open:
            self.panel_button.pos = utils.subtract_twoples(self.pos, (0, PanelButtonStyle.HEIGHT))
        else:
            self.panel_button.pos = (0, settings.WINDOW_HEIGHT-self.panel_button.style.HEIGHT)
