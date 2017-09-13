
import random
import pygame
# import Chess_GUI

class IzzI():
	def __init__(self, state=None):
		self.white_pieces = "PNBRQ" # excludes king
		self.black_pieces = "pnbrq"
		self.ranks = [8, 7, 6, 5, 4, 3, 2, 1]
		self.current_state = []
		self.turn = 0
		self.booo = 	"xxxxxxxxxx" \
			"xxxxxxxxxx" \
			"xrnbqkbnrx" \
			"xppppppppx" \
			"xoooooooox" \
			"xoooooooox" \
			"xoooooooox" \
			"xoooooooox" \
			"xPPPPPPPPx" \
			"xRNBQKBNRx" \
			"xxxxxxxxxx" \
			"xxxxxxxxxx"
		self.booo = list(self.booo)
		self.current_state = [self.booo, 0, -1]
		# self.start_board = self.booo, 0, -1  # board, whites turn, en_passant = -1
		self.history = []
		self.en_passant_square = -1
		if state is not None:
			self.current_state = state

	#######################
	# RUN & UNDO
	def run_chess(self):
		self.turn = self.current_state[1]
		self.en_passant_square = self.current_state[2]
		# print("turn: ", self.turn, "en_passant: ", self.en_passant_square)
		# add to history
		# save_to_hist = list(current_board)
		save_to_hist = list(self.current_state[0])
		self.history.append([save_to_hist, self.current_state[1], self.current_state[2]])  # maintain a copy of the board, turn and passant sq

		moves = self.get_all_moves(self.current_state[0], self.turn)
		print("moves, ", moves)
		self.make_best_move_depth1(moves)
		# change turns
		self.change_turns()
		self.current_state[1] = self.turn
		self.current_state[2] = self.en_passant_square
		return self.current_state

	def undo(self):
		if len(self.history) == 0:
			reset = "xxxxxxxxxx" \
						"xxxxxxxxxx" \
						"xrnbqkbnrx" \
						"xppppppppx" \
						"xoooooooox" \
						"xoooooooox" \
						"xoooooooox" \
						"xoooooooox" \
						"xPPPPPPPPx" \
						"xRNBQKBNRx" \
						"xxxxxxxxxx" \
						"xxxxxxxxxx"
			reset = list(reset)
			reset_state = reset, 0, -1
			print("DEFAULT POS")
			return reset_state
		else:
			self.current_state = self.history.pop()
			return self.current_state

	def run_move(self, from_sq, to_sq):
		save_to_hist = list(self.current_state[0])
		self.history.append([save_to_hist, self.current_state[1],
							 self.current_state[2]])  # maintain a copy of the board, turn and passant sq
		self.current_state[0], self.en_passant_square = self.move(self.current_state[0], from_sq, to_sq)
		self.current_state[1] = self.turn
		self.current_state[2] = self.en_passant_square
		return self.current_state

	########################
	# pseudo legal moves
	def make_best_move_depth1(self, moves):
		values = []
		indexes = []
		for i in range(len(moves)):
			move_set = moves[i]
			from_sq = move_set[0]
			to_sqs = move_set[1]
			for j in range(len(to_sqs)):
				self.current_state = self.run_move(from_sq, to_sqs[j])
				value = self.evaluate(self.current_state[0])
				print("From: ", self.sq64_to_RF(self.sq120_sq64(from_sq)), "To: ", self.sq64_to_RF(self.sq120_sq64(to_sqs[j])), "Value: ", value)
				values.append(value)
				indexes.append((i, j))
				self.undo()
		k = 0

		best_value = max(values)
		print("best value", best_value)
		best_indexes = []
		for v in values:
			if v == best_value:
				print(values[k])
				best_indexes.append(k)
			k += 1
		print("best indexes! :", best_indexes)
		best_index = random.randint(0, len(best_indexes)-1)
		print(best_indexes[best_index])
		n_index = best_indexes[best_index]
		# best_index = values.index(max(values))
		i, j = indexes[n_index]
		self.run_move(moves[i][0], moves[i][1][j])
		print(self.sq64_to_RF((self.sq120_sq64(moves[i][0]))), self.sq64_to_RF(self.sq120_sq64(moves[i][1][j])))

	def make_random_move(self, b, moves):
		# make random move
		random_piece_n = random.randint(0, len(moves) - 1)
		from_sq = moves[random_piece_n][0]
		to_sq = moves[random_piece_n][1][random.randint(0, len(moves[random_piece_n][1]) - 1)]
		print("from: ", self.sq64_to_RF(self.sq120_sq64(from_sq)), "to: ", self.sq64_to_RF(self.sq120_sq64(to_sq)))

		b, en_passant = self.move(b, from_sq, to_sq)
		# self.print_board(b)
		return b, en_passant

	def move(self, board, from_tile_n, to_tile_n):
		en_pass_sq = -1
		if board[from_tile_n] == 'P':
			if abs(to_tile_n-from_tile_n) == 20:
				en_pass_sq = from_tile_n - 10
		elif board[from_tile_n] == 'p':
			if abs(to_tile_n-from_tile_n) == 20:
				en_pass_sq = from_tile_n + 10

		board[to_tile_n] = board[from_tile_n]
		board[from_tile_n] = "o"
		return board, en_pass_sq

	def evaluate(self, board):
		whites_moves = self.get_all_moves(board, 0)
		white_move_count = 0
		blacks_moves = self.get_all_moves(board, 1)
		black_move_count = 0
		for i in range(len(whites_moves)):
			for j in range(len(whites_moves[i][1])):
				white_move_count += 1
		for i in range(len(blacks_moves)):
			for j in range(len(blacks_moves[i][1])):
				black_move_count += 1

		# print("mobility diff: ", white_move_count-black_move_count)
		count = {'K': 0, 'Q': 0, 'R': 0, 'B': 0, 'N': 0, 'P': 0, 'k': 0, 'q': 0, 'r': 0, 'b': 0, 'n': 0, 'p': 0}
		for i in board:
			if i == 'x':
				pass
			elif i == 'o':
				pass
			else:
				count[i] += 1
		value = (0 * (count['K'] - count['k'])) + (9 * (count['Q'] - count['q'])) + \
				(5 * (count['R'] - count['r'])) + (3 * (count['B'] - count['b'])) + \
				(3 * (count['N'] - count['n'])) + (1 * (count['P'] - count['p']))  + \
				.2 * (white_move_count - black_move_count)

		# value = 5*(count['R']-count['r']) + (count['P']-count['p'])
		if self.turn == 1:
			value *= -1
		# print("board value : ", value)
		return value

	#########################
	# Get Moves
	def get_all_moves(self, b, turn):
		moves = []
		for i in enumerate(b):
			if turn == 0:
				if i[1] == "P" or i[1] == "K" or i[1] == "R" or i[1] == "B" or i[1] == "N" or i[1] == "Q":
					piece_moves = self.get_piece_moves(b, i[0])
					if len(piece_moves) > 0:
						moves.append([i[0], piece_moves])
			elif turn == 1:
				if i[1] == "p" or i[1] == "k" or i[1] == "r" or i[1] == "b" or i[1] == "n" or i[1] == "q":
					piece_moves = self.get_piece_moves(b, i[0])
					if len(piece_moves) > 0:
						moves.append([i[0], piece_moves])
		return moves

	def get_piece_moves(self, board, tile_n):
		result = []
		# print(tile_n, board[tile_n])
		if board[tile_n] == "P":
			result = self.get_white_pawn_moves(board, tile_n)
		if board[tile_n] == "p":
			result = self.get_black_pawn_moves(board, tile_n)
		if board[tile_n] == "K":
			result = self.get_white_king_moves(board, tile_n)
		if board[tile_n] == "k":
			result = self.get_black_king_moves(board, tile_n)
		if board[tile_n] == "R":
			result = self.get_white_rook_moves(board, tile_n)
		if board[tile_n] == "r":
			result = self.get_black_rook_moves(board, tile_n)
		if board[tile_n] == "B":
			result = self.get_white_bishop_moves(board, tile_n)
		if board[tile_n] == "b":
			result = self.get_black_bishop_moves(board, tile_n)
		if board[tile_n] == "N":
			result = self.get_white_knight_moves(board, tile_n)
		if board[tile_n] == "n":
			result = self.get_black_knight_moves(board, tile_n)
		if board[tile_n] == "Q":
			result = self.get_white_queen_moves(board, tile_n)
		if board[tile_n] == "q":
			result = self.get_black_queen_moves(board, tile_n)
		return result

	def get_black_pawn_moves(self, board, tile_n):
		result = []
		if self.en_passant_square != -1:
			if tile_n == self.en_passant_square - 9 or tile_n == self.en_passant_square - 11:
				result.append(self.en_passant_square)
		# forward
		# initial move
		if tile_n < 40: # first row
			if board[tile_n + 10] == "o":
				result.append(tile_n + 10)
				if board[tile_n + 20] == "o":
					result.append(tile_n + 20)
		else:
			if board[tile_n + 10] == "o":
				result.append(tile_n + 10)
		###########
		# attack
		#############
		if board[tile_n + 11] in self.white_pieces:  # attack left only black pawn only
			result.append(tile_n + 11)
		if board[tile_n + 9] in self.white_pieces:  # attack right only black pawn only
			result.append(tile_n + 9)
		return result

	def get_white_pawn_moves(self, board, tile_n):
		result = []
		# forward
		# initial move
		if self.en_passant_square != -1:
			if tile_n == self.en_passant_square + 9 or tile_n == self.en_passant_square + 11:
				result.append(self.en_passant_square)
		if tile_n > 80: # first row
			if board[tile_n - 10] == "o":
				result.append(tile_n - 10)
				if board[tile_n - 20] == "o":
					result.append(tile_n - 20)
		else:
			if board[tile_n-10] == "o":
				result.append(tile_n-10)
		###########
		# attack
		#############
		if board[tile_n - 11] in self.black_pieces:  # attack left only black pawn only
			result.append(tile_n - 11)
		if board[tile_n - 9] in self.black_pieces:  # attack right only black pawn only
			result.append(tile_n - 9)
		return result

	def get_white_king_moves(self, board, tile_n):
		result = []
		down = tile_n + 10
		up = tile_n - 10
		right = tile_n - 1
		left = tile_n + 1
		up_left = tile_n - 11
		up_right = tile_n - 9
		down_left = tile_n + 9
		down_right = tile_n + 11

		# passive moves
		if board[down] == 'o':
			result.append(down)
		if board[up] == 'o':
			result.append(up)
		if board[left] == 'o':
			result.append(left)
		if board[right] == 'o':
			result.append(right)
		if board[up_right] == 'o':
			result.append(up_right)
		if board[down_right] == 'o':
			result.append(down_right)
		if board[up_left] == 'o':
			result.append(up_left)
		if board[down_left] == 'o':
			result.append(down_left)

		# attack moves
		if board[down] in self.black_pieces:
			result.append(down)
		if board[up] in self.black_pieces:
			result.append(up)
		if board[left] in self.black_pieces:
			result.append(left)
		if board[right] in self.black_pieces:
			result.append(right)
		if board[up_right] in self.black_pieces:
			result.append(up_right)
		if board[down_right] in self.black_pieces:
			result.append(down_right)
		if board[up_left] in self.black_pieces:
			result.append(up_left)
		if board[down_left] in self.black_pieces:
			result.append(down_left)

		return result

	def get_black_king_moves(self, board, tile_n):
		result = []
		up = tile_n + 10
		down = tile_n - 10
		left = tile_n - 1
		right = tile_n + 1
		down_right = tile_n - 11
		down_left = tile_n - 9
		up_right = tile_n + 9
		up_left = tile_n + 11

		# passive moves
		if board[down] == 'o':
			result.append(down)
		if board[up] == 'o':
			result.append(up)
		if board[left] == 'o':
			result.append(left)
		if board[right] == 'o':
			result.append(right)
		if board[up_right] == 'o':
			result.append(up_right)
		if board[down_right] == 'o':
			result.append(down_right)
		if board[up_left] == 'o':
			result.append(up_left)
		if board[down_left] == 'o':
			result.append(down_left)

		# attack moves
		if board[down] in self.white_pieces:
			result.append(down)
		if board[up] in self.white_pieces:
			result.append(up)
		if board[left] in self.white_pieces:
			result.append(left)
		if board[right] in self.white_pieces:
			result.append(right)
		if board[up_right] in self.white_pieces:
			result.append(up_right)
		if board[down_right] in self.white_pieces:
			result.append(down_right)
		if board[up_left] in self.white_pieces:
			result.append(up_left)
		if board[down_left] in self.white_pieces:
			result.append(down_left)

		return result

	def get_white_rook_moves(self, board, tile_n):
		result = []
		# UP
		i = tile_n
		while board[i] != 'x':
			i -= 10
			# open square
			if board[i] == 'o':
				result.append(i)
			# attack
			if board[i] in self.black_pieces:
				print("ATTACK WITH ROOK")
				result.append(i)
				break
			# self block
			if board[i] in self.white_pieces or board[i] == "K" or board[i] == "k":
				break
		# DOWN
		i = tile_n
		while board[i] != 'x':
			i += 10
			# open square
			if board[i] == 'o':
				result.append(i)
			# attack
			if board[i] in self.black_pieces:
				print("ATTACK WITH ROOK")
				result.append(i)
				break
			# self block
			if board[i] in self.white_pieces or board[i] == "K" or board[i] == "k":
				break

		# LEFT
		i = tile_n
		while board[i] != 'x':
			i -= 1
			# open square
			if board[i] == 'o':
				result.append(i)
			# attack
			if board[i] in self.black_pieces:
				print("ATTACK WITH ROOK")
				result.append(i)
				break
			# self block
			if board[i] in self.white_pieces or board[i] == "K" or board[i] == "k":
				break

		# RIGHT
		i = tile_n
		while board[i] != 'x':
			i += 1
			# open square
			if board[i] == 'o':
				result.append(i)
			# attack
			if board[i] in self.black_pieces:
				print("ATTACK WITH ROOK")
				result.append(i)
				break
			# self block
			if board[i] in self.white_pieces or board[i] == "K" or board[i] == "k":
				break
		return result

	def get_black_rook_moves(self, board, tile_n):
		result = []
		# UP
		i = tile_n
		while board[i] != 'x':
			i += 10
			# open square
			if board[i] == 'o':
				result.append(i)
			# attack
			if board[i] in self.white_pieces:
				print("ATTACK WITH ROOK")
				result.append(i)
				break
			# self block
			if board[i] in self.black_pieces or board[i] == "k" or board[i] == "K":
				break
		# DOWN
		i = tile_n
		while board[i] != 'x':
			i -= 10
			# open square
			if board[i] == 'o':
				result.append(i)
			# attack
			if board[i] in self.white_pieces:
				print("ATTACK WITH ROOK")
				result.append(i)
				break
			# self block
			if board[i] in self.black_pieces or board[i] == "k" or board[i] == "K":
				break

		# LEFT
		i = tile_n
		while board[i] != 'x':
			i += 1
			# open square
			if board[i] == 'o':
				result.append(i)
			# attack
			if board[i] in self.white_pieces:
				print("ATTACK WITH ROOK")
				result.append(i)
				break
			# self block
			if board[i] in self.black_pieces or board[i] == "k" or board[i] == "K":
				break

		# RIGHT
		i = tile_n
		while board[i] != 'x':
			i -= 1
			# open square
			if board[i] == 'o':
				result.append(i)
			# attack
			if board[i] in self.white_pieces:
				print("ATTACK WITH ROOK")
				result.append(i)
				break
			# self block
			if board[i] in self.black_pieces or board[i] == "k" or board[i] == "K":
				break
		return result

	def get_white_bishop_moves(self, board, tile_n):
		result = []
		# UP LEFT
		i = tile_n
		while board[i] != 'x':
			i -= 11
			# open square
			if board[i] == 'o':
				result.append(i)
			# attack
			if board[i] in self.black_pieces:
				print("ATTACK WITH ROOK")
				result.append(i)
				break
			# self block
			if board[i] in self.white_pieces or board[i] == "K" or board[i] == "k":
				break

		# UP RIGHT
		i = tile_n
		while board[i] != 'x':
			i -= 9
			# open square
			if board[i] == 'o':
				result.append(i)
			# attack
			if board[i] in self.black_pieces:
				print("ATTACK WITH ROOK")
				result.append(i)
				break
			# self block
			if board[i] in self.white_pieces or board[i] == "K" or board[i] == "k":
				break
		# DOWN LEFT
		i = tile_n
		while board[i] != 'x':
			i += 9
			# open square
			if board[i] == 'o':
				result.append(i)
			# attack
			if board[i] in self.black_pieces:
				print("ATTACK WITH ROOK")
				result.append(i)
				break
			# self block
			if board[i] in self.white_pieces or board[i] == "K" or board[i] == "k":
				break

		# DOWN RIGHT
		i = tile_n
		while board[i] != 'x':
			i += 11
			# open square
			if board[i] == 'o':
				result.append(i)
			# attack
			if board[i] in self.black_pieces:
				print("ATTACK WITH ROOK")
				result.append(i)
				break
			# self block
			if board[i] in self.white_pieces or board[i] == "K" or board[i] == "k":
				break
		return result

	def get_black_bishop_moves(self, board, tile_n):
		result = []
		# DOWN LEFT
		i = tile_n
		while board[i] != 'x':
			i += 11
			# open square
			if board[i] == 'o':
				result.append(i)
			# attack
			if board[i] in self.black_pieces:
				print("ATTACK WITH ROOK")
				result.append(i)
				break
			# self block
			if board[i] in self.white_pieces or board[i] == "K" or board[i] == "k":
				break

		# DOWN RIGHT
		i = tile_n
		while board[i] != 'x':
			i += 9
			# open square
			if board[i] == 'o':
				result.append(i)
			# attack
			if board[i] in self.black_pieces:
				print("ATTACK WITH ROOK")
				result.append(i)
				break
			# self block
			if board[i] in self.white_pieces or board[i] == "K" or board[i] == "k":
				break
		# UP LEFT
		i = tile_n
		while board[i] != 'x':
			i -= 9
			# open square
			if board[i] == 'o':
				result.append(i)
			# attack
			if board[i] in self.black_pieces:
				print("ATTACK WITH ROOK")
				result.append(i)
				break
			# self block
			if board[i] in self.white_pieces or board[i] == "K" or board[i] == "k":
				break

		# UP RIGHT
		i = tile_n
		while board[i] != 'x':
			i -= 11
			# open square
			if board[i] == 'o':
				result.append(i)
			# attack
			if board[i] in self.black_pieces:
				print("ATTACK WITH ROOK")
				result.append(i)
				break
			# self block
			if board[i] in self.white_pieces or board[i] == "K" or board[i] == "k":
				break
		return result

	def get_white_knight_moves(self, board, tile_n):
		result = []
		directions = [21, 19, 12, 8, -21, -19, -8]
		for i in range(len(directions)):
			if board[tile_n+directions[i]] == 'o' or board[tile_n+directions[i]] in self.black_pieces:
				result.append(tile_n+directions[i])
		return result

	def get_black_knight_moves(self, board, tile_n):
		result = []
		directions = [21, 19, 12, 8, -21, -19, -8]
		for i in range(len(directions)):
			if board[tile_n+directions[i]] == 'o' or board[tile_n+directions[i]] in self.white_pieces:
				result.append(tile_n+directions[i])
		return result

	def get_white_queen_moves(self, board, tile_n):
		result = []
		# UP
		i = tile_n
		while board[i] != 'x':
			i -= 10
			# open square
			if board[i] == 'o':
				result.append(i)
			# attack
			if board[i] in self.black_pieces:
				print("ATTACK WITH ROOK")
				result.append(i)
				break
			# self block
			if board[i] in self.white_pieces or board[i] == "K" or board[i] == "k":
				break
		# DOWN
		i = tile_n
		while board[i] != 'x':
			i += 10
			# open square
			if board[i] == 'o':
				result.append(i)
			# attack
			if board[i] in self.black_pieces:
				print("ATTACK WITH ROOK")
				result.append(i)
				break
			# self block
			if board[i] in self.white_pieces or board[i] == "K" or board[i] == "k":
				break

		# LEFT
		i = tile_n
		while board[i] != 'x':
			i -= 1
			# open square
			if board[i] == 'o':
				result.append(i)
			# attack
			if board[i] in self.black_pieces:
				print("ATTACK WITH ROOK")
				result.append(i)
				break
			# self block
			if board[i] in self.white_pieces or board[i] == "K" or board[i] == "k":
				break

		# RIGHT
		i = tile_n
		while board[i] != 'x':
			i += 1
			# open square
			if board[i] == 'o':
				result.append(i)
			# attack
			if board[i] in self.black_pieces:
				print("ATTACK WITH ROOK")
				result.append(i)
				break
			# self block
			if board[i] in self.white_pieces or board[i] == "K" or board[i] == "k":
				break

				# UP LEFT
				i = tile_n
				while board[i] != 'x':
					i -= 11
					# open square
					if board[i] == 'o':
						result.append(i)
					# attack
					if board[i] in self.black_pieces:
						print("ATTACK WITH ROOK")
						result.append(i)
						break
					# self block
					if board[i] in self.white_pieces or board[i] == "K" or board[i] == "k":
						break

				# UP RIGHT
				i = tile_n
				while board[i] != 'x':
					i -= 9
					# open square
					if board[i] == 'o':
						result.append(i)
					# attack
					if board[i] in self.black_pieces:
						print("ATTACK WITH ROOK")
						result.append(i)
						break
					# self block
					if board[i] in self.white_pieces or board[i] == "K" or board[i] == "k":
						break
				# DOWN LEFT
				i = tile_n
				while board[i] != 'x':
					i += 9
					# open square
					if board[i] == 'o':
						result.append(i)
					# attack
					if board[i] in self.black_pieces:
						print("ATTACK WITH ROOK")
						result.append(i)
						break
					# self block
					if board[i] in self.white_pieces or board[i] == "K" or board[i] == "k":
						break

				# DOWN RIGHT
				i = tile_n
				while board[i] != 'x':
					i += 11
					# open square
					if board[i] == 'o':
						result.append(i)
					# attack
					if board[i] in self.black_pieces:
						print("ATTACK WITH ROOK")
						result.append(i)
						break
					# self block
					if board[i] in self.white_pieces or board[i] == "K" or board[i] == "k":
						break

		return result

	def get_black_queen_moves(self, board, tile_n):
		result = []
		# UP
		i = tile_n
		while board[i] != 'x':
			i += 10
			# open square
			if board[i] == 'o':
				result.append(i)
			# attack
			if board[i] in self.white_pieces:
				print("ATTACK WITH ROOK")
				result.append(i)
				break
			# self block
			if board[i] in self.black_pieces or board[i] == "k" or board[i] == "K":
				break
		# DOWN
		i = tile_n
		while board[i] != 'x':
			i -= 10
			# open square
			if board[i] == 'o':
				result.append(i)
			# attack
			if board[i] in self.white_pieces:
				print("ATTACK WITH ROOK")
				result.append(i)
				break
			# self block
			if board[i] in self.black_pieces or board[i] == "k" or board[i] == "K":
				break

		# LEFT
		i = tile_n
		while board[i] != 'x':
			i += 1
			# open square
			if board[i] == 'o':
				result.append(i)
			# attack
			if board[i] in self.white_pieces:
				print("ATTACK WITH ROOK")
				result.append(i)
				break
			# self block
			if board[i] in self.black_pieces or board[i] == "k" or board[i] == "K":
				break

		# RIGHT
		i = tile_n
		while board[i] != 'x':
			i -= 1
			# open square
			if board[i] == 'o':
				result.append(i)
			# attack
			if board[i] in self.white_pieces:
				print("ATTACK WITH ROOK")
				result.append(i)
				break
			# self block
			if board[i] in self.black_pieces or board[i] == "k" or board[i] == "K":
				break

				# DOWN LEFT
				i = tile_n
				while board[i] != 'x':
					i += 11
					# open square
					if board[i] == 'o':
						result.append(i)
					# attack
					if board[i] in self.black_pieces:
						print("ATTACK WITH ROOK")
						result.append(i)
						break
					# self block
					if board[i] in self.white_pieces or board[i] == "K" or board[i] == "k":
						break

				# DOWN RIGHT
				i = tile_n
				while board[i] != 'x':
					i += 9
					# open square
					if board[i] == 'o':
						result.append(i)
					# attack
					if board[i] in self.black_pieces:
						print("ATTACK WITH ROOK")
						result.append(i)
						break
					# self block
					if board[i] in self.white_pieces or board[i] == "K" or board[i] == "k":
						break
				# UP LEFT
				i = tile_n
				while board[i] != 'x':
					i -= 9
					# open square
					if board[i] == 'o':
						result.append(i)
					# attack
					if board[i] in self.black_pieces:
						print("ATTACK WITH ROOK")
						result.append(i)
						break
					# self block
					if board[i] in self.white_pieces or board[i] == "K" or board[i] == "k":
						break

				# UP RIGHT
				i = tile_n
				while board[i] != 'x':
					i -= 11
					# open square
					if board[i] == 'o':
						result.append(i)
					# attack
					if board[i] in self.black_pieces:
						print("ATTACK WITH ROOK")
						result.append(i)
						break
					# self block
					if board[i] in self.white_pieces or board[i] == "K" or board[i] == "k":
						break

		return result

	####################
	# HELPER FUNCTIONS
	def RF_sq64(self, file, rank):
		sq = 0
		if file == 'A':
			file = 1
		elif file == 'B':
			file = 2
		elif file == 'C':
			file = 3
		elif file == 'D':
			file = 4
		elif file == 'E':
			file = 5
		elif file == 'F':
			file = 6
		elif file == 'G':
			file = 7
		elif file == 'H':
			file = 8
		else:
			file = -1
			print("error unkown file")
		sq = abs(rank-9)*8-8 + file
		return sq

	def sq64_to_RF(self, sq64):

		rank = 0
		if sq64 <= 8:
			rank = '8'
		elif sq64 <= 16:
			rank = '7'
		elif sq64 <= 24:
			rank = '6'
		elif sq64 <= 32:
			rank = '5'
		elif sq64 <= 40:
			rank = '4'
		elif sq64 <= 48:
			rank = '3'
		elif sq64 <= 56:
			rank = '2'
		elif sq64 <= 64:
			rank = '1'

		file = sq64 % 8
		if file == 1:
			file = 'A'
		elif file == 2:
			file = 'B'
		elif file == 3:
			file = 'C'
		elif file == 4:
			file = 'D'
		elif file == 5:
			file = 'E'
		elif file == 6:
			file = 'F'
		elif file == 7:
			file = 'G'
		elif file == 0:
			file = 'H'
		else:
			print("eror", file)
		return file, rank

	def change_turns(self):
		if self.turn == 1:
			self.turn = 0
		else:
			self.turn = 1
		# return turn

	def print_full_board(self, board):
		for i in range(0, 120):
			if i % 10 == 0:
				row = board[i:i + 10]
				row_str = ' '.join(row)
				print(i, row_str)

	def print_board(self, board):
		k = 0
		for i in range(20, 100):
			if i % 10 == 0:
				# print(board)
				# print(i)
				row = board[i + 1:i + 9]
				row_str = ' '.join(row)
				print(self.ranks[k], row_str)
				k += 1
		print('  A B C D E F G H')

	def sq120_sq64(self, sq):
		sq120 = []
		for i in range(120):
			# if i < 21:
			# 	sq120.append(-1)
			# if i > 100:
			# 	sq120.append(-1)
			# else:
			sq120.append(-1)
		skip = 0
		for i in range(20, 100):
			if i % 10 != 0 and (i -9) % 10 != 0:
				sq120[i] = i - 20 - skip
			if i % 10 == 0 and i != 20:
				skip += 2
		return sq120[sq]

	def sq64_to_sq120(self, sq):
		extra = 0
		for i in range(1, sq):
			if i % 8 == 0:
				extra += 2
		return sq + 20 + extra



