""" 
This file is responsible for storing all the information about the current state of the chess game.
It will also be responsible for determining the valid moves at the current state.
"""

class GameState():
    """ 
    Creates an instance of the game state
    """
    def __init__(self):
        # board is an 8x8 2d list, each element of the list has 1 character.
        # Characters w and b represtent pieces white or black
        # Character x represents an empty space that cannot be moved into
        # Character _ represents an empty space that can be moved into
        self.board = [
            ["x", "_", "x", "_", "x", "_", "x", "_"],
            ["_", "x", "_", "x", "_", "x", "_", "x"],
            ["x", "W", "x", "_", "x", "_", "x", "_"],
            ["_", "x", "_", "x", "B", "x", "_", "x"],
            ["x", "_", "x", "_", "x", "_", "x", "_"],
            ["_", "x", "_", "x", "_", "x", "_", "x"],
            ["x", "_", "x", "_", "x", "_", "x", "_"],
            ["_", "x", "_", "x", "_", "x", "_", "x"]
        ]

        self.BOARD_ROWS = ["A", "B", "C", "D", "E", "F", "G", "H"]
        self.BOARD_COLS = ["1", "2", "3", "4", "5", "6", "7", "8"]

        self.color_go = "black"

        self.available_jumps_log = []
        self.jumped_pieces_log = []
        self.jump_count = 0
        self.available_jumps = []
    def get_movable_pieces(self, color):
        """
        Finds out the movable pieces on the board
        Returns pieces in a list 
        """
        movable_pieces = self.get_all_players_pieces(color)
        movable_pieces = self.eliminate_immovable_pieces(movable_pieces, color)
        
        return movable_pieces


    def get_all_players_pieces(self, color):
        """
        Finds all the players pieces
        """
        pieces = []
        i = 0
        j = 0
        for x in self.board:
            for y in x:
                if (y == "b" or y == "B") and color == "black":
                    piece = self.format_piece(i, j)
                    pieces.append(piece)
                elif (y == "w" or y == "W") and color == "white":
                    piece = self.format_piece(i, j)
                    pieces.append(piece)

                j += 1

            i += 1
            j = 0

        return pieces

    def eliminate_immovable_pieces(self, pieces, color):
        """ 
        Find all the movable and immovable pieces by finding available moves
        Take out the immovable and return a list
        """
        movable_pieces = []

        for piece in pieces:
            if self.find_available_moves(piece, color):
                movable_pieces.append(piece)

        return movable_pieces

    def find_available_moves(self, piece, color):
        """ 
        Finds a pieces available moves
        Checks if move is blocked or empty
        Formats the move into piece
        Finds a pieces available jumps
        Checks if jump is valid
        Formats jumps into piece
        Adds jumps to moves
        Returns a list of positions where the piece can move
        Returns an empty string if no moves available
        """
        piece_index = self.get_index_of_piece(piece)
        available_moves = self.format_available_moves(self.get_available_moves(piece_index, color))
        self.get_available_jumps(piece_index, color)
        available_jumps = self.format_available_jumps()
        for jump, i in zip(available_jumps, range(len(available_jumps))):
            available_moves.insert(i, jump)
        
        # Set variables to default
        self.available_jumps = []
      
        self.available_jumps_log = []
       
        return available_moves
               
    def format_piece(self, r, c):
        """ 
        Formats a piece in the form A1
        Where A represents the row and 1 represents the column
        Ranges from (A to H) and (1 - 8)
        """
        row = chr(65 + r)
        col = str(c + 1)
        return f"{row + col}"

    def get_index_of_piece(self, piece):
        """ 
        Finds the index of the piece in the board
        Returns it as an array where row is first and col is second
        """
        split_row_col = list(piece)
        row = self.BOARD_ROWS.index(split_row_col[0])
        col = self.BOARD_COLS.index(split_row_col[1])
        return [row, col]
    
    def get_available_moves(self, piece_index, color):
        """ 
        Checks if the piece is on the edge
        Checks the pieces diaganols if it is empty
        Returns the diaganols indexs in a list if it is empty
        """
        if self.check_if_piece_on_edge_of_board(piece_index) == "Left":
            diaganol_right_normal = self.get_diaganol(piece_index, "Right", color)
            if self.check_if_piece_is_kinged(piece_index, color):
                diaganol_right_king = self.get_diaganol(piece_index, "Right-King", color)
                if color == "white":
                    return ["blocked", self.check_if_diaganol_empty(diaganol_right_king), "blocked", self.check_if_diaganol_empty(diaganol_right_normal)]
                else:
                    return ["blocked", self.check_if_diaganol_empty(diaganol_right_normal), "blocked", self.check_if_diaganol_empty(diaganol_right_king)]
            else:
                return ["blocked", self.check_if_diaganol_empty(diaganol_right_normal)]
        elif self.check_if_piece_on_edge_of_board(piece_index) == "Right":
            diaganol_left_normal = self.get_diaganol(piece_index, "Left", color)
            if self.check_if_piece_is_kinged(piece_index, color):
                diaganol_left_king = self.get_diaganol(piece_index, "Left-King", color)
                if color == "white":
                    return [self.check_if_diaganol_empty(diaganol_left_king), "blocked", self.check_if_diaganol_empty(diaganol_left_normal), "blocked"]
                else:
                    return ["blocked", self.check_if_diaganol_empty(diaganol_left_normal), "blocked", self.check_if_diaganol_empty(diaganol_left_king)]
            else:
                return [self.check_if_diaganol_empty(diaganol_left_normal), "blocked"]
        else:
            diaganol_left_normal = self.get_diaganol(piece_index, "Left", color)
            diaganol_right_normal = self.get_diaganol(piece_index, "Right", color)
            if self.check_if_piece_is_kinged(piece_index, color):
                diaganol_left_king = self.get_diaganol(piece_index, "Left-King", color)
                diaganol_right_king = self.get_diaganol(piece_index, "Right-King", color)
                if color == "white":
                    return [self.check_if_diaganol_empty(diaganol_left_king), self.check_if_diaganol_empty(diaganol_right_king), self.check_if_diaganol_empty(diaganol_left_normal), self.check_if_diaganol_empty(diaganol_right_normal)]
                else: 
                    return [self.check_if_diaganol_empty(diaganol_left_normal), self.check_if_diaganol_empty(diaganol_right_normal), self.check_if_diaganol_empty(diaganol_left_king), self.check_if_diaganol_empty(diaganol_right_king)]
            else:
                return [self.check_if_diaganol_empty(diaganol_left_normal), self.check_if_diaganol_empty(diaganol_right_normal)]

    def check_if_piece_on_edge_of_board(self, piece_index):
        """ 
        Finds out if the piece is on the edge of the board
        If it is return Left or Right, if not return False
        """
        if piece_index[1] == 0:
            return "Left"
        elif piece_index[1] == 7:
            return "Right"
        else:
            return False

    def check_if_piece_on_kings_edge(self, piece_index):
        """ 
        Finds out if the piece is on the top or bottom edge of the board
        If it is return top or bottom otherwise return false
        """
        if piece_index[0] == 0:
            return "Top"
        elif piece_index[0] == 7:
            return "Bottom"
        else: 
            return False

    def get_diaganol(self, piece_index, diaganol, color):
        """ 
        Gets the index of the diaganol position either to the right or left
        Returns index in a list where row is first col is second
        """
        if color == "black":
            if diaganol == "Right-King" or diaganol == "Left-King":
                row = piece_index[0] + 1
            else:
                row = piece_index[0] - 1
        elif color == "white":
            if diaganol == "Right-King" or diaganol == "Left-King":
               row = piece_index[0] - 1
            else: 
                row = piece_index[0] + 1

        if diaganol == "Left" or diaganol == "Left-King":
            col = piece_index[1] - 1
        elif diaganol == "Right" or diaganol == "Right-King":
            col = piece_index[1] + 1
        return [row, col]

    def check_if_diaganol_empty(self, diaganol):
        """ 
        Checks if the diaganol is an empty space on the board
        Returns the diaganol if it space is empty
        or returns blocked if space is taken
        """
        if self.board[diaganol[0]][diaganol[1]] == "_":
            return diaganol
        else: 
            return "blocked"

    def format_available_moves(self, moves):
        """ 
        Formats the available moves
        Returns a list where blocked is replaced by empty
        And eligable moves are formatted correctly
        """
        available_moves = []
        for move in moves:
            if move != "blocked":
                m = []
                available_move = self.format_piece(move[0], move[1])
                m.append(available_move)
                m.append("move")
                available_moves.append(m)
        return available_moves

    def get_available_jumps(self, piece_index, color):
        """
        Checks if the piece is on the edge
        Checks the pieces diaganols if it is has a piece of the opposite color
        Checks if you can jump that piece
        Returns the positions indexs if it can jump
        """
        if not self.check_if_piece_on_kings_edge(piece_index):
            if self.check_if_piece_on_edge_of_board(piece_index) == "Left":
                diaganol_right = self.get_diaganol(piece_index, "Right", color)
                self.check_jump(diaganol_right, "Right", color) 
            elif self.check_if_piece_on_edge_of_board(piece_index) == "Right":
                diaganol_left = self.get_diaganol(piece_index, "Left", color)
                self.check_jump(diaganol_left, "Left", color)
            else:
                diaganol_left = self.get_diaganol(piece_index, "Left", color)
                if self.check_if_piece_on_edge_of_board(diaganol_left) != "Left":
                    self.check_jump(diaganol_left, "Left", color)
                diaganol_right = self.get_diaganol(piece_index, "Right", color)
                if self.check_if_piece_on_edge_of_board(diaganol_right) != "Right":
                    self.check_jump(diaganol_right, "Right", color)

        return self.available_jumps

    def check_jump(self, diaganol, left_or_right, color):
        """
        Checks if the diaganol contains the opposite color piece
        If it does it checks the next right diaganol to see if it is empty
        If it is empty, returns the position as it can jump
        Also calls the get available jumps again to see if it can double jump
        If there is a piece in the way it returns blocked 
        """
        
        if self.check_if_diaganol_contains_opposite_color_piece(diaganol, color):
            if not self.check_if_piece_on_edge_of_board(diaganol) and not self.check_if_piece_on_kings_edge(diaganol):     
                new_diaganol = self.get_diaganol(diaganol, left_or_right, color)
                if self.check_if_diaganol_empty(new_diaganol) != "blocked":
                    self.available_jumps.append(new_diaganol)
                    self.jump_count += 1
                    self.jumped_pieces_log.append(self.format_piece(diaganol[0], diaganol[1]))
                    self.available_jumps_log.append(self.jumped_pieces_log[:])
                    self.get_available_jumps(new_diaganol, color)
                    self.delete_last_log()
                    return "success"
                else:
                    return "blocked"
            else:
                return "blocked"
        else: 
            return "blocked"

    def check_if_diaganol_contains_opposite_color_piece(self, diaganol, color):
        """ 
        Checks if the diaganol is an opposite color piece on the board
        Returns True if there is an opposite color piece
        or returns False if space is empty or filled with same color piece
        """
        if self.board[diaganol[0]][diaganol[1]] == "w" and color == "black":
            return True
        elif self.board[diaganol[0]][diaganol[1]] == "b" and color == "white":
            return True
        else: 
            return False

    def format_available_jumps(self):
        """
        Formats the available moves
        Returns a list where blocked is replaced by empty
        And eligable jumps are formatted correctly
        """
        available_jumps = []
        
        for jump in self.available_jumps:
            j = []
            available_jump = self.format_piece(jump[0], jump[1])
            j.append(available_jump)
            j.append("jump")
            available_jumps_log = self.available_jumps_log
            j.append(available_jumps_log)
            available_jumps.append(j)
        return available_jumps
        
    def move_piece(self, piece, move, option, color):
        """ 
        Moves the piece into the new postion on the board
        Removes the piece from its original postion on the board
        And places it into the empty space on the board
        Checks if move was a jump or not and removes pieces that were jumped
        """
        piece_index = self.get_index_of_piece(piece)
        new_position_index = self.get_index_of_piece(move[0])

        self.board[piece_index[0]][piece_index[1]] = "_"
        self.board[new_position_index[0]][new_position_index[1]] = "b" if color == "black" else "w"

        self.check_if_move_was_jump(move, option, color)

        self.check_if_piece_needs_kinged(new_position_index, color)

        return new_position_index    

    def check_if_move_was_jump(self, move, option, color):
        """
        Checks if the move was a jump
        Removes the pieces that was jumped over 
        """
        if move[1] == "jump":
            jumped_pieces = move[2][option - 1]
            for piece in jumped_pieces:
                self.remove_piece_from_board(piece)
            return jumped_pieces
        else:
            return "move"
        
    def check_if_piece_needs_kinged(self, piece_index, color):
        """
        Checks if the piece moved needs to be kinged
        Kings the piece if it in correct position 
        """ 
        if self.check_if_piece_on_kings_edge(piece_index) == "Top" and color == "black":
            self.king_piece(piece_index, color)
            return "Kinged"
        elif self.check_if_piece_on_kings_edge(piece_index) == "Bottom" and color == "white":
            self.king_piece(piece_index, color)
            return "Kinged"
        else:
            return "Not kinged"

    def king_piece(self, piece_index, color):
        """
        Kings the piece
        If color is black change piece from b to B
        If color is white change piece from w to W 
        """
        if color == "black" and not self.check_if_piece_is_kinged(piece_index, color):
            self.board[piece_index[0]][piece_index[1]] = "B"
        elif color == "white" and not self.check_if_piece_is_kinged(piece_index, color):
            self.board[piece_index[0]][piece_index[1]] = "W"

        return self.board[piece_index[0]][piece_index[1]]

    def check_if_piece_is_kinged(self, piece_index, color):
        """
        Checks if the piece is a king or not
        Returns true if it is and false if not 
        """
        if color == "black" and self.board[piece_index[0]][piece_index[1]] == "B":
            return True
        elif color == "white" and self.board[piece_index[0]][piece_index[1]] == "W":
            return True
        else:
            return False

    def remove_piece_from_board(self, piece):
        """ 
        Removes the inputted piece from the board state
        """
        piece_index = self.get_index_of_piece(piece)
        self.board[piece_index[0]][piece_index[1]] = "_"

    def delete_last_log(self):
        """ 
        Removes the last jumped pieces log
        Change jump count by 1
        """
        if self.jump_count != 0:
            self.jump_count -= 1
            del self.jumped_pieces_log[self.jump_count]
            

    def change_color_go(self):
        """ 
        Changes the color to whosever go it is
        """
        if self.color_go == "black":
            self.color_go = "white"
        elif self.color_go == "white":
            self.color_go = "black"
    
    
