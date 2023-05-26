import pygame
import static.colors as colors
import static.settings as settings
import src.utils.utils as utils
from src.interface.interface_element import InterfaceElement
from src.interface.window import Window
from src.utils.clock import Clock
from src.tracking.metrics import Metrics
from src.entities.entity import Entity
from src.entities.entity_manager import EntityManager
from src.styles.styles import SidePanelStyle
from src.styles.styles import SidePanelButtonStyle
from src.interface.stats import Stats
from src.interface.mini_map import MiniMap


class SidePanelButton(InterfaceElement):
    def __init__(self, panel_pos: tuple):
        style = SidePanelButtonStyle()
        pos = utils.subtract_twoples(panel_pos, (style.WIDTH, 0))
        InterfaceElement.__init__(self, style, pos)

    def render(self, screen: pygame.display, panel_open: bool) -> None:
        self.style.COLOR = colors.RED if panel_open else colors.GREEN
        if self.hovering():
            self.render_hover(screen)
        else:
            self.render_transparent(screen)
            self.render_border(screen)
        # self._render_carat(screen, panel_open)
    
    def _render_carat(self, screen: pygame.display, panel_open: bool) -> None:
        if panel_open:
            pass
        else:
            pass


class SidePanel(InterfaceElement):
    def __init__(self, window: Window) -> None:
        style = SidePanelStyle()
        pos = (settings.WINDOW_WIDTH-style.WIDTH, 0)
        InterfaceElement.__init__(self, style, pos)
        self.panel_button = SidePanelButton(self.pos)
        self.stats = Stats()
        self.minimap = MiniMap(window)
        self.panel_open = True
    
    def render(self, screen: pygame.display, entities: list[Entity]) -> None:
        self.panel_button.render(screen, self.panel_open)
        if self.panel_open:
            self.stats.render(screen)
            self.minimap.render(screen, entities)

    def handle_click(self, button: int) -> None:
        if self.panel_button.hovering():
            if button == settings.LEFT_CLICK:
                self.toggle_panel()
    
    def toggle_panel(self) -> None:
        self.panel_open = not self.panel_open
        if self.panel_open:
            self.panel_button.pos = utils.subtract_twoples(self.pos, (self.panel_button.style.WIDTH, 0))
            self.stats.hidden = False
            self.minimap.hidden = False
        else:
            self.panel_button.pos = (settings.WINDOW_WIDTH-self.panel_button.style.WIDTH, 0)
            self.stats.hidden = True
            self.minimap.hidden = True

    def update_stats(self, clock: Clock, e_man: EntityManager, metrics: Metrics) -> None:
        self.stats.clear()
        self.stats.add_stat("fps: ",
                            str(int(pygame.time.Clock.get_fps(clock.clock))))
        self.stats.add_stat("entities: ", 
                            str(len(e_man.entities)))
        self.stats.add_stat("entities all time: ", 
                            str(e_man.created))
        self.stats.add_stat("diseased entities: ", 
                            str(e_man.get_diseased_entities(e_man.entities)))
        self.stats.add_stat("entities eaten: ", 
                            str(e_man.eaten))
        # self.stats.add_stat("colonies: ",
        #                     str(len(c_man.colonies)))
        self.stats.add_stat("time elapsed: ", metrics.get_time_elapsed())
        self.stats.add_stat("entities per minute: ", 
                            str(int(metrics.get_rate("created") - metrics.get_rate("destroyed"))), 
                            color=colors.GREEN)
        self.stats.add_stat("created per minute: ", 
                            str(int(metrics.get_rate("created"))), 
                            color=colors.BLUE)
        self.stats.add_stat("destroyed per minute: ", 
                            str(int(metrics.get_rate("destroyed"))), 
                            color=colors.RED)
        self.stats.add_stat("diseased per minute: ", 
                            str(int(metrics.get_rate("diseased"))), 
                            colors.BROWN)
        # self.stats.add_stat("eaten per minute: ", 
        #                     str(int(metrics.get_rate("eaten"))), 
        #                     colors.ORANGE)

    # helpers
