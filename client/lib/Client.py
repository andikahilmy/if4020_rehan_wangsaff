import tkinter as tk
from tkinter import simpledialog, filedialog as fd
from .Database import Database
from .E2EE import E2EE
from .ALS import ALS
import hashlib
import threading
import asyncio
import json
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
    def __init__(self, parent, public_key, private_key,ds_public_key,ds_private_key,user_name,port):
        super().__init__(parent)
        self.title("Informasi Kunci")
        self.geometry("400x200")

        # E2EE Key
        e2ee_frame = tk.Frame(self, relief=tk.GROOVE,bd=2)
        e2ee_frame.pack(expand=True,fill=tk.X)
        tk.Label(e2ee_frame, text="Kunci E2EE", font=("Arial", 16),justify='center').pack(pady=(10, 0))
        # Public Key
        tk.Label(e2ee_frame, text="Kunci Publik:").pack(pady=(10, 0),anchor='w')
        tk.Label(e2ee_frame, text=str(public_key)).pack(pady=(0, 10),anchor='w')
        tk.Button(e2ee_frame, text="Unduh Kunci Publik", command=self.download_public_key).pack(pady=(0, 10),anchor='center')
        # Private Key
        tk.Label(e2ee_frame, text="Kunci Privat:").pack(pady=(10, 0),anchor='w')
        tk.Label(e2ee_frame, text=str(private_key)).pack(pady=(0, 10),anchor='w')
        tk.Button(e2ee_frame, text="Unduh Kunci Privat", command=self.download_private_key).pack(pady=(0, 10),anchor='center')

        self.public_key = public_key
        self.private_key = private_key

        self.port = port

        # Digital Signature Key
        ds_frame = tk.Frame(self, relief=tk.GROOVE,bd=2)
        ds_frame.pack(expand=True,fill=tk.X)
        tk.Label(ds_frame, text="Kunci Digital Signature", font=("Arial", 16)).pack(pady=(10, 0))
        # Public Key
        tk.Label(ds_frame, text="Kunci Publik:").pack(pady=(10, 0))
        tk.Label(ds_frame, text=str(ds_public_key)).pack(pady=(0, 10))
        tk.Button(ds_frame, text="Unduh Kunci Publik", command=self.download_ds_public_key).pack(pady=(0, 10))

        # Private Key
        tk.Label(ds_frame, text="Kunci Privat:").pack(pady=(10, 0))
        tk.Label(ds_frame, text=str(ds_private_key)).pack(pady=(0, 10))
        tk.Button(ds_frame, text="Unduh Kunci Privat", command=self.download_ds_private_key).pack(pady=(0, 10))

        self.ds_public_key = ds_public_key
        self.ds_private_key = ds_private_key

        self.user_name = user_name


    def download_public_key(self):
        try:
            with open(f"keys/{self.user_name}-{self.port}.ecpub", "x") as f:
                f.write(f"{self.user_name}::{self.port}::{self.public_key}")
        except FileExistsError:
            tk.messagebox.showwarning("File Sudah Ada", f"Kunci sudah ada di  [keys/{self.user_name}-{self.port}.ecpub] ", icon='warning')
        else:
            tk.messagebox.showinfo("Pengunduhan Sukses", f"Kunci berhasil disimpan di [keys/{self.user_name}-{self.port}.ecpub]")

    def download_private_key(self):
        try:
            with open(f"keys/{self.user_name}-{self.port}.ecprv", "x") as f:
                f.write(f"{self.user_name}::{self.port}::{self.private_key}")
        except FileExistsError:
            tk.messagebox.showwarning("File Sudah Ada", f"Kunci sudah ada di  [keys/{self.user_name}-{self.port}.ecprv] ", icon='warning')
        else:
            tk.messagebox.showinfo("Pengunduhan Sukses", f"Kunci berhasil disimpan di [keys/{self.user_name}-{self.port}.ecprv]")

    def download_ds_public_key(self):
        try:
            with open(f"keys/{self.user_name}-{self.port}.scpub", "x") as f:
                f.write(f"{self.user_name}::{self.port}::{self.ds_public_key}")
        except FileExistsError:
            tk.messagebox.showwarning("File Sudah Ada", f"Kunci sudah ada di  [keys/{self.user_name}-{self.port}.scpub] ", icon='warning')
        else:
            tk.messagebox.showinfo("Pengunduhan Sukses", f"Kunci berhasil disimpan di [keys/{self.user_name}-{self.port}.scpub]")

    def download_ds_private_key(self):
        try:
            with open(f"keys/{self.user_name}-{self.port}.scprv", "x") as f:
                f.write(f"{self.user_name}::{self.port}::{self.ds_private_key}")
        except FileExistsError:
            tk.messagebox.showwarning("File Sudah Ada", f"Kunci sudah ada di  [keys/{self.user_name}-{self.port}.scprv] ", icon='warning')
        else:
            tk.messagebox.showinfo("Pengunduhan Sukses", f"Kunci berhasil disimpan di [keys/{self.user_name}-{self.port}.scprv]")

