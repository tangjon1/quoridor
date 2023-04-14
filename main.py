import math
import pygame as pg
import Quoridor
import QuoridorBot
pg.init()

#  Game information
GRID_SIZE = 9
FENCE_COUNT = 10

#  Graphics information
TILE_SIZE = 60
TILE_COLOR_1 = (255, 205, 125)
TILE_COLOR_2 = (150, 119, 69)

PLAYER_SIZE = 40
P1_COLOR = (240, 60, 60)
P2_COLOR = (60, 60, 240)

FENCE_HEIGHT = 10
FENCE_LENGTH = TILE_SIZE
FENCE_COLOR = (59, 37, 16)

P1_HIGHLIGHT_COLOR = (255, 166, 166)
P2_HIGHLIGHT_COLOR = (166, 166, 255)

UI_AREA_ABOVE = 60
UI_AREA_LEFT = 0

FENCE_INFO_X_OFFSET = 10
FENCE_INFO_Y_OFFSET = 5

BOARD_SIZE = GRID_SIZE * TILE_SIZE
WIN_WIDTH = BOARD_SIZE + UI_AREA_LEFT
WIN_HEIGHT = BOARD_SIZE + UI_AREA_ABOVE

#  Menu Graphics
MENU_BUTTON_TEXT_SIZE = 25

MENU_START_GAME_X_OFFSET = WIN_WIDTH // 2
MENU_START_GAME_Y_OFFSET = WIN_HEIGHT // 3

