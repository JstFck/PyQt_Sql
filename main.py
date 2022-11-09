import sys


from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel, QTextEdit


class Open(QWidget):
    def __init__(self):
        super(Open, self).__init__()


class Create(QWidget):
    def __init__(self):
        super(Create, self).__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('Добавление базы данных')

        self.label = QLabel('Введите имя базы данных', self)
        self.move(0, 0)

        self.text_edit = QTextEdit(self)
        self.text_edit.move(0, 30)


class Edit(QWidget):
    def __init__(self):
        super(Edit, self).__init__()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('main')
        self.setGeometry(300, 300, 50, 130)

        self.open_btn = QPushButton('Открыть', self)
        self.open_btn.move(0, 0)
        self.create_btn = QPushButton('Создать', self)
        self.create_btn.move(0, 30)
        self.edit_btn = QPushButton('Редактировать', self)
        self.edit_btn.move(0, 60)
        self.open_btn.clicked.connect(self.show_window_open)
        self.create_btn.clicked.connect(self.show_window_create)
        self.edit_btn.clicked.connect(self.show_window_edit)

        global db_dict
        db_dict = {}

    def show_window_open(self):
        self.open = Open()
        self.open.show()

    def show_window_create(self):
        self.create = Create()
        self.create.show()

    def show_window_edit(self):
        self.edit = Edit()
        self.edit.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
