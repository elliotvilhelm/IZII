# empty : 0
# king : 1
# queen : 2
# rook : 3
# bishop : 4
# knight : 5
# pawn : 6
#
import copy
from random import randint
import time

WHITE = 0
BLACK = -1


class Piece:
	def __init__(self, ID, index, color):
		self.ID = ID
		self.row, self.column = index
		self.color = color

	def get_weight(self):
		if self.ID == 1 or -1:
			return 1000
		elif self.ID == 2 or -2:
			return 9
		elif self.ID == 3 or -3:
			return
		# elif self.ID == 4 or -4:
		# elif self.ID == 5 or -5:
		# elif self.ID == 6 or -6:

	def get_color(self):
		return self.color

	def get_piece_ID(self):
		return self.ID

	def get_index(self):
		return (self.row, self.column)

	def set_index(self, index):
		self.row, self.column = index


class BlackPawn(Piece):
	def __init__(self, index):
		Piece.__init__(self, -6, index, -1)
		self.first_move = True
		self.en_passant_vulnerable = False

	def get_possible_moves(self, board):
		possible_moves = []
		if self.get_passive_moves(board):
			possible_moves += self.get_passive_moves(board)
		if self.get_attack_moves(board):
			possible_moves += self.get_attack_moves(board)
		return possible_moves

	def get_passive_moves(self, board):
		passive_moves = []
		row_in_front = self.row + 1
		if row_in_front < 8:
			tile_in_front = board.tiles[row_in_front, self.column]
		else:
			return
		if tile_in_front.get_piece_ID() == 0:
			passive_moves.append((row_in_front, self.column))
		if self.first_move:
			if board.tiles[row_in_front+1, self.column].get_piece_ID() == 0 and board.tiles[row_in_front, self.column].get_piece_ID() == 0:
				passive_moves.append((row_in_front+1, self.column))
			# print("passive move: ", passive_move)
		return passive_moves

	def get_attack_moves(self, board):
		attack_moves = []
		if self.row == 7:
			return
		else:
			row_in_front = self.row + 1
		if self.right_clear(board):
			right_column = self.column - 1
			right_diagonal_ID = board.tiles[row_in_front, right_column].get_piece_ID()
			if right_diagonal_ID > 0 and right_diagonal_ID != 1:
				attack_moves.append((row_in_front, right_column))
		if self.left_clear(board):
			left_column = self.column + 1
			left_diagonal_ID = board.tiles[row_in_front, left_column].get_piece_ID()
			if left_diagonal_ID > 0 and left_diagonal_ID != 1:
				attack_moves.append((row_in_front, left_column))


		return attack_moves

	def get_en_passant(self, board):
		possible_passant = []
		right_index = (self.row, self.column - 1)
		if right_index not in board.tiles:
			tile_on_right = None
		else:
			tile_on_right = board.tiles[right_index]


		left_index = (self.row, self.column + 1)
		if left_index not in board.tiles:
			tile_on_left = None
		else:
			tile_on_left = board.tiles[left_index].get_piece()

		if tile_on_right != None:
			if tile_on_right.get_piece_ID() == 6:
				if tile_on_right.get_piece().en_passant_vulnerable:
					possible_passant.append((self.row+1, self.column-1))
		if tile_on_left != None:
			if tile_on_left.get_piece_ID() == 6:
				if tile_on_left.en_passant_vulnerable:
					possible_passant.append((self.row+1, self.column+1))
		return possible_passant

	def right_clear(self, board):
		if self.column == 0:
			return False
		else:
			return True

	def left_clear(self, board):
		if self.column == 7:
			return False
		else:
			return True

	def move(self, index):
		if self.row < 6:
			self.first_move = False
		if abs(index[0] - self.row) == 2:
			self.en_passant_vulnerable = True
		else:
			self.en_passant_vulnerable = False
		Piece.set_index(self, index)


class WhitePawn(Piece):
	def __init__(self, index):
		Piece.__init__(self, 6, index, 0)
		self.first_move = True
	def get_possible_moves(self, board):
		possible_moves = []
		if self.get_passive_moves(board):
			possible_moves += self.get_passive_moves(board)
		if self.get_attack_moves(board):
			possible_moves += self.get_attack_moves(board)
		return possible_moves
	def get_passive_moves(self, board):
		passive_moves = []
		row_in_front = self.row - 1
		if row_in_front > 0:
			tile_in_front = board.tiles[row_in_front, self.column]
		else:
			return
		if tile_in_front.get_piece_ID() == 0:
			passive_moves.append((row_in_front, self.column))
		if self.first_move:
			if board.tiles[row_in_front-1, self.column].get_piece_ID() == 0 and board.tiles[row_in_front, self.column].get_piece_ID() == 0:passive_moves.append((row_in_front-1, self.column))
		return passive_moves
	def get_attack_moves(self, board):
		attack_moves = []
		if self.row == 0:
			return
		else:
			row_in_front = self.row - 1
		if self.right_clear(board):
			right_column = self.column + 1
			right_diagonal_ID = board.tiles[row_in_front, right_column].get_piece_ID()
			if right_diagonal_ID < -1:
				attack_moves.append((row_in_front, right_column))
		if self.left_clear(board):
			# print("left clear")
			left_column = self.column - 1
			left_diagonal_ID = board.tiles[row_in_front, left_column].get_piece_ID()
			if left_diagonal_ID < -1:
				attack_moves.append((row_in_front, left_column))
		return attack_moves
	def get_en_passant(self, board):
		possible_passant = []
		right_index = (self.row, self.column + 1)
		if right_index not in board.tiles:
			tile_on_right = None # really tile on right as this happens for empty piece
		else:
			tile_on_right = board.tiles[right_index]

		left_index = (self.row, self.column - 1)
		if left_index not in board.tiles:
			tile_on_left = None
		else:
			tile_on_left = board.tiles[left_index]

		if tile_on_right != None:
			if tile_on_right.get_piece_ID() == -6:
				if tile_on_right.piece.en_passant_vulnerable:
					possible_passant.append((self.row-1, self.column + 1))
		if tile_on_left != None:
			if tile_on_left.get_piece_ID() == -6:
				if tile_on_left.get_piece().en_passant_vulnerable:
					possible_passant.append((self.row-1, self.column - 1))
		return possible_passant
	def right_clear(self, board):
		if self.column == 7:
			return False
		else:
			return True
	def left_clear(self, board):
		if self.column == 0:
			return False
		else:
			return True
	def move(self, index):
		if self.row < 6:
			self.first_move = False
		if abs(index[0] - self.row) == 2:
			self.en_passant_vulnerable = True
		else:
			self.en_passant_vulnerable = False
		Piece.set_index(self, index)


class WhiteBishop(Piece):
	def __init__(self, index):
		Piece.__init__(self, 4, index, 0)
	def get_possible_moves(self, board):
		possible_moves = []
		upper_right_delta = (-1, 1)
		upper_left_delta = (-1, -1)
		lower_right_delta = (1, 1)
		lower_left_delta = (1, -1)

		i = 1

		while board.validate_index((self.row + upper_left_delta[0]*i, self.column + upper_left_delta[1]*i)):
			temp_index = (self.row + upper_left_delta[0]*i, self.column + upper_left_delta[1]*i)
			id = board.tiles[temp_index].get_piece_ID()
			if id > 0: # blocked by my own color
				break
			elif id < -1: # enemy hit
				possible_moves.append(temp_index)
				break
			elif id == 0: # empty space
				possible_moves.append(temp_index) # empty space
			i += 1
		i = 1
		while board.validate_index((self.row + upper_right_delta[0]*i, self.column + upper_right_delta[1]*i)):
			temp_index = (self.row + upper_right_delta[0]*i, self.column + upper_right_delta[1]*i)
			id = board.tiles[temp_index].get_piece_ID()
			if id > 0: # blocked by my own color
				break
			elif id < -1: # enemy hit
				possible_moves.append(temp_index)
				break
			elif id == 0: # empty space
				possible_moves.append(temp_index) # empty space
			i += 1
		i = 1
		while board.validate_index((self.row + lower_left_delta[0]*i, self.column + lower_left_delta[1]*i)):
			temp_index = (self.row + lower_left_delta[0]*i, self.column + lower_left_delta[1]*i)
			id = board.tiles[temp_index].get_piece_ID()
			if id > 0: # blocked by my own color
				break
			elif id < -1: # enemy hit
				possible_moves.append(temp_index)
				break
			elif id == 0: # empty space
				possible_moves.append(temp_index) # empty space
			i += 1
		i = 1
		while board.validate_index((self.row + lower_right_delta[0]*i, self.column + lower_right_delta[1]*i)):
			temp_index = (self.row + lower_right_delta[0]*i, self.column + lower_right_delta[1]*i)
			id = board.tiles[temp_index].get_piece_ID()
			if id > 0: # blocked by my own color
				break
			elif id < -1: # enemy hit
				possible_moves.append(temp_index)
				break
			elif id == 0: # empty space
				possible_moves.append(temp_index) # empty space
			i += 1
		i = 1

		# print("White Bishop possible moves: ", possible_moves)
		return possible_moves
	def move(self, index):
		Piece.set_index(self, index)


