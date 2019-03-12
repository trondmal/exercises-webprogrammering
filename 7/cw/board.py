"""
Class representing the board.

@author Krisztian Balog
"""


class Board():
    BORDERS = {"top": 1, "right": 2, "bottom": 4, "left": 8}

    def __init__(self, size=7):
        self.__size = size
        # init board
        self.__board = []  # indexed as [y][x], that is, row then column
        for i in range(size):
            self.__board.append([0] * size)
        # how many colored squares each player has
        self.__colored = [0, 0]

    def has_border(self, x, y, border):
        """Checks if the square has a given border"""
        return self.__board[y][x] & self.BORDERS[border]

    def add_border(self, x, y, border, player):
        """Adds border to a given side."""
        self.__board[y][x] += self.BORDERS[border]
        self.__occupy(x, y, player)
        # also add border to the neighboring square
        if border == "top":
            if y > 0:
                self.__board[y - 1][x] += self.BORDERS["bottom"]
                self.__occupy(x, y - 1, player)
        elif border == "right":
            if x < self.__size - 1:
                self.__board[y][x + 1] += self.BORDERS["left"]
                self.__occupy(x + 1, y, player)
        elif border == "bottom":
            if y < self.__size - 1:
                self.__board[y + 1][x] += self.BORDERS["top"]
                self.__occupy(x, y + 1, player)
        elif border == "left":
            if x > 0:
                self.__board[y][x - 1] += self.BORDERS["right"]
                self.__occupy(x - 1, y, player)

    def __occupy(self, x, y, player):
        """Checks if a new area will get occupied by the given player."""
        queue = [(x, y)]
        area = []
        closed = True
        while closed and len(queue) > 0:
            (x, y) = queue.pop(0)
            if (x, y) in area:
                continue
            area.append((x, y))
            #print("Q: ", queue)
            #print("A: ", area)
            # try to extend in possible directions
            if not self.has_border(x, y, "top"):
                if y == 0:  # leaving the board
                    closed = False
                queue.append((x, y - 1))
            if not self.has_border(x, y, "right"):
                if x == self.__size - 1:  # leaving the board
                    closed = False
                queue.append((x + 1, y))
            if not self.has_border(x, y, "bottom"):
                if y == self.__size - 1:  # leaving the board
                    closed = False
                queue.append((x, y + 1))
            if not self.has_border(x, y, "left"):
                if x == 0:  # leaving the board
                    closed = False
                queue.append((x - 1, y))

        if closed:  # closed area => occupy it by player
            for (x, y) in area:
                self.__board[y][x] += player * 16
                self.__colored[player - 1] += 1

    def is_occupied(self, x, y):
        """Checks if a given square is occupied. 0: no, 1: player1, 2: player2."""
        return (self.__board[y][x] & 16) + (self.__board[y][x] & 32) * 2

    def get_size(self):
        return self.__size

    def get_board(self):
        return self.__board

    def get_colored(self):
        return self.__colored
