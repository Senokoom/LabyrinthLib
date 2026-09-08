class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walls = ['N', 'S', 'E', 'W']
        self.visited = False
        self.is_start = False
        self.is_finish = False

    def __str__(self) -> str:
        final_str = ''
        for x in self.walls:
            final_str += str(x)
        return final_str + " "