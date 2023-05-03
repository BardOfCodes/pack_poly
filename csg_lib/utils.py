import numpy as np
import torch as th


def get_points(res):
    points = np.stack(np.meshgrid(
        range(res), range(res), indexing="ij"), axis=-1)
    points = points.astype(np.float32)
    points = ((points + 0.5) / res - 0.5) * 2
    points = th.from_numpy(points).float()
    points = th.reshape(points, (-1, 2))
    return points
