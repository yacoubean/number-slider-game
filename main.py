import sys
from PyQt5.QtWidgets import QWidget, QApplication

from start_game import *


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
    # this has to be after the game window is drawn, because only then are the tiles fully in
    # place allowing me to get and store their positions
    set_board_positions(game_window.board_locations)
    sys.exit(app.exec_())