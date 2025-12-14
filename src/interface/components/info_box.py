import pygame
import utils.utils as utils
from interface.interface_element import InterfaceElement
from styles.styles import InfoBoxStyle
from styles.styles import InfoMessageStyle
from interface.text import Text
from utils.clock import Clock


class InfoMessage(InterfaceElement):
    def __init__(self, pos: tuple, text: Text, message: str, duration: int=None):
        style = InfoMessageStyle()
        style.HEIGHT = text.font_size
        InterfaceElement.__init__(self, style, pos)
        self.text = text
        self.message = message
        self.duration = duration

    def render(self, screen) -> None:
        self.style.WIDTH = self.text.font.size(self.message)[0]
        self.render_transparent(screen)
        self.text.render(screen, self.message, self.pos)


class InfoBox(InterfaceElement):
    def __init__(self, pos: tuple, font_size: int):
            style = InfoBoxStyle()
            style.HEIGHT = font_size
            InterfaceElement.__init__(self, style, pos)
            self.text = Text(font_size=font_size)
            self.messages = []

    def render(self, screen: pygame.Surface, clock: Clock) -> None:
        for i in range(len(self.messages)):
            self.messages[i].pos = (self.messages[i].pos[0], i*self.text.font_size)
            self.messages[i].render(screen)
        self._check_messages(clock)

    def add_message(self, message: str, duration: int=None) -> None:
        pos_x = utils.get_centered_x_pos(self.rect, self.text.font.size(message)[0])
        pos = (pos_x, self.pos[1])
        if duration:
            self.messages.append(InfoMessage(pos, self.text, message, duration=duration))
        else:
            self.messages.append(InfoMessage(pos, self.text, message))

    def _check_messages(self, clock: Clock) -> None:
        remove = []
        m: InfoMessage
        for m in self.messages:
            if m.duration:
                if clock.metronome_counter == 0: m.duration -= 1
                if not m.duration:
                    remove.append(m)
            else:
                remove.append(m)
        for r in remove: self.messages.remove(r)
