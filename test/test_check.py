from engine.check_detection import check_white_knights, check_white_sliders, check_white_pawns


def test_black_not_in_check_knight():
    board = "x"*20 + "xrnbqkbnrx" + "xppppppppx" + "xoooooooox" * 4 + "xPPPPPPPPx" + "xRNBQKBNRx" + "x"*20
    king_ind = board.find('k')
    assert check_white_knights(board, king_ind) is False


def test_black_not_in_check_sliders():
    board = "x"*20 + "xrnbqkbnrx" + "xppppppppx" + "xoooooooox" * 4 + "xPPPPPPPPx" + "xRNBQKBNRx" + "x"*20
    king_ind = board.find('k')
    assert check_white_sliders(board, king_ind) is False


def test_black_not_in_check_pawns():
    board = "x"*20 + "xrnbqkbnrx" + "xppppppppx" + "xoooooooox" * 4 + "xPPPPPPPPx" + "xRNBQKBNRx" + "x"*20
    king_ind = board.find('k')
    assert check_white_pawns(board, king_ind) is False
