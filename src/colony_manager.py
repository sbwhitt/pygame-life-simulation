import pygame
import static.colors as colors
import static.settings as settings
from src.colony import Colony
from src.entity import Entity
from src.window import Window


class ColonyManager:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.colonies = []
        self.created = 0
        self.destroyed = 0
    
    def update_colonies(self) -> None:
        for c in self.colonies:
            if len(c.members) <= 1:
                for e in c.members:
                    e.bound = False
                self._remove_colony(c)
    
    def render_colonies(self, window: Window) -> None:
        for c in self.colonies:
            for e in c.members:
                if settings.IN_GAME_SETTINGS["HIGHLIGHT"] and e.bound and window.contains(e.loc):
                    self._highlight(e, window)
    
    def bind(self, e1: Entity, e2: Entity) -> None:
        e1.dna.send_color(e2.dna)
        e1.dna.age_limit += 1
        e2.dna.age_limit += 1
        e1.nourished = True
        e2.nourished = True
        if e1.colony and e2.colony:
            pass
        elif e1.colony and not e2.colony:
            e1.colony.add_member(e2)
            e2.colony = e1.colony
            e2.bound = True
        elif not e1.colony and e2.colony:
            e2.colony.add_member(e1)
            e1.colony = e2.colony
            e1.bound = True
        else:
            c = Colony()
            self._add_colony(c)
            c.add_member(e1)
            c.add_member(e2)
            e1.colony = c
            e2.colony = c
            e1.bound = True
            e2.bound = True
    
    # helpers
    def _add_colony(self, colony: Colony) -> None:
        self.colonies.append(colony)
        self.created += 1

    def _remove_colony(self, colony: Colony) -> None:
        for e in colony.members:
            e.colony = None
        colony.members = []
        self.colonies.remove(colony)
        self.destroyed += 1

    def _highlight(self, entity: Entity, window: Window) -> None:
        points = [(entity.loc[0]-(entity.loc[0] % settings.ENT_WIDTH), entity.loc[1]-(entity.loc[1] % settings.ENT_WIDTH)),
                  (entity.loc[0]+(settings.ENT_WIDTH - entity.loc[0] % settings.ENT_WIDTH), entity.loc[1]-(entity.loc[1] % settings.ENT_WIDTH)),
                  (entity.loc[0]+(settings.ENT_WIDTH - entity.loc[0] % settings.ENT_WIDTH), entity.loc[1]+(settings.ENT_WIDTH - entity.loc[1] % settings.ENT_WIDTH)),
                  (entity.loc[0]-(entity.loc[0] % settings.ENT_WIDTH), entity.loc[1]+(settings.ENT_WIDTH - entity.loc[1] % settings.ENT_WIDTH))]
        for i in range(len(points)):
            points[i] = (points[i][0]-window.offset[0], points[i][1]-window.offset[1])
        pygame.draw.lines(self.screen, colors.GRAY, True, points, 2)