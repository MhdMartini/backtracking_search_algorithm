import numpy as np


class ShortestPath:
    def __init__(self, map_=None, start=None, destination=None):
        self.map = np.copy(map_)
        self.start = start
        self.destination = destination
        self.rows, self.cols = map_.shape
        self.que = [self.start]

        # print(self.map)
        # print()

        self.flood_fill()
        self.shortest_path = self.get_shortest_path()

    def get_neighbors(self, point, val=0):
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        r, c = point
        neighbors = []
        for direction in directions:
            dr, dc = direction
            candidate_row = r + dr
            candidate_col = c + dc
            if candidate_row < 0 or candidate_row >= self.rows:
                continue
            if candidate_col < 0 or candidate_col >= self.cols:
                continue
            if self.map[candidate_row, candidate_col] != val:
                continue
            # if self.map[candidate_row, candidate_col] == np.inf:
            #     continue
            neighbors.append((candidate_row, candidate_col))
        return neighbors

    def flood_fill(self):
        rank = 1
        self.map[self.start[0], self.start[1]] = rank
        while True:
            rank += 1
            for i in range(len(self.que)):
                current = self.que.pop(0)
                neighbors = self.get_neighbors(current)
                if not neighbors:
                    continue

                for neighbor in neighbors:
                    self.map[neighbor[0], neighbor[1]] = rank
                    self.que.append(neighbor)
                    if neighbor == self.destination:
                        # print(self.map)
                        return

    def get_shortest_path(self):
        # Given flood-filled self.map return the coordinates from source to destination
        path = []
        index = self.destination
        while True:
            val = self.map[index[0], index[1]]
            val = int(val)

            neighbors = self.get_neighbors(index, val - 1)
            for neighbor in neighbors:
                path.append(neighbor)
                index = neighbor
                break
            # print(val)
            if val == 1:
                path = path[::-1]
                path.append(self.destination)
                return path


if __name__ == '__main__':
    MAP = np.array([
        [0, 0, 0, 0, np.inf],
        [0, 0, np.inf, np.inf, 0],
        [0, 0, 0, 0, 0],
        [0, 0, np.inf, 0, 0],
        [np.inf, np.inf, 0, 0, 0],
    ])
    start = (0, 0)
    destination = (1, 4)
    path = ShortestPath(map_=MAP, start=start, destination=destination).shortest_path
    print(path)
