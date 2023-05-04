import packing.packing as P
import viz.visualize as viz
import packing.tetriminoes as tet
import numpy as np
from packing.polymino import Polyomino

# H = 8
# W = 4
# polyominoes = [
#     tet.L,
#     tet.L,
#     tet.LINE,
#     tet.T
# ]
if __name__ == '__main__':
    polyominoes = Polyomino(N=4).polys * 2
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
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ]
    board = np.zeros((6, 6)).tolist()
    blocks, locations, rotations = P.solve_polyomino_packing(polyominoes, board)
    rotated_blocks = P.apply_rotations(blocks, rotations)
    if locations:
        viz.draw_packing(rotated_blocks, locations, len(board[0]), len(board))


# H = 8
# W = 4
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

# # H = 2
# # W = 4
# # polyominoes = [
# #     tet.SQUARE,
# #     tet.SQUARE,
# # ]
# blocks, locations, rotations = P.solve_polyomino_packing(polyominoes, W, H)

# rotated_blocks = P.apply_rotations(blocks, rotations)
    
# if locations:
#     viz.draw_packing(rotated_blocks, locations, W, H)