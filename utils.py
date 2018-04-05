

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



# def sq120_sq64(sq):
#     return sq120[sq]


def sq64_to_sq120(sq):
    extra = 0
    for i in range(1, sq):
        if i % 8 == 0:
            extra += 2
    return sq + 20 + extra


# def print_move(move):
#     print(sq64_to_RF(sq120[(move[0])), sq64_to_RF(sq120_sq64(move[1])))


def copy_state(state):
    board = list(state[0])
    turn = state[1]
    en_pass_sq = state[2]
    half_move = state[3]
    full_move = state[4]
    castle_perm = list(state[5])
    white_king_sq = state[6]
    black_king_sq = state[7]
    return board, turn, en_pass_sq, half_move, full_move, castle_perm, white_king_sq, black_king_sq


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
    # print("error unkown file")
    print("rank", rank)
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
    return file, rank