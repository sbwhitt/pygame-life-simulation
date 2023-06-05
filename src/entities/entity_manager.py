import pygame
import random
import src.utils.utils as utils
import static.colors as colors
from static.settings import Settings as settings
from src.entities.entity import Entity
from src.utils.map import Map
from src.interface.window import Window
from src.colonies.colony_manager import ColonyManager
from src.utils.clock import Clock


class EntityManager:
    def __init__(self, screen: pygame.Surface,
                 map: Map=None,
                 entities: list[Entity]=None,
                 created: int=None,
                 destroyed: int=None,
                 diseased: int=None,
                 eaten: int=None):
        self.screen = screen
        self.m = map if map else Map()
        self.entities = entities if entities else []
        self.selected = []
        self.created = created if created else 0
        self.destroyed = destroyed if destroyed else 0
        self.diseased = diseased if diseased else 0
        self.eaten = eaten if eaten else 0
        self.dir_timer = 0
        self.move_timer = 0
        self.avg_color = pygame.Color(0, 0, 0)

    def update_entities(self, clock_time: int, c_man: ColonyManager) -> None:
        e: Entity
        for e in self.entities:
            surroundings = self.m.get_surroundings(e.loc)
            if not e.bound:
                e.dna.dir_timer += clock_time
                e.dna.move_timer += clock_time
                self.m.grid[e.loc].remove(e)
                neighbor = e.update(surroundings)
                if neighbor != None: c_man.bind(e, neighbor)
                self.m.grid[e.loc].append(e)
            elif e.bound:
                neighbor = e.look_for_colony(surroundings)
                if neighbor != None:
                    c_man.bind(e, neighbor)
                    self._spread_characteristics(e, neighbor)
            self._handle_collisions(e)
            self._handle_aging(e, clock_time, surroundings)
            e.scan_edges(self.m.get_surroundings(e.loc))

    def render_entities(self, window: Window) -> None:
        e: Entity
        for e in self.entities:
            # if window.under_stats(e.loc):
            #     pygame.draw.rect(self.screen, colors.GRAY,
            #                      e.rect.copy().move(-window.offset[0], -window.offset[1]), border_radius=0)
            if not window.contains(e.loc):
                continue
            if e.dna.diseased and settings.IN_GAME_SETTINGS["MARK_DISEASED"]:
                pygame.draw.rect(self.screen, colors.BLACK,
                                 e.rect.copy().move(-window.offset[0], -window.offset[1]), border_radius=0)
            else:
                pygame.draw.rect(self.screen, e.dna.color,
                                 e.rect.copy().move(-window.offset[0], -window.offset[1]), border_radius=0)
    
    def render_selected(self, window: Window, clock: Clock) -> None:
        if clock.metronome:
            return
        for e in self.selected:
            pygame.draw.lines(self.screen, colors.GRAY, True, utils.get_rect_outline(e.rect, window.offset), 2)

    def add_start_entities(self, window: Window) -> None:
        for e in [
            Entity(0+window.offset[0], 0+window.offset[1], colors.RED),
            Entity(int(window.offset[0]+((window.width)/2)), 0+window.offset[1], colors.GREEN),
            Entity(window.width+window.offset[0]-settings.ENT_WIDTH, 0+window.offset[1], colors.BLUE),
            Entity(0+window.offset[0], window.height+window.offset[1]-settings.ENT_WIDTH, colors.YELLOW),
            Entity(int(window.offset[0]+((window.width)/2)), window.height+window.offset[1]-settings.ENT_WIDTH, colors.CYAN),
            Entity(window.width+window.offset[0]-settings.ENT_WIDTH, window.height+window.offset[1] -
                   settings.ENT_WIDTH, colors.MAGENTA)
        ]:
            self._add_entity(e)
    
    def remove_entity(self, e: Entity) -> None:
        self.m.grid[e.loc].remove(e)
        self.entities.remove(e)
        if e.bound:
            e.colony.remove_member(e)
            e.colony = None
        if e in self.selected:
            self.selected.remove(e)
        self.destroyed += 1
        self._obituary(e)

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

    # mouse command function helpers
    def place_entity(self, pos: tuple, atts: dict) -> None:
        e = Entity(pos[0], pos[1], atts["color"])
        e.dna.diseased = atts["diseased"]
        e.dna.immune = atts["immune"]
        e.dna.immortal = atts["immortal"]
        e.dna.immobile = atts["immobile"]
        e.dna.sterile = atts["sterile"]
        e.dna.unbindable = atts["unbindable"]
        self._add_entity(e)

    def get_attributes(self, e: Entity) -> dict:
        return {
            "color": e.dna.color,
            "diseased": e.dna.diseased,
            "immune": e.dna.immune,
            "immortal": e.dna.immortal,
            "immobile": e.dna.immobile,
            "sterile": e.dna.sterile,
            "unbindable": e.dna.unbindable
        }
    
    def select_entity(self, e: Entity) -> None:
        if e not in self.selected: self.selected.append(e)

    def select_all_entities(self) -> None:
        self.selected = self.entities.copy()

    def clear_selected(self) -> None:
        self.selected.clear()

    def zoom_in_entities(self, speed: int) -> None:
        self.m.rebuild_map_in(speed)
        e: Entity
        for e in self.entities:
            loc_adj = utils.multiply_twople_by_constant(e.loc, speed)
            e.rect.update(loc_adj[0], loc_adj[1], e.rect.width*speed, e.rect.height*speed)
            e.loc = loc_adj
            self.m.grid[e.loc].append(e)

    def zoom_out_entities(self, speed: int) -> None:
        self.m.rebuild_map_out(speed)
        e: Entity
        for e in self.entities:
            loc_adj = utils.divide_twople_by_constant(e.loc, speed)
            e.rect.update(loc_adj[0], loc_adj[1], e.rect.width/speed, e.rect.height/speed)
            e.loc = loc_adj
            self.m.grid[e.loc].append(e)

    # key command function helpers
    def cull(self) -> None:
        for i in range(int(len(self.entities)/2)):
            self.remove_entity(self.entities[i])

    def randomize_color(self) -> None:
        for e in self.selected:
            e.dna.color = utils.get_random_color(10, 245)
        self.clear_selected()

    def update_all_colors(self, color) -> None:
        for e in self.selected:
            e.dna.color.update(color)
        self.clear_selected()

    def shift_colors(self) -> None:
        for e in self.selected:
            r_cpy, g_cpy, b_cpy = e.dna.color.r, e.dna.color.g, e.dna.color.b
            e.dna.color.update(g_cpy, b_cpy, r_cpy)
        self.clear_selected()

    def flip_colors(self) -> None:
        for e in self.selected:
            r_cpy, g_cpy, b_cpy = e.dna.color.r, e.dna.color.g, e.dna.color.b
            e.dna.color.update(255-g_cpy, 255-b_cpy, 255-r_cpy)
        self.clear_selected()
    
    def delete_selected(self) -> None:
        while len(self.selected) > 0:
            self.remove_entity(self.selected[len(self.selected)-1])
        self.clear_selected()

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

    def _spread_characteristics(self, e1: Entity, e2: Entity) -> None:
        e1.dna.send_color(e2.dna)
        r = random.randint(1, 4)
        if e1.dna.diseased or e2.dna.diseased:
            self._spread_disease([e1, e2])
            return
        elif r == 1:
            e1.dna.age_limit += 1
            e2.dna.age_limit += 1
        elif r == 2:
            e1.dna.nourished = True
            e2.dna.nourished = True

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
            if not e.dna.diseased and not e.dna.immune:
                e.dna.diseased = True
                self.diseased += 1

    def _cannibalize(self, eater: Entity, collisions: list[Entity]) -> None:
        for c in collisions:
            if c != eater and random.randint(0, 1) == 1:
                self._spread_color([eater, c])
                eater.dna.age_limit += 1
                eater.dna.nourished = True
                c.dna.eaten = True
                self.eaten += 1
                self.remove_entity(c)

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

    def _handle_aging(self, e: Entity, clock_time: int, surroundings: list[Entity]) -> None:
        if e.dna.age_timer > settings.AGE_LENGTH:
            if not e.dna.immortal:
                if e.dna.diseased:
                    self.remove_entity(e)
                    return
                e.dna.age += 1
                if e.dna.age >= e.dna.age_limit:
                    self.remove_entity(e)
                    return
            if len(self.entities) < settings.ENTITY_LIMIT:
                offspring = e.reproduce(surroundings)
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
