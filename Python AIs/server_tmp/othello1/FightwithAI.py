import argparse
from Reversi import Reversi
from dqn_agent import DQNAgent
from randomPlay import randomAgent

randomAI = True;
counter = 0;
max_episodes = 2
if  __name__  ==  "__main__" :
    # args
    parser = argparse.ArgumentParser ()
    parser.add_argument( "-m" , "--model_path" )
    parser.add_argument( "-s" , "--save" , dest = "save" , action = "store_true" )
    parser.set_defaults( save = False )
    args = parser.parse_args()
    '''
    # environmet, agent
    env = Reversi ()
    agent = DQNAgent (env.enable_actions, env.name, env.screen_n_rows, env.screen_n_cols)
    agent.load_model (args.model_path)
    '''
    ranagent = randomAgent()
    
    for episode in range(max_episodes):
        env = Reversi()
        #agent 생성
        agent = DQNAgent(env.enable_actions, env.name, env.screen_n_rows, env.screen_n_cols)
        agent.load_model()
        
    # game
        print ( " ------------- GAME START --------------- ",episode )
        while  not env.isEnd () :
            print ( " *** user 턴 ● *** " )#black : 1
            env.print_screen ()
            enables = env.get_enables ( 1 )
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
                    action_t = ranagent.select_actions(enables)
                    #print('>>>  {:}'.format (action_t))
                env.update (action_t, 1 )
            else :
                print ( " 경로 " )
                
               
            if env.isEnd () ==  True : break
            
            print ( " *** AI 턴  ○ *** " ) #white : 2
            env.print_screen()
            enables = env.get_enables( 2 )
            if  len (enables) >  0 :
                qvalue, action_t = agent.select_enable_action(env.screen, enables)
                print('>>>  {:}'.format (action_t))              
                env.update(action_t, 2 )
            else :
                print ( " 경로 " )
            
    
        print ( " *** 게임 종료 *** " )
        if env.winner() ==  1 :
            print ( "당신의 승리! 점수는 {:} 입니다. ".format (env.get_score (1)))
        else :
            print ( " 당신의 패배! AI 점수는 {:} 입니다. ".format (env.get_score (2)))
            counter = counter+1
    print("ai wins: ", counter)