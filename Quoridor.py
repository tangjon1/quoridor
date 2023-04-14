# Description: This program represents an implementation of the board game 'Quoridor' for two players. Quoridor is
#   played on a 9x9 grid, and each player controls one pawn. One player starts on the center of an edge of the board,
#   and the opposing player starts in the center of the opposing edge of the board, facing the first player. Each turn,
#   a player may either move their pawn orthogonally one tile, or place a fence on the border between tiles. Fences
#   block movement between the tiles it is placed between for both players. Each player starts with 10 fences. A player
#   wins when they reach the end of the board opposite to their starting side.
#
#   If the two players' pawns are facing each other, the player whose turn it is may 'jump' over the opposing pawn,
#   provided there is not a fence between the pawns nor behind the pawn that is being jumped over. If there is a fence
#   behind the pawn that is being jumped over, the jumping piece may instead move to either the left or right side of
#   the other pawn (diagonally).
#
#   In this implementation, players use the 'move_pawn' or 'place_fence' methods to perform the respective actions.
#   Player 1 starts on the top row, while Player 2 starts on the bottom row.

class QuoridorGame:
    """This class represents the Quoridor game, managing the game's current board state, player actions, and their
    validity."""

    def __init__(self, grid_size, fence_count):
        """Initializes the Quoridor game. Sets up the board, player starting positions, turn, and each players'
        number of fences."""
        #  Initialize the number of columns and rows.
        self._grid_size = grid_size

        #  Initialize the representation of the game board.
        self._game_board = {"board": [], "pawns": {"player_1": (), "player_2": ()}, "fences": {"player_vertical": [],
                            "player_horizontal": [], "border_vertical": [], "border_horizontal": []}}

        #  Initialize board, which is a list of lists. Tiles are represented as tuples of the respective
        #  coordinates in '(column, row)' format. The column and row tile length are increased by 1 to account for the
        #  border fences, but are otherwise unused during gameplay.
        board = self._game_board["board"]
        for i in range(0, self._grid_size + 1):
            board.append(list())
            column_list = board[i]
            for j in range(0, self._grid_size + 1):
                tile_to_add = (i, j)
                column_list.append(tile_to_add)

        #  Initialize pawn locations.
        self._game_board["pawns"]["player_1"] = (self._grid_size // 2, 0)
        self._game_board["pawns"]["player_2"] = (self._grid_size // 2, self._grid_size - 1)

        #  Initialize the fences around the borders of the playable area.
        #  Vertical fences are on the left of the associated tile.
        #  Horizontal fences are above the associated tile.
        vertical_fences = self._game_board["fences"]["border_vertical"]
        for i in board[0]:
            vertical_fences.append(i)
        for i in board[self._grid_size]:
            vertical_fences.append(i)

        horizontal_fences = self._game_board["fences"]["border_horizontal"]
        for i in board:
            horizontal_fences.append(i[0])
            horizontal_fences.append(i[self._grid_size])

        #  Initialize the players' available fences.
        self._player_1_fence_count = fence_count
        self._player_2_fence_count = fence_count

        #  Initialize the first player's turn.
        self._current_game_turn = 1

        #  Initialize the current game state ("ONGOING", "PLAYER_1_WIN", or "PLAYER_2_WIN").
        self._game_state = "ONGOING"

    def get_grid_size(self):
        """This method returns the size of the grid specified in '__init__'."""
        return self._grid_size

    def get_board(self):
        """This method returns the board, a list of lists of tuples."""
        return self._game_board["board"]

    def check_in_bounds(self, coord):
        """This method returns True if the given coordinates are within the bounds of the playable area, and False
        otherwise."""
        if coord[0] > (self.get_grid_size() - 1) or coord[0] < 0:
            return False
        if coord[1] > (self.get_grid_size() - 1) or coord[1] < 0:
            return False
        return True

    def get_opposing_num(self, player_num):
        """This method takes a player number and returns the opposing player's number."""
        if player_num == 1:
            return 2
        if player_num == 2:
            return 1

    def get_player_pawn(self, player_num):
        """This method takes a player number and returns the coordinates of that player's pawn as a tuple."""
        if player_num == 1:
            return self._game_board["pawns"]["player_1"]
        if player_num == 2:
            return self._game_board["pawns"]["player_2"]

    def set_player_pawn(self, player_num, coord):
        """This method takes a player number and moves that player's pawn to the specified tuple coordinates. Note this
        movement bypasses the rules of the game."""
        if player_num == 1:
            self._game_board["pawns"]["player_1"] = coord
        if player_num == 2:
            self._game_board["pawns"]["player_2"] = coord

    def get_opposing_pawn(self, player_num):
        """This method takes a player number and returns the coordinates of the opposing player's pawn."""
        if player_num == 1:
            return self._game_board["pawns"]["player_2"]
        if player_num == 2:
            return self._game_board["pawns"]["player_1"]

    def get_vertical_fences(self):
        """This method returns a list of the coordinates of all vertical fences (left of the tile)."""
        ver_fences = self._game_board["fences"]["border_vertical"] + self._game_board["fences"]["player_vertical"]
        return ver_fences

    def get_horizontal_fences(self):
        """This method returns a list of the coordinates of all horizontal fences (above the tile)."""
        hor_fences = self._game_board["fences"]["border_horizontal"] + self._game_board["fences"]["player_horizontal"]
        return hor_fences

    def get_player_vertical_fences(self):
        """This method returns a list of all player-placed vertical fences."""
        player_ver_fences = self._game_board["fences"]["player_vertical"]
        return player_ver_fences

    def get_player_horizontal_fences(self):
        """This method returns a list of all player-placed horizontal fences."""
        player_hor_fences = self._game_board["fences"]["player_horizontal"]
        return player_hor_fences

    def get_turn(self):
        """This method returns which player's turn it is: 'player_1' or 'player_2'."""
        return self._current_game_turn

    def check_turn(self, player_num):
        """This method takes a player number and returns True if it is currently that player's turn, and False
        otherwise."""
        if player_num == 1 and self._current_game_turn == 1:
            return True
        if player_num == 2 and self._current_game_turn == 2:
            return True
        return False

    def advance_turn(self):
        """This method advances the current player's turn to the next player's."""
        if self._current_game_turn == 1:
            self._current_game_turn = 2
        elif self._current_game_turn == 2:
            self._current_game_turn = 1

    def add_fence(self, alignment, coord):
        """This method adds a fence of the given alignment ('vertical' or 'horizontal') to the specified coordinate."""
        fences = self._game_board["fences"]
        if alignment == "vertical":
            fences["player_vertical"].append(coord)
        if alignment == "horizontal":
            fences["player_horizontal"].append(coord)

    def get_remaining_fences(self, player_num):
        """This method takes a player number and returns that player's number of remaining fences."""
        if player_num == 1:
            return self._player_1_fence_count
        if player_num == 2:
            return self._player_2_fence_count

    def decrement_fence_count(self, player_num):
        """This method takes a player number and decrements the number of that player's remaining fences by 1."""
        if player_num == 1:
            self._player_1_fence_count -= 1
        if player_num == 2:
            self._player_2_fence_count -= 1

    def get_game_state(self):
        """This method returns the current game state: 'ONGOING','PLAYER_1_WIN', or 'PLAYER_2_WIN'."""
        return self._game_state

    def is_ongoing(self):
        """This method returns True if the current game state is 'ONGOING', and False otherwise."""
        if self._game_state == "ONGOING":
            return True
        return False

    def set_victory(self, player_num):
        """This method changes the game state to a victory for the given player number."""
        if player_num == 0:
            self._game_state = "STALEMATE"
        if player_num == 1:
            self._game_state = "PLAYER_1_WIN"
        if player_num == 2:
            self._game_state = "PLAYER_2_WIN"

    def is_winner(self, player_num):
        """This method takes the players' number and returns True if that player has won, and False if that player
        has not won."""
        if player_num == 1 and self.get_game_state() == "PLAYER_1_WIN":
            return True
        if player_num == 2 and self.get_game_state() == "PLAYER_2_WIN":
            return True
        return False

    def is_winning_tile(self, player_num, tile_coord):
        """This method takes a player number and tile coordinate and returns True if the tile is a winning
        tile for the player."""
        if player_num == 1 and tile_coord[1] == (self.get_grid_size() - 1):
            return True
        if player_num == 2 and tile_coord[1] == 0:
            return True
        return False

    def winning_tiles(self, player_num):
        """This method takes a player number and returns a list of tuples that correspond to the tiles that that player
        wins on."""
        board = self.get_board()
        winning_tiles = []
        if player_num == 1:
            for i in board:
                winning_tiles.append(i[len(i) - 1])
        if player_num == 2:
            for i in board:
                winning_tiles.append(i[0])
        return winning_tiles

    def valid_tiles_above(self, player_num, coord, ver_fences, hor_fences, account_pawn=None):
        """This method takes a player_number, coordinate, list of vertical fences, and list of horizontal fences. It
        returns a list of the valid tiles a player on that spot may move to that are above the given position.
        This movement accounts for a possible 'jump' over facing pawns."""
        valid_tiles_above = []
        board = self.get_board()

        column = coord[0]
        row = coord[1]

        opposing_pawn = self.get_opposing_pawn(player_num)

        tile_above = board[column][row - 1]
        if not (board[column][row] in hor_fences):
            if account_pawn and not tile_above == opposing_pawn:
                valid_tiles_above.append(tile_above)
            elif not account_pawn:
                valid_tiles_above.append(tile_above)
        if account_pawn and tile_above == opposing_pawn and player_num == 2 and not (board[column][row] in hor_fences):
            if not (tile_above in hor_fences):
                valid_tiles_above.append(board[column][row - 2])
            else:
                if not (tile_above in ver_fences):
                    valid_tiles_above.append(board[column - 1][row - 1])
                if not (board[column + 1][row - 1] in ver_fences):
                    valid_tiles_above.append(board[column + 1][row - 1])
        return valid_tiles_above

    def valid_tiles_right(self, player_num, coord, ver_fences, hor_fences, account_pawn=None):
        """This method takes a player_number, coordinate, list of vertical fences, and list of horizontal fences. It
        returns a list of the valid tiles a player on that spot may move to that are right of the given position."""
        valid_tiles_right = []
        board = self.get_board()

        column = coord[0]
        row = coord[1]

        opposing_pawn = self.get_opposing_pawn(player_num)

        tile_right = board[column + 1][row]
        if not (tile_right in ver_fences):
            if account_pawn and not tile_right == opposing_pawn:
                valid_tiles_right.append(tile_right)
            elif not account_pawn:
                valid_tiles_right.append(tile_right)
        return valid_tiles_right

    def valid_tiles_below(self, player_num, coord, ver_fences, hor_fences, account_pawn=None):
        """This method takes a player_number, coordinate, list of vertical fences, and list of horizontal fences. It
        returns a list of the valid tiles a player on that spot may move to that are below the given position.
        This movement accounts for a possible 'jump' over facing pawns."""
        valid_tiles_below = []
        board = self.get_board()

        column = coord[0]
        row = coord[1]

        opposing_pawn = self.get_opposing_pawn(player_num)
        tile_below = board[column][row + 1]
        if not (tile_below in hor_fences):
            if account_pawn and not tile_below == opposing_pawn:
                valid_tiles_below.append(tile_below)
            elif not account_pawn:
                valid_tiles_below.append(tile_below)
        if account_pawn and tile_below == opposing_pawn and player_num == 1 and not (tile_below in hor_fences):
            if not board[column][row + 2] in hor_fences:
                valid_tiles_below.append(board[column][row + 2])
            else:
                if not (tile_below in ver_fences):
                    valid_tiles_below.append(board[column - 1][row + 1])
                if not (board[column + 1][row + 1] in ver_fences):
                    valid_tiles_below.append(board[column + 1][row + 1])
        return valid_tiles_below

    def valid_tiles_left(self, player_num, coord, ver_fences, hor_fences, account_pawn=None):
        """This method takes a player_number, coordinate, list of vertical fences, and list of horizontal fences. It
        returns a list of the valid tiles a player on that spot may move to that are left of the given position."""
        valid_tiles_left = []
        board = self.get_board()

        column = coord[0]
        row = coord[1]

        opposing_pawn = self.get_opposing_pawn(player_num)

        tile_left = board[column - 1][row]
        if not (board[column][row] in ver_fences):
            if account_pawn and not tile_left == opposing_pawn:
                valid_tiles_left.append(tile_left)
            elif not account_pawn:
                valid_tiles_left.append(tile_left)
        return valid_tiles_left

    def valid_tiles(self, player_num, coord, prop_fence_align=None, prop_fence_coord=None, account_pawn=None):
        """This method takes the player number as an integer and coordinates as a tuple (column, row) and returns a
        list of the valid positions (as tuples) to which a pawn on that tile may move to."""
        if account_pawn is None:
            account_pawn = True

        #  Get the positions of the fences
        ver_fences = list(self.get_vertical_fences())
        hor_fences = list(self.get_horizontal_fences())

        if prop_fence_align == "v":
            ver_fences.append(prop_fence_coord)
        if prop_fence_align == "h":
            hor_fences.append(prop_fence_coord)

        #  Check the tile orthogonally above
        tiles_above = self.valid_tiles_above(player_num, coord, ver_fences, hor_fences, account_pawn=account_pawn)

        #  Check the tile orthogonally right
        tiles_right = self.valid_tiles_right(player_num, coord, ver_fences, hor_fences, account_pawn=account_pawn)

        #  Check the tile orthogonally below
        tiles_below = self.valid_tiles_below(player_num, coord, ver_fences, hor_fences, account_pawn=account_pawn)

        #  Check the tile orthogonally left
        tiles_left = self.valid_tiles_left(player_num, coord, ver_fences, hor_fences, account_pawn=account_pawn)

        valid_tiles = tiles_above + tiles_right + tiles_below + tiles_left
        return valid_tiles

    def has_valid_moves(self, player_num):
        """This method returns True if the given player has any valid moves to make, either moving their pawn or
        placing a fence. Returns False otherwise."""
        valid_tiles = self.valid_tiles(player_num, self.get_player_pawn(player_num))

        if len(valid_tiles) == 0 and self.get_remaining_fences(player_num) < 1:
            return False

        return True

    def move_pawn(self, player_num, coord):
        """This method moves the specified player's pawn (1 or 2) to the specified coordinates (as
        given by a tuple). If the move is valid, the game board is updated and the method returns True. Otherwise, the
        game board is not updated and the method returns False."""
        if self.get_game_state() != "ONGOING":
            return False

        if not self.check_turn(player_num):
            return False

        player_coord = self.get_player_pawn(player_num)

        valid_tiles = self.valid_tiles(player_num, player_coord)

        if coord in valid_tiles:
            self.set_player_pawn(player_num, coord)
            if player_num == 1 and coord[1] == (self.get_grid_size() - 1):
                self.set_victory(player_num)
            if player_num == 2 and coord[1] == 0:
                self.set_victory(player_num)
            if not self.has_valid_moves(self.get_opposing_num(player_num)):
                self.set_victory(0)
            self.advance_turn()
            return True

        return False

    def fair_play_checker(self, player_num, prop_fence_align, prop_fence_coord, accessible_tiles=None, init_call=None):
        """This method returns True if there is a path that allows the given player's pawn to reach the end
         of the board and win. Returns False otherwise."""
        if init_call is None:
            init_call = True

        #  Track the tiles that are accessible by the given player
        if accessible_tiles is None:
            accessible_tiles = []

        #  Add the player's current position to the list of accessible tiles
        if init_call:
            accessible_tiles.append(self.get_player_pawn(player_num))

        #  Check the valid tiles for each of the already tracked tiles
        valid_tile_count = 0
        for i in range(0, len(accessible_tiles)):
            valid_tiles = self.valid_tiles(player_num, accessible_tiles[i], prop_fence_align, prop_fence_coord, False)
            for j in valid_tiles:
                if j not in accessible_tiles:
                    accessible_tiles.append(j)
                    valid_tile_count += 1

        #print(accessible_tiles)

        if valid_tile_count == 0:
            for i in range(0, len(accessible_tiles)):
                if accessible_tiles[i][1] == 0 and player_num == 2:
                    return True
                if accessible_tiles[i][1] == (self.get_grid_size() - 1) and player_num == 1:
                    return True
                if i == (len(accessible_tiles) - 1):
                    return False
        else:
            return self.fair_play_checker(player_num, prop_fence_align, prop_fence_coord, accessible_tiles, False)

    def place_fence(self, player_num, alignment, coord):
        """This method takes a player's number (1 or 2) and attempts to place one of their fences on the specified
        tile coordinate, aligned either vertically or horizontally (v or h). If the placement is valid and does not
        break the fair play rule, the method returns True. If the placement is valid but breaks the fair play rule,
        returns "breaks the fair play rule". Otherwise, the method returns False."""
        if self.get_game_state() != "ONGOING":
            return False

        if not self.check_turn(player_num):
            return False

        if self.get_remaining_fences(player_num) <= 0:
            return False

        if not self.check_in_bounds(coord):
            return False

        if alignment == "v":
            if coord not in self.get_vertical_fences():
                if not self.fair_play_checker(self.get_opposing_num(player_num), alignment, coord):
                    return False
                elif not self.fair_play_checker(player_num, alignment, coord):
                    return False
                else:
                    self.add_fence("vertical", coord)
                    self.decrement_fence_count(player_num)
                    if not self.has_valid_moves(self.get_opposing_num(player_num)):
                        self.set_victory(0)
                    self.advance_turn()
                    return True

        if alignment == "h":
            if coord not in self.get_horizontal_fences():
                if not self.fair_play_checker(self.get_opposing_num(player_num), alignment, coord):
                    return False
                elif not self.fair_play_checker(player_num, alignment, coord):
                    return False
                else:
                    self.add_fence("horizontal", coord)
                    self.decrement_fence_count(player_num)
                    if not self.has_valid_moves(self.get_opposing_num(player_num)):
                        self.set_victory(0)
                    self.advance_turn()
                return True

        return False

    def dir_move_pawn(self, player_num, direction):
        """This method moves the specified player's pawn in the specified direction: 'up', 'down', 'left', or
        'right'. Jumps cannot be performed using this method."""
        pawn_coord = self.get_player_pawn(player_num)
        board = self.get_board()

        cur_column = pawn_coord[0]
        cur_row = pawn_coord[1]

        if direction == "up":
            tile = board[cur_column][cur_row - 1]
        elif direction == "down":
            tile = board[cur_column][cur_row + 1]
        elif direction == "right":
            tile = board[cur_column + 1][cur_row]
        elif direction == "left":
            tile = board[cur_column - 1][cur_row]
        else:
            tile = (0, 0)

        return self.move_pawn(player_num, tile)

    def print_board(self):
        """Prints a representation of the current board. '1' represents Player 1's pawn. '2' represents Player 2's pawn.
        An 'X' represents a valid position that the current player may move to. A '.' represents an otherwise empty
        space."""
        rep_p1 = "1"
        rep_p2 = "2"
        rep_empty = "."
        rep_valid = "X"

        p1_valid = self.valid_tiles(1, self.get_player_pawn(1))
        p2_valid = self.valid_tiles(2, self.get_player_pawn(2))

        board = self._game_board["board"]
        display_row_list = []
        for i in range(0, self._grid_size):
            count = 0
            for j in board:
                if count != self._grid_size:
                    if j[i] == self._game_board["pawns"]["player_1"]:
                        display_row_list.append(rep_p1)
                    elif j[i] == self._game_board["pawns"]["player_2"]:
                        display_row_list.append(rep_p2)
                    else:
                        if self.get_turn() == 1 and j[i] in p1_valid:
                            display_row_list.append(rep_valid)
                        elif self.get_turn() == 2 and j[i] in p2_valid:
                            display_row_list.append(rep_valid)
                        else:
                            display_row_list.append(rep_empty)
                count += 1
            print(display_row_list)
            display_row_list.clear()

        if self.get_turn() == 1:
            print("Player 1 Valid Moves: ", p1_valid)
        if self.get_turn() == 2:
            print("Player 2 Valid Moves: ", p2_valid)
        print("Vertical Fences:", self._game_board["fences"]["player_vertical"])
        print("Horizontal Fences:", self._game_board["fences"]["player_horizontal"])
        print("Player 1 Remaining Fences:", self.get_remaining_fences(1))
        print("Player 2 Remaining Fences:", self.get_remaining_fences(2))
        #print("Border Vertical Fences:", self._game_board["fences"]["border_vertical"])
        #print("Border Horizontal Fences:", self._game_board["fences"]["border_horizontal"])


if __name__ == '__main__':
    q = QuoridorGame(9, 10)
    print(q.move_pawn(1, (4, 1)))
    q.print_board()