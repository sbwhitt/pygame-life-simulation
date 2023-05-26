import pygame
import src.utils.utils as utils
import static.colors as colors
import static.settings as settings
from src.interface.interface_element import InterfaceElement
from src.styles.styles import ColorPickerStyle
from src.styles.styles import ColorPickerOptionStyle


class ColorPickerOption(InterfaceElement):
    def __init__(self, option: str, pos: tuple, color: pygame.color):
        style = ColorPickerOptionStyle()
        style.COLOR = color
        self.control_color = color
        InterfaceElement.__init__(self, style, pos)
        self.option = option
        self.hidden = True
        self.updated = False
    
    def render(self, screen: pygame.display) -> None:
        self.render_opaque(screen)
        if self.hovering():
            self.render_border(screen)
    
    def pick_color(self, pos: tuple) -> None:
        x_adj = utils.subtract_twoples(pos, self.pos)[0]
        ratio = x_adj/self.style.WIDTH
        self.style.COLOR = utils.multiply_color(self.control_color, ratio)


class ColorPicker(InterfaceElement):
    def __init__(self, pos: tuple):
        style = ColorPickerStyle()
        InterfaceElement.__init__(self, style, pos)
        self.menu_open = False
        self.options = self._build_options([settings.COLOR_PICKER_OPTIONS[0],
                             settings.COLOR_PICKER_OPTIONS[1],
                             settings.COLOR_PICKER_OPTIONS[2]])
        self.style.COLOR = utils.get_random_color()
        self.current_color = self.style.COLOR
    
    def render(self, screen: pygame.display) -> None:
        if self.menu_open:
            self.render_hover(screen)
            self._render_menu_options(screen)
        elif self.hovering():
            self.render_hover(screen)
        else:
            self.render_transparent(screen)
            self.render_border(screen)

    def handle_click(self, button: int) -> None:
        if self._contains_click(button):
            self._toggle_menu()
        self._handle_option_click(button)
    
    # helpers

    def _render_menu_options(self, screen: pygame.display) -> None:
        if not self.menu_open:
            return
        o: ColorPickerOption
        for o in self.options:
            o.render(screen)

    def _toggle_menu(self) -> None:
        self.menu_open = not self.menu_open
        o: ColorPickerOption
        for o in self.options:
            o.hidden = not o.hidden

    def _contains_click(self, button: int) -> bool:
        if button == settings.LEFT_CLICK:
            return self.hovering()
    
    def _handle_option_click(self, button: int) -> bool:
        if button == settings.LEFT_CLICK:
            o: ColorPickerOption
            for o in self.options:
                if o.hovering():
                    self._pick_option(o, pygame.mouse.get_pos())

    def _set_current_color(self) -> None:
        self.style.COLOR = self._build_current_color()
        self.current_color = self._build_current_color()

    def _build_current_color(self) -> pygame.Color:
        c = pygame.Color(0, 0, 0)
        o: ColorPickerOption
        for o in self.options:
            c += o.style.COLOR
        return c

    def _build_options(self, options: list[str]) -> list[ColorPickerOption]:
        ops = []
        for i in range(len(options)):
            if settings.COLOR_PICKER_OPTIONS[i] == "Red":
                ops.append(self._build_option(options[i], i, colors.RED))
            if settings.COLOR_PICKER_OPTIONS[i] == "Green":
                ops.append(self._build_option(options[i], i, colors.GREEN))
            if settings.COLOR_PICKER_OPTIONS[i] == "Blue":
                ops.append(self._build_option(options[i], i, colors.BLUE))
        return ops
    
    def _build_option(self, option: str, offset: int, color: pygame.Color) -> ColorPickerOption:
        y_off = self.style.HEIGHT + (ColorPickerOptionStyle.HEIGHT*offset)
        p_adj = utils.add_twoples(self.pos, (0, y_off))
        return ColorPickerOption(option, p_adj, color)

    def _pick_option(self, option: ColorPickerOption, pos: tuple) -> None:
        option.pick_color(pos)
        self._set_current_color()
