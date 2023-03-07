""" 
This is the main file for the game. It will be responsible for handling user input
and displaying the current game state 
"""

import checkers_engine as check_eng
from run import cls, new_line
import colorama
from colorama import Fore, Back, Style

def start_game():
    """ 
    Start the checkers game
    """
    game_state = check_eng.GameState()

    start_game_loop(game_state)

def start_game_loop(game_state):
    """ 
    Starts the basic game loop
    Asks player to pick a piece to move from movable pieces
    When player has picked a piece
    Asks player to pick a move from available moves
    Moves that piece the player picked
    Moves on the other players go
    """
    moves = 0
    while moves < 3:
        display_board(game_state)

        new_line()

        print(Fore.YELLOW + "Choose a piece from the movable pieces eg.(1(F1) or 2(F2))")

        movable_pieces = game_state.get_movable_pieces()
        
        pieces = ""
        for piece, i in zip(movable_pieces, range(1, len(movable_pieces) + 1)):
            text = f"{i}) {piece}\n"
            pieces += text
        piece_selected = input(pieces)
        new_line()
        while True:
            if validate_selected_piece(piece_selected, movable_pieces):
                break
            display_board(game_state)
            print(Fore.YELLOW + f"Please input (1 - {len(movable_pieces)})")
            piece_selected = input(pieces)
            new_line()

        moves += 1

def display_board(game_state):
    """ 
    Prints the board state to the console
    """
    cls()
    board_state = game_state.board
    board_rows = game_state.BOARD_ROWS
    board_cols = " ".join(game_state.BOARD_COLS)
    for x, r in zip(board_state, board_rows):
        row = " ".join(x)
        print(r + " " + row)
    
    print("  " + board_cols)

def validate_selected_piece(option, pieces):
    """ 
    Checks if the option selected is a valid option
    Returns number of selected option if valid
    Or returns false if not valid
    """
    try:
        option_selected = int(option)
        if option_selected >= 1 and option_selected <= len(pieces):
            return option_selected
        else:
            raise ValueError()
    except:
        return False



        
