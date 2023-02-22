"""
PROGRAM KASIR
Melakukan login akun, menghitung harga pembelian dengan masukan pindaian kode batang, dan mendaftarkan produk

Dibuat oleh:
Tiffany Angel Darmadi 			(16522050)
Syaugi Adhia Feriyaldi 			(16522070)
Panji Sri Kuncara Wisma 		(19622140)
Muhammad Dava Fathurrahman 	    (19622160)
"""

"""
KAMUS
cart, data_user : array of array
item : array of string

qty, total_price, price, discount,  : array of int

root, registerPage, cashierpage, homepage, judul_home, borderLogin, login_label, username_label, id, password_label, password, login_button, judul_cashier, conAdminInfo_cashier, userLabel_cashier, userTitik_cashier, cashier_name, IDLabel_cashier, IDTitik_cashier, cashier_id, conDate_cashier, transaction_ganesha, TranscTitik_cashier, dateLabel_ganesha, DateTitik_cashier, date_cashier, conPayment_cashier, total_cashier, TotalTitik_cashier, total, CashLabel_cashier, CashTitik_cashier, Cash, ChangeLabel_cashier, ChangeTitik_cashier, Change, Pay_button, RegProduct_cashier, Logout_cashier, cartTree_frame, cartTree, cartTreescroll, scan_btn, judul_cashier, kode_register, kodeTitik_register, kode_entry, namaProduk_register, namaProdukTitik_register, namaProduk_entry, Harga_register, HargaTitik_register, Harga_entry, generate_btn, reg_btn, gotoCashierpage, scanreg_btn : tkinter widget
"""

# ALGORITMA

# Impor modul-modul yang dibutuhkan
import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
import time
from datetime import date
from datetime import datetime
import cv2
from pyzbar import pyzbar
from io import BytesIO
from barcode import EAN13
from barcode.writer import SVGWriter

# Inisialisasi array untuk produk yang dibeli
cart = []
item = []
qty = []
total_price = []
price = []
discount = []

# Fungsi untuk berpindah halaman
def raise_frame(frame):
    frame.tkraise()


# Prosedur login
def Login():
    global data_user

    # Mengecek akun kasir

    """
    KAMUS LOKAL
    myid, mypassword : string
    records, data_user : array of array
    """

    # Algoritma
    myid = str(id.get())
    mypassword = str(password.get())

    if myid != "" and mypassword != "": # JIka id dan password tidak kosong
        mysqldb = mysql.connector.connect(host="localhost", user="root", password="", database="Ganesha_Mart")
        mycursor = mysqldb.cursor()
        mycursor.execute("SELECT  * FROM admin WHERE id=%s AND password=%s", (myid, mypassword,))
        records = mycursor.fetchall()
        if len(records) > 0: # Jika akun ditemukan di database
            data_user = records
            cashier_name.config(text = data_user[0][2]) # Menampilkan nama kasir
            cashier_id.config(text = data_user[0][0]) # Menampilkan id kasir
            raise_frame(cashierpage) # pindah ke halaman pembelian
            id.delete(0, END)
            password.delete(0, END)
        else: # Jika akun tidak dimukan
            messagebox.showwarning("Login Gagal", "Password Anda salah!\nSilakan coba lagi")
            password.delete(0, END)
        mysqldb.close()
    else:
        messagebox.showwarning("Login Gagal", "ID dan Password tidak boleh kosong!")


# Prosedur logout
def logout():
    # Me-logout akun kasir

    """
    KAMUS LOKAL
    confirm : string
    """

    # Algoritma
    confirm = messagebox.askquestion(title="Logout", message="Anda yakin ingin logout?")
    if confirm == "yes": # Jika logout
        raise_frame(homepage) # pindah ke halaman login


