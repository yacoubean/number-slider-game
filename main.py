from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QHBoxLayout

from start_game import *


class MainGameWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Number Slide Game")
        outer_layout = QVBoxLayout()

        top_menu = QHBoxLayout()
        restart_game_btn = QPushButton("Restart game", self)
        restart_game_btn.clicked.connect(restart_game)
        top_menu.addWidget(restart_game_btn, alignment=Qt.AlignRight)

        self.board_locations = {}
        self.game_layout = GameLayout(self.board_locations)
        self.game_tiles = initiate_game_tiles(self, self.game_layout, self.board_locations)

        self.game_layout.define_layout(self.game_tiles)
        outer_layout.addLayout(top_menu)
        outer_layout.addLayout(self.game_layout)
        self.setLayout(outer_layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    game_window = MainGameWindow()
    game_window.show()
    # this has to be after the game window is drawn, because only then are the tiles fully in
    # place allowing me to get and store their positions
    set_board_positions(game_window.board_locations)
    sys.exit(app.exec_())
