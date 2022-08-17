import sys
import numpy as np
from PyQt6.QtWidgets import (
    QMainWindow, QPushButton, QApplication, QLabel,
    QGridLayout, QWidget, QButtonGroup, QVBoxLayout,
    QLineEdit, QHBoxLayout, QDialog
)
from PyQt6.QtCore import Qt
from field import Field
from skin import get_color


class MyDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.nickname = None

        self.blank = QLineEdit()

        self.btn = QPushButton("Submit")
        self.btn.clicked.connect(self.submit)

        vl = QVBoxLayout()
        vl.addWidget(QLabel("Nickname:"))
        hl = QHBoxLayout()
        hl.addWidget(self.blank)
        hl.addWidget(self.btn)
        vl.addLayout(hl)

        self.layout = vl
        self.setLayout(self.layout)

    def submit(self):
        if self.blank.text():
            self.nickname = self.blank.text()
            self.accept()


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.field = Field()
        self.skin = "Desert"

        self.nickname = None
        self.write_nickname()

        hl = QVBoxLayout()

        self.restart = QPushButton()
        self.restart.setText("Restart")
        self.restart.clicked.connect(self.field.field_restart)

        stats = QHBoxLayout()
        stats.addWidget(QLabel(self.nickname))
        stats.addWidget(self.field.turns_label)

        hl.addWidget(self.field)
        hl.addLayout(stats)
        hl.addWidget(self.restart)

        wg = QWidget()
        wg.setLayout(hl)
        self.setCentralWidget(wg)
        self.colorize()

    def colorize(self):
        self.setStyleSheet(get_color(self.skin)["Window"])
        self.restart.setStyleSheet(get_color(self.skin)["Restart"])
        self.field.skin = self.skin
        self.field.field_colorize()

    def write_nickname(self):
        dialog = MyDialog()
        if dialog.exec():
            self.nickname = dialog.nickname
        else:
            quit(0)


app = QApplication(sys.argv)
w = MyWindow()
w.show()
app.exec()
