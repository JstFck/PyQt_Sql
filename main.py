import sqlite3
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel, QLineEdit, QFileDialog, \
    QInputDialog, QTableWidget, QComboBox, QTableWidgetItem, QTextEdit, QVBoxLayout

global db_dict
db_dict: dict


class Open(QWidget):
    def __init__(self):
        super(Open, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Работа с базой данных')
        self.setGeometry(300, 300, 700, 550)

        self.db_choice = QComboBox(self)
        self.db_choice.addItems(db_dict)
        self.db_choice.move(10, 10)
        self.db_choice.resize(150, 20)

        self.label = QLabel('                                                                                   ', self)
        self.label.move(255, 13)

        self.table = QTableWidget(self)
        self.table.setColumnCount(5)
        self.table.setRowCount(0)
        self.table.move(10, 160)
        self.table.resize(615, 315)

        self.request_text = QTextEdit(self)
        self.request_text.move(10, 40)
        self.request_text.resize(300, 100)

        self.start_btn = QPushButton('Загрузить', self)
        self.start_btn.move(170, 10)
        self.start_btn.resize(75, 20)
        self.start_btn.clicked.connect(self.start_db)
        self.back_btn = QPushButton('Назад', self)
        self.back_btn.move(620, 520)
        self.back_btn.clicked.connect(self.back_to_main_window)

        self.label.setText('Выберите файл')

    def back_to_main_window(self):
        sql_app.show()
        Open.close(self)

    def start_db(self):
        con = sqlite3.connect(db_dict[self.db_choice.currentText()])
        cur = con.cursor()

        res = cur.execute(self.request_text.toPlainText()).fetchall()

        self.table.clear()
        self.table.setRowCount(0)

        for i, row in enumerate(res):
            self.table.setRowCount(self.table.rowCount() + 1)
            for j, elem in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(elem)))
        if self.request_text.toPlainText() == '' or self.request_text.toPlainText() is None:
            self.label.setText('Введите запрос')
        else:
            self.label.setText('База данных загружена')


class Create(QWidget):
    def __init__(self):
        super(Create, self).__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('Добавление базы данных')

        self.name_label = QLabel('Введите имя базы данных', self)
        self.name_label.move(10, 10)
        self.file_label = QLabel('Выберать файл', self)
        self.file_label.move(10, 60)
        self.save_label = QLabel('                                                                              ', self)
        self.save_label.move(10, 110)

        self.db_btn = QPushButton('Выберите файл', self)
        self.db_btn.move(10, 80)
        self.db_btn.clicked.connect(self.choice_db)
        self.back_btn = QPushButton('Назад', self)
        self.back_btn.move(220, 270)
        self.back_btn.clicked.connect(self.back_to_main_window)

        count_db = 0
        standard_db_name = 'data_base'

        if standard_db_name in db_dict.keys():
            count_db += 1
            standard_db_name += f' ({count_db})'

        self.name_db = QLineEdit(standard_db_name, self)
        self.name_db.move(10, 30)

    def back_to_main_window(self):
        sql_app.show()
        Create.close(self)

        count_db = 0
        standard_db_name = 'data_base'

        if standard_db_name in db_dict.keys():
            count_db += 1
            standard_db_name += f' ({count_db})'

        self.name_db = QLineEdit(standard_db_name, self)
        self.name_db.move(10, 30)

    def choice_db(self):
        self.file_db = QFileDialog.getOpenFileName(self, 'Выберать базу данных', '',
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

        self.save_label = QLabel('                                                                              ', self)
        self.save_label.move(10, 130)

        self.db = QComboBox(self)
        self.db.move(10, 10)
        self.db.resize(150, 20)
        self.db.addItems(db_dict.keys())

        self.del_btn = QPushButton('Удалить', self)
        self.del_btn.move(10, 40)
        self.del_btn.resize(150, 20)
        self.edit_name_btn = QPushButton('Изменить имя', self)
        self.edit_name_btn.move(10, 70)
        self.edit_name_btn.resize(150, 20)
        self.edit_file_btn = QPushButton('Изменить файл', self)
        self.edit_file_btn.move(10, 100)
        self.edit_file_btn.resize(150, 20)
        self.back_btn = QPushButton('Назад', self)
        self.back_btn.move(220, 270)

        self.del_btn.clicked.connect(self.del_db)
        self.edit_name_btn.clicked.connect(self.edit_name)
        self.edit_file_btn.clicked.connect(self.edit_file)
        self.back_btn.clicked.connect(self.back_to_main_window)

    def back_to_main_window(self):
        sql_app.show()
        Edit.close(self)

    def del_db(self):
        del db_dict[self.db.currentText()]
        self.save_label.setText('Файл удален')

    def edit_name(self):
        self.new_key_db = QInputDialog.getText(self, 'Редактирование', 'Введите новое имя')
        db_dict[self.new_key_db[0]] = db_dict.pop(self.db.currentText())
        self.save_label.setText('Имя изменено')

    def edit_file(self):
        db_dict[self.db.currentText()] = QFileDialog.getOpenFileName(self, 'Выберать базу данных', '',
                                                                     'Файл (*.sqlite);;Файл (*.sql);;Все файлы (*)')[0]
        self.save_label.setText('Файл изменен')


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('main')
        self.setGeometry(300, 300, 200, 130)

        self.open_btn = QPushButton('Открыть', self)
        self.open_btn.move(10, 10)
        self.open_btn.clicked.connect(self.show_window_open)
        self.create_btn = QPushButton('Создать', self)
        self.create_btn.move(10, 40)
        self.create_btn.clicked.connect(self.show_window_create)
        self.edit_btn = QPushButton('Редактировать', self)
        self.edit_btn.move(10, 70)
        self.edit_btn.clicked.connect(self.show_window_edit)

        layout = QVBoxLayout(self)
        layout.addWidget(self.open_btn)
        layout.addWidget(self.create_btn)
        layout.addWidget(self.edit_btn)
        container = QWidget(self)
        container.setLayout(layout)

        self.setCentralWidget(container)

        global db_dict
        db_dict = {}

    def show_window_open(self):
        self.open = Open()
        self.open.show()
        sql_app.close()

    def show_window_create(self):
        self.create = Create()
        self.create.show()
        sql_app.close()

    def show_window_edit(self):
        self.edit = Edit()
        self.edit.show()
        sql_app.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sql_app = MainWindow()
    sql_app.show()
    sys.exit(app.exec_())
