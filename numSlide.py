import sys
import random

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

def move_tile(tile_to_move, game_tiles):
    game_tile_to_move = game_tiles[tile_to_move]
    game_tile_to_move.anim = QPropertyAnimation(game_tile_to_move, b"pos")
    # hard coding where the tile should move to for now, since the tile we're moving was hard coded to tile 11 above
    game_tile_to_move.anim.setEndValue(QPoint(220, 221))
    game_tile_to_move.anim.setDuration(200)
    game_tile_to_move.anim.start()

class ClickableQLabel(QLabel):
    click_signal = pyqtSignal(object)

    def __init__(self, tile_num, game_tiles):
        QLabel.__init__(self)
        self.game_tiles = game_tiles

    def mouseReleaseEvent(self, ev):
        #hard coding which tile to move, tile 11 for now, for testing. need to implement tile move game logic later
        self.click_signal.emit(move_tile(11, self.game_tiles))


class NewGame(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Number Slide Game")
        self.game_tiles = []

        #load the game time images as clickable labels into the game_tiles list
        for tile_no in range(0, 15):
            tile_no_img_num = tile_no + 1
            num_img = QPixmap('images\\numTile{0}.png'.format(str(tile_no_img_num)))
            num_label = ClickableQLabel(tile_no, self.game_tiles)
            num_label.setPixmap(num_img)
            self.game_tiles.append(num_label)

        random.shuffle(self.game_tiles)

        #define the game grid layout
        game_layout = QGridLayout()
        game_layout.setHorizontalSpacing(0)
        game_layout.setVerticalSpacing(0)

        #add the game tiles to the game grid from the game_tiles list
        tile_num = 0
        for rowNum in range(0, 4):
            for colNum in range(0, 4):
                if tile_num < 15:
                    game_layout.addWidget(self.game_tiles[tile_num], rowNum, colNum)
                    tile_num += 1

        self.setLayout(game_layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gameWindow = NewGame()
    gameWindow.show()
    sys.exit(app.exec_())
