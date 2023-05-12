# First save the files
# load and render.
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
from pathlib import Path
import matplotlib.pyplot as plt
from viz.visualize_v2 import create_texture_files, draw_packing_with_texture, draw_polyomino_set, create_gif_mix

location = "./outputs/stability_vis"
path = Path(location)
path.mkdir(parents=True, exist_ok=True)
out_dir = lambda x : os.path.join(location, x)


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
    

def draw_images_for_best(solution_file, texture_files, save_location):
    # Draw GIF Simple:
    stability_scores, all_neighbors, all_solutions = cPickle.load(open(solution_file, "rb"))

    sorted_scores = sorted(stability_scores.items(), key=lambda x: x[1], reverse=True)

    polys = sorted_scores[0][0]

    H = 7
    W = 6
    blocks, locations, rotations = all_solutions[polys]
    rotated_blocks = P.apply_rotations(blocks, rotations)

    fig = draw_packing_with_texture(rotated_blocks, locations, H, W, texture_files)
    fig.show()
    plt.axis('off')
    fig.patch.set_facecolor('lightsteelblue')
    fig.savefig(os.path.join(save_location, f'/packing_0.png'), bbox_inches='tight', pad_inches=0)
    plt.close()

    fig = draw_polyomino_set(blocks, 2, 4, texture_files)
    fig.show()
    plt.axis('off')
    fig.patch.set_facecolor('lightsteelblue')
    fig.savefig(os.path.join(save_location, f'polys_0.png'), bbox_inches='tight', pad_inches=0)
    plt.close()


    for ind, neighbor in enumerate(all_neighbors[polys]):
        blocks, locations, rotations = all_solutions[neighbor]
        if blocks:
            rotated_blocks = P.apply_rotations(blocks, rotations)

            fig = draw_packing_with_texture(rotated_blocks, locations, H, W, texture_files)
            fig.show()
            plt.axis('off')
            fig.patch.set_facecolor('lightsteelblue')
            fig.savefig(os.path.join(save_location, f'packing_{ind+1}.png'), bbox_inches='tight', pad_inches=0)
            plt.close()
            
            fig = draw_polyomino_set(blocks, 2, 4, texture_files)
            fig.show()
            plt.axis('off')
            fig.patch.set_facecolor('lightsteelblue')
            fig.savefig(os.path.join(save_location, f'polys_{ind+1}.png'), bbox_inches='tight', pad_inches=0)
            plt.close()
        
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
    
    # Now render all the configuration for the best:
    # create textures if needed.
    texture_files = [os.path.join(location, f"tmp_{x}.png") for x in range(20) ]
    for path in texture_files:
        if not os.path.exists(path):
            texture_files = create_texture_files(k=20, location=location)
            break
    
    noise_factor = 1
    save_location = "../outputs/gif_stability"
    solution_file = out_dir(f"stability_scores_{noise_factor}.pkl")
    
    draw_images_for_best(solution_file, texture_files, save_location)
    
    output_path = os.path.join(save_location, 'output_2.gif')
    frame_rate = 1000  # in milliseconds

    create_gif_mix(save_location, output_path, 'polys_', 'packing_', frame_rate)
    
    # output_path = '../outputs/gif_stability_2/output_3.gif'
    # create_gif(folder_path, output_path, 'packing_', frame_rate)