def regProduct():
    # Mendaftarkan produk ke tabel daftar produk

    """
    KAMUS LOKAL
    kode, nama, harga : string
    """

    # Algoritma
    kode = kode_entry.get()
    nama = namaProduk_entry.get()
    harga = Harga_entry.get()

    mysqldb = mysql.connector.connect(host="localhost", user="root", password="", database="Ganesha_Mart")
    mycursor = mysqldb.cursor()
    
    # Memasukkan produk ke basis data
    mycursor.execute("INSERT INTO product (code, item, price, discount) VALUES (%s, %s, %s, %s)", (str(kode), str(nama), str(harga), 0))
    mysqldb.commit()

    messagebox.showinfo("Registrasi Produk Berhasil", "Produk berhasil didaftarkan")
    kode_entry.delete(0, END)
    namaProduk_entry.delete(0, END)
    Harga_entry.delete(0, END)

    mysqldb.close()


# Prosedur membuat barcode
def generate():
    # Membuat barcode

    """
    KAMUS LOKAL
    kode, nama, harga : string
    """

    # Algoritma
    kode = str(kode_entry.get())
    nama = str(namaProduk_entry.get())
    harga = str(Harga_entry.get())

    with open(nama + ".svg", "wb") as f:
        EAN13(kode, writer=SVGWriter()).write(f)
    
    regProduct()


# Inisialisasi jendela utama
root = Tk()
root.state('zoomed')
root.resizable(width=1366, height=705)
root.configure(background="#0087BB")
root.title('Sistem Kasir')

#INSIALISASI FRAME untuk tiap halaman
registerPage = Frame(root, background="#e9dcc3")
registerPage.place(x=0, y=0, width=1366, height=705)

cashierpage = Frame(root, background="#e9dcc3")
cashierpage.place(x=0, y=0, width=1366, height=705)

homepage = Frame(root, background="#e9dcc3")
homepage.place(x=0, y=0, width=1366, height=705)


#TAMPILAN HALAMAN LOGIN
judul_home = Label(homepage, text = "GANESHA MART", font=("Tahoma", 24), bg="#E41D1D", fg="#FFF", width=75, bd=0, padx=11, pady=15)
judul_home.place(x=0, y=0)

borderLogin = Label(homepage, bg="#E9DCC3", width=80, height=25, highlightthickness=3, highlightbackground="#E41D1D")
borderLogin.place(x=400, y=170)

login_label = Label(homepage, text="LOGIN", bg='#E9DCC3', font=("Tahoma", 28))
login_label.place(x=630, y = 200)

username_label = Label(homepage, text="ID", bg='#E9DCC3',font=("Tahoma", 16))
username_label.place(x=500, y = 330)

id = Entry(homepage, font=("Tahoma", 16))
id.place(x=650, y = 330)

password_label = Label(homepage, text="Password", bg='#E9DCC3', font=("Tahoma", 16))
password_label.place(x=500, y = 390)

password = Entry(homepage, show="*", font=("Tahoma", 16))
password.place(x=650, y = 390)

login_button = Button(homepage, text="LOGIN", font=("Tahoma", 16), bg="#E9DCC3", command=Login)
login_button.place(x=645,y=460)


# TAMPILAN CASHIERPAGE

# Fungsi menampilkan waktu dan tanggal
def tick():
    # Mengupdate waktu dan tanggal

    """
    KAMUS LOKAL
    now : int
    day, tanggal, waktu, time_string : string
    """

    # Algoritma
    global time_string
    now = time.localtime().tm_wday
    day = date.today().strftime("%A")
    tanggal = date.today().strftime("%d %B %Y")
    waktu = time.strftime('%H:%M:%S')
    time_string = day + ", " +  tanggal + " | " + waktu
    date_cashier.config(text=time_string)
    date_cashier.after(200,tick)  # meng-update waktu dan tanggal tiap 200ms


# Prosedur pembayaran
def Pay():
    # Menghitung harga uang kembalian

    """
    KAMUS LOKAL
    total : int
    cash : str
    """

    # Algoritma
    total = sum(total_price)-sum(discount)
    cash = Cash.get()

    if total != 0: # Jika total tidak nol
        if cash != "": # Jika uang tunai tidak kosong
            if int(cash) >= total:
                Change.config(text = str('{:,}'.format(int(cash)-total).replace(',','.'))) # Memformat ribuan dengan titik
                Receipt() # Memanggil prosedur cetak setruk
                remove()
            else:
                messagebox.showwarning("Pembayaran Gagal", "Uang Anda kurang!")
        else:
            messagebox.showwarning("Pembayaran Gagal", "Masukkan Uang Tunai!")