class BlackBishop(Piece):
	def __init__(self, index):
		Piece.__init__(self, -4, index, -1)
	def get_possible_moves(self, board):
		possible_moves = []
		upper_right_delta = (1, -1)
		upper_left_delta = (1, 1)
		lower_right_delta = (-1, -1)
		lower_left_delta = (-1, 1)

		i = 1

		while board.validate_index((self.row + upper_left_delta[0]*i, self.column + upper_left_delta[1]*i)):
			temp_index = (self.row + upper_left_delta[0]*i, self.column + upper_left_delta[1]*i)
			id = board.tiles[temp_index].get_piece_ID()
			if id < 0: # blocked by my own color
				break
			elif id > 1: # enemy hit
				possible_moves.append(temp_index)
				break
			elif id == 0: # empty space
				possible_moves.append(temp_index) # empty space
			i += 1
		i = 1
		while board.validate_index((self.row + upper_right_delta[0]*i, self.column + upper_right_delta[1]*i)):
			temp_index = (self.row + upper_right_delta[0]*i, self.column + upper_right_delta[1]*i)
			id = board.tiles[temp_index].get_piece_ID()
			if id < 0: # blocked by my own color
				break
			elif id > 1: # enemy hit
				possible_moves.append(temp_index)
				break
			elif id == 0: # empty space
				possible_moves.append(temp_index) # empty space
			i += 1
		i = 1
		while board.validate_index((self.row + lower_left_delta[0]*i, self.column + lower_left_delta[1]*i)):
			temp_index = (self.row + lower_left_delta[0]*i, self.column + lower_left_delta[1]*i)
			id = board.tiles[temp_index].get_piece_ID()
			if id < 0: # blocked by my own color
				break
			elif id > 1: # enemy hit
				possible_moves.append(temp_index)
				break
			elif id == 0: # empty space
				possible_moves.append(temp_index) # empty space
			i += 1
		i = 1
		while board.validate_index((self.row + lower_right_delta[0]*i, self.column + lower_right_delta[1]*i)):
			temp_index = (self.row + lower_right_delta[0]*i, self.column + lower_right_delta[1]*i)
			id = board.tiles[temp_index].get_piece_ID()
			if id < 0: # blocked by my own color
				break
			elif id >1: # enemy hit
				possible_moves.append(temp_index)
				break
			elif id == 0: # empty space
				possible_moves.append(temp_index) # empty space
			i += 1
		i = 1

		# print("Black Bishop possible moves: ", possible_moves)
		return possible_moves
	def move(self, index):
		Piece.set_index(self, index)


class WhiteRook(Piece):
	def __init__(self, index):
		Piece.__init__(self, 3, index, 0)
		self.has_moved = False
	def get_possible_moves(self, board):
		possible_moves = []
		forward_delta = (-1, 0)
		backward_delta = (1, 0)
		right_delta = (0, 1)
		left_delta = (0, -1)

		i = 1

		while board.validate_index((self.row + forward_delta[0]*i, self.column + forward_delta[1]*i)):
			temp_index = (self.row + forward_delta[0]*i, self.column + forward_delta[1]*i)
			id = board.tiles[temp_index].get_piece_ID()
			if id > 0: # blocked by my own color
				break
			elif id < -1: # enemy hit
				possible_moves.append(temp_index)
				break
			elif id == 0: # empty space
				possible_moves.append(temp_index) # empty space
			i += 1
		i = 1
		while board.validate_index((self.row + backward_delta[0]*i, self.column + backward_delta[1]*i)):
			temp_index = (self.row + backward_delta[0]*i, self.column + backward_delta[1]*i)
			id = board.tiles[temp_index].get_piece_ID()
			if id > 0: # blocked by my own color
				break
			elif id < -1: # enemy hit
				possible_moves.append(temp_index)
				break
			elif id == 0: # empty space
				possible_moves.append(temp_index) # empty space
			i += 1
		i = 1
		while board.validate_index((self.row + right_delta[0]*i, self.column + right_delta[1]*i)):
			temp_index = (self.row + right_delta[0]*i, self.column + right_delta[1]*i)
			id = board.tiles[temp_index].get_piece_ID()
			if id > 0: # blocked by my own color
				break
			elif id < -1: # enemy hit
				possible_moves.append(temp_index)
				break
			elif id == 0: # empty space
				possible_moves.append(temp_index) # empty space
			i += 1
		i = 1
		while board.validate_index((self.row + left_delta[0]*i, self.column + left_delta[1]*i)):
			temp_index = (self.row + left_delta[0]*i, self.column + left_delta[1]*i)
			id = board.tiles[temp_index].get_piece_ID()
			if id > 0: # blocked by my own color
				break
			elif id < -1: # enemy hit
				possible_moves.append(temp_index)
				break
			elif id == 0: # empty space
				possible_moves.append(temp_index) # empty space
			i += 1
		i = 1
		# print("White Rook possible moves: ", possible_moves)
		return possible_moves
	def move(self, index):
		if self.has_moved == False:
			self.has_moved = True
		Piece.set_index(self, index)


class BlackRook(Piece):
	def __init__(self, index):
		Piece.__init__(self, -3, index, -1)
		self.has_moved = False

	def get_possible_moves(self, board):
		possible_moves = []
		forward_delta = (1, 0)
		backward_delta = (-1, 0)
		right_delta = (0, -1)
		left_delta = (0, 1)

		i = 1

		while board.validate_index((self.row + forward_delta[0] * i, self.column + forward_delta[1] * i)):
			temp_index = (self.row + forward_delta[0] * i, self.column + forward_delta[1] * i)
			id = board.tiles[temp_index].get_piece_ID()
			if id < 0:  # blocked by my own color
				break
			elif id > 1:  # enemy hit
				possible_moves.append(temp_index)
				break
			elif id == 0:  # empty space
				possible_moves.append(temp_index)  # empty space
			i += 1
		i = 1
		while board.validate_index((self.row + backward_delta[0] * i, self.column + backward_delta[1] * i)):
			temp_index = (self.row + backward_delta[0] * i, self.column + backward_delta[1] * i)
			id = board.tiles[temp_index].get_piece_ID()
			if id < 0:  # blocked by my own color
				break
			elif id > 1:  # enemy hit
				possible_moves.append(temp_index)
				break
			elif id == 0:  # empty space
				possible_moves.append(temp_index)  # empty space
			i += 1
		i = 1
		while board.validate_index((self.row + right_delta[0] * i, self.column + right_delta[1] * i)):
			temp_index = (self.row + right_delta[0] * i, self.column + right_delta[1] * i)
			id = board.tiles[temp_index].get_piece_ID()
			if id < 0:  # blocked by my own color
				break
			elif id > 1:  # enemy hit
				possible_moves.append(temp_index)
				break
			elif id == 0:  # empty space
				possible_moves.append(temp_index)  # empty space
			i += 1
		i = 1
		while board.validate_index((self.row + left_delta[0] * i, self.column + left_delta[1] * i)):
			temp_index = (self.row + left_delta[0] * i, self.column + left_delta[1] * i)
			id = board.tiles[temp_index].get_piece_ID()
			if id < 0:  # blocked by my own color
				break
			elif id > 1:  # enemy hit
				possible_moves.append(temp_index)
				break
			elif id == 0:  # empty space
				possible_moves.append(temp_index)  # empty space
			i += 1
		i = 1
		# print("Black Rook possible moves: ", possible_moves)
		return possible_moves

	def move(self, index):
		if self.has_moved == False:
			self.has_moved = True
		Piece.set_index(self, index)


