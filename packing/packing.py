import z3
from z3 import Bool, Int, And, Or, Solver, Not, sat, If, Sum
import viz.visualize as viz
import packing.tetriminoes as tet

z3.set_param('parallel.enable', True)

def cell_value(z3_board, x, y):
    height = len(z3_board)
    width = len(z3_board[0])
    elements = [If(And(i == y, j == x), z3_board[i][j], 0) for i in range(height) for j in range(width)]
    return Sum(elements)

def rotated_coordinates(x, y, rotation):
    # Z3 rotation :
    return (If(rotation == 0, x, If(rotation == 90, y, If(rotation == 180, -x, -y))),
            If(rotation == 0, y, If(rotation == 90, -x, If(rotation == 180, -y, x))))

def rotator(x, y, rotation):
    # Python rotation :
    if rotation == 0:
        return x, y
    elif rotation == 90:
        return y, -x
    elif rotation == 180:
        return -x, -y
    elif rotation == 270:
        return -y, x
    
    raise ValueError(f"Invalid rotation {rotation}")

def apply_rotations(blocks, rotations):
    rotated_blocks = []
    for i in range(len(blocks)):
        rotated_blocks.append([])
        for x, y in blocks[i]:
            rotated_blocks[i].append(rotator(x, y, rotations[i]))
    return rotated_blocks

class Polyomino:
    def __init__(self, polyomino, board):
        self.blocks = polyomino
        self.board = board
        self.width = len(board[0])
        self.height = len(board)
        self.placed = Bool(f"placed_{id(self)}")
        self.x = Int(f"x_{id(self)}")
        self.y = Int(f"y_{id(self)}")
        self.rotation = Int(f"rotation_{id(self)}") 

def polyomino_constraints(polyomino, other_polyominoes):
    constraints = []

    for dx, dy in polyomino.blocks:
        rotated_dx, rotated_dy = rotated_coordinates(dx, dy, polyomino.rotation)
        x = polyomino.x + rotated_dx
        y = polyomino.y + rotated_dy

        # The polyomino must be placed within the board
        constraints.append(And(x >= 0, x < polyomino.width, y >= 0, y < polyomino.height))

        # The polyomino must not be placed on blocked cells
        constraints.append(If(polyomino.placed, cell_value(polyomino.board, x, y) == 0, True))
        # constraints.append(If(polyomino.placed, polyomino.board[y][x] == 0, True))

        # The polyomino must not overlap with any other polyominoes
        for other_polyomino in other_polyominoes:
            for other_dx, other_dy in other_polyomino.blocks:
                other_rotated_dx, other_rotated_dy = rotated_coordinates(other_dx, other_dy, other_polyomino.rotation)
                other_x = other_polyomino.x + other_rotated_dx
                other_y = other_polyomino.y + other_rotated_dy
                constraints.append(Or(Not(polyomino.placed),
                                      Not(other_polyomino.placed),
                                      x != other_x,
                                      y != other_y))

    # If the polyomino is not placed, its position and rotation variables should not affect the constraints
    constraints.append(Or(polyomino.placed, And(polyomino.x == 0, polyomino.y == 0, polyomino.rotation == 0)))

    # The rotation variable must be one of the allowed values (0, 90, 180, 270)
    constraints.append(Or(polyomino.rotation == 0,
                          polyomino.rotation == 90,
                          polyomino.rotation == 180,
                          polyomino.rotation == 270))

    return constraints

def solve_polyomino_packing(polyominoes, board):
    z3_board = [ [ Int(f"cell_{i}_{j}") for j in range(len(board[0]))] for i in range(len(board)) ]

    z3_polyominoes = [Polyomino(p, z3_board) for p in polyominoes]
    solver = Solver()

    # Add constraints for the board cells
    for i in range(len(board)):
        for j in range(len(board[0])):
            solver.add(z3_board[i][j] == board[i][j])

    for polyomino in z3_polyominoes:
        other_polyominoes = [p for p in z3_polyominoes if p != polyomino]
        solver.add(polyomino_constraints(polyomino, other_polyominoes))
    
    # constraint that all polyominoes must be placed
    solver.add([polyomino.placed for polyomino in z3_polyominoes])

    if solver.check() == sat:
        solution = solver.model()
        locations = []
        rotations = []
        blocks = []
        for polyomino in z3_polyominoes:
            if solution.evaluate(polyomino.placed):
                x = solution.evaluate(polyomino.x).as_long()
                y = solution.evaluate(polyomino.y).as_long()
                rotation = solution.evaluate(polyomino.rotation).as_long()
                locations += [(x, y)]
                rotations += [rotation]
                blocks += [polyomino.blocks]
                print(f"Polyomino {polyomino.blocks} is placed at ({x}, {y})")
        return blocks, locations, rotations
    else:
        print("No solution found")
        return None

if __name__ == '__main__':
    # Example usage: pack a 3x20 board with 3 polyominoes
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
    board = [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1],
        [0, 1, 1, 1, 1]
    ]
    blocks, locations, rotations = solve_polyomino_packing(polyominoes, board)
    rotated_blocks = apply_rotations(blocks, rotations)
    if locations:
        viz.draw_packing(rotated_blocks, locations, W, H)