import numpy as np
import pygame

from pygame.locals import *
from pygame import gfxdraw
from tqdm import tqdm
import nbody

import pickle
import os
import cv2
import glob
import shutil
print("Hello Jon!")
import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

try:
    os.mkdir('run')
except:
    print('Emptying old cache...')
    shutil.rmtree('run')
    os.mkdir('run')

WIDTH, HEIGHT = 1920, 1080
FPS = 60

pygame.font.init()

font = pygame.font.Font(pygame.font.get_default_font(), 12)
i_font = pygame.font.Font(pygame.font.get_default_font(), 24)



def setup():
    pygame.init()
    WIN = pygame.display.set_mode((WIDTH, HEIGHT), OPENGL)
    pygame.display.set_caption("N-Body Simulation")

    glutInit()

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, WIDTH / HEIGHT, 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)

    clock = pygame.time.Clock()


def render():
    pass



