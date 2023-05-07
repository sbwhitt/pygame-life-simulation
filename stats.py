import pygame
import colors
import settings


class Stats:
    def __init__(self, screen, width):
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.Font(
            pygame.font.get_default_font(), settings.FONT_SIZE)
        self.screen = screen
        self.width = width
        self.lines = []

    def add_line(self, title: str, value: str, color: pygame.Color = colors.BLACK) -> None:
        self.lines.append(pygame.font.Font.render(
            self.font, title, True, color))
        self.lines.append(pygame.font.Font.render(
            self.font, value, True, color))

    def draw_lines(self) -> None:
        for i in range(len(self.lines)):
            self.screen.blit(
                self.lines[i], (self.width+10, i*settings.FONT_SIZE))

    def clear(self) -> None:
        self.lines = []
