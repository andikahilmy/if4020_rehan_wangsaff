import os
import sqlite3
import uuid
import hashlib
import datetime
from .ECC_ElGamal import generate_keypair


class Database:
    DATABASE_PATH = "client/db/client.db"

    # def __init__(self) -> None:
    #     if(not os.path.exists(Database.DATABASE_PATH)):
    #       self.init_table()

    @staticmethod
    def init_table():
        if not os.path.exists(Database.DATABASE_PATH):
            db = sqlite3.connect(Database.DATABASE_PATH)
            db.execute(
                """
            create table user(
id varchar(36) primary key not null,
name text,
password text,
pubkey text,
privkey text);"""
            )
            db.execute(
                """
            CREATE TABLE chat(
  chat_id varchar(36) not null,
  src_port integer not null,
  content text,
  date text,
  PRIMARY KEY (chat_id)               
    );
"""
            )
            db.close()

    @staticmethod
    def get_message(src_port: int):
        db = sqlite3.connect(Database.DATABASE_PATH)
        db.cursor().execute("SELECT * FROM chat WHERE src_port=?", (src_port))
        output = db.cursor().fetchall()
        db.commit()
        db.close()
        return output

    @staticmethod
    def add_message(port: int, content: str):
        db = sqlite3.connect(Database.DATABASE_PATH)
        chat_id = uuid.uuid4()
        db.cursor().execute(
            "INSERT INTO chat VALUES(?,?,?,?)", (str(chat_id), port, content,datetime.datetime.now().isoformat())
        )
        db.commit()
        db.close()

    @staticmethod
    def add_user(name: str, password: str):
        public_key, private_key = generate_keypair()
        db = sqlite3.connect(Database.DATABASE_PATH)
        user_id = uuid.uuid4()
        db.cursor().execute(
            "INSERT INTO user VALUES(?,?,?,?,?)",
            (str(user_id), name, password, str(public_key), str(private_key)),
        )
        db.commit()
        db.close()

    # @staticmethod
    # def add_public_key(user_id:str,pubkey:str):
    #     db = sqlite3.connect(Database.DATABASE_PATH)
    #     db.cursor().execute("UPDATE user SET pubkey=? WHERE id=?",(pubkey,user_id))
    #     db.commit()
    #     db.close()

    @staticmethod
    def search_user_by_credential(name: str, password: str):
        db = sqlite3.connect(Database.DATABASE_PATH)
        cursor = db.cursor()
        cursor.execute(
            "SELECT * FROM user WHERE name=? AND password=?",
            (name, hashlib.sha256(password.encode()).hexdigest()),
        )
        output = cursor.fetchone()
        db.commit()
        db.close()
        return output


if __name__ == "__main__":
    d = Database()
