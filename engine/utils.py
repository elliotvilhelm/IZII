ranks = "87654321"


def swap_turn(turn):
    if turn is 0:
        return 1
    return 0

def update(board, pos, piece):
    return board[:pos] + piece + board[pos+1:]

def int_sq120_sq64():
    sq120 = []
    for i in range(120):
        sq120.append(-1)
    skip = 0
    for i in range(20, 100):
        if i % 10 != 0 and (i - 9) % 10 != 0:
            sq120[i] = i - 20 - skip
        if i % 10 == 0 and i != 20:
            skip += 2
    return sq120

def sq64_to_sq120(sq):
    extra = 0
    for i in range(1, sq):
        if i % 8 == 0:
            extra += 2
    return sq + 20 + extra

def copy_state(state):
    board = state[0]
    turn = state[1]
    en_pass_sq = state[2]
    half_move = state[3]
    full_move = state[4]
    castle_perm = state[5]
    white_king_sq = state[6]
    black_king_sq = state[7]
    return board, turn, en_pass_sq, half_move, full_move, castle_perm, white_king_sq, black_king_sq


def sq120_RF(sq120):
    sq64 = int_sq120_sq64()[sq120]
    return sq64_to_RF(sq64)


def RF_sq120(file, rank):
    return sq64_to_sq120(RF_sq64(file, rank))

# Helper Functions
def RF_sq64(file, rank):
    sq = 0
    file = file.upper()
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
    sq = abs(int(rank) - 9) * 8 - 8 + file
    return sq

def sq64_to_RF(sq64):

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
    return file+rank


def print_full_board(board):
    for i in range(0, 120):
        if i % 10 == 0:
            row = board[i:i + 10]
            row_str = ' '.join(row)
            print(i, row_str)



def print_board(board):
    k = 0
    for i in range(20, 100):
        if i % 10 == 0:
            row = board[i + 1:i + 9]
            row_str = ' '.join(row)
            print(ranks[k], row_str)
            k += 1
    print('  A B C D E F G H')

def set_state_from_fen(fen):
    ranks = fen.split(" ")[0].split("/")
    print("fen:  ", fen, "ranks:  ", ranks)
    board = ""
    board += 'x' * 21
    print(len(board))
    counter = 0
    for rank in ranks:
        counter += 1
        for ch in rank:
            if ch in "12345678":
                board += 'o' * int(ch)
            else:
                board += ch
        if counter % 8:
            board += 'x' * 2

    board += 'x' * 20
    state = [board]
    try:
        index = fen.index("w")
        state.append(0)
    except:
        index = fen.index("b")
        state.append(1)
    print("found turn: ", fen[index])
    print(board)
    print(print_board(board))
    state.append(-1)
    state.append(0)
    state.append(0)
    state.append('0000')  # should fix this to account for castle state from FEN
    state.append(board.index('K'))
    state.append(board.index('k'))
    return state

def get_board(board):
    # print("printing board: ", board)
    board_str = "\n"
    k = 0
    for i in range(20, 100):
        if i % 10 == 0:
            # print(board)
            # print(i)
            row = board[i + 1:i + 9]
            row_str = ' '.join(row)
            board_str += ranks[k] + row_str + "\n"
            # print(self.ranks[k], row_str)
            k += 1
    board_str += ' A B C D E F G H\n'
    return board_str

def in_range(tile_n):
    from engine.constants import A8, H1
    if tile_n < A8 or tile_n > H1:
        return False
    return True