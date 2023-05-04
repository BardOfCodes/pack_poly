import time
from generator.map_gen import get_map
import packing.tetriminoes as tet
from csg_lib import CSG2DExecutor
from packing.polymino import poly_generator
import torch as th
import numpy as np


class ListPolyGenerator():

    def __init__(self, poly_list):

        self.poly_list = [np.array(poly) for poly in poly_list]

    def sample(self):
        poly_pointer = np.random.randint(len(self.poly_list))
        flip_x, flip_y = np.random.randint(2), np.random.randint(2)
        cur_poly = self.get_poly(poly_pointer, flip_x, flip_y)
        key = (poly_pointer, flip_x, flip_y)
        return cur_poly, key
    
    def get_poly(self, ptr, flip_x, flip_y, adjust=True):
        
        cur_poly = self.poly_list[ptr].copy()
        if flip_x:
            cur_poly = self.flip_x(cur_poly)
        if flip_y:
            cur_poly = self.flip_y(cur_poly)
            
        return cur_poly
    
    def flip_x(self, poly):
        poly[:, 0] *= -1
        min_val = np.min(poly[:, 0])
        if min_val < 0:
            poly[:, 0] += -min_val
        return poly
        
    def flip_y(self, poly):
        poly[:, 1] *= -1
        min_val = np.min(poly[:, 1])
        if min_val < 0:
            poly[:, 1] += -min_val
        return poly
        
        

def generate_poly_tensors(all_poly, device):
    polys = []
    for poly in all_poly:
        all_x = [x[0] for x in poly]
        all_y = [x[1] for x in poly]
        max_x = max(all_x)
        max_y = max(all_y)
        poly_grid = np.zeros((max_x + 1, max_y + 1), dtype=np.float32)
        for point in poly:
            poly_grid[point[0], point[1]] = 1
        poly_tensor = th.from_numpy(poly_grid).to(device)
        polys.append(poly_tensor)
    return polys


def solve_puzzle_greedy(map_np, poly_generator, poly_try_limit=200, n_outer_try=200):
    np_map_np = map_np.copy()
    poly_seq = []
    n_options = np.stack(np.where(np_map_np == 1), -1)
    outer_try_count = 0
    st = time.time()
    while (n_options.shape[0] > 0):
        # Sample a polymino
        sample_poly, poly_sig = poly_generator.sample()
        poly_try_count = 0
        solved = False
        # Commented out random position sampling
        # while (poly_try_count < poly_try_limit):
        #     # Sample a position from n_options:
        #     position = n_options[np.random.randint(n_options.shape[0])]
        #     check_positions = position + sample_poly
        #     # check within bounds:
        #     if validate_on_board(check_positions, np_map_np.shape):
        #         sel = np_map_np[tuple(check_positions.T)]
        #         if np.all(sel == 1):
        #             np_map_np[tuple(check_positions.T)] = 2
        #             poly_seq.append((poly_sig, position))
        #             solved = True
        #             break
        #     poly_try_count += 1
        if not solved:
            # try all positions:
            for position in n_options:
                check_positions = position + sample_poly
                # check within bounds:
                if validate_on_board(check_positions, np_map_np.shape):
                    sel = np_map_np[tuple(check_positions.T)]
                    if np.all(sel == 1):
                        np_map_np[tuple(check_positions.T)] = 2
                        poly_seq.append((poly_sig, position))
                        solved = True
                        break
                poly_try_count += 1

        n_options = np.stack(np.where(np_map_np == 1), -1)
        if not solved:
            outer_try_count += 1
        else:
            outer_try_count = 0
        if outer_try_count > n_outer_try:
            # Quit search
            et = time.time()
            print("Time taken: ", et - st)
            count_failure = np.sum(np_map_np == 1)
            count_success = np.sum(np_map_np == 2)
            print("Failure count: ", count_failure)
            print("Success count: ", count_success)
            break

    # convert map to not contain any ones:
    np_map_np[np_map_np == 1] = 0
    np_map_np[np_map_np == 2] = 1
    return np_map_np, poly_seq


def validate_on_board(check_positions, board_shape):
    c1 = np.all(check_positions[:, 0] >= 0)
    c2 = np.all(check_positions[:, 1] >= 0)
    c3 = np.all(check_positions[:, 0] < board_shape[0])
    c4 = np.all(check_positions[:, 1] < board_shape[1])
    validity = c1 and c2 and c3 and c4
    return validity

def get_formatted_solution(res, solution, poly_generator):
    formatted_solution = []
    positions = []
    for sol in solution:
        poly_ptr = sol[0]
        poly = poly_generator.get_poly(*poly_ptr)
        # flip x, y
        # poly = poly_generator.flip_y(poly)
        poly = poly.tolist()
        # poly = [(x[1], x[0]) for x in poly]
        formatted_solution.append(poly)
        
        pos = np.array([sol[1]])
        # pos = poly_generator.flip_x(pos)
        pos = pos.tolist()[0]
        # pos = tuple([pos[1], res - pos[0]])
        positions.append(pos)
        
    return formatted_solution, positions
        
        

def generate_puzzle(board_size, polymino_N):
    device = th.device('cuda')
    executor = CSG2DExecutor(board_size, device)
    all_poly = poly_generator(polymino_N)
    poly_gen = ListPolyGenerator(all_poly)

    while(True):
        map_np = get_map(executor, n_ops=3, return_np=True)
        # poly_tensors = generate_poly_tensors(all_poly, device)
        new_map, solution = solve_puzzle_greedy(map_np, poly_gen)
        if len(solution) > 0:
            break
    map_np = ~map_np.astype(bool)
    new_map = ~new_map.astype(bool)
    
    formatted_poly, positions = get_formatted_solution(board_size, solution, poly_gen)

    return new_map, formatted_poly, positions


if __name__ == "__main__":

    new_map, formatted_poly, positions = generate_puzzle(board_size=8, polymino_N=4)
    print("number of polyminos: ", len(formatted_poly))
    print("positions: ", positions)
    print("polyminos: ", formatted_poly)
    print(new_map)
