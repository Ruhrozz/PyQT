from PyQt6.QtWidgets import (
    QPushButton, QLabel, QVBoxLayout,
    QLineEdit, QHBoxLayout, QDialog
)


class WIYNDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("What is your name?")
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

    @staticmethod
    def write_nickname():
        dialog = WIYNDialog()
        if dialog.exec():
            return dialog.nickname
        else:
            quit(0)
