import sys


from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton


class Window2(QWidget):
    def __init__(self):
        super(Window2, self).__init__()
        self.setWindowTitle('Window2')


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('main')
        self.setGeometry(300, 300, 300, 300)

        self.btn = QPushButton('Открыть', self)
        self.btn.clicked.connect(self.show_window_2)

    def show_window_2(self):
        self.w2 = Window2()
        self.w2.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
