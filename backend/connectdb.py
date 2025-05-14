import sqlite3
import os

database_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'skibsprovianten.db')

def connect_db():
  conn = sqlite3.connect(database_path)
  print("forbundet til databasen")
  return conn

if __name__ == "__main__":
  conn = connect_db()
  conn.close()
