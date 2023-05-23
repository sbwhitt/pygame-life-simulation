import pygame
import src.utils.utils as utils
from src.styles.styles import Style


class InterfaceElement:
    def __init__(self, style: Style, pos: tuple):
        self.style = style
        self.pos = utils.add_twoples(pos, self.style.MARGIN)
        self.rect = pygame.rect.Rect(self.pos[0],
                                     self.pos[1],
                                     self.style.WIDTH,
                                     self.style.HEIGHT)

    def render_hover(self, screen: pygame.display) -> None:
        pygame.draw.rect(screen, self.style.COLOR, self.rect)
        self.render_border(screen)
    
    def render_transparent(self, screen: pygame.display) -> None:
        utils.draw_rect_alpha(screen,
                              utils.get_color_transparent(self.style.COLOR, self.style.ALPHA),
                              self.rect)
    
    def render_border(self, screen: pygame.display) -> None:
        pygame.draw.lines(screen,
                          self.style.BORDER_COLOR,
                          True,
                          utils.get_rect_outline(self.rect),
                          self.style.BORDER_WIDTH)
    
    def hovering(self) -> bool:
        return utils.within_rect(pygame.mouse.get_pos(), self.rect)
