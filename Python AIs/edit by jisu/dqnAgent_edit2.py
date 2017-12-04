# -*- coding: utf-8 -*-
'''
white 기준으로 훈련  
'''
'''
black :-1 (oppsite)
white : 1 (own)
'''
from collections import deque
#import sys

import numpy as np
import tensorflow as tf
import random
class NuralNet:
    def __init__(self, inputX, session, flag, input_size = 64, output_size = 64, name = "main"):
        self.session = session
        self.input_size = input_size
        self.output_size = output_size
        self.net_name = name
        self.node_size = 64
        self.l_rate = 0.01 #learning rate
        self.inputX = inputX
        self.flag = flag
        self.initNetwork()
        
    def initNetwork(self):
        with tf.variable_scope(self.net_name):
            #[?,64]
            X = tf.reshape(self.inputX, [-1, 64])
            
            #Variable get variable
            
            #input layer
            w_input = tf.get_variable("W_input", shape=[64, self.node_size],initializer=tf.contrib.layers.xavier_initializer())
            b_input = tf.get_variable("B_input", shape=[self.node_size],initializer=tf.contrib.layers.xavier_initializer())
            input_layer = tf.nn.relu(tf.matmul(X,w_input)+b_input)
            
            #Hidden layer1
            w_hidden1 = tf.get_variable("W_hidden1", shape=[self.node_size, self.node_size],initializer=tf.contrib.layers.xavier_initializer())
            b_hidden1 = tf.get_variable("B_hidden1", shape=[self.node_size],initializer=tf.contrib.layers.xavier_initializer())
            hidden_layer1 = tf.nn.relu(tf.matmul(input_layer,w_hidden1)+b_hidden1)

            if self.flag is True:
                hidden_layer1 = tf.nn.dropout(hidden_layer1, 0.8)

            #Hidden layer2
            w_hidden2 = tf.get_variable("W_hidden2", shape=[self.node_size, self.node_size],initializer=tf.contrib.layers.xavier_initializer())
            b_hidden2 = tf.get_variable("B_hidden2", shape=[self.node_size],initializer=tf.contrib.layers.xavier_initializer())
            hidden_layer2 = tf.nn.relu(tf.matmul(hidden_layer1,w_hidden2)+b_hidden2)
    
            if self.flag is True:
                hidden_layer2 = tf.nn.dropout(hidden_layer2, 0.8)
    
			#output layer
            w_output = tf.get_variable("W_output", shape=[self.node_size, self.node_size],initializer=tf.contrib.layers.xavier_initializer())
            b_output = tf.get_variable("B_output", shape=[64],initializer=tf.contrib.layers.xavier_initializer())
            
            self._Qpred = tf.matmul(hidden_layer2,w_output)+b_output
               
        # We need to define the parts of the network needed for learning a policy
        self._Y = tf.placeholder(shape=[None, self.output_size], dtype=tf.float32)
        #loss(cost) function
        self.loss = tf.reduce_mean(tf.square (self._Qpred -  self._Y))
         #train operation
        self.optimizer = tf.train.AdamOptimizer( self.l_rate) #이게 성능 더 좋음 https://arxiv.org/pdf/1412.6980.pdf
        self.training = self.optimizer.minimize(self.loss) 

    def Qvalues(self,state):
        return self.session.run(self._Qpred, feed_dict={self.inputX:[state]})[0]  
    
    
