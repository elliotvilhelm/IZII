from utils import RF_sq64, sq64_to_sq120, print_board


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

board = 'R@a1,P@a2,p@a7,r@a8,N@b1,P@b2,p@b7,n@b8,B@c1,P@c2,p@c7,b@c8,Q@d1,P@d2,p@d7,q@d8,K@e1,P@e2,p@e7,k@e8,B@f1,P@f2,' \
        'p@f7,b@f8,N@g1,P@g2,p@g7,n@g8,R@h1,P@h2,p@h7,r@h8'

izii_board = ["x"] * 120
pieces = board.split(',')

for p in pieces:
    piece_with_RF = p.split('@')
    piece = piece_with_RF[0]
    RF = piece_with_RF[1]
    sq64 = RF_sq64(RF[0], RF[1])
    sq120 = sq64_to_sq120(sq64)
    izii_board[sq120] = piece


print_board(izii_board)







