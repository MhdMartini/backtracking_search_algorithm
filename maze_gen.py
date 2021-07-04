import numpy as np
import random
import uuid


class MazeGen:
    def __init__(self, width=50):
        # width is the side length of the square maze.
        # num is the number of explorable cells
        self.width = width
        self.map = np.ones((width, width))
        self.directions = ((0, 1), (0, -1), (1, 0), (-1, 0))

    def get_neighbors(self, pos):
        # look through the neighbors and return them if any
        neighbors = []
        r, c = pos
        for direction in self.directions:
            dr, dc = direction
            candidate_row = r + dr
            candidate_col = c + dc
            candidate_neigh = (candidate_row, candidate_col)
            if self.is_neighbor(candidate_neigh):
                neighbors.append(candidate_neigh)
        return neighbors

    def is_neighbor(self, pos):
        r, c = pos
        return not (r < 0 or r >= self.width or c < 0 or c >= self.width)

    def is_valid(self, pos):
        # a neighbor is valid if it is not a cell, and it is not surrounded by more than one cell
        r, c = pos
        if self.map[r, c] == 0:
            return False
        neighbors = self.get_neighbors(pos)
        num_cells = 0
        for neighbor in neighbors:
            if self.map[neighbor[0], neighbor[1]] == 0:
                num_cells += 1
        if num_cells <= 1:
            return True

    def maze_gen(self, start=None):
        if start is None:
            start = (random.choice(range(self.width)), random.choice(range(self.width)))
        self.map[start[0], start[1]] = 0

        neighbors = self.get_neighbors(start)
        if not neighbors:
            return

        for neighbor in random.sample(neighbors, len(neighbors)):
            if not self.is_valid(neighbor):
                continue
            if not self.maze_gen(neighbor):
                return True


def print_help():
    print()
    print("\tpython maze_gen.py [--width WIDTH] [--help | -h]")
    print()
    print("\t\t--width:\twidth of square maze, default is 75")
    print()


if __name__ == '__main__':
    import cv2
    import sys
    WIDTH = 75  # 50 x 50 map

    # lazy argument parser
    if "-h" in sys.argv or "--help" in sys.argv:
        print_help()
        sys.exit()

    for i in range(1, len(sys.argv), 2):
        if sys.argv[i] == "--width":
            WIDTH = int(sys.argv[i + 1])

    maze = MazeGen(width=WIDTH)
    try:
        maze.maze_gen()
    except Exception as e:
        print(e)
    finally:
        maze_name = f"maps/" + str(uuid.uuid1()) + ".png"
        cv2.imwrite(maze_name, maze.map * 255)
