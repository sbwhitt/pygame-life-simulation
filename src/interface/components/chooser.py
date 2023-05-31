import pygame
import src.utils.utils as utils
import static.colors as colors
import static.settings as settings
from src.interface.interface_element import InterfaceElement
from src.styles.styles import ChooserStyle
from src.interface.text import Text
from src.interface.components.checkbox import Checkbox


class Chooser(InterfaceElement):
    def __init__(self, pos: tuple, text: Text, option: str):
        style = ChooserStyle()
        InterfaceElement.__init__(self, style, pos)
        self.checkbox = Checkbox(self.pos)
        self.text = text
        self.option = option
        self.selected = False

    def render(self, screen: pygame.Surface) -> None:
        self.checkbox.style.COLOR = colors.BLACK if self.selected else colors.WHITE
        self.checkbox.render(screen)
        self.text.render(screen,
                        self.option,
                        utils.add_twoples(self.checkbox.pos, (self.checkbox.style.WIDTH+5, 2)))

    def handle_click(self, button: int) -> None:
        if self.checkbox.hovering() and button == settings.LEFT_CLICK:
            self.selected = not self.selected
