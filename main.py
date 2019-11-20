import sys
from functools import partial
from time import time

from PyQt5.QtWidgets import QTreeView, QTableWidget, \
    QHBoxLayout, QWidget, QAction, QMainWindow, \
    QTabWidget, QSplitter, QApplication, QPushButton, QTableWidgetItem, QTableView, QVBoxLayout, QTextEdit, QLineEdit, \
    QGridLayout, QLabel
from PyQt5.QtCore import Qt, QModelIndex, pyqtSlot, pyqtSignal
from PyQt5.QtGui import QStandardItem, QStandardItemModel, QGuiApplication
from icon import icon_font

from mysql_model import MysqlModel


class DBWorkSpace(QWidget):

    DB_NAME_INDEX = 0
    TBL_NAME_INDEX = 1
    date_view_update = pyqtSignal(int)
    curr_tbl_name = ''
    curr_db_name = ''

    def __init__(self):
        # self.tbl_info_model = QStandardItemModel()
        # self.tbl_info_model.setItem(self.DB_NAME_INDEX, QStandardItem())
        # self.tbl_info_model.setItem(self.TBL_NAME_INDEX, QStandardItem())
        # self.model = MysqlModel(host='zhongdian.hanson365.com', user='root', password='Hanxiang1234')
        self.model = MysqlModel(host='127.0.0.1', user='admin', password='123456')
        super(QWidget, self).__init__()
        hbox = QHBoxLayout()

        operate_space_layout = QVBoxLayout()
        operate_space_layout.addWidget(QTextEdit())

        data_view_space = QTableView()
        data_view_space.setModel(self.model.data_model)

        self.filter_editor = QLineEdit()
        self.filter_editor.setMinimumHeight(40)
        filter_apply_btn = QPushButton("apply")
        filter_apply_btn.setMinimumHeight(40)
        filter_apply_btn.clicked.connect(partial(self.filter_click))

        filter_layout = QHBoxLayout()
        filter_layout.addWidget(self.filter_editor)
        filter_layout.addWidget(filter_apply_btn)

        # tbl_name_label = QLabel()
        # tbl_name_label
        tbl_info_tab_layout = QGridLayout()

        data_view_tab_layout = QVBoxLayout()
        data_view_tab_layout.addLayout(filter_layout)
        data_view_tab_layout.addWidget(data_view_space)

        query_splitter = QSplitter()
        query_splitter.addWidget(QTextEdit())
        query_splitter.addWidget(QTableView())
        query_view_tab_layout = QHBoxLayout()
        query_view_tab_layout.addWidget(query_splitter)

        tbl_info_tab = QWidget()
        data_view_tab = QWidget()
        query_view_tab = QWidget()
        query_view_tab.setLayout(query_view_tab_layout)

        tbl_info_tab.setLayout(tbl_info_tab_layout)
        data_view_tab.setLayout(data_view_tab_layout)

        self.operate_tab = QTabWidget()
        self.operate_tab.addTab(tbl_info_tab, 'INFO')
        self.operate_tab.addTab(data_view_tab, 'DATA')
        self.operate_tab.addTab(query_view_tab, 'QUERY')

        nav_space = QTreeView()
        nav_space.setColumnHidden(0, True)
        nav_space.setHeaderHidden(True)
        nav_space.setModel(self.model.schema_model)
        nav_space.clicked.connect(self.show_click)

        splitter = QSplitter()
        splitter.addWidget(nav_space)
        splitter.addWidget(self.operate_tab)
        splitter.setStretchFactor(1, 1)
        splitter.setSizes([250, 550])
        hbox.addWidget(splitter)
        hbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(hbox)
        self.clipboard = QGuiApplication.clipboard()
        self.clipboard.changed.connect(self.show_clipboard)
        self.setStyleSheet('''
            # QHeaderView::section {
            #     background-color:#333;
            #     color: white;
            #     border:none;
            #     border-left: 1px solid #aaa;
            #     border-bottom: 1px solid #aaa;
            # }
            # QTreeView{
            #     color: #fff;
            #     border:none;
            #     background-color: #333;
            # }
            # QTableView{
            #     border:none;
            #     color: #fff;
            #     background-color: #333;
            # }
        ''')

    def add_db(self):
        self.model.add_db()

    @pyqtSlot(QModelIndex)
    def show_click(self, index):
        selected_item = self.model.schema_model.itemFromIndex(index)
        if selected_item.parent():
            self.curr_db_name = selected_item.parent().text()
            self.curr_tbl_name = selected_item.text()
            self.model.show_table_data(self.curr_db_name, self.curr_tbl_name)
        else:
            self.curr_db_name = selected_item.text()
            self.curr_tbl_name = ''

    @pyqtSlot(bool)
    def filter_click(self, _):
        print(self.filter_editor.text())
        self.model.show_table_data(self.curr_db_name, self.curr_tbl_name, self.filter_editor.text())

    def show_clipboard(self):
        originalText = self.clipboard.text()
        print((originalText,))


class MainWin(QMainWindow):

    def __init__(self):
        super(QMainWindow, self).__init__()
        self.setWindowTitle("title")
        self.tab = QTabWidget()
        self.tab.setTabsClosable(True)
        self.setCentralWidget(self.tab)
        fa5_icon = icon_font.icon('flag', color='#f00')
        file_menu = self.menuBar().addMenu('&File')
        open_action = QAction(fa5_icon, '&Open', self)
        open_action.triggered.connect(self.open_new)
        file_menu.addAction(open_action)
        self.tab.tabCloseRequested.connect(self.close_handler)

    def close_handler(self, index):
        print(index)
        self.tab.widget(index).deleteLater()

    def open_new(self):
        wp = DBWorkSpace()
        icon = icon_font.icon('server')
        index = self.tab.addTab(wp, str(time()))
        self.tab.setTabIcon(index, icon)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    import sys
    sys.excepthook = except_hook
    app = QApplication(sys.argv)
    main_win = MainWin()
    # main_win.setStyle(QStyleFactory.create("macintosh"))
    main_win.resize(900, 600)
    # main_win.showMaximized()
    main_win.show()
    # app.setStyleSheet('''
    # # QTabBar::tab {
    # #     height: 40px;
    # #     min-width: 100px;
    # #     padding-left: 20px;
    # #     border-top-left-radius: 50%;
    # #     border: 1px solid #C4C4C3;
    # #     border-top-right-radius: 50%;
    # #     border-bottom: 1px solid #fff;
    # # }
    # # QTabBar::tab::selected {
    # #     background-color: #fff;
    # # }
    #
    # ''')
    sys.exit(app.exec_())
