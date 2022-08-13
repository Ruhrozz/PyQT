import sys
import numpy as np
from PyQt6.QtWidgets import (
    QMainWindow, QApplication, QPushButton, QHBoxLayout,
    QGridLayout, QWidget, QVBoxLayout, QLineEdit, QLabel
)
from PyQt6.QtCore import Qt


HEIGHT = 5
WIDTH = 5

ALL = HEIGHT*WIDTH


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

        self.setFixedSize(270, 350)
        self.setStyleSheet("background-color: grey;")

        self.button_matrix = []
        self.matrix = np.ones(ALL, dtype=int)

        self.restart_button = QPushButton("Restart?")
        self.restart_button.setEnabled(False)
        self.restart_button.clicked.connect(self.restart)

        self.turn_count = 0
        self.color = [
            "background-color: #282828; padding: 20px;",
            "background-color: #a0a0a4; padding: 20px;",
        ]

        wg = QWidget()

        self.win_label = QLabel()
        self.win_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.turn_count_label = QLabel()
        self.turn_count_label.setAlignment(Qt.AlignmentFlag.AlignRight)

        hl = QHBoxLayout()
        hl.addWidget(self.win_label)
        hl.addWidget(self.turn_count_label)

        vl = QVBoxLayout()
        vl.addLayout(self.set_field())
        vl.addLayout(hl)
        vl.addWidget(self.restart_button)

        wg.setLayout(vl)
        self.setCentralWidget(wg)

        self.restart()

    def set_field(self):
        gl = QGridLayout()

        gl.setSpacing(0)

        for i in range(HEIGHT):
            for j in range(WIDTH):
                button = QPushButton()

                button.setFixedSize(50, 50)
                button.setStyleSheet(self.color[1])
                button.pressed.connect(self.clicked)

                gl.addWidget(button, i, j)
                self.button_matrix.append(button)

        gl.setColumnStretch(0, 1)
        gl.setColumnStretch(gl.columnCount(), 1)

        return gl

    def clicked(self):
        self.turn_count += 1
        self.turn_count_label.setText("Turns: " + str(self.turn_count))

        idx = self.button_matrix.index(self.sender())

        self.switch(idx)

        if self.matrix.sum() == ALL:
            self.win()

    def switch(self, idx):
        for i in range(idx % WIDTH, ALL, WIDTH):
            self.matrix[i] = (self.matrix[i] + 1) % 2
            self.button_matrix[i].setStyleSheet(self.color[self.matrix[i]])

        for i in range((idx // WIDTH) * WIDTH, (idx // WIDTH + 1) * WIDTH):
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

        for i in np.random.randint(0, ALL, 100):
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
