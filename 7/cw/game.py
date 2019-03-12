"""
Class representing the gameplay.

@author Krisztian Balog
"""

from board import Board
from datetime import datetime, timedelta


class Game():
    BOARD_SIZE = 7
    TIMEOUT = 3  # timeout in seconds; change it to -1 for no timeout

    STATUS = {  # status codes and their meanings
        100: "The game has not started yet (waiting for both players)",
        101: "The game has not started yet (waiting for the second player)",
        201: "It's Player 1's turn",
        202: "It's Player 2's turn",
        301: "The game has finished, Player 1 won",
        302: "The game has finished, Player 2 won",
        401: "The game has ended because of an illegal move by Player 1",
        402: "The game has ended because of an illegal move by Player 2",
        501: "The game has ended because of time-out by Player 1",
        502: "The game has ended because of time-out by Player 2"
    }

    def __init__(self):
        self.__players = []  # names of players
        self.__status = 100  # status of the game
        self.__board = Board()
        self.__last_move = ""
        self.__player = 1  # whose turn it is (1 or 2)
        self.__time_next_move = None

    def get_status_code(self):
        """Returns the status code of the game."""
        return self.__status

    def get_status(self):
        """Returns the full game status."""
        time_left = self.__time_left()
        return {
            "status_code": self.__status,
            "status": self.STATUS[self.__status],
            "score_1": self.__board.get_colored()[0],
            "score_2": self.__board.get_colored()[1],
            "board_size": self.BOARD_SIZE,
            "board": self.__board.get_board(),
            "time_left": time_left,
            "last_move": self.__last_move
        }

    def get_player(self, name):
        """Return the player no (1 or 2) for a given name or -1 if not exist."""
        try:
            return self.__players.index(name) + 1
        except ValueError:
            return -1

    def get_next_player(self):
        """Returns which player moves next."""
        return self.__player

    def add_player(self, name):
        """Adds a new player and returns whether it is player 1 or 2."""
        if len(self.__players) < 2:
            self.__players.append(name)
            if len(self.__players) == 2:  # let the game start
                self.__turn()
            else:
                self.__status = 101
            return len(self.__players)

    def __time_left(self):
        """Returns the time left for the given move and triggers the timeout (if applicable)."""
        if self.__time_next_move is not None and self.TIMEOUT > 0:
            timeleft = round((self.__time_next_move - datetime.now()).total_seconds() * 1000)
            if timeleft < 0:
                self.__status = 500 + self.__player
            else:
                return timeleft
        return 0

    def __turn(self):
        """It's the next player's turn."""
        if self.__status < 200:  # the game is just getting started
            self.__status = 201
        elif self.__status > 300:  # the game has already ended
            pass
        else:
            scores = self.__board.get_colored()
            # check if the game has finished
            if sum(scores) == self.BOARD_SIZE ** 2:
                winner = 1 if scores[0] > scores[1] else 2
                self.__status = 300 + winner
            else:
                self.__player = 3 - self.__player  # it's the other player's turn (1 => 2, 2 => 1)
                self.__status = 200 + self.__player
                if self.TIMEOUT > 0:  # reset timer
                    self.__time_next_move = datetime.now() + timedelta(seconds=self.TIMEOUT)

    def invalid_move(self, player):
        """Ends the game with invalid move."""
        self.__status = 400 + player

    def move(self, x, y, border):
        """Makes a move."""
        if self.__board.is_occupied(x, y) or self.__board.has_border(x, y, border):
            self.invalid_move(self.__player)
        else:
            if self.__time_left() >= 0:
                self.__board.add_border(x, y, border, self.__player)
                self.__last_move = ",".join([str(x), str(y), border])  # save the last valid move in x,y,side format
                self.__turn()
