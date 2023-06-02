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
        InterfaceElement.__init__(self, style, pos)
        self.control_color = color
        self.current_color = color
        self.ratio = 1.0
        self.option = option
        self.hidden = False
    
    def render(self, screen: pygame.Surface) -> None:
        if self.hovering():
            self.render_opaque(screen)
        else:
            self.render_transparent(screen)
        self._render_control_rect(screen)
        self.render_border(screen)
    
    def pick_color(self, pos: tuple) -> None:
        x_adj = utils.subtract_twoples(pos, self.pos)[0]
        self.ratio = x_adj/self.style.WIDTH
        self.current_color = utils.multiply_color(self.control_color, self.ratio)

    def set_color_value(self, ratio: float, color: pygame.Color) -> None:
        self.ratio = ratio
        self.current_color = color

    # helpers

    def _render_control_rect(self, screen: pygame.Surface) -> None:
        r = self.rect.copy()
        r.width = r.width*self.ratio
        pygame.draw.rect(screen, self.control_color, r)


class ColorPicker(InterfaceElement):
    def __init__(self, pos: tuple):
        style = ColorPickerStyle()
        InterfaceElement.__init__(self, style, pos)
        self.menu_open = True
        self.options = self._build_options()
        self.style.COLOR = self._build_current_color()
        self.current_color = self._build_current_color()
    
    def render(self, screen: pygame.Surface) -> None:
        if self.menu_open:
            self.render_hover(screen)
            self._render_menu_options(screen)
        elif self.hovering():
            self.render_hover(screen)
        else:
            self.render_transparent(screen)
            self.render_border(screen)

    def handle_click(self, button: int) -> None:
        # if self._contains_click(button):
        #     self._toggle_menu()
        self._handle_option_click(button)

    def toggle_hide(self):
        self.hidden = not self.hidden
        for o in self.options:
            o.hidden = not o.hidden

    def set_color(self, color: pygame.Color) -> None:
        for o in self.options:
            if o.option == settings.COLOR_PICKER_OPTIONS[0]:
                o.set_color_value(o.control_color.r/color.r, pygame.Color(color.r, 0, 0))
            elif o.option == settings.COLOR_PICKER_OPTIONS[1]:
                o.set_color_value(o.control_color.g/color.g, pygame.Color(0, color.g, 0))
            elif o.option == settings.COLOR_PICKER_OPTIONS[2]:
                o.set_color_value(o.control_color.b/color.b, pygame.Color(0, 0, color.b))
    
    # helpers

    def _render_menu_options(self, screen: pygame.Surface) -> None:
        if not self.menu_open:
            return
        o: ColorPickerOption
        for o in self.options:
            o.render(screen)

    # def _toggle_menu(self) -> None:
    #     self.menu_open = not self.menu_open
    #     o: ColorPickerOption
    #     for o in self.options:
    #         o.hidden = not o.hidden

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
            c += o.current_color
        return c

    def _build_options(self) -> list[ColorPickerOption]:
        ops = []
        for k, v in settings.COLOR_PICKER_OPTIONS.items():
            if v == "Red":
                ops.append(self._build_option(v, k, colors.RED))
            if v == "Green":
                ops.append(self._build_option(v, k, colors.GREEN))
            if v == "Blue":
                ops.append(self._build_option(v, k, colors.BLUE))
        return ops
    
    def _build_option(self, option: str, offset: int, color: pygame.Color) -> ColorPickerOption:
        y_off = self.style.HEIGHT + (ColorPickerOptionStyle.HEIGHT*offset)
        p_adj = utils.add_twoples(self.pos, (0, y_off))
        return ColorPickerOption(option, p_adj, color)

    def _pick_option(self, option: ColorPickerOption, pos: tuple) -> None:
        option.pick_color(pos)
        self._set_current_color()
