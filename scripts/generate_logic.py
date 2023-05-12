import packing.packing as P
import viz.visualize as viz
import packing.tetriminoes as tet
import numpy as np
import time
from packing.polymino import Polyomino
import matplotlib.pyplot as plt
from generator.map_solve import generate_puzzle
from packing.polymino import poly_generator
from itertools import combinations_with_replacement
from multiset import FrozenMultiset
import _pickle as cPickle
import argparse
import random
import os
from viz.visualize_v2 import create_texture_files, draw_packing_with_texture

board_dict = {
    0: [
        [1, 0, 0, 0, 0, 0, 1],
        [0, 0, 1, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 0, 0],
        [1, 0, 0, 0, 0, 0, 1],
    ],
    1: [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0],
        [0, 0, 1, 1, 1, 0, 0],
        [0, 0, 1, 1, 1, 0, 0],
        [0, 0, 0, 1, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 1],
    ],
    2: [
        [0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 1, 1, 0, 0],
        [0, 0, 1, 0, 0, 0, 0],
        [0, 0, 1, 0, 1, 0, 0],
        [0, 0, 0, 1, 1, 0, 0],
        [1, 0, 0, 0, 0, 0, 1],
    ],
    3: [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 0, 0],
        [0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0],
        [0, 0, 1, 1, 1, 0, 0],
        [1, 0, 0, 0, 0, 0, 1],
    ],
    4: [
        [1, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 1, 1, 0, 0],
        [0, 0, 1, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 0, 0],
        [1, 0, 0, 0, 0, 0, 1],
    ],
}


def solve(solve_id, location):
    board = board_dict[solve_id]
    board = (np.array(board) == 1).tolist()
    all_polyominoes = poly_generator(N=4)
    comb = list(combinations_with_replacement(all_polyominoes, 8))
    random.shuffle(comb)
    for ind, starting_polys in enumerate(comb):
        print("trying " + str(solve_id))
        print("Combination " + str(ind) + " out of " + str(len(comb)))
        starting_polys = list(starting_polys)
        blocks, locations, rotations = P.solve_polyomino_packing(
            starting_polys, board)

        if blocks is not None:
            print("Found a working solution!" + str(solve_id))
            solution = (blocks, locations, rotations)
            cPickle.dump(solution, open(
                os.path.join(location, f"logic_solution_{solve_id}.pkl"), "wb"))
            break
    
    # Special CASE for G.
    # I = all_polyominoes[0]
    # L = all_polyominoes[1]
    # T = all_polyominoes[2]
    # L_fliped = all_polyominoes[3]
    # S = all_polyominoes[4]
    # O = all_polyominoes[5]
    # S_fliped = all_polyominoes[6]
    # comb = []
    # comb.append([O.copy(), O.copy(), O.copy(), T.copy(), I.copy(), L.copy(), L.copy(), S_fliped.copy()])
    # comb.append([O.copy(), O.copy(), O.copy(), T.copy(), I.copy(), L_fliped.copy(), L_fliped.copy(), S_fliped.copy()])
    # comb.append([O.copy(), O.copy(), O.copy(), T.copy(), I.copy(), L.copy(), L.copy(), S.copy()])
    # comb.append([O.copy(), O.copy(), O.copy(), T.copy(), I.copy(), L_fliped.copy(), L_fliped.copy(), S.copy()])

if __name__ == '__main__':
    # Note: Can do this in parallel.
    parser = argparse.ArgumentParser()
    parser.add_argument('--thread_id', type=int, default=0)
    args = parser.parse_args()
    
    solve_ind = args.thread_id
    location ="../outputs/"
    
    solve(solve_ind, location)

    # create textures if needed.
    texture_files = [os.path.join(location, f"tmp_{x}.png") for x in range(20) ]
    for path in texture_files:
        if not os.path.exists(path):
            texture_files = create_texture_files(k=20, location=location)
            break
        
    # We can now visualize the solution.
    board = board_dict[solve_ind]
    board = (np.array(board) == 1).tolist()
    blocks, locations, rotations = cPickle.load(open(os.path.join(location, f"/logic_solution_{solve_ind}.pkl"), "rb"))
    rotated_blocks = P.apply_rotations(blocks, rotations)

    fig = draw_packing_with_texture(rotated_blocks, locations, len(board[0]), len(board), texture_files)
    fig.show()
    plt.axis('off')
    fig.patch.set_facecolor('lightsteelblue')
    fig.savefig(os.path.join(location, f'logic/{solve_ind}.png'), bbox_inches='tight', pad_inches=0)
    plt.close()
    