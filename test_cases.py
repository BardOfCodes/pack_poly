import packing.packing as P
import viz.visualize as viz
import packing.tetriminoes as tet
import numpy as np
import time
from packing.polymino import poly_generator

def empty_board(H, W):
    # to bool:
    return np.zeros((H, W)).astype(bool).tolist()
    # return np.zeros((H, W)).tolist()

class Test():
    def __init__(self, board, polyominoes):
        self.board = board
        self.polyominoes = polyominoes

tests = [
    Test(
        empty_board(10, 10),
        poly_generator(N=4)
    ),
    Test(
        empty_board(6, 6),
        poly_generator(N=4)
    ),
    Test(
        empty_board(7, 7),
        poly_generator(N=4) * 2
    ),
    Test(
        empty_board(8, 8),
        poly_generator(N=5)
    ),
]

def run_tests():
    total_elapsed = 0
    for test in tests:
        print(f"Running test with board size {len(test.board)}x{len(test.board[0])} and {len(test.polyominoes)} polyominoes")
        start = time.time()
        blocks, locations, rotations = P.solve_polyomino_packing(test.polyominoes, test.board)
        total_elapsed += time.time() - start
        rotated_blocks = P.apply_rotations(blocks, rotations)
        if locations:
            viz.draw_packing(rotated_blocks, locations, len(test.board[0]), len(test.board))

    print(f"Total elapsed time: {total_elapsed / 60} minutes")

if __name__ == '__main__':
    run_tests()