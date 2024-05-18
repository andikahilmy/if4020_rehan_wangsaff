import tkinter as tk


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
        self.connect_button = tk.Button(
            self.connect_frame, text="Hubungkan", font=("Arial", 12))
        self.connect_button.grid(row=2, column=0, columnspan=2)


