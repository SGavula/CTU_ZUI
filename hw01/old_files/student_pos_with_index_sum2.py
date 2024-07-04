from queue import PriorityQueue
from blockworld import BlockWorld
import numpy as np

class BlockWorldHeuristic(BlockWorld):
	def __init__(self, num_blocks=5, state=None):
		BlockWorld.__init__(self, num_blocks, state)

	# Potrebujem najst krabicu v ktorej sa nachadza cislo a potom potrebujem index toho cisla v tej krabici
	def heuristic(self, reversed_goal_state, goal_state):
		# print("Self number of blocks: ", self.num_blocks)
		# self_state = self.get_state()
		# goal_state = goal.get_state()
		self_state = [sublist[::-1] for sublist in self.get_state()]
		# print("Self state: ", self_state)
	
		reversed_goal_dic = {}
		goal_dic = {}

		score = 0

		for crate in reversed_goal_state:
			for num in crate:
				# print("Number: ", num)
				reversed_goal_dic[num] = crate.index(num)

		for crate in goal_state:
			for num in crate:
				# print("Number: ", num)
				goal_dic[num] = crate.index(num) 
		
		# print("Self state: ", self_state)
		for crate in self_state:
			for num in crate:
				index = crate.index(num)
				if reversed_goal_dic[num] != index:
					score += 10
				else:
					score += index
		# print(len(goal_state))
		# if len(goal_state) < 4:
			# for crate in self.get_state():
			# 	for num in crate:
			# 		index = crate.index(num)
			# 		if goal_dic[num] != index:
			# 			score += 10
			# 		else:
			# 			score += index
		# print("Index: ", score)

		# print("Goal dictionary: ", goal_dic)

		return score

class AStar():
	def search(self, start, goal):
		# ToDo. Return a list of optimal actions that takes start to goal.
		
		# You can access all actions and neighbors like this:
		# for action, neighbor in state.get_neighbors():
		# 	...

		reversed_goal = [sublist[::-1] for sublist in goal.get_state()]


		print("Start: ", start.get_actions())
		print("Goal: ", goal.get_state())
		print("Reversed Goal: ", reversed_goal)
		
		# Closed sets
		closed_sets = []
		open_sets = [start]
		# Open sets
		queue = PriorityQueue()
		
		queue.put((0, 0, [], start))

		while not queue.empty():
			priority, depth, moves, curr_state = queue.get()
			print("Current state: ", curr_state)
			
			new_depth = depth + 1

			# print("State: ", f"Priority: {priority} | Depth: {depth} | Moves: {moves} | Current state: {curr_state}")
			# print("Open sets: ", open_sets)
			
			if curr_state == goal:
				# print(moves)
				return moves

			for action, neighbour in curr_state.get_neighbors():
				score = neighbour.heuristic(reversed_goal, goal.get_state())
				if neighbour not in open_sets:
					if neighbour not in closed_sets:
						# print("Adding to queue: ", neighbour)
						# print("Action: ", action)
						# print("Moves: ", moves)
						new_moves = moves.copy()
						new_moves.append(action)
						# queue.put((score + new_depth, new_depth, new_moves, neighbour))
						queue.put((score, new_depth, new_moves, neighbour))
						open_sets.append(neighbour)
				# else:
					# print("Is in closed set or in open sets: ", curr_state)
			# print("Open sets after: ", open_sets)
			closed_sets.append(curr_state)

if __name__ == '__main__':
	# Here you can test your algorithm. You can try different N values, e.g. 6, 7.
	N = 9

	# start = BlockWorldHeuristic(N)
	# goal = BlockWorldHeuristic(N)

	# start = BlockWorldHeuristic(3, "[[1, 2], [3]]")
	# goal = BlockWorldHeuristic(3, "[[3, 2, 1]]")
	# start = BlockWorldHeuristic(7, "[[2], [6, 3], [7], [5, 1, 4]]")
	# goal = BlockWorldHeuristic(7, "[[7, 3, 5, 2, 1, 6], [4]]")
	start = BlockWorldHeuristic(8, "[[3, 8, 1, 5, 6, 2], [4], [7]]")
	goal = BlockWorldHeuristic(8, "[[7, 6, 1, 3, 2], [8, 4, 5]]")
	# start = BlockWorldHeuristic(9, "[[4, 1, 5, 7, 8, 6, 2, 3, 9]]")
	# goal = BlockWorldHeuristic(9, "[[4, 8, 3, 1, 2, 6, 5, 7, 9]]")
	# [[3, 8, 1, 5, 6, 2], [4], [7]] -> [[7, 6, 1, 3, 2], [8, 4, 5]]
	# [[4, 1, 5, 7, 8, 6, 2, 3, 9]] -> [[4, 8, 3, 1, 2, 6, 5, 7, 9]]
	# start = BlockWorldHeuristic(5, "[[3], [1, 5], [4], [2]]")
	# goal = BlockWorldHeuristic(5, "[[4, 1], [3, 5], [2]]")

	print("Searching for a path:")
	print(f"{start} -> {goal}")
	print()

	astar = AStar()
	path = astar.search(start, goal)

	# Testing
	# assert path == [(1, 0), (2, 1), (3, 2)]

	if path is not None:
		print("Found a path:")
		print(path)

		print("\nHere's how it goes:")

		s = start.clone()
		print(s)

		for a in path:
			s.apply(a)
			print(s)

	else:
		print("No path exists.")

	print("Total expanded nodes:", BlockWorld.expanded)