class WhiteQueen(Piece):

	def __init__(self, index):
		Piece.__init__(self, 2, index, 0)

	def get_possible_moves(self, board):
		possible_moves = []
		forward_delta = (-1, 0)
		backward_delta = (1, 0)
		right_delta = (0, 1)
		left_delta = (0, -1)

		upper_right_delta = (-1, 1)
		upper_left_delta = (-1, -1)
		lower_right_delta = (1, 1)
		lower_left_delta = (1, -1)

		i = 1
		while board.validate_index((self.row + forward_delta[0]*i, self.column + forward_delta[1]*i)):
			temp_index = (self.row + forward_delta[0]*i, self.column + forward_delta[1]*i)
			id = board.tiles[temp_index].get_piece_ID()
			if id > 0: # blocked by my own color
				break
			elif id < -1: # enemy hit
				possible_moves.append(temp_index)
				break
			elif id == 0: # empty space
				possible_moves.append(temp_index) # empty space
			i += 1
		i = 1
		while board.validate_index((self.row + backward_delta[0]*i, self.column + backward_delta[1]*i)):
			temp_index = (self.row + backward_delta[0]*i, self.column + backward_delta[1]*i)
			id = board.tiles[temp_index].get_piece_ID()
			if id > 0: # blocked by my own color
				break
			elif id < -1: # enemy hit
				possible_moves.append(temp_index)
				break
			elif id == 0: # empty space
				possible_moves.append(temp_index) # empty space
			i += 1
		i = 1
		while board.validate_index((self.row + right_delta[0]*i, self.column + right_delta[1]*i)):
			temp_index = (self.row + right_delta[0]*i, self.column + right_delta[1]*i)
			id = board.tiles[temp_index].get_piece_ID()
			if id > 0: # blocked by my own color
				break
			elif id < -1: # enemy hit
				possible_moves.append(temp_index)
				break
			elif id == 0: # empty space
				possible_moves.append(temp_index) # empty space
			i += 1
		i = 1
		while board.validate_index((self.row + left_delta[0]*i, self.column + left_delta[1]*i)):
			temp_index = (self.row + left_delta[0]*i, self.column + left_delta[1]*i)
			id = board.tiles[temp_index].get_piece_ID()
			if id > 0: # blocked by my own color
				break
			elif id < -1: # enemy hit
				possible_moves.append(temp_index)
				break
			elif id == 0: # empty space
				possible_moves.append(temp_index) # empty space
			i += 1
		i = 1
		while board.validate_index((self.row + upper_left_delta[0] * i, self.column + upper_left_delta[1] * i)):
			temp_index = (self.row + upper_left_delta[0] * i, self.column + upper_left_delta[1] * i)
			id = board.tiles[temp_index].get_piece_ID()
			if id > 0:  # blocked by my own color
				break
			elif id < -1:  # enemy hit
				possible_moves.append(temp_index)
				break
			elif id == 0:  # empty space
				possible_moves.append(temp_index)  # empty space
			i += 1
		i = 1
		while board.validate_index((self.row + upper_right_delta[0] * i, self.column + upper_right_delta[1] * i)):
			temp_index = (self.row + upper_right_delta[0] * i, self.column + upper_right_delta[1] * i)
			id = board.tiles[temp_index].get_piece_ID()
			if id > 0:  # blocked by my own color
				break
			elif id < -1:  # enemy hit
				possible_moves.append(temp_index)
				break
			elif id == 0:  # empty space
				possible_moves.append(temp_index)  # empty space
			i += 1
		i = 1
		while board.validate_index((self.row + lower_left_delta[0] * i, self.column + lower_left_delta[1] * i)):
			temp_index = (self.row + lower_left_delta[0] * i, self.column + lower_left_delta[1] * i)
			id = board.tiles[temp_index].get_piece_ID()
			if id > 0:  # blocked by my own color
				break
			elif id < -1:  # enemy hit
				possible_moves.append(temp_index)
				break
			elif id == 0:  # empty space
				possible_moves.append(temp_index)  # empty space
			i += 1
		i = 1
		while board.validate_index((self.row + lower_right_delta[0] * i, self.column + lower_right_delta[1] * i)):
			temp_index = (self.row + lower_right_delta[0] * i, self.column + lower_right_delta[1] * i)
			id = board.tiles[temp_index].get_piece_ID()
			if id > 0:  # blocked by my own color
				break
			elif id < -1:  # enemy hit
				possible_moves.append(temp_index)
				break
			elif id == 0:  # empty space
				possible_moves.append(temp_index)  # empty space
			i += 1
		# print("White Queen possible moves: ", possible_moves)
		return possible_moves

	def move(self, index):
		Piece.set_index(self, index)


class BlackQueen(Piece):

	def __init__(self, index):
		Piece.__init__(self, -2, index, -1)

	def get_possible_moves(self, board):
		possible_moves = []
		forward_delta = (1, 0)
		backward_delta = (-1, 0)
		right_delta = (0, -1)
		left_delta = (0, 1)

		upper_right_delta = (1, -1)
		upper_left_delta = (1, 1)
		lower_right_delta = (-1, -1)
		lower_left_delta = (-1, 1)

		i = 1

		while board.validate_index((self.row + forward_delta[0] * i, self.column + forward_delta[1] * i)):
			temp_index = (self.row + forward_delta[0] * i, self.column + forward_delta[1] * i)
			id = board.tiles[temp_index].get_piece_ID()
			if id < 0:  # blocked by my own color
				break
			elif id == 1:
				break
			elif id > 1:  # enemy hit
				possible_moves.append(temp_index)
				break
			elif id == 0:  # empty space
				possible_moves.append(temp_index)  # empty space
			i += 1
		i = 1
		while board.validate_index((self.row + backward_delta[0] * i, self.column + backward_delta[1] * i)):
			temp_index = (self.row + backward_delta[0] * i, self.column + backward_delta[1] * i)
			id = board.tiles[temp_index].get_piece_ID()
			if id < 0:  # blocked by my own color
				break
			elif id == 1:
				break
			elif id > 1:  # enemy hit
				possible_moves.append(temp_index)
				break
			elif id == 0:  # empty space
				possible_moves.append(temp_index)  # empty space
			i += 1
		i = 1
		while board.validate_index((self.row + right_delta[0] * i, self.column + right_delta[1] * i)):
			temp_index = (self.row + right_delta[0] * i, self.column + right_delta[1] * i)
			id = board.tiles[temp_index].get_piece_ID()
			if id < 0:  # blocked by my own color
				break
			elif id == 1:
				break
			elif id > 1:  # enemy hit
				possible_moves.append(temp_index)
				break

			elif id == 0:  # empty space
				possible_moves.append(temp_index)  # empty space
			i += 1
		i = 1
		while board.validate_index((self.row + left_delta[0] * i, self.column + left_delta[1] * i)):
			temp_index = (self.row + left_delta[0] * i, self.column + left_delta[1] * i)
			id = board.tiles[temp_index].get_piece_ID()
			if id < 0:  # blocked by my own color
				break
			elif id == 1:
				break
			elif id > 1:  # enemy hit
				possible_moves.append(temp_index)
				break
			elif id == 0:  # empty space
				possible_moves.append(temp_index)  # empty space
			i += 1
		i = 1

		while board.validate_index((self.row + upper_left_delta[0] * i, self.column + upper_left_delta[1] * i)):
			temp_index = (self.row + upper_left_delta[0] * i, self.column + upper_left_delta[1] * i)
			id = board.tiles[temp_index].get_piece_ID()
			if id < 0:  # blocked by my own color
				break
			elif id == 1:
				break
			elif id > 1:  # enemy hit
				possible_moves.append(temp_index)
				break
			elif id == 0:  # empty space
				possible_moves.append(temp_index)  # empty space
			i += 1
		i = 1
		while board.validate_index((self.row + upper_right_delta[0] * i, self.column + upper_right_delta[1] * i)):
			temp_index = (self.row + upper_right_delta[0] * i, self.column + upper_right_delta[1] * i)
			id = board.tiles[temp_index].get_piece_ID()
			if id < 0:  # blocked by my own color
				break
			elif id == 1:
				break
			elif id > 1:  # enemy hit
				possible_moves.append(temp_index)
				break
			elif id == 0:  # empty space
				possible_moves.append(temp_index)  # empty space
			i += 1
		i = 1
		while board.validate_index((self.row + lower_left_delta[0] * i, self.column + lower_left_delta[1] * i)):
			temp_index = (self.row + lower_left_delta[0] * i, self.column + lower_left_delta[1] * i)
			id = board.tiles[temp_index].get_piece_ID()
			if id < 0:  # blocked by my own color
				break
			elif id == 1:
				break
			elif id > 1:  # enemy hit
				possible_moves.append(temp_index)
				break
			elif id == 0:  # empty space
				possible_moves.append(temp_index)  # empty space
			i += 1
		i = 1
		while board.validate_index((self.row + lower_right_delta[0] * i, self.column + lower_right_delta[1] * i)):
			temp_index = (self.row + lower_right_delta[0] * i, self.column + lower_right_delta[1] * i)
			id = board.tiles[temp_index].get_piece_ID()
			if id < 0:  # blocked by my own color
				break
			elif id == 1:
				break
			elif id > 1:  # enemy hit
				possible_moves.append(temp_index)
				break
			elif id == 0:  # empty space
				possible_moves.append(temp_index)  # empty space
			i += 1
		i = 1

		# print("Black Rook possible moves: ", possible_moves)
		return possible_moves

	def move(self, index):
		Piece.set_index(self, index)


