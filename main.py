import sys
import os
import pygame
import shutil

import getPos
import renderBodies
import fileHandler

import sim.solarSystem
import sim.earthMoonSystem
import sim.plutoCharonSystem

try:
    os.mkdir('run')
except OSError as error:
    print('Emptying old cache...')
    shutil.rmtree('run')
    os.mkdir('run')

WIDTH, HEIGHT = 1920, 1080
FPS = 60

pygame.font.init()

font = pygame.font.Font(pygame.font.get_default_font(), 12)
i_font = pygame.font.Font(pygame.font.get_default_font(), 24)

CYCLES = 1024
BODIES = sim.solarSystem.bodies

VID_ID = sim.solarSystem.video_name

load = True
file = sys.argv

if __name__ == '__main__':
    if not load:
        poses = getPos.getPos(BODIES, CYCLES)
    else:
        poses = fileHandler.fileLoad(file)
