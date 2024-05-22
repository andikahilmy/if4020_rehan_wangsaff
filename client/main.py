from lib.Client import Client
from lib.Database import Database
import argparse

if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser(description="Run Wangsaff Client")
    parser.add_argument("--port", type=int, default=8000, help="Port to run client")
    args = parser.parse_args()
    Database.init_table()
    c = Client(args.port)
    c.mainloop()