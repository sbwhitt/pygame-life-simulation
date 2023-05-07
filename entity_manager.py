import pygame
import colors
import settings
import random
from entity import Entity
from map import Map


class EntityManager:
    def __init__(self, screen):
        self.screen = screen
        self.width = settings.WINDOW_WIDTH
        self.height = settings.WINDOW_HEIGHT
        self.m = Map(self.width, self.height)
        self.entities = []
        self.created = 0
        self.destroyed = 0
        self.dir_timer = 0
        self.move_timer = 0
        self.avg_color = pygame.Color(0, 0, 0)
    
    def update_entities(self, clock_time: int) -> None:
        for e in self.entities:
            e.dir_timer += clock_time
            e.move_timer += clock_time
            self.m.grid[e.loc].remove(e)
            e.update(self.width, self.height, self.m.get_surroundings(e.loc))
            self.m.grid[e.loc].append(e)
    
    def render_entities(self, clock_time: int, paused: bool) -> None:
        for e in self.entities:
            if not paused and e.age >= e.age_limit:
                self._remove_entity(e)
                continue

            if e.diseased and settings.IN_GAME_SETTINGS["MARK_DISEASED"]:
                pygame.draw.rect(self.screen, colors.BLACK, e.rect, border_radius=1)
            else:
                pygame.draw.rect(self.screen, e.color, e.rect, border_radius=1)
            if paused: continue

            self._handle_collisions(e)
            self._handle_aging(e, clock_time)

    def add_start_entities(self) -> None:
        for e in [
            Entity(0, 0, colors.RED),
            Entity(self.width/2, 0, colors.GREEN),
            Entity(self.width-settings.ENT_WIDTH, 0, colors.BLUE),
            Entity(0, self.height-settings.ENT_WIDTH, colors.YELLOW),
            Entity(self.width/2, self.height-settings.ENT_WIDTH, colors.CYAN),
            Entity(self.width-settings.ENT_WIDTH, self.height -
                   settings.ENT_WIDTH, colors.MAGENTA)
        ]:
            self._add_entity(e)
    
    def build_entities(self) -> None:
        self.add_start_entities()
        self.avg_color = self.find_avg_color()
        self.created = len(self.entities)

    def get_diseased_entities(self, entities: list[Entity]) -> int:
        res = 0
        for e in entities:
            if e.diseased:
                res += 1
        return res
    
    def find_avg_color(self) -> pygame.Color:
        r, g, b = 0, 0, 0
        for e in self.entities:
            r += e.color.r
            g += e.color.g
            b += e.color.b
        num_e = len(self.entities)
        return pygame.Color(int(r/num_e), int(g/num_e), int(b/num_e))

    # key command function helpers
    def cull(self) -> None:
        for i in range(int(len(self.entities)/2)):
            self._remove_entity(self.entities[i])
    
    def randomize_color(self) -> None:
        for e in self.entities:
            e.color = pygame.Color(random.randint(10, 245), random.randint(10, 245), random.randint(10, 245))
    
    def update_all_colors(self, color) -> None:
        for e in self.entities:
            e.color.update(color)
    
    def shift_colors(self) -> None:
        for e in self.entities:
            r_cpy, g_cpy, b_cpy = e.color.r, e.color.g, e.color.b
            e.color.update(g_cpy, b_cpy, r_cpy)

    def flip_colors(self) -> None:
        for e in self.entities:
            r_cpy, g_cpy, b_cpy = e.color.r, e.color.g, e.color.b
            e.color.update(255-g_cpy, 255-b_cpy, 255-r_cpy)
    
    # helpers
    def _add_entity(self, e: Entity) -> None:
        self.m.grid[e.loc].append(e)
        self.entities.append(e)
        self.created += 1
        self.avg_color = self._tally_avg_color(
            self.find_avg_color())

    def _remove_entity(self, e: Entity) -> None:
        self.m.grid[e.loc].remove(e)
        self.entities.remove(e)
        self.destroyed += 1
        self._obituary(e)

    def _spread_color(self, collisions: list[Entity]) -> None:
        r, g, b = 0, 0, 0
        highest_off = 0
        for e in collisions:
            highest_off = e.amnt_offspring if e.amnt_offspring > highest_off else highest_off
            r += e.color.r
            g += e.color.g
            b += e.color.b
        c = pygame.Color(int(r/len(collisions)),
                         int(g/len(collisions)), int(b/len(collisions)))
        for e in collisions:
            e.color = c.lerp(e.color, 0.5)

    def _spread_disease(self, collisions: list[Entity]) -> None:
        for e in collisions:
            if not e.diseased and not e.immune and random.randint(0, 1) == 1:
                e.diseased = True
    
    def _cannibalize(self, eater, collisions: list[Entity]) -> None:
        for c in collisions:
            if c != eater and random.randint(0, 1) == 1:
                self._spread_color([eater, c])
                eater.age_limit += 1
                eater.nourished = True
                c.eaten = True
                self._remove_entity(c)
    
    def _handle_collisions(self, e: Entity) -> None:
        collisions = self.m.grid[e.loc]
        if len(collisions) > 1:
            if e.diseased:
                self._spread_disease(collisions)
            if random.randint(1, 3) == 1:
                self._spread_color(collisions)
            if random.randint(1, 100) == 1:
                self._cannibalize(e, collisions)
    
    def _handle_aging(self, e: Entity, clock_time: int) -> None:
        if e.age_timer > settings.AGE_LENGTH:
            e.age += 1
            if len(self.entities) < settings.ENTITY_LIMIT:
                offspring = e.reproduce()
                if offspring:
                    self._add_entity(offspring)
            e.age_timer = 0
        else:
            e.age_timer += clock_time

    def _obituary(self, e: Entity) -> None:
        if not settings.IN_GAME_SETTINGS["LOGGING"]:
            return
        if e.diseased:
            print("an entity of generation " + str(e.generation) + " has perished from disease after " +
                  str(e.age) + " ages, leaving " + str(e.amnt_offspring) + " offspring")
        elif e.eaten:
            print("an entity of generation " + str(e.generation) + " has been eaten after " +
                  str(e.age) + " ages, leaving " + str(e.amnt_offspring) + " offspring")
        else:
            print("an entity of generation " + str(e.generation) + " has perished after " +
                  str(e.age) + " ages, leaving " + str(e.amnt_offspring) + " offspring")

    # probably broken, is it obvious??
    def _tally_avg_color(self, current_avg: tuple) -> pygame.Color:
        ents = len(self.entities)
        r, g, b = int(((ents-1)*self.avg_color.r + current_avg.r)/ents), int(((ents-1) *
                                                                              self.avg_color.g + current_avg.g)/ents), int(((ents-1)*self.avg_color.b + current_avg.b)/ents)
        return pygame.Color(r, g, b)
