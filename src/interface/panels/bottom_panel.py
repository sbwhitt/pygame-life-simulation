import pygame
import src.utils.utils as utils
import static.colors as colors
import static.settings as settings
from src.interface.interface_element import InterfaceElement
from src.styles.panel_styles import BottomPanelStyle
from src.interface.panels.panel_button import PanelButton
from src.styles.panel_styles import PanelButtonStyle
from src.interface.color_picker import ColorPicker
from src.interface.text import Text
from src.interface.chooser import Chooser
from src.styles.styles import ChooserStyle


class BottomPanel(InterfaceElement):
    def __init__(self):
        style = BottomPanelStyle()
        pos = (0, settings.WINDOW_HEIGHT - style.HEIGHT)
        InterfaceElement.__init__(self, style, pos)
        self.panel_button = PanelButton(utils.subtract_twoples(self.pos, (0, PanelButtonStyle.HEIGHT)))
        self.panel_open = True
        self.color_picker = ColorPicker(self.pos)
        self.text = Text(font_size=settings.FONT_SIZE)
        self.choosers = self._build_choosers([settings.CHOOSER_OPTIONS[0],
                                              settings.CHOOSER_OPTIONS[1],
                                              settings.CHOOSER_OPTIONS[2]])

    def render(self, screen: pygame.Surface) -> None:
        if self.panel_open:
            self.render_transparent(screen)
            self.render_border(screen)
            self.color_picker.render(screen)
            for c in self.choosers:
                c.render(screen)
        self.panel_button.render(screen, self.panel_open)
    
    def handle_click(self, button: int) -> None:
        if self.panel_button.hovering():
            if button == settings.LEFT_CLICK:
                self.toggle_panel()
        self.color_picker.handle_click(button)
        for c in self.choosers:
            c.handle_click(button)

    def toggle_panel(self) -> None:
        self.panel_open = not self.panel_open
        if self.panel_open:
            self.panel_button.pos = utils.subtract_twoples(self.pos, (0, PanelButtonStyle.HEIGHT))
        else:
            self.panel_button.pos = (0, settings.WINDOW_HEIGHT-self.panel_button.style.HEIGHT)

    def get_attributes(self) -> dict:
        return {"color": self.color_picker.current_color,
                "diseased": self.choosers[0].selected,
                "immune": self.choosers[1].selected,
                "immortal": self.choosers[2].selected}

    # helpers

    def _build_choosers(self, choosers: list[str]) -> list[Chooser]:
        c = []
        for i in range(len(choosers)):
            if settings.CHOOSER_OPTIONS[i] == "diseased":
                c.append(self._build_chooser(choosers[i], i))
            elif settings.CHOOSER_OPTIONS[i] == "immune":
                c.append(self._build_chooser(choosers[i], i))
            elif settings.CHOOSER_OPTIONS[i] == "immortal":
                c.append(self._build_chooser(choosers[i], i))
        return c
    
    def _build_chooser(self, option: str, offset: int) -> Chooser:
        pos = (self.color_picker.rect.right, self.pos[1] + (ChooserStyle.HEIGHT*offset*2))
        return Chooser(pos, self.text, option)