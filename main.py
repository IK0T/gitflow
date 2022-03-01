import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.con = sqlite3.connect("coffee.sqlite")
        self.cur = self.con.cursor()
        self.ok_button.clicked.connect(self.ok)
        self.fill_combobox()

    def ok(self):
        self.label_degree.setText('Степень обжарки:')
        self.label_status.setText('Вид:')
        self.label_taste.setText('Вкус:')
        self.label_price.setText('Цена:')
        self.label_volume.setText('Объем стакана:')
        command = '''SELECT * FROM coffie_variants WHERE sort_name = ?'''
        res = self.cur.execute(command, (self.comboBox.currentText(),)).fetchone()
        degree = self.cur.execute(f'''SELECT degree FROM degree_of_roasting WHERE
         id = {res[2]}''').fetchone()
        status = self.cur.execute(f'''SELECT status_name FROM status WHERE
         id = {res[3]}''').fetchone()
        self.label_degree.setText(f'{self.label_degree.text()} {degree[0]}')
        self.label_status.setText(f'{self.label_status.text()} {status[0]}')
        self.label_taste.setText(f'{self.label_taste.text()} {res[4]}')
        self.label_price.setText(f'{self.label_price.text()} {res[5]} руб.')
        self.label_volume.setText(f'{self.label_volume.text()} {res[6]} мл')

    def fill_combobox(self):
        command = '''SELECT sort_name FROM coffie_variants'''
        res = self.cur.execute(command).fetchall()
        lst = [elem[0] for elem in res]
        self.comboBox.addItems(lst)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())