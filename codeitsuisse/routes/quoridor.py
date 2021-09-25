import logging
import json

from flask import request, jsonify
import requests

from codeitsuisse import app

logger = logging.getLogger(__name__)
arena = 'https://cis2021-arena.herokuapp.com/quoridor/'

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

class Quoridor:
    def __init__(self, endpoint, id):
        super().__init__()
        self.endpoint = endpoint
        self.id = id
        self.board = []
        for i in range(9):
            row = []
            for j in range(9):
                row.append(0)
            self.board.append(row)
        self.bound = set()
        self.bound = set()
        self.me_pos = None
        self.com_pos = None
        self.firstMove = True

    def setSymbol(self, sym):
        self.symbol = sym
        if sym == 'first':
            self.me_pos = (5, 1)
            self.com_pos = (5, 9)
        else:
            self.com_pos = (5, 1)
            self.me_pos = (5, 9)

    def print(self):
        for i in range(9,0,-1):
            for j in range(9,0,-1):
                if j == self.me_pos[0] and i==self.me_pos[1]:
                    print('i ', end = '')
                elif j == self.com_pos[0] and i==self.com_pos[1]:
                    print('c ', end = '')
                else:
                    print('0 ', end = '')
            print()

    def valid(self, old, new, ano):
        x_diff = new[0] - old[0]
        y_diff = new[1] - old[1]
        if new == old:
            return False
        if x_diff+y_diff in (1,-1) and x_diff*y_diff == 0:
            if self.bound.__contains__((old, new)) or self.bound.__contains__((new, old)):
                return False
            if ano == new:
                return False
        elif x_diff in (-2,2) and y_diff == 0:
            if (old[0]+x_diff/2, old[1]) == ano:
                return valid(ano, new, None)
            else:
                return False
        elif y_diff in (-2,2) and x_diff == 0:
            if (old[0], old[1]+y_diff/2) == ano:
                return valid(ano, new, None)
            else:
                return False
        else:
            return False
    
    def move(self, pos, ifComp):
        if ifComp:
            if self.valid(self.com_pos, pos, self.me_pos):
                self.com_pos = pos
                return True
            else:
                return False
        else:
            if self.valid(self.me_pos, pos, self.com_pos):
                self.me_pos = pos
                return True
            else:
                return False
    
    def add_wall(self, pos):
        try:
            if pos.endswith('h'):
                x = ord(pos[0]) - 97 + 1
                y = int(pos[1])
                self.bound.add(((x, y), (x, y+1)))
                self.bound.add(((x+1, y), (x+1, y+1)))
            else:
                x = ord(pos[0]) - 97 + 1
                y = int(pos[1])
                self.bound.add(((x, y), (x+1, y)))
                self.bound.add(((x, y+1), (x+1, y+1)))
        except:
            return False
    
    def nextMove(self):
        "return a position"
        if self.symbol == 'first':
            return (5, self.me_pos[1]+1)
        else:
            return (5, self.me_pos[1]-1)
        
    
# pos_map = {(0,0): 'NW', (1,0): 'W', (2,0): 'SW', (0,1): 'N', (1,1): 'C',(2,1): 'S', (0,2): 'NE',(1,2): 'E', (2,2): 'SE'}

def flip(pos):
    res = {}
    res['action'] = '(╯°□°)╯︵ ┻━┻'
    return res

def move(pos):
    res = {}
    res['action'] = 'move'
    res['position'] = chr(pos[0]+96)+str(pos[1])
    return res

def wall(pos):
    res = {}
    res['action'] = 'move'
    res['position'] = chr(pos[0]+96)+str(pos[1])
    return res

def decode_pos(pos):
    "convert a1 to 11"
    return (ord(pos[0]) - 96, int(pos[1]))


@app.route('/quoridor', methods=['POST'])
def quoridor():
    try:
        return main(request)
    except:
        return ''

def main(request):
    data = request.get_json()
    logging.info("quoridor received: {}".format(data))
    id = data.get('battleId')
    new_game = Quoridor(arena, id)
    r = requests.get(url = arena+'start/'+id, stream = True).iter_lines()
    data = next(r)
    while data == b'':
        data = next(r)
    data = data[6:]
    # extracting data in json format
    data = json.loads(data)
    logging.info("quoridor received: {}".format(data))
    new_game.setSymbol(data.get('youAre'))
    # logging.info("symbol: {}".format(new_game.symbol))
    my_turn = (new_game.symbol == 'First')
    while data.get('winner') == None:
        if my_turn:
            pos = new_game.nextMove()
            res = move(pos)
            logging.info("My move: {}".format(res))
            new_game.move(pos, False)
            requests.post(url = arena+'play/'+id, json = res)
            my_turn = False
            None
        else:
            # r = requests.get(url = arena+'start/'+id, stream = True)
            while True:
                data = next(r)
                while data == b'':
                    data = next(r)
                data = data[6:]
                data = json.loads(data)
                logging.info("quoridor received: {}".format(data))
                pos_string = data.get('position', None)
                pos = None
                try:
                    pos = decode_pos(pos_string)
                except:
                    pos = None
                if pos == None:
                    data = {'winner': 'me'}
                    res = flip()
                    logging.info("My move: {}".format(res))
                    requests.post(url = arena+'play/'+id, json = res)
                    break
                    # return ''
                if data.get('player') != new_game.symbol:
                    if not new_game.move(pos, True):
                        res = flip()
                        logging.info("My move: {}".format(res))
                        requests.post(url = arena+'play/'+id, json = res)
                        break
                    my_turn = True
                    break
                else:
                    # if move != None and pos != pos_map[move]:
                    #     res = create_action(None)
                    #     logging.info("My move: {}".format(res))
                    #     requests.post(url = arena+'play/'+id, json = res)
                    # break
                    None
    # inputValue = data.get("input");
    # result = inputValue * inputValue
    logging.info('quoridor finished!')
    return ''


# if __name__ == "__main__":
#     test = Quoridor('asdf', '35efas')
#     test.setSymbol('first')
#     test.print()
#     while True:
#         x = int(input())
#         y = int(input())
#         test.move((x,y), True)
#         res = test.nextMove()
#         print(res)
#         test.move(res, False)
#         test.print()