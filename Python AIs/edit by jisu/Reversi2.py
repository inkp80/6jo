# -*- coding: utf-8 -*-

import copy
import numpy as np
'''

black : -1 (oppenent)
white : 1 (white)
'''
class Reversi :
    
    def __init__(self) :
        self.blank = 0
        self.black = -1
        self.white = 1
        
        self.rows = 8
        self.cols = 8
        
        self.reset()
        
    # 보드판을 초기화    
    def reset(self) :
        self.screen = np.zeros((self.rows, self.cols))
        self.invscreen = np.zeros((self.rows, self.cols))
        self.setCell(3, 3, self.white)
        self.setCell(3, 4, self.black)
        self.setCell(4, 3, self.black)
        self.setCell(4, 4, self.white)
        
    # 원하는 위치(x, y)에 돌을 놓음
    def setCell(self, x, y, value) :
        self.screen[x][y] = value
        
    # 원하는 위치에 누구의 돌이 놓여있는지 알려줌
    def getCell(self, x, y) :
        return self.screen[x][y]
        
    # action위치에 돌을 놓았을 때 뒤집힐 상대의 돌 위치를 List로 반환
    def flipList(self, action, color) :
        result = []
        if self.getCell(action[0], action[1]) != self.blank :
            return result
        
        vector = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
        for vec in vector :
            temp = copy.deepcopy(action)
            tempResult = []
            while True :
                if temp[0] + vec[0] < 0 or temp[1] + vec[1] < 0 or temp[0] + vec[0] > 7 or temp[1] + vec[1] > 7:
                    break;
                    
                temp[0] += vec[0]
                temp[1] += vec[1]

                if self.getCell(temp[0], temp[1]) == self.blank :
                    break;
                elif color == self.getCell(temp[0], temp[1]) :
                    result += tempResult
                    break;
                else :
                    tempResult.insert(0, [temp[0], temp[1]])
                
        return result
        
    # action위치에 돌을 두고, 적절한 상대의 돌을 뒤집음
    def doFlip(self, action, color) :
        flipList = self.flipList(action, color)
        self.setCell(action[0], action[1], color)
        for i in flipList :
            self.setCell(i[0], i[1], color)
        
    # 현재 플레이어가 둘 수 있는 위치들을 배열로 반환
    # 위치는 x,y좌표가 아닌 하나의 정수값으로 반환함  
    def getEnables(self, color) :
        result = []
        for i in range(64) :
            if self.getCell(i//8, i%8) == self.blank :
                if len(self.flipList([i//8, i%8], color)) > 0 :
                    result.insert(0, i)
                    
        return result
                
    # 해당 플레이어의 score를 반환
    def getScore(self, color) :
        score = 0
        for i in range(64) :
            if self.getCell(i//8, i%8) == color :
                score += 1
        return score
        
    # 현재 유리한 플레이어를 반환
    def winner(self) :
        blackScore = self.getScore(self.black)
        whiteScore = self.getScore(self.white)
        
        if blackScore == whiteScore :
            return 0
        elif blackScore > whiteScore :
            return self.black
        else :
            return self.white
        
    # 서로 놓을 돌이 없는 상태인지 알려줌
    def isEnd(self) :
        b = self.getEnables(self.black)
        w = self.getEnables(self.white)
        
        if len(b) == 0 and len(w) == 0:
            return True
        
        # 여기 코드 빠졌음. 넣어야 되나 말아야 되나 고민해라
        
        return False
        
    def printScreen(self) :
        i =  0
        for r in range (8) :
            s1 = ''
            for c in range (8) :
                s2 = ''
                if self.screen[r][c] ==  self.blank :
                    s2 = '{0:2d}'.format(i)
                elif self.screen [r][c] == self.black :
                    s2 = '● '
                elif self .screen [r][c] ==  self.white :
                    s2 = '○ '
                s1 = s1 + ' ' + s2
                i +=  1
            print (s1)
            
    def inverseScreen(self) :
        self.invscreen = np.zeros((self.rows, self.cols))
        for i in range (8) :
            for j in range (8) :
                if self.screen[i][j] ==  -1: #black
                    self.invscreen[i][j] =1
                elif self.screen[i][j] == 1:
                    self.invscreen[i][j] =-1
            
            

       
if  __name__  ==  "__main__" :
    # game
    env = Reversi()


    print ( " ------------- GAME START --------------- " )
    while not env.isEnd() :
        for i in [-1,1] :
            if i == env.black :
                print ( " *** 선수 턴 ● *** " )
            else :
                print ( " *** 인두 턴 ○ *** " )
            env.printScreen()
            enables = env.getEnables(i)
            if  len(enables) >  0 :
                flg =  False
                while not flg :
                    print ( " 번호를 입력하십시오 " )
                    for u in enables :
                        print(u)
                    inp =  input ( '>>>  ' )
                    action =  int (inp)
                    for j in enables :                
                        if action == j :
                            flg =  True                       
                            break
                n = env.doFlip([action//8, action%8], i)

            else :
                print ( " 둘 곳 없음! " )
                       
    print ( " *** 게임 종료 *** " )
    env.printScreen ()
    if env.winner () == env.black :
        print ( " 선수 ● 승리! 점수는 {:}/{:} 입니다. ".format (env.getScore (env.black), 64))
    else :
        print ( " 인두 ○ 승리! 점수는 {:} / {:} 입니다. " .format (env.getScore (env.white), 64))