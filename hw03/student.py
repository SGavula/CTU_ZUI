import random, time
import numpy as np

import ox

class UcbBandit():
    def __init__(self, board, c_uct):
        self.c_uct = c_uct
        self.actions = list(board.get_actions())
        self.qs = np.zeros(len(self.actions))
        self.visits = np.zeros(len(self.actions))
        self.last_idx = None

    def total_visits(self):
        return np.sum(self.visits)

    def select(self):
        # save self.last_idx with the selected action
        # This line computes uct value for all actions --> sugar syntax for loop
        ucb_vals = self.qs + self.c_uct * np.sqrt(np.log(self.total_visits()) / self.visits)
        self.last_idx = np.argmax(ucb_vals)
        return self.actions[self.last_idx]

    def update(self, value: float):
        self.visits[self.last_idx] += 1
        self.qs[self.last_idx] += (value - self.qs[self.last_idx]) / self.visits[self.last_idx]

    def best_action(self):
        return self.actions[np.argmax(self.visits)]

class MCTSBot:
    def __init__(self, play_as, time_limit):
        self.play_as = play_as
        self.time_limit = time_limit * 0.9
        self.node_dict = {}
        self.trace = []

    def has_node(self, board):
         return board in self.node_dict

    def make_node(self, board):
         self.node_dict[board] = UcbBandit(board, 1)

    def get_bandit(self, board):
         return self.node_dict[board]

    def select(self, board):
        while self.has_node(board):
            if board.is_terminal():
                break
            # Save node to the trace list for backpropagation
            self.trace.append(board.clone())
            # Get bandit
            bandit = self.get_bandit(board)
            # Choose the next action according to badint max ucb value
            next_action = bandit.select()
            board.apply_action(next_action)

        return board.clone()

    def simulate(self, board):
        while not board.is_terminal():
            random_action = np.random.choice(list(board.get_actions()))
            board.apply_action(random_action)
        return board.get_rewards()

    def backpropagate(self, reward):
        for board in reversed(self.trace):
            # Update parameters in bandit
            self.get_bandit(board).update(reward)      

    def iterate(self, board):
        self.trace = []
        # Check if board node exist
        if not self.has_node(board):
            self.make_node(board)

        # Get last board that we expanded
        best_board = self.select(board.clone())
        
        if best_board.is_terminal():
            rewards_list = best_board.get_rewards()
        else:
            # Create node
            self.make_node(best_board)
            # Simulate moves by choosing random moves till the terminal state of board and return the reward
            rewards_list = self.simulate(best_board.clone())

        # Backpropagate the reward
        reward = rewards_list[self.play_as]
        self.backpropagate(reward)
        

    def play_action(self, board):
        start_time = time.time()

        while (time.time() - start_time) < self.time_limit:
            self.iterate(board.clone())
        
        return self.get_bandit(board).best_action()

class MCTSBotRandom:
    def __init__(self, play_as: int, time_limit: float):
        self.play_as = play_as
        self.time_limit = time_limit * 0.9

    def play_action(self, board):
        return random.choice( list(board.get_actions()) )

# class HumanPlayer:
#     def 

# def print_num(board):
#     for i in range(len(board)):
#         if board[]
#         print(i)


if __name__ == "__main__":
    board = ox.Board(16)
    bots = [MCTSBot(0, 20.1), MCTSBot(1, 1.0)]

    n = 0
    while not board.is_terminal():
        current_player = board.current_player()
        current_player_mark = ox.MARKS_AS_CHAR[ ox.PLAYER_TO_MARK[current_player] ]
        
        current_bot = bots[current_player]
        a = current_bot.play_action(board)
        board.apply_action(a)

        print(f"{current_player_mark}: {a} -> \n{board}\n")
        # print(board.board)