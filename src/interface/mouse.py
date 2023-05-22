import pygame
import src.utils.utils as utils
import static.colors as colors
import static.settings as settings
from src.entities.entity_manager import EntityManager
from src.interface.window import Window

LEFT_CLICK = 0
MIDDLE_CLICK = 1
RIGHT_CLICK = 2


class Cursor:
    def __init__(self):
        self.start = (0, 0)
        self.end = (0, 0)
        self.rect = None

    def get_points(self) -> list[tuple]:
        pos = pygame.mouse.get_pos()
        return [(pos[0]-(pos[0] % settings.ENT_WIDTH), pos[1]-(pos[1] % settings.ENT_WIDTH)),
                  (pos[0]+(settings.ENT_WIDTH - pos[0] % settings.ENT_WIDTH),
                   pos[1]-(pos[1] % settings.ENT_WIDTH)),
                  (pos[0]+(settings.ENT_WIDTH - pos[0] % settings.ENT_WIDTH),
                   pos[1]+(settings.ENT_WIDTH - pos[1] % settings.ENT_WIDTH)),
                  (pos[0]-(pos[0] % settings.ENT_WIDTH), pos[1]+(settings.ENT_WIDTH - pos[1] % settings.ENT_WIDTH))]


class Mouse:
    def __init__(self, window: Window):
        self.window = window
        self.cursor = Cursor()
        self.drag_start = [(0, 0), (0, 0), (0, 0)]
        self.dragging = [False, False, False]
        self.click_timer = 0
        self.spawn_modulus = 250
        self.spawn_interval = 0
        self.deltas = [(settings.ENT_WIDTH, 0), (-settings.ENT_WIDTH, 0),
                       (0, -settings.ENT_WIDTH), (0, settings.ENT_WIDTH),
                       (settings.ENT_WIDTH, settings.ENT_WIDTH), (-settings.ENT_WIDTH, settings.ENT_WIDTH),
                       (settings.ENT_WIDTH, -settings.ENT_WIDTH), (-settings.ENT_WIDTH, -settings.ENT_WIDTH)]

    def spawn_outward(self, e_man: EntityManager, pos: tuple, elapsed) -> None:
        if self._increase_spawn_interval(elapsed):
            color = utils.get_random_color()
            for i in range(0, len(self.deltas)):
                d = utils.multiply_twople_by_constant(self.deltas[i], self.spawn_interval)
                pos_i = (utils.add_twoples(pos, d))
                e_man.place_entity(pos_i, color)

    def stop_spawn(self) -> None:
        self.click_timer = 0
        self.spawn_interval = False

    def highlight_cursor(self, screen: pygame.display) -> None:
        if self.dragging[LEFT_CLICK]:
            pygame.draw.lines(screen, colors.BLACK, True, points=utils.get_rect_outline(self.cursor.rect))
        else:
            pygame.draw.lines(screen, colors.BLACK, True, points=self.cursor.get_points())
    
    def drag(self, button: int) -> None:
        if not self.dragging[button]:
            self._start_drag(button)
        elif button == LEFT_CLICK:
            self.cursor.end = pygame.mouse.get_pos()
            self._build_cursor_rect()
        
    def select(self, e_man: EntityManager, shift: bool) -> None:
        if not shift: e_man.clear_selected()
        x, y = self.cursor.rect.left, self.cursor.rect.top
        while x < self.cursor.rect.right:
            y = self.cursor.rect.top
            while y < self.cursor.rect.bottom:
                for e in e_man.m.grid[utils.add_twoples((x, y), self.window.offset)]:
                    e_man.select_entity(e)
                y += settings.ENT_WIDTH
            x += settings.ENT_WIDTH
    
    def place_selected(self, e_man: EntityManager) -> None:
        x, y = self.cursor.rect.left, self.cursor.rect.top
        while x < self.cursor.rect.right:
            y = self.cursor.rect.top
            while y < self.cursor.rect.bottom:
                e_man.place_entity(utils.add_twoples((x, y), self.window.offset), utils.get_random_color())
                y += settings.ENT_WIDTH
            x += settings.ENT_WIDTH

    def delete_selected(self, e_man: EntityManager) -> None:
        x, y = self.cursor.rect.left, self.cursor.rect.top
        while x < self.cursor.rect.right:
            y = self.cursor.rect.top
            while y < self.cursor.rect.bottom:
                for e in e_man.m.grid[utils.add_twoples((x, y), self.window.offset)]:
                    e_man.remove_entity(e)
                y += settings.ENT_WIDTH
            x += settings.ENT_WIDTH
    
    def stop_drag(self, button: int) -> None:
        self.dragging[button] = False

    def get_drag_dir(self, button: int) -> tuple:
        pos = pygame.mouse.get_pos()
        dirx = 0
        diry = 0
        start = self.drag_start[button]
        if pos[0] > start[0]:
            dirx = settings.WORLD_SIZE/100
        elif pos[0] < start[0]:
            dirx = -settings.WORLD_SIZE/100
        if pos[1] > start[1]:
            diry = settings.WORLD_SIZE/100
        elif pos[1] < start[1]:
            diry = -settings.WORLD_SIZE/100
        return (dirx, diry)

    # helpers
    def _start_drag(self, button: int) -> None:
        self.dragging[button] = True
        m_pos = pygame.mouse.get_pos()
        self.drag_start[button] = m_pos
        if button == LEFT_CLICK:
            self.cursor.start = m_pos
            self.drag(LEFT_CLICK)
    
    def _build_cursor_rect(self) -> None:
        self.cursor.rect = utils.get_rect_from_twoples(self.cursor.start, self.cursor.end)

    def _increase_spawn_interval(self, elapsed) -> bool:
        self.click_timer += elapsed
        if int(self.click_timer / self.spawn_modulus) + 1 > self.spawn_interval:
            self.spawn_interval = int(self.click_timer / self.spawn_modulus) + 1
            return True
        return False
