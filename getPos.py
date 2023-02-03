# here jon, will this make you HAPPY?!?!?!?!?

import pickle
import sim.solarSystem

from tqdm import tqdm


def get_pos(bodies, cycles):
    batches = 1
    batch_size = cycles // batches
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
            if i % batch_size == 0:
                # print(f"Great Sucess {i}")
                with open('nbodies.pos', 'ab') as handle:
                    pickle.dump(poses, handle)
                    poses = [[] for i in range(len(bodies))]
    return poses

