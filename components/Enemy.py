import random

class Enemy:
    x = 0
    y = 0,
    speed = 0
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = random.randint(5, 10)