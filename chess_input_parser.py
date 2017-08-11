import BoardRepresentation as chess


def algebraic_notation_input(alg_not):
	input = []
	squares = "abcdefgh"
	pieces = "KQNRB"
	capture = "x"
	numbers = "123456789"
	castle = "O-"
	to_indexes = []
	to_index = ""
	i = 0

	# print(len(alg_not))
	while i < len(alg_not):
		if alg_not[i] in numbers and alg_not[i-1] in squares:
			to_index += alg_not[i]
			i +=1
		elif alg_not[i] in numbers:
			i += 1
		elif alg_not[i] == "O":
			to_index += alg_not[i]
			i += 1
		elif alg_not[i] == "-":
			to_index += alg_not[i]
			i += 1
		elif alg_not[i] == ".":
			i+=1
		elif alg_not[i] == "0":
			i += 1
		elif alg_not[i] in numbers:
			to_index += alg_not[i]
			i+= 1
		elif alg_not[i] == " ":
			if to_index != "":
				to_indexes.append(to_index)
			to_index = ""
			i += 1
		elif alg_not[i] == capture:
			i += 1
		elif alg_not[i] in squares:
			to_index += alg_not[i]
			i += 1
		elif alg_not[i] == capture:
				i += 1
		elif alg_not[i] in pieces:
			to_index += alg_not[i]
			i += 1
		else:
			# print("else", alg_not[i])
			i+=1
	to_indexes.append(to_index)
	# print(to_indexes)
	return to_indexes


