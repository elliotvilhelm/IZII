import random

init_board = "xxxxxxxxxx" \
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
init_board = list(init_board)

# current state = board, en_passant, num_moves


class IzzI:

	def __init__(self, state=None):

		self.white_pieces = "PNBRQ" # excludes king
		self.black_pieces = "pnbrq"
		self.all_white = "PKQRNBP"
		self.all_black = "pkqrnbp"
		self.black_sliders = "qrb"
		self.white_sliders = "QRB"
		self.ranks = [8, 7, 6, 5, 4, 3, 2, 1]
		self.current_state = []
		self.history = []
		# carries board, turn, enpassant, half_move, full_move, castle permission, whitekingsq, blackkingsq
		self.current_state = [init_board, 0, -1, 0, 1, [1,1,1,1], init_board.index('K'), init_board.index('k')]

		self.history.append(self.current_state)
		if state is not None:
			self.current_state = state

	#######################
	# RUN & UNDO
	def run_chess(self):
		# Save a COPY of the board to history
		self.save_state_to_hist()
		# Get All Pseudo Legal Moves
		moves = self.get_pseudo_moves(self.current_state[0], self.current_state[1])
		# if self.current_state[1] == 0:
		moves = self.get_legal_moves(moves)
		from_sq, to_sq = self.get_best_move_depth1(moves)
		if from_sq == -1:
			return self.current_state
		self.move(from_sq, to_sq)

		# change turns
		self.change_turns()
		return self.current_state

	def undo(self):
		if len(self.history) == 1:
			return self.history[0]
		else:
			self.current_state = self.history.pop()
			return self.current_state

	def run_move(self, from_sq, to_sq):
		self.save_state_to_hist()
		self.move(from_sq, to_sq)
		return self.current_state

	def save_state_to_hist(self):
		board_save = list(self.current_state[0])
		castle_perm = list(self.current_state[5])
		self.history.append([board_save, self.current_state[1], self.current_state[2], self.current_state[3],
							self.current_state[4], castle_perm, self.current_state[6], self.current_state[7]])

	########################
	# ALGORITHM
	def get_best_move_depth1(self, moves):
		values = []
		indexes = []
		for i in range(len(moves)):
			move_set = moves[i]
			from_sq = move_set[0]
			to_sqs = move_set[1]
			for j in range(len(to_sqs)):
				self.current_state = self.run_move(from_sq, to_sqs[j])
				value = self.evaluate(self.current_state[0])
				# print("From: ", self.sq64_to_RF(self.sq120_sq64(from_sq)), "To: ", self.sq64_to_RF(self.sq120_sq64(to_sqs[j])), "Value: ", value)
				values.append(value)
				indexes.append((i, j))
				self.undo()
		k = 0
		if len(moves) == 0:
			print("CHECK MATE")
			return -1, -1
		# print("values: ", values)
		best_value = max(values)
		# print("best value", best_value)
		best_indexes = []
		for v in values:
			if v == best_value:
				# print(values[k])
				best_indexes.append(k)
			k += 1
		# print("best indexes! :", best_indexes)
		best_index = random.randint(0, len(best_indexes)-1)
		# print(best_indexes[best_index])
		n_index = best_indexes[best_index]
		i, j = indexes[n_index]
		return moves[i][0], moves[i][1][j]

	# def make_random_move(self, b, moves):
	# 	# make random move
	# 	random_piece_n = random.randint(0, len(moves) - 1)
	# 	from_sq = moves[random_piece_n][0]
	# 	to_sq = moves[random_piece_n][1][random.randint(0, len(moves[random_piece_n][1]) - 1)]
	# 	print("from: ", self.sq64_to_RF(self.sq120_sq64(from_sq)), "to: ", self.sq64_to_RF(self.sq120_sq64(to_sq)))
	#
	# 	b, en_passant = self.move(b, from_sq, to_sq)
	# 	# self.print_board(b)
	# 	return b, en_passant

	########################
	# BOARD
	def move(self, from_tile_n, to_tile_n):
		en_pass_sq = -1
		board = self.current_state[0]
		### En Passant case
		if board[from_tile_n] == 'P':
			if abs(to_tile_n-from_tile_n) == 20:
				en_pass_sq = from_tile_n - 10
			if board[to_tile_n - 10] == 'x':
				board[from_tile_n] = 'Q'

		elif board[from_tile_n] == 'p':
			if abs(to_tile_n-from_tile_n) == 20:
				en_pass_sq = from_tile_n + 10
			if board[to_tile_n + 10] == 'x':
				board[from_tile_n] = 'q'
		### King move case
		elif board[from_tile_n] == 'K':
			self.current_state[6] = to_tile_n
			# save white to tile
		elif board[from_tile_n] == 'k':
			self.current_state[7] = to_tile_n
			# save black to tile
		board[to_tile_n] = board[from_tile_n]
		board[from_tile_n] = "o"
		self.current_state[2] = en_pass_sq

	def evaluate(self, board):
		whites_moves = self.get_pseudo_moves(board, 0)
		white_move_count = 0
		blacks_moves = self.get_pseudo_moves(board, 1)
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
				0 * (white_move_count - black_move_count)

		if self.current_state[1] == 1:
			value *= -1
		return value

	#########################
	# MOVE GENERATION
	def get_pseudo_moves(self, b, turn):
		moves = []
		for i in enumerate(b):
			if turn == 0:
				if i[1] in self.all_white:
					piece_moves = self.get_piece_moves(b, i[0])
					if len(piece_moves) > 0:
						moves.append([i[0], piece_moves])
			elif turn == 1:
				if i[1] in self.all_black:
					piece_moves = self.get_piece_moves(b, i[0])
					if len(piece_moves) > 0:
						moves.append([i[0], piece_moves])
		return moves

	def get_legal_moves(self, pseudo_moves):
		# take move
		# check if in check
		# valid/invalid move
		# undo move
		legal_moves = []
		legal_set = []
		in_check = False
		for i in range(len(pseudo_moves)):
			move_set = pseudo_moves[i]
			from_sq = move_set[0]
			to_sqs = move_set[1]
			for j in range(len(to_sqs)):
				self.run_move(from_sq, to_sqs[j])
				if self.current_state[1] == 0:
					in_check = self.white_in_check(self.current_state[0], self.current_state[6])
				elif self.current_state[1] == 1:
					in_check = self.black_in_check(self.current_state[0], self.current_state[7])
				if in_check is False:
					legal_set.append(to_sqs[j])
				# else:
					# print("check")
				self.undo()
			if len(legal_set) > 0:
				legal_moves.append([from_sq, legal_set])
			legal_set = []
		return legal_moves



	######################
	## CHECK SYSTEM
	# returns true if white is in check
	# checks for sliders
	# checks for knights
	# checks for pawns
	def white_in_check(self, board, tile_n):
		if self.check_black_sliders(board, tile_n) is True:
			return True
		if self.check_black_knights(board, tile_n) is True:
			return True
		if self.check_black_king(board, tile_n) is True:
			return True
		if self.check_black_pawns(board, tile_n) is True:
			return True
		else:
			return False

	def black_in_check(self, board, tile_n):
		if self.check_white_sliders(board, tile_n) is True:
			# print("fucking sliders")
			return True
		if self.check_white_knights(board, tile_n) is True:
			return True
		if self.check_white_king(board, tile_n) is True:
			return True
		if self.check_white_pawns(board, tile_n) is True:
			return True
		else:

			return False

	def check_black_pawns(self, board, tile_n):
		if board[tile_n-11] == 'p':
			# print("warning black pawn")
			return True
		if board[tile_n-9] == 'p':
			# print("warning black pawn")
			return True
		return False

	def check_white_pawns(self, board, tile_n):
		if board[tile_n+11] == 'P':
			# print("warning white pawn")
			return True
		if board[tile_n+9] == 'P':
			# print("warning white pawn")

			return True
		return False
	def check_black_king(self, board, tile_n):
		directions = [11, 10, 9, 1, -11, -10, -9, -1]
		for direction in directions:
			if board[tile_n + direction] == 'k':
				return True
		return False

	def check_white_king(self, board, tile_n):
		directions = [11, 10, 9, 1, -11, -10, -9, -1]
		for direction in directions:
			if board[tile_n + direction] == 'K':
				return True
		return False

	def check_black_knights(self, board, tile_n):
		directions = [21, 19, 12, 8, -21, -19, -8]
		for direction in directions:
			if board[tile_n+direction] == 'n':
				return True
		return False

	def check_white_knights(self, board, tile_n):
		directions = [21, 19, 12, 8, -21, -19, -8]
		for direction in directions:
			if board[tile_n+direction] == 'N':
				return True
		return False

	# returns false if no black sliders are found attacking tile_n square
	def check_black_sliders(self, board, tile_n):
		slider_found = False
		# UP
		i = tile_n
		while board[i] != 'x':
			i -= 10
			if board[i] in "qr":
				slider_found = True
				return slider_found # no need to check any more
			if board[i] in "pkbn":
				break
			if board[i] in self.all_white:
				break
		# DOWN
		i = tile_n
		while board[i] != 'x':
			i += 10
			if board[i] in "qr":
				slider_found = True
				return slider_found  # no need to check any more
			if board[i] in "pkbn":
				break
			if board[i] in self.all_white:
				break

		# LEFT
		i = tile_n
		while board[i] != 'x':
			i -= 1
			if board[i] in "qr":
				slider_found = True
				return slider_found  # no need to check any more
			if board[i] in "pkbn":
				break
			if board[i] in self.all_white:
				break


		# RIGHT
		i = tile_n
		while board[i] != 'x':
			i += 1
			if board[i] in "qr":
				slider_found = True
				return slider_found  # no need to check any more
			if board[i] in "pkbn":
				break
			if board[i] in self.all_white:
				break

		# UP LEFT
		i = tile_n
		while board[i] != 'x':
			i -= 11
			if board[i] in "qb":
				slider_found = True
				return slider_found  # no need to check any more
			if board[i] in "pkrn":
				break
			if board[i] in self.all_white:
				break

		# UP RIGHT
		i = tile_n
		while board[i] != 'x':
			i -= 9
			if board[i] in "qb":
				slider_found = True
				return slider_found  # no need to check any more
			if board[i] in "pkrn":
				break
			if board[i] in self.all_white:
				break
		# DOWN LEFT
		i = tile_n
		while board[i] != 'x':
			i += 9
			if board[i] in "qb":
				slider_found = True
				return slider_found # no need to check any more
			if board[i] in "pkrn":
				break
			if board[i] in self.all_white:
				break
		# DOWN RIGHT
		i = tile_n
		while board[i] != 'x':
			i += 11
			if board[i] in "qb":
				slider_found = True
				return slider_found # no need to check any more
			if board[i] in "pkrn":
				break
			if board[i] in self.all_white:
				break

		return slider_found

	def check_white_sliders(self, board, tile_n):
		slider_found = False
		# UP
		i = tile_n
		while board[i] != 'x':
			i -= 10
			if board[i] in "QR":
				slider_found = True
				return slider_found # no need to check any more
			if board[i] in "PKBN":
				break
			if board[i] in self.all_black:
				break
		# DOWN
		i = tile_n
		while board[i] != 'x':
			i += 10
			if board[i] in "QR":
				# print("queen rook ")
				slider_found = True
				return slider_found  # no need to check any more
			if board[i] in "PKBN":
				break
			if board[i] in self.all_black:
				# print("blocked by black")
				break
		# LEFT
		i = tile_n
		while board[i] != 'x':
			i -= 1
			if board[i] in "QR":
				# print("slider at", self.sq64_to_RF(self.sq120_sq64(i)))
				slider_found = True
				return slider_found  # no need to check any more
			if board[i] in "PKBN":
				break
			if board[i] in self.all_black:
				break

		# RIGHT
		i = tile_n
		while board[i] != 'x':
			i += 1
			if board[i] in "QR":
				slider_found = True
				return slider_found  # no need to check any more
			if board[i] in "PKBN":
				break
			if board[i] in self.all_black:
				break

		# UP LEFT
		i = tile_n
		while board[i] != 'x':
			i -= 11
			if board[i] in "QB":
				slider_found = True
				return slider_found  # no need to check any more
			if board[i] in "pkbn":
				break
			if board[i] in self.all_black:
				break

		# UP RIGHT
		i = tile_n
		while board[i] != 'x':
			i -= 9
			if board[i] in "QB":
				slider_found = True
				return slider_found  # no need to check any more
			if board[i] in "pkbn":
				break
			if board[i] in self.all_black:
				break
		# DOWN LEFT
		i = tile_n
		while board[i] != 'x':
			i += 9
			if board[i] in "QB":
				slider_found = True
				return slider_found # no need to check any more
			if board[i] in "pkbn":
				break
			if board[i] in self.all_black:
				break
		# DOWN RIGHT
		i = tile_n
		while board[i] != 'x':
			i += 11
			if board[i] in "QB":
				slider_found = True
				return slider_found # no need to check any more
			if board[i] in "pkbn":
				break
			if board[i] in self.all_black:
				break
		return slider_found

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
		en_passant_square = self.current_state[2]
		if en_passant_square != -1:
			if tile_n == en_passant_square - 9 or tile_n == en_passant_square - 11:
				result.append(en_passant_square)
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
		en_passant_square = self.current_state[2]
		# forward
		# initial move
		if en_passant_square != -1:
			if tile_n == en_passant_square + 9 or tile_n == en_passant_square + 11:
				result.append(en_passant_square)
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
				# print("ATTACK WITH ROOK")
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
				# print("ATTACK WITH ROOK")
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
				# print("ATTACK WITH ROOK")
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
				# print("ATTACK WITH ROOK")
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
				# print("ATTACK WITH ROOK")
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
				# print("ATTACK WITH ROOK")
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
				# print("ATTACK WITH ROOK")
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
				# print("ATTACK WITH ROOK")
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
				# print("ATTACK WITH ROOK")
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
				# print("ATTACK WITH ROOK")
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
				# print("ATTACK WITH ROOK")
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
				# print("ATTACK WITH ROOK")
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
				# print("ATTACK WITH ROOK")
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
				# print("ATTACK WITH ROOK")
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
				# print("ATTACK WITH ROOK")
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
				# print("ATTACK WITH ROOK")
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
				# print("ATTACK WITH ROOK")
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
				# print("ATTACK WITH ROOK")
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
				# print("ATTACK WITH ROOK")
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
				# print("ATTACK WITH ROOK")
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
				# print("ATTACK WITH ROOK")
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
				# print("ATTACK WITH ROOK")
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
				# print("ATTACK WITH ROOK")
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
				# print("ATTACK WITH ROOK")
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
				# print("ATTACK WITH ROOK")
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
				# print("ATTACK WITH ROOK")
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
				# print("ATTACK WITH ROOK")
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
				# print("ATTACK WITH ROOK")
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
				# print("ATTACK WITH ROOK")
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
				# print("ATTACK WITH ROOK")
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
				# print("ATTACK WITH ROOK")
				result.append(i)
				break
			# self block
			if board[i] in self.white_pieces or board[i] == "K" or board[i] == "k":
				break

		return result

	def get_board(self):
		return self.current_state[0]

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
			# print("error unkown file")
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
		if self.current_state[1] == 1:
			self.current_state[1] = 0
		else:
			self.current_state[1] = 1
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


if __name__ == '__main__':
	engine = IzzI()
	i = 0
	while i < 300:
		engine.run_chess()
		i += 11


