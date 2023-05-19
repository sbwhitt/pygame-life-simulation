import pygame
import static.settings as settings


class Clock:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.tock = 0
    
    def tick(self) -> int:
        self.clock.tick(settings.CLOCK_RATE)
        self.tock = self.clock.get_time()
        return self.tock
