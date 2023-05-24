import pygame
import asyncio
import src.utils.utils as utils
import static.colors as colors
import static.settings as settings
from src.interface.window import Window
from src.interface.stats import Stats
from src.tracking.metrics import Metrics
from src.entities.entity_manager import EntityManager
from src.colonies.colony_manager import ColonyManager
from src.interface.mini_map import MiniMap
from src.interface.mouse import Mouse
from src.utils.clock import Clock
from src.interface.picker_menu import PickerMenu
from src.interface.picker_menu import PickerMenuOption

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
            (self.window.width + settings.STATS_WIDTH, self.window.height), pygame.SCALED | pygame.RESIZABLE)
        self.e_man = EntityManager(self.screen)
        self.c_man = ColonyManager(self.screen)
        self.keys = []
        self.mouse = Mouse(self.window)
        self.stats = Stats()
        self.metrics = Metrics()
        self.minimap = MiniMap(self.screen, self.window)
        self.picker = PickerMenu((20, 20))

    def on_init(self) -> None:
        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP, pygame.MOUSEBUTTONDOWN])
        self._create_metrics()
        self._update_metrics()
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
        self._update_stats()
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
        self.stats.render(self.screen)
        self.mouse.highlight_cursor(self.screen)
        self.minimap.render(self.screen, self.e_man.entities)
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
    def _update_stats(self) -> None:
        self.stats.clear()
        self.stats.add_stat("fps: ",
                            str(int(pygame.time.Clock.get_fps(self.clock.clock))))
        self.stats.add_stat("entities: ", 
                            str(len(self.e_man.entities)))
        self.stats.add_stat("entities all time: ", 
                            str(self.e_man.created))
        self.stats.add_stat("diseased entities: ", 
                            str(self.e_man.get_diseased_entities(self.e_man.entities)))
        self.stats.add_stat("entities eaten: ", 
                            str(self.e_man.eaten))
        # self.stats.add_stat("colonies: ",
        #                     str(len(self.c_man.colonies)))
        self.stats.add_stat("time elapsed: ", self.metrics.get_time_elapsed())
        self.stats.add_stat("entities per minute: ", 
                            str(int(self.metrics.get_rate("created") - self.metrics.get_rate("destroyed"))), 
                            color=colors.GREEN)
        self.stats.add_stat("created per minute: ", 
                            str(int(self.metrics.get_rate("created"))), 
                            color=colors.BLUE)
        self.stats.add_stat("destroyed per minute: ", 
                            str(int(self.metrics.get_rate("destroyed"))), 
                            color=colors.RED)
        self.stats.add_stat("diseased per minute: ", 
                            str(int(self.metrics.get_rate("diseased"))), 
                            colors.BROWN)
        # self.stats.add_stat("eaten per minute: ", 
        #                     str(int(self.metrics.get_rate("eaten"))), 
        #                     colors.ORANGE)

    def _create_metrics(self) -> None:
        self.metrics.create_tracker("created")
        self.metrics.create_tracker("destroyed")
        self.metrics.create_tracker("diseased")
        self.metrics.create_tracker("eaten")

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
        if button-1 == settings.LEFT_CLICK:
            # left click picker menu
            if self.picker.contains_click(pygame.mouse.get_pos(), settings.LEFT_CLICK):
                if not self.picker.menu_open: self.picker.open_pick_menu()
                else: self.picker.close_pick_menu()
            # left click picker menu option
            elif self.picker.menu_open and self.picker.contains_option_click(pygame.mouse.get_pos(), settings.LEFT_CLICK):
                self.picker.close_pick_menu()
    
    def _handle_mouse_actions(self) -> None:
        # mouse buttons: 0 == left, 1 == middle, 2 == right
        buttons = pygame.mouse.get_pressed(3)
        if buttons[settings.LEFT_CLICK]:
            # pos = utils.get_tile_pos(pygame.mouse.get_pos(), self.window.offset)
            # self.e_man.place_entity(pos)
            self.mouse.drag(settings.LEFT_CLICK)
        elif self.mouse.dragging[settings.LEFT_CLICK]:
            self._execute_mouse_action(self.picker.selected_option, settings.LEFT_CLICK)
        if buttons[settings.MIDDLE_CLICK]:
            self.mouse.spawn_outward(self.e_man, self._get_tile_pos(pygame.mouse.get_pos()), self.clock.time)
        else:
            self.mouse.stop_spawn()
        if buttons[settings.RIGHT_CLICK]:
            self.mouse.drag(settings.RIGHT_CLICK)
        else:
            self.mouse.stop_drag(settings.RIGHT_CLICK)
    
    def _execute_mouse_action(self, menu_option: PickerMenuOption, button: int) -> None:
        # selection
        if menu_option.option == settings.ACTION_MENU_OPTIONS[0]:
            self.mouse.select(self.e_man, (pygame.K_LSHIFT in self.keys or pygame.K_RIGHT in self.keys))
        # creation
        elif menu_option.option == settings.ACTION_MENU_OPTIONS[1]:
            self.mouse.place_selected(self.e_man)
        # deletion
        elif menu_option.option == settings.ACTION_MENU_OPTIONS[2]:
            self.mouse.delete_selected(self.e_man)
        self.mouse.stop_drag(settings.LEFT_CLICK)

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
