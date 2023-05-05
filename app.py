import pygame
import asyncio
import colors
import settings
from stats import Stats
from entity_manager import EntityManager

'''
x == width == rect.left
y == height == rect.top
'''

class App:
    def __init__(self):
        self._running = True
        self.paused = False
        self.width = settings.WINDOW_WIDTH
        self.height = settings.WINDOW_HEIGHT
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width + settings.STATS_WIDTH, self.height), pygame.SCALED | pygame.RESIZABLE)
        self.e_man = EntityManager(self.screen)
        self.keys = []
        self.stats = Stats(self.screen, self.width)
    
    def on_init(self) -> None:
        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])
        self.e_man.build_entities()
        self._running = True
    
    def on_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.QUIT:
            self._running = False
        if event.type == pygame.KEYUP:
            self.keys.remove(event.unicode)
        if event.type == pygame.KEYDOWN:
            self._handlecmd(event.unicode)
            self.keys.append(event.unicode)

    def on_loop(self) -> None:
        if self.paused:
            return
        self.clock.tick(settings.CLOCK_RATE)
        self.e_man.update_entities(self.clock.get_time())
    
    def on_render(self) -> None:
        self.screen.fill(colors.WHITE)
        self.e_man.render_entities(self.clock.get_time(), self.paused)
        self._update_stats()
        pygame.display.flip()

    def on_cleanup(self) -> None:
        if settings.IN_GAME_SETTINGS["LOGGING"]:
            print("total entities (at end): " + str(len(self.e_man.entities)))
            print("total entities (all time): " + str(self.e_man.total_ent))
            print("average color (last frame): " + str(self.e_man.find_avg_color()))
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
        self.stats.add_line("entities: ")
        self.stats.add_line(str(len(self.e_man.entities)))
        self.stats.add_line("entities all time: ")
        self.stats.add_line(str(self.e_man.total_ent))
        self.stats.add_line("diseased entities: ")
        self.stats.add_line(str(self.e_man.get_diseased_entities(self.e_man.entities)))
        self.stats.add_line("avg color")
        current_avg = self.e_man.find_avg_color()
        self.stats.add_line(str(current_avg), current_avg)
        self.stats.add_line("avg color all time")
        self.stats.add_line(str(self.e_man.avg_color), self.e_man.avg_color)
        self.stats.draw_lines()
        pygame.draw.line(self.screen, colors.BLACK, (self.width, 0), (self.width, self.height))
    
    def _toggle_setting(self, setting: str) -> None:
        if settings.IN_GAME_SETTINGS[setting]:
            settings.IN_GAME_SETTINGS[setting] = 0
        else:
            settings.IN_GAME_SETTINGS[setting] = 1

    def _handlecmd(self, key: str) -> None:
        # cull half of entities
        if key == ('x' or key == 'X') and not self.paused:
            self.e_man.cull()
        # randomize entity colors
        elif key == ('r' or key == 'R') and not self.paused:
            self.e_man.randomize_color()
        # change colors to red
        elif key == '1' and not self.paused:
            self.e_man.update_all_colors((255, 0, 0))
        # change colors to green
        elif key == '2' and not self.paused:
            self.e_man.update_all_colors((0, 255, 0))
        # change colors to blue
        elif key == '3' and not self.paused:
            self.e_man.update_all_colors((0, 0, 255))
        # change colors to yellow
        elif key == '4' and not self.paused:
            self.e_man.update_all_colors((255, 255, 0))
        # change colors to magenta
        elif key == '5' and not self.paused:
            self.e_man.update_all_colors((255, 0, 255))
        # change colors to cyan
        elif key == '6' and not self.paused:
            self.e_man.update_all_colors((0, 255, 255))
        # shift colors
        elif key == ('c' or key == 'C') and not self.paused:
            self.e_man.shift_colors()
        # flip colors
        elif key == ('f' or key == 'F') and not self.paused:
            self.e_man.flip_colors()
        # add in start entities
        elif key == ('e' or key == 'E') and not self.paused:
            self.e_man.add_start_entities()
        elif key == 'd' or key == 'D':
            self._toggle_setting("MARK_DISEASED")
        elif key == 'l' or key == 'L':
            self._toggle_setting("LOGGING")
        # quit
        elif key == 'q' or key == 'Q':
            self._running = False
        # escape key, pause simulation
        elif key == '\x1b':
            self.paused = not self.paused
