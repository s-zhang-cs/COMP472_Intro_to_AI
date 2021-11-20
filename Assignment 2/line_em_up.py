import time
import sys
import numpy as np
from scipy.spatial.distance import pdist
from collections import Counter

class Game:
	MINIMAX = 0
	ALPHABETA = 1
	HUMAN = 2
	AI = 3

	def __init__(self, board_size, num_blocs, pos_blocs, win_size, max_depth_X, max_depth_O, max_time, minimax_alphabeta_switch, recommend = True):
		self.initialize_game(board_size, num_blocs, pos_blocs, win_size)
		self.minimax_alphabeta_switch = minimax_alphabeta_switch
		self.recommend = recommend
		self.max_depth_X = max_depth_X
		self.max_depth_O = max_depth_O
		self.max_time = max_time
		# stats
		self.evaluation_time_h1 = []
		self.evaluation_time_h2 = []


	def initialize_game(self, board_size, num_blocs, pos_blocs, win_size):
		self.board_size = board_size
		self.win_size = win_size

		#grid initialization
		self.num_blocs = num_blocs
		self.pos_blocs = pos_blocs
		self.current_state = [['.' for x in range(board_size)] for y in range(board_size)]
		for block in pos_blocs:
			x = block[0]
			y = block[1]
			self.current_state[x][y] = 'B'

		# Player X always plays first
		self.player_turn = 'X'

		# #tests
		# self.current_state = [
		# 	['O', 'O', '.', 'B', '.'],
		# 	['X', 'B', '.', '.', '.'],
		# 	['B', 'X', '.', 'B', '.'],
		# 	['O', 'B', 'X', '.', '.'],
		# 	['.', 'O', 'B', 'X', '.']
		# ]
		#
		# self.current_state = [
		# 	['O', 'O', 'X', 'B', 'X'],
		# 	['X', 'B', 'X', 'X', 'O'],
		# 	['B', 'X', '.', 'B', 'O'],
		# 	['O', 'B', 'X', 'X', 'O'],
		# 	['X', 'O', 'B', 'O', 'O']
		# ]
		#
		# self.current_state = [
		# 	['O', 'O', 'O', 'B', 'X'],
		# 	['X', 'B', 'X', 'X', 'X'],
		# 	['B', 'O', 'O', 'B', 'O'],
		# 	['O', 'B', 'O', 'O', 'X'],
		# 	['X', 'O', 'B', 'X', 'X']
		# ]

	def draw_board(self):
		print()
		for x in range(0, self.board_size):
			for y in range(0, self.board_size):
				print(F'{self.current_state[x][y]}', end="")
			print()
		print()

	def register_board(self):
		self.register_game_trace("", True)
		for x in range(0, self.board_size):
			for y in range(0, self.board_size):
				self.register_game_trace(self.current_state[x][y], False)
			self.register_game_trace("", True)
		self.register_game_trace("", True)

	def is_valid(self, px, py):
		if px < 0 or px > self.board_size - 1 or py < 0 or py > self.board_size - 1:
			return False
		elif self.current_state[px][py] != '.':
			return False
		else:
			return True

	def is_end(self):
		# Vertical win
		symbol = 'S'
		for i in range(0, self.board_size):
			win_count = 0
			for j in range(0, self.board_size):
				# user input
				if (self.current_state[j][i] == 'X' or self.current_state[j][i] == 'O'):
					# different from prev
					if (symbol != self.current_state[j][i]):
						win_count = 1
					# same as prev
					else:
						win_count = win_count + 1
					symbol = self.current_state[j][i]

				# default or block
				else:
					win_count = 0
					symbol = 'S'

				if (win_count >= self.win_size):
					return self.current_state[j][i]

		# Horizontal win
		symbol = 'S'
		for i in range(0, self.board_size):
			win_count = 0
			for j in range(0, self.board_size):
				# user input
				if(self.current_state[i][j] == 'X' or self.current_state[i][j] == 'O'):
					# different from prev
					if(symbol != self.current_state[i][j]):
						win_count = 1
					# same as prev
					else:
						win_count = win_count + 1
					symbol = self.current_state[i][j]

				# default or block
				else:
					win_count = 0
					symbol = 'S'

				if(win_count >= self.win_size):
					return self.current_state[i][j]


		# diagonals: /
		current_state_np = np.array(self.current_state)
		diags = [current_state_np[::-1, :].diagonal(i) for i in range(-current_state_np.shape[0] + 1, current_state_np.shape[1])]
		for diag in diags:
			symbol = 'S'
			win_count = 0
			for item in diag:
				# user input
				if(item == 'X' or item == 'O'):
					# different from prev
					if (symbol != item):
						win_count = 1
					# same as prev
					else:
						win_count = win_count + 1
					symbol = item
				# default or block
				else:
					win_count = 0
					symbol = 'S'
				if(win_count >= self.win_size):
					return item

		# diagonals: \
		diags = [current_state_np.diagonal(i) for i in range(current_state_np.shape[1] - 1, -current_state_np.shape[0], -1)]
		for diag in diags:
			symbol = 'S'
			win_count = 0;
			for item in diag:
				# user input
				if(item == 'X' or item == 'O'):
					# different from prev
					if (symbol != item):
						win_count = 1
					# same as prev
					else:
						win_count = win_count + 1
					symbol = item
				# default or block
				else:
					win_count = 0
					symbol = 'S'
				if(win_count >= self.win_size):
					return item

		# Is whole board full?
		for i in range(0, self.board_size):
			for j in range(0, self.board_size):
				# There's an empty field, we continue the game
				if (self.current_state[i][j] == '.'):
					return None
		# It's a tie!
		return '.'

	def check_end(self):
		self.result = self.is_end()
		# Printing the appropriate message if the game has ended
		if self.result != None:
			if self.result == 'X':
				print('The winner is X!')
			elif self.result == 'O':
				print('The winner is O!')
			elif self.result == '.':
				print("It's a tie!")
			# self.initialize_game()
		return self.result

	def input_move(self):
		while True:
			print(F'Player {self.player_turn}, enter your move:')
			px = int(input('enter the x coordinate: '))
			py = int(input('enter the y coordinate: '))
			if self.is_valid(px, py):
				return (px,py)
			else:
				print('The move is not valid! Try again.')

	def switch_player(self):
		if self.player_turn == 'X':
			self.player_turn = 'O'
		elif self.player_turn == 'O':
			self.player_turn = 'X'
		return self.player_turn

	def h2_eval(self, row_col_diag):
		# minimizing for X and maximizing for O
		prev = 'B'
		eval = 0
		consec = 0
		for item in row_col_diag:
			# new user consec sequence
			if(item != prev and (prev == 'B' or prev == '.')):
				consec = 1
			# user consec sequence interrupted
			elif(item != prev and prev != 'B' and prev != '.'):
				# X
				if(prev == 'X'):
					eval = eval - pow(2, consec)
				# O
				else:
					eval = eval + pow(2, consec)
				consec = 1
			# user consec sequence continues
			elif(item == prev and item != 'B' and item != '.'):
				consec = consec + 1
				# reached winning condition
				if(consec >= self.win_size):
					if(item == 'X'):
						return -sys.maxsize
					else:
						return sys.maxsize

			# reset consec when encountering non-user symbol
			if(item == 'B' or item == '.'):
				consec = 0

			prev = item

		if(prev == 'X'):
			eval = eval - pow(2, consec)
		elif(prev == 'O'):
			eval = eval + pow(2, consec)

		return eval

	def heuristic2(self):
		# minimizing for X and maximizing for O
		# intuition:
		# for every row, column, diagonal
		# we would have consecutive 'X's or 'O's, more consecutive = better
		# this heuristic tries to evaluate the board by calculating how many consecutive pieces each player has
		# longer consecutive sequences hold more weight than shorter ones
		eval = 0

		current_state_np = np.array(self.current_state)
		# rows
		for row in current_state_np:
			curr_eval = self.h2_eval(row)
			if(curr_eval == sys.maxsize or curr_eval == -sys.maxsize):
				return curr_eval
			eval = eval + curr_eval

		# # columns
		for col in current_state_np.T:
			curr_eval = self.h2_eval(col)
			if(curr_eval == sys.maxsize or curr_eval == -sys.maxsize):
				return curr_eval
			eval = eval + curr_eval

		# diagonals: /
		diags = [current_state_np[::-1, :].diagonal(i) for i in range(-current_state_np.shape[0] + 1, current_state_np.shape[1])]
		for diag in diags:
			curr_eval = self.h2_eval(diag)
			if(curr_eval == sys.maxsize or curr_eval == -sys.maxsize):
				return curr_eval
			eval = eval + curr_eval

		# # diagonals: \
		diags = [current_state_np.diagonal(i) for i in range(current_state_np.shape[1] - 1, -current_state_np.shape[0], -1)]
		for diag in diags:
			curr_eval = self.h2_eval(diag)
			if(curr_eval == sys.maxsize or curr_eval == -sys.maxsize):
				return curr_eval
			eval = eval + curr_eval

		return eval

	def heuristic1(self):
		# minimizing for X and maximizing for O
		# intuition:
		# for either 'X' or 'O', the more they spread, the less likely they will form a line of a certain length
		# this heuristic is a measure of dispersion between pieces of the same color by calculating the distance between them

		num_X = 0
		for i in range(0, self.board_size):
			for j in range(0, self.board_size):
				if(self.current_state[i][j] == 'X'):
					num_X = num_X + 1

		point_matrix_for_X = [['.' for x in range(2)] for y in range(num_X)]

		index = 0
		for i in range(0, self.board_size):
			for j in range(0, self.board_size):
				if(self.current_state[i][j] == 'X'):
					point_matrix_for_X[index][0] = i
					point_matrix_for_X[index][1] = j
					index = index + 1

		avg_distance_X = np.mean(pdist(point_matrix_for_X))
		return avg_distance_X

	def register_num_states_evaluated(self, depth):
		if depth in self.num_states_evaluated.keys():
			self.num_states_evaluated[depth] = self.num_states_evaluated[depth] + 1
		else:
			self.num_states_evaluated[depth] = 1

	def minimax(self, X_or_O, depth, max=False):
		# Minimizing for 'X' and maximizing for 'O'
		# Possible values are:
		# -sys.maxsize - win for 'X'
		# 0  - a tie
		# sys.maxsize  - win for 'O'
		value = sys.maxsize
		if max:
			value = -sys.maxsize
		x = None
		y = None

		# check if game ended
		result = self.is_end()
		if result == 'X':
			self.register_num_states_evaluated(depth)
			if(self.h1_h2_switch):
				self.total_states_h1 = self.total_states_h1 + 1
			else:
				self.total_states_h2 = self.total_states_h2 + 1
			return (-sys.maxsize, x, y)
		elif result == 'O':
			self.register_num_states_evaluated(depth)
			if(self.h1_h2_switch):
				self.total_states_h1 = self.total_states_h1 + 1
			else:
				self.total_states_h2 = self.total_states_h2 + 1
			return (sys.maxsize, x, y)
		elif result == '.':
			self.register_num_states_evaluated(depth)
			if(self.h1_h2_switch):
				self.total_states_h1 = self.total_states_h1 + 1
			else:
				self.total_states_h2 = self.total_states_h2 + 1
			return (0, x, y)

		# if no more time, stop recursion and use heuristic right away(leave 0.5s to do so)
		if(time.time() - self.timer_start > self.max_time - 0.5):
			self.register_num_states_evaluated(depth)
			self.ended_early = True
			if (self.h1_h2_switch):
				self.total_states_h1 = self.total_states_h1 + 1
				return (self.heuristic1(), x, y)
			else:
				self.total_states_h2 = self.total_states_h2 + 1
				return (self.heuristic2(), x, y)

		# after a certain depth's permutation, use heuristic to evaluate current state of game
		#player 1
		if(X_or_O and depth >= self.max_depth_X):
			self.register_num_states_evaluated(depth)
			if(self.h1_h2_switch):
				self.total_states_h1 = self.total_states_h1 + 1
				return (self.heuristic1(), x, y)
			else:
				self.total_states_h2 = self.total_states_h2 + 1
				return (self.heuristic2(), x, y)
		#player 2
		if((not X_or_O) and depth >= self.max_depth_O):
			self.register_num_states_evaluated(depth)
			if(self.h1_h2_switch):
				self.total_states_h1 = self.total_states_h1 + 1
				return (self.heuristic1(), x, y)
			else:
				self.total_states_h2 = self.total_states_h2 + 1
				return (self.heuristic2(), x, y)

		# when all scenarios are losing, x and y will remain 'None' and not be initialized. To remedy this, these
		# variables below will pick the coordinates of the 1st losing scenario as x and y.
		cood_x = None
		cood_y = None

		# state-space permutations
		for i in range(0, self.board_size):
			for j in range(0, self.board_size):
				if self.current_state[i][j] == '.':
					if(cood_x is None and cood_y is None):
						cood_x = i
						cood_y = j
					if max:
						self.current_state[i][j] = 'O'
						(v, _, _) = self.minimax(X_or_O, depth + 1, max=False)
						if v > value:
							value = v
							x = i
							y = j
					else:
						self.current_state[i][j] = 'X'
						(v, _, _) = self.minimax(X_or_O, depth + 1, max=True)
						if v < value:
							value = v
							x = i
							y = j
					self.current_state[i][j] = '.'

		if(x is None and y is None):
			if(self.h1_h2_switch):
				self.total_states_h1 = self.total_states_h1 + 1
			else:
				self.total_states_h2 = self.total_states_h2 + 1
			return (value, cood_x, cood_y)
		if (self.h1_h2_switch):
			self.total_states_h1 = self.total_states_h1 + 1
		else:
			self.total_states_h2 = self.total_states_h2 + 1
		return (value, x, y)

	def alphabeta(self, X_or_O, depth, alpha=-sys.maxsize, beta=sys.maxsize, max=False):
		# Minimizing for 'X' and maximizing for 'O'
		# Possible values are:
		# -sys.maxsize - win for 'X'
		# 0  - a tie
		# sys.maxsize  - win for 'O'

		value = sys.maxsize
		if max:
			value = -sys.maxsize
		x = None
		y = None

		# check if game ended
		result = self.is_end()
		if result == 'X':
			self.register_num_states_evaluated(depth)
			if(self.h1_h2_switch):
				self.total_states_h1 = self.total_states_h1 + 1
			else:
				self.total_states_h2 = self.total_states_h2 + 1
			return (-sys.maxsize, x, y)
		elif result == 'O':
			self.register_num_states_evaluated(depth)
			if(self.h1_h2_switch):
				self.total_states_h1 = self.total_states_h1 + 1
			else:
				self.total_states_h2 = self.total_states_h2 + 1
			return (sys.maxsize, x, y)
		elif result == '.':
			self.register_num_states_evaluated(depth)
			if(self.h1_h2_switch):
				self.total_states_h1 = self.total_states_h1 + 1
			else:
				self.total_states_h2 = self.total_states_h2 + 1
			return (0, x, y)

		# if no more time, stop recursion and use heuristic right away(leave 0.5s to do so)
		if(time.time() - self.timer_start > self.max_time - 0.5):
			self.register_num_states_evaluated(depth)
			self.ended_early = True
			if (self.h1_h2_switch):
				self.total_states_h1 = self.total_states_h1 + 1
				return (self.heuristic1(), x, y)
			else:
				self.total_states_h2 = self.total_states_h2 + 1
				return (self.heuristic2(), x, y)

		# after a certain depth's permutation, use heuristic to evaluate current state of game
		# leaving x, y as None here is okay, because they will be discarded anyway during recursion
		#player 1
		if(X_or_O and depth >= self.max_depth_X):
			self.register_num_states_evaluated(depth)
			if(self.h1_h2_switch):
				self.total_states_h1 = self.total_states_h1 + 1
				return (self.heuristic1(), x, y)
			else:
				self.total_states_h2 = self.total_states_h2 + 1
				return (self.heuristic2(), x, y)
		#player 2
		if((not X_or_O) and depth >= self.max_depth_O):
			self.register_num_states_evaluated(depth)
			if(self.h1_h2_switch):
				self.total_states_h1 = self.total_states_h1 + 1
				return (self.heuristic1(), x, y)
			else:
				self.total_states_h2 = self.total_states_h2 + 1
				return (self.heuristic2(), x, y)

		# when all scenarios are losing, x and y will remain 'None' and not be initialized. To remedy this, these
		# variables below will pick the coordinates of the 1st losing scenario as x and y.
		cood_x = None
		cood_y = None

		# state-space permutations
		for i in range(0, self.board_size):
			for j in range(0, self.board_size):
				if self.current_state[i][j] == '.':
					if(cood_x is None and cood_y is None):
						cood_x = i
						cood_y = j
					if max:
						self.current_state[i][j] = 'O'
						(v, _, _) = self.alphabeta(X_or_O, depth + 1, alpha, beta, max=False)
						if v > value:
							value = v
							x = i
							y = j
					else:
						self.current_state[i][j] = 'X'
						(v, _, _) = self.alphabeta(X_or_O, depth + 1, alpha, beta, max=True)
						if v < value:
							value = v
							x = i
							y = j
					self.current_state[i][j] = '.'

					# alpha-beta pruning
					if max:
						if value >= beta:
							return (value, i, j)
						if value > alpha:
							alpha = value
					else:
						if value <= alpha:
							return (value, i, j)
						if value < beta:
							beta = value

		if(x is None and y is None):
			if(self.h1_h2_switch):
				self.total_states_h1 = self.total_states_h1 + 1
			else:
				self.total_states_h2 = self.total_states_h2 + 1
			return (value, cood_x, cood_y)
		if (self.h1_h2_switch):
			self.total_states_h1 = self.total_states_h1 + 1
		else:
			self.total_states_h2 = self.total_states_h2 + 1
		return (value, x, y)

	def register_game_initialization(self, player_x, player_o):
		self.register_game_trace("board size = " + str(self.board_size) + ", number of blocs = " + str(self.num_blocs) + ", win size (consecutive pieces) = " + str(self.win_size) + ", maximum time allowed = " + str(self.max_time), True)
		self.register_game_trace("blocs = " + str(self.pos_blocs), True)
		# yea, ugly code, but it only executes once per run, and is really just hard for human to read but
		# not really a performance loss as it turns to goto during execution. Also, deadline.. /(>.<)\
		if(player_x == Game.AI):
			if(player_o == Game.AI):
				if(self.minimax_alphabeta_switch):
					if(self.player_X_heuristic == 0):
						self.register_game_trace("Player_X: AI, d = " + str(self.max_depth_X) + ", minimax, e1", True)
					else:
						self.register_game_trace("Player_X: AI, d = " + str(self.max_depth_X) + ", minimax, e2", True)
					if(self.player_O_heuristic == 0):
						self.register_game_trace("Player_O: AI, d = " + str(self.max_depth_O) + ", minimax, e1", True)
					else:
						self.register_game_trace("Player_O: AI, d = " + str(self.max_depth_O) + ", minimax, e2", True)
				else:
					if(self.player_X_heuristic == 0):
						self.register_game_trace("Player_X: AI, d = " + str(self.max_depth_X) + ", alphabeta, e1", True)
					else:
						self.register_game_trace("Player_O: AI, d = " + str(self.max_depth_O) + ", alphabeta, e2", True)
					if (self.player_O_heuristic == 0):
						self.register_game_trace("Player_X: AI, d = " + str(self.max_depth_X) + ", alphabeta, e1", True)
					else:
						self.register_game_trace("Player_O: AI, d = " + str(self.max_depth_O) + ", alphabeta, e2", True)
			else:
				if (self.minimax_alphabeta_switch):
					if (self.player_X_heuristic):
						self.register_game_trace("Player_X: AI, d = " + str(self.max_depth_X) + ", minimax, e1", True)
					else:
						self.register_game_trace("Player_O: H, d = " + str(self.max_depth_O) + ", minimax, e2", True)
					if(self.player_O_heuristic):
						self.register_game_trace("Player_X: AI, d = " + str(self.max_depth_X) + ", minimax, e1", True)
					else:
						self.register_game_trace("Player_O: H, d = " + str(self.max_depth_O) + ", minimax, e2", True)
				else:
					if (self.player_X_heuristic):
						self.register_game_trace("Player_X: AI, d = " + str(self.max_depth_X) + ", alphabeta, e1", True)
					else:
						self.register_game_trace("Player_O: H, d = " + str(self.max_depth_O) + ", alphabeta, e2", True)
					if(self.player_O_heuristic):
						self.register_game_trace("Player_X: AI, d = " + str(self.max_depth_X) + ", alphabeta, e1", True)
					else:
						self.register_game_trace("Player_O: H, d = " + str(self.max_depth_O) + ", alphabeta, e2", True)
		else:
			if (player_o == Game.AI):
				if (self.minimax_alphabeta_switch):
					if (self.player_X_heuristic):
						self.register_game_trace("Player_X: H, d = " + str(self.max_depth_X) + ", minimax, e1", True)
					else:
						self.register_game_trace("Player_O: AI, d = " + str(self.max_depth_O) + ", minimax, e2", True)
					if(self.player_O_heuristic):
						self.register_game_trace("Player_X: H, d = " + str(self.max_depth_X) + ", minimax, e1", True)
					else:
						self.register_game_trace("Player_O: AI, d = " + str(self.max_depth_O) + ", minimax, e2", True)
				else:
					if (self.player_X_heuristic):
						self.register_game_trace("Player_X: H, d = " + str(self.max_depth_X) + ", alphabeta, e1", True)
					else:
						self.register_game_trace("Player_O: AI, d = " + str(self.max_depth_O) + ", alphabeta, e2", True)
					if(self.player_O_heuristic):
						self.register_game_trace("Player_X: H, d = " + str(self.max_depth_X) + ", alphabeta, e1", True)
					else:
						self.register_game_trace("Player_O: AI, d = " + str(self.max_depth_O) + ", alphabeta, e2", True)
			else:
				if (self.minimax_alphabeta_switch):
					if (self.player_X_heuristic):
						self.register_game_trace("Player_X: H, d = " + str(self.max_depth_X) + ", minimax, e1", True)
					else:
						self.register_game_trace("Player_O: H, d = " + str(self.max_depth_O) + ", minimax, e2", True)
					if(self.player_O_heuristic):
						self.register_game_trace("Player_X: H, d = " + str(self.max_depth_X) + ", minimax, e1", True)
					else:
						self.register_game_trace("Player_O: H, d = " + str(self.max_depth_O) + ", minimax, e2", True)
				else:
					if (self.player_X_heuristic):
						self.register_game_trace("Player_X: H, d = " + str(self.max_depth_X) + ", alphabeta, e1", True)
					else:
						self.register_game_trace("Player_O: H, d = " + str(self.max_depth_O) + ", alphabeta, e2", True)
					if(self.player_O_heuristic):
						self.register_game_trace("Player_X: H, d = " + str(self.max_depth_X) + ", alphabeta, e1", True)
					else:
						self.register_game_trace("Player_O: H, d = " + str(self.max_depth_O) + ", alphabeta, e2", True)

	def play(self, player_x, player_o, player_X_heuristic = 0, player_O_heuristic = 0):
		self.player_X_heuristic = player_X_heuristic
		self.player_O_heuristic = player_O_heuristic
		self.total_states_h1 = 0
		self.total_states_h2 = 0
		self.total_moves = 0
		self.total_num_states_evaluated = {}
		self.register_game_initialization(player_x, player_o)
		if(self.minimax_alphabeta_switch):
			algo = self.MINIMAX
		else:
			algo = self.ALPHABETA
		while True:
			# game statistics
			self.num_states_evaluated = {}
			self.draw_board()
			self.register_board()
			if self.check_end():
				if not self.evaluation_time_h1:
					h1_average = None
				else:
					h1_average = np.average(self.evaluation_time_h1)
				if not self.evaluation_time_h2:
					h2_average = None
				else:
					h2_average = np.average(self.evaluation_time_h2)
				self.register_game_trace("i Average evaluation time: h1 = " + str(h1_average) + ", h2 = " + str(h2_average), True)
				self.register_game_trace("ii Total heuristic evaluations: h1 = " + str(self.total_states_h1) + ", h2 = " + str(self.total_states_h2), True)
				self.register_game_trace("iii Evaluations by depth: " + str(self.total_num_states_evaluated), True)
				self.register_game_trace("vi Total moves: " + str(self.total_moves), True)
				return
			start = time.time()
			self.timer_start = start
			self.ended_early = False
			if algo == self.MINIMAX:
				if self.player_turn == 'X':
					self.h1_h2_switch = player_X_heuristic
					(_, x, y) = self.minimax(True, 0, max=False)
				else:
					self.h1_h2_switch = player_O_heuristic
					(_, x, y) = self.minimax(False, 0, max=True)
			else: # algo == self.ALPHABETA
				if self.player_turn == 'X':
					self.h1_h2_switch = player_X_heuristic
					(m, x, y) = self.alphabeta(True, 0, max=False)
				else:
					self.h1_h2_switch = player_O_heuristic
					(m, x, y) = self.alphabeta(False, 0, max=True)
			end = time.time()
			self.total_moves = self.total_moves + 1
			if(self.h1_h2_switch):
				self.evaluation_time_h1.append(end - start)
			else:
				self.evaluation_time_h2.append(end - start)
			add_dict = Counter(self.total_num_states_evaluated) + Counter(self.num_states_evaluated)
			self.total_num_states_evaluated = dict(add_dict)
			if (self.player_turn == 'X' and player_x == self.HUMAN) or (self.player_turn == 'O' and player_o == self.HUMAN):
					if self.recommend:
						print(F'Evaluation time: {round(end - start, 7)}s')
						print(F'Recommended move: x = {x}, y = {y}')
					(x,y) = self.input_move()
			if (self.player_turn == 'X' and player_x == self.AI) or (self.player_turn == 'O' and player_o == self.AI):
						print(F'Evaluation time: {round(end - start, 7)}s')
						print(F'Player {self.player_turn} under AI control plays: x = {x}, y = {y}')
						self.register_game_trace("", True)
						self.register_game_trace("Player " + self.player_turn + " under AI controls plays: x = " + str(x) + ", y = " + str(y), True)
						self.register_game_trace("", True)

						# turn statistics
						if(self.ended_early):
							self.register_game_trace("~~~ This node search ended early because it is approaching max time. ~~~", True)
						self.register_game_trace("i Evaluation time: " + str(round(end - start, 7)),True)
						self.register_game_trace("ii Heuristic evaluations: " + str(sum(self.num_states_evaluated.values())), True)
						self.register_game_trace(("iii Evaluations by depth: " + str(self.num_states_evaluated)), True)
						self.register_game_trace("iv Average evaluation depth: " + str(self.calculate_weighted_average_from_dict(self.num_states_evaluated)), True)

			self.current_state[x][y] = self.player_turn
			self.switch_player()

	def calculate_weighted_average_from_dict(self, dict):
		total = 0
		count = 0
		for k, v in dict.items():
			total += k * v
			count += v
		mean = total / count
		return mean


	def register_game_trace(self, content, newLine):
		filename = "gameTrace-" + str(self.board_size) + str(self.num_blocs) + str(self.win_size) + str(self.max_time) + ".txt"
		with open(filename, 'a+') as f:
			if(newLine):
				f.write(content + "\n")
			else:
				f.write(content)


def main():
	g = Game(board_size = 4, num_blocs = 1, pos_blocs = [(1,3)], win_size = 4, max_depth_X = 10, max_depth_O = 10, max_time = 5, minimax_alphabeta_switch = False, recommend=True)
	# 0 for heuristic 1, 1 for heuristic 2 (default: both heuristic 1)
	g.play(player_x=Game.AI, player_o=Game.AI, player_X_heuristic=1, player_O_heuristic=1)

if __name__ == "__main__":
	main()