# Prosedur pencetakan setruk
def Receipt():
    # Mencetak setruk

    """
    KAMUS LOKAL
    newWindow, scrol_y, textarea : tkinter widget
    """

    # Algoritma

    # Inisialisasi jendela baru untuk setruk
    newWindow = Toplevel(root)
    newWindow.title("Cash Receipt")
    newWindow.geometry("510x600")
    newWindow.configure(background = "#0087BB" )

    scrol_y = Scrollbar(newWindow,orient=VERTICAL)

    textarea = Text(newWindow,width=49, height=27, font=("Tahoma", 14),yscrollcommand=scrol_y)
    textarea.place(x=0, y=0)
    scrol_y.pack(side=RIGHT,fill=Y)
    scrol_y.config(command=textarea.yview)
    
    textarea.delete(1.0,END)
    textarea.insert(END,"="*35)
    textarea.insert(END,"\t\t\tCASH RECEIPT\n")
    textarea.insert(END,"="*35)
    textarea.insert(END,f"Transaction No: \t010\n")
    textarea.insert(END,f"Date: {time_string}\n")
    textarea.insert(END,f"Cashier Name: {data_user[0][2]}\n")
    textarea.insert(END,"="*35)
    textarea.insert(END,"\nProduct\t\t\tQTY\t\tPrice\n")
    textarea.insert(END,"="*35)

    # Looping untuk menambahkan informasi setiap produk yang dibeli ke setruk
    for i in range(len(item)):
        textarea.insert((11.0), f"{item[i]}\t\t\t{qty[i]}\t\t{'{:,}'.format(int(total_price[i])).replace(',','.')}\n")
        if discount[i] != 0: # Jika diskon tidak nol
            textarea.insert((11.0), f"{'{:,}'.format(discount[i]).replace(',','.')}\n")

    
    textarea.insert(END,"="*35)
    textarea.insert(END,f"Sub Total\t: {'{:,}'.format(sum(total_price)).replace(',','.')}\n")
    textarea.insert(END,f"Discount\t: {'{:,}'.format(sum(discount)).replace(',','.')}\n")
    textarea.insert(END,f"Total \t: {'{:,}'.format(sum(total_price)-sum(discount)).replace(',','.')}\n")
    textarea.insert(END,f"Cash\t: {'{:,}'.format(int(Cash.get())).replace(',','.')}\n")
    textarea.insert(END,f"Change\t: {'{:,}'.format(int(Cash.get())-(sum(total_price)-sum(discount))).replace(',','.')}\n")
    textarea.insert(END,"="*35)
    textarea.insert(END,"\t\t\tTHANK YOU!\n")

    cartTree.delete(*cartTree.get_children())
    

    # Prosedur pendeteksi apabila setruk ditutup
    def close():
        newWindow.destroy()
        total.config(text="0")
        Cash.delete(0, END)
        Change.config(text="")
    
    newWindow.protocol("WM_DELETE_WINDOW", close)
    # newWindow.mainloop()


# Prosedur menghapus data produk yang telah dibeli
def remove():
    # Menghapus data produk yang telah dibeli

    """
    KAMUS LOKAL
    soldout : int
    """

    # Algoritma
    mysqldb = mysql.connector.connect(host="localhost", user="root", password="", database="ganesha_mart")
    mycursor = mysqldb.cursor()
    for soldout in range(len(cart)):        
        mycursor.execute("DELETE from product WHERE code=%s", (cart[soldout][0],))
        mysqldb.commit()

    mysqldb.close()

    cart.clear()
    item.clear()
    qty.clear()
    total_price.clear()
    price.clear()
    discount.clear()


# Tampilan halaman pembayaran
judul_cashier = Label(cashierpage, text = "GANESHA MART", font=("Tahoma", 24), bg="#E41D1D", fg="#FFF", width=75, bd=0, padx=11, pady=15)
judul_cashier.place(x=0, y=0)

