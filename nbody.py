import math

WIDTH, HEIGHT = 1920, 1080


class Nbody:
    G = 6.67428e-11
    AU = 149.6e6 * 1000
    distance_to_moon = 3.84399 * 10 ** 8
    PLUTO_TO_CHARON = 19640 * 1000
    TIMESTEP = 3600 * 24 * 365 * 10# seconds
    SCALE = 1 * 10 ** -8 / AU  # 75 / AU or 500 / distance-tomoon

    def __init__(self, x, y, z, radius, mass, colour, identify):
        self.x = x
        self.y = y
        self.z = z
        self.identify = identify
        self.radius = radius
        self.mass = mass
        self.colour = colour

        self.trail = []

        self.xv = 0
        self.yv = 0
        self.zv = 0

    def force(self, obj):
        obj_x = obj.x
        obj_y = obj.y
        obj_z = obj.z
        obj_dist_x = obj_x - self.x
        obj_dist_y = obj_y - self.y
        obj_dist_z = obj_z - self.z

        dist = math.sqrt(obj_dist_x ** 2 + obj_dist_y ** 2 + obj_dist_z ** 2)
        force = self.G * self.mass * obj.mass / dist ** 2

        angle = math.atan2(obj_dist_y, obj_dist_x)

        force_x = math.cos(angle) * force
        force_y = math.sin(angle) * force
        force_z = self.G * self.mass * obj.mass * obj_dist_z

        return force_x, force_y, force_z

    def position(self, bodies):
        total_force_x = 0
        total_force_y = 0

        for body in bodies:
            if self == body:
                continue

            force_x, force_y = self.force(body)
            total_force_x += force_x
            total_force_y += force_y

            self.xv += total_force_x / self.mass * self.TIMESTEP
            self.yv += total_force_y / self.mass * self.TIMESTEP

            self.x += self.xv * self.TIMESTEP
            self.y += self.yv * self.TIMESTEP

            self.trail.append((self.x, self.y))



    def get_draw_pos(self):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2
        self.update = []
        if len(self.trail) > 2:
            for point in self.trail:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                self.update.append((x, y))
        return x, y
