# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 16:54:42 2017

@author: eun
"""

from collections import deque
import os
#import sys

import numpy as np
import tensorflow as tf
import random

class DQNAgent :
    def __init__ ( self , path_name ,  rows , cols ) :
        
         #tensorflow 그래프 초기화 
         tf.reset_default_graph()
         
         #모델 저장을 위한 경로 지정
         self .name = os.path.splitext (os.path.basename(__file__))[0]
         self.path_name = path_name
         
         self.model_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),"models3")
         self.model_name = "{}.ckpt".format(self.path_name)
         
         
         #오델로 rows, cols
         self.rows= rows
         self.cols = cols
         
         #===============deep q leraning 뉴럴네트워크 위한 값들 설정=====================#
         
         self.minibatchsize = 20
         self.replayMemorySize = 6000
         
         self.learningRate =  0.1
         
         self.discountFactor = 0.9
         
         self.exploration = 0.1
     
         self.currentLoss=0
         
         #replay memory
         self.replayMemory = deque(maxlen=self.replayMemorySize)
         
         #모델 초기화
         self.initModel()
         
        
         
    def initModel(self):
        #2차원 배열을 입력으로 받음 
        self.inputX = tf.placeholder (tf.float32, [None , self.rows, self.cols])
        
        #size = 64
        
        self.node_size = 64
        
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
        
        self.output= tf.matmul(hidden_layer1,w_output)+b_output
        
        #loss function
        self._Y = tf.placeholder(tf.float32, [None , 64])
        self.loss = tf.reduce_mean(tf.square (self.output -  self._Y))
        
        
        #train operation
        optimizer = tf.train.RMSPropOptimizer ( self.learningRate)
        self.training = optimizer.minimize(self.loss)
        
        
        #session & saver
        self.saver= tf.train.Saver()
        self.sess = tf.Session()
        
        self.sess.run(tf.global_variables_initializer())
        
    def Qvalues(self,state):
        return self.sess.run(self.output, feed_dict={self.inputX:[state]})[0]
        
    #훈련시킬 때 action 선택 방법 오델로 전략 적용
    def selectAction(self, state, targets,epsilon):
        
        if np.random.rand() <=epsilon:
            return np.random.choice(targets)
        else:
            qvalue, action = self.selectEnableAction(state, targets)
            
            return action
    
    #Q값이 제일 큰 action 선택
    def selectEnableAction(self,state,targets):
        Q = self.Qvalues(state)
        
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
                qvalue,action = self.selectEnableAction(next_state,next_targets)
                Q_[action] = reward + self.discountFactor*qvalue
            
            y_stack = np.vstack([y_stack,Q_])
            x_stack = np.vstack([x_stack,[state]])
        
        self.currentLoss = self.sess.run(self.loss, feed_dict={self.inputX:x_stack, self._Y:y_stack})
            
        self.sess.run(self.training, feed_dict={self.inputX:x_stack, self._Y:y_stack})
        
        print("currentloss : ", self.currentLoss)
        
    def loadModel(self):
        # load from checkpoint
        checkpoint = tf.train.get_checkpoint_state(self.model_dir)
        self .saver.restore(self .sess, checkpoint.model_checkpoint_path)
        print("loaded!!")
        
    def saveModel(self):
        self .saver.save ( self .sess, os.path.join(self.model_dir, self .model_name))
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        