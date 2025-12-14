import pygame
import static.colors as colors
from static.settings import Settings as settings
import utils.utils as utils
from interface.interface_element import InterfaceElement
from interface.window import Window
from utils.clock import Clock
from tracking.metrics import Metrics
from entities.entity import Entity
from interface.components.panel_button import PanelButton
from entities.entity_manager import EntityManager
from styles.panel_styles import SidePanelStyle
from styles.panel_styles import PanelButtonStyle
from interface.components.stats import Stats
from interface.components.mini_map import MiniMap


class SidePanel(InterfaceElement):
    def __init__(self, window: Window) -> None:
        style = SidePanelStyle()
        pos = (settings.WINDOW_WIDTH-style.WIDTH, 0)
        InterfaceElement.__init__(self, style, pos)
        self.panel_button = PanelButton(utils.subtract_twoples(self.pos, (PanelButtonStyle.WIDTH, 0)))
        self.panel_open = True
        self.stats = Stats()
        self.minimap = MiniMap(window)
    
    def render(self, screen: pygame.Surface, entities: list[Entity]) -> None:
        self.panel_button.render(screen, self.panel_open)
        if self.panel_open:
            self.stats.render(screen)
            self.minimap.render(screen, entities)

    def handle_click(self, button: int) -> None:
        if self.panel_button.hovering():
            if button == settings.LEFT_CLICK:
                self.toggle_panel()
        elif self.minimap.hovering():
            if button == settings.LEFT_CLICK:
                self.minimap.handle_click(pygame.mouse.get_pos())
    
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
