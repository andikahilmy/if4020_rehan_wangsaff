import os
import sqlite3
import uuid

class Database:
    DATABASE_PATH = "client/db/client.db"

    def __init__(self) -> None:
        if(not os.path.exists(Database.DATABASE_PATH)):
          self.init_table()

    def init_table(self):
        db = sqlite3.connect(Database.DATABASE_PATH)
        db.execute(
            """create table user(
id varchar(36) primary key not null,
name text);"""
        )
        db.execute(
            """CREATE TABLE chat(
  chat_id varchar(36) not null,
  user_id varchar(36) not null,
  content text,
  date timestamp default CURRENT_TIMESTAMP,
  PRIMARY KEY (chat_id,user_id),
  FOREIGN KEY(user_id) REFERENCES user(id)                   
    );
"""
        )
        db.close()

    def get_message(self,user_id:str):
        db = sqlite3.connect(Database.DATABASE_PATH)
        db.cursor().execute("SELECT * FROM chat WHERE user_id=?",(user_id))
        output = db.cursor().fetchall()
        db.commit()
        db.close()
        return output

    def add_message(self,user_id:str,content:str):
        db = sqlite3.connect(Database.DATABASE_PATH)
        chat_id = uuid.uuid4()
        db.cursor().execute("INSERT INTO chat VALUES(?,?,?)",(chat_id,user_id,content))
        db.commit()
        db.close()
if __name__=="__main__":
    d = Database()