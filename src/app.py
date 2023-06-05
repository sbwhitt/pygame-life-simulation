import pygame
import asyncio
import static.colors as colors
from static.settings import Settings as settings
import src.utils.utils as utils
import src.utils.saver as saver
import src.utils.loader as loader
from src.interface.window import Window
from src.tracking.metrics import Metrics
from src.entities.entity_manager import EntityManager
from src.colonies.colony_manager import ColonyManager
from src.interface.mouse import Mouse
from src.utils.clock import Clock
from src.interface.panels.side_panel import SidePanel
from src.interface.panels.bottom_panel import BottomPanel
from src.utils.interface_map import InterfaceMap
from src.interface.components.info_box import InfoBox

'''
x == width == rect.left
y == height == rect.top
'''


class App:
    def __init__(self, save_file: str=None):
        self._running = True
        self.paused = True
        self.window = Window(0, 0)
        self.clock = Clock()
        self.screen = pygame.display.set_mode(
            (self.window.width, self.window.height), pygame.SCALED | pygame.RESIZABLE | pygame.DOUBLEBUF)
        self.screen.set_alpha(None)
        self.i_map = InterfaceMap()
        if not self._load_save_file(save_file):
            self.e_man = EntityManager(self.screen)
            self.c_man = ColonyManager(self.screen)
            self.metrics = Metrics()
        self.keys = []
        self.mouse = Mouse(self.window)
        self.info_box = InfoBox((0, 0), settings.FONT_SIZE_BIGGER)
        self.side_panel = SidePanel(self.window)
        self.bottom_panel = BottomPanel()

    def on_init(self) -> None:
        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP, pygame.MOUSEBUTTONDOWN])
        self._create_metrics()
        self._update_metrics()
        self._init_interface_map()
        # self.e_man.build_entities(self.window)
        self._running = True

    def on_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.QUIT:
            self._running = False
        if event.type == pygame.KEYUP:
            self.keys.remove(event.key)
        if event.type == pygame.KEYDOWN:
            self._handle_cmd(event.key)
            self.keys.append(event.key)
        if event.type == pygame.MOUSEBUTTONDOWN:
            # event.button is 1 indexed...
            self._handle_click(event.button)

    def on_loop(self) -> None:
        self._handle_keys_pressed()
        self._handle_mouse_actions()
        self._update_metrics()
        self.side_panel.update_stats(self.clock, self.e_man, self.metrics)
        self._check_interface_map()
        self.clock.step()
        if self.paused:
            return
        self.e_man.update_entities(self.clock.time, self.c_man)
        self.c_man.update_colonies()

    def on_render(self) -> None:
        self.screen.fill(colors.GRAY)
        self._render_map_background()
        self.e_man.render_entities(self.window)
        self.c_man.render_colonies(self.window)
        self.e_man.render_selected(self.window, self.clock)
        self.mouse.render_cursor(self.screen, self.i_map.active)
        self.side_panel.render(self.screen, self.e_man.entities)
        self.bottom_panel.render(self.screen)
        if self.paused:
            self.info_box.render(self.screen, "paused")
        pygame.display.flip()

    def on_cleanup(self) -> None:
        if settings.IN_GAME_SETTINGS["LOGGING"]:
            print("total entities (at end): " + str(len(self.e_man.entities)))
            print("total entities (all time): " + str(self.e_man.created))
            print("average color (last frame): " +
                  str(self.e_man.find_avg_color()))
            print("average color (all time): " + str(self.e_man.avg_color))
        if settings.AUTO_SAVE:
            saver.save_data(self._get_save_data())
        pygame.quit()

    async def on_execute(self) -> None:
        if self.on_init() == False:
            self._running = False
        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
            await asyncio.sleep(0)
        self.on_cleanup()

    # helpers

    def _load_save_file(self, save_file: str) -> bool:
        if save_file:
            data = loader.load_data(save_file)
            if data:
                self.e_man = EntityManager(self.screen,
                                       map=data["map"],
                                       entities=data["entities"],
                                       created=data["created"],
                                       destroyed=data["destroyed"],
                                       diseased=data["diseased"],
                                       eaten=data["eaten"])
                self.c_man = ColonyManager(self.screen,
                                       colonies=data["colonies"])
                self.metrics = Metrics(elapsed=data["elapsed"])
                return True

    def _get_save_data(self) -> dict:
        return {
                "ENT_WIDTH": settings.ENT_WIDTH,
                "WORLD_SIZE": settings.WORLD_SIZE,
                "DIRS": settings.DIRS,
                "map": self.e_man.m,
                "entities": self.e_man.entities,
                "created": self.e_man.created,
                "destroyed": self.e_man.destroyed,
                "diseased": self.e_man.diseased,
                "eaten": self.e_man.eaten,
                "colonies": self.c_man.colonies,
                "elapsed": self.metrics.time_elapsed
            }

    def _render_map_background(self) -> None:
        pos = utils.subtract_twoples((0, 0), self.window.offset)
        r = pygame.rect.Rect(pos[0], pos[1], settings.WORLD_SIZE, settings.WORLD_SIZE+settings.ENT_WIDTH)
        pygame.draw.rect(self.screen, colors.WHITE, r)

    def _create_metrics(self) -> None:
        self.metrics.create_tracker("created")
        self.metrics.create_tracker("destroyed")
        self.metrics.create_tracker("diseased")
        self.metrics.create_tracker("eaten")
    
    def _init_interface_map(self) -> None:
        # adding side panel toggle button
        self.i_map.add_element(self.side_panel.panel_button)
        # adding bottom panel elements
        self.i_map.add_element(self.bottom_panel.panel_button)
        for o in self.bottom_panel.color_picker.options:
            self.i_map.add_element(o)
        # adding bottom panel entity attribute choices
        for c in self.bottom_panel.choosers:
            self.i_map.add_element(c)
        # adding action picker menu options
        for a in self.bottom_panel.actions.options:
            self.i_map.add_element(a)
        # adding minimap
        self.i_map.add_element(self.side_panel.minimap)
    
    def _check_interface_map(self) -> None:
        if self.i_map.within_element(pygame.mouse.get_pos()):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def _update_metrics(self) -> None:
        self.metrics.update("created", self.e_man.created, self.paused)
        self.metrics.update("destroyed", self.e_man.destroyed, self.paused)
        self.metrics.update("diseased", self.e_man.diseased, self.paused)
        self.metrics.update("eaten", self.e_man.eaten, self.paused)

    def _toggle_setting(self, setting: str) -> None:
        if settings.IN_GAME_SETTINGS[setting]:
            settings.IN_GAME_SETTINGS[setting] = 0
            print(setting + ' toggled off')
        else:
            settings.IN_GAME_SETTINGS[setting] = 1
            print(setting + ' toggled on')

    def _zoom_in(self, speed: int) -> None:
        self.e_man.zoom_in_entities(speed)
        self.side_panel.minimap.zoom_in(speed)
        self.window.zoom_in(speed)

    def _zoom_out(self, speed: int) -> None:
        self.e_man.zoom_out_entities(speed)
        self.side_panel.minimap.zoom_out(speed)
        self.window.zoom_out(speed)

    def _handle_click(self, button) -> None:
        # why are event.button values different from pygame.mouse.get_pressed???
        # left click is 1 here but 0 elsewhere
        # single left click
        if self.i_map.active and button-1 == settings.LEFT_CLICK:
            self.side_panel.handle_click(settings.LEFT_CLICK)
            self.bottom_panel.handle_click(settings.LEFT_CLICK)
        # scroll wheel in
        elif button == settings.SCROLL_IN and settings.ENT_WIDTH*settings.SCROLL_SPEED <= 40:
            self._zoom_in(settings.SCROLL_SPEED)
        # scroll wheel out
        elif button == settings.SCROLL_OUT and int(settings.ENT_WIDTH/settings.SCROLL_SPEED) >= 5:
            self._zoom_out(settings.SCROLL_SPEED)

    def _handle_mouse_actions(self) -> None:
        # mouse buttons: 0 == left, 1 == middle, 2 == right
        buttons = pygame.mouse.get_pressed(3)
        if self.i_map.active:
            return
        if buttons[settings.LEFT_CLICK]:
            # copy is a special case here
            if self.bottom_panel.get_selected_action() == settings.ACTION_MENU_OPTIONS[3]:
                atts = self.mouse.copy_selected(self.e_man, utils.get_tile_pos(pygame.mouse.get_pos(), self.window.offset))
                if atts: self.bottom_panel.set_attributes(atts)
            else: self.mouse.drag(settings.LEFT_CLICK)
        elif self.mouse.dragging[settings.LEFT_CLICK]:
            shift = (pygame.K_LSHIFT in self.keys or pygame.K_RSHIFT in self.keys)
            self.mouse.execute_left_click_drag(self.bottom_panel.actions.selected_option,
                                          self.e_man,
                                          self.bottom_panel.get_attributes(),
                                          shift)
        if buttons[settings.MIDDLE_CLICK]:
            self.mouse.spawn_outward(self.e_man,
                                     utils.get_tile_pos(pygame.mouse.get_pos(), self.window.offset),
                                     self.bottom_panel.get_attributes(),
                                     self.clock.time)
        else:
            self.mouse.stop_spawn()
        if buttons[settings.RIGHT_CLICK]:
            self.mouse.drag(settings.RIGHT_CLICK)
        else:
            self.mouse.stop_drag(settings.RIGHT_CLICK)

    def _handle_cmd(self, key: str) -> None:
        # cull half of entities
        if key == pygame.K_x:
            self.e_man.cull()
        # randomize entity colors
        elif key == pygame.K_r:
            self.e_man.randomize_color()
        # change colors to red
        elif key == pygame.K_1:
            self.e_man.update_all_colors((255, 0, 0))
        # change colors to green
        elif key == pygame.K_2:
            self.e_man.update_all_colors((0, 255, 0))
        # change colors to blue
        elif key == pygame.K_3:
            self.e_man.update_all_colors((0, 0, 255))
        # change colors to yellow
        elif key == pygame.K_4:
            self.e_man.update_all_colors((255, 255, 0))
        # change colors to magenta
        elif key == pygame.K_5:
            self.e_man.update_all_colors((255, 0, 255))
        # change colors to cyan
        elif key == pygame.K_6:
            self.e_man.update_all_colors((0, 255, 255))
        elif (pygame.K_LCTRL in self.keys or pygame.K_RCTRL in self.keys) and key == pygame.K_a:
            self.e_man.select_all_entities()
        elif (pygame.K_LCTRL in self.keys or pygame.K_RCTRL in self.keys) and key == pygame.K_s:
            saver.save_data(self._get_save_data())
        # shift colors
        elif key == pygame.K_c:
            self.e_man.shift_colors()
        # flip colors
        elif key == pygame.K_f:
            self.e_man.flip_colors()
        # add in start entities
        elif key == pygame.K_e:
            self.e_man.add_start_entities(self.window)
        elif key == pygame.K_d:
            self._toggle_setting("MARK_DISEASED")
        elif key == pygame.K_l:
            self._toggle_setting("LOGGING")
        elif key == pygame.K_h:
            self._toggle_setting("HIGHLIGHT")
        # toggle side panel
        elif key == pygame.K_p:
            self.side_panel.toggle_panel()
        # toggle bottom panel
        elif key == pygame.K_b:
            self.bottom_panel.toggle_panel()
        # quit
        elif key == pygame.K_q:
            self._running = False
        # escape key, pause simulation
        elif key == pygame.K_ESCAPE:
            self.paused = not self.paused
        # delete selected entities
        elif key == pygame.K_DELETE:
            self.e_man.delete_selected()
    
    def _handle_keys_pressed(self) -> None:
        if pygame.K_UP in self.keys:
            self.window.move((0, -settings.WORLD_SIZE/100))
        if pygame.K_DOWN in self.keys:
            self.window.move((0, settings.WORLD_SIZE/100))
        if pygame.K_LEFT in self.keys:
            self.window.move((-settings.WORLD_SIZE/100, 0))
        if pygame.K_RIGHT in self.keys:
            self.window.move((settings.WORLD_SIZE/100, 0))
