import packing.packing as P
import viz.visualize as viz
import packing.tetriminoes as tet
import numpy as np
import time
from packing.polymino import Polyomino
from generator.map_solve import generate_puzzle

def generate_and_solve():
    # brute force to generate larger puzzle
    while True:
        board, formatted_poly, positions = generate_puzzle(board_size=8, polymino_N=4)
        if len(formatted_poly) > 5:
            break

    print("number of polyminos: ", len(formatted_poly))
    print("positions: ", positions)
    print("polyminos: ", formatted_poly)
    print(board)
    viz.draw_polymino_set(formatted_poly)
    board = (board).astype(int)
    board = np.flip(board, 0).tolist()

    start = time.time()
    blocks, locations, rotations = P.solve_polyomino_packing(formatted_poly, board)
    print(f"Elapsed Time: {(time.time() - start) / 60} minutes")

    rotated_blocks = P.apply_rotations(blocks, rotations)
    if locations:
        viz.draw_packing(rotated_blocks, locations, len(board[0]), len(board))

def manual_solve():
    polyominoes = Polyomino(N=4).polys
    # polyominoes = [
    #     tet.T,
    #     tet.T,
    #     tet.L,
    #     tet.L,
    #     tet.L,
    #     tet.LINE,
    #     tet.SQUARE,
    #     tet.SQUARE
    # ]
    print(len(polyominoes))
    board = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ]
    board = np.zeros((5, 5)).tolist()
    start = time.time()
    blocks, locations, rotations = P.solve_polyomino_packing(polyominoes, board)
    print(f"Elapsed Time: {(time.time() - start) / 60} minutes")

    rotated_blocks = P.apply_rotations(blocks, rotations)
    if locations:
        viz.draw_packing(rotated_blocks, locations, len(board[0]), len(board))

if __name__ == '__main__':
    # generate_and_solve()
    manual_solve()
