import pygame
import asyncio
import static.colors as colors
import static.settings as settings
from src.window import Window
from src.stats import Stats
from src.metrics import Metrics
from src.entity_manager import EntityManager

'''
x == width == rect.left
y == height == rect.top
'''


class App:
    def __init__(self):
        self._running = True
        self.paused = False
        self.window = Window(0, 0)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(
            (self.window.width + settings.STATS_WIDTH, self.window.height), pygame.SCALED | pygame.RESIZABLE)
        self.e_man = EntityManager(self.screen)
        self.keys = []
        self.stats = Stats(self.screen, self.window.width)
        self.metrics = Metrics()

    def on_init(self) -> None:
        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])
        self._create_metrics()
        self._update_metrics()
        self.e_man.build_entities(self.window)
        self._running = True

    def on_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.QUIT:
            self._running = False
        if event.type == pygame.KEYUP:
            self.keys.remove(event.key)
        if event.type == pygame.KEYDOWN:
            self._handlecmd(event.key)
            self.keys.append(event.key)

    def on_loop(self) -> None:
        self._handle_keys_pressed()
        if self.paused:
            return
        self.clock.tick(settings.CLOCK_RATE)
        self.e_man.update_entities(self.clock.get_time())

    def on_render(self) -> None:
        self.screen.fill(colors.WHITE)
        self.e_man.render_entities(self.window)
        self._update_stats()
        self._highlight_cursor()
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
            self._update_metrics()
            await asyncio.sleep(0)
        self.on_cleanup()

    # helpers
    def _update_stats(self) -> None:
        self.stats.clear()
        self.stats.add_line("entities: ", 
                            str(len(self.e_man.entities)))
        self.stats.add_line("entities all time: ", 
                            str(self.e_man.created))
        self.stats.add_line("diseased entities: ", 
                            str(self.e_man.get_diseased_entities(self.e_man.entities)))
        self.stats.add_line("entities eaten: ", 
                            str(self.e_man.eaten))
        self.stats.add_line("time elapsed: ", self.metrics.get_time_elapsed())
        self.stats.add_line("entities per minute: ", 
                            str(int(self.metrics.get_rate("created") - self.metrics.get_rate("destroyed"))), 
                            color=colors.GREEN)
        self.stats.add_line("created per minute: ", 
                            str(int(self.metrics.get_rate("created"))), 
                            color=colors.BLUE)
        self.stats.add_line("destroyed per minute: ", 
                            str(int(self.metrics.get_rate("destroyed"))), 
                            color=colors.RED)
        self.stats.add_line("diseased per minute: ", 
                            str(int(self.metrics.get_rate("diseased"))), 
                            colors.BROWN)
        self.stats.add_line("eaten per minute: ", 
                            str(int(self.metrics.get_rate("eaten"))), 
                            colors.ORANGE)
        self.stats.draw_lines()
        pygame.draw.line(self.screen, colors.BLACK,
                         (self.window.width, 0), (self.window.width, self.window.height))

    def _create_metrics(self) -> None:
        self.metrics.create_tracker("created")
        self.metrics.create_tracker("destroyed")
        self.metrics.create_tracker("diseased")
        self.metrics.create_tracker("eaten")

    def _update_metrics(self) -> None:
        self.metrics.update("created", self.e_man.created)
        self.metrics.update("destroyed", self.e_man.destroyed)
        self.metrics.update("diseased", self.e_man.diseased)
        self.metrics.update("eaten", self.e_man.eaten)

    def _toggle_setting(self, setting: str) -> None:
        if settings.IN_GAME_SETTINGS[setting]:
            settings.IN_GAME_SETTINGS[setting] = 0
            print(setting + ' toggled off')
        else:
            settings.IN_GAME_SETTINGS[setting] = 1
            print(setting + ' toggled on')

    def _highlight_cursor(self) -> None:
        pos = pygame.mouse.get_pos()
        points = [(pos[0]-(pos[0] % settings.ENT_WIDTH), pos[1]-(pos[1] % settings.ENT_WIDTH)),
                  (pos[0]+(settings.ENT_WIDTH - pos[0] % settings.ENT_WIDTH), pos[1]-(pos[1] % settings.ENT_WIDTH)),
                  (pos[0]+(settings.ENT_WIDTH - pos[0] % settings.ENT_WIDTH), pos[1]+(settings.ENT_WIDTH - pos[1] % settings.ENT_WIDTH)),
                  (pos[0]-(pos[0] % settings.ENT_WIDTH), pos[1]+(settings.ENT_WIDTH - pos[1] % settings.ENT_WIDTH))]
        pygame.draw.lines(self.screen, colors.BLACK, True, points=points)

    def _handlecmd(self, key: str) -> None:
        # cull half of entities
        if key == pygame.K_x and not self.paused:
            self.e_man.cull()
        # randomize entity colors
        elif key == pygame.K_r and not self.paused:
            self.e_man.randomize_color()
        # change colors to red
        elif key == pygame.K_1 and not self.paused:
            self.e_man.update_all_colors((255, 0, 0))
        # change colors to green
        elif key == pygame.K_2 and not self.paused:
            self.e_man.update_all_colors((0, 255, 0))
        # change colors to blue
        elif key == pygame.K_3 and not self.paused:
            self.e_man.update_all_colors((0, 0, 255))
        # change colors to yellow
        elif key == pygame.K_4 and not self.paused:
            self.e_man.update_all_colors((255, 255, 0))
        # change colors to magenta
        elif key == pygame.K_5 and not self.paused:
            self.e_man.update_all_colors((255, 0, 255))
        # change colors to cyan
        elif key == pygame.K_6 and not self.paused:
            self.e_man.update_all_colors((0, 255, 255))
        # shift colors
        elif key == pygame.K_c and not self.paused:
            self.e_man.shift_colors()
        # flip colors
        elif key == pygame.K_f and not self.paused:
            self.e_man.flip_colors()
        # add in start entities
        elif key == pygame.K_e and not self.paused:
            self.e_man.add_start_entities(self.window)
        elif key == pygame.K_d:
            self._toggle_setting("MARK_DISEASED")
        elif key == pygame.K_l:
            self._toggle_setting("LOGGING")
        # quit
        elif key == pygame.K_q:
            self._running = False
        # escape key, pause simulation
        elif key == pygame.K_ESCAPE:
            self.paused = not self.paused
    
    def _handle_keys_pressed(self) -> None:
        if pygame.K_UP in self.keys:
            self.window.move((0, -settings.ENT_WIDTH*2))
        if pygame.K_DOWN in self.keys:
            self.window.move((0, settings.ENT_WIDTH*2))
        if pygame.K_LEFT in self.keys:
            self.window.move((-settings.ENT_WIDTH*2, 0))
        if pygame.K_RIGHT in self.keys:
            self.window.move((settings.ENT_WIDTH*2, 0))