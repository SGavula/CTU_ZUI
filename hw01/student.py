from queue import PriorityQueue
from blockworld import BlockWorld
import numpy as np

class BlockWorldHeuristic(BlockWorld):
	def __init__(self, num_blocks=5, state=None):
		BlockWorld.__init__(self, num_blocks, state)

	def heuristic(self, goal):
		# Reverse boxes to make bottom box the first box in the list
		goal_state = [sublist[::-1] for sublist in goal.get_state()]
		self_state = [sublist[::-1] for sublist in self.get_state()]
	
		goal_dic = {}
		score = 0
		
		# Make goal directory with key box and saved values -> index of box and if of box below the current box in goal state  
		# (Goal index, id of item below me)
		for crate in goal_state:
			for num in crate:
				if crate.index(num) == 0:
					# Item on the bottom
					goal_dic[num] = (crate.index(num), -1)
				else:
					# Item not on the bottom, has some num below it
					below_idx = crate.index(num) - 1
					goal_dic[num] = (crate.index(num), crate[below_idx])

		# Calculate heuristic score for current state of the boxes
		for crate in self_state:
			for num in crate:
				index = crate.index(num)
				if goal_dic[num][0] != index:
					score += len(crate) - index
					break
				else:
					if index == 0:
						continue
					curr_below_idx = index - 1
					if crate[curr_below_idx] != goal_dic[num][1]:
						score += len(crate) - index
						break
		
		return score

class AStar():
	def search(self, start, goal):
		# ToDo. Return a list of optimal actions that takes start to goal.
		
		# You can access all actions and neighbors like this:
		# for action, neighbor in state.get_neighbors():
		# 	...
		
		# Open sets
		open_sets = [start]
		queue = PriorityQueue()
		
		order_in_queue = 0
		
		queue.put((0, 0, order_in_queue, 0, [], start))

		# Depth Breadth Search with priority queue
		while not queue.empty():
			priority, score, order_in_queue, depth, moves, curr_state = queue.get()
			
			new_depth = depth + 1
			
			if curr_state == goal:
				return moves

			for action, neighbour in curr_state.get_neighbors():
				score = neighbour.heuristic(goal)
				if neighbour not in open_sets:
					new_moves = moves.copy()
					new_moves.append(action)
					order_in_queue += 1
					queue.put((score + new_depth, score, order_in_queue, new_depth, new_moves, neighbour))
					open_sets.append(neighbour)
			

if __name__ == '__main__':
	# Here you can test your algorithm. You can try different N values, e.g. 6, 7.
	N = 9

	start = BlockWorldHeuristic(N)
	goal = BlockWorldHeuristic(N)

	print("Searching for a path:")
	print(f"{start} -> {goal}")
	print()

	astar = AStar()
	path = astar.search(start, goal)

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