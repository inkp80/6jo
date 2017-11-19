# -*- coding: utf-8 -*-
"""
Created on Sun Nov 19 00:05:50 2017

@author: bkd
"""

from Reversi import Reversi
from dqn_agent import DQNAgent

          
if  __name__  ==  "__main__" :
    
    # 반복횟수
    n_epochs =  1000
    # Reversi.py 파일의 변수들을 사용하기 위한 env객체를 선언
    env = Reversi ()
 
    # playerID    
    playerID = [env.black, env.white, env.black] #black-> white -> black순이므로 

    # player agent. player[0]과 player[1]은 각각 ([0, 1, ... , 63], 'Reversi', 8, 8) 의 값을 가지게 됨
    players = []
    # player [0] = env.Black
    players.append(DQNAgent(env.name, env.rows, env.cols))
    # player [1] = env.White
    players.append(DQNAgent(env.name, env.rows, env.cols))
   
    for e in  range (n_epochs) :
        # reset
        env.reset ()
        terminal =  False
        while terminal ==  False : # 1 에피소드가 끝날 때까지 루프
            
            for i in  range ( 0 , len (players)) :
                state = env.screen # 현재 보드판의 상태(배열)을 가져옴
                targets = env.getEnables (playerID[i]) # 배열(플레이어가 둘 수 있는 위치를 가짐)을 가져옴
                
                if  len (targets) >  0 : # 어딘가에 둘 수 있는 장소가있는 경우
                    # 행동을 선택  
                    action = players[i].selectAction(state, targets, players[i].exploration)
                    
                    # 행동을 실행
                    env.doFlip([action//8, action%8], playerID[i])
                        
                    # 종료 판정
                    win = env.winner () # 현재 유리한 플레이어
                    end = env.isEnd ()
                        
                    # 다음 상태
                    state_X = env.screen
                    target_X = env.getEnables(playerID[i + 1])
                    if  len (target_X) ==  0 :
                        target_X = env.getEnables(playerID[i])
                        
                    reward =  0
                    if end == True :
                        reward = 1
                           
                    players[i].storeExperience (state, targets, action, reward, state_X, target_X, end)
                    players[i].experienceReplay()                 
                
                    # for log
                    loss = players[i].current_loss
                    Q_max, Q_action = players[i].selectEnableAction (state, targets)
                    print("player:{:1d} | pos:[{:d}][{:d}] | LOSS: {:.4f} | Q_MAX: {:.4f}".format(playerID[i], action//8, action%8, loss, Q_max))

                # 행동을 실행 한 결과
                terminal = env.isEnd()     

        w = env.winner ()
        print("EPOCH: {:03d}/{:03d} | WIN: player{:1d}".format(e, n_epochs, w))                  
        
    # 저장後攻의 player2를 저장한다.
    players [ 1 ] .save_model ()    