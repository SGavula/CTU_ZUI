from queue import PriorityQueue
from blockworld import BlockWorld
import numpy as np

class BlockWorldHeuristic(BlockWorld):
	def __init__(self, num_blocks=5, state=None):
		BlockWorld.__init__(self, num_blocks, state)

	def heuristic(self, goal):
		# self_state = self.get_state()
		goal_state = goal.get_state()
		self_state = [sublist[::-1] for sublist in self.get_state()]
		# print("Self state: ", self_state)
	
		goal_dic = {}
		state_dic = {}
		score = 0
		
		# (Goal index, id of item below me, id of item above me)
		for crate in goal_state:
			for num in crate:
				# print("Number: ", num)
				if crate.index(num) == (len(crate) - 1):
					# Item on the bottom
					if len(crate) == 1:
						goal_dic[num] = (crate[::-1].index(num), -1, -1)
					else:	
						goal_dic[num] = (crate[::-1].index(num), -1, crate[crate.index(num) - 1])
				else:
					# Item not on the bottom, has some num below it
					below_idx = crate.index(num) + 1
					if crate.index(num) == 0:
						goal_dic[num] = (crate[::-1].index(num), crate[below_idx], -1)
					else:
						goal_dic[num] = (crate[::-1].index(num), crate[below_idx], crate[crate.index(num) - 1])

		# print("Goal directory: ", goal_dic)
		# print("Self state: ", self.get_state())
		# print("Self state reversed: ", self_state)

		for crate in self_state:
			for idx in range(len(crate)):
				num = crate[idx]
				if idx == 0:
					# I do not need to add score because it is on the position 0
					# The box on the bot
					if idx == goal_dic[num][0]:
						state_dic[num] = (True, 0)
						score -= 2
					else:
						state_dic[num] = (False, 0)
						score += 1
				else:				
					# The box on the top of some other box
					idx_below = idx - 1
					num_below = crate[idx_below]
					right_placed = (idx == goal_dic[num][0]) and (num_below == goal_dic[num][1]) and (state_dic[num_below][0] == True)
					# print(f"Number: {num} | Number below: {num_below} | Goal number below: {goal_dic[num][1]} | State dic {state_dic[num_below]} | {right_placed}")
					if right_placed == True:
						# Both numbers are correct placed
						curr_score = state_dic[num_below][1] - 1
						state_dic[num] = (True, curr_score)
						score += curr_score
					else:
						if state_dic[num_below][0] == True:
							# Current number is incorrect placed
							state_dic[num] = (False, 1)
							score += 1
						else:
							# Both numbers are incorrect placed
							curr_score = state_dic[num_below][1] + 1
							state_dic[num] = (False, curr_score)
							score += curr_score
		
		# print(f"Current state: {self_state} Score: {score}")
		return score

class AStar():
	def search(self, start, goal):
		# ToDo. Return a list of optimal actions that takes start to goal.
		
		# You can access all actions and neighbors like this:
		# for action, neighbor in state.get_neighbors():
		# 	...

		print("Start: ", start.get_actions())
		print("Goal: ", goal.get_state())
		# print("Reversed Goal: ", reversed_goal)
		
		# Closed sets
		open_sets = [start]
		# Open sets
		queue = PriorityQueue()
		
		queue.put((0, 0, [], start))

		while not queue.empty():
			priority, depth, moves, curr_state = queue.get()
			
			# print("State: ", f"Priority: {priority} | Depth: {depth} | Moves: {moves} | Current state: {curr_state}")
			
			new_depth = depth + 2
			
			if curr_state == goal:
				# print(moves)
				print("Number of moves: ", len(moves))
				return moves

			for action, neighbour in curr_state.get_neighbors():
				score = neighbour.heuristic(goal)
				if neighbour not in open_sets:
					new_moves = moves.copy()
					new_moves.append(action)
					queue.put((score + new_depth, new_depth, new_moves, neighbour))
					open_sets.append(neighbour)
			# print("Open sets after: ", open_sets)

