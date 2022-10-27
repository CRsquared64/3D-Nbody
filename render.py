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

import json

import sim.solarSystem
import sim.earthMoonSystem
import sim.plutoCharonSystem

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
    global vid_id, cycles

    cycles = 10000
    batches = 32
    batch_size = cycles / batches

    load = False
    save_bodies = True

    frame_interval = 24

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

    bodies = sim.plutoCharonSystem.bodies
    vid_id = sim.plutoCharonSystem.video_name

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
                    body.position(bodies)
                    poses[n].append(body.get_draw_pos())
                    pb.update(1)
                    with open('config/nb_run.dat', 'wb') as handle:
                        pickle.dump(poses, handle)

    if load:
        print("Loading Data")
        with open('config/nb_run.dat', 'rb') as handle:
            poses = pickle.load(handle)

    print("Rendering Frames")
    WIN = pygame.display.set_mode((WIDTH, HEIGHT), RESIZABLE)
    with tqdm(total=len(poses[0])) as pb:

        for i in range(len(poses[0])):
            pb.update(1)
            clock.tick(60)
            WIN.fill((5, 5, 5))
            d_count = i_font.render(f"Days: {(i * body.TIMESTEP) // 86400}", True, (
            255, 255, 255))  # amount of iterations, * timestep = seconds. seconds // 86400 == days OR amount of iterations * timestep = timescale per iteration
            h_count = i_font.render(f"Hours: {(i * body.TIMESTEP) // 3600}", True, (255, 255, 255))
            iterations = i_font.render(f"Iterations: {i}", True, (255, 255, 255))
            WIN.blit(d_count, (0, 0))
            WIN.blit(h_count, (0, 25))
            WIN.blit(iterations, (0, 50))

            if i % frame_interval == 0:
                for n, body in enumerate(bodies):
                    x, y = poses[n][i]
                    x = int(x)
                    y = int(y)

                    text = font.render(body.identify, True, body.colour)
                    WIN.blit(text, dest=(x, y))

                    # pygame.draw.circle(WIN, body.colour, (x, y), body.radius)  old method
                    gfxdraw.aacircle(WIN, x, y, body.radius, body.colour)
                    gfxdraw.filled_circle(WIN, x, y, body.radius, body.colour)


                    pygame.image.save(WIN, f'run/nb_frame0{i}.jpg')



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
