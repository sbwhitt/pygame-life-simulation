class Map:
    def __init__(self, w, h):
        self.width = w
        self.height = h
        self.grid = {}
        self._build_grid()

    def _build_grid(self):
        for i in range(int(self.width/10)):
            for j in range(int(self.height/10)+1):
                self.grid[(i*10, j*10)] = []
