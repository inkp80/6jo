# -*- coding: utf-8 -*-
'''
random AI
'''
import random
class randomAgent :
    def __init__ ( self  ) :
        
        self.action = 0
        
    def select_actions(self,enables):
        self.action = random.choice(enables)
        return self.action
        