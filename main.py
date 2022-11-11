import sys
import sqlite3

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel, QLineEdit, QFileDialog, \
    QInputDialog, QTableWidget, QComboBox, QVBoxLayout


global db_dict
db_dict: dict


class Open(QWidget):
    def __init__(self):
        super(Open, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Работа с базой данных')
        self.setGeometry(300, 300, 635, 335)

        self.db_choice = QInputDialog.getItem(self, 'Работа с базой данных', 'Выберите базу данных',
                                                    db_dict.keys(), 1, False)
        print(self.db_choice[0])
        self.con = sqlite3.connect(self.db_choice[0])
        self.cur = self.con.cursor()
        self.table = QTableWidget(self)
        self.table.setColumnCount(5)
        self.table.setRowCount(0)

        res = self.cur.execute("""SELECT * FROM Films""").fetchall()
        print(res)
        for i, row in enumerate(res):
            self.table.setRowCount(self.table.rowCount() + 1)
            for j, elem in enumerate(row):
                self.table.setItem(i, j, QTableWidget(str(elem)))

    # Доделать класс (проблема с бд в execute())


class Create(QWidget):
    def __init__(self):
        super(Create, self).__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('Добавление базы данных')

        self.name_label = QLabel('Введите имя базы данных', self)
        self.name_label.move(10, 10)
        self.file_label = QLabel('Выберите файл', self)
        self.file_label.move(10, 60)
        self.save_label = QLabel('                               ', self)
        self.save_label.move(10, 130)

        self.db_btn = QPushButton('Выберите файл', self)
        self.db_btn.move(10, 90)
        self.db_btn.clicked.connect(self.choice_db)

        self.name_db = QLineEdit(self)
        self.name_db.move(10, 30)

    def choice_db(self):
        self.file_db = QFileDialog.getOpenFileName(self, 'Выберите базу данных', '',
                                                   'Файл (*.sqlite);;Файл (*.sql);;Все файлы (*)')
        db_dict[self.name_db.text()] = self.file_db[0]
        self.save_label.setText('Сохранено')


class Edit(QWidget):
    def __init__(self):
        super(Edit, self).__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('Редактирование')

        self.save_label = QLabel('                  ', self)
        self.save_label.move(10, 130)

        self.db = QComboBox(self)
        self.db.move(10, 10)
        self.db.resize(150, 20)
        self.db.addItems(db_dict.keys())

        self.del_btn = QPushButton('Удалить', self)
        self.del_btn.move(10, 40)
        self.del_btn.resize(150, 20)
        self.del_btn.clicked.connect(self.del_db)
        self.edit_name_btn = QPushButton('Изменить имя', self)
        self.edit_name_btn.move(10, 70)
        self.edit_name_btn.resize(150, 20)
        self.edit_name_btn.clicked.connect(self.edit_name)
        self.edit_file_btn = QPushButton('Изменить файл', self)
        self.edit_file_btn.move(10, 100)
        self.edit_file_btn.resize(150, 20)
        self.edit_file_btn.clicked.connect(self.edit_file)

    def del_db(self):
        del db_dict[self.db.currentText()]
        self.save_label.setText('Сохранено')

    def edit_name(self):
        self.new_key_db = QInputDialog.getText(self, 'Редактирование', 'Введите новое имя')
        db_dict[self.new_key_db[0]] = db_dict.pop(self.db.currentText())
        self.save_label.setText('Сохранено')

    def edit_file(self):
        db_dict[self.db.currentText()] = QFileDialog.getOpenFileName(self, 'Выберите базу данных', '',
                                                                     'Файл (*.sqlite);;Файл (*.sql);;Все файлы (*)')[0]
        self.save_label.setText('Сохранено')


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('main')
        self.setGeometry(300, 300, 200, 130)

        self.open_btn = QPushButton('Открыть', self)
        self.open_btn.move(0, 0)
        self.open_btn.clicked.connect(self.show_window_open)
        self.create_btn = QPushButton('Создать', self)
        self.create_btn.move(0, 30)
        self.create_btn.clicked.connect(self.show_window_create)
        self.edit_btn = QPushButton('Редактировать', self)
        self.edit_btn.move(0, 60)
        self.edit_btn.clicked.connect(self.show_window_edit)

        global db_dict
        db_dict = {}

        layout = QVBoxLayout(self)
        layout.addWidget(self.open_btn)
        layout.addWidget(self.create_btn)
        layout.addWidget(self.edit_btn)
        container = QWidget(self)
        container.setLayout(layout)

        self.setCentralWidget(container)

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
