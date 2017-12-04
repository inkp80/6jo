import copy

from Reversi import Reversi
from dqn_agent import DQNAgent

          
if  __name__  ==  "__main__" :
    
    # parameters
    n_epochs =  1000
    # environment, agent
    env = Reversi ()
 
    # playerID    
    playerID = [env.Black, env.White, env.Black]#black-> white -> black순이므로 

    # player agent    
    players = []
    # player [0] = env.Black
    players.append (DQNAgent (env.enable_actions, env.name, env.screen_n_rows, env.screen_n_cols))
    # player [1] = env.White
    players.append (DQNAgent (env.enable_actions, env.name, env.screen_n_rows, env.screen_n_cols))
   
    
    for e in  range (n_epochs) :
        # reset
        env.reset ()
        terminal =  False
        while terminal ==  False : # 1 에피소드가 끝날 때까지 루프
            
            for i in  range ( 0 , len (players)) :
                state = env.screen
                targets = env.get_enables (playerID[i])
                
                if  len (targets) >  0 :
                    # 어딘가에 두는 장소가있는 경우

                    # 모든 수를 교육하는
                    for tr in targets :
                        tmp = copy.deepcopy (env)
                        tmp.update (tr, playerID [i])
                        # 종료 판정
                        win = tmp.winner ()
                        end = tmp.isEnd ()
                        # 다음 상태
                        state_X = tmp.screen
                        target_X = tmp.get_enables(playerID [i + 1 ])
                        if  len (target_X) ==  0 :
                            target_X = tmp.get_enables(playerID [i])

                        # 양자 교육
                        for j in  range ( 0 , len (players)) :
                            reword =  0
                            if end ==  True :
                                if win == playerID[j] :
                                    # 이기면 보상 1을 얻는다
                                    reword =  1
                           
                            players[j].store_experience (state, targets, tr, reword, state_X, target_X, end)
                            players[j].experience_replay()

                    
                    # 행동을 선택  
                    action = players[i].select_action(state, targets, players[i].exploration)
                    # 행동을 실행
                    env.update (action, playerID[i])
                    
                    # for log
                    loss = players[i].current_loss
                    Q_max, Q_action = players[i].select_enable_action (state, targets)
                   # print("player:{:1d} | pos:{:2d} | LOSS: {:.4f} | Q_MAX: {:.4f}".format(playerID[i], action, loss, Q_max))

                # 행동을 실행 한 결과
                terminal = env.isEnd ()     
                              
        w = env.winner ()
        print("EPOCH: {:03d}/{:03d} | WIN: player{:1d}".format(e, n_epochs, w))                  
        


    # 저장後攻의 player2를 저장한다.
    players [ 1 ] .save_model ()