class BlackKing(Piece):

	def __init__(self, index):
		Piece.__init__(self, -1, index, -1)
		self.in_check = False
		self.has_moved = False

	def get_possible_moves(self, board):
		"""there are eight squares to check"""
		# if self.test_square_for_check(board, self.get_index()) == False:
		# 	print("black King in check!!!!")

		possible_moves = []
		front = (self.row+1, self.column)
		back = (self.row-1, self.column)
		right = (self.row, self.column-1)
		left = (self.row, self.column+1)
		upper_right = (self.row+1, self.column-1)
		lower_right = (self.row-1, self.column-1)
		upper_left = (self.row+1, self.column+1)
		lower_left = (self.row-1, self.column+1)


		if self.test_square_for_check(board, front) and board.validate_index(front) and board.tiles[front].get_piece_ID() >= 0:
			possible_moves.append(front)
		if self.test_square_for_check(board, back) and board.validate_index(back) and board.tiles[back].get_piece_ID() >= 0:
			possible_moves.append(back)
		if self.test_square_for_check(board, right) and board.validate_index(right) and board.tiles[right].get_piece_ID() >= 0:
			possible_moves.append(right)
		if self.test_square_for_check(board, left) and board.validate_index(left) and board.tiles[left].get_piece_ID() >= 0:
			possible_moves.append(left)
		if board.validate_index(upper_right):
			if self.test_square_for_check(board, upper_right)  and board.tiles[upper_right].get_piece_ID() >= 0:
				possible_moves.append(upper_right)
		if self.test_square_for_check(board, upper_left) and board.validate_index(upper_left) and board.tiles[upper_left].get_piece_ID() >= 0:
			possible_moves.append(upper_left)
		if self.test_square_for_check(board, lower_right) and board.validate_index(lower_right) and board.tiles[lower_right].get_piece_ID() >= 0:
			possible_moves.append(lower_right)
		if self.test_square_for_check(board, lower_left) and board.validate_index(lower_left) and board.tiles[lower_left].get_piece_ID() >= 0:
			possible_moves.append(lower_left)

		# print("Black Kings Moves: ", possible_moves)

		# if self.test_square_for_check(board, self.get_index()) == False:
		# 	print("Black King in Check!", self.get_index())
		# 	self.test_square_for_check(board, self.get_index())
		# 	if len(possible_moves) == 0:
		# 		print("Check Mate! White"
		# 			  " Wins!")

		return possible_moves

	def test_square_for_check(self, board, index):
		"""
		:param board: chess booard
		:param index: location to be tested for safety
		:return: True or False is the index a safe spot
		"""
		if board.validate_index(index) == False:
			# print("false index : ", index)
			return False
		front_clear = self.check_front(board, index)
		back_clear = self.check_back(board, index)
		left_clear = self.check_left(board, index)
		right_clear = self.check_right(board, index)
		upper_right = self.check_upper_right(board, index)
		lower_right = self.check_lower_right(board, index)
		upper_left = self.check_upper_left(board, index)
		lower_left = self.check_lower_right(board, index)
		knights = self.check_for_knights(board, index)

		# if index == self.get_index():
			# print("testing : ", index, "front:", front_clear, " back:", back_clear, " upper_right:", upper_right, "upper left: ", upper_left,  "lower_right:", lower_right, "lower_left: ", lower_left, "knights: ", knights)

		if front_clear and back_clear and right_clear and left_clear and upper_right and lower_right and upper_left and lower_left and knights:# and board.tiles[index].get_piece_ID() >= 0:
			return True

		return False

	def check_back(self, board, index):
		row, col = index
		if board.validate_index((row-1, col)) == False:
			return True
		for i in range(index[0]-1, -1, -1): # from tile in front of me 'index[0]-1' to the 0 tile
			# print(i)
			if board.validate_index((i, index[1])): # makes sure the first index isn't off the board
				if board.tiles[i, index[1]].get_piece_color() == -1:
					return True # true meaning we are clear because we are being blocked by a piece of our own color
				if board.tiles[i, index[1]].get_piece_ID() >= 4:  # opponent is blocking themselves with horse, bishop, pawn
					return True
				if board.tiles[i, index[1]].get_piece_ID() == 2 or board.tiles[i, index[1]].get_piece_ID() == 3: # rook or queen in file
					return False
		return True # all good

	def check_front(self, board, index):
		for i in range(index[0]+1, 8):
			# if board.validate_index((i, index[i])) == False:
			# 	return False
			if board.tiles[i, index[1]].get_piece_color() == -1:
				return True  # true meaning we are clear because we are being blocked by a piece of our own color
			if board.tiles[i, index[1]].get_piece_ID() >= 4: # opponent is blocking themselves with horse, bishop, pawn
				return  True
			if board.tiles[i, index[1]].get_piece_ID() == 2 or board.tiles[i, index[1]].get_piece_ID() == 3:  # rook or queen in file
				return False
		return True  # all good

	def check_right(self, board, index):
		test_row = index[0]
		test_col = index[1] - 1
		# if board.tiles[test_row, test_col].get_piece_ID() == 6:  # OR PAWN!!!
		# 	return False
		while test_col >= 0:
			# if board.validate_index()
			if board.tiles[test_row, test_col].get_piece_color() == -1:
				return True
			if board.tiles[test_row, index[1]].get_piece_ID() >= 4: # opponent is blocking themselves with horse, bishop, pawn
				return  True
			if board.tiles[test_row, test_col].get_piece_ID() == 3 or board.tiles[test_row, test_col].get_piece_ID() == 2:  # rook or queen
				return False
			test_col -= 1
		return True

	def check_left(self, board, index):
		test_row = index[0]
		test_col = index[1] + 1
		if board.validate_index((test_row, test_col)) == False:
			return True
		# if board.tiles[test_row, test_col].get_piece_ID() == 6:  # OR PAWN!!!
		# 	return False
		while test_col <= 7:
			if board.tiles[test_row, test_col].get_piece_color() == -1:
				return True
			if board.tiles[test_row, index[1]].get_piece_ID() >= 4: # opponent is blocking themselves with horse, bishop, pawn
				return  True
			if board.tiles[test_row, test_col].get_piece_ID() == 3 or board.tiles[test_row, test_col].get_piece_ID() == 2:  # rook or queen
				return False
			test_col += 1
		return True

	def check_lower_left(self, board, index):
		test_row = index[0]-1
		test_col = index[1]+1

		while test_row >= 0 and test_col <= 7:
			# if board.validate_index()
			id = board.tiles[test_row, test_col].get_piece_ID()
			if board.tiles[test_row, test_col].get_piece_color() == -1:
				return True
			if id == 3 or id == 5 or id == 6: # diagnol is blocked
				return True
			if id == 4 or id == 2: # white bishop or queen
				return False
			test_row -= 1
			test_col += 1
		return True

	def check_upper_right(self, board, index):
		test_row = index[0]+1
		test_col = index[1]-1
		if board.validate_index((test_row, test_col)) == False:
			return False
		if board.tiles[test_row, test_col].get_piece_ID() == 6:  # OR PAWN!!!
			return False
		# color = board.tiles[test_row, test_col].get_piece().get_color()
		# if color == WHITE:
		# 	return True
		while test_row <= 7 and test_col >= 0:
			# if board.validate_index()
			id = board.tiles[test_row, test_col].get_piece_ID()
			if board.tiles[test_row, test_col].get_piece_color() == -1:

				return True
			if id == 3 or id == 5 or id == 6:  # diagonal is blocked
				return True
			if id == 4 or id == 2: # white bishop or queen
				return False
			test_row += 1
			test_col -= 1
		return True

	def check_upper_left(self, board, index):
		test_row = index[0]+1
		test_col = index[1]+1
		if board.validate_index((test_row, test_col)) == False:
			return True
		if board.tiles[test_row, test_col].get_piece_ID() == 6:  # OR PAWN!!!
			return False
		while test_row <= 7 and test_col <= 7:
			id = board.tiles[test_row, test_col].get_piece_ID()
			# if board.validate_index()
			if board.tiles[test_row, test_col].get_piece_color() == -1: # black : -1
				return True
			if id == 3 or id == 5 or id == 6:  # diagonal is blocked, rook, horse pawn
				# print("white black it with a horse / rook / ..")
				return True
			if id == 4 or id == 2: # white bishop or queen
				# print("U FUCKED white bishop snipes or queen snipes")
				return False
			else:
				pass
				# print("WHO AM I")
			test_row += 1
			test_col += 1

		return True

	def check_lower_right(self, board, index):
		test_row = index[0]-1
		test_col = index[1]-1
		while test_row >= 0 and test_col >= 0:
			id = board.tiles[test_row, test_col].get_piece_ID()
			if board.tiles[test_row, test_col].get_piece_color() == -1:
				return True
			if id == 3 or id == 5 or id == 6:  # diagonal is blocked
				return True
			if id == 4 or id == 2: # white bishop or queen
				return False
			test_row -= 1
			test_col -= 1
		return True

	def check_for_knights(self, board, index):
		test_moves = []
		row, column = index
		move_1 = (row - 2, column- 1)
		move_2 = (row- 2, column + 1)
		move_3 = (row - 1, column - 2)
		move_4 = (row - 1, column + 2)
		move_5 = (row + 1, column - 2)
		move_6 = (row + 1, column + 2)
		move_7 = (row + 2, column - 1)
		move_8 = (row + 2, column + 1)

		test_moves.append(move_1)
		test_moves.append(move_2)
		test_moves.append(move_3)
		test_moves.append(move_4)
		test_moves.append(move_5)
		test_moves.append(move_6)
		test_moves.append(move_7)
		test_moves.append(move_8)
		# print(index, "test moves" , test_moves)
		for i in range(len(test_moves)):
			if board.validate_index(test_moves[i]) == False:
				pass
				# return True
			else:
				if board.tiles[test_moves[i]].get_piece_ID() == 5:
					# print("black horse at ", test_moves[i])
					return False
		return True

	def check_king_side_castle_check_clear(self, board):
		if self.test_square_for_check(board, (0,5)) == False or self.test_square_for_check(board, (0,6)) == False:
			return False
		else:
			return True

	def king_side_castle_check(self, board):
		if self.has_moved == False:
			if board.tiles[0,7].get_piece_ID() == -3:
				if board.tiles[0,7].get_piece().has_moved == False:
					print("rook has not moved")
					if board.tiles[0,5].get_piece_ID() == 0 and board.tiles[0,6].get_piece_ID() == 0: # path is clear
						print("path for castling is clear")
						if self.check_king_side_castle_check_clear(board):
							print("king is not passing through check and will not be in check")
							return True
		else:
			return False

					# check if king will pass through a checked square
				# check if king will be in check

	def king_side_castle(self, board):
		self.move((0,6)) # moves king
		board.tiles[0,4].remove_piece()
		board.tiles[0,6].add_piece(self)
		rook = board.tiles[0,7].get_piece()
		rook.move((0,5)) # updates piece's row and column
		board.tiles[0,5].add_piece(board.tiles[0,7].get_piece()) # updates tile's piece
		board.tiles[0,7].remove_piece() # remove piece from to tile

	def check_queen_side_castle_check_clear(self, board):
		if self.test_square_for_check(board, (0, 3)) == False or self.test_square_for_check(board, (0, 2)) == False:
			return False
		else:
			return True

	def queen_side_castle_check(self, board):
		if self.has_moved == False:
			print("King has not moved")
			if board.tiles[0,0].get_piece_ID() == -3:
				if board.tiles[0,0].get_piece().has_moved == False:
					print("rook has not moved")
					if board.tiles[0,1].get_piece_ID() == 0 and board.tiles[0,2].get_piece_ID() == 0 and board.tiles[0,3].get_piece_ID() == 0:  # path is clear
						print("path for queen side castling is clear")
						if self.check_queen_side_castle_check_clear(board):
							print("king is not passing through check and will not be in check")
							return True
		else:
			return False

		# check if king will pass through a checked square
		# check if king will be in check

	def queen_side_castle(self, board):
		self.move((0, 2))  # moves king
		board.tiles[0, 4].remove_piece()
		board.tiles[0, 2].add_piece(self)
		rook = board.tiles[0, 0].get_piece()
		rook.move((0, 3))  # updates piece's row and column
		board.tiles[0, 3].add_piece(board.tiles[0, 0].get_piece())  # updates tile's piece
		board.tiles[0, 0].remove_piece()  # remove piece from to tile

	def test_self_for_check(self, board):
		return self.test_square_for_check(board, (self.row, self.column))

	def move(self, index):
		if self.has_moved == False:
			self.has_moved = True
		Piece.set_index(self, index)


