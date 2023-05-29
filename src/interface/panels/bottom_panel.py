import pygame
import src.utils.utils as utils
import static.colors as colors
import static.settings as settings
from src.interface.interface_element import InterfaceElement
from src.styles.panel_styles import BottomPanelStyle
from src.interface.panels.panel_button import PanelButton
from src.styles.panel_styles import PanelButtonStyle
from src.interface.color_picker import ColorPicker


class BottomPanel(InterfaceElement):
    def __init__(self):
        style = BottomPanelStyle()
        pos = (0, settings.WINDOW_HEIGHT - style.HEIGHT)
        InterfaceElement.__init__(self, style, pos)
        self.panel_button = PanelButton(utils.subtract_twoples(self.pos, (0, PanelButtonStyle.HEIGHT)))
        self.panel_open = True
        self.color_picker = ColorPicker(self.pos)

    def render(self, screen: pygame.Surface) -> None:
        if self.panel_open:
            self.render_transparent(screen)
            self.render_border(screen)
            self.color_picker.render(screen)
        self.panel_button.render(screen, self.panel_open)
    
    def handle_click(self, button: int) -> None:
        if self.panel_button.hovering():
            if button == settings.LEFT_CLICK:
                self.toggle_panel()
        self.color_picker.handle_click(button)

    def toggle_panel(self) -> None:
        self.panel_open = not self.panel_open
        if self.panel_open:
            self.panel_button.pos = utils.subtract_twoples(self.pos, (0, PanelButtonStyle.HEIGHT))
        else:
            self.panel_button.pos = (0, settings.WINDOW_HEIGHT-self.panel_button.style.HEIGHT)
