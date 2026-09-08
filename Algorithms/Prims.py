# Алгоритм:
# Выбираешь случайную стартовую клетку, помечаешь как посещённую
# Находишь всех её непосещённых соседей — это твой начальный "фронт"
# Пока фронт не пуст:
# Выбираешь случайную клетку из фронта
# Находишь у неё всех посещённых соседей
# Выбираешь одного из них случайно
# Убираешь стену между ними
# Помечаешь выбранную клетку как посещённую
# Добавляешь в фронт всех её непосещённых соседей (если их ещё нет во фронте)
from random import Random
from Cell import Cell
from utilz import Utilz


class Prims:
    def __init__(self, _rnd: Random, labyrinth: list[list[Cell]], size: tuple):
        self._rnd = _rnd
        self.labyrinth = labyrinth
        self.width, self.height = size
        first_cell = self._rnd.choice(self._rnd.choice(self.labyrinth))
        self.front = []
        first_cell.visited = True
        self.generate(first_cell)

    def generate(self, current_cell: Cell):
        for cell in Utilz.get_all_adjacent_not_visited_cells(self.labyrinth, current_cell, self.width, self.height):
            self.front.append(cell)
        while self.front:
            current_cell = self._rnd.choice(self.front)
            visited_adjacent_cells = Utilz.get_all_adjacent_visited_cells(self.labyrinth, current_cell, self.width, self.height)
            rnd_visited_cell = self._rnd.choice(visited_adjacent_cells)
            Utilz.destroy_wall(current_cell, rnd_visited_cell)
            current_cell.visited = True
            self.front.remove(current_cell)
            for cell in Utilz.get_all_adjacent_not_visited_cells(self.labyrinth, current_cell, self.width, self.height):
                if cell not in self.front:
                    self.front.append(cell)
        return self.labyrinth