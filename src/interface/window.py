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

    def set_offset(self, pos: tuple) -> None:
        new_x, new_y = self.offset[0], self.offset[1]
        if pos[0] >= 0 and pos[0]+self.width <= settings.WORLD_SIZE:
            new_x = pos[0]
        elif pos[0]+self.width > settings.WORLD_SIZE:
            new_x = settings.WORLD_SIZE-self.width
        elif pos[0] < 0:
            new_x = 0

        if pos[1] >= 0 and pos[1]+self.height <= settings.WORLD_SIZE:
            new_y = pos[1]
        elif pos[1]+self.height > settings.WORLD_SIZE:
            new_y = settings.WORLD_SIZE-self.height
        elif pos[1] < 0:
            new_y = 0

        # correcting new offset tuple to be aligned with entity grid
        corrected = utils.subtract_twoples((new_x, new_y), (new_x % settings.ENT_WIDTH, new_y % settings.ENT_WIDTH))
        self.offset = corrected