conAdminInfo_cashier = Label(cashierpage, bg="#E41D1D", width=40, height=3)
conAdminInfo_cashier.place(x=0, y=67)

userLabel_cashier = Label(cashierpage, text="Admin", font=("Tahoma",10), bg="#E41D1D", fg="#FFF")
userLabel_cashier.place(x=10,y=70)

userTitik_cashier = Label(cashierpage, text=":", font=("Tahoma",10), bg="#E41D1D", fg="#FFF")
userTitik_cashier.place(x=50,y=70)

cashier_name = Label(cashierpage, text="", font=("Tahoma",10), bg="#E41D1D", fg="#FFF")
cashier_name.place(x=60,y=70)

IDLabel_cashier = Label(cashierpage, text="ID", font=("Tahoma",10), bg="#E41D1D", fg="#FFF")
IDLabel_cashier.place(x=10,y=90)

IDTitik_cashier = Label(cashierpage, text=":", font=("Tahoma",10), bg="#E41D1D", fg="#FFF")
IDTitik_cashier.place(x=50,y=90)

cashier_id = Label(cashierpage, text="", font=("Tahoma",10), bg="#E41D1D", fg="#FFF")
cashier_id.place(x=60,y=90)


conDate_cashier = Label(cashierpage, bg="#E41D1D", width=46, height=3)
conDate_cashier.place(x=1040, y=69)

transaction_ganesha = Label(cashierpage, text="Transaction no", font=("Tahoma",10), bg="#E41D1D", fg="#FFF")
transaction_ganesha.place(x=1040,y=70)

TranscTitik_cashier = Label(cashierpage, text=":", font=("Tahoma",10), bg="#E41D1D", fg="#FFF")
TranscTitik_cashier.place(x=1130,y=70)

dateLabel_ganesha = Label(cashierpage, text="Date", font=("Tahoma",10), bg="#E41D1D", fg="#FFF")
dateLabel_ganesha.place(x=1040,y=90)

DateTitik_cashier = Label(cashierpage, text=":", font=("Tahoma",10), bg="#E41D1D", fg="#FFF")
DateTitik_cashier.place(x=1130,y=90)

date_cashier = Label(cashierpage, font=("Tahoma", 10), bg="#E41D1D" , fg="#FFF")
date_cashier.place(x=1140, y=90)

# Pemanggilan pertama fungsi untuk mengupdate waktu dan tanggal
tick()


conPayment_cashier = Label(cashierpage, bg="#E41D1D", width=45, height=12)
conPayment_cashier.place(x=1050, y=130)

total_cashier = Label(cashierpage, text="TOTAL Rp", font=("Tahoma",16), bg="#E41D1D", fg="#FFF")
total_cashier.place(x=1070,y=150)

TotalTitik_cashier = Label(cashierpage, text=":", font=("Tahoma",16), bg="#E41D1D", fg="#FFF")
TotalTitik_cashier.place(x=1170,y=150)

total = Label(cashierpage, text="0", font=("Tahoma",28), bg="#E41D1D", fg="#FFF", width=14, anchor="e")
total.place(x=1070,y=178)

CashLabel_cashier = Label(cashierpage, text="Cash", font=("Tahoma",12), bg="#E41D1D", fg="#FFF")
CashLabel_cashier.place(x=1070,y=240)

CashTitik_cashier = Label(cashierpage, text=":", font=("Tahoma",12), bg="#E41D1D", fg="#FFF")
CashTitik_cashier.place(x=1150,y=240)

Cash = Entry(cashierpage, font=("Tahoma", 14), bg="#E41D1D", fg="#FFF", width=15, relief=GROOVE)
Cash.place(x=1170, y=240)

ChangeLabel_cashier = Label(cashierpage, text="Change", font=("Tahoma",12), bg="#E41D1D", fg="#FFF")
ChangeLabel_cashier.place(x=1070,y=283)