if __name__ == '__main__':
	# Here you can test your algorithm. You can try different N values, e.g. 6, 7.
	N = 9

	# start = BlockWorldHeuristic(N)
	# goal = BlockWorldHeuristic(N)

	# start = BlockWorldHeuristic(3, "[[1, 2], [3]]")
	# goal = BlockWorldHeuristic(3, "[[3, 2, 1]]")
	# start = BlockWorldHeuristic(4, "[[6, 1], [7, 5]]")
	# goal = BlockWorldHeuristic(4, "[[1], [7, 6, 5]]")
	# start = BlockWorldHeuristic(5, "[[3], [1, 5], [4], [2]]")
	# goal = BlockWorldHeuristic(5, "[[4, 1], [3, 5], [2]]")
	# start = BlockWorldHeuristic(7, "[[2], [6, 3], [7], [5, 1, 4]]")
	# goal = BlockWorldHeuristic(7, "[[7, 3, 5, 2, 1, 6], [4]]")
	# start = BlockWorldHeuristic(8, "[[3, 8, 1, 5, 6, 2], [4], [7]]")
	# goal = BlockWorldHeuristic(8, "[[7, 6, 1, 3, 2], [8, 4, 5]]")
	# start = BlockWorldHeuristic(9, "[[4, 1, 5, 7, 8, 6, 2, 3, 9]]")
	# goal = BlockWorldHeuristic(9, "[[4, 8, 3, 1, 2, 6, 5, 7, 9]]")
	# start = BlockWorldHeuristic(7, "[[6, 7, 1, 4], [5], [3], [2]]")
	# goal = BlockWorldHeuristic(7, "[[3, 7, 5, 4, 1], [2, 6]]")
	# start = BlockWorldHeuristic(7, "[[1, 7, 3, 5, 6], [4, 2]]")
	# goal = BlockWorldHeuristic(7, "[[3, 7, 6, 4, 5], [2], [1]]")
	# start = BlockWorldHeuristic(8, "[[5, 7, 2, 1, 8, 3, 6], [4]]")
	# goal = BlockWorldHeuristic(8, "[[3, 2, 6, 4, 5], [8, 7, 1]]")
	# start = BlockWorldHeuristic(8, "[[7, 6], [4], [5, 1, 8], [3, 2]]")
	# goal = BlockWorldHeuristic(8, "[[4, 5, 3, 6, 8], [1, 7, 2]]")
	start = BlockWorldHeuristic(8, "[[3, 6], [1, 4, 5, 2, 7, 8]]")
	goal = BlockWorldHeuristic(8, "[[6], [3, 5, 2, 7, 8, 4, 1]]")
	# start = BlockWorldHeuristic(7, "[[5, 4, 1, 6, 3, 2, 7]]")
	# goal = BlockWorldHeuristic(7, "[[3, 4, 7, 6, 5, 1], [2]]")
	# start = BlockWorldHeuristic(7, "[[7, 6, 5, 4, 3, 2, 1]]")
	# goal = BlockWorldHeuristic(7, "[[1, 2, 3, 4, 5, 6, 7]]")
	# 7/1 [[5, 4, 1, 6, 3, 2, 7]] -> [[3, 4, 7, 6, 5, 1], [2]]
	# [[3, 8, 1, 5, 6, 2], [4], [7]] -> [[7, 6, 1, 3, 2], [8, 4, 5]]
	# [[3, 8, 1, 5, 9], [4, 2, 7], [6]] -> [[8, 4, 5, 7, 1, 6, 2, 9], [3]]
	# [[6, 7, 1, 4], [5], [3], [2]] -> [[3, 7, 5, 4, 1], [2, 6]]
	# 8/1 [[5, 7, 2, 1, 8, 3, 6], [4]] -> [[3, 2, 6, 4, 5], [8, 7, 1]]
	# 8/2 [[7, 6], [4], [5, 1, 8], [3, 2]] -> [[4, 5, 3, 6, 8], [1, 7, 2]]
	# 8/0 [[3, 6], [1, 4, 5, 2, 7, 8]] -> [[6], [3, 5, 2, 7, 8, 4, 1]]

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