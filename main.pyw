import json
import sys
from test import run_tests
import numpy as np
from PyQt6.QtWidgets import (
    QMainWindow, QApplication, QPushButton, QHBoxLayout, QCheckBox,
    QGridLayout, QWidget, QVBoxLayout, QLineEdit, QLabel,
)
from PyQt6.QtCore import Qt


def give_title(turns):
    titles = [
        "TILES DESTRUCTOR",
        "very good, dude",
        "not bad player",
        "bruh...",
        "..noobie?",
        "the worst noob I've ever seen...",
    ]
    return "You are " + titles[min(turns // 7, 5)]


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        run_tests()

        with open("config.json", "r") as file:
            self.cfg = json.load(file)

        self.width, self.height = self.cfg["Levels"]["Normal"]
        self.square = self.width * self.height
        self.diffs = [name for name in self.cfg["Levels"]]

        self.levels = []
        self.button_matrix = []
        self.matrix = np.ones(self.square, dtype=int)

        self.restart_button = QPushButton("Restart?")
        self.restart_button.clicked.connect(self.restart)

        self.setStyleSheet("background-color: grey;")
        self.color = [
            "background-color: #282828; padding: 20px;",
            "background-color: #a0a0a4; padding: 20px;",
        ]

        self.win_label = QLabel()
        self.win_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.turn_count = 0
        self.turn_count_label = QLabel()
        self.turn_count_label.setAlignment(Qt.AlignmentFlag.AlignRight)

        hl = QHBoxLayout()
        hl.addWidget(self.win_label)
        hl.addWidget(self.turn_count_label)

        self.gl = QGridLayout()
        self.gl.addLayout(self.set_field(), 0, 0)
        self.gl.addLayout(hl, 1, 0)
        self.gl.addWidget(self.restart_button, 2, 0)
        self.gl.addLayout(self.set_levels(), 0, 1)

        wg = QWidget()
        wg.setLayout(self.gl)
        self.setCentralWidget(wg)

        self.restart()

    def set_levels(self):
        vl = QVBoxLayout()

        for i, name in enumerate(self.diffs, 0):
            box = QCheckBox(name)
            if name == "Normal":
                box.setChecked(True)
            box.clicked.connect(self.levels_clicked)
            vl.addWidget(box)
            self.levels.append(box)

        return vl

    def set_field(self):
        gl = QGridLayout()
        gl.setSpacing(0)

        for y in range(self.height):
            for x in range(self.width):
                button = QPushButton()

                button.setFixedSize(50, 50)
                button.setStyleSheet(self.color[1])
                button.pressed.connect(self.field_clicked)

                gl.addWidget(button, x, y)
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

        self.width, self.height = self.cfg["Levels"][self.diffs[idx]]
        self.square = self.width * self.height

        for button in self.button_matrix:
            button.setParent(None)

        self.button_matrix = []
        self.matrix = np.ones(self.square, dtype=int)

        self.gl.addLayout(self.set_field(), 0, 0)
        self.restart()
        self.centralize()

    def centralize(self):
        QApplication.instance().processEvents()
        self.adjustSize()

        frame_geo = self.frameGeometry()
        screen = self.window().windowHandle().screen()
        center_loc = screen.geometry().center()
        frame_geo.moveCenter(center_loc)
        self.move(frame_geo.topLeft())

    def field_clicked(self):
        self.turn_count += 1
        self.turn_count_label.setText("Turns: " + str(self.turn_count))

        idx = self.button_matrix.index(self.sender())

        self.switch(idx)

        if self.matrix.sum() == self.square:
            self.win()

    def switch(self, idx):
        for i in range(idx % self.width, self.square, self.width):
            self.matrix[i] = (self.matrix[i] + 1) % 2
            self.button_matrix[i].setStyleSheet(self.color[self.matrix[i]])

        for i in range((idx // self.width) * self.width, (idx // self.width + 1) * self.width):
            if i == idx:
                continue
            self.matrix[i] = (self.matrix[i] + 1) % 2
            self.button_matrix[i].setStyleSheet(self.color[self.matrix[i]])

    def win(self):
        for button in self.button_matrix:
            button.setEnabled(False)
        self.win_label.setText("You win!!! \n" + give_title(self.turn_count))

    def restart(self):
        how_many = np.random.randint(self.square // 2, self.square)

        while True:
            for i in np.random.randint(0, self.square, how_many):
                self.switch(i)

            if self.matrix.sum() != self.square:
                break

        for button in self.button_matrix:
            button.setEnabled(True)

        self.win_label.setText("Turn all Gray tiles to White")
        self.turn_count_label.setText("Turns: 0")
        self.turn_count = 0



app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()
