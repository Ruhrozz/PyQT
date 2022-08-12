import sys
import numpy as np
from PyQt6.QtWidgets import (
    QMainWindow, QApplication, QPushButton,
    QGridLayout, QWidget, QVBoxLayout, QLineEdit, QLabel,
)
from PyQt6.QtCore import Qt


HEIGHT = 5
WIDTH = 5

ALL = HEIGHT*WIDTH


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # self.setFixedSize(200, 200)

        self.button_matrix = []
        self.matrix = np.ones(ALL, dtype=int)
        self.color = [
            "background-color: #ff0f00; padding: 20px;",
            "background-color: #008000; padding: 20px;",
        ]

        wg = QWidget()

        hl = QVBoxLayout()
        gl = self.set_field()
        hl.addLayout(gl)
        hl.addWidget(QLabel('QQQ'))
        hl.setAlignment(Qt.AlignmentFlag.AlignRight)

        wg.setLayout(hl)
        self.setCentralWidget(wg)

        for i in np.random.randint(0, ALL, 100):
            self.switch(i)

    def set_field(self):
        gl = QGridLayout()

        gl.setSpacing(0)

        for i in range(HEIGHT):
            for j in range(WIDTH):
                button = QPushButton()

                button.setFixedSize(30, 30)
                button.setStyleSheet(self.color[1])
                button.pressed.connect(self.clicked)

                gl.addWidget(button, i, j)
                self.button_matrix.append(button)

        gl.setAlignment(Qt.AlignmentFlag.AlignRight)
        gl.setColumnStretch(gl.columnCount(), 1)
        gl.setRowStretch(gl.rowCount(), 1)

        return gl

    def clicked(self):
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
        print("win")


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()