def generate_from_indexes(to_indexes):
	Chess = chess.Game()

	pieces = "KQNRB"
	squares = "abcdefgh"
	pairs = []
	piece_dict = {"K":1, "Q":2, "R":3, "B":4, "N":5}
	file = {"a": 0, "b": 1, "c": 2, "d": 3, "e":4, "f":5, "g":6, "h":7}
	turn = 0 # white
	turn_mult = 1
	numbers = "0123456789"
	from_file = ""
	to_indexes_cleaned = []

	for i in range(len(to_indexes)):
		print("Move: ", i)
		to_index = to_indexes[i]

		# print("given to index: ", to_index)


		if to_index[0] in pieces: 		# if it is a king queen rook bishop knight move
			print("not pawn", i)
			# print(i, pairs, len(pairs))
			id = piece_dict[to_index[0]]
			id = id * turn_mult
			# print("ID: ", id)
			# find out where the KQNR is
			# see if file is given
			if to_index[2] in squares: # file is given as in two of the same could hit, !! knight and rook !!
			# 	print("file is given, id: ", id, to_index)
				from_file = to_index[1]
				from_row = None
				real_to_index = to_index[2]+to_index[3]
			elif to_index[1] in numbers:
				# print("SPECIAL BITCH", to_index)
				from_row = to_index[1]
				real_to_index = to_index[2]+to_index[3]
			else:
				print("given standard", to_index)
				from_file = None
				from_row = None
				real_to_index = to_index[1]+to_index[2]

			print(real_to_index)
			for index, tile  in Chess.board.tiles.items(): # look through board
				if tile.get_piece_ID() == id: # if same id as yo
					piece = tile.get_piece()
					moves = piece.get_possible_moves(Chess.board) # get possible moves
					print("moves : ", moves, "ID: ", piece.ID, "pos: ", piece.get_index(), "move to: ", chess_notation_to_index(real_to_index))
					if chess_notation_to_index(real_to_index) in moves:
						# print("MOVES", moves)
						if from_file == None:
							pairs.append([index_to_chess_notation(piece.get_index()), real_to_index])
						else:
							index = piece.get_index()
							if file[from_file] == index[1]:
								pairs.append([index_to_chess_notation(piece.get_index()), real_to_index])
						# if from_file != None:
						# 	index = piece.get_index()
						# 	if file[from_file] == index[1]:
						# 		pairs.append([index_to_chess_notation(piece.get_index()), real_to_index])
						# if from_row != None:
						# 	index = piece.get_index()
						# 	if piece.row == index[1]:
						# 		pairs.append([index_to_chess_notation(piece.get_index()), real_to_index])
						# else:
						# 	pairs.append([index_to_chess_notation(piece.get_index()), real_to_index])


						# print("its in knight: ", piece.get_index(), index_to_chess_notation(piece.get_index()))
						# print(pairs[i])
			print("i: ", i, len(pairs)-1)
			temp = len(pairs)-1
			Chess.test_run_chess_notation([pairs[temp]])  # should work when its all there
			# Chess.test_run_chess_notation([pairs[i]]) # should work when its all there
			# else:
			# 	real_to_index = to_index[1]+to_index[2]
			# 	# print("real_ to index: ", real_to_index)

		elif to_index[0] in squares:
			# print("i: ", i, len(pairs)-1)
			print("pawn", i)
			id = 6 * turn_mult # pawn
			if to_index[1] in squares:
				from_file = to_index[0]
				real_to_index = to_index[1]+to_index[2]
				print("pawn capture, real_to: ", real_to_index, "from file: ", from_file)
				# pawn capture
				# passant = []
				# passant = piece.get_en_passant(self)
				# if to_index in passant:
				# 	if self.turn == 0:
				# 		self.tiles[to_index[0] + 1, to_index[1]].remove_piece()
				# 		move_me.move(to_index)
				# 		self.tiles[to_index].add_piece(self.tiles[from_index].get_piece())
				# 		self.tiles[from_index].remove_piece()
				# 		self.turn = 1
				# 	else:
				# 		self.tiles[to_index[0] - 1, to_index[1]].remove_piece()
				# 		move_me.move(to_index)
				# 		self.tiles[to_index].add_piece(self.tiles[from_index].get_piece())
				# 		self.tiles[from_index].remove_piece()
				# 		self.turn = 0
				# 	return True

			else:
				from_file = None
				real_to_index = to_index


			for index, tile  in Chess.board.tiles.items(): # look through board
				if tile.get_piece_ID() == id: # if same id as yo
					piece = tile.get_piece()
					moves = piece.get_possible_moves(Chess.board) # get possible moves
					passant = piece.get_en_passant(Chess.board)
					if passant:
						moves+=passant
					print("pawn :", piece.get_index(), "moves: ", moves)
					if chess_notation_to_index(real_to_index) in moves:
						if  from_file == None:
							pairs.append([index_to_chess_notation(piece.get_index()), real_to_index])
						else:
							index = piece.get_index()
							print("from",from_file)
							if file[from_file] == index[1]:
								pairs.append([index_to_chess_notation(piece.get_index()), real_to_index])
			print("i: ", i, len(pairs) - 1)

			temp = len(pairs) - 1
			Chess.test_run_chess_notation([pairs[temp]])  # should work when its all
			# Chess.test_run_chess_notation([pairs[i]])  # should work when its all there


							# print("possible_moves PAWN = ", moves)
				# print("pawn up: ", real_to_index)
				# pawn move up
			# pairs.append(['', to_index])
		# else:
		# 	print("CASTLINGGG", to_index)
		elif to_index == "O-O":
			print('king castle')
			if turn == 0:
				from_index = 'e1'
				to_index = 'g1'
			else:
				from_index = 'e8'
				to_index = 'g8'
			pairs.append([from_index, to_index])
			Chess.test_run_chess_notation([[from_index, to_index]])  # should work when its all there
			print("kingside Castle: ", from_index, to_index)

		elif to_index == "O-O-O":
			print('kqueencastle')
			if turn == 0:
				from_index = 'e1'
				to_index = 'c1'
			else:
				from_index = 'e8'
				to_index = 'c8'
			pairs.append([from_index, to_index])
			Chess.test_run_chess_notation([[from_index, to_index]])  # should work when its all there
			print("queenside Castle: ", from_index, to_index)
		else:
			print(to_index)
			print("WHAT HAPPEND>>>????")
			print("WHAT HAPPEND>>>????")
			print("WHAT HAPPEND>>>????")

		# to_indexes_cleaned.append(real_to_index)
		if turn == 0:
			turn = 1
		else:
			turn = 0
		turn_mult *= -1


	# print("to index: ", to_indexes_cleaned) #, len(to_indexes), len(to_indexes_cleaned))
	# print("pairs", pairs)
	return pairs


def index_to_chess_notation(index):
	letters = "ABCDEFGH"
	numbers = "87654321"
	return letters[index[1]]+numbers[index[0]]


def chess_notation_to_index(index):
	letters = "ABCDEFGH"
	index = index.upper()
	column_letter = index[0]
	row_number = index[1]
	row_index = 8 - int(row_number)
	column_index = letters.index(column_letter)
	return (row_index, column_index)


def convert(set):
	to_indexes = algebraic_notation_input(set)
	# print(to_indexes)
	move_set = generate_from_indexes(to_indexes)
	print(move_set)
	return move_set