class WhiteKing(Piece):

	def __init__(self, index):
		Piece.__init__(self, 1, index, 0)
		self.in_check = False
		self.has_moved = False

	def get_possible_moves(self, board):
		"""there are eight squares to check"""
		# if self.test_square_for_check(board, self.get_index()) == False:
		# 	print("white King in check!!!!")
		possible_moves = []
		front = (self.row-1, self.column)
		back = (self.row+1, self.column)
		right = (self.row, self.column+1)
		left = (self.row, self.column-1)
		upper_right = (self.row-1, self.column+1)
		lower_right = (self.row+1, self.column+1)
		upper_left = (self.row-1, self.column-1)
		lower_left = (self.row+1, self.column-1)
		index  = self.get_index()
# check is square in front puts you in check
		if self.test_square_for_check(board, front) and board.validate_index(front) and board.tiles[front].get_piece_ID() <= 0:
			possible_moves.append(front)

		if self.test_square_for_check(board, back) and board.validate_index(back) and board.tiles[back].get_piece_ID() <= 0:
			possible_moves.append(back)

		if self.test_square_for_check(board, right) and board.validate_index(right) and board.tiles[right].get_piece_ID() <= 0:
			possible_moves.append(right)

		if self.test_square_for_check(board, left) and board.validate_index(left) and board.tiles[left].get_piece_ID() <= 0:
			possible_moves.append(left)

		if self.test_square_for_check(board, upper_right) and board.validate_index(upper_right) and board.tiles[upper_right].get_piece_ID() <= 0:
			possible_moves.append(upper_right)
		if self.test_square_for_check(board, lower_left) and board.validate_index(lower_left) and board.tiles[lower_left].get_piece_ID() <= 0:
			possible_moves.append(lower_left)

		if self.test_square_for_check(board, upper_left) and board.validate_index(upper_left) and board.tiles[upper_left].get_piece_ID() <= 0:
			possible_moves.append(upper_left)

		if self.test_square_for_check(board, lower_right) and board.validate_index(lower_right) and board.tiles[lower_right].get_piece_ID() <= 0:
			possible_moves.append(lower_right)




		if self.test_square_for_check(board, self.get_index()) == False:
			self.in_check = True
			print("White King in Check!", self.get_index())
			self.test_square_for_check(board, self.get_index())
			if len(possible_moves) == 0:
				print("Check Mate! Black Wins!")
		else:
			self.in_check = False
		# print("possible moves white king: ",possible_moves)
		return possible_moves

	def test_square_for_check(self, board, index):
		"""
		:param board: chessboard object
		:param index: location to be tested for safety
		:return: True IS CLEAR or False is NOT CLEAR
		"""


		if board.validate_index(index) == False:
			return False


		front_clear = self.check_front(board, index)
		# print("front_clear: " , front_clear)
		back_clear = self.check_back(board, index)
		right_clear = self.check_right(board, index)
		left_clear = self.check_left(board, index)
		upper_right = self.check_upper_right(board, index)
		# print("upper right clear: ", upper_right)
		lower_right = self.check_lower_right(board, index)
		upper_left = self.check_upper_left(board, index)
		lower_left = self.check_lower_right(board, index)
		knights = self.check_for_knights(board, index)

		# print("testing : ", index, "front:", front_clear, " back:", back_clear, " upper_right:", upper_right, "upper left: ", upper_left,  "lower_right:", lower_right, "lower_left: ", lower_left, "knights: ", knights)

		if front_clear == True and back_clear == True and left_clear == True and right_clear == True and upper_right == True and lower_right == True and upper_left == True and lower_left == True and knights == True: # and board.tiles[index].get_piece_ID() >= 0:
			return True
		return False

	def check_front(self, board, index):
		# print(index)
		for i in range(index[0]-1, -1, -1): # from tile in front of me 'index[0]-1' to the 0 tile
			# print("Current test index: ", index)
			# print("Check Front: ", (i, index[1]))
			if board.validate_index((i, index[1])): # makes sure the first index isn't off the board
				if board.tiles[i, index[1]].get_piece_color() == 0:
					return True # true meaning we are clear because we are being blocked by a piece of our own color
				if board.tiles[i, index[1]].get_piece_ID() <= -4:  # opponent is blocking themselves with horse, bishop, pawn
					return True
				if board.tiles[i, index[1]].get_piece_ID() == -2 or board.tiles[i, index[1]].get_piece_ID() == -3: # rook or queen in file
					return False
		return True # all good

	def check_back(self, board, index):
		for i in range(index[0]+1, 8):
			# if board.validate_index((i, index[i])) == False:
			# 	return True
			if board.tiles[i, index[1]].get_piece_color() == 0:
				return True  # true meaning we are clear because we are being blocked by a piece of our own color
			if board.tiles[i, index[1]].get_piece_ID() <= -4:  # opponent is blocking themselves with horse, bishop, pawn
				return True
			if board.tiles[i, index[1]].get_piece_ID() == -2 or board.tiles[i, index[1]].get_piece_ID() == -3:  # rook or queen in file
				return False
		return True  # all good

	def check_right(self, board, index):
		test_row = index[0]
		test_col = index[1]+1
		if board.validate_index((test_row, test_col)) == False:
			return True
		# if board.tiles[test_row, test_col].get_piece_ID() == -6: # OR PAWN!!!
		# 	return False
		while test_row >= 0 and test_col <= 7:
			# if board.validate_index()
			# print("check_upper_right of ", index, " is : ", test_row, test_col)
			if board.tiles[test_row, test_col].get_piece_color() == 0:
				return True
			if board.tiles[test_row, test_col].get_piece_ID() == -4 or board.tiles[test_row, test_col].get_piece_ID() == -2: # white bishop or queen
				# print("im at: ", self.row, self.column, " i am a : ", self.get_piece_ID(), "sniper location: ", test_row, test_col, "sniper id:  ", board.tiles[test_row, test_col])
				return False
			test_col += 1
		return True

	def check_left(self, board, index):
		test_row = index[0]
		test_col = index[1]-1
		if board.validate_index((test_row, test_col-1)) == False:
			return True
		while test_col  >= 0:
			# if board.validate_index()
			# print("check_upper_right of ", index, " is : ", test_row, test_col)
			if board.tiles[test_row, test_col].get_piece_color() == 0:
				return True
			if board.tiles[test_row, test_col].get_piece_ID() == -4 or board.tiles[test_row, test_col].get_piece_ID() == -2: # white bishop or queen
				# print("im at: ", self.row, self.column, " i am a : ", self.get_piece_ID(), "sniper location: ", test_row, test_col, "sniper id:  ", board.tiles[test_row, test_col])
				return False
			test_col -= 1
		return True

	def check_upper_right(self, board, index):
		test_row = index[0]-1
		test_col = index[1]+1
		if board.validate_index((test_row, test_col)) == False:
			return True
		if board.tiles[test_row, test_col].get_piece_ID() == -6: # OR PAWN!!!
			return False
		while test_row >= 0 and test_col <= 7:
			# if board.validate_index()
			# print("check_upper_right of ", index, " is : ", test_row, test_col)
			id = board.tiles[test_row, test_col].get_piece_ID()
			if board.tiles[test_row, test_col].get_piece_color() == 0:
				return True
			if  id == -3 or id == -5 or id == -6:  # diagonal is blocked
				return True
			if id == -4 or id == -2: # white bishop or queen
				# print("im at: ", self.row, self.column, " i am a : ", self.get_piece_ID(), "sniper location: ", test_row, test_col, "sniper id:  ", board.tiles[test_row, test_col])
				return False
			test_row -= 1
			test_col += 1
		return True

	def check_lower_left(self, board, index):
		test_row = index[0]+1
		test_col = index[1]-1
		while test_row <= 7 and test_col >= 0:
			id = board.tiles[test_row, test_col].get_piece_ID()
			print("lower left :", test_row, test_col)
			# if board.validate_index()
			if board.tiles[test_row, test_col].get_piece_color() == 0:
				return True
			if id == -3 or id ==-5 or id == -6:  # diagonal is blocked
				return True
			if id == -4 or id == -2: # white bishop or queen
				return False
			test_row += 1
			test_col -= 1
		return True

	def check_lower_right(self, board, index):
		test_row = index[0]+1
		test_col = index[1]+1
		while test_row <= 7 and test_col <= 7:
			# if board.validate_index()
			id = board.tiles[test_row, test_col].get_piece_ID()
			if board.tiles[test_row, test_col].get_piece_color() == 0:
				return True
			if id == -3 or id == -5 or id == -6:  # diagonal is blocked
				return True
			if id == -4 or id == -2: # white bishop or queen
				return False
			test_row += 1
			test_col += 1
		return True

	def check_upper_left(self, board, index):
		test_row = index[0]-1
		test_col = index[1]-1
		if board.validate_index((test_row,test_col)) == False:
			return True
		if board.tiles[test_row, test_col].get_piece_ID() == -6: # OR PAWN!!!
			return False
		while test_row >= 0 and test_col >= 0:
			id = board.tiles[test_row, test_col].get_piece_ID()
			if board.tiles[test_row, test_col].get_piece_color() == 0:
				# print("protected by white®", test_row, test_col)
				return True
			if id == -3 or id == -5 or id == -6:  # diagonal is blocked
				# print("blocked black piece®", test_row, test_col)
				return True
			if id == -4 or id == -2: # black bishop or queen

				# print("nigger sniper")
				return False
			test_row -= 1
			test_col -= 1
		return True

	def check_for_knights(self, board, index):
		# print("checking if knights are attacking", index)
		test_moves = []
		row, column = index
		move_1 = (row - 2, column- 1)
		move_2 = (row- 2, column + 1)
		move_3 = (row - 1, column - 2)
		move_4 = (row - 1, column + 2)
		move_5 = (row + 1, column - 2)
		move_6 = (row + 1, column + 2)
		move_7 = (row + 2, column - 1)
		move_8 = (row + 2, column + 1)

		test_moves.append(move_1)
		test_moves.append(move_2)
		test_moves.append(move_3)
		test_moves.append(move_4)
		test_moves.append(move_5)
		test_moves.append(move_6)
		test_moves.append(move_7)
		test_moves.append(move_8)
		# print(index, "test moves" , test_moves)
		for i in range(len(test_moves)):
			if board.validate_index(test_moves[i]) == False:
				# return True
				pass
			else:
				if board.tiles[test_moves[i]].get_piece_ID() == -5:
					# print("black horse at ", test_moves[i])
					return False
		return True

	def check_king_side_castle_check_clear(self, board):
		if self.test_square_for_check(board, (7,5)) == False or self.test_square_for_check(board, (7,6)) == False:
			return False
		else:
			return True

	def king_side_castle_check(self, board):
		if self.has_moved == False:
			print("King has not moved")
			if board.tiles[7,7].get_piece_ID() == 3:
				if board.tiles[7,7].get_piece().has_moved == False:
					print("rook has not moved")
					if board.tiles[7,5].get_piece_ID() == 0 and board.tiles[7,5].get_piece_ID() == 0: # path is clear
						print("path for castling is clear")
						if self.check_king_side_castle_check_clear(board):
							print("king is not passing through check and will not be in check")
							return True
		else:
			return False

					# check if king will pass through a checked square
				# check if king will be in check

	def king_side_castle(self, board):
		self.move((7,6)) # moves king
		board.tiles[7,4].remove_piece()
		board.tiles[7,6].add_piece(self)
		rook = board.tiles[7,7].get_piece()
		rook.move((7,5)) # updates piece's row and column
		board.tiles[7,5].add_piece(board.tiles[7,7].get_piece()) # updates tile's piece
		board.tiles[7,7].remove_piece() # remove piece from to tile

	def check_queen_side_castle_check_clear(self, board):
		if self.test_square_for_check(board, (7, 3)) == False or self.test_square_for_check(board, (7, 2)) == False:
			return False
		else:
			return True

	def queen_side_castle_check(self, board):
		if self.has_moved == False:
			print("King has not moved")
			if board.tiles[7,0].get_piece_ID() == 3:
				if board.tiles[7,0].get_piece().has_moved == False:
					print("rook has not moved")
					if board.tiles[7,1].get_piece_ID() == 0 and board.tiles[7,2].get_piece_ID() == 0 and board.tiles[7,3].get_piece_ID() == 0:  # path is clear
						print("path for queen side castling is clear")
						if self.check_queen_side_castle_check_clear(board):
							print("king is not passing through check and will not be in check")
							return True
		else:
			return False

		# check if king will pass through a checked square
		# check if king will be in check

	def queen_side_castle(self, board):
		self.move((7, 2))  # moves king
		board.tiles[7, 4].remove_piece()
		board.tiles[7, 2].add_piece(self)
		rook = board.tiles[7, 0].get_piece()
		rook.move((7, 3))  # updates piece's row and column
		board.tiles[7, 3].add_piece(board.tiles[7, 0].get_piece())  # updates tile's piece
		board.tiles[7, 0].remove_piece()  # remove piece from to tile

	def test_self_for_check(self, board):
		return self.test_square_for_check(board, (self.row, self.column))

	def move(self, index):
		if self.has_moved == False:
			self.has_moved = True
		Piece.set_index(self, index)


