import src.utils.utils as utils
import static.settings as settings


class Window:
    def __init__(self, offset_x: int, offset_y: int):
        self.width = settings.WINDOW_WIDTH
        self.height = settings.WINDOW_HEIGHT
        self.offset = (offset_x, offset_y)
    
    def move(self, dir: tuple) -> None:
        if self.offset[0] + dir[0] >= 0 and self.offset[0] + self.width + dir[0] <= settings.WORLD_SIZE:
            self.offset = utils.add_twoples(self.offset, (dir[0], 0))
        if self.offset[1] + dir[1] >= 0 and self.offset[1] + self.height + dir[1] <= settings.WORLD_SIZE:
            self.offset = utils.add_twoples(self.offset, (0, dir[1]))
    
    def contains(self, point: tuple) -> bool:
        return (point[0] >= self.offset[0] and 
            point[0] < self.width + self.offset[0] and 
            point[1] >= self.offset[1] and 
            point[1] < self.height + self.offset[1])
    
    def under_stats(self, point: tuple) -> bool:
        return (point[0] >= self.offset[0] + self.width and 
            point[0] < self.width + self.offset[0] and 
            point[1] >= self.offset[1] and 
            point[1] < self.height + self.offset[1])
