import sys
import numpy as np
from PyQt6.QtWidgets import (
    QMainWindow, QApplication, QPushButton, QHBoxLayout, QCheckBox,
    QGridLayout, QWidget, QVBoxLayout, QLineEdit, QLabel
)
from PyQt6.QtCore import Qt


def get_difficulty(idx):
    diffs = [3, 5, 10]

    if idx > 2:
        idx = 2

    return diffs[idx]


def give_title(turns):
    titles = [
        "TILES DESTRUCTOR",
        "very good, dude",
        "not bad player",
        "bruh...",
        "..noobie?",
        "the worst noob I've ever seen...",
    ]

    turns //= 7
    if turns > 5:
        turns = 5

    return "You are " + titles[turns]


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.HEIGHT = 5
        self.WIDTH = 5

        self.ALL = self.HEIGHT * self.WIDTH

        self.setFixedSize(350, 350)
        self.setStyleSheet("background-color: grey;")

        self.levels = []
        self.button_matrix = []
        self.matrix = np.ones(self.ALL, dtype=int)

        self.restart_button = QPushButton("Restart?")
        self.restart_button.setEnabled(False)
        self.restart_button.clicked.connect(self.restart)

        self.turn_count = 0
        self.color = [
            "background-color: #282828; padding: 20px;",
            "background-color: #a0a0a4; padding: 20px;",
        ]

        self.win_label = QLabel()
        self.win_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.turn_count_label = QLabel()
        self.turn_count_label.setAlignment(Qt.AlignmentFlag.AlignRight)

        hl = QHBoxLayout()
        hl.addWidget(self.win_label)
        hl.addWidget(self.turn_count_label)

        gl = QGridLayout()
        gl.addLayout(self.set_field(), 0, 0)
        gl.addLayout(hl, 1, 0)
        gl.addWidget(self.restart_button, 2, 0)

        vl = self.set_levels()

        gl.addLayout(vl, 0, 1)

        wg = QWidget()
        wg.setLayout(gl)
        self.setCentralWidget(wg)

        self.restart()

    def set_levels(self):
        vl = QVBoxLayout()

        diff = ["Easy", "Normal", "Hard"]
        for i, name in enumerate(diff, 0):
            box = QCheckBox(name)
            box.clicked.connect(self.levels_clicked)
            vl.addWidget(box)
            self.levels.append(box)

        return vl

    def set_field(self):
        gl = QGridLayout()

        gl.setSpacing(0)

        for i in range(self.HEIGHT):
            for j in range(self.WIDTH):
                button = QPushButton()

                button.setFixedSize(50, 50)
                button.setStyleSheet(self.color[1])
                button.pressed.connect(self.field_clicked)

                gl.addWidget(button, i, j)
                self.button_matrix.append(button)

        gl.setColumnStretch(0, 1)
        gl.setColumnStretch(gl.columnCount(), 1)

        return gl

    def levels_clicked(self):
        idx = self.levels.index(self.sender())

        for i, box in enumerate(self.levels, 0):
            if i != idx:
                box.setChecked(False)
            else:
                box.setChecked(True)

        diff = get_difficulty(idx)

        self.HEIGHT = self.WIDTH = diff
        self.ALL = self.HEIGHT * self.WIDTH

        # TODO: not working
        self.__init__()

    def field_clicked(self):
        self.turn_count += 1
        self.turn_count_label.setText("Turns: " + str(self.turn_count))

        idx = self.button_matrix.index(self.sender())

        self.switch(idx)

        if self.matrix.sum() == self.ALL:
            self.win()

    def switch(self, idx):
        for i in range(idx % self.WIDTH, self.ALL, self.WIDTH):
            self.matrix[i] = (self.matrix[i] + 1) % 2
            self.button_matrix[i].setStyleSheet(self.color[self.matrix[i]])

        for i in range((idx // self.WIDTH) * self.WIDTH, (idx // self.WIDTH + 1) * self.WIDTH):
            if i == idx:
                continue
            self.matrix[i] = (self.matrix[i] + 1) % 2
            self.button_matrix[i].setStyleSheet(self.color[self.matrix[i]])

    def win(self):
        for button in self.button_matrix:
            button.setEnabled(False)
        self.win_label.setText("You win!!! \n" + give_title(self.turn_count))
        self.restart_button.setEnabled(True)

    def restart(self):
        self.restart_button.setEnabled(False)

        for i in np.random.randint(0, self.ALL, 100):
            self.switch(i)

        for button in self.button_matrix:
            button.setEnabled(True)

        self.win_label.setText("Turn all Gray tiles to White")
        self.turn_count_label.setText("Turns: 0")
        self.turn_count = 0


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()
