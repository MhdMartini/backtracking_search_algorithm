import numpy as np
from shortest_path import ShortestPath
import cv2
import random


class Searcher:
    def __init__(self, map_, start=None, vid=False):
        self.map_name = map_
        self.map = cv2.imread(self.map_name, 0) // 255
        self.start_map = np.copy(self.map)  # save start map
        self.rows, self.cols = self.map.shape
        self.start = start if start is not None else self.get_start()
        self.current = self.start
        self.vid = vid
        self.visited_coords = []
        self.discovered_coords = set()
        self.directions = {
            "E": (0, 1),
            "N": (-1, 0),
            "W": (0, -1),
            "S": (1, 0)
        }
        self.searcher(self.current)

    def get_start(self):
        # get a random start position
        while True:
            coord = (random.choice(range(self.rows)), random.choice(range(self.cols)))
            if self.map[coord[0], coord[1]] == 0:
                return coord

    def not_valid(self, pos):
        r, c = pos
        return r < 0 or r >= self.rows or c < 0 or c >= self.cols

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

            if self.not_valid((candidate_row, candidate_col)):
                continue

            if map_[candidate_row, candidate_col] == 0:
                possible_dirs[baring] = direction

        return possible_dirs

    def searcher(self, pos):
        # Backtracking search. Fill self.visited_coords with the blocks to be searched.
        self.map[pos[0], pos[1]] = 1
        self.current = pos
        directions = self.get_directions(pos)
        self.add_discovered(pos, directions)  # Add the discovered cells to the self.discovered_coords

        if not directions:
            if 0 not in self.map:
                # print(self.map)
                # print(self.visited_coords)
                if self.vid:
                    self.plot_path()
                raise Exception(f"Done in {len(self.visited_coords)} steps.")
            return

        for baring, direction in directions.items():
            pos_new = (pos[0] + direction[0], pos[1] + direction[1])
            self.move_to(pos_new)
            self.searcher(pos_new)

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
        # Find the shortest path between self.current and pos_new given the self.discovered_coords
        discovered_map = self.get_discovered_map()
        if self.current != pos_new:
            path = ShortestPath(map_=discovered_map, start=self.current, destination=pos_new).shortest_path
            self.visited_coords.extend(path)

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

    def plot_path(self):
        start = np.copy(self.start_map) * 255
        start = cv2.merge((start, start, start))
        start[self.start[0], self.start[1], 2] += 150
        vid_name = f"{self.map_name.split('.')[0]}.avi"
        out = cv2.VideoWriter(vid_name, cv2.VideoWriter_fourcc(*'DIVX'), 30, (self.cols, self.rows))
        out.write(start)
        temp = np.copy(start)
        for i, coord in enumerate(self.visited_coords, start=1):
            temp = np.copy(temp)
            color = temp[coord[0], coord[1], 2]
            if color > 0:
                temp[coord[0], coord[1], 1] += 200
            else:
                temp[coord[0], coord[1], 2] += 150
            out.write(temp)
        out.release()


if __name__ == '__main__':

    MAP = "maps/map2_100_i.png"
    try:
        Searcher(MAP, start=None, vid=False)
    except Exception as e:
        print(e)
