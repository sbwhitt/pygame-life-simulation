import time

class Tracker:
    def __init__(self, name: str):
        self.name = name
        self.per_minute = 0

class Metrics:
    def __init__(self):
        self.timestamp = time.time()
        self.time_elapsed = 0
        self.trackers = {}
    
    def get_rate(self, name: str) -> float:
        if self.trackers.get(name):
            return self.trackers[name].per_minute
        return -1
    
    def update(self, name: str, amount: int) -> None:
        self.time_elapsed += time.time() - self.timestamp
        self.timestamp = time.time()
        if self.trackers.get(name):
            self.trackers[name].per_minute = self._calculate_per_minute(amount)
    
    def create_tracker(self, name: str) -> None:
        self.trackers[name] = Tracker(name)

    def _calculate_per_minute(self, amount: int) -> float:
        if self.time_elapsed == 0: return 0
        return amount / (self.time_elapsed/60)
