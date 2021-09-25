import logging
import json
from typing import Collection

from flask import request, jsonify
import requests

from codeitsuisse import app

logger = logging.getLogger(__name__)
arena = 'https://cis2021-arena.herokuapp.com/parasite/'

class Board:
    def __init__(self,board,interest):
        self.board = board
        self.row = len(board)
        self.col = len(board[0])
        self.interest = interest
        self.start_x,self.start_y = None,None
    def findstartpoint(self):
        for i,row in enumerate(self.board):
            for j,value in enumerate(row):
                if value == 3:
                    self.start_x,self.start_y = i,j
    def bfs(self,p1):
        queue = []
        px = [-1, 0, 1, 0]
        py = [0, -1, 0, 1]
        board = [ [ 100 for i in range(self.col)] for _ in range(self.row)]
        board[self.start_x][self.start_y] = 0
        queue.append(self.start_x,self.start_y)
        while len(queue) > 0:
            x,y = queue.pop()
            for i in range(4):
                go_x,go_y = x+px[i],y+py[i]
                if go_x < self.row and go_x>0 and go_y < self.col and go_y > 0 and self.board[go_x][go_y] != 0 :
                    board[go_x] = min( board[x] + 1,board[x])
                    board[go_y] = min( board[y] + 1,board[y])
                    queue.append(go_x,go_y)
        for i,j in self.interest:
            if self.board[go_x][go_y] != 0:
                p1[str(i)+','+str(j)] = board[i][j]
            else:
                p1[str(i)+','+str(j)] = -1

        

@app.route('/parasite', methods=['POST'])
def parasite():
    datas = request.get_json()
    res = []
    logging.info("received: {}".format(datas))
    for index,data in enumerate(datas):
        res_dic = {'room':index}
        board = Board(data['grid'],data['interestedIndividuals'])
        p1 = {}
        board.bfs(p1)
        res_dic['p1'] = p1
        res.append(res_dic)
    logging.info("My result :{}".format(res))
    return json.dumps(res)