# Initialize chess engine
myisabel = IzzI()
# Graphics consants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 20, 0)
GREEN = (0, 220, 10)
BLUE = (50, 50, 150)
FPS = 10
SCREEN_WIDTH = 450
SCREEN_HEIGHT = 450
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
SCALE = 40
coordinates = []


class GUI(object):
	def __init__(self):
		pygame.init()
		self.board =  myisabel.booo
		self.board = list(self.board)
		self.size = [SCREEN_WIDTH, SCREEN_HEIGHT]
		self.screen = pygame.display.set_mode(self.size)
		pygame.display.set_caption("Chess")
		pygame.mouse.set_visible(False)

		# Create our objects and set the data
		self.done = False
		self.clock = pygame.time.Clock()
		self.BackGround = Background('chess_board.jpg', [0, 0])
		self.score = 0
		self.game_over = False

		self.initialize_images()
		self.Move = 0
		self.i = 0

		pygame.display.set_caption("Chess")
		pygame.mouse.set_visible(False)
		for i in range(8):
			for j in range(8):
				coordinates.append([i + 1, j + 1])
		print(coordinates)
		self.turn = 0
		self.en_passant = -1

	def initialize_images(self):
		self.white_king = pygame.image.load("images/white_king.gif").convert_alpha()
		self.white_king_rect = self.white_king.get_rect()

		self.white_bishop = pygame.image.load("images/white_bishop.gif").convert_alpha()
		self.white_bishop_rect = self.white_bishop.get_rect()

		self.white_queen = pygame.image.load("images/white_queen.gif").convert_alpha()
		self.white_queen_rect = self.white_queen.get_rect()

		self.white_rook = pygame.image.load("images/white_rook.gif").convert_alpha()
		self.white_rook_rect = self.white_rook.get_rect()

		self.white_pawn = pygame.image.load("images/white_pawn.gif").convert_alpha()
		self.white_pawn_rect = self.white_king.get_rect()

		self.white_knight = pygame.image.load("images/white_knight.gif").convert_alpha()
		self.white_king_rect = self.white_knight.get_rect()

		"""black"""
		self.black_king = pygame.image.load("images/black_king.gif").convert_alpha()
		self.black_king_rect = self.black_king.get_rect()

		self.black_queen = pygame.image.load("images/black_queen.gif").convert_alpha()
		self.black_queen_rect = self.white_queen.get_rect()

		self.black_bishop = pygame.image.load("images/black_bishop.gif").convert_alpha()
		self.black_bishop_rect = self.white_bishop.get_rect()

		self.black_rook = pygame.image.load("images/black_rook.gif").convert_alpha()
		self.black_rook_rect = self.white_rook.get_rect()

		self.black_pawn = pygame.image.load("images/black_pawn.gif").convert_alpha()
		self.black_pawn_rect = self.black_king.get_rect()

		self.black_knight = pygame.image.load("images/black_knight.gif").convert_alpha()
		self.black_king_rect = self.black_knight.get_rect()

	def process_events(self):
		""" Process all of the events. Return a "True" if we need to close the window. """
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return True
			# if event.type == pygame.MOUSEBUTTONDOWN:
			# if self.game_over:
			# self.__init__()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					self.board, self.turn, self.en_passant = myisabel.run_chess()
					return False
				if event.key == pygame.K_SPACE:
					self.board = []
					self.board, self.turn, self.en_passant = myisabel.undo()
					# print("GUI HERE I GOT YOUR BOARD here your board::: ")
					# myisabel.print_board(self.board)
					return False
				# print("turn: ", self.turn, "en_passant: ", self.en_passant)

		return False

	def step(self):
		if not self.game_over:
			# self.done = self.process_events()
			self.process_events()
			self.display_frame(self.screen)
			self.clock.tick(60)
		if self.done is True:
			pygame.quit()

	def run_steps(self):
		i = 0
		while True:
			self.step()

	def sq120_sq64(self, sq):
		sq120 = []
		for i in range(120):
			# if i < 21:
			# 	sq120.append(-1)
			# if i > 100:
			# 	sq120.append(-1)
			# else:
			sq120.append(-1)
		skip = 0
		for i in range(20, 100):
			if i % 10 != 0 and (i - 9) % 10 != 0:
				sq120[i] = i - 20 - skip
			if i % 10 == 0 and i != 20:
				skip += 2
		return sq120[sq]

	def display_frame(self, screen):
		""" Display everything to the screen for the game. """
		screen.fill([255, 255, 255])
		screen.blit(self.BackGround.image, self.BackGround.rect)
		for i in range(20, 120):
			xbuffer = -35
			ybuffer = -35
			sq64 = self.sq120_sq64(i)
			if self.board[i] == 'P':
				screen.blit(self.white_pawn,
							[coordinates[sq64 - 1][1] * 52 + xbuffer, coordinates[sq64 - 1][0] * 52 + ybuffer])
			if self.board[i] == 'p':
				screen.blit(self.black_pawn,
							[coordinates[sq64 - 1][1] * 52 + xbuffer, coordinates[sq64 - 1][0] * 52 + ybuffer])
			if self.board[i] == 'K':
				screen.blit(self.white_king,
							[coordinates[sq64 - 1][1] * 52 + xbuffer, coordinates[sq64 - 1][0] * 52 + ybuffer])
			if self.board[i] == 'k':
				screen.blit(self.black_king,
							[coordinates[sq64 - 1][1] * 52 + xbuffer, coordinates[sq64 - 1][0] * 52 + ybuffer])
			if self.board[i] == 'Q':
				screen.blit(self.white_queen,
							[coordinates[sq64 - 1][1] * 52 + xbuffer, coordinates[sq64 - 1][0] * 52 + ybuffer])
			if self.board[i] == 'q':
				screen.blit(self.black_queen,
							[coordinates[sq64 - 1][1] * 52 + xbuffer, coordinates[sq64 - 1][0] * 52 + ybuffer])
			if self.board[i] == 'R':
				screen.blit(self.white_rook,
							[coordinates[sq64 - 1][1] * 52 + xbuffer, coordinates[sq64 - 1][0] * 52 + ybuffer])
			if self.board[i] == 'r':
				screen.blit(self.black_rook,
							[coordinates[sq64 - 1][1] * 52 + xbuffer, coordinates[sq64 - 1][0] * 52 + ybuffer])
			if self.board[i] == 'B':
				screen.blit(self.white_bishop,
							[coordinates[sq64 - 1][1] * 52 + xbuffer, coordinates[sq64 - 1][0] * 52 + ybuffer])
			if self.board[i] == 'b':
				screen.blit(self.black_bishop,
							[coordinates[sq64 - 1][1] * 52 + xbuffer, coordinates[sq64 - 1][0] * 52 + ybuffer])
			if self.board[i] == 'N':
				screen.blit(self.white_knight,
							[coordinates[sq64 - 1][1] * 52 + xbuffer, coordinates[sq64 - 1][0] * 52 + ybuffer])
			if self.board[i] == 'n':
				screen.blit(self.black_knight,
							[coordinates[sq64 - 1][1] * 52 + xbuffer, coordinates[sq64 - 1][0] * 52 + ybuffer])

		pygame.display.flip()


class Background(pygame.sprite.Sprite):
	def __init__(self, image_file, location):
		pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
		self.image = pygame.image.load(image_file)
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = location

# b = "xxxxxxxxxx" \
# 	"xxxxxxxxxx" \
# 	"xrnbqkbnrx" \
# 	"xppppppppx" \
# 	"xoooooooox" \
# 	"xoooooooox" \
# 	"xoooooooox" \
# 	"xoooooooox" \
# 	"xPPPPPPPPx" \
# 	"xRNBQKBNRx" \
# 	"xxxxxxxxxx" \
# 	"xxxxxxxxxx"
# # 0 - 9
# # 10 - 19
# # 20 - 29  20, 1, 2, 3, 4, 5, 6, 7, 8, 29
# # 30 - 39 .. 30, 9, 10, 11, 12, 13, 14, 15, 16, 39
# # 120 - 129
#
# b = list(b)

gui = GUI()
gui.run_steps()

# test_transforms()
# test_RF_sq64()
# test_sq64()
# test_sq120()
# print_full_board(b)
# test_sq64_RF()

# test_white_pawn()
# run_chess()



