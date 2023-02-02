import numpy as np
import pygame

from pygame.locals import *
from pygame import gfxdraw
from pynndescent import NNDescent

from tqdm import tqdm
import nbody

import pickle
import os
import cv2
import glob
import shutil

import json

import sim.solarSystem
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

save_config = True

WIDTH, HEIGHT = 1920, 1080
FPS = 60

pygame.font.init()

font = pygame.font.Font(pygame.font.get_default_font(), 12)
i_font = pygame.font.Font(pygame.font.get_default_font(), 24)


def read_config():
    with open('config/config.json') as json_file:
        data = json.load(json_file)
        for i in data:
            cycles = (['cycles'])
            batches = (['batches'])
            load = (['load'])
            save_bodies = (['save_bodies'])
        return cycles, batches, load, save_bodies


vid_id = ""
cycles = ""


def render():
    pygame.init()
    WIN = pygame.display.set_mode((WIDTH, HEIGHT), OPENGL)
    pygame.display.set_caption("N-Body Simulation")

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, WIDTH / HEIGHT, 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)

    global vid_id, cycles

    cycles = 150
    batches = 32
    batch_size = cycles / batches

    load = False
    save_bodies = True

    frame_interval = 1

    print(f"Config \n"
          f"Cycles: {cycles} \n"
          f"Timestep: {nbody.Nbody.TIMESTEP} \n"
          f"batches: {batches} \n"
          f"batch size: {batch_size} \n"
          f"frame_interval: {frame_interval}")
    run = False

    # Convert to json

    data = {"cycles: ": cycles,
            "batches: ": batches,
            "batch_size: ": batch_size,
            "load: ": load,
            "save_bodies: ": save_bodies}
    data = json.dumps(data)

    if save_config:
        with open('config/config.json', 'w', ) as json_file:
            json.dump(data, json_file)

    clock = pygame.time.Clock()

    bodies = sim.solarSystem.bodies

    points = [(body.x, body.y, body.z) for body in bodies]

    points_array = np.array(points)

    nn = NNDescent(points_array)
    vid_id = sim.solarSystem.video_name

    if save_bodies:
        with open('config/bodies.json', 'wb') as handle:
            pickle.dump(bodies, handle)

    poses = [[] for i in range(len(bodies))]
    amount = len(bodies) * cycles

    if not load:
        n = 0
        print("Calculating Positions")
        with tqdm(total=amount) as pb:
            for i in range(cycles):
                n = n + 1
                for n, body in enumerate(bodies):
                    body.position(bodies, nn)
                    poses[n].append(body.get_draw_pos())
                    pb.update(1)
                    with open('config/nb_run.dat', 'wb') as handle:
                        pickle.dump(poses, handle)

    if load:
        print("Loading Data")
        with open('config/nb_run.dat', 'rb') as handle:
            poses = pickle.load(handle)

    print("Rendering Frames")

    trails = []
    for n in range(len(bodies)):
        trails.append([])
    frame_counter = 0

    with tqdm(total=len(poses[0])) as pb:
        for i in range(len(poses[0])):
            glClear(GL_COLOR_BUFFER_BIT)

            center_x, center_y, center_z = bodies[0].get_draw_pos()

            eye_x, eye_y, eye_z = center_x, center_y, center_z + 10
            up_x, up_y, up_z = 0, 1, 0

            gluLookAt(eye_x, eye_y, eye_z, center_x, center_y, center_z, up_x, up_y, up_z)

            for n, body in enumerate(bodies):

                # Draw the trail
                glBegin(GL_LINE_STRIP)
                for x, y, z in body.update:
                    glColor3f(body.colour[0], body.colour[1], body.colour[2])
                    glVertex3f(x, y, z)
                glEnd()

                modelview_matrix = glGetDoublev(GL_MODELVIEW_MATRIX)
                projection_matrix = glGetDoublev(GL_PROJECTION_MATRIX)

                viewport = glGetIntegerv(GL_VIEWPORT)

                win_x, win_y, win_z = gluProject(body.x, body.y, body.z, modelview_matrix, projection_matrix, viewport)

                if win_x >= 0 and win_x <= WIDTH and win_y >= 0 and win_y <= HEIGHT:
                    # sphere no on screen
                    print("On Screen")
                    glPushMatrix()
                    glTranslatef(body.x, body.y, body.z)
                    quadric = gluNewQuadric()
                    glColor3f(body.colour[0], body.colour[1], body.colour[2])
                    gluSphere(quadric, body.radius, 20, 20)
                    glPopMatrix()
                else:
                    print(
                        f"modelview_matrix: {modelview_matrix}, projection_matrix: {projection_matrix}, win_x/y/z: {win_x, win_y, win_z}")

                    continue

            # Update the screen to show the drawn spheres and trails
            pygame.display.flip()

            pb.update(1)

            pygame.image.save(WIN, f'run/solar_system{frame_counter}.jpg')
            frame_counter += 1

    # pygame.display.update()
    print("Render Done!")
    pygame.quit()


if __name__ == '__main__':
    render()
    print("Reading Frames")
    filenames = sorted(glob.glob("run/*.jpg"), key=os.path.getmtime)

    images = [cv2.imread(img) for img in filenames]
    img_amount = len(images)

    video_name = f"{vid_id}_{cycles}_{nbody.Nbody.TIMESTEP}.mp4"
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(video_name, fourcc, FPS, (WIDTH, HEIGHT))

    print("Creating Video From Frames")
    with tqdm(total=img_amount) as pb:
        for img in images:
            video.write(img)
            pb.update(1)

cv2.destroyAllWindows()
video.release()
