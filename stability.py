import packing.packing as P
import viz.visualize as viz
import packing.tetriminoes as tet
import numpy as np
import time
from tqdm import tqdm
import logging
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
    solution_cache = {}
    for starting_polys in tqdm(comb):
        starting_polys = list(starting_polys)
        unique_original_sig = tuple([tuple(x) for x in starting_polys])
        num_success = 0
        total = 0
        for i in range(len(all_polyominoes)):
            # replace i-th polyomino with j-th polyomino

            for j in range(len(all_polyominoes)):

                curr_polyominoes = starting_polys.copy()
                curr_polyominoes.pop(i)
                curr_polyominoes += [all_polyominoes[j]]
                # check if it results in the same solution
                unique_sig = tuple([tuple(x) for x in curr_polyominoes])
                if unique_sig == unique_original_sig:
                    continue

                if unique_sig in solution_cache.keys():
                    logger.info("Found a solution in the cache!")
                    solved, rotated_blocks, locations = solution_cache[unique_sig]
                    if solved:
                        num_success += 1
                else:
                    logger.info(f"New Puzzle to solve.")
                    blocks, locations, rotations = P.solve_polyomino_packing(
                        curr_polyominoes, board)

                    if blocks is not None:
                        rotated_blocks = P.apply_rotations(blocks, rotations)
                        solution_cache[unique_sig] = (
                            True, rotated_blocks, locations)
                        # if locations:
                        #     viz.draw_packing(rotated_blocks, locations, W, H)

                        num_success += 1
                    else:
                        solution_cache[unique_sig] = (False, None, None)

                total += 1

        success_rates.append(num_success / total)
        
        logger.info(f"Stability rate: {success_rates[-1]}")

    # print(f"Total number of successes: {num_success}"
    #       f" out of {total} trials")
    # print(f"Success rate: {num_success / total}")
    print(success_rates)
    # Print the most stable configuration
    max_stability = max(success_rates)
    max_idx = success_rates.index(max_stability)
    print(f"Most stable configuration: {comb[max_idx]}")
    print(f"Stability rate: {max_stability}")

if __name__ == '__main__':
    # create a logger:

    logger = logging.getLogger('stability')
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler('stability.log')
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    start = time.time()
    stability_exp()
    end = time.time()
    print(f"Total time: {end - start} seconds")