class WhiteKnight(Piece):
	def __init__(self, index):
		Piece.__init__(self, 5, index, 0)

	def get_possible_moves(self, board):
		possible_moves = []
		test_moves = []

		move_1 = (self.row-2, self.column-1)
		move_2 = (self.row-2, self.column+1)
		move_3 = (self.row-1, self.column-2)
		move_4 = (self.row-1, self.column+2)
		move_5 = (self.row+1, self.column-2)
		move_6 = (self.row+1, self.column+2)
		move_7 = (self.row+2, self.column-1)
		move_8 = (self.row+2, self.column+1)

		test_moves.append(move_1)
		test_moves.append(move_2)
		test_moves.append(move_3)
		test_moves.append(move_4)
		test_moves.append(move_5)
		test_moves.append(move_6)
		test_moves.append(move_7)
		test_moves.append(move_8)

		for i in range(len(test_moves)):
			if board.validate_index(test_moves[i]):
				if board.tiles[test_moves[i]].get_piece_ID() == 0:
					possible_moves.append(test_moves[i])
				elif board.tiles[test_moves[i]].get_piece_ID() < -1:
					possible_moves.append(test_moves[i])
				elif board.tiles[test_moves[i]].get_piece_ID() > 0:
					pass

		# print("White Knight possible moves: ", possible_moves)
		return possible_moves

	def move(self, index):
		Piece.set_index(self, index)


class BlackKnight(Piece):

	def __init__(self, index):
		Piece.__init__(self, -5, index, -1)

	def get_possible_moves(self, board):
		possible_moves = []
		test_moves = []

		move_1 = (self.row-2, self.column-1)
		move_2 = (self.row-2, self.column+1)
		move_3 = (self.row-1, self.column-2)
		move_4 = (self.row-1, self.column+2)
		move_5 = (self.row+1, self.column-2)
		move_6 = (self.row+1, self.column+2)
		move_7 = (self.row+2, self.column-1)
		move_8 = (self.row+2, self.column+1)

		test_moves.append(move_1)
		test_moves.append(move_2)
		test_moves.append(move_3)
		test_moves.append(move_4)
		test_moves.append(move_5)
		test_moves.append(move_6)
		test_moves.append(move_7)
		test_moves.append(move_8)

		for i in range(len(test_moves)):
			if board.validate_index(test_moves[i]):
				if board.tiles[test_moves[i]].get_piece_ID() == 0:
					possible_moves.append(test_moves[i])
				elif board.tiles[test_moves[i]].get_piece_ID() > 1:
					possible_moves.append(test_moves[i])
				elif board.tiles[test_moves[i]].get_piece_ID() < 0:
					pass
		# print("Black Knight possible moves: ", possible_moves)
		return possible_moves

	def move(self, index):
		Piece.set_index(self, index)


