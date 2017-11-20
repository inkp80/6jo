# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 16:54:42 2017

@author: eun
"""

from collections import deque
#import sys

import numpy as np
import tensorflow as tf
import random

class DQNAgent :
    def __init__ ( self ,  rows , cols ) :
        
         #tensorflow 그래프 초기화 
         tf.reset_default_graph()

         #오델로 rows, cols
         self.rows= rows
         self.cols = cols
         
         #===============deep q leraning 뉴럴네트워크 위한 값들 설정=====================#
         
         self.minibatchsize = 20
         self.replayMemorySize = 600
         
         self.learningRate =  0.1
         
         self.discountFactor = 0.9
         
         self.exploration = 0.1
     
         self.currentLoss=0
         #================Q network 변수들===================================#
         
         #2차원 배열을 입력으로 받음 
         self.inputX = tf.placeholder (tf.float32, [None , self.rows, self.cols])
         
         self._Y = tf.placeholder(tf.float32, [None , 64])
         #size = 64
         self.node_size = 64
            
         
         #replay memory
         self.replayMemory = deque(maxlen=self.replayMemorySize)
         
         #모델 초기화
         self.mainQ = self.initModel('main1')
         
         self.targetQ = self.initModel('target')
         
         self.loss, self.training = self.buildOperation()
         
         #session & saver
         self.saver= tf.train.Saver()
         self.sess = tf.Session()
        
         self.sess.run(tf.global_variables_initializer())
         
    def initModel(self,name):
        with tf.variable_scope(name):
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
            
            #output layer
            w_output = tf.get_variable("W_output", shape=[self.node_size, self.node_size],initializer=tf.contrib.layers.xavier_initializer())
            
            b_output = tf.get_variable("B_output", shape=[64],initializer=tf.contrib.layers.xavier_initializer())
            
            output= tf.matmul(hidden_layer1,w_output)+b_output
        return output

    #loss function 과 loss function minimize
    def buildOperation(self):
        #loss(cost) function
        loss = tf.reduce_mean(tf.square (self.mainQ -  self._Y))
         #train operation
        optimizer = tf.train.RMSPropOptimizer ( self.learningRate)
        training = optimizer.minimize(loss)
       
        return loss, training
     
    #main network의 Qvalue 구한다. 
    def Qvalues(self,state):
        return self.sess.run(self.mainQ, feed_dict={self.inputX:[state]})[0]
    #targetnetwork 의 Qvalue구한다.
    def targetQvalues(self,state):
        return self.sess.run(self.targetQ, feed_dict={self.inputX:[state]})[0]
        
    #훈련시킬 때 action 선택 방법 오델로 전략 적용
    def selectAction(self, state, targets,epsilon):
        
        if np.random.rand() <=epsilon:
            return np.random.choice(targets)
        else:
            qvalue, action = self.selectEnableAction(state, targets)
            
            return action
    
    #Q값이 제일 큰 action 선택
    def selectEnableAction(self,state,targets,isTarget=False):
        
        if(isTarget==False):
             Q = self.Qvalues(state)
        else:
              Q = self.targetQvalues(state)
              print("targetnetwork!")
        
        index = np.argsort (Q)
        
        for action in  reversed(index) :
            if action in targets :
                break 
        # max_action Q (state, action)
        qvalue = Q[action]       
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
            Q_ = self.Qvalues(state)
            
            if done : 
                Q_[action] = reward
            else :
                qvalue,action = self.selectEnableAction(next_state,next_targets,True)
                Q_[action] = reward + self.discountFactor*qvalue
            
            y_stack = np.vstack([y_stack,Q_])
            x_stack = np.vstack([x_stack,[state]])
        
        self.currentLoss = self.sess.run(self.loss, feed_dict={self.inputX:x_stack, self._Y:y_stack})
            
        self.sess.run(self.training, feed_dict={self.inputX:x_stack, self._Y:y_stack})
        
        print("currentloss : ", self.currentLoss)
        
    #모델을 정해진 경로에서 불러옴  
    def loadModel(self):
        # load from checkpoint
       # checkpoint = tf.train.get_checkpoint_state(self.model_dir)
        checkpoint = tf.train.get_checkpoint_state('./testing/')
        self .saver.restore(self .sess, checkpoint.model_checkpoint_path)
        print(checkpoint)
        print("loaded!!")
        
    '''
    지정된 경로에 ckpt파일 형식으로 모델 저장 
    현재 같은 경로에 있는 testing 폴더안에 model.ckpt파일 생성  
    '''
    def saveModel(self):
        #self .saver.save ( self .sess, os.path.join(self.model_dir, self .model_name))
        self.saver.save(self.sess, './testing/model.ckpt')
    
    #target network에 복사하기  김성훈 교수님 코드의 함수와 똑같음  
    def update_target_network(self):
        copy_op = []

        main_vars = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope='main1')
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
        a = self.Qvalues(screen_)
        b =  self.targetQvalues(screen_)
        print("Qvalues : ", a)
        print("Qvalues : ", b)