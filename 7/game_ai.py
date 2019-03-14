"""
Game AI -- this is for you to complete
"""

import requests
import time
import random
import copy


SERVER = "http://127.0.0.1:5000"  # this will not change
TEAM_ID = "ErlendMoen"  # set it to your GitHub username

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

def greedyMove(board,player):
    
    max_score = [-1, -1, "", board.get_colored()[player-1]]
    legal_moves = []
    for x in range(7):
        for y in range(7):
            for border in ["top","right","bottom","left"]:
                if ((not board.has_border(x, y, border)) and (not board.is_occupied(x, y))):
                    
                    tempBoard = copy.deepcopy(board)
                    tempBoard.add_border(x, y, border, player)
                    if tempBoard.get_colored()[player-1] > max_score[3]:
                        print("updated max score: ", tempBoard.get_colored()[player-1])
                        max_score = [x, y, border, tempBoard.get_colored()[player-1]]
                    else:
                        
                        legal_moves.append([x, y, border])

    if max_score[3] == board.get_colored()[player-1]:
        i = random.randrange(len(legal_moves))
        print("index: ", i)
        m = legal_moves[i]
        board.add_border(m[0],m[1],m[2],player)
        print("Making a move: ({},{}) {}".format(m[0], m[1], m[2]))
        move = str(m[0]) + "," + str(m[1]) + "," + m[2]
        status = requests.get(SERVER + "/move/" + TEAM_ID + "/" + move).json()
    else:
        board.add_border(max_score[0],max_score[1],max_score[2],player)
        print("Making a move: ({},{}) {}".format(max_score[0], max_score[1], max_score[2]))
        move = str(max_score[0]) + "," + str(max_score[1]) + "," + max_score[2]
        status = requests.get(SERVER + "/move/" + TEAM_ID + "/" + move).json()

def deep(board, player, depth):
    if player == 1:
            next_player = 2

    elif player == 2:
        next_player = 1

    if depth <= 0:
        return board.get_colored()[0]-board.get_colored()[1]
    else:
        #max_score = [-1, -1, "", board.get_colored()[player-1]]
        max_score = board.get_colored()[0]-board.get_colored()[1]

        for x in range(7):
            for y in range(7):
                for border in ["top","right","bottom","left"]:
                    if ((not board.has_border(x, y, border)) and (not board.is_occupied(x, y))):
                    
                        tempBoard = copy.deepcopy(board)
                        tempBoard.add_border(x, y, border, next_player) # make move for "next" player
                        score = deep(tempBoard, next_player, depth-1) #calculate score for current player

                        if score > max_score:
                            max_score = score
        return max_score 

def deepMove(board,player,depth):
    max_score_move = [-1, -1, "", -1000] #x,y,border,score
    legal_moves =[]
    for x in range(7):
        for y in range(7):
            for border in ["top","right", "bottom", "left"]:
                if ((not board.has_border(x,y,border)) and (not board.is_occupied(x,y))):
                    tempBoard = copy.deepcopy(board)
                    tempBoard.add_border(x,y,border,player) # make move for current player
                    score = deep(tempBoard, player, depth) #calculate relative score of move recursively
                    if player == 2:
                        score *= -1
                    if score > max_score_move[3]:
                        max_score_move = [x,y,border,score]
                    else:
                        legal_moves.append([x,y,border])
    print("Score: ", max_score_move[3])
    if max_score_move[3] <= board.get_colored()[player-1]:
        i = random.randrange(len(legal_moves))
        print("index: ", i)
        m = legal_moves[i]
        board.add_border(m[0],m[1],m[2],player)
        print("Making a move: ({},{}) {}".format(m[0], m[1], m[2]))
        move = str(m[0]) + "," + str(m[1]) + "," + m[2]
        status = requests.get(SERVER + "/move/" + TEAM_ID + "/" + move).json()
    else:
        board.add_border(max_score_move[0],max_score_move[1],max_score_move[2],player)
        print("Making a move: ({},{}) {}".format(max_score_move[0], max_score_move[1], max_score_move[2]))
        move = str(max_score_move[0]) + "," + str(max_score_move[1]) + "," + max_score_move[2]
        status = requests.get(SERVER + "/move/" + TEAM_ID + "/" + move).json()

def reg():
    # register using a fixed team_id
    resp = requests.get(SERVER + "/reg/" + TEAM_ID).json()  # register 1st team

    if resp["response"] == "OK":
        # save which player we are
        print("Registered successfully as Player {}".format(resp["player"]))
        return resp["player"]
    else:
        # TODO handle the case where the response was ERROR
        pass


def play(player):
    game_over = False
    board = Board(7)
    move_nr = 0
    while not game_over:
        time.sleep(0.5)  # wait a bit before making a new status request
        # request the status of the game
        status = requests.get(SERVER + "/status").json()
        if status["status_code"] > 300:
            game_over = True
        elif status["status_code"] == 200 + player:  # it's our turn
            move_nr += 1
            print("It's our turn ({}ms left)".format(status["time_left"]))
            lastMove = status["last_move"]
            if lastMove != "":
                # add last move to board
                last_x, last_y, last_border = lastMove.split(",")
                if player == 1:
                    last_player = 2
                elif player == 2:
                    last_player = 1
                board.add_border(int(last_x), int(last_y), last_border, last_player)
            if move_nr < 35:
                greedyMove(board,player)
            else:
                deepMove(board,player,2)


if __name__ == "__main__":
    
    player = reg()
    play(player)
