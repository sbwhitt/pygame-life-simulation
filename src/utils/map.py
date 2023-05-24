import src.utils.utils as utils
import static.settings as settings
from src.entities.entity import Entity


class Map:
    def __init__(self, w, h):
        self.width = w
        self.height = h
        self.grid = {}
        self.dirs = [(0, -settings.ENT_WIDTH),
                       (-settings.ENT_WIDTH, 0),
                       (0, settings.ENT_WIDTH),
                       (settings.ENT_WIDTH, 0)]
        self._build_grid()

    def get_surroundings(self, pos: tuple) -> list[Entity]:
        surroundings = [None, None, None, None]
        for i in range(0, len(surroundings)):
            tile = self.grid.get(utils.add_twoples(pos, self.dirs[i]))
            if tile and len(tile) > 0:
                surroundings[i] = tile[0]
        return surroundings

    def _build_grid(self) -> None:
        for i in range(int(self.width/settings.ENT_WIDTH)):
            for j in range(int(self.height/settings.ENT_WIDTH)+1):
                self.grid[(i*settings.ENT_WIDTH, j*settings.ENT_WIDTH)] = []
