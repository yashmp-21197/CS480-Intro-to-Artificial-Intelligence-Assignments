from games import *
import utils


def check_inputted_row(row):
    if len(row) != 3:
        raise Exception('inputted length must be 3.')
    else:
        for ch in row:
            if ch not in ['X', 'O', '-']:
                raise Exception('inputted characters must be any of {X, O, -}')


if __name__ == '__main__':

    print('=' * 50)
    print('=' * 50)
    print('TIK-TAK-TOE')
    print('=' * 50)
    print('=' * 50)

    first_row = input('input first row of TIK-TAK-TOE (e.g. XO- without space) ==> ')
    first_row = first_row.upper()
    first_row = [ch for ch in first_row]
    check_inputted_row(first_row)
    second_row = input('input second row of TIK-TAK-TOE (e.g. XO- without space) ==> ')
    second_row = second_row.upper()
    second_row = [ch for ch in second_row]
    check_inputted_row(second_row)
    third_row = input('input third row of TIK-TAK-TOE (e.g. XO- without space) ==> ')
    third_row = third_row.upper()
    third_row = [ch for ch in third_row]
    check_inputted_row(third_row)
    tik_tak_toe_game_board = [first_row, second_row, third_row]

    free_count = first_row.count('-') + second_row.count('-') + third_row.count('-')
    current_player = 'O' if free_count % 2 == 0 else 'X'

    # generating current_state
    moves = []
    board = {}

    for i in range(0, len(tik_tak_toe_game_board)):
        for j in range(0, len(tik_tak_toe_game_board[i])):
            if tik_tak_toe_game_board[i][j] != '-':
                board[(1 + i, 1 + j)] = tik_tak_toe_game_board[i][j]
            else:
                moves.append((1 + i, 1 + j))

    current_state = GameState(to_move=current_player, utility=0, board=board, moves=moves)

    # Checking for initial terminal state
    row1 = (board.get((1, 1)) == board.get((1, 2)) == board.get((1, 3)) is not None != '-')
    row2 = (board.get((2, 1)) == board.get((2, 2)) == board.get((2, 3)) is not None != '-')
    row3 = (board.get((3, 1)) == board.get((3, 2)) == board.get((3, 3)) is not None != '-')
    column1 = (board.get((1, 1)) == board.get((2, 1)) == board.get((3, 1)) is not None != '-')
    column2 = (board.get((1, 2)) == board.get((2, 2)) == board.get((3, 2)) is not None != '-')
    column3 = (board.get((1, 3)) == board.get((2, 3)) == board.get((3, 3)) is not None != '-')
    diagonal1 = (board.get((1, 1)) == board.get((2, 2)) == board.get((3, 3)) is not None != '-')
    diagonal2 = (board.get((1, 3)) == board.get((2, 2)) == board.get((3, 1)) is not None != '-')
    all_filled = (free_count == 0)

    winner = None
    if row1:
        winner = board[(1, 1)]
    elif row2:
        winner = board[(2, 1)]
    elif row3:
        winner = board[(3, 1)]
    elif column1:
        winner = board[(1, 1)]
    elif column2:
        winner = board[(1, 2)]
    elif column3:
        winner = board[(1, 3)]
    elif diagonal1:
        winner = board[(1, 1)]
    elif diagonal2:
        winner = board[(1, 3)]

    terminal_state = (row1 or row2 or row3 or column1 or column2 or column3 or diagonal1 or diagonal2 or all_filled)
    terminal_state_utility = None

    if terminal_state:
        if winner == 'X':
            terminal_state_utility = 1
        elif winner == 'O':
            terminal_state_utility = -1
        else:
            terminal_state_utility = 0

    ttt_game = TicTacToe()
    # Setting initial state
    ttt_game.set_state(current_state)

    print("Whose turn is it now?")
    if winner is None:
        print(f'{current_player}')
    else:
        print(f'games is finished and won by {winner}. so, there are no more turns.')
    print()

    print("What is the value of the current state from the perspective of X?")
    if terminal_state:
        print(terminal_state_utility)
    else:
        print(utils.x_utility)
    print()

    print("How many states did the minimax algorithm evaluate?")
    if terminal_state:
        print(1)
    else:
        minimax_decision(current_state, ttt_game)
        print(utils.num_states_evaluated_minimax)
        utils.num_states_evaluated_minimax = 1
    print()

    print("How many states did the alpha-beta pruning algorithm evaluate?")
    if terminal_state:
        print(1)
    else:
        alphabeta_search(current_state, ttt_game)
        print(utils.num_states_evaluated_alphabeta)
        utils.num_states_evaluated_alphabeta = 1
    print()

    print(
        "Assuming both X and O play optimally, does X have a guaranteed win? Is it a tie? Is it a guaranteed loss for "
        "X?")
    if terminal_state:
        if winner == 'X':
            x_result = "X will win."
        elif winner == 'O':
            x_result = "X will lose."
        else:
            x_result = "It is a tie."
    elif utils.x_utility == 1:
        x_result = "X will win."
    elif utils.x_utility == -1:
        x_result = "X will lose."
    else:
        x_result = "It is a tie."
    print(x_result)
    print()

    print("Assuming both X and O would play optimally, how would they play till the game ends?")
    if terminal_state:
        ttt_game.display(ttt_game.initial)
    else:
        ttt_game.play_game(alphabeta_player, alphabeta_player)
