from engine.utils import int_sq120_sq64

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

# init_board = "xxxxxxxxxx" \
#              "xxxxxxxxxx" \
#              "xooookooox" \
#              "xoooooooox" \
#              "xoRoooooox" \
#              "xooQooooox" \
#              "xoooooooox" \
#              "xoooooooox" \
#              "xoooooooox" \
#              "xooooKooox" \
#              "xxxxxxxxxx" \
#              "xxxxxxxxxx"
# init_board = list(init_board)

sq120 = int_sq120_sq64()

# Common squares
A1 = 91
B1 = 92
C1 = 93
D1 = 94
E1 = 95
F1 = 96
G1 = 97
H1 = 98

A8 = 21
B8 = 22
C8 = 23
D8 = 24
E8 = 25
F8 = 26
G8 = 27
H8 = 28

RANK7 = 39
RANK2 = 81

WHITE = 0
BLACK = 1
# State indexes
BOARD_INDEX = 0
TURN_INDEX = 1
EN_PAS_INDEX = 2
HALF_MOVE_INDEX = 3
FULL_MOVE_INDEX = 4
C_PERM_INDEX = 5
WK_SQ_INDEX = 6
BK_SQ_INDEX = 7
# Castle Perm indexes
WKC_INDEX = 0
WQC_INDEX = 1
BKC_INDEX = 2
BQC_INDEX = 3

# Castle States
CASTLE_NEW = '0'
CASTLE_OPEN = '1'
CASTLED = '2'
CASTLE_VOIDED = '3'

black_pieces = "pnbrq"
white_pieces = "PNBRQ"  # excludes king
all_white = "PKQRNBP"  # includes king
all_black = "pkqrnbp"
black_sliders = "qrb"
white_sliders = "QRB"
all_pieces = "KQRBNPkqrbnp"
ranks = "87654321"

# Directions
"""
0 1 .. . 9
10 11 .. 19

  NW  N  NE
W           E
  SW  S SE
"""
NORTH = -10
SOUTH = 10
WEST = -1
EAST = 1
NORTH_WEST = -11
NORTH_EAST = -9
SOUTH_WEST = 9
SOUTH_EAST = 11
KING_MOVES = {NORTH, SOUTH, EAST, WEST, NORTH_WEST, NORTH_EAST, SOUTH_WEST, SOUTH_EAST}
KNIGHT_MOVES = {21, 19, 12, 8, -21, -19, -8, -12}

# W_PAWN_MOVES = {-10}
# W_PAWN_ATTACKS = {-9, -11}
#
# B_PAWN_MOVES = {10}
# B_PAWN_ATTACKS = {9, 11}

Q_MOVES = {-11, -10, -9, -1, 1, 9, 10, 11}
R_MOVES = {-10, -1, 1, 10}
B_MOVES = {-11, -9, 9, 11}


PIECE_MOVES = {'Q': Q_MOVES, 'R': R_MOVES, 'B': B_MOVES, 'q': Q_MOVES, 'r': R_MOVES, 'b': B_MOVES}

OUT_OF_BOUND = 'x'
EMPTY = 'o'

WHITE_PIECES = {'P', 'N', 'B', 'R', 'Q', 'K'}
BLACK_PIECES = {'p', 'n', 'b', 'r', 'q', 'k'}

W_ROOK = 'R'
W_QUEEN = 'Q'
W_PAWN = 'P'


B_ROOK = 'r'
B_QUEEN = 'q'
B_PAWN = 'p'

init_state = [init_board, 0, -1, 0, 1, '0000', init_board.index('K'), init_board.index('k')]
