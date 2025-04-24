# utils/timer.py
import time

class Timer:
    def __init__(self):
        self.reset()

    def reset(self):
        self.start = time.time()

    def elapsed(self):
        return time.time() - self.start

    def has_elapsed(self, seconds):
        return self.elapsed() >= seconds

def ms_to_frames(milliseconds, fps=60):
    return int((milliseconds / 1000) * fps)

def now_ms():
    return int(time.time() * 1000)