class DQNAgent :
    def __init__ ( self ,  rows , cols, flag ) :
        """
        rows : 행
        cols : 열
        flag : is Train? train일경우 true, fightwithAI일 경우 false
        """
        #tensorflow 그래프 초기화 
        tf.reset_default_graph()
    
        #오델로 rows, cols
        self.rows= rows
        self.cols = cols
        self.flag = flag
        #===============deep q leraning 뉴럴네트워크 위한 값들 설정=====================#
         
        self.minibatchsize = 60
        self.replayMemorySize = 50000
        
        self.discountFactor = 0.9
    
        self.currentLoss=0
        #================Q network 변수들===================================#
         
        #2차원 배열을 입력으로 받음 
        self.inputX = tf.placeholder (tf.float32, [None , self.rows, self.cols])
         
        #self._Y = tf.placeholder(tf.float32, [None , 64])
        #size = 64
        
        
        #session
        self.sess = tf.Session()    
         
        #replay memory
        self.replayMemory = deque(maxlen=self.replayMemorySize)
        
        #모델 초기화
        self.mainQ = NuralNet(self.inputX, self.sess, self.flag, 64, 64, name="main")
        self.targetQ = NuralNet(self.inputX, self.sess, self.flag, 64, 64, name="target") 
        
        #saver
        self.saver= tf.train.Saver()
        
        self.sess.run(tf.global_variables_initializer())

        
    #훈련시킬 때 action 선택 방법 오델로 전략 적용
    def selectAction(self, state, targets,epsilon):
        
        if np.random.rand() <=epsilon:
            
            if self.flag is True:
                #오델로 전략
                if targets.count(0) != 0:
                    print("strategy 0")
                    return 0 
                elif targets.count(7) != 0:
                    print("strategy 7")
                    return 7
                elif targets.count(56) != 0:
                    print("strategy 56")
                    return 56
                elif targets.count(63) != 0:
                    print("strategy 63")
                    return 63
            
            return np.random.choice(targets)
        else:
            qvalue, action = self.selectEnableAction(state, targets)
            
            return action
    
    #Q값이 제일 큰 action 선택
    def selectEnableAction(self,state,targets,isTarget=False):
        
        if(isTarget==False):
            Q = self.mainQ.Qvalues(state)
        else:
            Q = self.targetQ.Qvalues(state)
        
        index = np.argsort(Q)
        
        for action in  reversed(index) :
            if action in targets :
                break 
        # max_action Q (state, action)
        qvalue = Q[action]       
        #return qvalue, action  
        return qvalue, action    
    
    #state, action, reward, done 을 저장      
    def store_experience(self, state, action, reward,next_state,next_targets, done):
        self.replayMemory.append((state, action, reward,next_state,next_targets, done))
        
        if len(self.replayMemory) > self.replayMemorySize:
                      self.replayMemory.popleft()

    
    #쌓아놓은 data들을 한꺼번에 학습  
    def experience_replay(self):
        print("experience replay!")
        minibatch = random.sample(self.replayMemory , self.minibatchsize)
        
        x_stack = np.empty(0).reshape(0,8,8)
        y_stack = np.empty(0).reshape(0,64)
        for state, action, reward,next_state,next_targets, done in minibatch:
            Q_ = self.mainQ.Qvalues(state)
            
            if done : 
                Q_[action] = reward
            else :
                qvalue,action = self.selectEnableAction(next_state,next_targets,True)
                Q_[action] = reward + self.discountFactor*qvalue
            
            y_stack = np.vstack([y_stack,Q_])
            x_stack = np.vstack([x_stack,[state]])
        
        self.currentLoss = self.sess.run(self.mainQ.loss, feed_dict={self.inputX:x_stack, self.mainQ._Y:y_stack})
            
        self.sess.run(self.mainQ.training, feed_dict={self.inputX:x_stack, self.mainQ._Y:y_stack})
        
        print("currentloss : ", self.currentLoss)
        
    #모델을 정해진 경로에서 불러옴  
    def loadModel(self):
        # load from checkpoint
       # checkpoint = tf.train.get_checkpoint_state(self.model_dir)
        checkpoint = tf.train.get_checkpoint_state('./testing_jisu/')
        if checkpoint :
            self .saver.restore(self .sess, checkpoint.model_checkpoint_path)
            print(checkpoint)
            print("loaded!!")
        
    '''
    지정된 경로에 ckpt파일 형식으로 모델 저장 
    현재 같은 경로에 있는 testing 폴더안에 model.ckpt파일 생성  
    '''
    def saveModel(self):
        #self .saver.save ( self .sess, os.path.join(self.model_dir, self .model_name))
        self.saver.save(self.sess, './testing_jisu/model.ckpt')
    
    #target network에 복사하기  김성훈 교수님 코드의 함수와 똑같음  
    def update_target_network(self):
        copy_op = []

        main_vars = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope='main')
        target_vars = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope='target')

        # 학습 네트웍의 변수의 값들을 타겟 네트웍으로 복사해서 타겟 네트웍의 값들을 최신으로 업데이트합니다.
        for main_var, target_var in zip(main_vars, target_vars):
            copy_op.append(target_var.assign(main_var.value()))

        self.sess.run(copy_op)

    #qvalue 확인을 위해  그냥 넣은 함수 
    def show_variable(self) :
        screen_ = np.zeros((8,8))
        screen_[3,3]=2
        screen_[3,4]=1
        screen_[4,3]=1
        screen_[4,4]=2
        a = self.mainQ.Qvalues(screen_)
        b = self.targetQ.Qvalues(screen_)
        print("Qvalues : ", a)
        print("Qvalues : ", b)