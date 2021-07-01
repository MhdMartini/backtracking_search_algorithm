import numpy as np
from math import sqrt


class Searcher:
    def __init__(self, map_, start=(0, 0)):
        self.map = map_
        self.rows, self.cols = self.map.shape
        self.current = start
        self.visited_coords = []
        self.discovered_coords = set()
        self.directions = {
            "E": (0, 1),
            "N": (-1, 0),
            "W": (0, -1),
            "S": (1, 0)
        }
        self.searcher(start)

    def get_directions(self, pos, map_=None):
        # Get the e, n, w, s directions around a given position which are not walls
        if map_ is None:
            map_ = self.map

        possible_dirs = {}
        r, c = pos
        for baring, direction in self.directions.items():
            dr, dc = direction
            candidate_row = r + dr
            candidate_col = c + dc

            if candidate_col < 0 or candidate_col >= self.cols:
                continue
            if candidate_row < 0 or candidate_row >= self.rows:
                continue

            if map_[candidate_row, candidate_col] == 0:
                possible_dirs[baring] = direction

        return possible_dirs

    def searcher(self, pos):
        # Backtracking search. Return the order of blocks to be searched
        self.map[pos[0], pos[1]] = 1
        self.current = pos
        directions = self.get_directions(pos)
        self.add_discovered(pos, directions)  # Add the discovered cells to the self.discovered_coords

        if not directions:
            if 0 not in self.map:
                # Can be safely deleted to maintain the uninformed search criteria
                print(self.map)
                raise Exception("Done!")
            return False

        for baring, direction in directions.items():
            pos_new = (pos[0] + direction[0], pos[1] + direction[1])
            self.move_to(pos_new)
            # TODO:
            # Add code to move to the new position
            # The new position could be adjacent (n, w, e, s) in which case there is no problem
            # But if it is not, we can use flood fill on the nodes the agent has discovered to find the shortest path

            # print(pos_new)  # This is the next cell to search

            if self.searcher(pos_new):
                return True

        return False

    def adjacent(self, pos_new):
        r, c = self.current
        r_new, c_new = pos_new
        if c == c_new and (r - r_new)**2 == 1:
            return True
        if r == r_new and (c - c_new)**2 == 1:
            return True
        return False

    def add_discovered(self, pos, directions):
        # Add current position and other possible positions to the self.discovered set
        self.discovered_coords.add(pos)

        r, c = pos
        for _, direction in directions.items():
            dr, dc = direction
            row_new = r + dr
            col_new = c + dc
            self.discovered_coords.add((row_new, col_new))

    def move_to(self, pos_new):
        # if the new position is adjacent to the old position, just append it
        # Otherwise, find the shortest path and append those cells.
        if self.adjacent(pos_new):
            self.visited_coords.append(pos_new)
            return

        # Only get here when the new positions is far away from current position
        # Build a matrix where discovered points are marked as 0, and others are marked as inf
        # Then, find the shortest path between self.current and pos_new given the self.discovered_coords
        discovered_map = self.get_discovered_map()
        path = self.shortest_path(discovered_map, pos_new)

    def get_discovered_map(self):
        discovered_map = []
        for i in range(self.rows):
            row_new = []
            for j in range(self.cols):
                if (i, j) in self.discovered_coords:
                    row_new.append(0)
                else:
                    row_new.append(np.inf)
            discovered_map.append(row_new)

        # # debugging
        # print(np.array(discovered_map))
        # raise Exception("Debugging")

        return np.array(discovered_map)

    def coords_from_directions(self, current, directions):
        # get the directions dictionary and the current position and return the cells coordinates
        coords = []
        r, c = current
        for _, direction in directions.items():
            dr, dc = direction
            row = r + dr
            col = c + dc
            coords.append((row, col))
        return coords

    def parse_discovered(self, discovered_map):
        print(discovered_map)

    def shortest_path(self, discovered_map, pos_new, current=None, rank=1):
        if not current:
            current = self.current

        print(f"\n current: {current}, destination: {pos_new}")

        discovered_map_temp = np.copy(discovered_map)
        cells = [current]
        cells_index = 0
        discovered_map_temp[current[0], current[1]] = rank
        while True:
            # Flood fill the discovered map from source to destination
            # ITS WRONG
            try:
                directions = self.get_directions(cells[cells_index], map_=discovered_map_temp)
                if directions:
                    rank += 1
                # print(discovered_map)
            except IndexError:
                print(discovered_map_temp)
                break

            coords = self.coords_from_directions(cells[cells_index], directions)

            for coord in coords:
                if coord not in cells:
                    cells.append(coord)
                    discovered_map_temp[coord[0], coord[1]] = rank
                    if coord == pos_new:
                        return self.parse_discovered(discovered_map_temp)
            cells_index += 1
        print("Here")
        # if current == pos_new:
        #     # we arrived at the destination
        #     discovered_map[current] = rank
        #     # print("found it")
        #     return True


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
        # raise e
        print(e)
