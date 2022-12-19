import pygame
import random

class Entity:
    def __init__(self, *args):
        self.rect = pygame.Rect(args[0], args[1], 10, 10)
        self.choice = random.randint(1, 5)
        self.age = 0
        self.age_limit = random.randint(2, 5)
        self.age_timer = 0
        self.move_timer = 0
        self.dir_timer = 0
        self.amnt_offspring = 0
        self.generation = 1
        if len(args) == 3:
            self.color = self._mutate_color(args[2])
        else:
            self.color = pygame.Color(random.randint(10, 200), random.randint(10, 200), random.randint(10, 200))
    
    def update(self, height, width):
        self.choice = self._choose_dir()
        if self.move_timer > 50:
            if self.choice == 1 and self.rect.top != 0:
                self.rect = self.rect.move(0, -10)
            elif self.choice == 2 and self.rect.left != 0:
                self.rect = self.rect.move(-10, 0)
            elif self.choice == 3 and self.rect.bottom != width:
                self.rect = self.rect.move(0, 10)
            elif self.choice == 4 and self.rect.right != height:
                self.rect = self.rect.move(10, 0)
            self.move_timer = 0
            return (self.rect.top, self.rect.left)
    
    def reproduce(self):
        r = random.randint(0, 1)
        if r == 1:
            print("an entity of generation " + str(self.generation) + " has reproduced")
            self.amnt_offspring += 1
            e = Entity(self.rect.left, self.rect.top, self.color)
            e.generation = self.generation + 1
            return e
        return None
    
    def _mutate_color(self, p_color):
        res = pygame.Color(0, 0, 0)
        if p_color.r >= 20 and p_color.r <= 235:
            res.r = random.randint(p_color.r-20, p_color.r+20)
        else:
            res.r = p_color.r
        if p_color.g >= 20 and p_color.g <= 235:
            res.g = random.randint(p_color.g-20, p_color.g+20)
        else:
            res.g = p_color.g
        if p_color.b >= 20 and p_color.b <= 235:
            res.b = random.randint(p_color.b-20, p_color.b+20)
        else:
            res.b = p_color.b
        return res

    def _choose_dir(self):
        if (self.dir_timer > 700):
            self.dir_timer = 0
            return random.randint(1, 5)