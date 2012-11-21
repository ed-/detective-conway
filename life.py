from cell import Cell

def neighborhood(row, column):
    return [(row - 1, column - 1),
            (row - 1, column),
            (row - 1, column + 1),
            (row, column - 1),
            (row, column + 1),
            (row + 1, column - 1),
            (row + 1, column),
            (row + 1, column + 1)]

class Life(object):
    width = 0
    height = 0
    board = None

    def __init__(self, width, height, data=None):
        self.width = width
        self.height = height
        self.board = [[Cell(0)
                        for c in range(width)]
                       for r in range(height)]
        if data:
            self.load(data)

    def __str__(self):
        return '\n'.join([' '.join(['#' if cell.state == 1 else '.'
                                    for cell in row]) for row in self.board])

    def __dict__(self):
        return {'width': self.width,
                'height': self.height,
                'cells': [cell.state for row in self.board for cell in row]
               }

    def clone(self):
        data = [cell.state for row in self.board for cell in row]
        return Life(self.width, self.height, data)

    def diff(self, other):
        z = 0
        for r in range(self.height):
            for c in range(self.width):
                a = self.board[r][c].state
                b = other.board[r][c].state
                if a != b:
                    z += 1
        return z
            
    def load(self, data):
        row, column = 0, 0
        for d in data:
            state = 1 if bool(d) else 0
            self.board[row][column].prep(state)
            self.board[row][column].tick()
            column += 1
            if column >= self.width:
                column = 0
                row += 1
            if row >= self.height:
                break

    def dump(self):
        return [cell.state for row in self.board for cell in row]

    def state_at(self, row, column):
        if row < 0 or row >= self.height:
            return 0
        if column < 0 or column >= self.width:
            return 0
        return self.board[row][column].state

    def tick(self):
        for r, row in enumerate(self.board):
            for c, cell in enumerate(row):
                current = self.state_at(r, c)
                neighbors = [self.state_at(nr, rc) for (nr, rc) in
                             neighborhood(r, c)]
                living = len([n for n in neighbors if n == 1])
                if (cell.state == 1):
                    if living < 2:
                        cell.prep(0)
                    elif living in [2, 3]:
                        cell.prep(1)
                    else:
                        cell.prep(0)
                else:
                    if living == 3:
                        cell.prep(1)
                    else:
                        cell.prep(0)
        for row in self.board:
            for cell in row:
                cell.tick()
