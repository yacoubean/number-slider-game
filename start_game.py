import sys
import os

from PyQt5.QtWidgets import QGridLayout, QLabel, QDialog, QDialogButtonBox, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal, Qt
from random import choice

from game_play import check_move, move_tile


def set_board_positions(board_locations):
    for row_num in range(0, 4):
        for col_num in range(0, 4):
            board_locations[row_num][col_num].position = board_locations[row_num][col_num].pos()


def initiate_game_tiles(self, game_layout, board_locations):
    game_tiles = []
    self.announce_win = announce_win

    # comment out this os command if running from source. this is needed when running from an .exe file
    # os.chdir(sys._MEIPASS)

    # load the game time images as clickable labels into the game_tiles list
    for tile_no in range(0, 15):
        tile_no_img_num = tile_no + 1
        num_img = QPixmap('images\\numTile{0}.png'.format(str(tile_no_img_num)))
        num_label = ClickableQLabel(tile_no, game_layout, game_tiles, board_locations, self.announce_win)
        num_label.setPixmap(num_img)
        num_label.is_empty_tile = False
        game_tiles.append(num_label)

    return game_tiles


def restart_game():
    os.execl(sys.executable, sys.executable, *sys.argv)


def announce_win(self):
    you_won_dialog = CustomDialog(self)
    if you_won_dialog.exec():
        restart_game()
    else:
        sys.exit("Player chose to quit the game")


class CustomDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Game over")
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        dialog_buttons = QDialogButtonBox.Yes | QDialogButtonBox.No

        self.buttonBox = QDialogButtonBox(dialog_buttons)
        # noinspection PyUnresolvedReferences
        self.buttonBox.accepted.connect(self.accept)
        # noinspection PyUnresolvedReferences
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel("You won! Play again?")
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


class GameLayout(QGridLayout):
    def __init__(self, board_locations):
        QGridLayout.__init__(self)
        self.board_locations = board_locations
        self.placed_tiles = []

    def define_layout(self, game_tiles):
        # define the game grid layout
        GameLayout.setHorizontalSpacing(self, 0)
        GameLayout.setVerticalSpacing(self, 0)

        # add the game tiles to the game grid from the game_tiles list
        tile_num = 0
        for row_num in range(0, 4):
            self.board_locations[row_num] = {}
            for col_num in range(0, 4):
                if tile_num < 15:
                    # select a random tile that wasn't already placed on the game board
                    random_tile = choice([i for i in range(0, 15) if i not in self.placed_tiles])
                    self.addWidget(game_tiles[random_tile], row_num, col_num)
                    self.board_locations[row_num][col_num] = game_tiles[random_tile]
                    game_tiles[random_tile].board_location = str(row_num) + '-' + str(col_num)
                    self.placed_tiles.append(random_tile)
                    tile_num += 1

        # add a board location for the bottom right square, which always starts empty so won't have a tile in it yet
        empty_tile = ClickableQLabel(15, self, game_tiles, self.board_locations, None)
        empty_tile.is_empty_tile = True
        game_tiles.append(empty_tile)
        self.addWidget(empty_tile, 3, 3)
        self.board_locations[3][3] = empty_tile
        game_tiles[15].board_location = '3-3'

    # the logic for is_solvable was taken from https://www.geeksforgeeks.org/check-instance-15-puzzle-solvable/
    # in my case the grid is always 4x4 with empty space at bottom right, so that simplifies the logic
    def is_solvable(self):
        num_inversions = self.get_inversions()
        if num_inversions % 2 == 0:
            return True
        return False

    def get_inversions(self):
        cnt = 0
        for i, x in enumerate(self.placed_tiles[:-1]):
            if x != '':
                for y in self.placed_tiles[i + 1:]:
                    if y != '' and int(x) > int(y):
                        cnt += 1
        return cnt


class ClickableQLabel(QLabel):
    click_signal = pyqtSignal(object)

    def __init__(self, tile_num, game_layout, game_tiles, board_locations, announce_win_obj):
        QLabel.__init__(self)
        self.tile_num = tile_num
        self.game_tiles = game_tiles
        self.game_layout = game_layout
        self.board_locations = board_locations
        self.announce_win = announce_win_obj

    def mouseReleaseEvent(self, ev):
        valid_move_location = check_move(self.tile_num, self.game_tiles, self.board_locations)

        if 'qpoint' in valid_move_location:
            # noinspection PyUnresolvedReferences
            self.click_signal.emit(
                move_tile(
                    self,
                    valid_move_location,
                    self.tile_num,
                    self.game_layout,
                    self.game_tiles,
                    self.board_locations
                )
            )
