import time
import math

import pygame
from pygame.locals import *
import random
pygame.init()


WIDTH, HEIGHT = 2240,1260
WIN = pygame.display.set_mode((WIDTH, HEIGHT), RESIZABLE)

class Body:
    G = 6.67428e-11
    AU = 149.6e6 * 1000
    TIMESTEP = 360 * 12
    SCALE = 75 / AU

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
                #update.append((x,y))

            #pygame.draw.lines(win, self.colour, False, update, 2)
        pygame.draw.circle(win,self.colour, (x,y), self.radius)





def run_SOL():
    run = True
    clock = pygame.time.Clock()

    SUN = Body(0, 0, 15, 1.98892 * 10 ** 30, (255,165,0))
    SUN2 = Body(2 * Body.AU, 2, 8, 1.98892 * 10 ** 30, (255, 165, 0))
    SUN2.yv = 200.236 * 1000
    EARTH = Body(-1 * Body.AU, 2, 4, 5.9742 * 10**24,(0,0,255))
    EARTH.yv = 29.783 * 1000
    MARS = Body(-1.524 * Body.AU, 0, 3, 6.39 * 10**23, (255,25,0))
    MARS.yv = 24.077 * 1000
    VENUS = Body(0.723 * Body.AU, 0, 3.5, 4.865 * 10**24, (255,255,255))
    VENUS.yv = -35.02 * 1000

    MOON = Body(-1.02 * Body.AU, 2, 2, 1.73477e22, (150,150,150))
    MOON.yv = 2.9783e4

    asteroid = Body(5 * Body.AU, 2, 1, 5 * 10**17, (100,100,100))
    asteroid.yv = 10.40 * 1000

    MERCURY = Body(0.387 * Body.AU, 0, 2, 3.30 * 10**23 ,(150,150,150))
    MERCURY.yv = -47.4 * 1000

    JUPITER = Body(-5.203 * Body.AU, 0, 8, 1.9 *10 ** 27, (125,84,84))
    JUPITER.yv = 13.07 * 1000

    SATURN = Body(-9.5 * Body.AU, 0, 6, 5.683 * 10 ** 26, (255,253,208))
    SATURN.yv = 9.69 * 1000

    bodies = [SUN, MARS, VENUS, MERCURY, EARTH, asteroid, JUPITER, SATURN]
    i = 0
    while run:
        clock.tick(2400)
        WIN.fill((0, 0, 0))
        fps = int(clock.get_fps())



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        for body in bodies:
            body.position(bodies)
            body.plot(WIN)

        pygame.display.update()
    pygame.quit()



def Run_galaxu():
    run = True
    clock = pygame.time.Clock()

    B_HOLE = Body(2 * Body.AU,0, 20, 2*10**30, (0,0,0))


    B_HOLE2 = Body(0, 0, 12, 2 * 10 **30, (9, 0, 0))


    bodies = [B_HOLE2]

    for i in range(5, 15):
        x = (-1 + i * 0.15)
        y = 0

        generated = Body(x * Body.AU, y * Body.AU, 5, 0.01 * 10 ** 24, (200, 200, 255))
        generated.yv = 25  * 1000
        bodies.append(generated)



    while run:
        clock.tick(120)
        WIN.fill((25, 25, 25))


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        for body in bodies:
            body.position(bodies)
            body.plot(WIN)
        pygame.display.update()
    pygame.quit()


run_SOL()