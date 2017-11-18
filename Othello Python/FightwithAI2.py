# -*- coding: utf-8 -*-

from Reversi2 import Reversi
from randomPlay import randomAgent
from alphaBetaAI import alphaBetaAgent
import copy
import numpy as np

'''
env.printScreen() 주석처리 되어 있음 
'''
#true일 경우 random한 것과 대전  
randomAI = True;

#AI가 이기는 횟수 계산
counter = 0;

#대전할 게임 횟수  
max_episodes = 5

if  __name__  ==  "__main__" :
    # args

    
    for episode in range(max_episodes):
        env = Reversi()
        randomagent = randomAgent()
        alphabeta_agent = alphaBetaAgent(2)
    # game
        print ( " ------------- GAME START --------------- ",episode )
        while  not env.isEnd () :
            print ( " *** user 턴 ● *** " )#black : 1
            #env.printScreen ()
            enables = env.getEnables( 1 )
            if  len (enables) >  0 :
                if(randomAI == False) :
                    flg =  False
                    while not flg : #입력가능한 값들중 이상한 값을 집어넣는것 방지
                        print( " 번호를 입력하십시오 " )
                        print(enables)
                        inp =  input ( '>>>  ' )
                        action_t =  int(inp)
                        for i in enables :                
                            if action_t == i :
                                flg =  True                       
                                break
                
                else:
                    #action_t = random.choice(enables)
                    action_t = randomagent.select_actions(enables)
                    #print('>>>  {:}'.format (action_t))
                   
                
                env.doFlip([action_t//8, action_t%8], 1)
            else :
                print ( " 경로 " )
                
               
            if env.isEnd () ==  True : break
            
            print ( " *** AI 턴  ○ *** " ) #white : 2
            #env.printScreen()
            enables = env.getEnables( 2 )
            if  len (enables) >  0 :
                temp  = copy.deepcopy(env.screen)
                action_t = alphabeta_agent.nextMove(temp)
                print('>>>  {:}'.format(action_t))
                env.doFlip(action_t, 2)
                    
            else :
                print ( " 경로 " )
            
    
        print ( " *** 게임 종료 *** " )
        if env.winner() ==  1 :
            print ( "당신의 승리! 점수는 {:} 입니다. ".format (env.getScore (1)))
        else :
            print ( " 당신의 패배! AI 점수는 {:} 입니다. ".format (env.getScore (2)))
            counter = counter+1
    print("ai wins: ", counter)
