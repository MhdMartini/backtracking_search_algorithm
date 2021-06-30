import numpy as np


def get_directions(map_, pos):
    # Get the e, n, w, s directions around a given position which are not walls
    directions = {
        "E": (0, 1),
        "N": (-1, 0),
        "W": (0, -1),
        "S": (1, 0)
    }

    possible_dirs = {}
    for baring, direction in directions.items():
        r, c = pos
        dr, dc = direction
        candidate_row = r + dr
        candidate_col = c + dc
        rows, cols = map_.shape

        if candidate_col < 0 or candidate_col >= cols:
            continue
        if candidate_row < 0 or candidate_row >= rows:
            continue

        if map_[candidate_row, candidate_col] == 0:
            possible_dirs[baring] = direction

    return possible_dirs


def searcher(map_, pos):
    # Backtracking search. Return the order of blocks to be searched
    map_[pos[0], pos[1]] = 1
    directions = get_directions(map_, pos)

    if not directions:
        if 0 not in map_:
            print(map_)
            raise Exception("Done")
        return False

    for baring, direction in directions.items():
        pos_new = (pos[0] + direction[0], pos[1] + direction[1])

        # print(pos_new)  # This is the next cell to search

        if searcher(map_, pos_new):
            return True

    return False


if __name__ == '__main__':

    MAP = np.array([
        [0, 0, 0, 0, 1],
        [0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [1, 1, 0, 0, 0],
    ])
    START = (0, 0)

    try:
        searcher(MAP, START)
    except Exception as e:
        print(e)
