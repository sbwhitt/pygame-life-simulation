import time


class Tracker:
    def __init__(self, name: str):
        self.name = name
        self.per_minute = 0


class Metrics:
    def __init__(self, elapsed: int=None):
        self.timestamp = time.time()
        self.time_elapsed = elapsed if elapsed else 0
        self.trackers = {}

    def get_rate(self, name: str) -> float:
        if self.trackers.get(name):
            return self.trackers[name].per_minute
        return -1

    def get_time_elapsed(self) -> str:
        if self.time_elapsed == 0:
            return "00:00:00"
        t = self.time_elapsed
        hours = int(t/3600)
        t -= int(hours*3600)
        minutes = int(t/60)
        t -= int(minutes*60)
        return str(hours) + "h:" + str(minutes) + "m:" + str(int(t)) + "s"

    def update(self, name: str, amount: int, paused: bool) -> None:
        if not paused:
            self.time_elapsed += time.time() - self.timestamp
        self.timestamp = time.time()
        if self.trackers.get(name):
            self.trackers[name].per_minute = self._calculate_per_minute(amount)

    def create_tracker(self, name: str) -> None:
        self.trackers[name] = Tracker(name)

    def _calculate_per_minute(self, amount: int) -> float:
        if self.time_elapsed == 0:
            return 0
        return amount / (self.time_elapsed/60)
