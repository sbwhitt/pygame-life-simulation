import pygame
import static.settings as settings


class Clock:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.time = 0
        self.metronome = False
        self.metronome_counter = 0
    
    def step(self) -> int:
        self._swing()
        self.clock.tick(settings.CLOCK_RATE)
        self.time = self.clock.get_time()
        return self.time
    
    def _swing(self) -> None:
        self.metronome_counter += 1
        if self.metronome_counter == settings.METRONOME_RATE:
            self.metronome = not self.metronome
            self.metronome_counter = 0
