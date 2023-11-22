from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout, QPushButton

from start_game import *


class MainGameWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("NumberSlider")
        self.outer_layout = QVBoxLayout()

        self.top_menu = QHBoxLayout()
        self.move_ctr = 0

        set_move_counter(self, self.move_ctr)

        new_game_btn = QPushButton("New game", self)
        new_game_btn.clicked.connect(restart_game)
        self.top_menu.addWidget(new_game_btn, alignment=Qt.AlignRight)

        def setup_game():
            self.board_locations = {}
            self.game_layout = GameLayout(self.board_locations, self)
            self.game_tiles = initiate_game_tiles(self, self.game_layout, self.board_locations)
            self.game_layout.define_layout(self.game_tiles)

        setup_game()

        while not self.game_layout.is_solvable():
            setup_game()

        self.outer_layout.addLayout(self.top_menu)
        self.outer_layout.addLayout(self.game_layout)
        self.setLayout(self.outer_layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    game_window = MainGameWindow()
    game_window.show()
    # this has to be after the game window is drawn because only then are the tiles fully in
    # place allowing me to get and store their positions
    set_board_positions(game_window.board_locations)
    sys.exit(app.exec_())
