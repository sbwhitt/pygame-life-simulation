import pygame
import src.utils.utils as utils
import static.colors as colors
import static.settings as settings
from src.interface.text import Text
from src.interface.interface_element import InterfaceElement
from src.styles.styles import PickerMenuOptionStyle
from src.styles.styles import PickerMenuStyle


class PickerMenuOption(InterfaceElement):
    def __init__(self, option: str, pos: tuple):
        InterfaceElement.__init__(self, PickerMenuOptionStyle(), pos)
        self.option = option
        self.hidden = True
        self.selected = False
        self.text = Text(settings.FONT_SIZE_SMALLER)
    
    def render(self, screen: pygame.display) -> None:
        if self.hovering():
            self.render_hover(screen)
        else:
            self.render_transparent(screen)
        self._render_option_text(screen)
    
    # helpers

    def _render_option_text(self, screen: pygame.display) -> None:
        self.text.render(screen, self.option, self.pos)


class PickerMenu(InterfaceElement):
    def __init__(self, pos: tuple):
        InterfaceElement.__init__(self, PickerMenuStyle(), pos)
        self.options = []
        self.menu_open = False
        self._build_options([settings.ACTION_MENU_OPTIONS[0],
                             settings.ACTION_MENU_OPTIONS[1],
                             settings.ACTION_MENU_OPTIONS[2]])
        self.selected_option = None if len(self.options) < 1 else self.options[0]
        self.title_text = Text(settings.FONT_SIZE)
        self.action_text = Text(settings.FONT_SIZE_SMALLER)
    
    def render(self, screen: pygame.display) -> None:
        if self.hovering() or self.menu_open:
            self.render_hover(screen)
        else:
            self.render_transparent(screen)
        self._render_menu_text(screen)
        if self.menu_open:
            self._render_menu_options(screen)
    
    def handle_click(self, button: int) -> None:
        # left click picker menu
            if self._contains_click(button):
                if not self.menu_open: self.open_pick_menu()
                else: self.close_pick_menu()
            # left click picker menu option
            elif self.menu_open and self._contains_option_click(button):
                self.close_pick_menu()

    def open_pick_menu(self) -> None:
        self.menu_open = True
        o: PickerMenuOption
        for o in self.options: o.hidden = False
    
    def close_pick_menu(self) -> None:
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
    
    def _render_menu_options(self, screen: pygame.display) -> None:
        if not self.menu_open:
            return
        o: PickerMenuOption
        for o in self.options:
            o.render(screen)
    
    def _render_menu_text(self, screen: pygame.display) -> None:
        self.title_text.render(screen, "Actions", self.pos)
        self.action_text.render(screen, self.selected_option.option, utils.add_twoples(self.pos, (0, settings.FONT_SIZE)))

    def _build_options(self, options: list[str]) -> list[PickerMenuOption]:
        for i in range(len(options)):
            self.options.append(self._build_option(options[i], i))
    
    def _build_option(self, option: str, offset: int) -> PickerMenuOption:
        x_off = self.style.WIDTH+(self.style.WIDTH*offset)
        p_adj = utils.add_twoples(self.pos, (x_off, 0))
        return PickerMenuOption(option, p_adj)

    def _pick_option(self, option: PickerMenuOption) -> None:
        self.selected_option = option
