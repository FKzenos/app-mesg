import sqlite3
import bcrypt

DB = "./db/test.db"

class Main():
    def __init__(self):
        pass
        

    def main(self):
        self.createUser()

        """conn = self.connect()
        if conn == False:
            return()
        fd = conn.cursor()
        fd.execute("CREATE TABLE IF NOT EXISTS Users(Username, Password)")
        fd.execute('''INSERT INTO Users VALUES('machin', 'passtest'),('truc','passbidule')''')
        conn.commit()
        fd.execute("SELECT * FROM Users")
        ret = fd.fetchall()
        for row in ret:
            print(row)
        print(conn.total_changes)"""

    def connect(self):
        try:
            conn = sqlite3.connect(DB)
            fd = conn.cursor()
            fd.execute('SELECT SQLITE_VERSION()')
            version = fd.fetchone()
            print(f"Successfully connected to SQLite version: {version[0]}")
            fd.close()
            return (conn)
        except sqlite3.Error as e:
            print(f"Connection failed: {e}")
            return False

    def createUser(self):
        username = input("enter username")
        password = input("enter password")
        passcheck = input("enter password again")
        conn = self.connect()
        if password != passcheck:
            return False
        if conn == False:
            return False
        fd = conn.cursor()
        fd.execute("SELECT Username FROM Users WHERE Username = ?;", (username,))
        ret = fd.fetchall()
        for row in ret:
            if row == username:
                print("Username taken")
                return False
        print(ret)
        
        

        


if __name__ == "__main__":
    app = Main()
    app.main()