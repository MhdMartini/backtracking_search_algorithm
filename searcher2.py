import numpy as np


class Searcher:
    def __init__(self, map_, start=(0, 0)):
        self.map = map_
        self.rows, self.cols = self.map.shape
        self.start = start
        self.visited_coords = []
        self.directions = {
            "E": (0, 1),
            "N": (-1, 0),
            "W": (0, -1),
            "S": (1, 0)
        }
        self.searcher(self.start)

    def get_directions(self, pos):
        # Get the e, n, w, s directions around a given position which are not walls
        possible_dirs = {}
        for baring, direction in self.directions.items():
            r, c = pos
            dr, dc = direction
            candidate_row = r + dr
            candidate_col = c + dc

            if candidate_col < 0 or candidate_col >= self.cols:
                continue
            if candidate_row < 0 or candidate_row >= self.rows:
                continue

            if self.map[candidate_row, candidate_col] == 0:
                possible_dirs[baring] = direction

        return possible_dirs

    def searcher(self, pos):
        # Backtracking search. Return the order of blocks to be searched
        self.map[pos[0], pos[1]] = 1
        directions = self.get_directions(pos)

        if not directions:
            if 0 not in self.map:
                # Can be safely deleted to maintain the uninformed search criteria
                print(self.map)
                raise Exception("Done")
            return False

        for baring, direction in directions.items():
            pos_new = (pos[0] + direction[0], pos[1] + direction[1])
            # TODO:
            # Add code to move to the new position
            # The new position could be adjacent (n, w, e, s) in which case there is no problem
            # But if it is not, we can use flood fill on the nodes the agent has discovered to find the shortest path

            # print(pos_new)  # This is the next cell to search

            if self.searcher(pos_new):
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
        Searcher(MAP, start=START)
    except Exception as e:
        print(e)
