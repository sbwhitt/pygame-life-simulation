class Map:
    def __init__(self, w, h):
        self.width = w
        self.height = h
        self.grid = {}
        self._build_grid()

    def get_surroundings(self, pos):
        surroundings = [None, None, None, None]
        for i in range(0, 4):
            if i == 0 and self.grid.get((pos[0], pos[1]-10)) != None: #up
                surroundings[0] = (self.grid.get((pos[0], pos[1]-10)))
            if i == 1 and self.grid.get((pos[0]-10, pos[1])) != None: #left
                surroundings[1] = (self.grid.get((pos[0]-10, pos[1])))
            if i == 2 and self.grid.get((pos[0], pos[1]+10)) != None: #down
                surroundings[2] = (self.grid.get((pos[0], pos[1]+10)))
            if i == 3 and self.grid.get((pos[0]+10, pos[1])) != None: #right
                surroundings[3] = (self.grid.get((pos[0]+10, pos[1])))
        return surroundings

    def _build_grid(self):
        for i in range(int(self.width/10)):
            for j in range(int(self.height/10)+1):
                self.grid[(i*10, j*10)] = []
