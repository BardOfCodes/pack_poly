import packing.packing as P
import viz.visualize as viz
import packing.tetriminoes as tet


H = 8
W = 4
polyominoes = [
    tet.T,
    tet.T,
    tet.L,
    tet.L,
    tet.L,
    tet.LINE,
    tet.SQUARE,
    tet.SQUARE
]

# H = 2
# W = 4
# polyominoes = [
#     tet.SQUARE,
#     tet.SQUARE,
# ]
blocks, locations, rotations = P.solve_polyomino_packing(polyominoes, W, H)

rotated_blocks = P.apply_rotations(blocks, rotations)
    
if locations:
    viz.draw_packing(rotated_blocks, locations, W, H)