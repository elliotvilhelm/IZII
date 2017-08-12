"""
TO DO:
Implement Castling done
Implement Finish CheckMate
Implement Pawn Promotion **
Implement Score **
Implement GUI done
Implement Input from Algebraic Notation done
Implement MinMax
Diagnol and sides overlap .. queen checks diagnol .. piece moves diagnol back
Revealing youself to a check is not in yet
"""
import chess_input_parser
import chessboard_test_functions
import move_sets
import GUI


chess_game = GUI.Chess_GUI(move_sets.Aronian)
# chess_game.run_steps()  # will run moves_set
chess_game.run_best_step()  # will play self chess
