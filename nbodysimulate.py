import time
import math
import pygame
import random
pygame.init()

WIDTH, HEIGHT = 800,800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

class Body:
    G = 6.67428e-11
    AU = 149.6e6 * 1000
    TIMESTEP = 3600 * 24
    SCALE = 125 / AU

    def __init__(self, x, y, radius, mass, colour):
        self.x = x
        self.y = y
        self.radius = radius
        self.mass = mass
        self.colour = colour

        self.trail = []

        self.xv = 0
        self.yv = 0

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
            total_force_x += force_x
            total_force_y += force_y

            self.xv += total_force_x / self.mass * self.TIMESTEP
            self.yv += total_force_y / self.mass * self.TIMESTEP

            self.x += self.xv * self.TIMESTEP
            self.y += self.yv * self.TIMESTEP

            self.trail.append((self.x, self.y))

    def plot(self, win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        if len(self.trail) > 2:
            update = []
            for point in self.trail:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                update.append((x,y))

            pygame.draw.lines(win, self.colour, False, update, 2)
        pygame.draw.circle(win,self.colour, (x,y), self.radius)







def run():
    run = True
    clock = pygame.time.Clock()
    WIN.fill((0,0,0))

    SUN = Body(0, 0, 15, 1.98892 * 10 ** 30, (255,165,0))
    EARTH = Body(-1 * Body.AU, 0, 4, 5.9742 * 10**24,(0,0,255))
    EARTH.yv = 29.783 * 1000
    MARS = Body(-1.524 * Body.AU, 0, 3, 6.39 * 10 ** 23, (255,255,0))
    MARS.yv = 24.077 * 1000
    MOON = Body(-1.01 * Body.AU, -1, 4, 7.34767309 * 5 ** 22, (50,50,50))
    MOON.yv = 29.783 * 1000

    #B_hole = Body(0,0, 30, 1.98892e+36, (0,0,0))
    bodies = [EARTH, SUN]
    while run:
        clock.tick(60)
        WIN.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        for body in bodies:
            body.position(bodies)
            body.plot(WIN)
        pygame.display.update()
    pygame.quit()





run()
