# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 01:19:28 2017

@author: bkd
"""

from collections import deque
import os

import numpy as np
import tensorflow as tf

class DQNAgent :

    def __init__ (self, pathName, rows, cols, name) :
        tf.reset_default_graph()
        self.rows = rows
        self.cols = cols
        
        self.name = os.path.splitext(os.path.basename(__file__))[0]
        
        self.pathName = pathName
        
        self.minibatchSize = 64
        self.replayMemorySize = 6000
        self.learningRate = 0.01
        self.discountFactor = 0.9
        
        self.currentLoss = 0.0
        
        # 모델 세이브
        self.modelDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models1")
        self.modelName = "{}.ckpt".format(self.pathName)
        
        # Replay memory
        self.replayMemory = deque(maxlen = self.replayMemorySize)
        
        # 모델 초기화
        self.initModel()

    def initModel (self, l_rate = 1e-1) :
        # 2차원 배열을 입력으로 받음
        self.inputX = tf.placeholder(tf.float32, [None, self.rows, self.cols])

        size =  self.rows *  self.cols
        X = tf.reshape ( self.inputX, [-1 , size]) # [?,64]
        
        # Input Layer
        W1 = tf.get_variable("W1", shape = [size, size], initializer = tf.contrib.layers.xavier_initializer())        
        b1 = tf.get_variable("b1", shape = [size], initializer = tf.contrib.layers.xavier_initializer())
        L1 = tf.nn.relu(tf.matmul(X, W1) + b1)
        
        # Hidden Layer
        W2 = tf.get_variable("W2", shape = [size, size], initializer = tf.contrib.layers.xavier_initializer())        
        b2 = tf.get_variable("b2", shape = [size], initializer = tf.contrib.layers.xavier_initializer())
        L2 = tf.nn.relu(tf.matmul(L1, W2) + b2)

        # Output Layer
        W3 = tf.get_variable("W3", shape = [size, size], initializer = tf.contrib.layers.xavier_initializer())        
        b3 = tf.get_variable("b3", shape = [size], initializer = tf.contrib.layers.xavier_initializer())
        self.Qpredict = tf.matmul (L2, W3) + b3

        # loss function
        self.y = tf.placeholder(tf.float32, [None, size])
        self.loss = tf.reduce_mean(tf.square(self.y - self.Qpredict))

        # train operation
        self.training = tf.train.AdamOptimizer(learning_rate=l_rate).minimize(self.loss)

        # saver
        self.saver = tf.train.Saver()
        
        self.sess = tf.Session()
        self.sess.run(tf.global_variables_initializer())
        
        # y가 2차원 배열로 리턴되므로 (1,64) [0]번째만 반환 
    def Qvalues (self, state) :
        # Q (state, action) of all actions
        return self.sess.run(self.Qpredict, feed_dict = {self.inputX : [state]})[0]

    def selectAction (self, state, targets, epsilon) :
        if np.random.rand () <= epsilon :
            # random
            return np.random.choice(targets)
        else :
            # max_action Q (state, action)
            qvalue, action = self.selectEnableAction(state, targets)
            return action
            
    # qvalue중에서 target안에 있고 가장 큰 값 고름  
    def selectEnableAction(self, state, targets) :
        Qs = self.Qvalues(state)
        # descend = np.sort (Qs)
        index = np.argsort(Qs) # 값이 제일 작은 것의 index순으로 정렬  
        for action in reversed(index) :
            if action in targets :
                break 
        # max_action Q (state, action)
        qvalue = Qs[action]

        return qvalue, action
        
    def storeExperience (self, state, targets, action, reward, state_1, targets_1, terminal) :
        self.replayMemory.append ((state, targets, action, reward, state_1, targets_1, terminal))
        if len(self.replayMemory) > self.replayMemorySize :
            self.replayMemory.popleft()

    def experienceReplay (self) :
        state_minibatch = []
        y_minibatch = []

        # sample random minibatch
        minibatchSize =  min(len(self.replayMemory), self.minibatchSize)
        #minibatch size만큼 0~len(D)에 있는 숫자들로 배열 생성 random으로 골라내는것  
        minibatch_indexes = np.random.randint(0, len(self.replayMemory), minibatchSize)

        for j in minibatch_indexes :
            state_j, targets_j, action_j, reward_j, state_j_1, targets_j_1, terminal = self.replayMemory[j]
            y_j = self.Qvalues(state_j)

            if terminal :
                y_j[action_j] = reward_j
            else :
                # reward_j + gamma * max_action 'Q (state'action ')
                qvalue, action =  self.selectEnableAction (state_j_1, targets_j_1)
                y_j [action_j] = reward_j + self.discountFactor * qvalue

            state_minibatch.append (state_j)
            y_minibatch.append (y_j)

        # training
        self.sess.run(self.training, feed_dict = {self.inputX : state_minibatch, self.y : y_minibatch})

        # for log
        self.currentLoss = self.sess.run(self.loss, feed_dict = {self.inputX : state_minibatch, self.y : y_minibatch})


    def loadModel (self, model_path = None) :
        if model_path :
            # load from model_path
            self.saver.restore(self.sess, model_path)
        else :
            # load from checkpoint
            checkpoint = tf.train.get_checkpoint_state(self.modelDir + " ")
            if checkpoint and checkpoint.model_checkpoint_path :
                self.saver.restore (self.sess, checkpoint.model_checkpoint_path)

    def saveModel(self) :
        self.saver.save(self.sess, os.path.join(self.modeDir, self.modelName))