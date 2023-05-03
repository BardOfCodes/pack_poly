from z3 import Bool, Int, And, Or, Solver, Not, sat, If
import viz.visualize as viz
import packing.tetriminoes as tet

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
    def __init__(self, polyomino, board_width, board_height):
        self.blocks = polyomino
        self.width = board_width
        self.height = board_height
        self.placed = Bool(f"placed_{id(self)}")
        self.x = Int(f"x_{id(self)}")
        self.y = Int(f"y_{id(self)}")
        self.rotation = Int(f"rotation_{id(self)}") 

# def polyomino_constraints(polyomino, other_polyominoes):
#     constraints = []

#     for dx, dy in polyomino.blocks:
#         x = polyomino.x + dx
#         y = polyomino.y + dy

#         # The polyomino must be placed within the board
#         constraints.append(And(x >= 0, x < polyomino.width, y >= 0, y < polyomino.height))

#         # The polyomino must not overlap with any other polyominoes
#         for other_polyomino in other_polyominoes:
#             for other_dx, other_dy in other_polyomino.blocks:
#                 other_x = other_polyomino.x + other_dx
#                 other_y = other_polyomino.y + other_dy
#                 constraints.append(Or(Not(polyomino.placed),
#                                       Not(other_polyomino.placed),
#                                       x != other_x,
#                                       y != other_y))

#     # If the polyomino is not placed, its position variables should not affect the constraints
#     constraints.append(Or(polyomino.placed, And(polyomino.x == 0, polyomino.y == 0)))

#     return constraints

def polyomino_constraints(polyomino, other_polyominoes):
    constraints = []

    for dx, dy in polyomino.blocks:
        rotated_dx, rotated_dy = rotated_coordinates(dx, dy, polyomino.rotation)
        x = polyomino.x + rotated_dx
        y = polyomino.y + rotated_dy

        # The polyomino must be placed within the board
        constraints.append(And(x >= 0, x < polyomino.width, y >= 0, y < polyomino.height))

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

def solve_polyomino_packing(polyominoes, board_width, board_height):
    z3_polyominoes = [Polyomino(p, board_width, board_height) for p in polyominoes]
    solver = Solver()

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
    blocks, locations, rotations = solve_polyomino_packing(polyominoes, W, H)
    rotated_blocks = apply_rotations(blocks, rotations)
    if locations:
        viz.draw_packing(rotated_blocks, locations, W, H)