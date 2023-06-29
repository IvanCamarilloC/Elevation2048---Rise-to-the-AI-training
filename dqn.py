from collections import deque
import random 
import math
import matplotlib.pyplot as plt
import time 

import jugador as j


import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

class DQN(nn.Module): 
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(256, 2048)
        self.fc2 = nn.Linear(2048, 2048)
        self.fc3 = nn.Linear(2048, 4)

    def forward(self, x):
        x = self.fc1(x)
        x = F.relu(x)
        x = self.fc2(x)
        x= F.relu(x)
        x = self.fc3(x)
        return x
    
class DQN2048Solver: 
    def __init__(self, n_episodes = 1000, n_win_ticks = 195, max_env_steps = None, gamma = 1.0, epsilon = 1.0, epsilon_min = 0.01, epsilon_log_decay = 0.995, alpha = 0.01, alpha_decay = 0.01, batch_size = 64, monitor = False, quiet = False):
        self.memory = deque(maxlen = 100000)
        self.env = j.PartidaFactory.create_partida()
        self.batch_size = batch_size
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_log_decay
        self.alpha = alpha
        self.alpha_decay = alpha_decay
        self.n_episodes = n_episodes
        self.n_win_ticks = n_win_ticks
        self.quiet = quiet
        self.scores = []
        self.mean_scores = []
        self.max_env_steps = max_env_steps
        self.steps = 0

        # Init model 
        self.model = DQN()
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr = self.alpha)
        self.criterion = nn.MSELoss()

    def get_epsilon(self, t):
        return max(self.epsilon_min, min(self.epsilon, 1.0 - math.log10((t + 1) * self.epsilon_decay)))
    
    def preprocess_state(self, state):      
        return torch.tensor(state, dtype = torch.float32)
    
    def choose_action(self, state, epsilon):
        if(np.random.random() <= epsilon):
            return random.randint(0, 3)
        else:
            return torch.argmax(self.model(state)).item()
    
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def replay(self, batch_size):
        y_batch, y_target_batch = [], []
        minibatch = random.sample(self.memory, min(len(self.memory), batch_size))
        for state, action, reward, next_state, done in minibatch:
            y = self.model(state)
            y_target = y.clone().detach()
            with torch.no_grad():
                y_target[action] = reward if done else reward + self.gamma * torch.max(self.model(next_state)).item()
            y_batch.append(y)
            y_target_batch.append(y_target)
        y_batch = torch.cat(y_batch)
        y_target_batch = torch.cat(y_target_batch)

        self.optimizer.zero_grad()
        loss = self.criterion(y_batch, y_target_batch)
        loss.backward()
        self.optimizer.step()

        if self.epsilon > self.epsilon_min:
                self.epsilon *= self.epsilon_decay

    def run(self):
        scores = deque(maxlen = 200)
        for reps in range(10):
            print(reps)
            for e in range(100):
                print(e)
                self.env.reset()
                state = self.preprocess_state(self.env.getHotEncodedMatrixFlatten())
                done = False
                i = 0
                while not done:
                    #if e % 50 == 0:
                        #print(self.env.getMatrix())
                        #self.env.showUI()
                    action = self.choose_action(state, self.get_epsilon(e))
                    next_state, reward, done, cambios = self.env.play(action)
                    while cambios == False:     
                        reps = 0
                        random.seed(time.time()+reps)
                        action = random.randint(0, 3) 
                        next_state, reward, done, cambios = self.env.play(random.randint(0, 3))
                        reps += 1
                    next_state = self.preprocess_state(next_state)
                    self.remember(state, action, reward, next_state, done)
                    state = next_state
                    self.steps += 1
                    i += 1
                scores.append(self.env.getScore())
                mean_score = np.mean(scores)
                if self.env.getScore() >= 8000:
                    self.env.showUI()
                else:
                    print(self.env.getScore())
                    #print("Not solved")
            self.replay(self.batch_size)  
        plt.plot(scores)
        plt.show()


if __name__ == "__main__":
    dqn_solver = DQN2048Solver()
    dqn_solver.run()
