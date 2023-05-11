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
        if e1.dna.diseased or e2.dna.diseased:
            e1.dna.diseased, e2.dna.diseased = True, True
        else:
            e1.dna.age_limit += 1
            e2.dna.age_limit += 1
            e1.nourished = True
            e2.nourished = True
        if e1.colony and e2.colony:
            # self._join_colonies(e1.colony, e2.colony)
            pass
        elif e1.colony and not e2.colony:
            e1.colony.add_member(e2)
            e2.bound = True
        elif not e1.colony and e2.colony:
            e2.colony.add_member(e1)
            e1.bound = True
        else:
            c = Colony()
            self._add_colony(c)
            c.add_member(e1)
            c.add_member(e2)
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
    
    def _join_colonies(self, c1: "Colony", c2: "Colony") -> None:
        for i in range(len(c2.members)):
            c1.add_member(c2.members[i])
        self._remove_colony(c2)

    def _highlight(self, entity: Entity, window: Window) -> None:
        # line segments of entity: up, left, down, right
        uldr = [
            (
                # top left point
                (entity.loc[0] - (entity.loc[0] % settings.ENT_WIDTH) - window.offset[0], entity.loc[1] - (entity.loc[1] % settings.ENT_WIDTH) - window.offset[1]),
                # top right point
                (entity.loc[0] + (settings.ENT_WIDTH - entity.loc[0] % settings.ENT_WIDTH) - window.offset[0], entity.loc[1] + entity.loc[1] % settings.ENT_WIDTH - window.offset[1])
            ),
            (
                # top left point
                (entity.loc[0] - (entity.loc[0] % settings.ENT_WIDTH) - window.offset[0], entity.loc[1] - (entity.loc[1] % settings.ENT_WIDTH) - window.offset[1]),
                # bottom left point
                (entity.loc[0] - (entity.loc[0] % settings.ENT_WIDTH) - window.offset[0], settings.ENT_WIDTH + (entity.loc[1] - (entity.loc[1] % settings.ENT_WIDTH)) - window.offset[1])
            ),
            (
                # bottom left point
                (entity.loc[0] - (entity.loc[0] % settings.ENT_WIDTH) - window.offset[0], settings.ENT_WIDTH + (entity.loc[1] - (entity.loc[1] % settings.ENT_WIDTH)) - window.offset[1]),
                # bottom right point
                (settings.ENT_WIDTH + entity.loc[0] - entity.loc[0] % settings.ENT_WIDTH - window.offset[0], settings.ENT_WIDTH + entity.loc[1] - entity.loc[1] % settings.ENT_WIDTH - window.offset[1])
            ),
            (
                # top right point
                (entity.loc[0] + (settings.ENT_WIDTH - entity.loc[0] % settings.ENT_WIDTH) - window.offset[0], entity.loc[1] + (settings.ENT_WIDTH - entity.loc[1] % settings.ENT_WIDTH) - window.offset[1]),
                # bottom right point
                (settings.ENT_WIDTH + entity.loc[0] - entity.loc[0] % settings.ENT_WIDTH - window.offset[0], entity.loc[1] - entity.loc[1] % settings.ENT_WIDTH - window.offset[1])
            )
        ]
        for i in range(len(entity.edges)):
            if entity.edges[i]:
                pygame.draw.lines(self.screen, colors.BLACK, True, uldr[i], 2)
