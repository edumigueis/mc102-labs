import sys


class PGM:
    """Class responsible for representing a PGM file and contain its operations"""

    def __init__(self, header: str, max_pixel: str, matrix: list[list[int]]):
        self.header = header
        self.max_pixel = max_pixel
        self.matrix = matrix
        self.size = (len(matrix), len(matrix[0]))

    def __find_connected_regions(self, tolerance: int,
                                 pos: tuple[int, int],
                                 ignore=-1) -> list[tuple[int, int]]:
        """Finds an entire connected region given a seed and returns it in a position array"""
        rows = len(self.matrix)
        cols = len(self.matrix[0])
        visited = [[False] * cols for _ in range(rows)]
        connected_region = []

        def get_next_connected_pos(row: int, col: int):
            if (row < 0 or row >= rows
                    or col < 0 or col >= cols) or visited[row][col]:
                return
            diff = abs(self.matrix[row][col] - self.matrix[pos[0]][pos[1]])
            if ignore != self.matrix[row][col] and diff <= tolerance:
                visited[row][col] = True
                connected_region.append((row, col))
                # Up, down, left, right
                get_next_connected_pos(row - 1, col)
                get_next_connected_pos(row + 1, col)
                get_next_connected_pos(row, col - 1)
                get_next_connected_pos(row, col + 1)
                # Diagonals
                get_next_connected_pos(row - 1, col - 1)
                get_next_connected_pos(row - 1, col + 1)
                get_next_connected_pos(row + 1, col - 1)
                get_next_connected_pos(row + 1, col + 1)

        get_next_connected_pos(pos[0], pos[1])

        return connected_region

    """All functions are derivatives from the connected areas logic"""

    def bucket(self, c: int, t: int, pos: tuple[int, int]) -> None:
        for coord in self.__find_connected_regions(t, pos, c):
            self.matrix[coord[0]][coord[1]] = c

    def negative(self, t: int, pos: tuple[int, int]) -> None:
        for coord in self.__find_connected_regions(t, pos):
            self.matrix[coord[0]][coord[1]] = 255 - \
                self.matrix[coord[0]][coord[1]]

    def cmask(self, t: int, pos: tuple[int, int]) -> None:
        con_reg = self.__find_connected_regions(t, pos)
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[0])):
                if (i, j) in con_reg:
                    self.matrix[i][j] = 0
                else:
                    self.matrix[i][j] = 255


class PGMFileUtil:
    """Class to deal with PGM files in relation to the PGM class"""
    @staticmethod
    def read_file(file_path: str) -> PGM:
        try:
            with open(file_path, 'r') as file:
                data = [line.strip()
                        for line in file.readlines() if line.strip()]
            size = int(data[2].split(" ")[1])
            return PGM(data[1], data[3], [list(map(int, row.split()))
                                          for row in data[-size:]])
        except IOError:
            print("Error reading data from:", file_path)
            return None

    @staticmethod
    def save_to_file(pgm: PGM, file_path: str) -> None:
        try:
            data = f"P2\n{pgm.header}\n{pgm.size[1]} {pgm.size[0]}\n{pgm.max_pixel}\n"
            data += '\n'.join([' '.join(map(str, row)) for row in pgm.matrix])
            with open(file_path, 'w') as file:
                file.write(data)
        except IOError:
            print("Error saving data to:", file_path)


def main():
    sys.setrecursionlimit(16385)
    pgm = PGMFileUtil.read_file(input())
    n = int(input())
    for _ in range(n):
        op = input().split(" ")
        match op[0]:
            case "bucket":
                pgm.bucket(int(op[1]), int(op[2]), (int(op[4]), int(op[3])))
            case "negative":
                pgm.negative(int(op[1]), (int(op[3]), int(op[2])))
            case "cmask":
                pgm.cmask(int(op[1]), (int(op[3]), int(op[2])))
            case "save":
                pgm.header = "# Imagem criada pelo lab13"
                PGMFileUtil.save_to_file(pgm, op[1])


if __name__ == "__main__":
    main()
