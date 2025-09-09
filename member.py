import sys
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.uic import loadUi
from PyQt5.QtCore import QDate
import pymysql

class member(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        loadUi('form_member.ui',self)
        self.setWindowTitle('Form Member')
        self.tampilDataMember()
        self.btnAdd.clicked.connect(self.entriDataMember)
        self.tabelMember.itemSelectionChanged.connect(self.tampilDataTerpilih)
        self.btnPerbarui.clicked.connect(self.perbaruiDataMember)
        self.btnHapus.clicked.connect(self.hapusDataMember)

    def tampilPesan(self,pesan):
        msgbox=QMessageBox()
        msgbox.setIcon(QMessageBox.Information)
        msgbox.setWindowTitle('Form Member')
        msgbox.setText(pesan)
        msgbox.exec()

    def tampilDataMember(self):
        #koneksi
        conn=pymysql.connect(host="localhost",user="root",password="",database="perpustakaan_db")

        #menampilkan tabel member
        query="SELECT * FROM tbl_member"
        cursor=conn.cursor()
        cursor.execute(query)
        data_member=cursor.fetchall()

        #data member
        n_member=len(data_member)
        self.tabelMember.setRowCount(n_member)
        baris=0

        for x in data_member:
           self.tabelMember.setItem(baris,0,QTableWidgetItem(str(x[0])))
           self.tabelMember.setItem(baris,1,QTableWidgetItem(x[1]))
           self.tabelMember.setItem(baris,2,QTableWidgetItem(str(x[2])))
           baris=baris+1

    def entriDataMember(self):
        #ambildataMember
        nama=self.editNama.text()
        tanggalJoin=self.editTanggalJoin.text()

        #conn
        conn=pymysql.connect(host="localhost",user="root",password="",database="perpustakaan_db")

        #memasukan data ke tabel member
        query="INSERT INTO tbl_member(nama,tanggal_join) VALUES(%s, %s)"
        data=(nama,tanggalJoin)
        cursor=conn.cursor()
        cursor.execute(query,data)
        conn.commit()

        #tutup koneksi
        conn.close()

        #tampil pesan
        self.tampilPesan('input success')

        #menampilkan data Buku pada tabel
        self.tampilDataMember()

        #reset
        self.resetText()

    def resetText(self):
        self.editNama.clear()
        self.editTanggalJoin.clear()

    def tampilDataTerpilih(self):
        #menyimpan detail data member yang dipilih
        data=self.tabelMember.selectedItems()
        idMember=data[0].text()
        nama=data[1].text()
        #tanggalJoin=data[2].date().toString("yyyy-mm-dd")
        tanggalJoin=QDate.fromString(data[2].text(),"yyyy-MM-dd")
        
        #self.tampilPesan(' success')
        #menampilkan detail member pada line edit
        self.editID.setText(idMember)
        self.editNama.setText(nama)
        self.editTanggalJoin.setDate(tanggalJoin)

    def perbaruiDataMember(self):
        #menyimpan data pada kotak text
        idMember=self.editID.displayText()
        nama=self.editNama.displayText()
        tanggalJoin=self.editTanggalJoin.date().toString("yyyy-MM-dd")

        #membuat koneksi
        conn=pymysql.connect(host="localhost",user="root",password="",database="perpustakaan_db")

        #perbarui data member
        query="UPDATE tbl_member SET nama=%s, tanggal_join=%s WHERE id_member=%s"
        data=(nama,tanggalJoin,int(idMember))
        cursor=conn.cursor()
        cursor.execute(query,data)
        conn.commit()

        #menutup koneksi
        conn.close()

        #menampilkan pesan
        self.tampilPesan('data Berhasil Diubah')

        #tampilkan data member
        self.tampilDataMember()

    def tampilJendelaKonfirmasi(self, pesan):
        msgbox=QMessageBox()
        msgbox.setIcon(QMessageBox.Question)
        msgbox.setWindowTitle('Konfirmasi')
        msgbox.setText(pesan)
        msgbox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        return msgbox.exec()

    def hapusDataMember(self):
        #simpan data id member
        idMember=self.editID.text()

        jendela_konfirmasi=self.tampilJendelaKonfirmasi('apakah anda yakin ingin menghapus data ini?')

        if jendela_konfirmasi==QMessageBox.Ok:
            #koneksi
            conn=pymysql.connect(host="localhost",user="root",password="",database="perpustakaan_db")

            #hapus Data Member
            query="DELETE FROM tbl_member WHERE id_member=%s"
            data=(int(idMember),)
            cursor=conn.cursor()
            cursor.execute(query,data)
            conn.commit()

            #tutup koneksi
            conn.close()

            #tampil pesan
            self.tampilPesan('data berhasil dihapus')

            #tampil data buku
            self.tampilDataMember()

if __name__=="__main__":
    app=QApplication(sys.argv)
    form=member()
    form.show()
    sys.exit(app.exec())
        

    
