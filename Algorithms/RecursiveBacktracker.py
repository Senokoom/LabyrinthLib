from types import CellType
from Cell import Cell
from random import Random
from utilz import Utilz

class RecursiveBacktracker:
    def __init__(self, _rnd: Random, labyrinth: list[list[Cell]], size: tuple):
        self._rnd = _rnd
        self.labyrinth = labyrinth
        self.width, self.height = size
        first_cell = self._rnd.choice(self._rnd.choice(self.labyrinth))
        self.stack = []
        self.stack.append(first_cell)
        self.generate(first_cell)

    def generate(self, current_cell: Cell):
        while len(self.stack) != 0:
            current_cell = self.stack[-1]
            adjacent_cells = Utilz.get_all_adjacent_not_visited_cells(self.labyrinth, current_cell, self.width, self.height)
            if adjacent_cells:
                next_cell = self._rnd.choice(adjacent_cells)
                Utilz.destroy_wall(current_cell, next_cell)
                next_cell.visited = True
                self.stack.append(next_cell)
            else:
                self.stack.pop()
        return self.labyrinth


    def generate_recursion(self, current_cell: Cell):
        if not current_cell.visited:
            self.stack.append(current_cell)
        current_cell.visited = True
        adjacent_cells = Utilz.get_all_adjacent_not_visited_cells(self.labyrinth, current_cell, self.width, self.height)
        if adjacent_cells:
            next_cell = self._rnd.choice(adjacent_cells)
            Utilz.destroy_wall(current_cell, next_cell)
            return self.generate(next_cell)
        else:
            if self.stack:
                return self.generate(self.stack.pop())
            else:
                return self.labyrinth

