from lib.Client import Client
from lib.Database import Database

if __name__ == "__main__":
    Database.init_table()
    c = Client()
    c.mainloop()