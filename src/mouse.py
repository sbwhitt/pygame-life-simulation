import pygame
import static.colors as colors
import static.settings as settings


class Mouse:
    def __init__(self):
        self.drag_start = (0, 0)
        self.dragging = False
    
    def highlight_cursor(self, screen: pygame.display) -> None:
        pos = pygame.mouse.get_pos()
        points = [(pos[0]-(pos[0] % settings.ENT_WIDTH), pos[1]-(pos[1] % settings.ENT_WIDTH)),
                  (pos[0]+(settings.ENT_WIDTH - pos[0] % settings.ENT_WIDTH), pos[1]-(pos[1] % settings.ENT_WIDTH)),
                  (pos[0]+(settings.ENT_WIDTH - pos[0] % settings.ENT_WIDTH), pos[1]+(settings.ENT_WIDTH - pos[1] % settings.ENT_WIDTH)),
                  (pos[0]-(pos[0] % settings.ENT_WIDTH), pos[1]+(settings.ENT_WIDTH - pos[1] % settings.ENT_WIDTH))]
        pygame.draw.lines(screen, colors.BLACK, True, points=points)
    
    def get_drag_dir(self) -> tuple:
        pos = pygame.mouse.get_pos()
        dirx = 0
        diry = 0
        if pos[0] > self.drag_start[0]: dirx = settings.ENT_WIDTH*2
        elif pos[0] < self.drag_start[0]: dirx = -settings.ENT_WIDTH*2
        if pos[1] > self.drag_start[1]: diry = settings.ENT_WIDTH*2
        elif pos[1] < self.drag_start[1]: diry = -settings.ENT_WIDTH*2

        return (dirx, diry)
