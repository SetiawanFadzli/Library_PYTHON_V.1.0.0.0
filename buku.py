import sys
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.uic import loadUi
import pymysql

class buku(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        loadUi('form_buku.ui',self)
        self.setWindowTitle('Python GUI & MySQL')
        self.tampilDataBuku()
        self.btnAdd.clicked.connect(self.entriDataBuku)
        self.tabelBuku.itemSelectionChanged.connect(self.tampilDataTerpilih)
        self.btnPerbarui.clicked.connect(self.perbaruiDataBuku)
        self.btnHapus.clicked.connect(self.hapusDataBuku)
        
    def tampilPesan(self,pesan):
        msgbox=QMessageBox()
        msgbox.setIcon(QMessageBox.Information)
        msgbox.setWindowTitle('Python GUI & MySQL | Form Buku')
        msgbox.setText(pesan)
        msgbox.exec()

    def tampilDataBuku(self):
        #koneksi
        conn=pymysql.connect(host="localhost",user="root",password="",database="perpustakaan_db")

        #menampilkan pada tabel tbl_buku
        query="SELECT * FROM tbl_buku"
        cursor=conn.cursor()
        cursor.execute(query)
        data_buku=cursor.fetchall()

        #menampilkan data pada tabel yang terdapat di form
        n_buku=len(data_buku)
        self.tabelBuku.setRowCount(n_buku)
        baris=0

        for x in data_buku:
            self.tabelBuku.setItem(baris,0,QTableWidgetItem(x[0]))
            self.tabelBuku.setItem(baris,1,QTableWidgetItem(x[1]))
            self.tabelBuku.setItem(baris,2,QTableWidgetItem(x[2]))
            self.tabelBuku.setItem(baris,3,QTableWidgetItem(x[3]))
            self.tabelBuku.setItem(baris,4,QTableWidgetItem(str(x[4])))
            self.tabelBuku.setItem(baris,5,QTableWidgetItem(x[5]))
            self.tabelBuku.setItem(baris,6,QTableWidgetItem(str(x[6])))
            baris=baris+1

    def entriDataBuku(self):
        #ambil data pada form
        isbn=self.editISBN.text()
        judul=self.editJudul.text()
        pengarang=self.editPengarang.text()
        penerbit=self.editPenerbit.text()
        tahun=self.editTahun.text()
        kategori=self.editKategori.text()
        jumlah=self.editJumlah.text()

        #conn
        conn=pymysql.connect(host="localhost",user="root",password="",database="perpustakaan_db")

        #memasukkan data ke dalam tabel tbl_buku
        query="INSERT INTO tbl_buku(isbn, judul, pengarang, penerbit, tahun, kategori, jumlah) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        data=(isbn,judul, pengarang, penerbit, int(tahun), kategori, int(jumlah))
        cursor=conn.cursor()
        cursor.execute(query, data)
        conn.commit()

        #tutup koneksi
        conn.close()

        #tampilkan pesan
        self.tampilPesan('Input Success')

        #menampilkan data buku pada tabel
        self.tampilDataBuku()

        #reset
        self.resetText()

    def resetText(self):
        self.editISBN.clear()
        self.editJudul.clear()
        self.editPengarang.clear()
        self.editPenerbit.clear()
        self.editTahun.clear()
        self.editKategori.clear()
        self.editJumlah.clear()

    def tampilDataTerpilih(self):
        #menyimpan detail data buku yang dipilih
        data=self.tabelBuku.selectedItems()
        isbn=data[0].text()
        judul=data[1].text()
        pengarang=data[2].text()
        penerbit=data[3].text()
        tahun=data[4].text()
        kategori=data[5].text()
        jumlah=data[6].text()

        #menampilkan detail buku pada kotak line edit
        self.editISBN.setText(isbn)
        self.editJudul.setText(judul)
        self.editPengarang.setText(pengarang)
        self.editPenerbit.setText(penerbit)
        self.editTahun.setText(tahun)
        self.editKategori.setText(kategori)
        self.editJumlah.setText(jumlah)

    def perbaruiDataBuku(self):
        #menyimpan data yang dimasukkan pada kotak text
        isbn=self.editISBN.displayText()
        judul=self.editJudul.displayText()
        pengarang=self.editPengarang.displayText()
        penerbit=self.editPenerbit.displayText()
        tahun=self.editTahun.displayText()
        kategori=self.editKategori.displayText()
        jumlah=self.editJumlah.displayText()

        #membuatKoneksi
        conn=pymysql.connect(host="localhost",user="root",password="",database="perpustakaan_db")

        #perbarui data buku
        query="UPDATE tbl_buku SET judul=%s, pengarang=%s, penerbit=%s, tahun=%s, kategori=%s, jumlah=%s WHERE isbn=%s"
        data=(judul, pengarang, penerbit, int(tahun), kategori, int(jumlah), isbn)
        cursor=conn.cursor()
        cursor.execute(query,data)
        conn.commit()

        #menutup koneksi
        conn.close()

        #menampilkan pesan
        self.tampilPesan('data berhasil diubah')

        #tampilkan data buku menggunakan fungsi tampilDataBuku
        self.tampilDataBuku()

    def tampilJendelaKonfirmasi(self, pesan):
        msgbox=QMessageBox()
        msgbox.setIcon(QMessageBox.Question)
        msgbox.setWindowTitle('Konfirmasi')
        msgbox.setText(pesan)
        msgbox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        return msgbox.exec()

    def hapusDataBuku(self):
        #menyimpan data isbn
        #isbn.editISBN.displayText()
        isbn=self.editISBN.text()

        jendela_konfirmasi=self.tampilJendelaKonfirmasi('Apakah Anda Yakin Akan Menghapus Data Ini?')

        if jendela_konfirmasi==QMessageBox.Ok:
            #menciptakan koneksi ke server MySQL
            conn=pymysql.connect(host="localhost", user="root", password="",database="perpustakaan_db")

            #menghapus data buku
            query="DELETE FROM tbl_buku WHERE isbn=%s"
            data=(isbn,)
            cursor=conn.cursor()
            cursor.execute(query, data)
            conn.commit()

            #menutup koneksi
            conn.close()

            #menampilkan pesan menggunakan fungsi tampilPesan
            self.tampilPesan('Data Berhasil Dihapus')

            #menampilkan data buku menggunakan fungsi tampilDataBuku
            self.tampilDataBuku()

if __name__=="__main__":
    app=QApplication(sys.argv)
    form=buku()
    form.show()
    sys.exit(app.exec())
