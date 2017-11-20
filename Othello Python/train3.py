# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import copy
from Reversi2 import Reversi
from alphaBetaAI import alphaBetaAgent
from dqn_agent3 import DQNAgent

if  __name__  ==  "__main__" :
    
    trainEpisode = 3

    env = Reversi()
    
    
    counter = 0 #dqn ai가 이긴 횟수  
    
    #dqn AI  여기서는 검은색 돌
    dqnAI = DQNAgent( 8 , 8, True)
   
    #알파베타 ai는 흰색 돌 
    alphabetaAI = alphaBetaAgent(2)
  
    #학습된 모델 불러온다.
    dqnAI.loadModel()
    dqnAI.update_target_network()
    dqnAI.show_variable()

    #지정된 수만큼 학습 시킴. 항상 검은색 돌이 먼저 시작함 
    for episode in range(trainEpisode):
        
        #환경 초기화  변수 setting
        env.reset()
        done = False
        
        state = copy.deepcopy(env.screen)
        targets = env.getEnables(1)
        
        epsilon =  1. / ((episode / 50) + 1)
        reward = 0
        print("Episode: {} ".format(episode))
     #   env.printScreen()
        while not done:
            #dqn agent 차례 
            
            if len (targets) >  0 :
                action_t = dqnAI.selectAction(state, targets,epsilon)
                
                #dqn agent가 행한 action을 action변수에 따로 저장  
                action = action_t
                env.doFlip([action_t//8, action_t%8], 1)
                print("Dqn : ",action_t)
              #  env.printScreen()
                
            #끝남 유무와 승자을 알아온다 
            done = env.isEnd()
            win = env.winner()
            
            if done == True : 
                if(win == env.black):
                    reward = 1
                    counter  = counter+1
                elif(win == env.white):
                    reward = -1
                else:
                    reward =0 
                dqnAI.store_experience(state, action, reward,state,targets, done)
                print("1 :",action, reward,targets, done)
                break
            
            #alpha beta agent 차례  
            targets = env.getEnables( 2 )
            
            if  len (targets) >  0 :
                temp  = copy.deepcopy(env.screen)
                action_t = alphabetaAI.nextMove(temp)
                env.doFlip(action_t, 2)
                print("Alpha : ", action_t)
    #            env.printScreen()
            
            #상대방의 수가 끝난후 상태 저장 
            next_state = copy.deepcopy(env.screen)
            #다음에 내가 놓을 수 있는 targets 저장 
            targets = env.getEnables(1)
            
            done = env.isEnd()
            win = env.winner()
            if done == True : 
                if(win == env.black):
                    reward = 1
                    counter  = counter+1
                elif(win == env.white):
                    reward = -1
                else:
                    reward =0 
                    
            dqnAI.store_experience(state, action, reward,next_state,targets, done)
   #         print("2 :",action, reward,next_state,targets, done)
            
            state = next_state
            
        print("winner : " ,env.winner())
            #end while
        
        if(episode%5 ==1 ):
            for k in range(2):
                dqnAI.experience_replay()
       
            
            
            
    dqnAI.saveModel()
    dqnAI.show_variable()
 
  

            
        
            
          
          
          