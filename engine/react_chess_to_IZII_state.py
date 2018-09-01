from engine.utils import RF_sq64, sq64_to_sq120, print_board


def react_chess_board_to_IZII_board(board):
    if board is None:
        exit()

    izii_board = ["x"] * 120
    pieces = board.split(',')
    for i in range(len(izii_board)):
        if i >= 20 and i < 100:
            if i % 10 != 0 and i % 10 != 9:
                izii_board[i] = 'o'


    for p in pieces:
        # print("pp", p)
        piece_with_RF = p.split('@')
        # print("look: ", piece_with_RF)
        piece = piece_with_RF[0]
        RF = piece_with_RF[1]
        sq64 = RF_sq64(RF[0], RF[1])
        sq120 = sq64_to_sq120(sq64)
        izii_board[sq120] = piece
    return ''.join(izii_board)







