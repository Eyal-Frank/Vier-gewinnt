#!/usr/bin/env python3
from itertools import groupby, chain

NONE = '.'
RED = 'R'
YELLOW = 'Y'

# ANSI escape codes for colors
RED_COLOR = '\033[91m'
YELLOW_COLOR = '\033[93m'
RESET_COLOR = '\033[0m'

def diagonalsPos(matrix, cols, rows):
    """Get positive diagonals, going from bottom-left to top-right."""
    for di in ([(j, i - j) for j in range(cols)] for i in range(cols + rows - 1)):
        yield [matrix[i][j] for i, j in di if 0 <= i < cols and 0 <= j < rows]

def diagonalsNeg(matrix, cols, rows):
    """Get negative diagonals, going from top-left to bottom-right."""
    for di in ([(j, i - cols + j + 1) for j in range(cols)] for i in range(cols + rows - 1)):
        yield [matrix[i][j] for i, j in di if 0 <= i < cols and 0 <= j < rows]

class Game:
    def __init__(self, cols=7, rows=6, requiredToWin=4):
        """Create a new game."""
        self.cols = cols
        self.rows = rows
        self.win = requiredToWin
        self.board = [[NONE] * rows for _ in range(cols)]

    def reset(self):
        """Reset the game board."""
        self.board = [[NONE] * self.rows for _ in range(self.cols)]

    def insert(self, column, color):
        """Insert the color in the given column."""
        c = self.board[column]
        if c[0] != NONE:
            raise Exception('Column is full')

        i = -1
        while c[i] != NONE:
            i -= 1
        c[i] = color

        self.checkForWin()

    def checkForWin(self):
        """Check the current board for a winner."""
        w = self.getWinner()
        if w:
            self.printBoard()
            raise Exception(w + ' won!')

    def getWinner(self):
        """Get the winner on the current board."""
        lines = (
            self.board,  # columns
            zip(*self.board),  # rows
            diagonalsPos(self.board, self.cols, self.rows),  # positive diagonals
            diagonalsNeg(self.board, self.cols, self.rows)  # negative diagonals
        )

        for line in chain(*lines):
            for color, group in groupby(line):
                if color != NONE and len(list(group)) >= self.win:
                    return color

    def printBoard(self):
        """Print the board."""
        print('  '.join(map(str, range(self.cols))))
        for y in range(self.rows):
            print('  '.join(self.colorize(self.board[x][y]) for x in range(self.cols)))
        print()

    def colorize(self, cell):
        """Colorize the cell based on its content."""
        if cell == RED:
            return f'{RED_COLOR}{cell}{RESET_COLOR}'
        elif cell == YELLOW:
            return f'{YELLOW_COLOR}{cell}{RESET_COLOR}'
        else:
            return cell

if __name__ == '__main__':
    g = Game()
    turn = RED
    while True:
        g.printBoard()
        row = input('{}\'s turn (Enter column number or R to reset): '.format('Red' if turn == RED else 'Yellow'))
        if row.lower() == 'r':
            g.reset()
            turn = RED
            print("Game has been reset.")
            continue
        try:
            g.insert(int(row), turn)
            turn = YELLOW if turn == RED else RED
        except Exception as e:
            print(e)
