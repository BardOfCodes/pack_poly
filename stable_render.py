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
import _pickle as cPickle
H = 5
W = 5

out_dir = lambda x : os.path.join('./outputs/new/stability_out', x)

def compute_stability(distance=2):
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
                if not distance == 0:
                    continue

            diff = polys - other
            if len(diff) == distance: # they are neighbors
                if blocks and other_blocks: # both are stable
                    stability_scores[polys] = stability_scores.get(polys, np.zeros(2)) + np.array([1, 1])
                else:
                    stability_scores[polys] = stability_scores.get(polys, np.zeros(2)) + np.array([0, 1])

                all_neighbors[polys] = all_neighbors.get(polys, []) + [other]

    # compute normalized scores
    for (polys, score) in stability_scores.items():
        stability_scores[polys] = score[0] / score[1]
    
    
    solutions = [stability_scores, all_neighbors, all_solutions]
    cPickle.dump(solutions, open(out_dir(f'stability_scores_{distance}.pkl'), 'wb'))
    
    
if __name__ == '__main__':

    logger = logging.getLogger('stability')
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler('stability.log')
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    start = time.time()
    # stability_exp()
    for i in range(0, 5):
        compute_stability(distance=i)
        
    end = time.time()
    print(f"Total time: {end - start} seconds")
