import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QSize

from folders_based_tab_widget import FoldersBasedTabWidget
from global_declarations import General

class HelloWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(General.WINDOW_WIDTH.value, General.WINDOW_HEIGHT.value))
        self.setWindowTitle("DMC Control Unit")
        self.setWindowFilePath('')

        tabs = FoldersBasedTabWidget(tabs_folder='tabs', parent=self)
        self.setCentralWidget(tabs)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = HelloWindow()
    mainWin.show()
    sys.exit(app.exec_())