import packing.packing as P
import viz.visualize as viz
import packing.tetriminoes as tet
import numpy as np
import time
import logging
import threading
import argparse
import pickle
import os
import torch
from multiset import FrozenMultiset
from tqdm import tqdm
from packing.polymino import poly_generator
from itertools import combinations_with_replacement
from torchvision.utils import make_grid, save_image

H = 5
W = 5

out_dir = lambda x : os.path.join('./stability_out', x)

def compute_stability(args):
    pkl_files = [f for f in os.listdir(out_dir('')) if 'solutions_' in f]
    print(pkl_files)
    all_solutions = {}
    for f in pkl_files:
        with open(out_dir(f), 'rb') as f:
            solutions = pickle.load(f)
            all_solutions = {**all_solutions, **solutions} # merge dictionaries

    print(len(all_solutions))

    # for each solution, compute stability score
    stability_scores = {}
    all_neighbors = {}
    for (polys, (blocks, _, _)) in all_solutions.items():
        for (other, (other_blocks, _, _)) in all_solutions.items():
            if polys == other:
                continue

            diff = polys - other
            if len(diff) == 1: # they are neighbors
                if blocks and other_blocks: # both are stable
                    stability_scores[polys] = stability_scores.get(polys, np.zeros(2)) + np.array([1, 1])
                else:
                    stability_scores[polys] = stability_scores.get(polys, np.zeros(2)) + np.array([0, 1])

                all_neighbors[polys] = all_neighbors.get(polys, []) + [other]

    # compute normalized scores
    for (polys, score) in stability_scores.items():
        stability_scores[polys] = score[0] / score[1]
    
    sorted_scores = sorted(stability_scores.items(), key=lambda x: x[1], reverse=True)
    for i in range(3): # most stable
        polys = sorted_scores[i][0]
        viz.draw_polymino_set(polys, filename=f'most_stable_{i}.png')
        blocks, locations, rotations = all_solutions[polys]
        rotated_blocks = P.apply_rotations(blocks, rotations)
        viz.draw_packing(rotated_blocks, locations, W, H, filename=f'most_stable_{i}_packing')

        imgs = []
        for neighbor in all_neighbors[polys]:
            blocks, locations, rotations = all_solutions[neighbor]
            if blocks:
                rotated_blocks = P.apply_rotations(blocks, rotations)
                imgs += [viz.draw_packing(rotated_blocks, locations, W, H)]
        
        imgs = torch.stack(imgs) / 255.0
        imgs = make_grid(imgs, nrow=1)
        print(imgs.shape)
        print(imgs.max())
        save_image(imgs, out_dir(f'most_stable_{i}_neighbors.png'))

        print(sorted_scores[i])

    for i in range(3): # least stable
        print(sorted_scores[-i-1])

    return

def pack_all_combinations(args):
    board = np.zeros((H, W)).astype(bool).tolist()
    all_polyominoes = poly_generator(N=4, workers=1)
    comb = list(combinations_with_replacement(all_polyominoes, 6))
    print(f"Total number of combinations: {len(comb)}")

    solutions = {}
    for i in tqdm(range(args.thread_id, len(comb), args.nthreads)):
        polys = list(comb[i])
        blocks, locations, rotations = P.solve_polyomino_packing(polys, board)
        hashable_poly = FrozenMultiset(frozenset(x) for x in polys)
        solutions[hashable_poly] = (blocks, locations, rotations)
    
    with open(out_dir(f"solutions_{args.thread_id}.pkl"), 'wb') as f:
        pickle.dump(solutions, f)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--stage', type=str, default=None)
    parser.add_argument('--nthreads', type=int, default=1)
    parser.add_argument('--thread_id', type=int, default=0)
    args = parser.parse_args()
    # create a logger:

    logger = logging.getLogger('stability')
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler('stability.log')
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    start = time.time()
    # stability_exp()
    if args.stage == 'preproc':
        pack_all_combinations(args)
    else:
        compute_stability(args)
    end = time.time()
    print(f"Total time: {end - start} seconds")
