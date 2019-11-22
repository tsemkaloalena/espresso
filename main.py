import sys
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QListView, QListWidget, QTableWidgetItem
from PyQt5 import QtCore, QtGui, QtWidgets


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.loadUi('films.db')
        self.setupUi()

    def loadUi(self, dbname):
        con = sqlite3.connect(dbname)
        cur = con.cursor()

        year = cur.execute("""SELECT DISTINCT year FROM Films""").fetchall()
        years = list(map(lambda x: str(x[0]), year))

        dur = cur.execute("""SELECT DISTINCT duration FROM Films""").fetchall()
        duration = list(map(lambda x: str(x[0]), dur))

        con.close()
        self.comboBox.addItems(['0'])
        self.comboBox.addItems(years)
        self.comboBox_2.addItems(['0'])
        self.comboBox_2.addItems(duration)

    def setupUi(self):
        self.year = '0'
        self.duration = '0'
        self.comboBox.activated[str].connect(self.get_year)
        self.comboBox_2.activated[str].connect(self.get_duration)
        self.pushButton.clicked.connect(self.load_params)

    def get_year(self):
        self.year = self.comboBox.currentText()

    def get_duration(self):
        self.duration = self.comboBox_2.currentText()

    def load_params(self):
        self.request = ''
        if self.lineEdit.text():
            self.request += f'title = "{self.lineEdit.text()}"'
            if self.year != '0':
                self.request += f' and year = {self.year}'
                if self.duration != '0':
                    self.request += f' and duration = {self.duration}'
            else:
                if self.duration != '0':
                    self.request += f' and duration = {self.duration}'
        else:
            if self.year != '0':
                self.request += f' year = {self.year}'
                if self.duration != '0':
                    self.request += f' and duration = {self.duration}'
            else:
                if self.duration != '0':
                    self.request += f' duration = {self.duration}'
        filter = "SELECT * FROM Films WHERE " + self.request

        self.search(filter)

    def search(self, filter):
        con = sqlite3.connect('films.db')
        cur = con.cursor()
        result = cur.execute(filter).fetchall()[0]
        title = ['id', 'title', 'year', 'genre', 'duration']

        self.tableWidget.setColumnCount(len(title))
        self.tableWidget.setHorizontalHeaderLabels(title)

        self.tableWidget.setRowCount(1)
        for i, elem in enumerate(result):
            self.tableWidget.setItem(0, i, QTableWidgetItem(str(elem)))

        self.tableWidget.resizeColumnsToContents()






app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())