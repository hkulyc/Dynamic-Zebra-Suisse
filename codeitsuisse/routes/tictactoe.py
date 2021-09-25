import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

def findEmpty(board):
    "given a matrix, find the last step to win, return None otherwise"
    # find on row
    for i in range(len(board)):
        empty = None
        for j in range(len(board[0])):
            if board[i][j] == 0:
                if empty == None:
                    empty = (i,j)
                else:
                    break
            if j == 2:
                return empty

    # find on col
    for i in range(len(board)):
        empty = None
        for j in range(len(board[0])):
            if board[j][i] == 0:
                if empty == None:
                    empty = (j,i)
                else:
                    break
                if j == 2:
                    return empty
    
    # find on two diagnal
    count = 0
    for i in range(len(board)):
        empty = None
        j = i
        if board[i][j] == 0:
            count += 1
    if count == 1:
        for i in range(len(board)):
            j = i
            if board[i][j] == 0:
                return (i,j)

    count = 0
    for i in range(len(board)):
        empty = None
        j = 2 - i
        if board[i][j] == 0:
            count += 1
    if count == 1:
        for i in range(len(board)):
            j = 2-i
            if board[i][j] == 0:
                return (i,j)
    return None

def findDial(board):
    "find the diagnal"
    for i in range(len(board)):
        for j in range(len(board)):
            if i==1 and j==1:
                continue
            if board[i][j] == 'c':
                if board[2-i][2-j] == 0:
                    return (2-i,2-j)
    return None

def findAny(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i,j)

class TicTacToe:
    def __init__(self, endpoint, id):
        super().__init__()
        self.endpoint = endpoint
        self.id = id
        self.board = [[0, 0, 0], [0,0,0], [0,0,0]]
        self.firstMove = True

    def setSymbol(self, sym):
        self.symbol = sym

    def print(self):
        for i in self.board:
            print(i)
    
    def add(self, pos, ifComp):
        try:
            if self.board[pos[0]][pos[1]] != 0:
                return False
        except:
            return False
        if ifComp:
            self.board[pos[0]][pos[1]] = 'c'
        else:
            self.board[pos[0]][pos[1]] = 'i'
        return True
    
    def nextMove(self):
        "return a position"
        res = None
        if self.firstMove:
            if self.board[1][1] != 0:
                res = (0,0)
            else:
                # find diagnal

                res = findDial(self.board)
        else:
            res = findEmpty(self.board)
            if res == None:
                # find diagnal
                res = findDial(self.board)
        if res == None:
            res = findAny(self.board)
        self.firstMove = False
        return res

def createAction(pos):
    res = {}
    pos_map = {(0,0): 'NW', (1,0): 'W', (2,0): 'SW', (0,1): 'N', (1,1): 'C',(2,1): 'S', (0,2): 'NE',(1,2): 'E', (2,2): 'SE'}
    if pos_map.get(pos, None) == None:
        res[action] = '(╯°□°)╯︵ ┻━┻'
    else:
        res[action] = 'putSymbol'
        res[position] = pos_map[pos]


@app.route('/tic-tac-toe', methods=['POST'])
def evaluate():
    data = request.get_json()
    logging.info("tictactoe received: {}".format(data))
    inputValue = data.get("input");
    result = inputValue * inputValue
    logging.info("My result :{}".format(result))
    return json.dumps(result)


if __name__ == "__main__":
    test = TicTacToe('asdf', '35efas')
    test.setSymbol('0')
    while True:
        x = int(input())
        y = int(input())
        test.add((x,y), True)
        res = test.nextMove()
        print(res)
        test.add(res, False)
        test.print()