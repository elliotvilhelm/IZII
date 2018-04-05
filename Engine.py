# TO DO: Add full move half move and castle permission updates
import random
from gen_moves import *
from evaluate_state import evaluate_state
from constants import *
from utils import *


class IZII:
    def __init__(self):
        pass

    # Algorithm
    def best_move(self, state, depth=2):
        moves = self.get_all_moves_at_state(state)

        if state[1] == 0:
            current_score = -9999.0
        else:
            current_score = 9999.0
        move_n = -1
        turn = state[1]
        for i in range(len(moves)):
            new_state = self.move_at_state(state, moves[i])
            score = self.minimax(depth, new_state, -999, 999)
            if turn == 0:
                if score > current_score:
                    move_n = i
                    current_score = score
                elif score == current_score:
                    if random.randint(1, 5) == 3:
                        move_n = i
                        current_score = score
            elif turn == 1:
                if score < current_score:
                    move_n = i
                    current_score = score
                elif score == current_score:
                    if random.randint(1, 5) == 3:
                        move_n = i
                        current_score = score
        return moves[move_n]

    def minimax(self, depth, state, alpha, beta):
        player_turn = state[1]

        if depth == 0:
            b_val = evaluate_state(state)
            return b_val
        legal_moves = self.get_all_moves_at_state(state)

        if player_turn == 0:
            best_value = -999
            history = []
            if len(legal_moves) is 0:
                if self.white_in_check(state[0], state[6]):
                    print("real mate found for black")
                    self.print_board(state[0])
                    return -9999
                else:
                    print("real mate found for white")
                    self.print_board(state[0])

                    return 9999
            for i in range(len(legal_moves)):

                moveset = legal_moves[i]
                history.append(copy_state(state))
                state = self.run_move_at_state(state, moveset)
                value = self.minimax(depth - 1, state, alpha, beta)
                state = history.pop()
                best_value = max(best_value, value)
                alpha = max(alpha, best_value)
                if beta <= alpha:   # prune
                    break
            return best_value
        elif player_turn == 1:
            history = []
            best_value = 999
            if len(legal_moves) == 0:
                if self.black_in_check(state[0], state[7]):
                    print("real mate found for white")
                    return 9999
                else:
                    return -999
            for i in range(len(legal_moves)):
                moveset = legal_moves[i]
                history.append(state)
                state = self.run_move_at_state(state, moveset)
                value = self.minimax(depth - 1, state, alpha, beta)
                state = history.pop()
                best_value = min(best_value, value)
                beta = min(beta, best_value)
                if beta <= alpha:
                    break
            return best_value

    def run_move_at_state(self, state, move):
        return_state = self.move_at_state(state, move)
        return return_state

    def move_at_state(self, state, move):
        board = list(state[BOARD_INDEX])
        turn = state[TURN_INDEX]
        en_pass_sq = state[EN_PAS_INDEX]
        half_move = state[HALF_MOVE_INDEX]
        full_move = state[FULL_MOVE_INDEX]
        castle_perm = list(state[C_PERM_INDEX])
        white_king_sq = state[WK_SQ_INDEX]
        black_king_sq = state[BK_SQ_INDEX]
        from_tile_n = move[0]
        to_tile_n = move[1]

        ### En Passant case
        en_pass_sq = -1
        if board[from_tile_n] == 'P':
            if from_tile_n >= 81:
                if abs(to_tile_n - from_tile_n) == 20:
                    en_pass_sq = from_tile_n - 10
            # promote
            if board[to_tile_n - 10] == 'x':
                board[from_tile_n] = 'Q'
        elif board[from_tile_n] == 'p':
            if from_tile_n >= 38:
                if abs(to_tile_n - from_tile_n) == 20:
                    en_pass_sq = from_tile_n + 10
            # promote
            if board[to_tile_n + 10] == 'x':
                board[from_tile_n] = 'q'
        ### King move case

        elif board[from_tile_n] == 'K':

            white_king_sq = to_tile_n
            castle_perm[WKC_INDEX] = -1
            castle_perm[WQC_INDEX] = -1
        elif board[from_tile_n] == 'k':
            black_king_sq = to_tile_n
            castle_perm[BKC_INDEX] = -1
            castle_perm[BQC_INDEX] = -1
        elif board[from_tile_n] == 'R':
            if from_tile_n == H1:  # king side
                castle_perm[WKC_INDEX] = -1
            elif from_tile_n == A1:
                castle_perm[WQC_INDEX] = -1
        elif board[from_tile_n] == 'r':
            if from_tile_n == H8:  # king side
                castle_perm[BKC_INDEX] = -1
            elif from_tile_n == A8:
                castle_perm[BQC_INDEX] = -1

        # Check if attacking black king side rook
        if to_tile_n == A1:
            castle_perm[WQC_INDEX] = -1
        elif to_tile_n == H1:
            castle_perm[WKC_INDEX] = -1
        elif to_tile_n == A8:
            castle_perm[BQC_INDEX] = -1
        elif to_tile_n == H8:
            castle_perm[BKC_INDEX] = -1

        if from_tile_n == 95 and to_tile_n == 97 and board[from_tile_n] == 'K':  # and castle_perm[0] == 1:
            board[95] = "o"
            board[96] = 'R'
            board[97] = 'K'
            white_king_sq = 97
            board[98] = 'o'
            castle_perm[0] = 2
            castle_perm[1] = 2

        elif from_tile_n == 95 and to_tile_n == 93 and board[from_tile_n] == 'K':  # queen side castle
            board[91] = "o"
            board[92] = 'o'
            board[93] = 'K'
            white_king_sq = 93
            board[94] = 'R'
            board[95] = 'o'
            castle_perm[0] = 2
            castle_perm[1] = 2
        elif from_tile_n == 25 and to_tile_n == 27 and board[from_tile_n] == 'k':  # king side castle
            board[25] = "o"
            board[26] = 'r'
            board[27] = 'k'
            black_king_sq = 27
            board[28] = 'o'
            castle_perm[2] = 2
            castle_perm[3] = 2
        elif from_tile_n == 25 and to_tile_n == 23 and board[from_tile_n] == 'k':  # queen side castle
            board[21] = "o"
            board[22] = 'o'
            board[23] = 'k'
            black_king_sq = 23
            board[24] = 'r'
            board[25] = 'o'
            castle_perm[2] = 2
            castle_perm[3] = 2
        else:
            board[to_tile_n] = board[from_tile_n]
            board[from_tile_n] = "o"

        # Change Turns
        if turn == 0:
            turn = 1
        else:
            turn = 0
        # print(board[to_tile_n])
        return board, turn, en_pass_sq, half_move, full_move, castle_perm, white_king_sq, black_king_sq

    # Castle
    def check_wc_k(self, state):  # return true if kingside castle is availible
        # check if im in check
        # check if state perm is valid
        # check if the path is clear
        castle_perm = state[5][0]
        board = state[0]
        if castle_perm == -1:
            return False
        elif castle_perm == 2:
            return False
        elif self.white_in_check(state[0], state[6]):
            return False
        elif self.white_in_check(state[0], state[6] + 1):
            return False

        elif board[96] == 'o' and board[97] == 'o':  # and castle_perm != -1 and castle_perm != 2:
            return True
        else:
            return False

    def check_wc_q(self, state):  # return true if kingside castle is availible
        # check if im in check
        # check if state perm is valid
        # check if the path is clear
        board = state[0]
        castle_perm = state[5][1]
        if castle_perm == -1:
            return False
        elif castle_perm == 2:
            return False
        elif self.white_in_check(state[0], state[6]):
            return False
        elif self.white_in_check(state[0], state[6] - 1):
            return False

        elif board[92] == 'o' and board[93] == 'o' and board[94] == 'o':
            return True
        return False

    def check_bc_k(self, state):  # return true if kingside castle is availible
        # check if im in check
        # check if state perm is valid
        # check if the path is clear
        board = state[0]
        castle_perm = state[5][2]
        if castle_perm == -1:
            return False
        elif castle_perm == 2:
            return False
        elif self.black_in_check(state[0], state[7]):
            return False
        elif self.black_in_check(state[0], state[7] + 1):
            return False

        elif board[26] == 'o' and board[27] == 'o':
            return True
        return False

    def check_bc_q(self, state):  # return true if kingside castle is availible
        # check if im in check
        # check if state perm is valid
        # check if the path is clear
        board = state[0]
        castle_perm = state[5][3]

        if castle_perm == -1:
            return False
        elif castle_perm == 2:
            return False
        elif self.black_in_check(state[0], state[7]):
            return False
        elif self.black_in_check(state[0], state[7] - 1):
            return False

        elif board[22] == 'o' and board[23] == 'o' and board[24] == 'o':
            return True
        return False

    # Check
    def white_in_check(self, board, tile_n):
        # self.print_board(board)
        if self.check_black_sliders(board, tile_n) is True:
            return True
        if self.check_black_knights(board, tile_n) is True:
            return True
        if self.check_black_king(board, tile_n) is True:
            return True
        if self.check_black_pawns(board, tile_n) is True:
            return True
        else:
            return False

    def black_in_check(self, board, tile_n):
        if self.check_white_sliders(board, tile_n) is True:
            # print("fucking sliders")
            return True
        if self.check_white_knights(board, tile_n) is True:
            return True
        if self.check_white_king(board, tile_n) is True:
            return True
        if self.check_white_pawns(board, tile_n) is True:
            return True
        else:

            return False

    def check_black_pawns(self, board, tile_n):
        if board[tile_n - 11] == 'p':
            # print("warning black pawn")
            return True
        if board[tile_n - 9] == 'p':
            # print("warning black pawn")
            return True
        return False

    def check_white_pawns(self, board, tile_n):
        if board[tile_n + 11] == 'P':
            # print("warning white pawn")
            return True
        if board[tile_n + 9] == 'P':
            # print("warning white pawn")

            return True
        return False

    def check_black_king(self, board, tile_n):
        directions = [11, 10, 9, 1, -11, -10, -9, -1]
        for direction in directions:
            if board[tile_n + direction] == 'k':
                return True
        return False

    def check_white_king(self, board, tile_n):
        directions = [11, 10, 9, 1, -11, -10, -9, -1]
        for direction in directions:
            if board[tile_n + direction] == 'K':
                return True
        return False

    def check_black_knights(self, board, tile_n):
        directions = [21, 19, 12, 8, -21, -19, -8, -12]
        for direction in directions:
            # print(tile_n+direction)
            if board[tile_n + direction] == 'n':
                return True
        return False

    def check_white_knights(self, board, tile_n):
        directions = [21, 19, 12, 8, -21, -19, -8, -12]
        for direction in directions:
            if board[tile_n + direction] == 'N':
                return True
        return False

    def check_black_sliders(self, board, tile_n):
        slider_found = False
        # UP
        i = tile_n
        while board[i] != 'x':
            i -= 10
            if board[i] in "qr":
                slider_found = True
                return slider_found  # no need to check any more
            if board[i] in "pkbn":
                break
            if board[i] in all_white:
                break
        # DOWN
        i = tile_n
        while board[i] != 'x':
            i += 10
            if board[i] in "qr":
                slider_found = True
                return slider_found  # no need to check any more
            if board[i] in "pkbn":
                break
            if board[i] in all_white:
                break

        # LEFT
        i = tile_n
        while board[i] != 'x':
            i -= 1
            if board[i] in "qr":
                slider_found = True
                return slider_found  # no need to check any more
            if board[i] in "pkbn":
                break
            if board[i] in all_white:
                break

        # RIGHT
        i = tile_n
        while board[i] != 'x':
            i += 1
            if board[i] in "qr":
                slider_found = True
                return slider_found  # no need to check any more
            if board[i] in "pkbn":
                break
            if board[i] in all_white:
                break

        # UP LEFT
        i = tile_n
        while board[i] != 'x':
            i -= 11
            if board[i] in "qb":
                slider_found = True
                return slider_found  # no need to check any more
            if board[i] in "pkrn":
                break
            if board[i] in all_white:
                break

        # UP RIGHT
        i = tile_n
        while board[i] != 'x':
            i -= 9
            if board[i] in "qb":
                slider_found = True
                return slider_found  # no need to check any more
            if board[i] in "pkrn":
                break
            if board[i] in all_white:
                break
        # DOWN LEFT
        i = tile_n
        while board[i] != 'x':
            i += 9
            if board[i] in "qb":
                slider_found = True
                return slider_found  # no need to check any more
            if board[i] in "pkrn":
                break
            if board[i] in all_white:
                break
        # DOWN RIGHT
        i = tile_n
        while board[i] != 'x':
            i += 11
            if board[i] in "qb":
                slider_found = True
                return slider_found  # no need to check any more
            if board[i] in "pkrn":
                break
            if board[i] in all_white:
                break

        return slider_found

    def check_white_sliders(self, board, tile_n):
        slider_found = False
        # UP
        i = tile_n
        while board[i] != 'x':
            i -= 10
            if board[i] in "QR":
                slider_found = True
                return slider_found  # no need to check any more
            if board[i] in "PKBN":
                break
            if board[i] in all_black:
                break
        # DOWN
        i = tile_n
        while board[i] != 'x':
            i += 10
            if board[i] in "QR":
                # print("queen rook ")
                slider_found = True
                return slider_found  # no need to check any more
            if board[i] in "PKBN":
                break
            if board[i] in all_black:
                # print("blocked by black")
                break
        # LEFT
        i = tile_n
        while board[i] != 'x':
            i -= 1
            if board[i] in "QR":
                # print("slider at", self.sq64_to_RF(self.sq120_sq64(i)))
                slider_found = True
                return slider_found  # no need to check any more
            if board[i] in "PKBN":
                break
            if board[i] in all_black:
                break

        # RIGHT
        i = tile_n
        while board[i] != 'x':
            i += 1
            if board[i] in "QR":
                slider_found = True
                return slider_found  # no need to check any more
            if board[i] in "PKBN":
                break
            if board[i] in all_black:
                break

        # UP LEFT
        i = tile_n
        while board[i] != 'x':
            i -= 11
            if board[i] in "QB":
                slider_found = True
                return slider_found  # no need to check any more
            if board[i] in "pkbn":
                break
            if board[i] in all_black:
                break

        # UP RIGHT
        i = tile_n
        while board[i] != 'x':
            i -= 9
            if board[i] in "QB":
                slider_found = True
                return slider_found  # no need to check any more
            if board[i] in "pkbn":
                break
            if board[i] in all_black:
                break
        # DOWN LEFT
        i = tile_n
        while board[i] != 'x':
            i += 9
            if board[i] in "QB":
                slider_found = True
                return slider_found  # no need to check any more
            if board[i] in "pkbn":
                break
            if board[i] in all_black:
                break
        # DOWN RIGHT
        i = tile_n
        while board[i] != 'x':
            i += 11
            if board[i] in "QB":
                slider_found = True
                return slider_found  # no need to check any more
            if board[i] in "pkbn":
                break
            if board[i] in all_black:
                break
        return slider_found

    # Get Moves
    def get_all_moves_at_state(self, state):
        psuedo = self.get_pseudo_moves_beta(state)
        legal = self.get_legal_moves_beta(state, psuedo)
        return legal

    def get_piece_moves(self, state, tile_n):
        board = state[0]
        en_pass_sq = state[2]
        result = []
        # print(tile_n, board[tile_n])
        if board[tile_n] == "P":
            result = get_white_pawn_moves(board, en_pass_sq, tile_n)
        if board[tile_n] == "p":
            result = get_black_pawn_moves(board, en_pass_sq, tile_n)
        if board[tile_n] == "K":
            result = get_white_king_moves(board, tile_n)
        if board[tile_n] == "k":
            result = get_black_king_moves(board, tile_n)
        if board[tile_n] == "R":
            result = get_white_rook_moves(board, tile_n)
        if board[tile_n] == "r":
            result = get_black_rook_moves(board, tile_n)
        if board[tile_n] == "B":
            result = get_white_bishop_moves(board, tile_n)
        if board[tile_n] == "b":
            result = get_black_bishop_moves(board, tile_n)
        if board[tile_n] == "N":
            result = get_white_knight_moves(board, tile_n)
        if board[tile_n] == "n":
            result = get_black_knight_moves(board, tile_n)
        if board[tile_n] == "Q":
            result = get_white_queen_moves(board, tile_n)
        if board[tile_n] == "q":
            result = get_black_queen_moves(board, tile_n)
        return result

    def get_pseudo_moves_beta(self, state):
        moves = []
        b = state[0]
        turn = state[1]
        for i in range(len(b)):
            if turn == 0:
                if b[i] in all_white:
                    piece_moves = self.get_piece_moves(state, i)
                    for k in range(len(piece_moves)):
                        moves.append([i, piece_moves[k]])
                        # if len(piece_moves) > 0:
                        # 	moves.append([i, piece_moves])
            elif turn == 1:
                if b[i] in all_black:
                    piece_moves = self.get_piece_moves(state, i)
                    for k in range(len(piece_moves)):
                        moves.append([i, piece_moves[k]])
                        # if len(piece_moves) > 0:
                        # 	moves.append([i, piece_moves])

        if state[1] == 0:
            if self.check_wc_k(state):  # if im not in check and i have not fucked up my castle perm add the move
                state[5][0] = 1
                moves.append([95, 97])
            if self.check_wc_q(state):
                state[5][1] = 1
                moves.append([95, 93])
        if state[1] == 1:
            if self.check_bc_k(state):
                state[5][2] = 1
                moves.append([25, 27])
            if self.check_bc_q(state):
                state[5][3] = 1
                moves.append([25, 23])
        return moves

    def get_legal_moves_beta(self, state, pseudo_moves):
        # take move
        # check if in check
        # valid/invalid move
        # undo move
        legal_moves = []
        in_check = False
        # if state[1] == 0:
        # print("pseudo moves: ", pseudo_moves)
        for i in range(len(pseudo_moves)):
            move_set = pseudo_moves[i]
            from_sq = move_set[0]
            to_sq = move_set[1]
            # for j in range(len(to_sqs)):
            if pseudo_moves[i] == [95, 97]:
                # print("ITS wk CASTLE TIME")
                s2 = self.run_move_at_state(state, (95, 97))  # move king
                s2 = self.run_move_at_state(state, (98, 96))  # move queen
            elif pseudo_moves[i] == [95, 93]:
                # print("ITS wq CASTLE TIME")
                s2 = self.run_move_at_state(state, (95, 93))  # move king
                s2 = self.run_move_at_state(state, (91, 94))  # move queen
            elif pseudo_moves[i] == [25, 27]:
                # print("ITS bk CASTLE TIME")
                s2 = self.run_move_at_state(state, (25, 27))  # move king
                s2 = self.run_move_at_state(state, (28, 26))  # move queen
            elif pseudo_moves[i] == [25, 23]:
                # print("ITS bq CASTLE TIME")
                s2 = self.run_move_at_state(state, (25, 23))  # move king
                s2 = self.run_move_at_state(state, (21, 24))  # move queen
            else:
                s2 = self.run_move_at_state(state, (from_sq, to_sq))

            if s2[1] == 1:
                in_check = self.white_in_check(s2[0], s2[6])

            elif s2[1] == 0:
                in_check = self.black_in_check(s2[0], s2[7])
            if in_check is False:
                legal_moves.append(pseudo_moves[i])
        return legal_moves

    def print_full_board(self, board):
        for i in range(0, 120):
            if i % 10 == 0:
                row = board[i:i + 10]
                row_str = ' '.join(row)
                print(i, row_str)

    def print_board(self, board):
        # print("printing board: ", board)
        k = 0
        for i in range(20, 100):
            if i % 10 == 0:
                # print(board)
                # print(i)
                row = board[i + 1:i + 9]
                row_str = ' '.join(row)
                print(ranks[k], row_str)
                k += 1
        print('  A B C D E F G H')

    def get_board(self, board):
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

    def set_state_from_fen(self, fen):
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

                # board[counter - 8
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
        print(self.print_board(board))
        state.append(-1)
        state.append(0)
        state.append(0)
        state.append([0, 0, 0, 0])
        state.append(board.index('K'))
        state.append(board.index('k'))
        return state
