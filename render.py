import pygame
from pygame.locals import *
from tqdm import tqdm
import nbody

import pickle
import os
import cv2
import glob

import json

import sim.solarSystem
import sim.earthMoonSystem

try:
    os.mkdir('run')
except:
    print('Directory "run" already exists')

save_config = True


WIDTH, HEIGHT = 1920, 1080
FPS = 60

pygame.font.init()
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video = cv2.VideoWriter('video.mp4', fourcc, FPS, (WIDTH, HEIGHT))

font = pygame.font.Font(pygame.font.get_default_font(), 12)


def read_config():
    with open('config/config.json') as json_file:
        data = json.load(json_file)
        for i in data:
            cycles = (['cycles'])
            batches = (['batches'])
            load =  (['load'])
            save_bodies = (['save_bodies'])
        return cycles, batches, load, save_bodies




def render():

    cycles = 100000
    batches = 32
    batch_size = cycles / batches

    load = False
    save_bodies = True

    frame_interval =  60

    print(f"Config \n"
          f"Cycles: {cycles} \n"
          f"batches: {batches} \n"
          f"batch size: {batch_size} \n"
          f"frame_interval: {frame_interval}")
    run = False

    #Convert to json

    data = {"cycles: ": cycles,
            "batches: ": batches,
            "batch_size: ": batch_size,
            "load: ": load,
            "save_bodies: ": save_bodies}
    data = json.dumps(data)


    if save_config:
        with open('config/config.json', 'w',) as json_file:
            json.dump(data, json_file)



    clock = pygame.time.Clock()

    bodies = sim.earthMoonSystem.bodies

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
            clock.tick(240)
            WIN.fill((5, 5, 5))
            for n, body in enumerate(bodies):
                x, y = poses[n][i]

                text = font.render(body.identify, True, body.colour)
                WIN.blit(text, dest=(x, y))
                # pygame.draw.lines(WIN, body.colour, False, body.update, 2)
                pygame.draw.circle(WIN, body.colour, (x, y), body.radius)

            if i % frame_interval == 0:
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
    print("Creating Video From Frames")
    with tqdm(total=img_amount) as pb:
        for img in images:
            video.write(img)
            pb.update(1)

cv2.destroyAllWindows()
video.release()
 