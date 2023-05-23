import instanciaPartida as ip
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torchvision.transforms as T
from collections import namedtuple, deque
from itertools import count
import random

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def encode_state(partida):
    # Creo que ni siquiera es necesario hacer el hot encoding
    # TODO hacer esto mas eficiente
    board = torch.tensor([partida.getHotEncodedMatrixFlatten]).to(device, dtype=torch.float)
    board = board.reshape(1, 4, 4, 16).permute(0, 3, 1, 2)
    return board

Transition = namedtuple('Transition',
                        ('state', 'action', 'next_state', 'reward'))

class ReplayMemory(object):
    def __init__(self, capacity):
        self.memory = deque([],maxlen=capacity)

    def push(self, *args):
        self.memory.append(Transition(*args))

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)
    
class ConvBlock(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(ConvBlock, self).__init__()
        d = output_dim // 4
        self.conv1 = nn.Conv2d(input_dim, d, 1, padding='same')
        self.conv2 = nn.Conv2d(input_dim, d, 2, padding='same')
        self.conv3 = nn.Conv2d(input_dim, d, 3, padding='same')
        self.conv4 = nn.Conv2d(input_dim, d, 4, padding='same')

    def forward(self, x):
        x = x.to(device)
        output1 = self.conv1(x)
        output2 = self.conv2(x)
        output3 = self.conv3(x)
        output4 = self.conv4(x)
        return torch.cat((output1, output2, output3, output4), dim=1)

class DQN(nn.Module):

    def __init__(self):
        super(DQN, self).__init__()
        self.conv1 = ConvBlock(16, 2048)
        self.conv2 = ConvBlock(2048, 2048)
        self.conv3 = ConvBlock(2048, 2048)
        self.dense1 = nn.Linear(2048 * 16, 1024)
        self.dense6 = nn.Linear(1024, 4)
    
    def forward(self, x):
        x = x.to(device)
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))
        x = nn.Flatten()(x)
        x = F.dropout(self.dense1(x))
        return self.dense6(x)

# Neural Network Initialisation and utilities
BATCH_SIZE = 64
GAMMA = 0.99
EPS_START = 0.9
EPS_END = 0.01
EPS_DECAY = 0.9999
TARGET_UPDATE = 20
n_actions = 4

policy_net = DQN().to(device)
target_net = DQN().to(device)
# target_net.load_state_dict(policy_net.state_dict())
policy_net.load_state_dict(torch.load('/content/drive/MyDrive/2048_reinforcement_learning/policy_net.pth'))
target_net.load_state_dict(torch.load('/content/drive/MyDrive/2048_reinforcement_learning/target_net.pth'))
target_net.eval()
policy_net.train()

optimizer = optim.Adam(policy_net.parameters(), lr=5e-5)
# scheduler = optim.lr_scheduler.ExponentialLR(optimizer, gamma=0.98)
memory = ReplayMemory(50000)

steps_done = 0

def select_action(state):
    global steps_done
    sample = random.random()
    eps_threshold = max(EPS_END, EPS_START * (EPS_DECAY ** steps_done))
    steps_done += 1
    if sample > eps_threshold:
        with torch.no_grad():
            return policy_net(state).max(1)[1].view(1, 1)
    else:
        return torch.tensor([[random.randrange(n_actions)]], device=device, dtype=torch.long)
    
def optimize_model():
    if len(memory) < BATCH_SIZE:
        return
    transitions = memory.sample(BATCH_SIZE)
    batch = Transition(*zip(*transitions))

    non_final_mask = torch.tensor(tuple(map(lambda s: s is not None,
                                          batch.next_state)), device=device, dtype=torch.bool)
    non_final_next_states = torch.cat([s for s in batch.next_state
                                                if s is not None])
    state_batch = torch.cat(batch.state)
    action_batch = torch.cat(batch.action)
    reward_batch = torch.cat(batch.reward)

    state_action_values = policy_net(state_batch).gather(1, action_batch)

    next_state_values = torch.zeros(BATCH_SIZE, device=device)
    next_state_values[non_final_mask] = target_net(non_final_next_states).max(1)[0].detach()
    expected_state_action_values = (next_state_values * GAMMA) + reward_batch

    criterion = nn.MSELoss()
    loss = criterion(state_action_values, expected_state_action_values.unsqueeze(1))

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    # global steps_done
    # if steps_done % 5000 == 0 and steps_done < 1000000:
    #   print("Learning rate changed.")
    #   scheduler.step()

def same_move(state, next_state, last_memory):
  return torch.eq(state, last_memory.state).all() and torch.eq(next_state, last_memory.next_state).all()


partida = ip.Partida()

total_scores, best_tile_list = [], []

num_episodes = 5000
for i_episode in range(num_episodes):
    print(f"Episode {i_episode}")
    partida.reset()
    state = encode_state(partida).float()
    duplicate = False
    non_valid_count, valid_count = 0, 0
    for t in count():
        # Select and perform an action
        action = select_action(state)
        old_score = partida.getScore()
        old_max = partida.getMaxTile()
        partida.play(action.item())

        done = game.is_game_over()

        reward = (game.total_score - old_score)
        reward = torch.tensor([reward], device=device)

        # Observe new state
        if not done:
            next_state = encode_state(game.board).float()
        else:
            next_state = None
        
        if next_state != None and torch.eq(state, next_state).all():
          non_valid_count += 1
          reward -= 10
        else:
          valid_count += 1

        # Store the transition in memory
        # if next_state != None and duplicate and not torch.eq(state, next_state).all():
        #   duplicate = False

        # if not duplicate:
        if next_state == None or len(memory) == 0 or not same_move(state, next_state, memory.memory[-1]):
          memory.push(state, action, next_state, reward)
        
        # if next_state != None:
        #   duplicate = torch.eq(state, next_state).all()
          
        # Move to the next state
        state = next_state

        # Perform one step of the optimization (on the policy network)
        # optimize_model()
        
        if done:
          for _ in range(100):
            optimize_model()

          print(game.board)
          print(f"Episode Score: {game.total_score}")
          print(f"Non valid move count: {non_valid_count}")
          print(f"Valid move count: {valid_count}")
          total_scores.append(game.total_score)
          best_tile_list.append(game.board.max())
          if i_episode > 50:
            average = sum(total_scores[-50:]) / 50
            print(f"50 episode running average: {average}")
          break

    # Update the target network, copying all weights and biases in DQN
    if i_episode % TARGET_UPDATE == 0:
        target_net.load_state_dict(policy_net.state_dict())
        policy_net.train()
    
    if i_episode % 100 == 0:
        torch.save(policy_net.state_dict(), '/content/drive/MyDrive/2048_reinforcement_learning/policy_net.pth')
        torch.save(target_net.state_dict(), '/content/drive/MyDrive/2048_reinforcement_learning/target_net.pth')

print('Complete')
