import pygame
import src.utils.utils as utils
import static.colors as colors
from static.settings import Settings as settings
from src.interface.text import Text
from src.interface.interface_element import InterfaceElement
from src.styles.styles import ActionMenuOptionStyle
from src.styles.styles import ActionMenuStyle


class ActionMenuOption(InterfaceElement):
    def __init__(self, option: str, pos: tuple, color: pygame.color):
        style = ActionMenuOptionStyle()
        style.COLOR = color
        InterfaceElement.__init__(self, style, pos)
        self.option = option
        self.selected = False
        self.text = Text(settings.FONT_SIZE_SMALLER)
    
    def render(self, screen: pygame.Surface) -> None:
        if self.hovering() or self.selected:
            self.render_hover(screen)
        else:
            self.render_transparent(screen)
        self._render_option_text(screen)
    
    # helpers

    def _render_option_text(self, screen: pygame.Surface) -> None:
        self.text.render(screen, self.option, self.pos)


# TODO: make this look better
class ActionMenu(InterfaceElement):
    def __init__(self, pos: tuple):
        style = ActionMenuStyle()
        pos = utils.subtract_twoples(pos, (style.WIDTH, 0))
        InterfaceElement.__init__(self, style, pos)
        self.positions = [(0, 0), (1, 0), (0, 1), (1, 1)]
        self.options = self._build_options()
        self.selected_option = None if len(self.options) < 1 else self.options[0]
        self._pick_option(self.selected_option)
    
    def render(self, screen: pygame.Surface) -> None:
        self._render_menu_options(screen)
    
    def handle_click(self, button: int) -> None:
        if button == settings.LEFT_CLICK:
            o: ActionMenuOption
            for o in self.options:
                if o.hovering():
                    self._pick_option(o)

    # helpers

    def _render_menu_options(self, screen: pygame.Surface) -> None:
        o: ActionMenuOption
        for o in self.options:
            o.render(screen)

    def _build_options(self) -> list[ActionMenuOption]:
        ops = []
        for k, v in settings.ACTION_MENU_OPTIONS.items():
            if v == "Create":
                ops.append(self._build_option(v, k, colors.GREEN))
            if v == "Select":
                ops.append(self._build_option(v, k, colors.CYAN))
            if v == "Delete":
                ops.append(self._build_option(v, k, colors.RED))
            if v == "Copy":
                ops.append(self._build_option(v, k, colors.ORANGE))
        return ops
    
    def _build_option(self, option: str, offset: int, color: pygame.Color) -> ActionMenuOption:
        p_off = utils.multiply_twoples(self.positions[offset], (ActionMenuOptionStyle.WIDTH, ActionMenuOptionStyle.HEIGHT))
        p_adj = utils.add_twoples(self.pos, p_off)
        return ActionMenuOption(option, p_adj, color)

    def _pick_option(self, option: ActionMenuOption) -> None:
        self.selected_option.selected = False
        self.selected_option = option
        option.selected = True
