import pygame
import random
import static.settings as settings
from src.dna import DNA


class Entity:
    def __init__(self, *args):
        self.rect = pygame.Rect(
            args[0], args[1], settings.ENT_WIDTH, settings.ENT_WIDTH)
        self.loc = (args[0], args[1])
        self.choice = 0
        self.bound = False
        if len(args) == 3:
            self.dna = DNA(args[2])
        else:
            self.dna = DNA(pygame.Color(random.randint(
                10, 200), random.randint(10, 200), random.randint(10, 200)))

    def update(self, width: int, height: int, surroundings: list[list["Entity"] | None]) -> None:
        self.choice = self._choose_dir(surroundings)
        if self.dna.move_timer > settings.MOVE_INTERVAL:
            if self.choice == 0 and self.rect.top != 0:  # up
                self.rect = self.rect.move(0, -settings.ENT_WIDTH)
            elif self.choice == 1 and self.rect.left != 0:  # left
                self.rect = self.rect.move(-settings.ENT_WIDTH, 0)
            elif self.choice == 2 and self.rect.bottom != height:  # down
                self.rect = self.rect.move(0, settings.ENT_WIDTH)
            elif self.choice == 3 and self.rect.right != width:  # right
                self.rect = self.rect.move(settings.ENT_WIDTH, 0)
            self.dna.move_timer = 0
            self.loc = (self.rect.left, self.rect.top)

    def reproduce(self) -> "Entity|None":
        r = random.randint(0, 1+self.dna.amnt_offspring)
        if (self.dna.nourished or r == 1) and not self.dna.diseased:
            offspring = Entity(self.rect.left, self.rect.top)
            if random.randint(1, 100) == 1:
                # chance to mutate diseased into a new random color
                offspring.dna.mutate()
            else:
                offspring.dna.inherit(self.dna)
            
            self._degenerate()
            self._broadcast(offspring)
            return offspring
        return None

    def _degenerate(self) -> None:
        self.dna.nourished = False
        self.dna.amnt_offspring += 1
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

    def _is_safe(self, target: list["Entity"]) -> bool:
        for e in target:
            if e.dna.diseased:
                return False
        return True

    def _is_empty(self, target: list["Entity"]) -> bool:
        if len(target) > 0:
            return False
        return True
    
    def _bind(self, collisions: list["Entity"]) -> bool:
        for c in collisions:
            if self.dna.compatible(c.dna):
                self.bound = True
                c.bound = True
                return True
        return False

    def _choose_dir(self, surroundings: list[list["Entity"] | None]) -> int:
        if (not self.bound and self.dna.dir_timer > settings.DIR_INTERVAL):
            self.dna.dir_timer = 0
            choices = []
            for i in range(len(surroundings)):
                if surroundings[i] != None and self._is_safe(surroundings[i]):
                    if random.randint(1, 5) == 1 and self._bind(surroundings[i]): return
                    choices.append(i)
            if choices:
                c = choices[random.randint(0, len(choices)-1)]
                return c
            else:
                return -1
