import pygame
import src.utils.utils as utils
import static.colors as colors
from static.settings import Settings as settings
from src.interface.interface_element import InterfaceElement
from src.styles.styles import MouseCursorStyle
from src.entities.entity_manager import EntityManager
from src.interface.window import Window
from src.interface.components.action_menu import ActionMenuOption


class Cursor(InterfaceElement):
    def __init__(self):
        InterfaceElement.__init__(self, MouseCursorStyle(), (0, 0))
        self.start = (0, 0)
        self.end = (0, 0)

    def update(self, dragging: bool) -> None:
        if dragging:
            r = utils.get_rect_from_twoples(self.start, self.end)
            self.pos = r.topleft
            self.style.WIDTH = r.width
            self.style.HEIGHT = r.height
        else:
            self.pos = utils.get_tile_pos(pygame.mouse.get_pos())
            self.style.WIDTH = settings.ENT_WIDTH
            self.style.HEIGHT = settings.ENT_WIDTH
    
    def render(self, screen: pygame.Surface, action: str) -> None:
        self._set_color(action)
        self.render_border(screen)

    # helpers

    def _set_color(self, action: str) -> None:
        if action == settings.ACTION_MENU_OPTIONS[0]:
            self.style.BORDER_COLOR = colors.GREEN
        elif action == settings.ACTION_MENU_OPTIONS[1]:
            self.style.BORDER_COLOR = colors.CYAN
        elif action == settings.ACTION_MENU_OPTIONS[2]:
            self.style.BORDER_COLOR = colors.RED
        elif action == settings.ACTION_MENU_OPTIONS[3]:
            self.style.BORDER_COLOR = colors.ORANGE


class Mouse:
    def __init__(self, window: Window):
        self.window = window
        self.cursor = Cursor()
        self.drag_start = [(0, 0), (0, 0), (0, 0)]
        self.dragging = [False, False, False]
        self.click_timer = 0
        self.spawn_modulus = 250
        self.spawn_interval = 0

    def render_cursor(self, screen: pygame.Surface, i_map_active: bool, action: str) -> None:
        if not i_map_active:
            self.cursor.update(self.dragging[settings.LEFT_CLICK])
            self.cursor.render(screen, action)

    def spawn_outward(self, e_man: EntityManager, pos: tuple, atts: dict, elapsed) -> None:
        if self._increase_spawn_interval(elapsed):
            for i in range(0, len(settings.DIRS)):
                d = utils.multiply_twople_by_constant(settings.DIRS[i], self.spawn_interval)
                pos_i = (utils.add_twoples(pos, d))
                e_man.place_entity(pos_i, atts)

    def stop_spawn(self) -> None:
        self.click_timer = 0
        self.spawn_interval = False
    
    def drag(self, button: int) -> None:
        if not self.dragging[button]:
            self._start_drag(button)
        elif button == settings.LEFT_CLICK:
            self.cursor.end = pygame.mouse.get_pos()
            self._build_cursor_rect()
        elif button == settings.RIGHT_CLICK:
            self.window.move(self._get_drag_dir(settings.RIGHT_CLICK))

    def execute_left_click_drag(self, menu_option: ActionMenuOption, e_man: EntityManager, atts: dict, shift: bool=False) -> None:
        # creation
        if menu_option.option == settings.ACTION_MENU_OPTIONS[0]:
            self.place_selected(e_man, atts)
        # selection
        elif menu_option.option == settings.ACTION_MENU_OPTIONS[1]:
            self.select(e_man, shift)
        # deletion
        elif menu_option.option == settings.ACTION_MENU_OPTIONS[2]:
            self.delete_selected(e_man)
        self.stop_drag(settings.LEFT_CLICK)
        
    def select(self, e_man: EntityManager, shift: bool) -> None:
        if not shift: e_man.clear_selected()
        x, y = self.cursor.rect.left, self.cursor.rect.top
        while x < self.cursor.rect.right:
            y = self.cursor.rect.top
            while y < self.cursor.rect.bottom:
                pos = utils.add_twoples((x, y), self.window.offset)
                if e_man.m.grid.get(pos) == None:
                    y += settings.ENT_WIDTH
                    continue
                for e in e_man.m.grid[pos]:
                    e_man.select_entity(e)
                y += settings.ENT_WIDTH
            x += settings.ENT_WIDTH
    
    def place_selected(self, e_man: EntityManager, atts: dict) -> None:
        x, y = self.cursor.rect.left, self.cursor.rect.top
        while x < self.cursor.rect.right:
            y = self.cursor.rect.top
            while y < self.cursor.rect.bottom:
                pos = utils.add_twoples((x, y), self.window.offset)
                if e_man.m.grid.get(pos) == None:
                    y += settings.ENT_WIDTH
                    continue
                e_man.place_entity(pos, atts)
                y += settings.ENT_WIDTH
            x += settings.ENT_WIDTH

    def delete_selected(self, e_man: EntityManager) -> None:
        x, y = self.cursor.rect.left, self.cursor.rect.top
        while x < self.cursor.rect.right:
            y = self.cursor.rect.top
            while y < self.cursor.rect.bottom:
                pos = utils.add_twoples((x, y), self.window.offset)
                if e_man.m.grid.get(pos) == None:
                    y += settings.ENT_WIDTH
                    continue
                for e in e_man.m.grid[utils.add_twoples((x, y), self.window.offset)]:
                    e_man.remove_entity(e)
                y += settings.ENT_WIDTH
            x += settings.ENT_WIDTH

    def copy_selected(self, e_man: EntityManager, pos: tuple) -> dict:
        if e_man.m.grid.get(pos):
            return e_man.get_attributes(e_man.m.grid.get(pos)[0])
    
    def stop_drag(self, button: int) -> None:
        self.dragging[button] = False

    # helpers

    def _start_drag(self, button: int) -> None:
        self.dragging[button] = True
        m_pos = pygame.mouse.get_pos()
        self.drag_start[button] = m_pos
        if button == settings.LEFT_CLICK:
            self.cursor.start = m_pos
            self.drag(settings.LEFT_CLICK)
    
    def _get_drag_dir(self, button: int) -> tuple:
        pos = pygame.mouse.get_pos()
        dirx = 0
        diry = 0
        start = self.drag_start[button]
        if pos[0] > start[0]:
            dirx = int(settings.WORLD_SIZE/100)
        elif pos[0] < start[0]:
            dirx = -int(settings.WORLD_SIZE/100)
        if pos[1] > start[1]:
            diry = int(settings.WORLD_SIZE/100)
        elif pos[1] < start[1]:
            diry = -int(settings.WORLD_SIZE/100)
        return (dirx, diry)
    
    def _build_cursor_rect(self) -> None:
        self.cursor.rect = utils.get_rect_from_twoples(self.cursor.start, self.cursor.end)

    def _increase_spawn_interval(self, elapsed) -> bool:
        self.click_timer += elapsed
        if int(self.click_timer / self.spawn_modulus) + 1 > self.spawn_interval:
            self.spawn_interval = int(self.click_timer / self.spawn_modulus) + 1
            return True
        return False
