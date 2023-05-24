import pygame
import random
import static.settings as settings


class DNA:
    def __init__(self, color):
        self.color = color
        self.genes = random.randint(6, 24)
        self.age = 0
        self.age_limit = random.randint(3, 6)
        self.age_timer = 0
        self.curve = random.randint(0, int(settings.ENT_WIDTH/2))
        self.move_timer = 0
        self.dir_timer = 0
        self.amnt_offspring = 0
        self.generation = 1
        self.diseased = False
        self.immune = False
        self.nourished = False
        self.eaten = False
    
    def inherit(self, parent: "DNA") -> None:
        self.color = self._mutate_color(parent.color)
        self.generation = parent.generation + 1
        self.curve = parent.curve

    def mutate(self) -> None:
        self.diseased = (random.randint(0, 2) == 1)
        self.immune = (
            not self.diseased and self._determine_immunity())
        self.color = pygame.Color(random.randint(
            10, 200), random.randint(10, 200), random.randint(10, 200))
        self.curve = random.randint(0, int(settings.ENT_WIDTH/2))
    
    def compatible(self, candidate: "DNA") -> bool:
        if self._compare_colors(candidate.color):
            return True
        return False
    
    def send_color(self, target: "DNA") -> None:
        if self.genes > 0:
            c = pygame.Color(self.color.r, self.color.g, self.color.b)
            c.r = c.r+random.randint(-1, 2) if c.r < 240 and c.r > 50 else c.r
            c.g = c.g+random.randint(-1, 2) if c.g < 240 and c.g > 50 else c.g
            c.b = c.b+random.randint(-1, 2) if c.b < 240 and c.b > 50 else c.b
            c = pygame.color.Color(int((c.r + target.color.r)/2),
                                    int((c.g + target.color.g)/2),
                                    int((c.b + target.color.b)/2))
            self.color = c
            target.color = c
            self.genes -= 1

    def _compare_colors(self, color: pygame.Color) -> bool:
        return ((self.color.r - color.r <= 20 and self.color.r - color.r >= -20) and
                (self.color.g - color.g <= 20 and self.color.g - color.g >= -20) and
                (self.color.b - color.b <= 20 and self.color.b - color.b >= -20))

    def _determine_immunity(self) -> bool:
        return self.immune or (random.randint(0, 2) == 1) 

    def _mutate_color(self, p_color: pygame.Color) -> pygame.Color:
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