class Client(tk.Tk):
    def __init__(self,server_port:int):
        super().__init__()

        # Atur window
        self.title("Wangsaff ©")
        self.geometry("1000x600")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.start_page = StartPage(self)
        self.chat_page = ChatPage(self,server_port)

        self.show_page(self.start_page)


    def show_page(self, page):
        page.tkraise()

class StartPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.grid(row=0, column=0, sticky='nsew')

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        container = tk.Frame(self)
        container.grid(row=0, column=0)
        
        # Big Label for title
        self.title_label = tk.Label(
            container, text="Wangsaff ©", font=("Arial", 24), pady=10)
        self.title_label.pack()
        
        # Author credit
        self.author_label = tk.Label(
            container, text="by Rehan Wangsaff team", font=("Arial", 12), pady=10)
        self.author_label.pack()

        # Frame untuk memasukkan kunci private dirinya dan kunci publik lawan bicaranya disusun vertikal dan diakhiri tombol "Hubungkan". Frame memiliki border dan label memasukkan kunci publik dan entri berada pada baris yang sama, begitupun yang kunci privat
        self.connect_frame = tk.Frame(container, bd=2, relief=tk.GROOVE)
        self.connect_frame.pack(pady=10)
        
        self.connect_label = tk.Label(
            self.connect_frame, text="Kunci Publik Lawan Bicara:", font=("Arial", 12), anchor='w')
        self.connect_label.grid(row=0, column=0, sticky='w')
        self.public_entry = tk.Entry(self.connect_frame, font=("Arial", 12))
        self.public_entry.grid(row=0, column=1)
        
        self.connect_button = tk.Button(
            self.connect_frame, text="Pilih Kunci Publik", font=("Arial", 12), bd=4, command=self.select_public_key)
        self.connect_button.grid(row=0, column=2)
        
        self.connect_label = tk.Label(
            self.connect_frame, text="Kunci Privat Anda:", font=("Arial", 12), anchor='w')
        self.connect_label.grid(row=1, column=0, sticky='w')
        self.private_entry = tk.Entry(self.connect_frame, font=("Arial", 12))
        self.private_entry.grid(row=1, column=1)
        
        self.connect_button = tk.Button(
            self.connect_frame, text="Pilih Kunci Privat", font=("Arial", 12), bd=4, command=self.select_private_key)
        self.connect_button.grid(row=1, column=2)
        
        self.connect_frame.grid_rowconfigure(2, minsize=50)
        
        self.connect_button = tk.Button(
            self.connect_frame, text="Hubungkan", font=("Arial", 12), bd=4, command=self.open_chat)
        self.connect_button.grid(row=2, column=0, columnspan=2)
        
        # Tombol untuk mengakses kunci pengguna
        self.register_login_frame = tk.Frame(container, bd=2, relief=tk.GROOVE)
        self.register_login_frame.pack(pady=10)
        self.register_button = tk.Button(
            self.register_login_frame, text="Daftar", font=("Arial", 12), bd=4, command=self.register_user)
        self.register_button.grid(row=0, column=0)
        self.register_login_frame.grid_columnconfigure(1, minsize=50)
        self.login_button = tk.Button(
            self.register_login_frame, text="Masuk", font=("Arial", 12), bd=4, command=self.login)
        self.login_button.grid(row=0, column=1)

    def open_chat(self):
        # Kalau belum kekonek jangan buka
        if not self.master.chat_page.port:
            tk.messagebox.showerror("Error", "Cannot contact server!")
        # Bikin dialog konfirmasi "Apakah kunci yang Anda masukkan sudah benar?"
        confirm = tk.messagebox.askyesno("Konfirmasi", "Apakah kunci yang Anda masukkan sudah benar?")
        if not confirm:
            return
        # Baca entry kunci privat dan publik.
        public_key = self.public_entry.get()
        private_key = self.private_entry.get()
        # Jika salah satu kosong, tampilkan pesan error
        if not public_key or not private_key:
            tk.messagebox.showerror("Error", "Kunci Publik dan Privat Harus Diisi!")
            return
        # init chat
        try:
            self.master.chat_page.init_chat(public_key,private_key)
            # Buka chat window
            self.master.show_page(self.master.chat_page)
        except ValueError as e:
            tk.messagebox.showerror("Error", str(e))

    def register_user(self):
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
        # Block kalau belum kekonek
        if not self.master.chat_page.port:
            tk.messagebox.showerror("Error", "Cannot contact server!")
        dialog = LoginDialog(self)
        # cari user
        user = Database.search_user_by_credential(dialog.username, dialog.password)
        if user:
            # Bikin dialog yang menampilkan kunci pengguna beserta tombol untuk mengunduh kunci
            # TODO kunci buat digital signature
            KeyDialog(self, user[3], user[4], "", "", user[1],self.master.chat_page.port)
        else:
            tk.messagebox.showerror("Error", "Username atau kata sandi salah!")

    def select_public_key(self):
        file_path = fd.askopenfilename(title="Pilih Kunci Publik")
        if not file_path:
            return 
        with open(file_path, "r") as f:
            self.public_entry.insert(0, f.read())

    def select_private_key(self):
        file_path = fd.askopenfilename(title="Pilih Kunci Privat")
        if not file_path:
            return
        with open(file_path, "r") as f:
            self.private_entry.insert(0, f.read())

