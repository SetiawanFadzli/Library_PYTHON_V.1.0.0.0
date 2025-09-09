import sys
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.uic import loadUi
from PyQt5.QtCore import QDate
import pymysql

class pinjam(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        loadUi('form_pinjam.ui', self)
        self.setWindowTitle('Form Pinjam')
        self.tabelMember.itemSelectionChanged.connect(self.tampilDataTerpilihMember)
        self.tabelBuku.itemSelectionChanged.connect(self.tampilDataTerpilih)
        self.tampilDataMember()
        self.tampilDataBuku()
        self.btnPinjam.clicked.connect(self.entriPinjam)

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

    def tampilDataTerpilihMember(self):
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

    def tampilDataTerpilih(self):
        #menyimpan detail data buku yang dipilih
        data=self.tabelBuku.selectedItems()
        isbn=data[0].text()
        judul=data[1].text()
        pengarang=data[2].text()
        penerbit=data[3].text()
        #tahun=data[4].text()
        #kategori=data[5].text()
        #jumlah=data[6].text()

        #menampilkan detail buku pada kotak line edit
        self.editISBN.setText(isbn)
        self.editJudul.setText(judul)
        self.editPengarang.setText(pengarang)
        self.editPenerbit.setText(penerbit)
        #self.editTahun.setText(tahun)
        #self.editKategori.setText(kategori)
        #self.editJumlah.setText(jumlah)

    def entriPinjam(self):
        #ambilDataMember
        idMember=self.editID.text()

        #ambilDataBuku
        ISBN=self.editISBN.text()

        conn=pymysql.connect(host="localhost",user="root",password="",db="perpustakaan_db")
        query="INSERT INTO tbl_pinjam(id_member,id_buku) VALUES (%s, %s)"
        data=(int(idMember),int(ISBN),)
        cursor=conn.cursor()
        cursor.execute(query,data)
        conn.commit()

        conn.close()
        
        

if __name__=="__main__":
    app=QApplication(sys.argv)
    form=pinjam()
    form.show()
    sys.exit(app.exec())
