import pygame
import settings
import random

class Entity:
    def __init__(self, *args):
        self.rect = pygame.Rect(args[0], args[1], settings.ENT_WIDTH, settings.ENT_WIDTH)
        self.loc = (args[0], args[1])
        self.choice = random.randint(1, 5)
        self.age = 0
        self.age_limit = random.randint(3, 6)
        self.age_timer = 0
        self.move_timer = 0
        self.dir_timer = 0
        self.amnt_offspring = 0
        self.generation = 1
        self.diseased = False
        if len(args) == 3:
            self.color = args[2]
        else:
            self.color = pygame.Color(random.randint(10, 200), random.randint(10, 200), random.randint(10, 200))
    
    def update(self, width, height, surroundings) -> None:
        self.choice = self._choose_dir(surroundings)
        if self.move_timer > settings.MOVE_INTERVAL:
            if self.choice == 0 and self.rect.top != 0: #up
                self.rect = self.rect.move(0, -settings.ENT_WIDTH)
            elif self.choice == 1 and self.rect.left != 0: #left
                self.rect = self.rect.move(-settings.ENT_WIDTH, 0)
            elif self.choice == 2 and self.rect.bottom != height: #down
                self.rect = self.rect.move(0, settings.ENT_WIDTH)
            elif self.choice == 3 and self.rect.right != width: #right
                self.rect = self.rect.move(settings.ENT_WIDTH, 0)
            self.move_timer = 0
            self.loc = (self.rect.left, self.rect.top)
    
    def reproduce(self):
        r = random.randint(0, 1+self.amnt_offspring)
        if r == 1 and not self.diseased:
            self.amnt_offspring += 1
            self.age_limit -= 1
            e = Entity(self.rect.left, self.rect.top)
            if random.randint(1, 100) == 1:
                # chance to mutate diseased into a new random color
                e.diseased = (random.randint(0, 2) == 1)
                e.color = pygame.Color(random.randint(10, 200), random.randint(10, 200), random.randint(10, 200))
            else:
                # inheriting and slightly mutating parent color
                e.color = self._mutate_color(self.color)
            if e.diseased:
                if settings.LOGGING: print("an entity of generation " + str(self.generation) + " has reproduced with disease")
            else:
                if settings.LOGGING: print("an entity of generation " + str(self.generation) + " has reproduced")
            e.generation = self.generation + 1
            return e
        return None
    
    def _mutate_color(self, p_color) -> pygame.Color:
        res = pygame.Color(0, 0, 0)
        if p_color.r >= 20 and p_color.r <= 235:
            res.r = random.randint(p_color.r-20, p_color.r+20)
        elif p_color.r > 235:
            res.r = random.randint(p_color.r-10, p_color.r)
        elif p_color.r < 20:
            res.r = random.randint(p_color.r, p_color.r+10)
        if p_color.g >= 20 and p_color.g <= 235:
            res.g = random.randint(p_color.g-20, p_color.g+20)
        elif p_color.g > 235:
            res.g = random.randint(p_color.g-10, p_color.g)
        elif p_color.g < 20:
            res.g = random.randint(p_color.g, p_color.g+10)
        if p_color.b >= 20 and p_color.b <= 235:
            res.b = random.randint(p_color.b-20, p_color.b+20)
        elif p_color.b > 235:
            res.b = random.randint(p_color.b-10, p_color.b)
        elif p_color.b < 20:
            res.b = random.randint(p_color.b, p_color.b+10)
        return res

    def _safe(self, target) -> bool:
        for e in target:
            if e.diseased:
                return False
        return True

    def _choose_dir(self, surroundings) -> int:
        if (self.dir_timer > settings.DIR_INTERVAL):
            self.dir_timer = 0
            choices = []
            for i in range(len(surroundings)):
                if surroundings[i] != None and self._safe(surroundings[i]):
                    choices.append(i)
            if choices:
                c = choices[random.randint(0, len(choices)-1)]
                return c
            else:
                return -1