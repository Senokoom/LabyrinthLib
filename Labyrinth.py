from Algorithms.HuntAndKill import HuntAndKill
from Algorithms.Prims import Prims
from Algorithms.RecursiveBacktracker import RecursiveBacktracker
from Cell import Cell
from hashlib import sha256
import random as rnd
from copy import deepcopy

class Labyrinth:
    def __init__(self, size: int | tuple, seed: str | int = None, start_pos: tuple = None, end_pos: tuple = None):
        """
        Creates a Labyrinth object with given size and seed.
        :param size: can be tuple or integer. Sets the size of your labyrinth. Example: (2,3) | 3
        :param seed: Has to be str or int. Sets the seed for your labyrinth. Labyrinth generated with the same seed and algorithm will be the same. . If not inputted will be randomly generated
        :param start_pos Has to be a tuple(int). (column, row). Start position of you labyrinth. Must be in size range (from 0 to size-1). If not inputted will be randomly generated
        :param end_pos Has to be a tuple(int). (column, row). End position of you labyrinth. Must be in size range (from 0 to size-1). If not inputted will be randomly generated
        """
        self.width = 0
        self.height = 0
        self.size_list = []

        self.HashedSeed = sha256(str(seed).encode("utf-8") if seed else str(rnd.randint(1000000, 99999999)).encode()).hexdigest()
        # print(self.HashedSeed)
        self.seedRandom = rnd.Random(self.HashedSeed)

        if isinstance(size, int):
            self.width = self.height = size
        elif isinstance(size, tuple) or isinstance(size, list):
            if len(size) == 2:
                self.width, self.height = tuple(map(int, size))
            elif len(size) == 1:
                self.width = self.height = size[0]
        # print(self.width, self.height)
        self.cells_labyrinth = [[Cell(x, y) for x in range(self.width)] for y in range(self.height)]
        # print(self.cells_labyrinth)
        self.start_pos = start_pos if start_pos else (self.seedRandom.randint(0, self.width-1), self.seedRandom.randint(0, self.height-1))
        self.end_pos = end_pos if end_pos else (self.seedRandom.randint(0, self.width-1), self.seedRandom.randint(0, self.height-1))

    def recursive_backtracker(self):
        return RecursiveBacktracker(self.seedRandom, deepcopy(self.cells_labyrinth), (self.width,self.height)).labyrinth

    def hunt_and_kill(self):
        return HuntAndKill(self.seedRandom, deepcopy(self.cells_labyrinth), (self.width,self.height)).labyrinth

    def prims(self):
        return Prims(self.seedRandom, deepcopy(self.cells_labyrinth), (self.width,self.height)).labyrinth

    def to_dense_matrix(self):
        dense_matrix = [["|" for _ in range(self.width*2+1)] for _ in range(self.height*2+1)]
        for i in range(len(dense_matrix)):
            for j in range(len(dense_matrix[i])):
                if i % 2 == 0 and j % 2 == 0:
                    dense_matrix[i][j] = "+"
                elif i % 2 == 0 and j % 2 == 1:
                    dense_matrix[i][j] = "-"
                elif i % 2 == 1 and j % 2 == 0:
                    dense_matrix[i][j] = "|"
                else:
                    dense_matrix[i][j] = "#"
        return dense_matrix

    def to_ascii(self, labyrinth: list[list[Cell]]) -> str:
        ascii_matrix = self.to_dense_matrix()
        ascii_lab = ""
        for i in range(self.height):
            for j in range(self.width):
                ascii_matrix[i*2+1][j*2+1] = " "
                if not ("E" in labyrinth[i][j].walls):
                    ascii_matrix[i*2+1][j*2+2] = " "
                if not ("W" in labyrinth[i][j].walls):
                    ascii_matrix[i*2+1][j*2] = " "
                if not ("N" in labyrinth[i][j].walls):
                    ascii_matrix[i*2][j*2+1] = " "
                if not ("S" in labyrinth[i][j].walls):
                    ascii_matrix[i*2+2][j*2+1] = " "
        for row in ascii_matrix:
            for cell in row:
                ascii_lab += cell
            ascii_lab += '\n'
        return ascii_lab


    def __str__(self) -> str:
        result = ''
        for row in self.cells_labyrinth:
            for cell in row:
                result += str(cell)
            result += '\n'
        return result


l = Labyrinth((10,10), 10)
print(l.to_ascii(l.recursive_backtracker()))
print(l.to_ascii(l.hunt_and_kill()))
print(l.to_ascii(l.prims()))
