import pygame
import src.utils.utils as utils
import static.colors as colors
import static.settings as settings
from src.interface.interface_element import InterfaceElement
from src.styles.panel_styles import BottomPanelStyle
from src.interface.components.panel_button import PanelButton
from src.styles.panel_styles import PanelButtonStyle
from src.interface.components.color_picker import ColorPicker
from src.interface.text import Text
from src.interface.components.chooser import Chooser
from src.styles.styles import ChooserStyle
from src.interface.components.action_menu import ActionMenu


class BottomPanel(InterfaceElement):
    def __init__(self):
        style = BottomPanelStyle()
        pos = (0, settings.WINDOW_HEIGHT - style.HEIGHT)
        InterfaceElement.__init__(self, style, pos)
        self.panel_button = PanelButton(utils.subtract_twoples(self.pos, (0, PanelButtonStyle.HEIGHT)))
        self.panel_open = True
        self.color_picker = ColorPicker(self.pos)
        self.text = Text(font_size=settings.FONT_SIZE)
        self.choosers = self._build_choosers()
        self.actions = ActionMenu(utils.add_twoples(self.pos, (self.style.WIDTH, 0)))

    def render(self, screen: pygame.Surface) -> None:
        if self.panel_open:
            self.render_transparent(screen)
            self.render_border(screen)
            self.color_picker.render(screen)
            for c in self.choosers:
                c.render(screen)
            self.actions.render(screen)
        self.panel_button.render(screen, self.panel_open)
    
    def handle_click(self, button: int) -> None:
        if self.panel_button.hovering():
            if button == settings.LEFT_CLICK:
                self.toggle_panel()
        self.color_picker.handle_click(button)
        for c in self.choosers:
            if button == settings.LEFT_CLICK and c.hovering():
                c.handle_click(settings.LEFT_CLICK)
        if button == settings.LEFT_CLICK and self.actions.hovering():
            self.actions.handle_click(settings.LEFT_CLICK)

    def toggle_panel(self) -> None:
        self.panel_open = not self.panel_open
        if self.panel_open:
            self.panel_button.pos = utils.subtract_twoples(self.pos, (0, PanelButtonStyle.HEIGHT))
            self.color_picker.toggle_hide()
            self._toggle_hide_choosers()
            self._toggle_hide_actions()
        else:
            self.panel_button.pos = (0, settings.WINDOW_HEIGHT-self.panel_button.style.HEIGHT)
            self.color_picker.toggle_hide()
            self._toggle_hide_choosers()
            self._toggle_hide_actions()

    def get_attributes(self) -> dict:
        atts = {}
        atts["color"] = self.color_picker.current_color
        for k, v in settings.CHOOSER_OPTIONS.items():
            atts[v] = self.choosers[k].selected
        return atts

    # helpers

    def _toggle_hide_choosers(self) -> None:
        for c in self.choosers:
            c.hidden = not c.hidden

    def _toggle_hide_actions(self) -> None:
        for a in self.actions.options:
            a.hidden = not a.hidden

    def _build_choosers(self) -> list[Chooser]:
        c = []
        for k, v in settings.CHOOSER_OPTIONS.items():
            c.append(self._build_chooser(v, k))
        return c
    
    def _build_chooser(self, option: str, offset: int) -> Chooser:
        pos = (self.color_picker.rect.right, self.pos[1] + (int(ChooserStyle.HEIGHT*offset*1.7)))
        return Chooser(pos, self.text, option)
