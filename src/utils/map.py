import src.utils.utils as utils
from static.settings import Settings as settings
from src.entities.entity import Entity


class Map:
    def __init__(self):
        self.grid = self._build_grid()

    def get_surroundings(self, pos: tuple) -> list[Entity]:
        surroundings = [None, None, None, None]
        for i in range(0, len(surroundings)):
            tile = self.grid.get(utils.add_twoples(pos, settings.DIRS[i]))
            if tile and len(tile) > 0:
                surroundings[i] = tile[0]
        return surroundings

    def rebuild_map_in(self, speed: int) -> None:
        self._resize_settings_up(speed)
        self.grid = self._build_grid()

    def rebuild_map_out(self, speed: int) -> None:
        self._resize_settings_down(speed)
        self.grid = self._build_grid()

    def _build_grid(self) -> dict:
        g = {}
        for i in range(int(settings.WORLD_SIZE/settings.ENT_WIDTH)):
            for j in range(int(settings.WORLD_SIZE/settings.ENT_WIDTH)+1):
                g[(i*settings.ENT_WIDTH, j*settings.ENT_WIDTH)] = []
        return g

    def _resize_settings_up(self, speed: int) -> None:
        settings.ENT_WIDTH = settings.ENT_WIDTH * speed
        settings.WORLD_SIZE = settings.WORLD_SIZE * speed
        settings.DIRS = [(0, -settings.ENT_WIDTH), (-settings.ENT_WIDTH, 0),
            (0, settings.ENT_WIDTH), (settings.ENT_WIDTH, 0),
            (-settings.ENT_WIDTH, -settings.ENT_WIDTH), (-settings.ENT_WIDTH, settings.ENT_WIDTH),
            (settings.ENT_WIDTH, settings.ENT_WIDTH), (settings.ENT_WIDTH, -settings.ENT_WIDTH)]

    def _resize_settings_down(self, speed: int) -> None:
        settings.ENT_WIDTH = int(settings.ENT_WIDTH / speed)
        settings.WORLD_SIZE = int(settings.WORLD_SIZE / speed)
        settings.DIRS = [(0, -settings.ENT_WIDTH), (-settings.ENT_WIDTH, 0),
            (0, settings.ENT_WIDTH), (settings.ENT_WIDTH, 0),
            (-settings.ENT_WIDTH, -settings.ENT_WIDTH), (-settings.ENT_WIDTH, settings.ENT_WIDTH),
            (settings.ENT_WIDTH, settings.ENT_WIDTH), (settings.ENT_WIDTH, -settings.ENT_WIDTH)]
