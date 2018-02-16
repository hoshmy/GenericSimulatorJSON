import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QSize

from folders_based_tab_widget import FoldersBasedTabWidget
from global_declarations import General


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(General.WINDOW_WIDTH.value, General.WINDOW_HEIGHT.value))
        self.setWindowTitle("DMC Control Unit")
        self.setWindowFilePath('')

        tabs = FoldersBasedTabWidget(tabs_folder='tabs', parent=self)
        self.setCentralWidget(tabs)
        self._location_on_the_screen()

    def _location_on_the_screen(self):
        ag = QDesktopWidget().availableGeometry()
        sg = QDesktopWidget().screenGeometry()

        widget = self.geometry()
        x = 0
        y = ag.height() - General.WINDOW_HEIGHT.value
        self.move(x, y)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())