class Tile:
	def __init__(self, row, column, piece=None):
		self.row = row
		self.column = column
		self.piece = piece
	def add_piece(self, piece):
		self.piece = piece
	def remove_piece(self):
		self.piece = None
	def empty(self):
		if self.piece == None:
			return True
		else:
			return False
	def get_piece(self):
		if self.empty() != True:
			return self.piece
		else:
			return None
	def get_piece_ID(self):
		if self.piece == None:
			return 0
		else:
			return self.piece.ID
	def get_index(self):
		return (self.row, self.column)
	def get_info(self):
		symbol = ' '
		if self.get_piece_ID() == -6:
			symbol = '\u2659'
		if self.get_piece_ID() == 6:
			symbol = '\u265f'
		if self.get_piece_ID() == -1:
			symbol = '\u2654'
		if self.get_piece_ID() == 1:
			symbol = '\u265A'
		if self.get_piece_ID() == 4: # bishop
			symbol = '\u265D'
		if self.get_piece_ID() == -4:
			symbol = '\u2657'
		if self.get_piece_ID() == 3: # rook
			symbol = '\u265C'
		if self.get_piece_ID() == -3:
			symbol = '\u2656'
		if self.get_piece_ID() == 2:  # queen
			symbol = '\u265B'
		if self.get_piece_ID() == -2:
			symbol = '\u2655'
		if self.get_piece_ID() == 5:  # queen
			symbol = '\u265E'
		if self.get_piece_ID() == -5:
			symbol = '\u2658'

		""" DEBUG PRINT"""
		# return "(" + str(self.row) + ", " + str(self.column) + ") " + symbol #str(self.get_piece_ID())
		""" Chess Notation"""
		return self.index_to_chess_notation((self.row, self.column)) + " " + symbol + "(" + str(self.row) + ", " + str(self.column) + ") " # + symbol #str(self.get_piece_ID())
		return symbol  # str(self.get_piece_ID())
	def get_piece_color(self):
		if self.empty():
			return None
		else:
			return self.piece.get_color()
	def index_to_chess_notation(self, index):
		letters = "ABCDEFGH"
		numbers = "87654321"
		return letters[index[1]] + numbers[index[0]]


class Board:

	def __init__(self):
		self.tiles = {}
		self.initialize_board()
		self.turn = 0 # white first

	def initialize_board(self):
		for i in range(8):
			for j in range(8):
				self.tiles.update({(i,j): Tile(i,j)})
		for i in range(8):
			self.tiles[1,i].add_piece(BlackPawn(self.tiles[1,i].get_index()))
		for i in range(8):
			self.tiles[6, i].add_piece(WhitePawn(self.tiles[6, i].get_index()))
		self.tiles[0,4].add_piece(BlackKing(self.tiles[0,4].get_index()))
		self.tiles[7,4].add_piece(WhiteKing(self.tiles[7,4].get_index()))
		self.tiles[7,2].add_piece(WhiteBishop(self.tiles[7,2].get_index()))
		self.tiles[7,5].add_piece(WhiteBishop(self.tiles[7,5].get_index()))
		self.tiles[0, 2].add_piece(BlackBishop(self.tiles[0, 2].get_index()))
		self.tiles[0, 5].add_piece(BlackBishop(self.tiles[0, 5].get_index()))
		self.tiles[7, 0].add_piece(WhiteRook(self.tiles[7, 0].get_index()))
		self.tiles[7, 7].add_piece(WhiteRook(self.tiles[7, 7].get_index()))
		self.tiles[0, 0].add_piece(BlackRook(self.tiles[0, 0].get_index()))
		self.tiles[0, 7].add_piece(BlackRook(self.tiles[0, 7].get_index()))
		self.tiles[7, 3].add_piece(WhiteQueen(self.tiles[7, 3].get_index()))
		self.tiles[0, 3].add_piece(BlackQueen(self.tiles[0, 3].get_index()))
		self.tiles[7, 1].add_piece(WhiteKnight(self.tiles[7, 1].get_index()))
		self.tiles[7, 6].add_piece(WhiteKnight(self.tiles[7, 6].get_index()))
		self.tiles[0, 1].add_piece(BlackKnight(self.tiles[0, 1].get_index()))
		self.tiles[0, 6].add_piece(BlackKnight(self.tiles[0, 6].get_index()))

	def show_board(self):
		row = []
		for i in range(8):
			for j in range(8):
				row.append(self.tiles[(i,j)].get_info())
			print(str(8-i), row)
			row.clear()
		print("    A    B    C    D    E    F    G    H")
		print("")

	def validate_index(self, index):
		if index in self.tiles:
			return True
		else:
			return False

	def index_to_chess_notation(self, index):
		letters = "ABCDEFGH"
		numbers = "87654321"
		return (letters[index[1]], numbers[index[0]])

	def just_move(self, from_index, to_index):
		move_me = self.tiles[from_index].get_piece()
		if move_me == None:
			print("move me: ", move_me, "from index :", from_index)
			return False
		self.clear_en_passants()  # ehh en passant is a bitch
		move_me.move(to_index)  # updates piece's row and column
		self.tiles[to_index].add_piece(self.tiles[from_index].get_piece())  # updates tile's piece
		self.tiles[from_index].remove_piece()  # remove piece from to tile
		self.turn = 1 if self.turn == 0 else 0  # switch player turn
		return True

	def move(self, turn_color, from_index, to_index):
		## testing :
		self.get_all_possible_moves()

		if turn_color != self.turn:
			print("idk how tf this would happen")
			return False
		elif not self.validate_index(from_index) or not self.validate_index(to_index):
			print("out of index")
			return False
		elif self.tiles[from_index].get_piece_ID() == 0:
			print("from index is an empty square")
			return False
		elif self.tiles[from_index].get_piece().color != -1*self.turn:
			print("wrong color piece")
			return False

		all_moves = self.get_all_possible_moves()
		print("ALL MOVES: ", all_moves)

		move_me = self.tiles[from_index].get_piece()
		possible_moves = move_me.get_possible_moves(self)
		arman_bitch = []
		for i in range(len(possible_moves)):
			arman_bitch.append(self.index_to_chess_notation(possible_moves[i]))
		print("possible moves for ", self.index_to_chess_notation(from_index), "is : ", arman_bitch)

		"""deal with check"""
		# get king index
		# # test if he is in check
		# for index, tile in self.tiles.items():
		# 	piece = tile.get_piece()
		# 	if tile.get_piece_ID() == 1 and self.turn == 0:
		# 		clear = piece.test_square_for_check(self, index)
		# 		if not clear:
		# 			# THREE OPTIONS
		# 			# 1 move king out of check
		# 			# king_moves = piece.get_possible_moves()
		#
		# 			print("white king in check")
		# 	elif tile.get_piece_ID() == -1 and self.turn == -1:
		# 		clear = piece.test_square_for_check(self, index)
		# 		if not clear:
		# 			print("black king in check")


		"""deal with en passant"""
		passant = []
		if move_me.get_piece_ID() == 6 or move_me.get_piece_ID() == -6:
			passant = move_me.get_en_passant(self)
		if to_index in passant:
			if self.turn == 0:
				self.tiles[to_index[0]+1, to_index[1]].remove_piece()
				move_me.move(to_index)
				self.tiles[to_index].add_piece(self.tiles[from_index].get_piece())
				self.tiles[from_index].remove_piece()
				self.turn = 1
			else:
				self.tiles[to_index[0] - 1, to_index[1]].remove_piece()
				move_me.move(to_index)
				self.tiles[to_index].add_piece(self.tiles[from_index].get_piece())
				self.tiles[from_index].remove_piece()
				self.turn = 0
			return True
		"""castling"""
		if move_me.get_piece_ID() == 1: # white king
			if to_index == (7,6): # king side Castle for white
				possible_castle = move_me.king_side_castle_check(self)
				if possible_castle:
					move_me.king_side_castle(self)
					self.turn = 1 if self.turn == 0 else 0  # switch player turn
					return True
			if to_index == (7, 2): # queen side castle for king
				possible_castle = move_me.queen_side_castle_check(self)
				if possible_castle:
					move_me.queen_side_castle(self)
					self.turn = 1 if self.turn == 0 else 0  # switch player turn
					return True
		if move_me.get_piece_ID() == -1:
			if to_index == (0,6): # king side Castle for white
				possible_castle = move_me.king_side_castle_check(self)
				if possible_castle:
					move_me.king_side_castle(self)
					self.turn = 1 if self.turn == 0 else 0  # switch player turn
					return True
			if to_index == (0, 2): # queen side castle for king
				possible_castle = move_me.queen_side_castle_check(self)
				if possible_castle:
					move_me.queen_side_castle(self)
					self.turn = 1 if self.turn == 0 else 0  # switch player turn
					return True
		"""regular move"""
		if to_index not in possible_moves:
			print("Not a valid to_index")
			return False
		else:
			self.clear_en_passants() # ehh en passant is a bitch
			move_me.move(to_index) # updates piece's row and column
			self.tiles[to_index].add_piece(self.tiles[from_index].get_piece()) # updates tile's piece
			self.tiles[from_index].remove_piece() # remove piece from to tile
			self.turn = 1 if self.turn == 0 else 0 # switch player turn
			return True

	def get_all_possible_moves(self):
		all_moves = []
		possible_moves = []
		king_moves = []
		passant = []
		for index, tile in self.tiles.items():
			id = tile.get_piece_ID()
			if self.turn == 0:
				if id > 0:
					piece = tile.get_piece()
					if id == 1:
						king_set = piece.get_possible_moves(self)
						for i in range(len(king_set)):
							king_moves.append([piece.get_index(), king_set[i]])
						# king_moves.append(piece.get_possible_moves(self))
					# else:
					possible_moves = piece.get_possible_moves(self)
					if id == 6:
						possible_moves += piece.get_en_passant(self)
					# print("id: ", tile.get_piece_ID(), "location: ", index, "moves: ", possible_moves)
					for i in range(len(possible_moves)):
						all_moves.append([piece.get_index(), possible_moves[i]])

			elif self.turn == 1:
				if id < 0:
					piece = tile.get_piece()
					if id == -1:
						king_set = piece.get_possible_moves(self)
						for i in range(len(king_set)):
							king_moves.append([piece.get_index(), king_set[i]])
					# else:
					possible_moves = piece.get_possible_moves(self)
					if id == -6:
						possible_moves += piece.get_en_passant(self)
					# print("id: ", tile.get_piece_ID(), "location: ", index, "moves: ", possible_moves)
					for i in range(len(possible_moves)):
						all_moves.append([piece.get_index(), possible_moves[i]])
			# print(index)
		# if self.check_king() == False:
		# 	return king_moves
		# print("KING MOVES", king_moves)
		# for i in range(len(king_moves)-1):
		# 	print("kings moves: ", self.index_to_chess_notation(king_moves[i]))

		for index, tile in self.tiles.items():
			# print("FUCK")
			piece = tile.get_piece()
			if tile.get_piece_ID() == 1 and self.turn == 0:
				king_index = piece.get_index()
				clear = piece.test_square_for_check(self, index)
				if not clear:
					# THREE OPTIONS
					# 1 move king out of check
					# 2 take
					# 3 take or block with other piece
					print("white king in check")
					temp_board = copy.deepcopy(self)  # make a deep copy of y
					# temp_board.show_board()
					# print("deep copy: ", temp_board)
					for index, tile in temp_board.tiles.items():
						print("index: ", index, "tile: ", tile.get_piece())
					# print("king index", king_index)
					# temp_board = Game()
					# temp_board.tiles = self.tiles
					for i in range(len(all_moves)):
						# print("testing  move: ", all_moves[i][0], all_moves[i][1])
						temp_king = temp_board.tiles[king_index].get_piece()
						# for index, piece range(len(temp_board.b))
						# print("tiles", temp_board.tiles)
						temp_board.just_move(all_moves[i][0], all_moves[i][1])
						if temp_king == None:
							print("temp king is None")
						elif temp_king.test_square_for_check(temp_board, king_index):  # kinlear
							king_moves.append(all_moves[i])



						temp_board = copy.deepcopy(self)  # make a deep copy of y
					# king_moves = piece.get_possible_moves()
					# for i in range(len(king_moves)-1):
					# 	print("kings moves: ", self.index_to_chess_notation(king_moves[i]))
					print("KING MOVES", king_moves)
					return king_moves
			elif tile.get_piece_ID() == -1 and self.turn == 1:
				king_index = piece.get_index()
				clear = piece.test_square_for_check(self, index)
				if not clear:
					print("black king in check")

					temp_board = copy.deepcopy(self)  # make a deep copy of y
					# temp_board.show_board()
					# temp_board = Board()
					# temp_board.tiles = dict(self.tiles)
					for i in range(len(all_moves)):
						temp_board.just_move(all_moves[i][0], all_moves[i][1])
						temp_king = temp_board.tiles[king_index].get_piece()
						if temp_king == None:
							print("temp king is None")
						elif temp_king.test_square_for_check(temp_board, king_index):  # king is now clear
							king_moves.append(all_moves[i])
						temp_board = copy.deepcopy(self)  # make a deep copy of y
					# for i in range(len(king_moves)-1):
					# 	print("kings moves: ", self.index_to_chess_notation(king_moves[i]))
					print("KING MOVES", king_moves)
					return king_moves
		# for i in range(len(all_moves)):
		# 	print("All move: ", self.index_to_chess_notation(all_moves[i][0]), self.index_to_chess_notation(all_moves[i][1]))
		return all_moves

	def clear_en_passants(self):
		for index, tile in self.tiles.items():
			## sneak this in for now
			#############
			########## adding promotion very dirty tsk tsk here tsk
			id = tile.get_piece_ID()
			if id == 6 or id == -6:
				tile.piece.en_passant_vulnerable = False
				if id == 6:
					index = tile.get_index()
					if index[0] == 0:
						self.tiles[index].remove_piece()
						self.tiles[index].add_piece(WhiteQueen(index))
				else:
					if index[0] == 7:
						self.tiles[index].remove_piece()
						self.tiles[index].add_piece(BlackQueen(index))

	def evaluate_board(self):
		id_weights = []
		id_to_weight = {1: 900, 2: 9, 3: 5, 4: 3, 5: 3, 6: 1}
		for index, tile in self.tiles.items():
			id = tile.get_piece_ID()
			if id != 0:
				weight = id_to_weight[abs(id)]
				id_weights.append([abs(id), weight])


			# print("piece weight", weight)
		# print("ID WEIGHTS!: ", id_weights)


