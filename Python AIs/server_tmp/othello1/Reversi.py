import os
import numpy as np

class Reversi :

    def __init__ ( self ) :
        # parameters
        self .name = os.path.splitext (os.path.basename ( __file__ ))[ 0 ]
        self .Blank =  0
        self .Black =  1
        self .White =  2
        self .screen_n_rows =  8
        self .screen_n_cols =  8
        self .enable_actions = np.arange ( self .screen_n_rows * self .screen_n_cols)
        # variables
        self .reset ()
        

    def  reset ( self ) :
        "" " 반면 초기화 " ""
        # reset ball position
        self .screen = np.zeros(( self.screen_n_rows, self .screen_n_cols))
        self .set_cells ( 27 , self .White)
        self .set_cells ( 28 , self .Black)
        self .set_cells ( 35 , self .Black)
        self .set_cells ( 36 , self .White)

    def  get_cells ( self , i ) :
        r =  int (i / self .screen_n_cols)
        c =  int (i - (r * self .screen_n_cols))
        return  self .screen [r][c]  
        
       
    def  set_cells ( self , i , value ) :
        r =  int (i /  self .screen_n_cols)
        c =  int (i - (r *  self .screen_n_cols))
        self .screen [r][c] = value
      
      
    def  print_screen ( self ) :
        "" " 반면 출력 " ""
        i =  0
        for r in  range ( self .screen_n_rows) :
            s1 =  ''
            for c in  range ( self .screen_n_cols) :
                s2 =  ''
                if  self .screen [r][c] ==  self .Blank :
                    s2 =  '{0:2d}'.format ( self .enable_actions[i])
                elif  self.screen [r][c] ==  self .Black :
                    s2 =  ' ●'
                elif  self .screen [r][c] ==  self .White :
                    s2 =  ' ○'
                s1 = s1 +  ' '  + s2
                i +=  1
            print (s1)


    def  put_piece ( self , action , color , puton = True ) :
        "" " 자기 말 color (1 or 2)를 위치 action (0 ~ 63)에 넣어 함수 " ""
         
        if self.get_cells(action) !=  self.Blank :
            return  - 1

        """ ----------------------------------------------- ----------
           가로 세로 대각선의 8 가지는 1 차원 데이터이므로,
           현재 위치에서 -9 -8 -7, -1, 1, 7, 8, 9] 
           어긋난 방향을보고 있습니다.
           이것은 [- 1, 0, 1]과 [-8, 0, 8]의 조합으로 검사합니다
           (0과 0 쌍은 제외)
        """
        t, x, y, l = 0 ,action%8, action//8, []
        for di, fi in  zip ([ - 1 , 0 , 1] ,[ x, 7 , 7-x]) :
            for dj, fj in  zip ( [- 8 , 0 , 8] , [y, 7 , 7-y]) :
                
                if  not di == dj ==  0 :
                    b, j, k, m, n = [], 0 , 0 , [], 0                    
                    "" " a : 대상 위치의 id 목록 " ""
                    a =  self .enable_actions [action+di+dj::di+dj][:min(fi,fj)]
                    "" " b : 대상 위치의 말 id리스트 " ""
                    for i in a :
                        b.append ( self .get_cells(i))
                    
                    # print ( "a = {:}"format (a))
                    # print ( "b = {:}"format (b))
                    for i in b :
                        if i ==  0 : # 공백
                            break  
                        elif i == color : # 자기 말이 있으면 그 사이에 상대의 말을 취할
                            "" " 취할 수를 확정하는 " "" 
                            n = k
                            "" " 기울인다 조각을 확정 " "" 
                            l += m
                            "" " 그 방향의 탐사 종료 " ""
                            break
                        else : # 상대의 말
                            k +=  1
                            "" " 기울인다 위치를 재고하는 " "" 
                            m.insert ( 0 ,a[j])
                        j +=  1
                    # print ( "n = {:}"format (n))    
                    t += n
                    
        # print ( "t = {:}"format (t))            
        # print ( "l = {:}"format (l))            
        if t ==  0 :
            return  0
            
        if puton :
            "" " 기울인다 돌을 등록 할 " ""
            for i in l :
                self .set_cells (i, color)
            "" " 지금 둔 돌을 추가하는 " "" 
            self .set_cells (action, color)
            
            
        return t
        
    def  winner ( self ) :
        "" " 이긴 쪽을 돌려 " ""
        Black_score =  self .get_score ( self .Black)
        White_score =  self .get_score ( self .White)
            
        if Black_score == White_score :
            return  0  # 무승부
        elif Black_score > White_score :
            return  self .Black # Black 승리
        elif Black_score < White_score :
            return  self .White # White 승리
        
    def  get_score ( self , color ) :
        "" " 지정된 색상의 현재 점수를 반환 " ""
        score =  0
        for i in  self .enable_actions :
            if  self .get_cells (i) == color :
                score +=  1
        return score

    def  get_enables ( self , color ) :
        result = []
        "" " 둘 위치 목록을 반환 " ""
        for action in  self .enable_actions :
            if  self .get_cells (action) ==  self .Blank :
                "" " 빈 자리 " ""
                if  self .put_piece (action, color, False ) >  0 :
                    "" " 여기 둘 !! " ""
                    result.insert ( 0 , action)
        return result
                    

    def  update ( self , action , color ) :
        """
        action : 돌을 놓는 위치 0부터 63
        """
        # 매스에 둔 경우에 취할 수
        n =  self .put_piece (action, color, False )
        if n > 0 :
            # 매스는 유효합니다
            self .put_piece (action, color)


        return n
            
       
    def  isEnd ( self ) :
        e1 =  self .get_enables ( self .Black)        
        e2 =  self .get_enables ( self .White)  
        if  len (e1) ==  0  and  len (e2) ==  0 :
            # 쌍방 둘 수 없게되면 게임 종료
            return  True
            
        for action in  self .enable_actions :
            if  self .get_cells (action) ==  self .Blank :
                return  False

        return  True
    
if  __name__  ==  "__main__" :
   # game
    env = Reversi ()
    print ( " ------------- GAME START --------------- " )
    while not env.isEnd () :
        for i in  range ( 1 , 3 ) :
            if i == env.Black :
                print ( " *** 선수 턴 ● *** " )
            else :
                print ( " *** 인두 턴 ○ *** " )
            env.print_screen ()
            enables = env.get_enables (i)
            if  len (enables) >  0 :
                flg =  False
                while not flg :
                    print ( " 번호를 입력하십시오 " )
                    print (enables)
                    inp =  input ( '>>>  ' )
                    action_t =  int (inp)
                    for j in enables :                
                        if action_t == j :
                            flg =  True                       
                            break
                n = env.execute_action (action_t, i)

            else :
                print ( " 경로 " )
                       

    print ( " *** 게임 종료 *** " )
    env.print_screen ()
    if env.winner () == env.Black :
        print ( " 선수 ● 승리! 점수는 {:}/{:} 입니다. ".format (env.get_score (env.Black), len (env.enable_actions)))
    else :
        print ( " 인두 ○ 승리! 점수는 { : } / { : } 입니다. " .format (env.get_score (env.White), len (env.enable_actions)))