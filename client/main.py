from lib.Client import Client
from lib.Database import Database
import argparse

if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser(description="Run Wangsaff Client")
    # parser.add_argument("port", type=int, help="Port to run client")
    parser.add_argument("server-port", type=int, help="Server port")
    args = vars(parser.parse_args())
    Database.init_table()
    c = Client(args['server-port'])
    c.mainloop()