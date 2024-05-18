import tkinter as tk
from tkinter import simpledialog
from lib.Database import Database
from lib.ECC_ElGamal import generate_keypair
import hashlib

class RegisterDialog(simpledialog.Dialog):
    def body(self, master):
        self.title("Pendaftaran Akun")

        tk.Label(master, text="Nama Pengguna:",anchor='w').grid(row=0, column=0, padx=10, pady=5,sticky='w')
        self.entry_username = tk.Entry(master)
        self.entry_username.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(master, text="Kata Sandi:",anchor='w').grid(row=1, column=0, padx=10, pady=5,sticky='w')
        self.entry_password = tk.Entry(master, show='*')
        self.entry_password.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(master, text="Konfirmasi Kata Sandi:",anchor='w').grid(row=2, column=0, padx=10, pady=5,sticky='w')
        self.entry_confirm_password = tk.Entry(master, show='*')
        self.entry_confirm_password.grid(row=2, column=1, padx=10, pady=5)
        # Fokuskan input pertama ke username
        return self.entry_username 

    def apply(self):
        self.username = self.entry_username.get()
        self.password = self.entry_password.get()
        self.confirm_password = self.entry_confirm_password.get()
class LoginDialog(simpledialog.Dialog):
    def body(self, master):
        self.title("Halaman Masuk")

        tk.Label(master, text="Nama Pengguna:",anchor='w').grid(row=0, column=0, padx=10, pady=5,sticky='w')
        self.entry_username = tk.Entry(master)
        self.entry_username.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(master, text="Kata Sandi:",anchor='w').grid(row=1, column=0, padx=10, pady=5,sticky='w')
        self.entry_password = tk.Entry(master, show='*')
        self.entry_password.grid(row=1, column=1, padx=10, pady=5)

        # Fokuskan input pertama ke username
        return self.entry_username 

    def apply(self):
        self.username = self.entry_username.get()
        self.password = self.entry_password.get()

class KeyDialog(tk.Toplevel):
    def __init__(self, parent, public_key, private_key):
        super().__init__(parent)
        self.title("Informasi Kunci")
        self.geometry("400x200")
        
        # Public Key
        tk.Label(self, text="Kunci Publik Anda:").pack(pady=(10, 0))
        tk.Label(self, text=str(public_key)).pack(pady=(0, 10))
        tk.Button(self, text="Unduh Kunci Publik", command=self.download_public_key).pack(pady=(0, 10))

        # Private Key
        tk.Label(self, text="Kunci Privat Anda:").pack(pady=(10, 0))
        tk.Label(self, text=str(private_key)).pack(pady=(0, 10))
        tk.Button(self, text="Unduh Kunci Privat", command=self.download_private_key).pack(pady=(0, 10))

        self.public_key = public_key
        self.private_key = private_key

    def download_public_key(self):
        tk.messagebox.showinfo("Kunci Publik Anda", f"Kunci Publik Anda:\n{self.public_key}")

    def download_private_key(self):
        tk.messagebox.showinfo("Kunci Privat Anda", f"Kunci Privat Anda:\n{self.private_key}")

class Client(tk.Tk):
    def __init__(self):
        super().__init__()

        # Atur window
        self.title("Wangsaff ©")
        self.geometry("1000x600")

        # Big Lable for title
        self.title_label = tk.Label(
            self, text="Wangsaff ©", font=("Arial", 24), pady=10)
        self.title_label.pack()
        # Author credit
        self.author_label = tk.Label(
            self, text="by Rehan Wangsaff team", font=("Arial", 12), pady=10)
        self.author_label.pack()

        # Frame untuk memasukkan kunci private dirinya dan kunci publik lawan bicaranya disusun vertikal dan diakhiri tombol "Hubungkan". Frame memiliki border dan label memasukkan kunci publik dan entri berada pada baris yang sama, begitupun yang kunci privat
        self.connect_frame = tk.Frame(self, bd=2, relief=tk.GROOVE)
        self.connect_frame.pack(pady=10)
        self.connect_label = tk.Label(
            self.connect_frame, text="Kunci Publik Lawan Bicara:", font=("Arial", 12),anchor='w')
        self.connect_label.grid(row=0, column=0,sticky='w')
        self.connect_entry = tk.Entry(self.connect_frame, font=("Arial", 12))
        self.connect_entry.grid(row=0, column=1)
        self.connect_label = tk.Label(
            self.connect_frame, text="Kunci Privat Anda:", font=("Arial", 12),anchor='w')
        self.connect_label.grid(row=1, column=0,sticky='w')
        self.connect_entry = tk.Entry(self.connect_frame, font=("Arial", 12))
        self.connect_entry.grid(row=1, column=1)
        # Tambahkan margin antara entry dan tombol
        self.connect_frame.grid_rowconfigure(2, minsize=50)
        self.connect_button = tk.Button(
            self.connect_frame, text="Hubungkan", font=("Arial", 12),bd=4)
        self.connect_button.grid(row=2, column=0, columnspan=2)
        # Tombol untuk mengakses kunci pengguna
        self.register_login_frame = tk.Frame(self, bd=2, relief=tk.GROOVE)
        self.register_login_frame.pack(pady=10)
        self.register_button = tk.Button(
            self.register_login_frame, text="Daftar", font=("Arial", 12),bd=4,command=self.register)
        self.register_button.grid(row=0, column=0)
        self.register_login_frame.grid_columnconfigure(1, minsize=50)
        self.login_button = tk.Button(
            self.register_login_frame, text="Masuk", font=("Arial", 12),bd=4,command=self.login)
        self.login_button.grid(row=0, column=1)

    def register(self):
        dialog = RegisterDialog(self)
        if dialog.username and dialog.password and dialog.confirm_password:
            if dialog.password != dialog.confirm_password:
                tk.messagebox.showerror("Error", "Kata Sandi Tidak Cocok!")
            else:
                Database.add_user(dialog.username, hashlib.sha256(dialog.password.encode()).hexdigest())
                tk.messagebox.showinfo("Sukses", "Pendaftaran berhasil!\nSilahkan Masuk Untuk Melihat Kunci Anda.")
        else:
            tk.messagebox.showerror("Error", "Semua Kolom Harus Diisi!")

    def login(self):
        dialog = LoginDialog(self)
        # cari user
        user = Database.search_user_by_credential(dialog.username, dialog.password)
        if user:
            # Generate key ulang
            public_key,private_key = generate_keypair()
            # Simpan public key ke database
            Database.add_public_key(user[0],str(public_key))
            # Bikin dialog yang menampilkan kunci pengguna beserta tombol untuk mengunduh kunci
            KeyDialog(self, public_key, private_key)


        else:
            tk.messagebox.showerror("Error", "Username atau kata sandi salah!")