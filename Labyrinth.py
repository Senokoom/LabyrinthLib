from Algorithms.HuntAndKill import HuntAndKill
from Algorithms.Prims import Prims
from Algorithms.RecursiveBacktracker import RecursiveBacktracker
from Cell import Cell
from hashlib import sha256
import random as rnd
from copy import deepcopy
from PIL import Image, ImageDraw
import datetime


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

        self.start_pos = start_pos
        self.end_pos = end_pos

        if not start_pos or not(self.width-1 >= start_pos[0] >= 0 and self.height-1 >= start_pos[1] >= 0):
            start_pos = (self.seedRandom.randint(0, self.width), self.seedRandom.randint(0, self.height))
        if not end_pos or not(self.width - 1 >= end_pos[0] >= 0 and self.height - 1 >= end_pos[1] >= 0):
            end_pos = (self.seedRandom.randint(0, self.width), self.seedRandom.randint(0, self.height))

        self.cells_labyrinth = [[Cell(x, y) for x in range(self.width)] for y in range(self.height)]
        self.cells_labyrinth[start_pos[1]][start_pos[0]].is_start = True
        self.cells_labyrinth[end_pos[1]][end_pos[0]].is_finish = True


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

    def to_png(self, labyrinth,filename, cell_size=20, wall_thickness=5):
        # 1. Считаем реальный размер картинки
        step = cell_size + wall_thickness

        offset = 6

        width_px = self.width * step + wall_thickness + offset*2
        height_px = self.height * step + wall_thickness + offset*2

        # 2. Создаем белый холст
        image = Image.new('RGB', (width_px, height_px), 'white')
        draw = ImageDraw.Draw(image)

        # print(labyrinth)

        # 3. Рисуем стены
        for y in range(self.height):
            for x in range(self.width):
                cell = labyrinth[y][x]
                # Координаты начала клетки
                start_x = wall_thickness + x * step
                start_y = wall_thickness + y * step

                # Координаты конца клетки
                end_x = start_x + cell_size+offset
                end_y = start_y + cell_size+offset

                if cell.is_start:
                    draw.rectangle([(start_x, start_y), (end_x, start_y+cell_size+offset)], 'lime')
                if cell.is_finish:
                    draw.rectangle([(start_x, start_y), (end_x, start_y+cell_size+offset)], 'gold')


                # --- Рисуем Северную стену (верх) ---
                if "N" in cell.walls:
                    # Линия от левого верха до правого верха клетки
                    draw.line([(start_x, start_y), (end_x, start_y)], fill='black', width=wall_thickness)

                # --- Рисуем Западную стену (слева) ---
                if "W" in cell.walls:
                    # Линия от левого верха до левого низа клетки
                    draw.line([(start_x, start_y), (start_x, end_y)], fill='black', width=wall_thickness)

                # --- Рисуем Восточную стену (справа) ---
                # Важно: рисуем её только если это последняя колонка,
                # иначе она продублируется со стеной "W" соседней клетки справа.
                if "E" in cell.walls and x == self.width - 1:
                    draw.line([(end_x, start_y), (end_x, end_y)], fill='black', width=wall_thickness)

                # --- Рисуем Южную стену (снизу) ---
                # Важно: рисуем её только если это последняя строка,
                # иначе она продублируется со стеной "N" соседней клетки снизу.
                if "S" in cell.walls and y == self.height - 1:
                    draw.line([(start_x, end_y), (end_x, end_y)], fill='black', width=wall_thickness)
        image.save(f"{filename}.png")



    def __str__(self) -> str:
        result = ''
        for row in self.cells_labyrinth:
            for cell in row:
                result += str(cell)
            result += '\n'
        return result


l = Labyrinth((100,10))
# print(l.to_ascii(l.recursive_backtracker()))
# print(l.to_ascii(l.hunt_and_kill()))
# print(l.to_ascii(l.prims()))
l.to_png(l.hunt_and_kill(), f"C:/Users/levak/PycharmProjects/LabyrinthLib/pictures/{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") }")