ChangeTitik_cashier = Label(cashierpage, text=":", font=("Tahoma",12), bg="#E41D1D", fg="#FFF")
ChangeTitik_cashier.place(x=1150,y=283)

Change = Label(cashierpage, text="0", font=("Tahoma",14), bg="#E41D1D", fg="#FFF")
Change.place(x=1170,y=280)

Pay_button = Button(cashierpage, text="Pay", font=("Tahoma", 12), padx=10, bg="#FFF", command=Pay)
Pay_button.place(x=1300,y=325)

RegProduct_cashier = Label(cashierpage, text = "Register Produk", font=("Tahoma", 12), bg="#e9dcc3")
RegProduct_cashier.place(x=50, y=600)
RegProduct_cashier.bind("<Button-1>", lambda e:raise_frame(registerPage))

Logout_cashier = Label(cashierpage, text = "Logout", font=("Tahoma", 12), bg="#e9dcc3")
Logout_cashier.place(x=10, y=670)
Logout_cashier.bind("<Button-1>", lambda e:logout())

cartTree_frame = Frame(cashierpage, width=745, height=405, bg="red")
cartTree_frame.place(x=50, y=150)

cartTree = ttk.Treeview(cartTree_frame, height =19, column=("c1", "c2", "c3", "c4", "c5"), show='headings')
cartTree.column("#1", anchor=CENTER, width=60)
cartTree.heading("#1", text="NO")
cartTree.column("#2", anchor=CENTER, width=300)
cartTree.heading("#2", text="ITEM")
cartTree.column("#3", anchor=CENTER, width=70)
cartTree.heading("#3", text="QTY")
cartTree.column("#4", anchor=CENTER, width=150)
cartTree.heading("#4", text="PRICE")
cartTree.column("#5", anchor=CENTER, width=160)
cartTree.heading("#5", text="TOTAL")

cartTree.place(x=0, y=0)

cartTree.tag_configure("even", foreground="black", background="white")
cartTree.tag_configure("odd", foreground="white", background="black")

cartTreescroll = Scrollbar(cartTree, orient="vertical", command=cartTree.yview)
cartTree.configure(yscrollcommand=cartTreescroll.set)
cartTreescroll.place(x=740, y=0, relheight=1, anchor='ne')


# Fungsi pemindaian produk yang dibeli
def Scan():
    # Memindai barcode dan menambahkan produk ke tabel pembelian

    """
    KAMUS LOKAL
    lanjut : bool
    kode : str
    row = array
    i, no : int
    """

    # Algoritma
    mysqldb = mysql.connector.connect(host="localhost", user="root", password="", database="Ganesha_Mart")
    mycursor = mysqldb.cursor()
    cap = cv2.VideoCapture(0)

    lanjut = True
    while lanjut == True :
        ret, frame = cap.read()
        decode_QR = pyzbar.decode(frame)
        for qrcode in decode_QR:
            kode = str(qrcode.data).replace("'", "")
            kode = kode[1:]
            (x,y,w,h) = qrcode.rect
            cv2.rectangle(frame, (x,y),(x + w, y +w),(0,255,0), 2)
            cv2.putText(frame, kode, (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255), 2)

            mycursor.execute("SELECT  * FROM product WHERE code=%s", (kode,))
            records = mycursor.fetchall()

            # Jika kode produk ditemukan di basis data
            if len(records) > 0:
                row = list(records[0])
                if row not in cart:
                    cart.append(row)
                    
                    # Jika produk sama dengan produk sebelumnya
                    if row[1] in item:
                        idx = item.index(row[1])
                        qty[idx] += 1
                        total_price[idx] *= qty[idx]
                        discount[idx] *= qty[idx]
                    else:    
                        item.append(row[1])
                        qty.append(1)
                        price.append(row[2])
                        total_price.append(row[2])
                        discount.append(row[3])
                    lanjut = False
                    
        cv2.imshow("QR Code Scanner",frame)

        if cv2.waitKey(1) & 0xFF == ord("q") :
            break 


    cartTree.delete(*cartTree.get_children())
    no = 1

    # Looping untuk menambahkan produk yang dibeli ke tabel pembeliab
    for i in range(len(item)):
        mycart = (no, item[i], qty[i], price[i], total_price[i])
        if no%2 == 0:
            cartTree.insert("", END, values=mycart, tags=("even",))
        else:
            cartTree.insert("", END, values=mycart, tags=("odd",))
        no += 1
    
    # Meng-update harga total
    total.config(text = str('{:,}'.format(sum(total_price)-sum(discount)).replace(',','.')))

    cap.release()
    cv2.destroyAllWindows()


