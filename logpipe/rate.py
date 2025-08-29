"""count events per second, useful for monitoring log throughput"""

import time

class RateCounter:
    def __init__(self, window=10):
        self.window = window
        self.timestamps = []

    def tick(self):
        now = time.monotonic()
        self.timestamps.append(now)
        # trim old
        cutoff = now - self.window
        self.timestamps = [t for t in self.timestamps if t > cutoff]

    def rate(self):
        if len(self.timestamps) < 2:
            return 0.0
        span = self.timestamps[-1] - self.timestamps[0]
        if span <= 0:
            return 0.0
        return (len(self.timestamps) - 1) / span
