import pygame
import src.utils.utils as utils
import static.colors as colors
import static.settings as settings
from src.interface.text import Text
from src.interface.interface_element import InterfaceElement
from src.styles.styles import PickerMenuOptionStyle
from src.styles.styles import PickerMenuStyle


class PickerMenuOption(InterfaceElement):
    def __init__(self, option: str, pos: tuple, color: pygame.color):
        style = PickerMenuOptionStyle()
        style.COLOR = color
        InterfaceElement.__init__(self, style, pos)
        self.option = option
        self.hidden = True
        self.selected = False
        self.text = Text(settings.FONT_SIZE_SMALLER)
    
    def render(self, screen: pygame.Surface) -> None:
        if self.hovering():
            self.render_hover(screen)
        else:
            self.render_transparent(screen)
            self.render_border(screen)
        self._render_option_text(screen)
    
    # helpers

    def _render_option_text(self, screen: pygame.Surface) -> None:
        self.text.render(screen, self.option, self.pos)


# TODO: make this look better
class PickerMenu(InterfaceElement):
    def __init__(self, pos: tuple):
        InterfaceElement.__init__(self, PickerMenuStyle(), pos)
        self.menu_open = False
        self.options = self._build_options([settings.ACTION_MENU_OPTIONS[0],
                             settings.ACTION_MENU_OPTIONS[1],
                             settings.ACTION_MENU_OPTIONS[2]])
        self.selected_option = None if len(self.options) < 1 else self.options[0]
        self.title_text = Text(settings.FONT_SIZE)
        self.action_text = Text(settings.FONT_SIZE_SMALLER)
    
    def render(self, screen: pygame.Surface) -> None:
        self.style.COLOR = self.selected_option.style.COLOR
        if self.hovering() or self.menu_open:
            self.render_hover(screen)
        else:
            self.render_transparent(screen)
            self.render_border(screen)
        self._render_menu_text(screen)
        if self.menu_open:
            self._render_menu_options(screen)
    
    def handle_click(self, button: int) -> None:
        # left click picker menu
            if self._contains_click(button):
                if not self.menu_open: self.open_menu()
                else: self.close_menu()
            # left click picker menu option
            elif self.menu_open and self._contains_option_click(button):
                self.close_menu()

    def open_menu(self) -> None:
        self.menu_open = True
        o: PickerMenuOption
        for o in self.options: o.hidden = False
    
    def close_menu(self) -> None:
        self.menu_open = False
        o: PickerMenuOption
        for o in self.options: o.hidden = True

    # helpers

    def _contains_click(self, button: int) -> bool:
        if button == settings.LEFT_CLICK:
            return self.hovering()
    
    def _contains_option_click(self, button: int) -> bool:
        if button == settings.LEFT_CLICK:
            o: PickerMenuOption
            for o in self.options:
                if o.hovering():
                    self._pick_option(o)
                    return True
        return False
    
    def _render_menu_options(self, screen: pygame.Surface) -> None:
        if not self.menu_open:
            return
        o: PickerMenuOption
        for o in self.options:
            o.render(screen)
    
    def _render_menu_text(self, screen: pygame.Surface) -> None:
        self.title_text.render(screen, "Actions", self.pos)
        self.action_text.render(screen, self.selected_option.option, utils.add_twoples(self.pos, (0, settings.FONT_SIZE)))

    def _build_options(self, options: list[str]) -> list[PickerMenuOption]:
        ops = []
        for i in range(len(options)):
            if settings.ACTION_MENU_OPTIONS[i] == "Selection":
                ops.append(self._build_option(options[i], i, colors.CYAN))
            if settings.ACTION_MENU_OPTIONS[i] == "Creation":
                ops.append(self._build_option(options[i], i, colors.GREEN))
            if settings.ACTION_MENU_OPTIONS[i] == "Deletion":
                ops.append(self._build_option(options[i], i, colors.RED))
        return ops
    
    def _build_option(self, option: str, offset: int, color: pygame.Color) -> PickerMenuOption:
        y_off = self.style.HEIGHT + (self.style.WIDTH*offset)
        p_adj = utils.add_twoples(self.pos, (0, y_off))
        return PickerMenuOption(option, p_adj, color)

    def _pick_option(self, option: PickerMenuOption) -> None:
        self.selected_option = option