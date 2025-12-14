import pygame
import random
import utils.utils as utils
from static.settings import Settings as settings
from entities.dna import DNA


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

    def update(self, surroundings: list["Entity"]) -> "Entity":
        # if self.dna.diseased:
        #     self.dna.recover()
        if not self.dna.unbindable:
            neighbor = self._choose_neighbor(surroundings)
            if neighbor != None:
                return neighbor
        if not self.dna.immobile and (not self.bound and self.dna.dir_timer > settings.DIR_INTERVAL):
            self._move(self._choose_dir(surroundings))
        return None

    def reproduce(self, surroundings: list["Entity"]) -> "Entity|None":
        if self.dna.sterile: return
        self.dna.genes += 1
        r = random.randint(0, 1+self.dna.amnt_offspring)
        spawn_loc = self._choose_spawn_location(surroundings)
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
                    if not self.dna.immune and neighbor.dna.diseased and random.randint(1, settings.DISEASE_SPREAD_CHANCE) == 1:
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

    # helpers
    
    def _move(self, choice: int) -> None:
        if self.dna.move_timer > settings.MOVE_INTERVAL:
            if choice == 0 and self.rect.top != 0:  # up
                self.rect = self.rect.move(settings.DIRS[choice][0], settings.DIRS[choice][1])
            elif choice == 1 and self.rect.left != 0:  # left
                self.rect = self.rect.move(settings.DIRS[choice][0], settings.DIRS[choice][1])
            elif choice == 2 and self.rect.bottom <= settings.WORLD_SIZE:  # down
                self.rect = self.rect.move(settings.DIRS[choice][0], settings.DIRS[choice][1])
            elif choice == 3 and self.rect.right < settings.WORLD_SIZE:  # right
                self.rect = self.rect.move(settings.DIRS[choice][0], settings.DIRS[choice][1])
            self.dna.move_timer = 0
            self.loc = (self.rect.left, self.rect.top)
    
    def _choose_dir(self, surroundings: list["Entity"]) -> int:
        self.dna.dir_timer = 0
        choices = []
        for i in range(len(surroundings)):
            if not surroundings[i]: choices.append(i)
        if len(choices) > 0:
            return choices[random.randint(0, len(choices)-1)]
        return -1
    
    def _choose_spawn_location(self, surroundings: list["Entity"]) -> tuple|None:       
        choice = self._choose_dir(surroundings)
        if choice >= 0:
            spawn_loc = utils.add_twoples(self.loc, settings.DIRS[choice])
            return spawn_loc
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
        if not self.dna.immune and collision.dna.diseased and random.randint(1, settings.DISEASE_SPREAD_CHANCE) == 1:
            self.dna.diseased = True
            return None
        if self.dna.compatible(collision.dna):
            return collision
    
    def _choose_neighbor(self, surroundings: list["Entity"]) -> "Entity":
        for i in range(len(surroundings)):
            if random.randint(1, 10) == 1 and surroundings[i] != None:
                neighbor = self._check_neighbor(surroundings[i])
                if neighbor != None and not neighbor.dna.unbindable:
                    return neighbor
        return None
