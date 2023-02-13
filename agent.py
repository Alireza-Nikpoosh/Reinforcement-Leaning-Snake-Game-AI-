# -*- coding: utf-8 -*-
"""
Created on Sat Feb 11 18:47:13 2023

@author: A-NIK
"""
import pygame
import matplotlib.pyplot as plt
from IPython import display
from model import Linear_QNet, QTrainer
import torch 
import random
import numpy as np
import consts
from game_manager import GameManager
from collections import deque 
MAX_MEMORY = 100000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    
    def __init__(self):
        self.game_count = 0
        self.epsilon = 0 #constant for randomness
        self.gamma = 0.85 #discount rate
        self.memory = deque(maxlen = MAX_MEMORY)
        self.model = Linear_QNet(11, 256, 4)
        self.train = QTrainer(self.model, LR, self.gamma)
    def get_state(self, game):
        state = list()
        head = game.snake.get_head()
        if(head == None):
            return np.ndarray([0,0,0,0,0,0,0,0,0,0,0])
        direction = game.snake.direction 
        dir_is_left = direction == "LEFT"
        dir_is_right = direction == "RIGHT"
        dir_is_up = direction == "UP"
        dir_is_down = direction == "DOWN"
        danger_is_straight = 0
        danger_is_left = 0
        danger_is_right = 0
        for block in consts.block_cells:
            if (
            (dir_is_up and (head[0] == block[0]) and (head[1] > block[1])) or
            (dir_is_down and (head[0] == block[0]) and (head[1] < block[1]))or
            (dir_is_left and (head[1] == block[1]) and (head[0] > block[0]))or
            (dir_is_right and (head[1] == block[1]) and (head[0] <block[0]))
            ):
             danger_is_straight = 1
            if (
            ((dir_is_up or dir_is_down) and (head[0] < block[0]) and (head[1] == block[1])) or
            (dir_is_left and (head[1] > block[1]) and (head[0] == block[0]))or
            (dir_is_right and (head[1] < block[1]) and (head[0] == block[0]))
            ):
             danger_is_right = 1
            if (
             ((dir_is_up or dir_is_down) and (head[0] > block[0]) and (head[1] == block[1])) or
             (dir_is_left and (head[1] < block[1]) and (head[0] == block[0]))or
             (dir_is_right and (head[1] > block[1]) and (head[0] == block[0]))
             ):
              danger_is_left = 1
            
        state = [
            danger_is_straight,
            danger_is_left,
            danger_is_right,
            
            dir_is_up,
            dir_is_down,
            dir_is_left,
            dir_is_right,
            
            #food location
            game.fruit_pos[0] < head[0], 
            game.fruit_pos[0] > head[0],
            game.fruit_pos[1] < head[1],
            game.fruit_pos[1] > head[1]

            ]
        return np.array(state,dtype = int)
    def remember(self, state, action, reward, next_state, game_over):
        self.memory.append((state, action, reward, next_state, game_over))
        
        
    def train_long_momory(self, state, action, reward, next_state, game_over):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory
        states, actions, rewards, next_states, game_overs = zip(*mini_sample)
        self.train.train_step(states, actions, rewards, next_states, game_overs)
        
        
        
    def train_short_memory(self,state, action, reward, next_state, game_over):
        self.train.train_step(state, action, reward, next_state, game_over)
        
    def get_action(self, state):
        directions = ["U","D","L","R"]
        directions_unicode = list(map(ord,directions))
        self.epsilon = 80 - self.game_count
        if np.random.randint(0,200) < self.epsilon:
            move = np.random.choice(directions_unicode, 1)[0]
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = directions_unicode[torch.argmax(prediction).item()]
        return move

def train():
    clock = pygame.time.Clock()
    plot_mean_scores = []
    scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game =  GameManager(consts.table_size, consts.sx, consts.sy, consts.block_cells, consts.keys)
    while True:
        pygame.display.flip()
        clock.tick(120)
        prev_state = agent.get_state(game)
        move = agent.get_action(prev_state)
        reward, game_over, score = game.handle_action(move)
        new_state = agent.get_state(game)
        
        agent.train_short_memory(prev_state, move, reward, new_state, game_over)
        agent.remember(prev_state, move, reward, new_state, game_over)
        
        if(game_over):
            print("GAME IS OVER GAME IS OVERRRRRR")
            game.reset()
            agent.game_count += 1
            agent.train_long_momory(prev_state, move, reward, new_state, game_over)
            if(score > record):
                record = score
                agent.model.save()
            scores.append(score)
            
            total_score += score
            mean_score = total_score / agent.game_count
            plot_mean_scores.append(mean_score)
            plt.ion()
            display.clear_output(wait=True)
            display.display(plt.gcf())
            plt.clf()
            plt.title('Training...')
            plt.xlabel('Number of Games')
            plt.ylabel('Score')
            plt.plot(scores)
            plt.plot(plot_mean_scores)
            plt.ylim(ymin=0)
            plt.text(len(scores)-1, scores[-1], str(scores[-1]))
            plt.text(len(plot_mean_scores)-1, plot_mean_scores[-1], str(plot_mean_scores[-1]))
            plt.show(block=False)
            plt.pause(.1)
train()