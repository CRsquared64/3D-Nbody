import sys
import os
import pygame
import shutil

import getPos
import renderBodies
import fileHandler

import sim.solarSystem

# import sim.earthMoonSystem
# import sim.plutoCharonSystem

try:
    os.mkdir('run')
except OSError as error:
    print('Emptying old cache...')
    shutil.rmtree('run')
    os.mkdir('run')

WIDTH, HEIGHT = 1920, 1080
FPS = 60

CYCLES = 1024
BODIES = sim.solarSystem.bodies

VID_ID = sim.solarSystem.video_name

load = True
file = str(sys.argv[1])

if __name__ == '__main__':
    if not load:
        print(f"Generating {len(BODIES)} bodies, for {CYCLES} cycles.")
        poses = getPos.get_pos(BODIES, CYCLES)
        print("Generation Finished")
    else:
        poses = fileHandler.file_load(file)
        print(f"Loaded positions from {file}")

        print(poses)
