import Engine
import re
import logging
from utils import *
from constants import sq120
engine = Engine.IZII()
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

init_board = list(init_board)
# board, turn, en pas, healf move, full move, castle perm, white king sq, black king sq
init_state = [init_board, 0, -1, 0, 1, [0, 0, 0, 0], init_board.index('K'), init_board.index('k')]

WHITE = 0
BLACK = 1

print("helo me")
def reply(command):
    logging.debug('<<' + command)
    sys.stdout.write(command + '\n')
    sys.stdout.flush()


def run_xboard():
    state = init_state
    force_mode = False
    history = []
    if sys.stdout.isatty():
        reply("-> Welcome to IZZI!, type 'new' to start a new game")

    # Begin Input loop
    while True:
        try:
            line = input()
        except IOError:
            print('-> got IOError')
            continue
        # Prep and log input
        cmd = line.strip()  # remove whitespace
        logging.debug(">> " + cmd)
        if cmd == 'xboard':
            reply("tellics say     IZZI")
            reply("tellics say     (c) Elliot Vilhelm Pourmand, All rights reserved.")
        elif cmd == 'new':
            state = init_state
            history = []
            force_mode = False
        elif cmd == 'protover 2':
            reply('feature myname="Elliots\'s IZII"')
            reply('feature ping=1')
            reply('feature san=0')
            reply('feature sigint=0')
            reply('feature sigterm=0')
            reply('feature setboard=1')
            reply('feature debug=1')
            reply('feature time=0')
            reply('feature done=1')
        elif cmd == 'force':
            force_mode = True
        elif cmd == 'go':  # start playing
            force_mode = False
            print("turn: ", state[1])
            logging.debug("turn")
            logging.debug(state[1])
            move = engine.best_move(state, 3)
            logging.debug(engine.get_all_moves_at_state(state))
            logging.debug(state[5])
            logging.debug(state[2])

            print(move)
            fromsq = sq120[move[0]]
            tosq = sq120[move[1]]
            fromsq = sq64_to_RF(fromsq)
            tosq = sq64_to_RF(tosq)
            move_txt = fromsq[0] + fromsq[1] + tosq[0] + tosq[1]
            state = engine.run_move_at_state(state, move)
            reply("# moving in go")
            reply("move " + move_txt.lower())
        elif cmd.startswith('ping'):
            n = cmd.split(' ')[-1]
            reply('pong ' + n)
        elif cmd == 'white':
            # my_team = WHITE
            reply('#Changed to  white')
        elif cmd == 'black':
            # my_team = BLACK
            reply('#Changed to black')
        elif cmd == 'quit':
            return
        elif cmd.startswith('set board'):
            fen = cmd[9:].strip()
            state = engine.set_state_from_fen(fen)
            print("turn: ", state[1])
        else:
            if re.match('^[a-h][1-8][a-h][1-8].?$', cmd):
                # Update my board
                fromsq = cmd[0:2]
                tosq = cmd[2:4]
                fromsq120 = sq64_to_sq120(RF_sq64(fromsq[0], fromsq[1]))
                tosq120 = sq64_to_sq120(RF_sq64(tosq[0], tosq[1]))
                history.append(state)
                state = engine.run_move_at_state(state, [fromsq120, tosq120])
                logging.debug("state after re.match")
                logging.debug(engine.get_board(state[0]))
                if not force_mode:
                    logging.debug(engine.get_all_moves_at_state(state))
                    logging.debug(state[5])
                    logging.debug(state[2])
                    move = engine.best_move(state, 3)
                    fromsq = sq120[move[0]]
                    tosq = sq120[move[1]]
                    fromsq = sq64_to_RF(fromsq)
                    tosq = sq64_to_RF(tosq)
                    move_txt = fromsq[0] + fromsq[1] + tosq[0] + tosq[1]
                    state = engine.run_move_at_state(state, move)
                    logging.debug(engine.get_board(state[0]))
                    reply("# state after moving in not force")
                    reply("move " + move_txt.lower())
            else:
                reply("#non registered command : '" + cmd + "'")


if __name__ == '__main__':
    import sys
    import random
    import string

    logging.basicConfig(filename='test.log'.join(random.choices(string.ascii_uppercase + string.digits, k=3)), level=logging.DEBUG)
    run_xboard()
