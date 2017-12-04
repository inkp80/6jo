# -*- coding: utf-8 -*-
from copy import deepcopy

from Reversi2 import Reversi

#무한대 설정  
INF = float('inf')

'''
black's color :1 
white's color :2

탐색 depth = 3으로 설정  
'''
class alphaBetaAgent :
    def __init__ ( self , color) :
        self.color = color
        if self.color == 1:
            self.opcolor = 2 #상대편 색깔  
        else:
            self.opcolor = 1
            
        self.boardenv = Reversi()
        self.depth =3
        
    
    def endState(self,board):
        self.boardenv.screen = deepcopy(board)
        done = self.boardenv.isEnd();
        #return gameplay.gameOver(state)
        return done
    
    '''
    다음에 수를 놓을 위치를 리턴함  
    '''
    def nextMove(self,board):
        (move, value) = self.max_val(board, -INF, INF, self.depth)
        return move
    
    
    def max_val(self,state, alpha, beta, depth):
        if self.endState(state):
            return None, self.utility(state)
        elif depth == 0:
            return None, self.evaluation(state)
        best = None
        v = -INF
        
        self.boardenv.screen = deepcopy(state)
        enables = self.boardenv.getEnables(self.color)
        moves = self.successors(state, enables,self.color)
      
        for (move, state_) in moves:
            value = self.min_val(state_, alpha, beta, depth - 1)[1]
            if best is None or value > v:
                best = move
                v = value
            if v >= beta:
                return best, v
            alpha = max(alpha, v)
        return best, v

    def min_val(self,state, alpha, beta, depth):
        if self.endState(state):
            return None, self.utility(state)
        elif depth == 0:
            return None, self.evaluation(state)
        best = None
        v = INF
      
        self.boardenv.screen = deepcopy(state)
        enables = self.boardenv.getEnables(self.opcolor)
        moves = self.successors(state, enables,self.opcolor)
        
        for (move, state_) in moves:
            value = self.max_val(state_, alpha, beta, depth - 1)[1]
            if best is None or value < v:
                best = move
                v = value
            if alpha >= v:
                return best, v
            beta = min(beta, v)
        return best, v
    
    '''
    ### Generate all the possible moves and 
    ### the new state related with the move
    '''
    def successors(self,state, enables,color):
        successors_list = []
        moves = []
  
        moves = enables
        for j in moves:
            self.boardenv.screen = deepcopy(state)
            self.boardenv.doFlip([j//8, j%8], color)
            temp = deepcopy(self.boardenv.screen)
            successors_list.append(([j//8, j%8], temp))
        return successors_list
    
    
    
    def utility(self,state):
        answer = 0
        self.boardenv.screen = state
        if self.boardenv.getScore(self.color) == self.boardenv.getScore(self.opcolor):
            answer=0
        elif self.boardenv.getScore(self.color) > self.boardenv.getScore(self.opcolor):
            answer = INF
        else:
            answer = -INF
        return answer
    
    '''
    평가 함수
    각 board의 상태를 숫자로 변환해줌  
    ### Implementation of Positional Strategy
    '''
    def evaluation(self,state):
        result = 0
        weight = [[99,-8,8,6,6,8,-8,99],[-8,-24,-4,-3,-3,-4,-24,-8],
        [8,-4,7,4,4,7,-4,8],[6,-3,4,0,0,4,-3,6],
        [6,-3,4,0,0,4,-3,6],[8,-4,7,4,4,7,-4,8],
        [-8,-24,-4,-3,-3,-4,-24,-8],[99,-8,8,6,6,8,-8,99]]
    
        for i in range(8):
            for j in range(8):
                if state[i][j] == self.color:
                    result += weight[i][j]
                if state[i][j] == self.opcolor:
                    result -= weight[i][j]
    
        return result

if  __name__  ==  "__main__" :
    # game
    env = alphaBetaAgent(1)


        
   