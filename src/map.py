import static.settings as settings
from src.entity import Entity


class Map:
    def __init__(self, w, h):
        self.width = w
        self.height = h
        self.grid = {}
        self._build_grid()

    def get_surroundings(self, pos: tuple) -> list[list[Entity] | None]:
        surroundings = [None, None, None, None]
        for i in range(0, 4):
            if i == 0 and self.grid.get((pos[0], pos[1]-settings.ENT_WIDTH)) != None:  # up
                surroundings[0] = self.grid.get((pos[0], pos[1]-settings.ENT_WIDTH))
            if i == 1 and self.grid.get((pos[0]-settings.ENT_WIDTH, pos[1])) != None:  # left
                surroundings[1] = self.grid.get((pos[0]-settings.ENT_WIDTH, pos[1]))
            if i == 2 and self.grid.get((pos[0], pos[1]+settings.ENT_WIDTH)) != None:  # down
                surroundings[2] = self.grid.get((pos[0], pos[1]+settings.ENT_WIDTH))
            if i == 3 and self.grid.get((pos[0]+settings.ENT_WIDTH, pos[1])) != None:  # right
                surroundings[3] = self.grid.get((pos[0]+settings.ENT_WIDTH, pos[1]))
        return surroundings

    def _build_grid(self) -> None:
        for i in range(int(self.width/settings.ENT_WIDTH)):
            for j in range(int(self.height/settings.ENT_WIDTH)+1):
                self.grid[(i*settings.ENT_WIDTH, j*settings.ENT_WIDTH)] = []