MENU_BOT_SETTINGS_X_OFFSET = 2 * (WIN_WIDTH // 3)
MENU_BOT_SETTINGS_DISTANCE = 60
MENU_BOT_SETTINGS_Y_OFFSET = MENU_START_GAME_Y_OFFSET + MENU_BOT_SETTINGS_DISTANCE


#  Menu Buttons
MENU_START_GAME = "PLAY"  # Starts a default PvP game
#  Bot Options
MENU_BOT_NONE = "NONE"
MENU_BOT_PLAYER_1 = "PLAYER 1"
MENU_BOT_PLAYER_2 = "PLAYER 2"
MENU_PLAY_VS_BOT = "PLAY VERSUS BOT"  # Starts a game against an AI opponent
#  Game Mode Options
MENU_MODE_STANDARD = "STANDARD"

#  Initialize display
pg.display.set_caption("Quoridor")
WIN = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
WIN.fill((0, 0, 0))

#  Initialize game
q = Quoridor.QuoridorGame(GRID_SIZE, FENCE_COUNT)


class Button:
    """This class represents a clickable object with an associated Rect."""
    def __init__(self, string, rect):
        """Initializes a button with the specified purpose (string) and Rect object."""
        self._text = string
        self._rect = rect

    def is_cursor_selected(self):
        """Returns True if the cursor position is within the Rect area."""
        if self._rect.collidepoint(pg.mouse.get_pos()):
            return True
        return False

    def get_text(self):
        """Returns the text of the Button."""
        return self._text

    def get_rect(self):
        """This method returns the Rect of the Button."""
        return self._rect

    def draw_highlight_selected(self):
        """Draws a highlight Rect to show that the button is selected."""
        if self.is_cursor_selected():
            pg.draw.rect(WIN, P1_HIGHLIGHT_COLOR, self._rect, 3)
            return True


class MenuDisplay:
    """This class contains the methods used to display the main menu in a window."""
    def __init__(self):
        """Initializes the menu."""
        self._button_list = self.draw_menu()
        self._button_list_copy = list(self._button_list)

    def draw_button(self, text, draw_coord, text_size, text_color):
        """This method creates and returns a button object with text and draws it centered
        on the specified tuple coordinate."""
        button_text_style = pg.font.SysFont(None, text_size)
        button = button_text_style.render(text, False, text_color)
        button_size = button.get_size()
        button_x_offset = draw_coord[0] - (button_size[0] // 2)
        button_y_offset = draw_coord[1] - (button_size[1] // 2)
        WIN.blit(button, (button_x_offset, button_y_offset))

        button_rect = pg.rect.Rect(button_x_offset, button_y_offset, button_size[0], button_size[1])
        button_obj = Button(text, button_rect)
        return button_obj

    def get_button_list(self):
        """This method returns a list of clickable buttons on the menu."""
        return self._button_list_copy

    def get_button_by_text(self, text):
        """This method returns the button with the specified text, if available."""
        button_list = self.get_button_list()
        for i in button_list:
            if i.get_text() == text:
                return i
        return None

    def draw_menu(self):
        """Draws the menu elements. Returns a list of Button objects."""
        buttons = []

        # Title text
        title_text_style = pg.font.SysFont(None, 50)

        quoridor_title = title_text_style.render("QUORIDOR", False, (255, 255, 255))
        quoridor_title_size = quoridor_title.get_size()
        title_x_offset = (WIN_WIDTH // 2) - (quoridor_title_size[0] // 2)
        WIN.blit(quoridor_title, (title_x_offset, 20))

        #  Bot settings text
        text_style = pg.font.SysFont(None, 30)

        bot_settings_header = text_style.render("BOT:", False, (255, 255, 255))
        bot_settings_header_size = bot_settings_header.get_size()
        WIN.blit(bot_settings_header, (MENU_BOT_SETTINGS_X_OFFSET - (bot_settings_header_size[0] // 2), MENU_BOT_SETTINGS_Y_OFFSET - (bot_settings_header_size[1] // 2)))

        #  Start Game Button
        buttons.append(self.draw_button(MENU_START_GAME, (MENU_START_GAME_X_OFFSET, MENU_START_GAME_Y_OFFSET), 40, (255, 255, 255)))

        #  Bot Setting: None
        buttons.append(self.draw_button(MENU_BOT_NONE, (MENU_BOT_SETTINGS_X_OFFSET, MENU_BOT_SETTINGS_Y_OFFSET + MENU_BOT_SETTINGS_DISTANCE), MENU_BUTTON_TEXT_SIZE, (255, 255, 255)))

        #  Bot Setting: Player 1
        buttons.append(self.draw_button(MENU_BOT_PLAYER_1, (MENU_BOT_SETTINGS_X_OFFSET, MENU_BOT_SETTINGS_Y_OFFSET + (2 * MENU_BOT_SETTINGS_DISTANCE)), MENU_BUTTON_TEXT_SIZE, P1_COLOR))

        #  Bot Setting: Player 2
        buttons.append(self.draw_button(MENU_BOT_PLAYER_2, (MENU_BOT_SETTINGS_X_OFFSET, MENU_BOT_SETTINGS_Y_OFFSET + (3 * MENU_BOT_SETTINGS_DISTANCE)), MENU_BUTTON_TEXT_SIZE, P2_COLOR))

        return buttons

    def active_menu(self, list_of_buttons):
        WIN.fill((0, 0, 0))
        self.draw_menu()
        for i in list_of_buttons:
            if i.draw_highlight_selected():
                return i.get_text()


class GameDisplay:
    """This class contains the methods used to display the game in a window."""
    def __init__(self):
        """Initializes the board."""
        self._drawn_board = self.draw_board()
        self._drawn_board_copy = dict(self._drawn_board)

        self._fence_rects = self.generate_fence_rects()
        self._fence_rects_copy = dict(self._fence_rects)

        self.draw_pawns()

        self.draw_ui()

    def draw_board(self):
        """This method draws the board in the window. Returns a dictionary with the coordinate tuples as keys and the
        Rect objects as values."""
        board = q.get_board()
        tiles = {}

        x_tile_offset = UI_AREA_LEFT
        swap_colors = False
        for i in board:
            y_tile_offset = UI_AREA_ABOVE
            for j in i:
                tile = pg.Rect(x_tile_offset, y_tile_offset, TILE_SIZE, TILE_SIZE)
                tiles[j] = tile

                if swap_colors:
                    pg.draw.rect(WIN, TILE_COLOR_1, tile)
                else:
                    pg.draw.rect(WIN, TILE_COLOR_2, tile)

                y_tile_offset += TILE_SIZE
                swap_colors = not swap_colors
            swap_colors = not swap_colors
            x_tile_offset += TILE_SIZE
        return tiles

    def get_tiles(self):
        """This method returns a dictionary of the tiles with the tuple board coordinates as keys and the Rect objects
        as values."""
        return self._drawn_board_copy

    def get_fences(self):
        """This method returns a dictionary of the fences with the tuple board coordinates as keys and the Rect objects
        as values."""
        return self._fence_rects_copy

    def get_rect_from_coord(self, coord):
        """This method takes a tuple coordinate and returns the associated Rect object."""
        tiles = self.get_tiles()
        return tiles[coord]

    def get_coord_from_rect(self, tile):
        """This method takes a tile Rect object and returns its coordinates on the board."""
        board_coord_x = ((tile.x - UI_AREA_LEFT) / TILE_SIZE)
        board_coord_y = ((tile.y - UI_AREA_ABOVE) / TILE_SIZE)
        return math.floor(board_coord_x), math.floor(board_coord_y)

    def get_coord_from_fence_rect(self, fence_rect):
        """This method takes a fence Rect object and returns the associated coordinates on the board."""
        if fence_rect.height > fence_rect.width: #  Vertical fence
            board_coord_x = ((fence_rect.x - UI_AREA_LEFT + fence_rect.width ) / TILE_SIZE)
            board_coord_y = ((fence_rect.y - UI_AREA_ABOVE) / TILE_SIZE)

        if fence_rect.height < fence_rect.width: #  Horizontal fence
            board_coord_x = ((fence_rect.x - UI_AREA_LEFT) / TILE_SIZE)
            board_coord_y = ((fence_rect.y - UI_AREA_ABOVE + fence_rect.height) / TILE_SIZE)

        return math.floor(board_coord_x), math.floor(board_coord_y)

    def generate_fence_rects(self):
        """This method creates rect objects for every possible fence location on the board. Returns a dictionary with
        containing 'vertical' and 'horizontal' dictionaries. These dictionaries contain the coordinate tuples as keys
        and the Rect objects as values."""
        tiles = self.get_tiles()
        fences = {"vertical": {}, "horizontal": {}}

        for i in tiles:
            tile_coord = self.get_coord_from_rect(tiles[i])
            if tile_coord[0] != 0 and tile_coord[0] != GRID_SIZE:
                ver_fence = pg.Rect(tiles[i].x - (FENCE_HEIGHT//2), tiles[i].y, FENCE_HEIGHT, FENCE_LENGTH)
                fences["vertical"][tile_coord] = ver_fence
            if tile_coord[1] != 0 and tile_coord[1] != GRID_SIZE:
                hor_fence = pg.Rect(tiles[i].x, tiles[i].y - (FENCE_HEIGHT//2), FENCE_LENGTH, FENCE_HEIGHT)
                fences["horizontal"][tile_coord] = hor_fence

        return fences

    def draw_pawns(self):
        """This method draws the current locations of a given player's pawn onto the board."""
        p1_rect = self.get_rect_from_coord(q.get_player_pawn(1))
        p2_rect = self.get_rect_from_coord(q.get_player_pawn(2))

        pg.draw.circle(WIN, P1_COLOR, p1_rect.center, (PLAYER_SIZE//2))
        pg.draw.circle(WIN, P2_COLOR, p2_rect.center, (PLAYER_SIZE//2))

    def draw_placed_fences(self):
        """This method draws the current placed fences on the board."""
        fence_placements = self.get_fences()
        ver_fences = q.get_player_vertical_fences()
        hor_fences = q.get_player_horizontal_fences()

        for i in fence_placements["vertical"]:
            for j in ver_fences:
                if i == j:
                    pg.draw.rect(WIN, FENCE_COLOR, fence_placements["vertical"][i])

        for i in fence_placements["horizontal"]:
            for j in hor_fences:
                if i == j:
                    pg.draw.rect(WIN, FENCE_COLOR, fence_placements["horizontal"][i])

    def draw_ui(self):
        """Draws the UI elements on the game screen."""
        text_style = pg.font.SysFont(None, 30)

        p1_fence_title = text_style.render("Player 1 Fences:", False, P1_HIGHLIGHT_COLOR)
        p1_fence_title_size = p1_fence_title.get_size()
        WIN.blit(p1_fence_title, (FENCE_INFO_X_OFFSET, FENCE_INFO_Y_OFFSET))

        p1_fence_number = text_style.render(str(q.get_remaining_fences(1)), False, P1_HIGHLIGHT_COLOR)
        p1_fence_number_size = p1_fence_number.get_size()
        p1_x_offset = (p1_fence_title_size[0] // 2) - (p1_fence_number_size[0] // 2)
        p1_y_offset = (p1_fence_title_size[1] + (2 * FENCE_INFO_Y_OFFSET))
        WIN.blit(p1_fence_number, (p1_x_offset, p1_y_offset))

        p2_fence_title = text_style.render("Player 2 Fences:", False, P2_HIGHLIGHT_COLOR)
        p2_fence_title_size = p2_fence_title.get_size()
        fence_display_x_offset = WIN_WIDTH - p2_fence_title_size[0] - FENCE_INFO_X_OFFSET
        WIN.blit(p2_fence_title, (fence_display_x_offset, FENCE_INFO_Y_OFFSET))

        p2_fence_number = text_style.render(str(q.get_remaining_fences(2)), False, P2_HIGHLIGHT_COLOR)
        p2_fence_number_size = p2_fence_number.get_size()
        p2_x_offset = WIN_WIDTH - (p2_fence_title_size[0] // 2) - (p2_fence_number_size[0 // 2])
        p2_y_offset = (p2_fence_title_size[1] + (2 * FENCE_INFO_Y_OFFSET))
        WIN.blit(p2_fence_number, (p2_x_offset, p2_y_offset))

    def draw_victory(self):
        """This method displays text informing the players of the victor, and prompts the players to quit."""
        text_style = pg.font.SysFont(None, 35)

        if q.get_game_state() == "PLAYER_1_WIN":
            victory_text = "PLAYER 1 WIN"
            color = P1_COLOR
        elif q.get_game_state() == "PLAYER_2_WIN":
            victory_text = "PLAYER 2 WIN"
            color = P2_COLOR
        elif q.get_game_state() == "STALEMATE":
            victory_text = "STALEMATE"
            color = (255, 255, 255)

        victory_1 = text_style.render(victory_text, False, color)
        victory_1_size = victory_1.get_size()
        p1_x_offset = (WIN_WIDTH // 2) - (victory_1_size[0] // 2)
        p1_y_offset = (UI_AREA_ABOVE // 2) - (victory_1_size[1] // 2)
        WIN.blit(victory_1, (p1_x_offset, p1_y_offset))


    def draw_entire_board(self):
        """This method draws all tiles, pawns, and fences onto the window."""
        self.draw_board()
        self.draw_pawns()
        self.draw_placed_fences()

    def draw_entire_screen(self):
        """This method draws everything onto the window."""
        WIN.fill((0, 0, 0))
        self.draw_entire_board()
        self.draw_ui()

    def pos_in_list_of_rect(self, win_coord, list_of_rects):
        """This method takes a position on the window as a tuple coordinate and a list of Rect objects, and returns the
        first Rect that is contains the given coordinate. If none of the Rects contain the coordinate, returns None."""
        for i in list_of_rects:
            if i.collidepoint(win_coord):
                return i
        return None

    def highlight_selected_rect(self, player_num, rect):
        """This method draws a highlight Rect of the given player's highlight color."""
        if player_num == 1:
            highlight_color = P1_HIGHLIGHT_COLOR
        elif player_num == 2:
            highlight_color = P2_HIGHLIGHT_COLOR

        draw_highlight_rect = True
        fair_play = True

        if rect.width != rect.height:
            if rect.width > rect.height:
                ali = "h"
            else:
                ali = "v"
            opp = q.get_opposing_num(player_num)
            rect_coord = self.get_coord_from_fence_rect(rect)
            fair_play = q.fair_play_checker(opp, ali, rect_coord) and q.fair_play_checker(player_num, ali, rect_coord)

        if rect.width != rect.height and q.get_remaining_fences(player_num) < 1:
            draw_highlight_rect = False
        if not fair_play:
            draw_highlight_rect = False

        if draw_highlight_rect:
            pg.draw.rect(WIN, highlight_color, rect)
            self.draw_placed_fences()

    def active_turn(self, player_num):
        valid_rects = []
        for i in q.valid_tiles(player_num, q.get_player_pawn(player_num)):
            valid_rects.append(self.get_rect_from_coord(i))

        fences = self.get_fences()
        for i in fences["vertical"]:
            valid_rects.append(fences["vertical"][i])
        for i in fences["horizontal"]:
            valid_rects.append(fences["horizontal"][i])

        gd.draw_entire_screen()

        selected_rect = self.pos_in_list_of_rect(pg.mouse.get_pos(), valid_rects)

        if selected_rect is not None:
            self.highlight_selected_rect(player_num, selected_rect)

        elif selected_rect is None:
            gd.draw_entire_screen()

        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN and selected_rect is not None:
                if selected_rect.width == selected_rect.height:
                    q.move_pawn(player_num, self.get_coord_from_rect(selected_rect))
                elif selected_rect.height > selected_rect.width:
                    q.place_fence(player_num, "v", self.get_coord_from_fence_rect(selected_rect))
                elif selected_rect.width > selected_rect.height:
                    q.place_fence(player_num, "h", self.get_coord_from_fence_rect(selected_rect))
                gd.draw_entire_screen()


if __name__ == '__main__':
    menu = MenuDisplay()
    start_game = False
    init_game = False

    bot_screen_draw = False

    #  Default Mode Settings
    mode_standard = True

    #  Default Bot Settings
    bot_select = MENU_BOT_NONE
    bot_none = True
    bot_player_1 = False
    bot_player_2 = False
    bot_player_num = None

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            if not start_game:
                menu.draw_menu()
                if event.type == pg.MOUSEBUTTONDOWN:
                    print("Registered Mouse Down")
                    for i in menu.get_button_list():
                        print(i.get_text() + ": " + str(i.is_cursor_selected()))
                    print(menu.active_menu(menu.get_button_list()))
                    #  Button to start game with current settings
                    if menu.active_menu(menu.get_button_list()) == MENU_START_GAME:
                        print("Starting game")
                        start_game = True

                    #  Bot Settings
                    if menu.active_menu(menu.get_button_list()) == MENU_BOT_NONE:
                        bot_none = True
                        bot_player_1 = False
                        bot_player_2 = False
                        bot_select = MENU_BOT_NONE
                    if menu.active_menu(menu.get_button_list()) == MENU_BOT_PLAYER_1:
                        bot_none = False
                        bot_player_1 = True
                        bot_player_2 = False
                        bot_select = MENU_BOT_PLAYER_1
                    if menu.active_menu(menu.get_button_list()) == MENU_BOT_PLAYER_2:
                        bot_none = False
                        bot_player_1 = False
                        bot_player_2 = True
                        bot_select = MENU_BOT_PLAYER_2
            pg.draw.rect(WIN, (255, 255, 255), menu.get_button_by_text(bot_select).get_rect(), 3)

        if start_game:
            if not init_game:
                gd = GameDisplay()
                init_game = True

            if q.is_ongoing():
                if not bot_screen_draw:
                    if bot_player_1:
                        bot_player_num = 1
                    elif bot_player_2:
                        bot_player_num = 2
                    if not bot_none:
                        bot = QuoridorBot.Bot(q, bot_player_num)
                    gd.draw_entire_screen()
                    pg.display.update()
                    bot_screen_draw = True
                if q.get_turn() == 1:
                    if not bot_player_1:
                        gd.active_turn(1)
                    else:
                        bot.make_move_v2(1)
                        gd.draw_entire_screen()
                elif q.get_turn() == 2:
                    if not bot_player_2:
                        gd.active_turn(2)
                    else:
                        bot.make_move_v2(2)
                        gd.draw_entire_screen()
            else:
                gd.draw_entire_screen()
                gd.draw_victory()
                if event.type == pg.MOUSEBUTTONDOWN:
                    running = False

        pg.display.update()









