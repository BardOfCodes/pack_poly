import packing.packing as P
import viz.visualize as viz
import packing.tetriminoes as tet
import numpy as np
import time
from tqdm import tqdm
from packing.polymino import poly_generator
from itertools import combinations_with_replacement

H = 4
W = 5

def stability_exp():
    board = np.zeros((H, W)).astype(bool).tolist()
    all_polyominoes = poly_generator(N=4)
    comb = list(combinations_with_replacement(all_polyominoes, 5))
    print(f"Total number of combinations: {len(list(comb))}")

    success_rates = []
    for starting_polys in tqdm(comb):
        starting_polys = list(starting_polys)
        num_success = 0
        total = 0
        for i in range(len(all_polyominoes)):
            # replace i-th polyomino with j-th polyomino
            for j in range(len(all_polyominoes)):
                if j == i:
                    continue

                curr_polyominoes = starting_polys.copy()
                curr_polyominoes.pop(i)
                curr_polyominoes += [starting_polys[j]]

                blocks, locations, rotations = P.solve_polyomino_packing(curr_polyominoes, board)
                if blocks is not None:
                    rotated_blocks = P.apply_rotations(blocks, rotations)
                    if locations:
                        viz.draw_packing(rotated_blocks, locations, W, H)

                    num_success += 1

                total += 1

        success_rates.append(num_success / total)            
        print(success_rates[-1])

    # print(f"Total number of successes: {num_success}"
    #       f" out of {total} trials")
    # print(f"Success rate: {num_success / total}")
    print(success_rates)

if __name__ == '__main__':
    stability_exp()