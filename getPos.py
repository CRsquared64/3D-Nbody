# here jon, will this make you HAPPY?!?!?!?!?
from nbody import Nbody
from pynndescent import NNDescent

import pickle
import sim.solarSystem

import numpy as np
from tqdm import tqdm


def getPos(bodies, cycles):
    batches = 4
    batch_size = cycles / batches
    points = [(body.x, body.y, body.z) for body in bodies]

    points_array = np.array(points)

    nn = NNDescent(points_array)
    vid_id = sim.solarSystem.video_name

    poses = [[] for i in range(len(bodies))]
    amount = len(bodies) * cycles
    n = 0
    print("Calculating Positions")
    with tqdm(total=amount) as pb:
        for i in range(cycles):
            n = n + 1
            for n, body in enumerate(bodies):
                body.position(bodies, nn)
                poses[n].append(body.get_draw_pos())
                pb.update(1)
            if i % batch_size == 0:
                with open('nbodies.pos', 'ab') as handle:
                    pickle.dump(poses, handle)



getPos(sim.solarSystem.bodies, 128)
