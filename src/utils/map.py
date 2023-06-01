import src.utils.utils as utils
import static.settings as settings
from src.entities.entity import Entity


class Map:
    def __init__(self, w, h):
        self.width = w
        self.height = h
        self.grid = self._build_grid()

    def get_surroundings(self, pos: tuple) -> list[Entity]:
        surroundings = [None, None, None, None]
        for i in range(0, len(surroundings)):
            tile = self.grid.get(utils.add_twoples(pos, settings.DIRS[i]))
            if tile and len(tile) > 0:
                surroundings[i] = tile[0]
        return surroundings

    def rebuild_map_in(self) -> None:
        if settings.ENT_WIDTH*2 <= 40:
            settings.ENT_WIDTH = settings.ENT_WIDTH*2
            settings.WORLD_SIZE = settings.WORLD_SIZE*2
            self.grid = self._build_grid()

    def rebuild_map_out(self) -> None:
        if settings.ENT_WIDTH/2 >= 5:
            settings.ENT_WIDTH = settings.ENT_WIDTH/2
            settings.WORLD_SIZE = settings.WORLD_SIZE/2
            self.grid = self._build_grid()

    def _build_grid(self) -> dict:
        g = {}
        for i in range(int(self.width/settings.ENT_WIDTH)):
            for j in range(int(self.height/settings.ENT_WIDTH)+1):
                g[(i*settings.ENT_WIDTH, j*settings.ENT_WIDTH)] = []
        return g
