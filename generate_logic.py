import packing.packing as P
import viz.visualize as viz
import packing.tetriminoes as tet
import numpy as np
import time
from packing.polymino import Polyomino
from generator.map_solve import generate_puzzle
from packing.polymino import poly_generator
from itertools import combinations_with_replacement
from multiset import FrozenMultiset
import _pickle as cPickle
import argparse
import random

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


def solve(solve_id):
    board = board_dict[solve_id]
    board = (np.array(board) == 1).tolist()
    all_polyominoes = poly_generator(N=4)
    # comb = list(combinations_with_replacement(all_polyominoes, 8))
    # random.shuffle(comb)
    I = all_polyominoes[0]
    L = all_polyominoes[1]
    T = all_polyominoes[2]
    L_fliped = all_polyominoes[3]
    S = all_polyominoes[4]
    O = all_polyominoes[5]
    S_fliped = all_polyominoes[6]
    comb = []
    comb.append([O.copy(), O.copy(), O.copy(), T.copy(), I.copy(), L.copy(), L.copy(), S_fliped.copy()])
    comb.append([O.copy(), O.copy(), O.copy(), T.copy(), I.copy(), L_fliped.copy(), L_fliped.copy(), S_fliped.copy()])
    comb.append([O.copy(), O.copy(), O.copy(), T.copy(), I.copy(), L.copy(), L.copy(), S.copy()])
    comb.append([O.copy(), O.copy(), O.copy(), T.copy(), I.copy(), L_fliped.copy(), L_fliped.copy(), S.copy()])
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
                f"outputs/logic_solution_{solve_id}.pkl", "wb"))
            break


if __name__ == '__main__':
    # generate_and_solve()
    parser = argparse.ArgumentParser()
    parser.add_argument('--thread_id', type=int, default=2)
    args = parser.parse_args()
    solve(args.thread_id)
