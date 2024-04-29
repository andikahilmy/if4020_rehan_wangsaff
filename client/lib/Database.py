import os
import sqlite3


class Database:
    DATABASE_PATH = "client/db/client.db"

    def __init__(self) -> None:
        if(not os.path.exists(Database.DATABASE_PATH)):
          self.init_table()

    def init_table(self):
        self.db = sqlite3.connect(Database.DATABASE_PATH)
        self.db.execute(
            """create table user(
id varchar(36) primary key not null,
name text);"""
        )
        self.db.execute(
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
        self.db.close()
if __name__=="__main__":
    d = Database()