class Player:
	def __init__(self, color, board):
		self.color = color
		self.board = board

	def make_move(self, start_index, end_index):
		success = self.board.move(self.color, start_index, end_index)
		return success


class Game:
	def __init__(self):
		self.board = Board()
		self.player1 = Player(0, self.board)
		self.player2 = Player(1, self.board)
	def run(self):
		self.board.show_board()
		while True:
			success = self.player_one_move()
			while success == False:
				self.board.show_board()
				success = self.player_one_move()

			self.board.show_board()
			success = self.player_two_move()
			while success == False:
				self.board.show_board()
				success = self.player_two_move()
			self.board.show_board()
	def test_run_list(self, indexes):
		i = 0
		j = 1
		while j < len(indexes):
			self.board.show_board()
			self.player1.make_move(indexes[i][0], indexes[i][1])
			# print(indexes[i][0], indexes[i][1])
			self.board.show_board()
			self.player2.make_move(indexes[j][0], indexes[j][1])
			# print(indexes[j][0], indexes[j][1])
			i += 2
			j += 2
	def test_run_chess_notation(self, indexes):
		for i in range(len(indexes)):
			# row = self.chess_notation_to_index(indexes[i][0])
			# col = self.chess_notation_to_index(indexes[i][1])
			# self.board.move(row, col)
			if self.board.turn == 0:
				self.board.show_board()
				print("indexes: ", indexes)
				self.player1.make_move(self.chess_notation_to_index(indexes[i][0]), self.chess_notation_to_index(indexes[i][1]))
			else:
				self.board.show_board()
				self.player2.make_move(self.chess_notation_to_index(indexes[i][0]), self.chess_notation_to_index(indexes[i][1]))
			print("Move Number: ", i+1, " ", indexes[i])
			print(indexes[i])
		# input()
		# self.board.show_board()
		# print(indexes[i])
	def random_step(self):
		all_moves = self.board.get_all_possible_moves()
		# if self.board.check_king() == False:
		# 	print("CHECK")
		# if all_moves == None or len(all_moves) == 0:
		# 	# if self.board.turn == 0:
		# 	if self.board.check_king() == False:
		# 		print("MATE")
		# 		print("NO MOVES!")
		# 		return False
		# print("all moves", all_moves)

		if len(all_moves) == 0:
			time.sleep(100)
			# while True:
			# 	print("NO FUCKING MOVES")
		random_int = randint(0, len(all_moves) - 1)
		print(random_int, len(all_moves))
		move = all_moves[random_int]
		print("move: ", self.index_to_chess_notation(move[0]), self.index_to_chess_notation(move[1]))
		if self.board.turn == 0:
			success = self.player1.make_move(move[0], move[1])
			self.board.turn = 1
		else:
			success = self.player2.make_move(move[0], move[1])
			self.board.turn = 0

		return success
	def step(self, index):
		if self.board.turn == 0:
			self.board.show_board()
			self.player1.make_move(self.chess_notation_to_index(index[0]), self.chess_notation_to_index(index[1]))
		else:
			self.board.show_board()
			self.player2.make_move(self.chess_notation_to_index(index[0]), self.chess_notation_to_index(index[1]))
			# print("Move Number: ", i+1, " ", indexes[i])
	def player_one_move(self):
		start_index = self.chess_notation_to_index(input("Player 1 Enter start index:  "))
		end_index = self.chess_notation_to_index(input("Player 1 Enter end index:  "))
		success = self.player1.make_move(start_index, end_index)
		return  success
	def player_two_move(self):
		start_index = self.chess_notation_to_index(input("Player 2 Enter start index:  "))
		end_index = self.chess_notation_to_index(input("Player 2 Enter end index:  "))
		success = self.player2.make_move(start_index, end_index)
		return success
	def index_to_chess_notation(self, index):
		letters = "ABCDEFGH"
		numbers = "87654321"
		return (letters[index[1]], numbers[index[0]])
	def chess_notation_to_index(self, index):
		letters = "ABCDEFGH"
		index = index.upper()
		column_letter = index[0]
		row_number = index[1]
		row_index = 8 - int(row_number)
		column_index = letters.index(column_letter)
		return (row_index, column_index)





