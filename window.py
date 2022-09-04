import sys
from PyQt6.QtWidgets import (
    QMainWindow, QPushButton, QApplication, QLabel,
    QWidget, QVBoxLayout,
    QHBoxLayout,
)
from field import Field
from skin import get_color
from dialogs import WIYNDialog


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.field = Field()
        self.skin = "Standard"
        self.nickname = WIYNDialog.write_nickname()

        self.restart = QPushButton()
        self.restart.setText("Restart")
        self.restart.clicked.connect(self.field.field_restart)

        stats = QHBoxLayout()
        stats.addWidget(QLabel(self.nickname))
        stats.addWidget(self.field.turns_label)

        hl = QVBoxLayout()
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MyWindow()
    w.show()
    app.exec()
