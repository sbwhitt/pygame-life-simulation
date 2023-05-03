import pygame
import colors
import settings

class Stats:
  def __init__(self, screen, width):
    pygame.init()
    pygame.font.init()
    self.font = pygame.font.Font(pygame.font.get_default_font(), settings.FONT_SIZE)
    self.screen = screen
    self.width = width
    self.lines = []

  def add_line(self, content, color=colors.BLACK):
    self.lines.append(pygame.font.Font.render(self.font, content, True, color))
  
  def draw_lines(self):
    for i in range(len(self.lines)):
      self.screen.blit(self.lines[i], (self.width+10, i*settings.FONT_SIZE))
  
  def clear(self):
    self.lines = []
