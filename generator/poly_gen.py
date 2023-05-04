
# copied from: https://codereview.stackexchange.com/questions/283149/polyominoes-generator
from time import time
from concurrent.futures import ProcessPoolExecutor, wait

def get_free_edges(tile):
    free_edges = []
    for x,y in tile:
        if (x - 1, y) not in tile: free_edges.append((x - 1, y))
        if (x + 1, y) not in tile: free_edges.append((x + 1, y))
        if (x, y - 1) not in tile: free_edges.append((x, y - 1))
        if (x, y + 1) not in tile: free_edges.append((x, y + 1))
    return sorted(set(free_edges))

def rotate90(tile):
    rotated = []
    zerox,zeroy = tile[0][0],tile[0][1]
    for x,y in tile: rotated.append((-y+zeroy, x+zerox))
    return sorted(set(rotated))

def reflect(tile):
    reflected = []
    for x,y in tile: reflected.append((-x, y))
    return sorted(set(reflected))

def normalize(tile):
    xmin = min(tile, key=lambda t: t[0])[0]
    ymin = min(tile, key=lambda t: t[1])[1]
    normalized = []
    for x,y in tile: normalized.append((x - xmin, y - ymin))
    return sorted(normalized)

def old_remove_duplicates(tiles):
    seen = []
    seen_add = seen.append
    return [x for x in tiles if not (x in seen or seen_add(x))]

def remove_duplicates(tiles):
    set_ = set(tuple(x) for x in tiles)
    return [list(x) for x in set_]

def all_variants_nonunique(tile):
    a = tile
    for _ in range(4):
        yield normalize(a)
        yield normalize(reflect(a))
        a = rotate90(a)

def all_variants(tile):
    return remove_duplicates(all_variants_nonunique(tile))

def is_valid(tile1,tile2):
    for x,y in tile2:
        if (x,y) in tile1:
            return False
        else:
            continue
    return True

def connect(tile, root):
    result = []
    seen = []
    root_variants = all_variants(root)
    tile_variants = all_variants(tile)
    for r in root_variants:
        free = get_free_edges(r)
        for dx,dy in free:
            for tile in tile_variants:
                for x,y in tile:
                    x2 = -x + dx
                    y2 = -y + dy
                    moved_tile = [(x + x2, y + y2) for x, y in tile]
                    if is_valid(r,moved_tile):
                        poly = normalize(r + moved_tile)
                        if poly not in seen:
                            seen += all_variants(poly)
                            result.append(poly)
    return result

def level_linear(tiles,root,n=2):
    if not isinstance(tiles[0], list): tiles = [tiles]
    result = []
    seen = []
    if n == 2:
        for tile in tiles:
            data = connect(tile, root)
            for i in data:
                if i not in seen:
                    result.append(i)
                    seen += all_variants(i)
        return result
    else:
        return level_linear(level_linear(tiles, root,n-1), root)
    
def level_multi(tiles,root,n=2):
    if not isinstance(tiles[0], list): tiles = [tiles]
    result = []
    seen = set()
    if n == 2:
        futures = [executor.submit(connect, tile, root) for tile in tiles] # maybe round brackets
        a,b = wait(futures)
        for future in a:
            for i in future.result():
                ti = tuple(i)
                if ti not in seen:
                    result.append(i)
                    seen.update(tuple(x) for x in all_variants(ti))
        return result
    else:
        return level_multi(level_multi(tiles, root,n-1), root)
def pretty_print(tiles):
    for tile in tiles:
        x,y = zip(*tile)
        for i in range(max(x) + 1):
            for j in range(max(y) + 1):
                if (i, j) in tile:
                    print("\033[107m   \033[00m",end="")
                else:
                    print("\033[40m   \033[00m",end="")
            print()
        print()
        print()

if __name__ == '__main__':

    executor = ProcessPoolExecutor(max_workers=10)
    root = [(0,0)]

    ts = time()
    #result = level_linear(root,root,6)
    result = level_multi(root,root,10)
    #pretty_print(result)
    print('Total free polyominoes:',len(result))
    print('Took %s seconds'%(time() - ts))