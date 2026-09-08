from Cell import Cell


class Utilz:
    def __init__(self):
        pass

    @classmethod
    def get_all_adjacent_visited_cells(cls, labyrinth, current_cell: Cell, width, height):
        x, y = current_cell.x, current_cell.y
        adjacent_cells_not_visited = []
        if x < width - 1:
            if labyrinth[y][x + 1].visited:
                adjacent_cells_not_visited.append(labyrinth[y][x + 1])
        if x != 0:
            if labyrinth[y][x - 1].visited:
                adjacent_cells_not_visited.append(labyrinth[y][x - 1])
        if y < height - 1:
            if labyrinth[y + 1][x].visited:
                adjacent_cells_not_visited.append(labyrinth[y + 1][x])
        if y != 0:
            if labyrinth[y - 1][x].visited:
                adjacent_cells_not_visited.append(labyrinth[y - 1][x])
        # print(adjacent_cells_not_visited)
        return adjacent_cells_not_visited


    @classmethod
    def get_all_adjacent_not_visited_cells(cls, labyrinth, current_cell: Cell, width, height):
        x,y = current_cell.x, current_cell.y
        adjacent_cells_not_visited = []
        if x < width-1:
            if not labyrinth[y][x + 1].visited:
                adjacent_cells_not_visited.append(labyrinth[y][x + 1])
        if x != 0:
            if not labyrinth[y][x - 1].visited:
                adjacent_cells_not_visited.append(labyrinth[y][x - 1])
        if y < height-1:
            if not labyrinth[y+1][x].visited:
                adjacent_cells_not_visited.append(labyrinth[y + 1][x])
        if y != 0:
            if not labyrinth[y-1][x].visited:
                adjacent_cells_not_visited.append(labyrinth[y - 1][x])
        # print(adjacent_cells_not_visited)
        return adjacent_cells_not_visited

    @classmethod
    def destroy_wall(cls, current_cell: Cell, next_cell: Cell):
        result_x = current_cell.x - next_cell.x
        result_y = current_cell.y - next_cell.y

        #print(current_cell.x, current_cell.y, next_cell.x, next_cell.y)
        #
        # string = ''
        # for row in self.labyrinth:
        #     for cell in row:
        #         string += str(cell)
        #     string += '\n'
        # print(string)

        match result_x:
            case 1:
                current_cell.walls.remove("W")
                next_cell.walls.remove("E")
                return
            case -1:
                current_cell.walls.remove("E")
                next_cell.walls.remove("W")
                return
            case _:
                pass
        match result_y:
            case 1:
                current_cell.walls.remove("N")
                next_cell.walls.remove("S")
                return
            case -1:
                current_cell.walls.remove("S")
                next_cell.walls.remove("N")
                return
            case _:
                pass
        return