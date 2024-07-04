from blockworld import BlockWorldEnv
import random
import math

class QLearning():
	# don't modify the methods' signatures!
	def __init__(self, env: BlockWorldEnv):
		self.env = env
		self.q_dict = {}

	def get_best_action(self, state, goal):
		best_action = None
		max_value = float('-inf')

		for a in state.get_actions():
			if (state, goal, a) in self.q_dict:
				value = self.q_dict[(state, goal, a)]
				if value > max_value:
					max_value = value
					best_action = a

		if best_action == None:
			num_actions = len(state.get_actions())
			random_action_idx = random.randint(0, num_actions - 1)
			return state.get_actions()[random_action_idx], 0
		else:
			return best_action, max_value

	def get_value_from_q_dict(self, state, goal, action):
		if (state, goal, action) in self.q_dict:
			return self.q_dict.get((state, goal, action))
		else:
			#return 0 as value
			return 0

	def train(self):
		# Use BlockWorldEnv to simulate the environment with reset() and step() methods.

		# s = self.env.reset()
		# s_, r, done = self.env.step(a)

		num_episodes = 10000
		max_steps_per_episode = 100

		alpha = 0.1
		discount_rate = 0.99

		exploration_rate = 1
		max_exploration_rate = 1
		min_exploration_rate = 0.01
		exploration_decay_rate = 0.001

		episode = 1

		# Q-learning algorithm
		while True:
			# if episode % 10 == 0:
			# 	print(f"Episode with number: {episode}")
			
			# Initialize starting variables
			state, goal = self.env.reset()
			done = False

			for step in range(max_steps_per_episode):
				expl_threshold = random.uniform(0, 1)
				if expl_threshold > exploration_rate:
					# Get action from q-dict
					action, max_value = self.get_best_action(state, goal)
				else:
					# random action
					num_actions = len(state.get_actions())
					random_action_idx = random.randint(0, num_actions - 1)
					action = state.get_actions()[random_action_idx]

				new_state_tuple, reward, done = self.env.step(action)

				new_state = new_state_tuple[0]

				new_action, new_max_value = self.get_best_action(new_state, goal)
				self.q_dict[(state, goal, action)] = (1 - alpha) * self.get_value_from_q_dict(state, goal, action) + alpha * (reward + discount_rate * new_max_value)

				state = new_state

				if done == True:
					break

			exploration_rate = min_exploration_rate + (max_exploration_rate - min_exploration_rate) * math.exp(-exploration_decay_rate * episode)
			episode += 1

	def act(self, s):
		action, max_value = self.get_best_action(s[0], s[1])
		return action


if __name__ == '__main__':
	# Here you can test your algorithm. Stick with N <= 4
	# N = 4
	N = 4

	env = BlockWorldEnv(N)
	qlearning = QLearning(env)

	# Train
	qlearning.train()

	# Evaluate
	test_env = BlockWorldEnv(N)

	test_problems = 100
	solved = 0
	avg_steps = []

	for test_id in range(test_problems):
		s = test_env.reset()
		done = False

		print(f"\nProblem {test_id}:")
		print(f"{s[0]} -> {s[1]}")

		for step in range(50): 	# max 50 steps per problem
			a = qlearning.act(s)
			s_, r, done = test_env.step(a)

			print(f"{a}: {s[0]}")

			s = s_

			if done:
				solved += 1
				avg_steps.append(step + 1)
				break

	avg_steps = sum(avg_steps) / len(avg_steps)
	print(f"Solved {solved}/{test_problems} problems, with average number of steps {avg_steps}.")