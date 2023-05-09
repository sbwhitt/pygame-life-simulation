import pygame
import random
import static.colors as colors
import static.settings as settings
from src.entity import Entity
from src.map import Map
from src.window import Window


class EntityManager:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.m = Map(settings.WORLD_SIZE, settings.WORLD_SIZE)
        self.entities = []
        self.created = 0
        self.destroyed = 0
        self.diseased = 0
        self.eaten = 0
        self.dir_timer = 0
        self.move_timer = 0
        self.avg_color = pygame.Color(0, 0, 0)

    def update_entities(self, clock_time: int) -> None:
        for e in self.entities:
            e.dna.dir_timer += clock_time
            e.dna.move_timer += clock_time
            self.m.grid[e.loc].remove(e)
            if not e.bound: e.update(settings.WORLD_SIZE, settings.WORLD_SIZE, self.m.get_surroundings(e.loc))
            self.m.grid[e.loc].append(e)
            self._handle_collisions(e)
            self._handle_aging(e, clock_time)

    def render_entities(self, window: Window) -> None:
        for e in self.entities:
            # if window.under_stats(e.loc):
            #     pygame.draw.rect(self.screen, colors.GRAY,
            #                      e.rect.copy().move(-window.offset[0], -window.offset[1]), border_radius=0)
            if not window.contains(e.loc):
                continue
            if e.bound:
                self._highlight(e, window)
            if e.dna.diseased and settings.IN_GAME_SETTINGS["MARK_DISEASED"]:
                pygame.draw.rect(self.screen, colors.BLACK,
                                 e.rect.copy().move(-window.offset[0], -window.offset[1]), border_radius=0)
            else:
                pygame.draw.rect(self.screen, e.dna.color, 
                                 e.rect.copy().move(-window.offset[0], -window.offset[1]), border_radius=0)

    def add_start_entities(self, window: Window) -> None:
        for e in [
            Entity(0+window.offset[0], 0+window.offset[1], colors.RED),
            Entity(int((window.width+window.offset[0])/2), 0+window.offset[1], colors.GREEN),
            Entity(window.width+window.offset[0]-settings.ENT_WIDTH, 0+window.offset[1], colors.BLUE),
            Entity(0+window.offset[0], window.height+window.offset[1]-settings.ENT_WIDTH, colors.YELLOW),
            Entity(int((window.width+window.offset[0])/2), window.height+window.offset[1]-settings.ENT_WIDTH, colors.CYAN),
            Entity(window.width+window.offset[0]-settings.ENT_WIDTH, window.height+window.offset[1] -
                   settings.ENT_WIDTH, colors.MAGENTA)
        ]:
            self._add_entity(e)

    def build_entities(self, window: Window) -> None:
        self.add_start_entities(window)
        # self.avg_color = self.find_avg_color()
        self.created = len(self.entities)

    def get_diseased_entities(self, entities: list[Entity]) -> int:
        res = 0
        for e in entities:
            if e.dna.diseased:
                res += 1
        return res

    def find_avg_color(self) -> pygame.Color:
        r, g, b = 0, 0, 0
        for e in self.entities:
            r += e.dna.color.r
            g += e.dna.color.g
            b += e.dna.color.b
        num_e = len(self.entities)
        return pygame.Color(int(r/num_e), int(g/num_e), int(b/num_e))

    # key command function helpers
    def cull(self) -> None:
        for i in range(int(len(self.entities)/2)):
            self._remove_entity(self.entities[i])

    def randomize_color(self) -> None:
        for e in self.entities:
            e.dna.color = pygame.Color(random.randint(
                10, 245), random.randint(10, 245), random.randint(10, 245))

    def update_all_colors(self, color) -> None:
        for e in self.entities:
            e.dna.color.update(color)

    def shift_colors(self) -> None:
        for e in self.entities:
            r_cpy, g_cpy, b_cpy = e.dna.color.r, e.dna.color.g, e.dna.color.b
            e.dna.color.update(g_cpy, b_cpy, r_cpy)

    def flip_colors(self) -> None:
        for e in self.entities:
            r_cpy, g_cpy, b_cpy = e.dna.color.r, e.dna.color.g, e.dna.color.b
            e.dna.color.update(255-g_cpy, 255-b_cpy, 255-r_cpy)

    # helpers
    def _add_entity(self, e: Entity) -> None:
        if self.m.grid.get(e.loc) == None: return
        self.m.grid[e.loc].append(e)
        self.entities.append(e)
        self.created += 1
        if e.dna.diseased:
            self.diseased += 1
        # self.avg_color = self._tally_avg_color(
        #     self.find_avg_color())

    def _remove_entity(self, e: Entity) -> None:
        self.m.grid[e.loc].remove(e)
        self.entities.remove(e)
        self.destroyed += 1
        self._obituary(e)
    
    def _highlight(self, entity: Entity, window: Window) -> None:
        points = [(entity.loc[0]-(entity.loc[0] % settings.ENT_WIDTH), entity.loc[1]-(entity.loc[1] % settings.ENT_WIDTH)),
                  (entity.loc[0]+(settings.ENT_WIDTH - entity.loc[0] % settings.ENT_WIDTH), entity.loc[1]-(entity.loc[1] % settings.ENT_WIDTH)),
                  (entity.loc[0]+(settings.ENT_WIDTH - entity.loc[0] % settings.ENT_WIDTH), entity.loc[1]+(settings.ENT_WIDTH - entity.loc[1] % settings.ENT_WIDTH)),
                  (entity.loc[0]-(entity.loc[0] % settings.ENT_WIDTH), entity.loc[1]+(settings.ENT_WIDTH - entity.loc[1] % settings.ENT_WIDTH))]
        for i in range(len(points)):
            points[i] = (points[i][0]-window.offset[0], points[i][1]-window.offset[1])
        pygame.draw.lines(self.screen, colors.BLACK, True, points, 3)

    def _spread_color(self, collisions: list[Entity]) -> None:
        r, g, b = 0, 0, 0
        highest_off = 0
        for e in collisions:
            highest_off = e.dna.amnt_offspring if e.dna.amnt_offspring > highest_off else highest_off
            r += e.dna.color.r
            g += e.dna.color.g
            b += e.dna.color.b
        c = pygame.Color(int(r/len(collisions)),
                         int(g/len(collisions)), int(b/len(collisions)))
        for e in collisions:
            e.dna.color = c.lerp(e.dna.color, 0.5)

    def _spread_disease(self, collisions: list[Entity]) -> None:
        for e in collisions:
            if not e.dna.diseased and not e.dna.immune and random.randint(0, 1) == 1:
                e.dna.diseased = True
                self.diseased += 1

    def _spread_curve(self, collisions: list[Entity]) -> None:
        c = 0
        for e in collisions:
            c += e.dna.curve
        c = int(c/len(collisions))
        for e in collisions:
            e.dna.curve = c

    def _cannibalize(self, eater: Entity, collisions: list[Entity]) -> None:
        for c in collisions:
            if c != eater and random.randint(0, 1) == 1:
                self._spread_color([eater, c])
                eater.dna.age_limit += 1
                eater.dna.curve = int( (eater.dna.curve + c.dna.curve)/2 )
                eater.dna.nourished = True
                c.dna.eaten = True
                self.eaten += 1
                self._remove_entity(c)

    def _handle_collisions(self, e: Entity) -> None:
        collisions = self.m.grid[e.loc]
        if len(collisions) > 1:
            if e.dna.diseased:
                self._spread_disease(collisions)
            if random.randint(1, 3) == 1:
                self._spread_color(collisions)
            # if random.randint(1, 3) == 1:
            #     self._spread_curve(collisions)
            if random.randint(1, 50) == 1:
                self._cannibalize(e, collisions)

    def _handle_aging(self, e: Entity, clock_time: int) -> None:
        if e.dna.age_timer > settings.AGE_LENGTH:
            e.dna.age += 1
            if e.dna.age >= e.dna.age_limit:
                self._remove_entity(e)
                return
            if len(self.entities) < settings.ENTITY_LIMIT:
                offspring = e.reproduce()
                if offspring:
                    self._add_entity(offspring)
            e.dna.age_timer = 0
        else:
            e.dna.age_timer += clock_time

    def _obituary(self, e: Entity) -> None:
        if not settings.IN_GAME_SETTINGS["LOGGING"]:
            return
        if e.dna.diseased:
            print("an entity of generation " + str(e.dna.generation) + " has perished from disease after " +
                  str(e.dna.age) + " ages, leaving " + str(e.dna.amnt_offspring) + " offspring")
        elif e.dna.eaten:
            print("an entity of generation " + str(e.dna.generation) + " has been eaten after " +
                  str(e.dna.age) + " ages, leaving " + str(e.dna.amnt_offspring) + " offspring")
        else:
            print("an entity of generation " + str(e.dna.generation) + " has perished after " +
                  str(e.dna.age) + " ages, leaving " + str(e.dna.amnt_offspring) + " offspring")

    # probably broken, is it obvious??
    def _tally_avg_color(self, current_avg: tuple) -> pygame.Color:
        ents = len(self.entities)
        r, g, b = int(((ents-1)*self.avg_color.r + current_avg.r)/ents), int(((ents-1) *
                                                                              self.avg_color.g + current_avg.g)/ents), int(((ents-1)*self.avg_color.b + current_avg.b)/ents)
        return pygame.Color(r, g, b)