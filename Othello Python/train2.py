# -*- coding: utf-8 -*-

import copy
from Reversi2 import Reversi
from alphaBetaAI import alphaBetaAgent
from dqn_agent2 import DQNAgent

import os


if  __name__  ==  "__main__" :
    
    trainEpisode = 1
    path_name = os.path.splitext (os.path.basename(__file__))[ 0 ]
    
    env = Reversi()
    
    playerID = [env.black, env.white, env.black]
    
    counter = 0 #dqn ai가 이긴 횟수  
    dqnAI = DQNAgent(path_name ,  8 , 8)
    
    #알파베타 ai는 흰색 돌 
    alphabetaAI = alphaBetaAgent(2)
    
    for episode in range(trainEpisode):
        env.reset()
        done = False
        
        state = copy.deepcopy(env.screen)
        targets = env.getEnables(1)
        epsilon =  1. / ((episode / 50) + 1)
        reward = 0
        print("Episode: {} ".format(episode))
        while not done:
            #dqn agent 차례 
            
            if len (targets) >  0 :
                action_t = dqnAI.selectAction(state, targets,epsilon)
                
                action = action_t
                env.doFlip([action_t//8, action_t%8], 1)
                #print("Dqn : ",action_t)
            done = env.isEnd()
            
            if done == True : 
                if(env.winner() == env.black):
                    reward = 1
                    counter  = counter+1
                elif(env.winner() == env.white):
                    reward = -1
                else:
                    reward =0 
                dqnAI.store_experience(state, action, reward,state,targets, done)
                print("1 :",state, action, reward,state,targets, done)
                break
            
            #alpha beta agent 차
            targets = env.getEnables( 2 )
            
            if  len (targets) >  0 :
                temp  = copy.deepcopy(env.screen)
                action_t = alphabetaAI.nextMove(temp)
                env.doFlip(action_t, 2)
                #print("Alpha : ", action_t)
            state = copy.deepcopy(env.screen)
            targets = env.getEnables(1)
            
            done = env.isEnd()
            if done == True : 
                if(env.winner() == env.black):
                    reward = 1
                    counter  = counter+1
                elif(env.winner() == env.white):
                    reward = -1
                else:
                    reward =0 
                    
            dqnAI.store_experience(state, action, reward,state,targets, done)
           # print("2 :",state, action, reward,state,targets, done)
        print("winner : " ,env.winner())
            #end while
        
        if(episode%5 ==0 ):
            for k in range(10):
                dqnAI.experience_replay()
            
    dqnAI.saveModel()

            
        
            
          
          
          