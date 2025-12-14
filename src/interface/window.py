import utils.utils as utils
from static.settings import Settings as settings


class Window:
    def __init__(self, offset_x: int, offset_y: int):
        self.width = settings.WINDOW_WIDTH
        self.height = settings.WINDOW_HEIGHT
        self.offset = (offset_x, offset_y)
    
    def move(self, dir: tuple) -> None:
        if self.offset[0] + dir[0] >= 0 - self.width and self.offset[0] + self.width + dir[0] <= settings.WORLD_SIZE + self.width:
            self.offset = utils.add_twoples(self.offset, (dir[0], 0))
        if self.offset[1] + dir[1] >= 0 - self.height and self.offset[1] + self.height + dir[1] <= settings.WORLD_SIZE + self.height:
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
        if pos[0] >= 0 - self.width and pos[0]+self.width <= settings.WORLD_SIZE + self.width:
            new_x = pos[0]
        elif pos[0]+self.width > settings.WORLD_SIZE + self.width:
            new_x = settings.WORLD_SIZE
        elif pos[0] < 0 - self.width:
            new_x = 0 - self.width

        if pos[1] >= 0 - self.height and pos[1]+self.height <= settings.WORLD_SIZE + self.height:
            new_y = pos[1]
        elif pos[1]+self.height > settings.WORLD_SIZE + self.height:
            new_y = settings.WORLD_SIZE
        elif pos[1] < 0 - self.height:
            new_y = 0

        # correcting new offset tuple to be aligned with entity grid
        corrected = utils.subtract_twoples((new_x, new_y), (new_x % settings.ENT_WIDTH, new_y % settings.ENT_WIDTH))
        self.offset = corrected

# TODO: make zoom centered
    def zoom_in(self, speed: int) -> None:
        # print("in old off: " + str(self.offset))
        off_adj = utils.multiply_twople_by_constant(self.offset, speed)
        # mod = utils.multiply_twople_by_constant((int(self.width/2), int(self.height/2)), speed)
        # off_center = utils.subtract_twoples(off_adj, (int(self.width/2), int(self.height/2)))
        # self.set_offset(utils.add_twoples(off_adj, mod)
        self.set_offset(off_adj)
        # print("in new off: " + str(self.offset))

    def zoom_out(self, speed: int) -> None:
        # print("out old off: " + str(self.offset))
        off_adj = utils.divide_twople_by_constant(self.offset, speed)
        # mod = utils.divide_twople_by_constant((int(self.width/2), int(self.height/2)), speed)
        # off_center = utils.subtract_twoples(off_adj, (int(self.width/2), int(self.height/2)))
        # self.set_offset(utils.subtract_twoples(off_adj, mod))
        self.set_offset(off_adj)
        # print("out new off: " + str(self.offset))
