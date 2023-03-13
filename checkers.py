""" 
This is the main file for the game. It will be responsible for handling user input
and displaying the current game state 
"""

import checkers_engine as check_eng
from run import cls, new_line
import colorama
from colorama import Fore, Back, Style
import time
import smart_move_finder as smf

def start_game():
    """ 
    Start the checkers game
    """
    game_state = check_eng.GameState()

    player_one = 0 # If a human is playing, this will be 0, if an AI is playing this will be 1, 2, or 3

    player_two = 1 # If a human is playing, this will be 0, if an AI is playing this will be 1, 2, or 3

    start_game_loop(game_state, player_one, player_two)

def start_game_loop(game_state, p1, p2):
    """ 
    Starts the basic game loop
    Asks player to pick a piece to move from movable pieces
    When player has picked a piece
    Asks player to pick a move from available moves
    Moves that piece the player picked
    Moves on to the other players go
    """
    moves = 0
    game_over = False
    while not game_over:
        color = game_state.color_go
        human_turn = (color == "black" and not p1) or (color == "white" and not p2)

        movable_pieces = game_state.get_movable_pieces(color)
        if not movable_pieces:
            game_over = True
            print("Total Moves: " + str(moves))
        else:
            selecting_move = True 
            while selecting_move and human_turn:
                selected_piece = select_piece(game_state, movable_pieces, color)
                
                selected_move = select_move(game_state, selected_piece, color)

                if selected_move != "return":
                    game_state.move_piece(selected_piece, selected_move[0], selected_move[1], color)
                    selecting_move = False

            if not human_turn:
                available_moves = game_state.find_all_available_moves(color)

                ai_move = smf.find_best_move(game_state, available_moves)

                game_state.move_piece(ai_move[0], ai_move[1], ai_move[2], ai_move[3])
            
            display_board(game_state)
            
            #time.sleep(2)

            game_state.change_color_go()
            
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

def select_piece(game_state, movable_pieces, color):
    """
    Asks player to pick a piece to move from movable pieces
    Validates the option selected
    """
    display_board(game_state)

    new_line()

    print(Fore.YELLOW + "Choose a piece from the movable pieces eg.(1(F1) or 2(F2)...)")

    options = ""
    for piece, i in zip(movable_pieces, range(1, len(movable_pieces) + 1)):
        text = f"{i}) {piece}\n"
        options += text
    option_selected = input(options)
    new_line()
    while True:
        if validate_selected_option(option_selected, "movable_pieces", movable_pieces):
            return movable_pieces[validate_selected_option(option_selected, "movable_pieces", movable_pieces) - 1]
            break
        display_board(game_state)
        new_line() 
        print(Fore.YELLOW + f"Please input (1 - {len(movable_pieces)})")
        option_selected = input(options)
          

def validate_selected_option(option, type, list):
    """ 
    Checks if the option selected is a valid option
    Returns number of selected option if valid
    Or returns false if not valid
    """
    try:
        if option == "r" and type == "available_moves":
            return "return"
        option_selected = int(option)
        if option_selected >= 1 and option_selected <= len(list):
            return option_selected
        else:
            raise ValueError()
    except:
        return False

def select_move(game_state, piece, color):
    """
    Asks player to pick a board position for the selected piece to move to from available moves
    Validates the option selected
    """
    display_board(game_state)

    new_line()

    print(Fore.YELLOW + "Choose a position to move to eg.(1(F1) or 2(F2)...)")
    print(Fore.YELLOW + "(Enter r to return to selecting a piece)")

    available_moves = game_state.find_available_moves(piece, color)

    formatted_moves = format_available_moves(available_moves)

    options = ""
    for move, i in zip(formatted_moves, range(1, len(formatted_moves) + 1)):
        text = f"{i}) {move}\n"
        options += text
    option_selected = input(options)
    new_line()
    while True:
        if validate_selected_option(option_selected, "available_moves", available_moves) == "return":
            return "return"
            break
        elif validate_selected_option(option_selected, "available_moves", available_moves):
            return [available_moves[validate_selected_option(option_selected, "available_moves", available_moves) - 1], validate_selected_option(option_selected, "available_moves", available_moves)]
            break
        display_board(game_state)
        new_line()
        print(Fore.YELLOW + f"Please input (1 - {len(available_moves)})")
        option_selected = input(options)

def format_available_moves(moves):
    """ 
    Formats the available moves correctly to display to user
    """
    formatted_moves = []
    for move in moves:
        formatted_move = ""
        if move[1] == "move":
           formatted_move += "Move to: " + move[0]
        elif move[1] == "jump":
            formatted_move += "Jump to: " + move[0]
        formatted_moves.append(formatted_move)
    
    return formatted_moves
                    
def ai_select_piece(game_state, movable_pieces, color):
    """
    AI selects a piece to move from movable pieces 
    """
    ai_piece = smf.find_random_piece(movable_pieces)
    return ai_piece

def ai_select_move(game_state, piece, color):
    """ 
    AI selects a move from available moves
    """
    available_moves = game_state.find_available_moves(piece, color)
    ai_move = smf.find_random_move(available_moves)
    move = [ai_move, available_moves.index(ai_move) + 1]
    return move




        
