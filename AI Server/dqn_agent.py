# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 01:19:28 2017

@author: bkd
"""

from collections import deque

import numpy as np
import tensorflow as tf
import random
import copy

class DQNAgent :

    def __init__(self, rows, cols, flag, name) :
        # 오델로 rows, cols
        self.rows = rows
        self.cols = cols
        self.flag = flag
        self.good = [0, 7, 56, 63]
        self.bad = [1, 6, 8, 9, 14, 15, 48, 49, 54, 55, 57, 62]
        
        # DQN 뉴럴네트워크를 위한 값들        
        self.miniBatchSize = 60
        self.replayMemorySize = 6000
        self.learningRate = 0.1
        self.discountFactor = 0.9
        self.currentLoss = 0.0
        
        # Q 네트워크 변수들
        self.inputX = tf.placeholder(tf.float32, [None, self.rows, self.cols])
        self.y = tf.placeholder(tf.float32, [None, 64])
        self.size = 64
        
        # Replay memory
        self.replayMemory = deque(maxlen = self.replayMemorySize)
        
        # 모델 초기화
        self.mainQ = self.initModel(name + 'main')
        self.targetQ = self.initModel(name +'target')
        self.loss = tf.reduce_mean(tf.square(self.mainQ - self.y))
        self.training = tf.train.AdamOptimizer(self.learningRate).minimize(self.loss)
        
        # session, saver
        self.saver = tf.train.Saver()
        self.sess = tf.Session()
        self.sess.run(tf.global_variables_initializer())

    def initModel(self, name) :
        with tf.variable_scope(name) :
            # [1, 64] 형태의 2차원 배열로 reshape
            X = tf.reshape ( self.inputX, [-1 , self.size])
        
            # Input Layer
            W1 = tf.get_variable("W1", shape = [self.size, self.size], initializer = tf.contrib.layers.xavier_initializer())        
            b1 = tf.get_variable("b1", shape = [self.size], initializer = tf.contrib.layers.xavier_initializer())
            L1 = tf.nn.relu(tf.matmul(X, W1) + b1)
        
            # Hidden Layer
            W2 = tf.get_variable("W2", shape = [self.size, self.size], initializer = tf.contrib.layers.xavier_initializer())        
            b2 = tf.get_variable("b2", shape = [self.size], initializer = tf.contrib.layers.xavier_initializer())
            L2 = tf.nn.relu(tf.matmul(L1, W2) + b2)
            
            if self.flag is True :
                L2 = tf.nn.dropout(L2, 0.8)

            # Output Layer
            W3 = tf.get_variable("W3", shape = [self.size, self.size], initializer = tf.contrib.layers.xavier_initializer())        
            b3 = tf.get_variable("b3", shape = [self.size], initializer = tf.contrib.layers.xavier_initializer())
            output = tf.matmul (L2, W3) + b3
            
        return output

    # main network의 Qvalue를 구함
    def Qvalues(self, state) :
        # Q (state, action) of all actions
        return self.sess.run(self.mainQ, feed_dict = {self.inputX : [state]})[0]
        
    # target network의 Qvalue를 구함
    def targetQvalues(self, state) :
        # Q (state, action) of all actions
        return self.sess.run(self.targetQ, feed_dict = {self.inputX : [state]})[0]

    def selectAction (self, state, targets, epsilon) :
        if np.random.rand() <= epsilon :
            # random
            return np.random.choice(targets)
        else :
            qvalue, action = self.selectEnableAction(state, targets)
            return action
            
    # qvalue중에서 target안에 있고 가장 큰 값 고름  
    def selectEnableAction(self, state, targets, isTarget = False) :
        if isTarget == False :
            Qs = self.Qvalues(state)
        else :
            Qs = self.targetQvalues(state)
            
        index = np.argsort(Qs) # 값이 제일 작은 것의 index순으로 정렬  
        
        for action in reversed(index) :
            if action in targets :
                break 
        # max_action Q (state, action)
        qvalue = Qs[action]

        return qvalue, action
        
    def storeExperience (self, state, action, reward, nextState, nextTargets, done) :
        self.replayMemory.append ((state, action, reward, nextState, nextTargets, done))
        
        if len(self.replayMemory) > self.replayMemorySize :
            self.replayMemory.popleft()

    def experienceReplay (self) :
        miniBatch = random.sample(self.replayMemory, self.miniBatchSize)
        
        xStack = np.empty(0).reshape(0, 8, 8)
        yStack = np.empty(0).reshape(0, 64)
        
        for state, action, reward, nextState, nextTargets, done in miniBatch:
            Q_ = self.Qvalues(state)
            
            if done : 
                Q_[action] = reward
            else :
                qvalue, _ = self.selectEnableAction(nextState, nextTargets, True)
                Q_[action] = reward + self.discountFactor * qvalue
            
            yStack = np.vstack([yStack, Q_])
            xStack = np.vstack([xStack, [state]])
        
        self.currentLoss = self.sess.run(self.loss, feed_dict={self.inputX:xStack, self.y:yStack})
            
        self.sess.run(self.training, feed_dict={self.inputX:xStack, self.y:yStack})

    def updateTargetNetwork(self, dest_scope_name, src_scope_name) :
        copyOp = []
        mainVars = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope=src_scope_name)
        targetVars = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope=dest_scope_name)
        
        for mainVar, targetVar in zip(mainVars, targetVars) :
            copyOp.append(targetVar.assign(mainVar.value()))
            
        self.sess.run(copyOp)

    def loadModel(self, name) :
        checkpoint = tf.train.get_checkpoint_state('./testing_' + name + '/')
        if checkpoint :
            self.saver.restore(self.sess, './testing_'+ name + '/' + name + 'Model.ckpt')
            print(checkpoint)

    def saveModel(self, name) :
        self.saver.save(self.sess, './testing_' + name + '/' + name + 'Model.ckpt')