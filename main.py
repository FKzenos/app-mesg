import sqlite3
import bcrypt

DB = "./db/test.db"

class Main():
    def __init__(self):
        self.curUser = ""

    def main(self):
        #self.createUser()
        self.login()
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
        if password != passcheck:
            print("passwords do not match")
            return False
        conn = self.connect()
        if conn == False:
            return False
        fd = conn.cursor()
        fd.execute("CREATE TABLE IF NOT EXISTS Users(Username, Password)")
        conn.commit()
        fd.execute("SELECT Username FROM Users WHERE Username = ?;", (username,))
        ret = fd.fetchall()
        for row in ret:
            if row[0] == username:
                print("Username taken")
                return False
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password, salt)
        fd.execute("INSERT INTO Users VALUES(?,?)", (username, hashed))
        conn.commit()
        
    def login(self):
        username = input("enter username")
        password = input("enter password")
        conn = self.connect()
        if conn == False:
            return False
        fd = conn.cursor()
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password,salt)
        fd.execute("SELECT Username,Password FROM Users WHERE Username = ?;", (username,))
        ret = fd.fetchall()
        for row in ret:
            if row[0] == username:
                if hashed == row[1]:
                    self.curUser = username


        
        

        


if __name__ == "__main__":
    app = Main()
    app.main()