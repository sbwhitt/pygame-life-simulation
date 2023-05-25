import pygame
import static.settings as settings
import static.colors as colors


# TODO: create font objects at program start and pass to Text objects as param to avoid creating new font objects every time
class Text:
    def __init__(self, font_size: int=settings.FONT_SIZE, color: pygame.Color=colors.BLACK):
        self.font_size = font_size
        self.color = color
        self.font = self._init_font()
    
    def render(self, screen: pygame.display, text: str, pos: tuple) -> None:
        screen.blit(self.font.render(text, True, self.color), pos)

    # helpers

    def _init_font(self) -> pygame.font.Font:
        pygame.font.init()
        return pygame.font.Font(pygame.font.get_default_font(), self.font_size)