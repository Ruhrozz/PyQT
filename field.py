import numpy as np
from PyQt6.QtWidgets import QPushButton, QGridLayout, QWidget, QButtonGroup, QLabel
from PyQt6.QtCore import Qt
from skin import get_color


class Field(QWidget):
    def __init__(self):
        super(Field, self).__init__()

        self.layout = QGridLayout()
        self.button_group = QButtonGroup()
        self.status = np.zeros(25, dtype=bool)
        self.field_size = (5, 5)
        self.turns_count = 0
        self.turns_label = QLabel("Turns: " + str(self.turns_count))
        self.turns_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.skin = "Standard"

        self.field_create()
        self.field_restart()
        self.setLayout(self.layout)

    def field_create(self):
        width, height = self.field_size
        bg = self.button_group
        gl = self.layout

        i = 0
        for x in range(height):
            for y in range(width):
                btn = QPushButton()
                btn.setFixedSize(50, 50)
                gl.addWidget(btn, x, y)
                bg.addButton(btn, i)
                i += 1

        bg.buttonClicked.connect(self.field_clicked)

        gl.setSpacing(0)
        gl.setRowStretch(gl.rowCount(), 1)
        gl.setColumnStretch(gl.columnCount(), 1)

        self.field_colorize()

    def field_clicked(self, button):
        btn_id = self.button_group.id(button)
        self.turns_count += 1
        self.turns_label.setText("Turns: " + str(self.turns_count))
        self.field_switch(btn_id)
        self.field_colorize()
        self.field_victory()

    def field_switch(self, btn_id):
        width, height = self.field_size
        x = btn_id % width
        y = btn_id // width * width
        self.status[x:width*height:width] = ~self.status[x:width*height:width]
        self.status[y:y + width] = ~self.status[y:y + width]
        self.status[btn_id] = ~self.status[btn_id]

    def field_colorize(self):
        color = get_color(self.skin)["Tiles"]
        bg = self.button_group
        for button in bg.buttons():
            state = self.status[bg.id(button)]
            button.setStyleSheet(color[state])

    def field_victory(self):
        if self.status.sum() == 0:
            print("You won!")
            for button in self.button_group.buttons():
                button.setEnabled(False)

    def field_restart(self):
        self.turns_count = 0
        self.turns_label.setText("Turns: " + str(self.turns_count))

        for button in self.button_group.buttons():
            button.setEnabled(True)

        square = self.field_size[0] * self.field_size[1]
        while True:
            for i in np.random.randint(0, square, np.random.randint(square, square+7)):
                self.field_switch(i)

            if self.status.sum() != 0:
                break

        self.field_colorize()
