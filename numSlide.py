import sys
import pprint

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from random import choice

from PyQt5.QtWidgets import QLabel


def set_board_positions(board_locations):
    for row_num in range(1,5):
        for col_num in range(1,5):
            board_locations[row_num][col_num].position = board_locations[row_num][col_num].pos()


def move_tile(tile_to_move, new_tile_location, game_tiles):
    game_tile_to_move = game_tiles[tile_to_move]
    game_tile_to_move.anim = QPropertyAnimation(game_tile_to_move, b"pos")
    game_tile_to_move.anim.setEndValue(new_tile_location) # QPoint(220, 221)
    game_tile_to_move.anim.setDuration(200)
    game_tile_to_move.anim.start()


def find_opening(tile_num,tile_row,tile_col,board_locations,game_tiles):
    row_above = tile_row - 1
    row_below = tile_row + 1
    col_left = tile_col - 1
    col_right = tile_col + 1

    opening_found = False

    if row_above > 0:
        tile_above = board_locations[row_above][tile_col]
        if not isinstance(tile_above,ClickableQLabel):
            # tile above is a valid game location, and it's empty
            opening_found = tile_above.position
            new_tile_row = row_above
            new_tile_col = tile_col
    if row_below < 5:
        tile_below = board_locations[row_below][tile_col]
        if not isinstance(tile_below,ClickableQLabel):
            # tile below is a valid game location, and it's empty
            opening_found = tile_below.position
            new_tile_row = row_below
            new_tile_col = tile_col
    if col_left > 0:
        tile_left = board_locations[tile_row][col_left]
        if not isinstance(tile_left,ClickableQLabel):
            # tile left is a valid game location, and it's empty
            opening_found = tile_left.position
            new_tile_row = tile_row
            new_tile_col = col_left
    if col_right < 5:
        tile_right = board_locations[tile_row][col_right]
        if not isinstance(tile_right,ClickableQLabel):
            # tile right is a valid game location, and it's empty
            opening_found = tile_right.position
            new_tile_row = tile_row
            new_tile_col = col_right

    if isinstance(opening_found,QPoint):
        # get the placeholder QLabel from the empty tile location
        empty_tile = board_locations[new_tile_row][new_tile_col]
        # store the moving tile's old position
        moving_tile_position = board_locations[tile_row][tile_col].position
        # set the moving tile's position to the empty tile's position
        board_locations[tile_row][tile_col].position = empty_tile.position
        # set the empty tile's position to its new location (the moving tile's old position)
        empty_tile.position = moving_tile_position
        # now actually move the tiles in the board_locations dictionary
        board_locations[new_tile_row][new_tile_col] = board_locations[tile_row][tile_col]
        board_locations[tile_row][tile_col] = empty_tile
        game_tiles[tile_num].board_location = str(new_tile_row) + '-' + str(new_tile_col)

    return opening_found


def check_move(tile_num,game_tiles,board_locations):
    this_tile_loc = game_tiles[tile_num].board_location
    tile_row_col = this_tile_loc.split('-')
    this_tile_row = int(tile_row_col[0])
    this_tile_col = int(tile_row_col[1])
    open_tile = find_opening(tile_num,this_tile_row,this_tile_col,board_locations,game_tiles)

    return open_tile


class ClickableQLabel(QLabel):
    click_signal = pyqtSignal(object)

    def __init__(self, tile_num, game_tiles, board_locations):
        QLabel.__init__(self)
        self.tile_num = tile_num
        self.game_tiles = game_tiles
        self.board_locations = board_locations

    def mouseReleaseEvent(self, ev):
        valid_move_location = check_move(self.tile_num, self.game_tiles, self.board_locations)

        if isinstance(valid_move_location, QPoint):
            self.click_signal.emit(move_tile(self.tile_num, valid_move_location, self.game_tiles))
            pprint.pprint(self.board_locations[4][4])


class NewGame(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Number Slide Game")
        self.game_tiles = []
        self.board_locations = {}

        # load the game time images as clickable labels into the game_tiles list
        for tile_no in range(0, 15):
            tile_no_img_num = tile_no + 1
            num_img = QPixmap('images\\numTile{0}.png'.format(str(tile_no_img_num)))
            num_label = ClickableQLabel(tile_no, self.game_tiles, self.board_locations)
            num_label.setPixmap(num_img)
            self.game_tiles.append(num_label)

        # define the game grid layout
        game_layout = QGridLayout()
        game_layout.setHorizontalSpacing(0)
        game_layout.setVerticalSpacing(0)

        # add the game tiles to the game grid from the game_tiles list
        tile_num = 0
        placed_tiles = []
        for row_num in range(0, 4):
            this_row = row_num+1
            self.board_locations[this_row] = {}
            for col_num in range(0, 4):
                this_col = col_num+1
                if tile_num < 15:
                    # select a random tile that wasn't already placed on the game board
                    random_tile = choice([i for i in range(0,15) if i not in placed_tiles])
                    game_layout.addWidget(self.game_tiles[random_tile], row_num, col_num)
                    self.board_locations[this_row][this_col] = self.game_tiles[random_tile]
                    self.game_tiles[random_tile].board_location = str(this_row)+'-'+str(this_col)
                    placed_tiles.append(random_tile)
                    tile_num += 1
        # add a board location for the bottom right square, which always starts empty so won't have a tile in it yet
        empty_tile = QLabel('')
        game_layout.addWidget(empty_tile)
        self.board_locations[4][4] = empty_tile

        self.setLayout(game_layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gameWindow = NewGame()
    gameWindow.show()
    set_board_positions(gameWindow.board_locations)
    sys.exit(app.exec_())