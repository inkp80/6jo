from copy import deepcopy
import numpy
INF = float('inf')

class minmaxAgent :
    def __init__ ( self , color) :
        self.color = color
        if self.color == 1:
            self.opcolor = 2 #상대편 색깔  
        else:
            self.opcolor = 1
        
    def endState(self,done):
        #return gameplay.gameOver(state)
        return done
    
    def nextMove(self,board, enables):
        depth = 4
        (move, value) = self.max_val(board, -INF, INF, depth,enables)
        return move
    
    def max_val(self,state, alpha, beta, depth,enables):
        if depth == 0:
            return None, self.evaluation(state)
        best = None
        v = -INF
     
        moves = self.successors(state, enables)
      
        for (move, state) in moves:
            value = self.min_val(state, alpha, beta, depth - 1,enables)[1]
            if best is None or value > v:
                best = move
                v = value
            if v >= beta:
                return best, v
            alpha = max(alpha, v)
        return best, v
        
    

    '''
    def nextMoveR(board, color):
        depth = 4
    
        (move, value) = min_val(board, -INF, INF, depth, color, True)
        return move
        #return nextMove(board, gameplay.opponent(color), time)
    '''
    ### state in this program is always a "board"
    ### Check if the state is the end
    

    def min_val(self,state, alpha, beta, depth, color):
        if depth == 0:
            return None, self.evaluation(state, color)
        best = None
        v = INF
      
        moves = self.successors(state, self.opcolor)
        
        for (move, state) in moves:
            value = self.max_val(state, alpha, beta, depth - 1, color)[1]
            if best is None or value < v:
                best = move
                v = value
            if alpha >= v:
                return best, v
            beta = min(beta, v)
        return best, v
    
    
    ### Generate all the possible moves and 
    ### the new state related with the move
    def successors(self,state, enables):
        successors_list = []
        moves = []
        '''
        for i in range(8):
            for j in range(8):
                if gameplay.valid(state, color, (i, j)):
                    moves.append((i, j))
        '''
        moves = enables
        for moves in moves:
            newBoard = deepcopy(state)
            gameplay.doMove(newBoard, color, moves)
            successors_list.append((moves, newBoard))
        return successors_list
    
    
    
    def utility(state, color):
        answer = 0
        if gameplay.score(state)[0] == gameplay.score(state)[1]:
            answer = 0
        elif gameplay.score(state)[0] < gameplay.score(state)[1] and color == "W":
            answer = INF
        elif gameplay.score(state)[0] > gameplay.score(state)[1] and color == "B":
            answer = INF
        else:
            answer = -INF
        return answer
    
    
    ### Implementation of Positional Strategy
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
    
        #if reversed:
        #    result = -result
    
        return result



        
   