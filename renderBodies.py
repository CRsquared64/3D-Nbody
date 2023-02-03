import math

import pygame
import glm


def window(Width, Height, Name):
    global persp
    pygame.init()
    WIN = pygame.display.set_mode((Width, Height))
    pygame.display.set_caption(Name)
    pygame.font.init()

    font = pygame.font.Font(pygame.font.get_default_font(), 12)
    i_font = pygame.font.Font(pygame.font.get_default_font(), 24)

    persp = glm.perspective(math.radians(90), Width / Height, 0, 1000)




def render_frame(pos, surface, cam_x, cam_y, cam_z, pitch, yaw, roll):
    trans = glm.translate(glm.mat4(1), glm.vec3(-cam_x, -cam_y, -cam_z))
    trans = trans * persp
    trans.



def render_video(filelist):
    pass
