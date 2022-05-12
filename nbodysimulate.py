import math
import matplotlib
from astropy import constants as const


class Body:
    G = const.G
    AU = const.AU

    def __init__(self, x, y, radius, mass, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.mass = mass
        self.color = color

        self.trail = []

        self.xv = 0
        self.xy = 0
