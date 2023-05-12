import packing.packing as P
import viz.visualize as viz
import packing.tetriminoes as tet
import numpy as np
import time
from packing.polymino import poly_generator
from generator.map_solve import generate_puzzle
import _pickle as cPickle

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
# Tests for partially empty boards

# Property Based Testing via Generator
# Test for existence
def generate_and_solve(board_size=8, polymino_N=3, min_count=5, n_test=10):
    # brute force to generate larger puzzle
    for test_id in range(n_test):
        while True:
            board, formatted_poly, positions = generate_puzzle(board_size=board_size,
                                                               polymino_N=polymino_N)
            if len(formatted_poly) > min_count:
                break
        board = (board).astype(bool)
        board = np.flip(board, 0).tolist()
        formatted_poly = [[(y[0], y[1]) for y in x] for x in formatted_poly]
        print(
            f"Running test with board size {len(board)}x{len(board[0])} and {len(formatted_poly)} polyominoes")
        blocks, locations, rotations = P.solve_polyomino_packing(
            formatted_poly, board)
        rotated_blocks = P.apply_rotations(blocks, rotations)
        # verify solution?
        verify_solution(board, rotated_blocks, locations)
        solution = [blocks, locations, rotations]
        cPickle.dump(solution, open(f"outputs/generated_solution_{test_id}.pkl", "wb"))


def verify_solution(board, blocks, locations):
    H, W = len(board), len(board[0])
    filled_positions = []
    for ind, cur_block in enumerate(blocks):
        # check if block is in board
        cur_location = locations[ind]
        for dx, dy in cur_block:
            pos = (cur_location[0] + dx, cur_location[1] + dy)
            assert 0 <= pos[1] < H
            assert 0 <= pos[0] < W
            assert board[pos[1]][pos[0]] == False
            filled_positions.append(pos)
    for i in range(H):
        for j in range(W):
            if board[i][j] == 0:
                assert (j, i) in filled_positions


def run_tests():
    total_elapsed = 0
    for test_id, test in enumerate(tests):
        print(
            f"Running test with board size {len(test.board)}x{len(test.board[0])} and {len(test.polyominoes)} polyominoes")
        start = time.time()
        blocks, locations, rotations = P.solve_polyomino_packing(
            test.polyominoes, test.board)
        total_elapsed += time.time() - start
        rotated_blocks = P.apply_rotations(blocks, rotations)
        verify_solution(test.board, rotated_blocks, locations)
        solution = [blocks, locations, rotations]
        cPickle.dump(solution, open(f"outputs/handcrafted_solution_{test_id}.pkl", "wb"))
        # if locations:
        #     viz.draw_packing(rotated_blocks, locations,
        #                      len(test.board[0]), len(test.board))

    print(f"Total elapsed time: {total_elapsed / 60} minutes")

    # for generated tests:
    print("Testing with generated puzzles")
    start = time.time()
    generate_and_solve(board_size=8, polymino_N=4, min_count=5, n_test=10)
    end = time.time()
    print(f"Total elapsed time: {(end - start) / 60} minutes")


if __name__ == '__main__':
    run_tests()
