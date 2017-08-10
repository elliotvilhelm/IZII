"""
TO DO:
Implement Castling done
Implement Finish CheckMate
Implement Pawn Promotion **
Implement Score **
Implement GUI done
Implement Input from Algebraic Notation done
Implement MinMax
"""
import BoardRepresentation as chess
import chessboard_test_functions

# Chess = chess.Game()
# test_king(Chess)
# Chess.run()
# test_bishop(Chess)
# test_en_passant(Chess)
# Kasparov_vs_Topalov_1999_immortal(Chess)
# Morphy_vs_Anderseen_1858(Chess)
# test_king_side_castle(Chess)
# test_queen_side_castle(Chess)
# scholars_mate(Chess)
# chess.run_GUI()

# to_indexes = algebraic_notation_input(Nezhmet_Kismet)
# print(to_indexes)
# move_set = None
# Chess = chess.Game()
# Chess.random_step()
# # move_set = generate_from_indexes(to_indexes)
#
# # gui = chess.Chess_GUI()
# # gui
# print(move_set)
# chess_with_gui = chess.Chess_GUI(move_set)
# # chess_with_gui.run_logic()
# chess_with_gui.run_random_step()


# black_check = [['e2', 'e3'], ['f7', 'f6'], ['d1', 'h5'], ['g7', 'g6']]
black_check = [['e2', 'e3'], ['f7', 'f6'],  ['d1', 'h5'], ['g7', 'g6'], ['a2','a3'], ['a7', 'a5']]
black_check2 = [['e2', 'e3'], ['f7', 'f6'], ['b2', 'b4'], ['d7', 'd6'],  ['d1', 'h5'], ['g7', 'g6'], ['a2','a3'], ['a7', 'a5']]
chess_game = chess.Chess_GUI(black_check)
# chess_game.run_steps()

chess_game.run_random_step()
