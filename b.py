import sys

from PyQt5.QtCore import QBasicTimer
from PyQt5.QtWidgets import QApplication, QFrame, QPushButton, QHBoxLayout


class MainWin(QFrame):

    def __init__(self):
        super().__init__()
        btn = QPushButton("ok")
        layout = QHBoxLayout()
        layout.addWidget(btn)
        self.setLayout(layout)
        self.timer = QBasicTimer()
        # self.timer.start(1000, self)
        btn.clicked.connect(self.counter)

    def paintEvent(self, e):
        print(e)

    def timerEvent(self, event):
        print(event)

    def counter(self):
        for i in range(1000000):
            print(i)


if __name__ == '__main__':
    app = QApplication([])
    mainwin = MainWin()
    mainwin.show()
    sys.exit(app.exec_())

