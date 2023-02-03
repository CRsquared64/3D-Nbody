import random
from math import *

import pygame.display


#      x*     y*     z*
#  x =  1      0      0
#  y =  0   cosθ  -sinθ
#  z =  0   sinθ   cosθ
#
def rotateX(x, y, z, roll):
    roll = radians(-roll)  # matrixes are the wrong way round so flip the sign
    vert = (x,
            cos(roll) * y + -sin(roll) * z,
            sin(roll) * y + cos(roll) * z)
    return vert


#         x*  y*    z*
# x =   cosθ   0  sinθ
# y =      0   1     0
# z =  -sinθ   0  cosθ
#
def rotateY(x, y, z, pitch):
    pitch = radians(-pitch)  # matrixes are the wrong way round so flip the sign
    return (cos(pitch) * x + sin(pitch) * z,
            y,
            -sin(pitch) * x + cos(pitch) * z)


#        x*    y* z*
# x =  cosθ -sinθ  0
# y =  sinθ  cosθ  0
# z =     0     0  1
#
def rotateZ(x, y, z, yaw):
    yaw = radians(-yaw)  # matrixes are the wrong way round so flip the sign
    return (cos(yaw) * x + -sin(yaw) * y,
            sin(yaw) * x + cos(yaw) * y,
            z)


def translate(x, y, z, x2, y2, z2):
    return (
        x + x2,
        y + y2,
        z + z2
    )



def bdiv(a, b):
    if b == 0:
        return 0
    return a / b


def project(x, y, z, cx, cy, cz, cro, cpi, cya, width, height, fov):
    # Convert to relative coordinates
    x, y, z = translate(x, y, z, -cx, -cy, -cz)
    x, y, z = rotateX(x, y, z, -cro)
    x, y, z = rotateY(x, y, z, -cpi)
    x, y, z = rotateZ(x, y, z, -cya)

    if x < 0:
        return 0, 0, 0  # Factor of 0

    factor = bdiv(atan(radians(180 - fov) / 2), x)
    y = y * factor * width + height / 2
    z = -z * factor * width + height / 2
    return y, z, factor


def setup(width, height, name):
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption(name)

    return window


def draw_circle(x, y, z, radius, cx, cy, cz, cro, cpi, cya, width, height, fov, surface):
    x, y, z = project(x, y, z, cx, cy, cz, cro, cpi, cya, width, height, fov)
    pygame.draw.circle(surface, (255, 255, 255), (x, y), z*radius)


def draw(positions, cx, cy, cz, cro, cpi, cya, width, height, fov, surface):
    surface.fill((0, 0, 0))
    for x, y, z, radius in positions:
        draw_circle(x, y, z, radius, cx, cy, cz, cro, cpi, cya, width, height, fov, surface)
    pygame.display.update()


def easy_animate(positions_through_time, W, H, name):
    window = setup(W, H, name)

    roll = 0
    pitch = 0
    yaw = 0
    capture = True
    clock = pygame.time.Clock()
    for positions in positions_through_time:
        print(positions)
        draw(positions, 0, 0, 0, roll, pitch, yaw, W, H, 90, window)

        if capture and pygame.mouse.get_focused():
            x, y = pygame.mouse.get_pos()
            pygame.mouse.set_pos(W / 2, H / 2)

            dx = x - W / 2
            dy = y - H / 2

            pitch -= dy
            yaw -= dx
            print(pitch, yaw)

        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    capture = False

        clock.tick(24)


if __name__ == "__main__":  # Testing
    W, H = 500, 500

    # Testing data generation info
    BOUNDING_BOX = 100
    AMOUNT = 1000
    RADIUS_MIN = 900
    RADIUS_MAX = 1000
    SPEED_MIN = 0
    SPEED_MAX = 1

    points = list()
    speeds = list()
    for i in range(AMOUNT):
        points.append([
            random.randint(-BOUNDING_BOX, BOUNDING_BOX),
            random.randint(-BOUNDING_BOX, BOUNDING_BOX),
            random.randint(-BOUNDING_BOX, BOUNDING_BOX),
            random.randint(RADIUS_MIN, RADIUS_MAX),
        ])
        speeds.append([
            random.randint(SPEED_MIN, SPEED_MAX) * (-1 if random.randint(0, 1) else 1),
            random.randint(SPEED_MIN, SPEED_MAX) * (-1 if random.randint(0, 1) else 1),
            random.randint(SPEED_MIN, SPEED_MAX) * (-1 if random.randint(0, 1) else 1),
        ])

    window = setup(W, H, "TestRenderer")

    roll = 0
    pitch = 0
    yaw = 0
    capture = True
    clock = pygame.time.Clock()
    while True:
        draw(points, 0, 0, 0, roll, pitch, yaw, W, H, 90, window)
        for i in range(AMOUNT):
            points[i][0] += speeds[i][0]
            points[i][1] += speeds[i][1]
            points[i][2] += speeds[i][2]

        if capture and pygame.mouse.get_focused():
            x, y = pygame.mouse.get_pos()
            pygame.mouse.set_pos(W / 2, H / 2)

            dx = x - W / 2
            dy = y - H / 2

            pitch -= dy
            yaw -= dx
            print(pitch, yaw)

        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    capture = False

        clock.tick(24)
