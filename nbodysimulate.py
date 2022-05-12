import math
import matplotlib
from astropy import constants as const


class Body:
    G = const.G
    AU = const.AU
    TIMESTEP = 3600 * 24

    def __init__(self, x, y, radius, mass, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.mass = mass
        self.color = color

        self.trail = []

        self.xv = 0
        self.xy = 0

    def force(self, obj):
        obj_x = obj.x
        obj_y = obj.y
        obj_dist_x = obj_x - self.x
        obj_dist_y = obj_y - self.y

        dist = math.sqrt(obj_dist_x ** 2 + obj_dist_y ** 2)
        force = self.G * self.mass * obj.mass / dist ** 2

        angle = math.atan2(obj_dist_y, obj_dist_x)

        force_x = math.cos(angle) * force
        force_y = math.sin(angle) * force

        return force_x, force_y

    def position(self, bodies):
        total_force_x = total_force_y = 0

        for body in bodies:
            if self == body:
                continue

            force_x, force_y = self.force(body)
bodies = [1,2,3]