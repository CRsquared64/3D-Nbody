import time
import math
import pygame

pygame.init()

WIDTH, HEIGHT = 800,800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

class Body:
    G = 6.67428e-11
    AU = 149.6e6 * 1000
    TIMESTEP = 36000 * 24
    SCALE = 250 / AU

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

            self.xv = total_force_x / self.mass * self.TIMESTEP
            self.yv = total_force_y / self.mass * self.TIMESTEP

            self.x += self.xv * self.TIMESTEP
            self.y += self.yv * self.TIMESTEP

            self.trail.append((self.x, self.y))

    def plot(self, win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2
        pygame.draw.circle(win,self.colour, (x,y), self.radius)







def run():
    run = True
    clock = pygame.time.Clock()
    WIN.fill((0,0,0))

    BODY_1 = Body(0, 0, 30, 1.98892 * 10 ** 30, (255,0,0))
    BODY_2 = Body(-1 * Body.AU, 0, 16, 5.9742 * 10 ** 24,(0,0,255))
    BODY_2.y.
    bodies = [BODY_1, BODY_2]
    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        for body in bodies:
            body.position(bodies)
            body.plot(WIN)
        pygame.display.update()
    pygame.quit()





run()
