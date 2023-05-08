import pygame
import random
import static.settings as settings


class DNA:
    def __init__(self, color):
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
        self.color = color
    
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
