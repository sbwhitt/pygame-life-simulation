import pygame
import random
import src.utils.utils as utils
import static.settings as settings
from src.entities.dna import DNA


class Entity:
    def __init__(self, *args):
        self.rect = pygame.Rect(
            args[0], args[1], settings.ENT_WIDTH, settings.ENT_WIDTH)
        self.loc = (args[0], args[1])
        self.choice = 0
        self.bound = False
        self.colony = None
        # up, left, down, right
        self.edges = [True, True, True, True]
        if len(args) == 3:
            self.dna = DNA(args[2])
        else:
            self.dna = DNA(utils.get_random_color())

    def update(self, width: int, height: int, surroundings: list["Entity"]) -> "Entity":
        neighbor = self._choose_neighbor(surroundings)
        if neighbor != None:
            return neighbor
        if (not self.bound and self.dna.dir_timer > settings.DIR_INTERVAL):
            self._choose_dir(surroundings, width, height)
        return None

    def reproduce(self) -> "Entity|None":
        self.dna.genes += 1
        r = random.randint(0, 1+self.dna.amnt_offspring)
        spawn_loc = self._choose_spawn_location()
        if not self.dna.diseased and spawn_loc and (self.dna.nourished or r == 1):
            offspring = Entity(spawn_loc[0], spawn_loc[1])
            if random.randint(1, settings.MUTATE_CHANCE) == 1:
                # chance to mutate diseased into a new random color
                offspring.dna.mutate()
            else:
                offspring.dna.inherit(self.dna)
            
            self._degenerate()
            self._broadcast(offspring)
            return offspring
        return None
    
    def look_for_colony(self, surroundings: list["Entity"]) -> "Entity":
        for s in surroundings:
            if s: 
                neighbor = self._check_neighbor(s)
                if neighbor != None and neighbor.colony != self.colony and neighbor.bound:
                    if neighbor.dna.diseased and random.randint(1, settings.DISEASE_SPREAD_CHANCE) == 1:
                        self.dna.diseased = True
                        return None
                    return neighbor
        return None
    
    def scan_edges(self, surroundings: list["Entity"]) -> None:
        for i in range(len(surroundings)):
            if surroundings[i] and surroundings[i].bound:
                    self.edges[i] = False
                    if self.bound and random.randint(1, 4) == 1:
                        self.dna.send_color(surroundings[i].dna)
            else: self.edges[i] = True
    
    def _move(self, width: int, height: int, choice: int) -> None:
        if self.dna.move_timer > settings.MOVE_INTERVAL:
            if choice == 0 and self.rect.top != 0:  # up
                self.rect = self.rect.move(0, -settings.ENT_WIDTH)
            elif choice == 1 and self.rect.left != 0:  # left
                self.rect = self.rect.move(-settings.ENT_WIDTH, 0)
            elif choice == 2 and self.rect.bottom <= height:  # down
                self.rect = self.rect.move(0, settings.ENT_WIDTH)
            elif choice == 3 and self.rect.right < width:  # right
                self.rect = self.rect.move(settings.ENT_WIDTH, 0)
            self.dna.move_timer = 0
            self.loc = (self.rect.left, self.rect.top)
    
    def _choose_dir(self, surroundings: list["Entity"], width: int, height: int) -> int:
        self.dna.dir_timer = 0
        choices = -1
        for s in surroundings:
            if not s: choices += 1
        if choices > 0:
            self._move(width, height, random.randint(0, choices))
    
    def _choose_spawn_location(self) -> tuple|None:
        # up left down right
        dirs = [(0, -settings.ENT_WIDTH), (-settings.ENT_WIDTH, 0), (0, settings.ENT_WIDTH), (settings.ENT_WIDTH, 0)]
        for i in range(len(self.edges)):
            if self.edges[i]:
                return (self.loc[0] + dirs[i][0], self.loc[1] + dirs[i][1])
        return None

    def _degenerate(self) -> None:
        self.dna.nourished = False
        self.dna.amnt_offspring += 1
        if random.randint(0, 1):
            self.dna.age_limit -= 1
    
    def _broadcast(self, offspring) -> None:
        if not settings.IN_GAME_SETTINGS["LOGGING"]:
            return
        if offspring.dna.diseased:
            print("an entity of generation " +
                    str(self.dna.generation) + " has reproduced with disease")
        elif offspring.dna.immune:
            print("an entity of generation " +
                    str(self.dna.generation) + " has reproduced with immunity")
        else:
            print("an entity of generation " +
                    str(self.dna.generation) + " has reproduced")
    
    def _check_neighbor(self, collision: "Entity") -> "Entity":
        if collision.dna.diseased and random.randint(1, settings.DISEASE_SPREAD_CHANCE) == 1:
            self.dna.diseased = True
            return None
        if self.dna.compatible(collision.dna):
            return collision
    
    def _choose_neighbor(self, surroundings: list["Entity"]) -> "Entity":
        for i in range(len(surroundings)):
            if random.randint(1, 10) == 1 and surroundings[i] != None:
                neighbor = self._check_neighbor(surroundings[i])
                if neighbor != None:
                    return neighbor
        return None
