import numpy as np
import random
import cv2
import uuid
from tqdm import tqdm


class Cell:
    def __init__(self, val=None, prev=None, next_=None, row=None, col=None):
        self.val = val
        self.prev = prev
        self.next = next_
        self.row = row
        self.col = col

    def __repr__(self):
        return str(self.val)


class BacktrackSearch:
    def __init__(self, map_name, start=None, vid=False):
        self.map_name = map_name
        self.start_np_map = cv2.imread(map_name, 0) // 255
        self.rows, self.cols = self.start_np_map.shape

        self.start_map = self.construct_map(self.start_np_map)
        self.map = np.copy(self.start_map)

        self.start = start if start is not None else self.get_rand_start()
        self.directions = ((0, 1), (1, 0), (0, -1), (-1, 0))

        source = self.map[self.start[0]][self.start[1]]
        self.path = self.search(source)

        self.print_result()
        if vid:
            print("\nSaving Video ..")
            self.plot_path()
            print("Video saved!")

    def print_result(self):
        print(f"Map size: {self.rows} x {self.cols}")
        print(f"Start Position: {self.start}")
        print(f"Explorable cells: {(self.start_np_map==0).sum()}")
        print(f"Done in {len(self.path)} steps.")

    def construct_map(self, map_):
        # make 2d map of cell objects
        cells_map = []
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                row.append(Cell(val=map_[i, j], row=i, col=j))
            cells_map.append(row)
        return cells_map

    def get_rand_start(self):
        # get a random start position
        while True:
            coord = (random.choice(range(self.rows)), random.choice(range(self.cols)))
            if self.map[coord[0]][coord[1]].val == 0:
                return coord

    def get_neighbors(self, cell):
        r, c = cell.row, cell.col

        neighbors = []
        for direction in self.directions:
            dr, dc = direction
            candidate_row = r + dr
            candidate_col = c + dc

            if candidate_row < 0 or candidate_row >= self.rows:
                continue
            if candidate_col < 0 or candidate_col >= self.cols:
                continue
            if self.map[candidate_row][candidate_col].val == 1:
                continue

            neighbors.append(self.map[candidate_row][candidate_col])

        return neighbors

    def search(self, source):
        que = [source]
        path = []
        while len(que):
            current = que.pop()
            if current.val == 1:
                continue
            if current not in path:
                path.append(current)
                current.val = 1

            neighbors = self.get_neighbors(current)

            if not neighbors:
                backtracked = self.backtrack(current)
                path.extend(backtracked)
                # print_cells(backtracked)
                # raise Exception("debug")
                continue

            for neighbor in neighbors:
                que.append(neighbor)
                neighbor.prev = current
                current.next = neighbor

        return path

    def backtrack(self, cell):
        backtracked = []
        while True:
            if cell.prev is None:
                return backtracked
            backtracked.append(cell.prev)
            neighbors = self.get_neighbors(cell.prev)
            for neighbor in neighbors:
                if neighbor.val == 0:
                    return backtracked
            cell = cell.prev

    def get_np_map(self, map_=None):
        if map_ is None:
            map_ = self.start_map
        np_map = np.zeros((self.rows, self.cols))
        for i in range(self.rows):
            for j in range(self.cols):
                np_map[i, j] = map_[i][j].val
        return np_map

    def convert_path(self):
        path = []
        for cell in self.path:
            path.append((cell.row, cell.col))
        return path

    def plot_path(self):
        start_map = self.start_np_map * 255
        start_map = cv2.merge((start_map, start_map, start_map))
        start_map[self.start[0], self.start[1], 0] = 200

        vid_name = f"{self.map_name.split('.')[0]}{uuid.uuid1()}.avi"

        out = cv2.VideoWriter(vid_name, cv2.VideoWriter_fourcc(*'DIVX'), 60, (500, 500))
        out.write(cv2.resize(start_map, (500, 500), interpolation=cv2.INTER_AREA))
        temp = np.copy(start_map)
        path = self.convert_path()

        for i in tqdm(range(1, len(path))):
            coord = path[i]
        # for i, coord in enumerate(path, start=1):
            temp = np.copy(temp)
            color = temp[coord[0], coord[1], 2]
            if color > 0:
                temp[coord[0], coord[1], 1] += 200
            else:
                temp[coord[0], coord[1], 2] += 150
            out.write(cv2.resize(temp, (500, 500), interpolation=cv2.INTER_AREA))
        out.release()


def print_cells(cells):
    for cell in cells:
        print(f"({cell.row},{cell.col})", end=" ")
    print()


def print_map(map_):
    for _ in range(2):
        print("*")
    for row in map_:
        for val in row:
            print(val, end="   ")
        print()
    print("*")


def print_help():
    print()
    print("\tpython searcher.py [--map MAP] [--start START] [--vid VID] [--help | -h]")
    print()
    print("\t\t--map:\t\tpath to map image, default is maps/map2_100_i.png")
    print("\t\t--start:\tstart position <row,col>, default is randomly generated")
    print("\t\t--vid:\t\tboolean for video output, default is False")
    print()


if __name__ == '__main__':
    import sys
    MAP = "maps/map2_125_i.png"
    START = None
    VID = False

    # lazy argument parser
    if "-h" in sys.argv or "--help" in sys.argv:
        print_help()
        sys.exit()

    for i in range(1, len(sys.argv), 2):
        if sys.argv[i] == "--map":
            MAP = sys.argv[i + 1]
        elif sys.argv[i] == "--start":
            START = sys.argv[i + 1].split(",")
            START = (int(START[0]), int(START[1]))
        elif sys.argv[i] == "--vid":
            VID = sys.argv[i + 1] == "True"

    BacktrackSearch(map_name=MAP, start=START, vid=VID)
