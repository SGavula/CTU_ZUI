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
		
		# Make goal directory with key box and saved values -> index of box and box below in goal state  
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

		# Calculate heuristic score if current state of the boxes
		for crate in self_state:
			for num in crate:
				index = crate.index(num)
				if goal_dic[num][0] != index:
					score += len(crate) - index
					break
				else:
					if index != 0:
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
				# print(moves)
				print("Number of moves: ", len(moves))
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

	# start = BlockWorldHeuristic(N)
	# goal = BlockWorldHeuristic(N)

	# start = BlockWorldHeuristic(3, "[[1, 2], [3]]")
    # goal = BlockWorldHeuristic(3, "[[3, 2, 1]]")
    # start = BlockWorldHeuristic(4, "[[3, 2, 1], [4]]")
    # goal = BlockWorldHeuristic(4, "[[4, 3, 2, 1]]")
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
	# start = BlockWorldHeuristic(8, "[[3, 6], [1, 4, 5, 2, 7, 8]]")
	# goal = BlockWorldHeuristic(8, "[[6], [3, 5, 2, 7, 8, 4, 1]]")
	# start = BlockWorldHeuristic(7, "[[5, 4, 1, 6, 3, 2, 7]]")
	# goal = BlockWorldHeuristic(7, "[[3, 4, 7, 6, 5, 1], [2]]")
	# start = BlockWorldHeuristic(7, "[[7, 6, 5, 4, 3, 2, 1]]")
	# goal = BlockWorldHeuristic(7, "[[1, 2, 3, 4, 5, 6, 7]]")
	start = BlockWorldHeuristic(9, "[[9, 7, 2, 3, 5], [8], [6, 1, 4]]")
	goal = BlockWorldHeuristic(9, "[[9, 4, 8, 7, 2, 6, 5, 3, 1]]")

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