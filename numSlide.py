import sys
# import pprint

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from random import choice

from PyQt5.QtWidgets import QLabel


def set_board_positions(board_locations):
    for row_num in range(0,4):
        for col_num in range(0,4):
            board_locations[row_num][col_num].position = board_locations[row_num][col_num].pos()


def find_opening(tile_num,tile_row,tile_col,board_locations,game_tiles):
    row_above = tile_row - 1
    row_below = tile_row + 1
    col_left = tile_col - 1
    col_right = tile_col + 1

    opening_found = {}

    if row_above > -1:
        tile_above = board_locations[row_above][tile_col]
        if tile_above.is_empty_tile:
            # tile above is a valid game location, and it's empty
            opening_found['qpoint'] = tile_above.position
            opening_found['new_row'] = row_above
            opening_found['new_col'] = tile_col
    if row_below < 4:
        tile_below = board_locations[row_below][tile_col]
        if tile_below.is_empty_tile:
            # tile below is a valid game location, and it's empty
            opening_found['qpoint'] = tile_below.position
            opening_found['new_row'] = row_below
            opening_found['new_col'] = tile_col
    if col_left > -1:
        tile_left = board_locations[tile_row][col_left]
        if tile_left.is_empty_tile:
            # tile left is a valid game location, and it's empty
            opening_found['qpoint'] = tile_left.position
            opening_found['new_row'] = tile_row
            opening_found['new_col'] = col_left
    if col_right < 4:
        tile_right = board_locations[tile_row][col_right]
        if tile_right.is_empty_tile:
            # tile right is a valid game location, and it's empty
            opening_found['qpoint'] = tile_right.position
            opening_found['new_row'] = tile_row
            opening_found['new_col'] = col_right

    if 'qpoint' in opening_found:
        # get the placeholder QLabel from the empty tile location
        empty_tile = board_locations[opening_found['new_row']][opening_found['new_col']]
        # store the moving tile's old position
        moving_tile_position = board_locations[tile_row][tile_col].position
        # set the moving tile's position to the empty tile's position
        board_locations[tile_row][tile_col].position = empty_tile.position
        # set the empty tile's position to its new location (the moving tile's old position)
        empty_tile.position = moving_tile_position
        # now actually move the tiles in the board_locations dictionary
        board_locations[opening_found['new_row']][opening_found['new_col']] = board_locations[tile_row][tile_col]
        board_locations[tile_row][tile_col] = empty_tile
        # game_tiles[tile_num].board_location = str(opening_found['new_row']) + '-' + str(opening_found['new_col'])

    return opening_found


def check_move(tile_num,game_tiles,board_locations):
    this_tile_loc = game_tiles[tile_num].board_location
    tile_row_col = this_tile_loc.split('-')
    this_tile_row = int(tile_row_col[0])
    this_tile_col = int(tile_row_col[1])
    open_tile = find_opening(tile_num,this_tile_row,this_tile_col,board_locations,game_tiles)

    return open_tile


def move_tile(new_tile_location, tile_to_move, game_layout, game_tiles):
    game_tile_to_move = game_tiles[tile_to_move]
    original_tile_loc = game_tile_to_move.board_location.split('-')
    original_tile_row = int(original_tile_loc[0])
    original_tile_col = int(original_tile_loc[1])
    game_layout.removeWidget(game_tiles[tile_to_move])
    game_layout.removeWidget(game_tiles[15]) # 15 is hard coded here because the open tile will always be tile_num=15
    game_layout.addWidget(game_tiles[15], original_tile_row, original_tile_col)
    game_layout.addWidget(game_tiles[tile_to_move], new_tile_location['new_row'], new_tile_location['new_col'])

    tile_to_move_board_loc = game_tiles[tile_to_move].board_location
    game_tiles[tile_to_move].board_location = game_tiles[15].board_location
    game_tiles[15].board_location = tile_to_move_board_loc


    game_tile_to_move.anim = QPropertyAnimation(game_tile_to_move, b"pos")
    game_tile_to_move.anim.setEndValue(new_tile_location['qpoint'])
    game_tile_to_move.anim.setDuration(200)
    game_tile_to_move.anim.start()


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


class MainGameClass(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Number Slide Game")
        self.board_locations = {}
        self.game_layout = GameLayout(self.board_locations)
        self.game_tiles = initiate_game_tiles(self.game_layout, self.board_locations)

        self.game_layout.define_layout(self.game_tiles)
        self.setLayout(self.game_layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    game_window = MainGameClass()
    game_window.show()
    set_board_positions(game_window.board_locations)
    sys.exit(app.exec_())