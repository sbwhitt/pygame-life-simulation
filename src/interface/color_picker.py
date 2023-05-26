import pygame
import src.utils.utils as utils
import static.settings as settings
from src.interface.interface_element import InterfaceElement
from src.styles.styles import ColorPickerStyle
from src.styles.styles import ColorPickerOptionStyle
from src.utils.clock import Clock


class ColorPickerOption(InterfaceElement):
    def __init__(self, pos: tuple):
        style = ColorPickerOptionStyle()
        InterfaceElement.__init__(self, style, pos)
        self.hidden = True
        self.updated = False
    
    def update(self, clock: Clock) -> None:
        if clock.metronome_counter == 0:
            self.style.COLOR = utils.get_random_color()
    
    def select_color(self) -> pygame.Color:
        return self.style.COLOR


class ColorPicker(InterfaceElement):
    def __init__(self, pos: tuple):
        style = ColorPickerStyle()
        InterfaceElement.__init__(self, style, pos)
        self.style.COLOR = utils.get_random_color()
        self.current_color = self.style.COLOR
        self.menu_open = False
        option_pos = utils.add_twoples(self.pos, (0, self.style.HEIGHT))
        self.color_picker_option = ColorPickerOption(option_pos)
    
    def render(self, screen: pygame.display, clock: Clock) -> None:
        if self.menu_open:
            self.render_hover(screen)
            self.color_picker_option.update(clock)
            self.color_picker_option.render(screen)
        elif self.hovering():
            self.render_hover(screen)
        else:
            self.render_transparent(screen)
            self.render_border(screen)

    def handle_click(self, button: int) -> None:
        if self._contains_click(button):
            self._toggle_menu()
        elif self._contains_option_click(button):
            self._update_current_color(self.color_picker_option.select_color())
            self._toggle_menu()
    
    # helpers

    def _toggle_menu(self) -> None:
        self.menu_open = not self.menu_open
        self.color_picker_option.hidden = not self.color_picker_option.hidden
    
    def _update_current_color(self, color: pygame.Color) -> None:
        self.style.COLOR = color
        self.current_color = color

    def _contains_click(self, button: int) -> bool:
        if button == settings.LEFT_CLICK:
            return self.hovering()
    
    def _contains_option_click(self, button: int) -> bool:
        if button == settings.LEFT_CLICK:
            if self.color_picker_option.hovering() and self.menu_open:
                return True
        return False
