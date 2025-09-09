import sys
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.uic import loadUi
from buku import buku
from member import member
from PyQt5.QtCore import QDate
import pymysql

class menu(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        loadUi('menu.ui',self)
        self.setWindowTitle('Form Menu')
        self.btnBuku.clicked.connect(self.bukaFormBuku)
        self.btnMember.clicked.connect(self.bukaFormMember)

    def bukaFormMember(self):
        self.form_member=member()
        self.form_member.show()
    
    def bukaFormBuku(self):
        self.form_buku=buku()
        self.form_buku.show()

if __name__=="__main__":
    app=QApplication(sys.argv)
    form=menu()
    form.show()
    sys.exit(app.exec())
       
