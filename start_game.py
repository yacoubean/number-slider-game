from PyQt5.QtWidgets import QGridLayout, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal
from random import choice

from game_play import check_move, move_tile


def set_board_positions(board_locations):
    for row_num in range(0,4):
        for col_num in range(0,4):
            board_locations[row_num][col_num].position = board_locations[row_num][col_num].pos()


def initiate_game_tiles(game_layout, board_locations):
    game_tiles = []

    # load the game time images as clickable labels into the game_tiles list
    for tile_no in range(0, 15):
        tile_no_img_num = tile_no + 1
        num_img = QPixmap('images\\numTile{0}.png'.format(str(tile_no_img_num)))
        num_label = ClickableQLabel(tile_no, game_layout, game_tiles, board_locations)
        num_label.setPixmap(num_img)
        num_label.is_empty_tile = False
        game_tiles.append(num_label)

    return game_tiles


class GameLayout(QGridLayout):
    def __init__(self, board_locations):
        QGridLayout.__init__(self)
        self.board_locations = board_locations

    def define_layout(self, game_tiles):
        # define the game grid layout
        GameLayout.setHorizontalSpacing(self,0)
        GameLayout.setVerticalSpacing(self,0)

        # add the game tiles to the game grid from the game_tiles list
        tile_num = 0
        placed_tiles = []
        for row_num in range(0, 4):
            self.board_locations[row_num] = {}
            for col_num in range(0, 4):
                if tile_num < 15:
                    # select a random tile that wasn't already placed on the game board
                    random_tile = choice([i for i in range(0, 15) if i not in placed_tiles])
                    self.addWidget(game_tiles[random_tile], row_num, col_num)
                    self.board_locations[row_num][col_num] = game_tiles[random_tile]
                    game_tiles[random_tile].board_location = str(row_num) + '-' + str(col_num)
                    placed_tiles.append(random_tile)
                    tile_num += 1
        # add a board location for the bottom right square, which always starts empty so won't have a tile in it yet
        empty_tile = ClickableQLabel(15, self, game_tiles, self.board_locations)
        empty_tile.is_empty_tile = True
        game_tiles.append(empty_tile)
        self.addWidget(empty_tile,3,3)
        self.board_locations[3][3] = empty_tile
        game_tiles[15].board_location = '3-3'


class ClickableQLabel(QLabel):
    click_signal = pyqtSignal(object)

    def __init__(self, tile_num, game_layout, game_tiles, board_locations):
        QLabel.__init__(self)
        self.tile_num = tile_num
        self.game_tiles = game_tiles
        self.game_layout = game_layout
        self.board_locations = board_locations

    def mouseReleaseEvent(self, ev):
        valid_move_location = check_move(self.tile_num, self.game_tiles, self.board_locations)

        if 'qpoint' in valid_move_location:
            self.click_signal.emit(move_tile(valid_move_location, self.tile_num, self.game_layout, self.game_tiles))