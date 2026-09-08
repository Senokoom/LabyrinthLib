from random import Random
from Cell import Cell
from utilz import Utilz

class HuntAndKill:
    def __init__(self, _rnd: Random, labyrinth: list[list[Cell]], size: tuple):
        self._rnd = _rnd
        self.labyrinth = labyrinth
        self.width, self.height = size
        first_cell = self._rnd.choice(self._rnd.choice(self.labyrinth))
        first_cell.visited = True
        self.generate(first_cell)

    def generate(self, current_cell: Cell):
        while self.not_visited():
            while True:
                if adjacent_cells := Utilz.get_all_adjacent_not_visited_cells(self.labyrinth, current_cell, self.width, self.height):
                    next_cell: Cell = self._rnd.choice(adjacent_cells)
                    Utilz.destroy_wall(current_cell, next_cell)
                    next_cell.visited = True
                    current_cell = next_cell
                else:
                    break
            current_cell = self.hunt()
            if current_cell:
                adjacent_visited_cells = Utilz.get_all_adjacent_visited_cells(self.labyrinth, current_cell, self.width, self.height)
                adjacent_visited_cell: Cell = self._rnd.choice(adjacent_visited_cells)
                Utilz.destroy_wall(current_cell, adjacent_visited_cell)
                current_cell.visited = True
            else:
                break
        return self.labyrinth

    def not_visited(self):
        for row in self.labyrinth:
            for cell in row:
                if not cell.visited:
                    return True
        return False



    def generate_recursion(self, current_cell: Cell):
        if not current_cell.visited:
            current_cell.visited = True
        adjacent_cells = Utilz.get_all_adjacent_not_visited_cells(self.labyrinth, current_cell, self.width, self.height)
        if adjacent_cells:
            next_cell = self._rnd.choice(adjacent_cells)
            Utilz.destroy_wall(current_cell, next_cell)
            return self.generate(next_cell)
        else:
            next_cell = self.hunt()
            if next_cell:
                return self.generate(next_cell)
            else:
                return self.labyrinth

    def hunt(self)->Cell|None:
        for row in self.labyrinth:
            for cell in row:
                if not cell.visited and Utilz.get_all_adjacent_visited_cells(self.labyrinth, cell, self.width, self.height):
                    return cell
        return None