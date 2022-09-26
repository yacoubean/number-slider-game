import sys
import random

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class ClickableQLabel(QLabel):
    clickSignal = pyqtSignal(object)

    def __init__(self, move_tile, tile_num, parent=None):
        QLabel.__init__(self, parent)
        self.clickSignal.connect(move_tile)

    def mouseReleaseEvent(self, ev):
        #hard coding which tile to move, tile 11 for now, for testing. need to implement tile move game logic later
        self.clickSignal.emit(self.move_tile(11)) #currently this is where the code fails, without throwing an error
        #super(QLabel, self).mouseReleaseEvent(ev)


class NewGame(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Number Slide Game")
        self.gameTiles = []

        #load the game time images as clickable labels into the gameTiles list
        for tile_no in range(0, 15):
            tile_no_img_num = tile_no + 1
            num_img = QPixmap('images\\numTile{0}.png'.format(str(tile_no_img_num)))
            num_label = ClickableQLabel(self.move_tile, tile_no)
            num_label.setPixmap(num_img)
            self.gameTiles.append(num_label)

        random.shuffle(self.gameTiles)

        #define the game grid layout
        game_layout = QGridLayout()
        game_layout.setHorizontalSpacing(0)
        game_layout.setVerticalSpacing(0)

        #add the game tiles to the game grid from the gameTiles list
        tile_num = 0
        for rowNum in range(0, 4):
            for colNum in range(0, 4):
                if tile_num < 15:
                    game_layout.addWidget(self.gameTiles[tile_num], rowNum, colNum)
                    tile_num += 1

        self.setLayout(game_layout)

    def move_tile(self, tile_to_move):
        game_tile_to_move = self.gameTiles[tile_to_move]
        game_tile_to_move.anim = QPropertyAnimation(game_tile_to_move, b"pos")
        #hard coding where the tile should move to for now, since the tile we're moving was hard coded to tile 11 above
        game_tile_to_move.anim.setEndValue(QPoint(220, 221))
        game_tile_to_move.anim.setDuration(200)
        game_tile_to_move.anim.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gameWindow = NewGame()
    gameWindow.show()
    sys.exit(app.exec_())