class ChatPage(tk.Frame):
    def __init__(self, parent, server_port:int):
        super().__init__(parent)
        self.server_port = server_port
        # Init koneksi
        self.init_connection()
        # grid semua elemen
        self.grid(row=0, column=0, sticky='nsew')
        # Buat chat screen
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Buat PanedWindow untuk memisahkan tombol back,chat screen dan message box
        paned_window = tk.PanedWindow(self, orient=tk.VERTICAL)
        paned_window.grid(row=0, column=0, sticky='nsew')

        # tombol back
        back_frame = tk.Frame(paned_window)
        #WARNING: kalau nih fungsi kelar bakal kena garbage collection dan gambar ilang, makanya perlu pakain self
        self.back_logo = tk.PhotoImage(file="res/images/arrow.png").subsample(16,16)
        tk.Button(back_frame, command=self.back_to_start,compound=tk.LEFT,image=self.back_logo,height=30,width=75,bd=4).pack(pady=10,side=tk.LEFT)
        paned_window.add(back_frame)
        
        # frame untuk chat screen
        top_frame = tk.Frame(paned_window)
        paned_window.add(top_frame, stretch='always')
        paned_window.paneconfig(top_frame, height=400)  # Tinggi chat screen

        # Atur scrollbar
        chat_display_frame = tk.Frame(top_frame)
        chat_display_frame.pack(fill=tk.BOTH, expand=True)
        chat_display_scrollbar = tk.Scrollbar(chat_display_frame)
        self.chat_display = tk.Text(chat_display_frame, state='disabled', width=50, height=10, yscrollcommand=chat_display_scrollbar.set)
        chat_display_scrollbar.config(command=self.chat_display.yview)
        chat_display_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.chat_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=3)

        # Frame untuk input teks
        input_frame = tk.Frame(paned_window)
        input_frame.pack(fill=tk.X, expand=True, pady=5)
        paned_window.add(input_frame, stretch='always')
        input_frame.grid_columnconfigure(0, weight=1)

        # Input pesan dan tombol
        self.message_entry = tk.Entry(input_frame, width=50)
        self.message_entry.grid(row=0, column=0, padx=5, pady=5, sticky='ew')
        tk.Button(input_frame, text="Send", command=self.send_message).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(input_frame, text="Sign and Send", command=self.send_message).grid(row=0, column=2, padx=5, pady=5)

    def init_connection(self)->None:
        # Buat thread untuk handle koneksi
        self.async_loop = asyncio.new_event_loop()
        self.queue = asyncio.Queue()
        threading.Thread(target=self._start_connection).start()

    def _start_connection(self)->None:
        # Jalankan fungsi handler koneksi secara asynchronous
        asyncio.set_event_loop(self.async_loop)
        # self.async_loop.run_until_complete(self._async_handle_connection())
        self.async_loop.create_task(self._async_handle_connection())
        self.async_loop.run_forever()
        # asyncio.run(self._async_handle_connection())

    async def _async_handle_connection(self)->None:
        self.als = ALS(self.server_port,self.receive_message_handler,self.queue)
        print("aku")
        await self.als.start_connection()
        print("kena")
        # await self.als.connected_event.wait()
        print("Ass")
        print("port",self.als.get_port())
        self.port = self.als.get_port()
        print("a")
        print(self.port)
        self.master.title(f"(Wangsaff ©)@{self.port}")
    
    def receive_message_handler(self,encrypted_message:str):
        print("MEssage",encrypted_message)
        # if encrypted_message['message'] in ['Connection Established','Message sent','Failed to send message'] or encrypted_message['message'].startswith("Failed to send message:"):
        #     return
        # decrypt_data
        message = E2EE.decrypt(encrypted_message,self.private_key)
        print("dec message",message)
        # Tampilin di layar
        self.chat_display.tag_configure('tag-them', justify=tk.RIGHT)
        self.chat_display.config(state='normal')
        self.chat_display.insert(tk.END, f"{self.chatmate}: {message}\n",'tag-them')
        # Tombol buat melihat dan verifikasi signature
        view_button = tk.Button(self.chat_display, text="Lihat Signature", command=self.view_signature)
        verify_button = tk.Button(self.chat_display, text="Verifikasi Signature", command=self.verify_signature)

        # Tambahkan tombol ke display
        self.chat_display.window_create(tk.END, window=view_button,align=tk.RIGHT)
        self.chat_display.window_create(tk.END, window=verify_button,align=tk.RIGHT)
        self.chat_display.insert(tk.END, "\n")

        # Hapus teks di message box
        self.chat_display.config(state='disabled')
        self.message_entry.delete(0, tk.END)

    def init_chat(self,public_key:str,private_key:str):
        tmp = public_key.split("::")
        if len(tmp)<3:
            raise ValueError("Invalid public key format")
        self.chatmate = tmp[0]
        self.mate_port = int(tmp[1])
        self.public_key = tmp[2]
        tmp = private_key.split("::")
        if len(tmp)<3:
            raise ValueError("Invalid private key format")
        self.private_key = int(tmp[2])

    def send_message(self):
        if self.port:
            # Bikin thread untuk kirim pesan
            threading.Thread(target=self._send_message,daemon=True).start()

    def _send_message(self):
        # Kirim secara asynchronous
        asyncio.run(self._async_send_message())
    
    async def _async_send_message(self):
        message = self.message_entry.get()
        print(message)
        if message:
            # Simpan ke database
            e2ee_encrypted_message = E2EE.encrypt(message.encode(),self.public_key)
            Database.add_message(self.port,e2ee_encrypted_message)
            # Buat payload
            payload = {
                "src_port": self.port,
                "dst_port": self.mate_port,
                "message": e2ee_encrypted_message
            }
            # Kirim pesan
            asyncio.run_coroutine_threadsafe(self.als.send(json.dumps(payload)), self.async_loop)
            # asyncio.run_coroutine_threadsafe(messagesender(msg), async_loop)
            # await self.als.send(e2ee_encrypted_message)
            # Cetak Pesan
            self.chat_display.tag_configure('tag-us', justify=tk.LEFT)
            self.chat_display.config(state='normal')
            self.chat_display.insert(tk.END, f"You: {message}\n",'tag-us')

            # Tombol buat melihat dan verifikasi signature
            view_button = tk.Button(self.chat_display, text="Lihat Signature", command=self.view_signature)
            verify_button = tk.Button(self.chat_display, text="Verifikasi Signature", command=self.verify_signature)

            # Tambahkan tombol ke display
            self.chat_display.window_create(tk.END, window=view_button)
            self.chat_display.window_create(tk.END, window=verify_button)
            self.chat_display.insert(tk.END, "\n")

            # Hapus teks di message box
            self.chat_display.config(state='disabled')
            self.message_entry.delete(0, tk.END)

    def back_to_start(self):
        self.master.show_page(self.master.start_page)

    def verify_signature(self):
        tk.messagebox.showinfo("Verification", "The signature is valid.")

    def view_signature(self):
        tk.messagebox.showinfo("Pake Nanya")