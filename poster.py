import sys
from functools import partial
from time import time

import os
from PyQt5.QtWidgets import QTreeView, QTableWidget, \
    QHBoxLayout, QWidget, QAction, QMainWindow, \
    QTabWidget, QSplitter, QApplication, QPushButton, \
    QTableWidgetItem, QTableView, QVBoxLayout, QTextEdit, QLineEdit, \
    QGridLayout, QLabel, QListWidget, QListView
from PyQt5.QtCore import Qt, QModelIndex, pyqtSlot, pyqtSignal
from PyQt5.QtGui import QStandardItem, QStandardItemModel, QGuiApplication
from icon import icon_font


class MainWin(QMainWindow):
    items = QStandardItemModel()
    signal = pyqtSignal(str)

    def __init__(self):
        super(QMainWindow, self).__init__()
        self.setWindowTitle("POSTER")


        a = os.listdir('./workspace')
        for i in a:
            item = QStandardItem("%s" % i)
            self.items.appendRow(item)
        nav = QListView()
        nav.setModel(self.items)

        self.workspace = WorkSpace()
        nav.clicked.connect(self.emit_openfile)

        right_layout = QVBoxLayout()

        splitter = QSplitter()
        splitter.addWidget(nav)
        splitter.addWidget(self.workspace)
        splitter.setStretchFactor(1, 1)
        splitter.setSizes([250, 550])

        self.setCentralWidget(splitter)

    def emit_openfile(self, index):
        self.signal.connect(self.workspace.open_file)
        a = self.items.itemFromIndex(index)
        self.signal.emit(a.text())


class WorkSpace(QWidget):

    def __init__(self):
        super(QWidget, self).__init__()
        label = QLabel('11212')
        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)

    @pyqtSlot(str)
    def open_file(self, filename):
        print(filename)

        with open('./workspace/' + filename, 'r+', encoding='utf-8') as fp:
            for i in fp.readlines():
                print(i)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    import sys
    sys.excepthook = except_hook
    app = QApplication(sys.argv)
    main_win = MainWin()
    main_win.resize(900, 600)
    main_win.show()
    sys.exit(app.exec_())
