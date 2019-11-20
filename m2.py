import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QStandardItem, QStandardItemModel, QIcon
from icon import IconicFont

class StandardItemModel(QStandardItemModel):
    ExpandableRole = QtCore.Qt.UserRole + 500

    def hasChildren(self, index):
        if self.data(index, StandardItemModel.ExpandableRole):
            return True
        return super(StandardItemModel, self).hasChildren(index)

class Window(QtWidgets.QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.mytreeview = QtWidgets.QTreeView()
        self.model = StandardItemModel(self.mytreeview)
        self.mytreeview.setModel(self.model)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.mytreeview)
        self.mytreeview.expanded.connect(self.update_model)
        self.initialise_model()

    def initialise_model(self):
        self.model.clear()
        for file_name_entry in fileobject:
            item = QStandardItem(file_name_entry.strip())
            item.setData(True, StandardItemModel.ExpandableRole)
            item.setData("this is a parent", QtCore.Qt.ToolTipRole)
            ic = IconicFont().icon(
                'server',
                'cancel',
                options=[
                    {'scale_factor': 0.9},
                    {'color': 'red'}
                ]
            )
            item.setIcon(ic)
            self.model.appendRow(item)

    def update_model(self, index):
        parent_item = self.model.itemFromIndex(index)
        if not parent_item.rowCount():
            for child_name_entry in parent_text_fileobject:
                child_item = QStandardItem(child_name_entry.strip())
                child_item.setData("this is a child", QtCore.Qt.ToolTipRole)
                parent_item.appendRow(child_item)

# dummy test data
fileobject = 'parent1 parent2 parent3'.split()
parent_text_fileobject = 'child_a child_b child_c'.split()

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())