scan_btn = Button(cashierpage, text="Scan", font=("Tahoma", 12), padx=10, bg="#E41D1D", fg="#FFF", command=Scan)
scan_btn.place(x=1300,y=670)


# Fungsi pindai kode batang untuk halaman registrasi produk
def Scanreg():
    # Memindai barcode dan memasukkan kode box input

    """
    KAMUS LOKAL
    lanjut : bool
    kode : str
    """

    # Algoritma
    kode_entry.delete(0, END)
    cap = cv2.VideoCapture(0)

    lanjut = True
    while lanjut == True :
        ret, frame = cap.read()
        decode_QR = pyzbar.decode(frame)
        for qrcode in decode_QR:
            kode = str(qrcode.data).replace("'", "")
            kode = kode[1:]
            (x,y,w,h) = qrcode.rect
            cv2.rectangle(frame, (x,y),(x + w, y +w),(0,255,0), 2)
            cv2.putText(frame, kode, (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255), 2)

            kode_entry.insert(0, kode)

            lanjut = False
                    
        cv2.imshow("QR Code Scanner",frame)

        if cv2.waitKey(1) & 0xFF == ord("q") :
            break 

    cap.release()
    cv2.destroyAllWindows()


# Tampilan halaman registrasi produk
judul_cashier = Label(registerPage, text = "GANESHA MART", font=("Tahoma", 24), bg="#E41D1D", fg="#FFF", width=75, bd=0, padx=11, pady=15)
judul_cashier.place(x=0, y=0)

kode_register = Label(registerPage, text="Kode", font=("Tahoma", 12), bg="#E9DCC3")
kode_register.place(x=100,y=130)

kodeTitik_register = Label(registerPage, text=":", font=("Tahoma",12), bg="#E9DCC3")
kodeTitik_register.place(x=230,y=130)

kode_entry = Entry(registerPage, font=("Tahoma",12))
kode_entry.place(x=260, y=130)

namaProduk_register = Label(registerPage, text="Nama Produk", font=("Tahoma", 12), bg="#E9DCC3")
namaProduk_register.place(x=100,y=190)

namaProdukTitik_register = Label(registerPage, text=":", font=("Tahoma",12), bg="#E9DCC3")
namaProdukTitik_register.place(x=230,y=190)

namaProduk_entry = Entry(registerPage, font=("Tahoma",12))
namaProduk_entry.place(x=260, y =190)

Harga_register = Label(registerPage, text="Harga", font=("Tahoma", 12), bg="#E9DCC3")
Harga_register.place(x=100,y=250)

HargaTitik_register = Label(registerPage, text=":", font=("Tahoma",12), bg="#E9DCC3")
HargaTitik_register.place(x=230,y=250)

Harga_entry = Entry(registerPage, font=("Tahoma",12))
Harga_entry.place(x=260, y=250)

generate_btn = Button(registerPage, text="Generate", font=("Tahoma", 12), command=generate)
generate_btn.place(x=190, y=350)

reg_btn = Button(registerPage, text="Register Produk", font=("Tahoma", 12), command=regProduct)
reg_btn.place(x=320, y=350)

gotoCashierpage = Label(registerPage, text = "Cashier Page", font=("Tahoma", 12), bg="#e9dcc3")
gotoCashierpage.place(x=10, y=670)
gotoCashierpage.bind("<Button-1>", lambda e:raise_frame(cashierpage))

scanreg_btn = Button(registerPage, text="Scan", font=("Tahoma", 12), command=Scanreg, padx=10)
scanreg_btn.place(x=1300, y=670)

root.mainloop()