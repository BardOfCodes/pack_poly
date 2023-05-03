# Sample random CSG programs.
import torch as th
import numpy as np
import random


BOOLEAN = ['union', 'intersection', 'difference']
PRIMITIVE = ['rectangle', 'ellipse']

TRANSLATION_BOUNDS = (-0.5, 0.5)
SCALE_BOUNDS = (0.25, 1.5)
ROTATION_BOUNDS = (-np.pi, np.pi)

PRIM_OCC_LIMITS = [0.05, 0.1]
PROGRAM_OCC_LIMIT = [0.1, 0.2]
CHILD_MATCH_LIMIT = 0.8


def sample_primitive():
    translation = np.random.uniform(*TRANSLATION_BOUNDS, size=(2,))
    scale = np.random.uniform(*SCALE_BOUNDS, size=(2,))
    rotation = np.random.uniform(*ROTATION_BOUNDS)

    if np.random.uniform() > 0.5:
        primitive = PRIMITIVE[0]
    else:
        primitive = PRIMITIVE[1]

    primitive_string = f'{primitive}({translation[0]:.3f}, {translation[1]:.3f}, {scale[0]:.3f}, {scale[1]:.3f}, {rotation:.1f})'
    return primitive_string


def sample_boolean():
    boolean = BOOLEAN[np.random.randint(3)]
    return boolean


def valid_primitive(primitive, executor):
    # hack_expr = ["union", primitive, primitive]
    hack_expr = [primitive]
    output = executor.execute(hack_expr)
    occupancy = output.mean().item()

    if PRIM_OCC_LIMITS[0] < occupancy < PRIM_OCC_LIMITS[1]:
        return True
    else:
        return False


def valid_program(all_programs, executor):
    output = executor.eval_batch_execute(all_programs)
    # should not be similar to either childs:
    parent = output[0]
    left_child = output[1]
    right_child = output[2]
    left_match = th.logical_and(parent, left_child).float().mean().item()
    right_match = th.logical_and(parent, right_child).float().mean().item()
    if left_match > CHILD_MATCH_LIMIT or right_match > CHILD_MATCH_LIMIT:
        return False
    occupancy = parent.mean().item()

    if PROGRAM_OCC_LIMIT[0] < occupancy < PROGRAM_OCC_LIMIT[1]:
        return True
    else:
        return False


def get_random_csg_program(executor, n_ops=2):

    while (True):
        init_primitive = sample_primitive()
        if valid_primitive(init_primitive, executor):
            break
        else:
            print("stuck with primitive generation")
    csg_program = [init_primitive]

    for i in range(n_ops):

        while (True):
            new_primitive = sample_primitive()
            new_op = sample_boolean()
            if np.random.uniform() > 0.5:
                # left
                new_program = [new_op, new_primitive] + csg_program
            else:
                # right
                new_program = [new_op] + csg_program +  [new_primitive]
            all_programs = [new_program, csg_program, [new_primitive]]
            if valid_program(all_programs, executor):
                break
            else:
                print('stuck with program generation')
        csg_program = new_program
    # quick render file:
    return csg_program

def get_map(executor, n_ops=2):
    
    map_expr = get_random_csg_program(executor, n_ops)
    map_tensor = executor.execute(map_expr)
    map_tensor = map_tensor.cpu().numpy()
    
    return map_tensor


if __name__ == "__main__":
    
    import sys
    sys.path.insert(0, './')
    from csg_lib import CSG2DExecutor
    from generator.map_gen import get_random_csg_program
    executor = CSG2DExecutor(64, th.device('cuda'))

    random_program = get_map(executor, n_ops=4)