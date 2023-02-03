# here jon, will this make you HAPPY?!?!?!?!?

import pickle

from tqdm import tqdm

import sim.solarSystem


def get_pos(bodies, cycles):
    batches = 1
    nn = False
    vid_id = sim.solarSystem.video_name

    poses = [[] for i in range(len(bodies))]
    amount = len(bodies) * cycles
    print("Calculating Positions")
    with tqdm(total=amount) as pb:
        for i in range(cycles):
            for n, body in enumerate(bodies):
                body.position(bodies, nn)
                poses[n].append((*body.get_draw_pos(), body.radius))

                pb.update(1)
    with open('nbodies.pos', 'wb') as handle:
        pickle.dump(poses, handle)
    return poses

get_pos(sim.solarSystem.bodies, 500)