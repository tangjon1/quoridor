import random
import pygame as pg
import time


class Bot:
    """Governs the actions of the artificial 'intelligence' when playing against a bot."""
    def __init__(self, quoridor, player_num):
        """Initializes the Quoridor bot to play as the specified player in the specified game."""
        self._quoridor = quoridor
        self._player_num = player_num
        self._min_think_time = 1300

    def find_min_moves(self, player_num, account_pawn, pfence_align=None, pfence_coord=None, cur_tiles=None, path_count=None, num_moves=None, coords=None):
        """This method returns the length of the shortest path from the given tile to a winning tile."""
        q = self._quoridor

        if path_count is None:
            path_count = 0

        if cur_tiles is None:
            cur_tiles = [q.get_player_pawn(player_num)]

        if num_moves is None:
            num_moves = {}

        if coords is None:
            coords = set()

        if len(cur_tiles) == 0:
            return None

        if type(cur_tiles) is tuple:
            cur_tiles = [cur_tiles]

        for i in cur_tiles:
            if q.is_winning_tile(player_num, i):
                return path_count

        if (path_count + 1) not in num_moves:
            num_moves[path_count + 1] = []

        for i in cur_tiles:
            valid_tiles = q.valid_tiles(player_num, i, pfence_align, pfence_coord, account_pawn)
            for j in valid_tiles:
                if j not in num_moves[path_count + 1] and j not in coords:
                    num_moves[path_count + 1].append(j)
            coords.add(i)

        path_count += 1
        return self.find_min_moves(player_num, account_pawn, pfence_align, pfence_coord, num_moves[path_count], path_count, num_moves, coords)

    def find_optimal_path(self, player_num, account_pawn, pfence_align=None, pfence_coord=None, path=None, cur_tile=None):
        """This method takes a player number and returns the path to win that requires the least moves. The path
        is in the form of a list of tuples, starting with the starting tile."""
        q = self._quoridor

        if cur_tile is None:
            cur_tile = q.get_player_pawn(player_num)

        if path is None:
            path = []

        path.append(cur_tile)

        if q.is_winning_tile(player_num, cur_tile):
            return path

        cur_min_move = self.find_min_moves(player_num, account_pawn, pfence_align, pfence_coord, cur_tiles=cur_tile)

        valid_tiles = q.valid_tiles(player_num, cur_tile, pfence_align, pfence_coord, account_pawn)

        for i in valid_tiles:
            p_min_move = self.find_min_moves(player_num, account_pawn, pfence_align, pfence_coord, cur_tiles=i)
            if p_min_move is not None and cur_min_move is not None:
                if p_min_move < cur_min_move:
                    return self.find_optimal_path(player_num, account_pawn, pfence_align, pfence_coord, path, i)
            else:
                return path

    def find_rand_optimal_path(self, player_num, account_pawn, pfence_align=None, pfence_coord=None, path=None, cur_tile=None):
        """This method returns the shortest path, in any tile order."""
        q = self._quoridor

        if cur_tile is None:
            cur_tile = q.get_player_pawn(player_num)

        if path is None:
            path = []

        path.append(cur_tile)

        if q.is_winning_tile(player_num, cur_tile):
            return path

        cur_min_moves = self.find_min_moves(player_num, account_pawn, pfence_align, pfence_coord, cur_tiles=cur_tile)

        valid_tiles = q.valid_tiles(player_num, cur_tile, pfence_align, pfence_coord, account_pawn)
        path_valid_tiles = []

        for i in valid_tiles:
            p_min_moves = self.find_min_moves(player_num, account_pawn, pfence_align, pfence_coord, cur_tiles=i)
            if cur_min_moves is not None and p_min_moves is not None:
                if p_min_moves < cur_min_moves:
                    path_valid_tiles.append(i)
            else:
                return path

        return self.find_rand_optimal_path(player_num, account_pawn, pfence_align, pfence_coord, path, random.choice(path_valid_tiles))

    def get_optimal_fence_placement(self, player_num, account_pawn):
        """This method returns the coordinates of possible fences that would most hinder the opponent with regards to
        the number of moves required to win. Returns the fence as a dictionary with the alignment as the key and the
        tuple as the value."""
        q = self._quoridor

        board = q.get_board()
        opponent_num = q.get_opposing_num(player_num)
        #print("Self:", player_num)
        #print("Opponent:", opponent_num)
        alignments = ["v", "h"]

        best_fences = {}

        for row in board:
            for coord in row:
                for align in alignments:
                    fair_play = True
                    for temp_num in range(1, 3):
                        if not q.fair_play_checker(temp_num, align, coord):
                            fair_play = False
                    if fair_play:
                        opponent_min_moves = self.find_min_moves(opponent_num, False)
                        self_min_moves = self.find_min_moves(player_num, False)
                        p_min_moves_opponent = self.find_min_moves(opponent_num, account_pawn, align, coord)
                        p_min_moves_self = self.find_min_moves(player_num, account_pawn, align, coord)
                        if p_min_moves_opponent is not None and p_min_moves_self is not None:
                            move_change_opponent = p_min_moves_opponent - opponent_min_moves
                            move_change_self = p_min_moves_self - self_min_moves

                            #  Positive: The opponent's path length is increased more than ours
                            move_change_diff = move_change_opponent - move_change_self
                            #print()
                            #print("Alignment:", align)
                            #print("Coords:", coord)
                            #print("Self Original Min Moves:", self_min_moves)
                            #print("Self Theoretical Min Moves:", p_min_moves_self)
                            #print("Self Move Difference:", move_change_self)
                            #print("Opponent Original Min Moves:", opponent_min_moves)
                            #print("Opponent Theoretical Min Moves:", p_min_moves_opponent)
                            #print("Opponent Move Difference:", move_change_opponent)
                            #print("Move Change Difference:", move_change_diff)

                            if move_change_diff not in best_fences:
                                best_fences[move_change_diff] = {}
                            #if len(best_fences[move_change]) not in best_fences[move_change]:
                            best_fences[move_change_diff][len(best_fences[move_change_diff]) + 1] = {}
                            best_fences[move_change_diff][len(best_fences[move_change_diff])]["alignment"] = align
                            best_fences[move_change_diff][len(best_fences[move_change_diff])]["coord"] = coord
        return best_fences

    def get_fence_increased_moves(self, best_fences_list):
        """Takes the output from 'get_optimal_fence_placement' and returns the maximum amount of turns that could
        be added to the enemy player's path with a single fence."""
        max_move_increase = None
        for i in best_fences_list:
            if max_move_increase is None:
                max_move_increase = int(i)
            if int(i) > max_move_increase:
                max_move_increase = int(i)
        return max_move_increase

    def make_move_v2(self, player_num):
        q = self._quoridor
        opponent_num = q.get_opposing_num(player_num)

        self_min_path = self.find_rand_optimal_path(player_num, True)
        opponent_min_path = self.find_optimal_path(opponent_num, True)

        print("Self Path:", self_min_path)
        print("Opponent Path:", opponent_min_path)

        if len(self_min_path) >= 2:
            self_next_tile = self_min_path[1]
        else:
            self_next_tile = random.choice(q.valid_tiles(player_num, q.get_player_pawn(player_num)))

        if len(opponent_min_path) >= 2:
            opponent_next_tile = opponent_min_path[1]
        else:
            opponent_next_tile = random.choice(q.valid_tiles(opponent_num, q.get_player_pawn(opponent_num)))

        #  Action 1: Win
        if q.is_winning_tile(player_num, self_next_tile):
            pg.time.delay(self._min_think_time)
            q.move_pawn(player_num, self_next_tile)
            return

        #  Action 2: Block Win
        if q.get_remaining_fences(player_num) > 0:
            if q.is_winning_tile(opponent_num, opponent_next_tile):
                pg.time.delay(self._min_think_time)
                if opponent_num == 1:
                    front_tile = (q.get_player_pawn(opponent_num)[0], (q.get_player_pawn(opponent_num)[1] + 1))
                elif opponent_num == 2:
                    front_tile = q.get_player_pawn(opponent_num)
                if not q.place_fence(player_num, "h", front_tile):
                    q.move_pawn(player_num, self_next_tile)
                return

            #  Action 3: Place Beneficial, Non-Neutral Fence
            best_fences = self.get_optimal_fence_placement(player_num, False)
            max_move_diff = self.get_fence_increased_moves(best_fences)

            if max_move_diff > 1:
                random.seed()
                rand_fence = random.randint(1, len(best_fences[max_move_diff]))
                alignment = best_fences[max_move_diff][rand_fence]["alignment"]
                coord = best_fences[max_move_diff][rand_fence]["coord"]
                if not q.place_fence(player_num, alignment, coord):
                    q.move_pawn(player_num, self_next_tile)
                #print(best_fences)
                #print("Max Move Diff:", max_move_diff)
                #print("Fence of ")
                return

            #  Action 4: Move to the next tile unless it is in front of the opponent, in which case, place a fence in
            if opponent_num == 1:
                tile_in_front = (q.get_player_pawn(opponent_num)[0], (q.get_player_pawn(opponent_num)[1] + 1))
            elif opponent_num == 2:
                tile_in_front = (q.get_player_pawn(opponent_num)[0], (q.get_player_pawn(opponent_num)[1] - 1))

            if self_next_tile == tile_in_front:
                if opponent_num == 1:
                    front_tile = (q.get_player_pawn(opponent_num)[0], (q.get_player_pawn(opponent_num)[1] + 1))
                elif opponent_num == 2:
                    front_tile = q.get_player_pawn(opponent_num)
                if not q.place_fence(player_num, "h", front_tile):
                    q.move_pawn(player_num, self_next_tile)
                return
        pg.time.delay(self._min_think_time)
        q.move_pawn(player_num, self_next_tile)
        return


if __name__ == '__main__':
    q = Quoridor.QuoridorGame(9, 10)
    q.add_fence("horizontal", (1, 4))
    q.add_fence("horizontal", (2, 4))
    q.add_fence("horizontal", (3, 4))
    q.add_fence("horizontal", (4, 4))
    q.add_fence("horizontal", (5, 4))
    q.add_fence("horizontal", (6, 4))
    q.add_fence("horizontal", (7, 4))
    q.add_fence("horizontal", (8, 4))

    #q.add_fence("horizontal", (0, 1))
    q.add_fence("vertical", (4, 5))
    q.add_fence("vertical", (4, 6))
    q.add_fence("vertical", (4, 7))
    q.add_fence("vertical", (4, 8))

    q.add_fence("vertical", (1, 4))
    q.add_fence("vertical", (1, 5))
    q.add_fence("vertical", (1, 6))
    q.add_fence("vertical", (1, 7))

    q.add_fence("horizontal", (0, 3))

    q.set_player_pawn(1, (0, 2))

    bot_player_num = 2
    bot = Bot(q, bot_player_num)

    q.print_board()
    print(bot.get_optimal_fence_placement(bot_player_num, False))
    q.print_board()











