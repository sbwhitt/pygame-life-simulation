import pygame
import asyncio
import static.colors as colors
import static.settings as settings
from src.interface.window import Window
from src.tracking.metrics import Metrics
from src.entities.entity_manager import EntityManager
from src.colonies.colony_manager import ColonyManager
from src.interface.mouse import Mouse
from src.utils.clock import Clock
from src.interface.panels.side_panel import SidePanel
from src.interface.panels.bottom_panel import BottomPanel
from src.utils.interface_map import InterfaceMap
from src.interface.picker_menu import PickerMenu

'''
x == width == rect.left
y == height == rect.top
'''


class App:
    def __init__(self):
        self._running = True
        self.paused = False
        self.window = Window(0, 0)
        self.clock = Clock()
        self.screen = pygame.display.set_mode(
            (self.window.width, self.window.height), pygame.SCALED | pygame.RESIZABLE | pygame.DOUBLEBUF)
        self.screen.set_alpha(None)
        self.i_map = InterfaceMap()
        self.e_man = EntityManager(self.screen)
        self.c_man = ColonyManager(self.screen)
        self.keys = []
        self.mouse = Mouse(self.window)
        self.metrics = Metrics()
        self.side_panel = SidePanel(self.window)
        self.bottom_panel = BottomPanel()
        self.picker = PickerMenu((0, 0))

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
        self.screen.fill(colors.WHITE)
        self.e_man.render_entities(self.window)
        self.c_man.render_colonies(self.window)
        self.e_man.render_selected(self.window, self.clock)
        self.mouse.render_cursor(self.screen, self.i_map.active)
        self.side_panel.render(self.screen, self.e_man.entities)
        self.bottom_panel.render(self.screen)
        self.picker.render(self.screen)
        pygame.display.flip()

    def on_cleanup(self) -> None:
        if settings.IN_GAME_SETTINGS["LOGGING"]:
            print("total entities (at end): " + str(len(self.e_man.entities)))
            print("total entities (all time): " + str(self.e_man.created))
            print("average color (last frame): " +
                  str(self.e_man.find_avg_color()))
            print("average color (all time): " + str(self.e_man.avg_color))
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

    def _create_metrics(self) -> None:
        self.metrics.create_tracker("created")
        self.metrics.create_tracker("destroyed")
        self.metrics.create_tracker("diseased")
        self.metrics.create_tracker("eaten")
    
    def _init_interface_map(self) -> None:
        # adding action picker menu
        self.i_map.add_element(self.picker)
        for o in self.picker.options:
            self.i_map.add_element(o)
        # adding side panel toggle button
        self.i_map.add_element(self.side_panel.panel_button)
        # adding bottom panel elements
        self.i_map.add_element(self.bottom_panel.panel_button)
        for o in self.bottom_panel.color_picker.options:
            self.i_map.add_element(o)
        for c in self.bottom_panel.choosers:
            self.i_map.add_element(c)
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
    
    def _get_tile_pos(self, pos: tuple) -> tuple:
        loc = (pos[0]+self.window.offset[0], pos[1]+self.window.offset[1])
        return (loc[0]-(loc[0] % settings.ENT_WIDTH), loc[1]-(loc[1] % settings.ENT_WIDTH))
    
    def _handle_click(self, button) -> None:
        # why are event.button values different from pygame.mouse.get_pressed???
        # left click is 1 here but 0 elsewhere
        if self.i_map.active and button-1 == settings.LEFT_CLICK:
            self.picker.handle_click(settings.LEFT_CLICK)
            self.side_panel.handle_click(settings.LEFT_CLICK)
            self.bottom_panel.handle_click(settings.LEFT_CLICK)
    
    def _handle_mouse_actions(self) -> None:
        # mouse buttons: 0 == left, 1 == middle, 2 == right
        buttons = pygame.mouse.get_pressed(3)
        if self.i_map.active:
            return
        if buttons[settings.LEFT_CLICK]:
            self.mouse.drag(settings.LEFT_CLICK)
        elif self.mouse.dragging[settings.LEFT_CLICK]:
            shift = (pygame.K_LSHIFT in self.keys or pygame.K_RIGHT in self.keys)
            self.mouse.execute_left_click(self.picker.selected_option,
                                          self.e_man,
                                          self.bottom_panel.color_picker.current_color,
                                          shift)
        if buttons[settings.MIDDLE_CLICK]:
            self.mouse.spawn_outward(self.e_man,
                                     self._get_tile_pos(pygame.mouse.get_pos()),
                                     self.bottom_panel.color_picker.current_color, self.clock.time)
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
