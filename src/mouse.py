import pygame
import src.utils as utils
import static.colors as colors
import static.settings as settings
from src.entity_manager import EntityManager


class Mouse:
    def __init__(self):
        self.drag_start = (0, 0)
        self.dragging = False
        self.click_timer = 0
        self.spawn_modulus = 250
        self.spawn_interval = 0
        self.deltas = [(settings.ENT_WIDTH, 0), (-settings.ENT_WIDTH, 0), (0, -settings.ENT_WIDTH), (0, settings.ENT_WIDTH)]

    def spawn_outward(self, e_man: EntityManager, pos: tuple, elapsed) -> None:
        if self._increase(elapsed):
            color = utils.get_random_color()
            for i in range(0, len(self.deltas)):
                d = utils.multiply_twople_by_constant(self.deltas[i], self.spawn_interval)
                pos_i = (utils.add_twoples(pos, d))
                e_man.place_entity(pos_i, color)

    def stop_spawn(self) -> None:
        self.click_timer = 0
        self.spawn_interval = False

    def highlight_cursor(self, screen: pygame.display) -> None:
        pos = pygame.mouse.get_pos()
        points = [(pos[0]-(pos[0] % settings.ENT_WIDTH), pos[1]-(pos[1] % settings.ENT_WIDTH)),
                  (pos[0]+(settings.ENT_WIDTH - pos[0] % settings.ENT_WIDTH),
                   pos[1]-(pos[1] % settings.ENT_WIDTH)),
                  (pos[0]+(settings.ENT_WIDTH - pos[0] % settings.ENT_WIDTH),
                   pos[1]+(settings.ENT_WIDTH - pos[1] % settings.ENT_WIDTH)),
                  (pos[0]-(pos[0] % settings.ENT_WIDTH), pos[1]+(settings.ENT_WIDTH - pos[1] % settings.ENT_WIDTH))]
        pygame.draw.lines(screen, colors.BLACK, True, points=points)

    def get_drag_dir(self) -> tuple:
        pos = pygame.mouse.get_pos()
        dirx = 0
        diry = 0
        if pos[0] > self.drag_start[0]:
            dirx = settings.ENT_WIDTH*2
        elif pos[0] < self.drag_start[0]:
            dirx = -settings.ENT_WIDTH*2
        if pos[1] > self.drag_start[1]:
            diry = settings.ENT_WIDTH*2
        elif pos[1] < self.drag_start[1]:
            diry = -settings.ENT_WIDTH*2

        return (dirx, diry)

    def _increase(self, elapsed) -> bool:
        self.click_timer += elapsed
        if int(self.click_timer / self.spawn_modulus) + 1 > self.spawn_interval:
            self.spawn_interval = int(self.click_timer / self.spawn_modulus) + 1
            return True
        return False
