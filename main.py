import sqlite3
import bcrypt
import tkinter


DB = "./db/test.db"

class Main():
    def __init__(self):
        pass

    def main(self):
        def __init__(self):
        
            self.window = tkinter.Tk()
            self.window.geometry("1920x1080")
            self.window.title("Connexion / Inscription")
            self.window.configure(bg="black")

            self.frame = tkinter.Frame(self.window, bg="black")
            self.frame.place(relx=0.5, rely=0.5, anchor="center")

        def clear_frame():
            for widget in self.frame.winfo_children():
                widget.destroy()

        def login():
            username = username_entry.get()
            password = password_entry.get()
            if username == "admin" and password == "password":
                login_label.config(text="Bienvenue", fg="green")
            else:
                login_label.config(text="Identifiants incorrects", fg="red")

        def show_login():
            clear_frame()
    
    global username_entry, password_entry, login_label

    tkinter.Label(frame, text="Nom utilisateur", bg="black", font=("Arial", 12)).grid(row=0, column=0, sticky="w", pady=5)
    username_entry = tkinter.Entry(frame, bg="#ddd", font=("Arial", 12))
    username_entry.grid(row=0, column=1, pady=5)

    tkinter.Label(frame, text="Mot de passe", bg="black", font=("Arial", 12)).grid(row=1, column=0, sticky="w", pady=5)
    password_entry = tkinter.Entry(frame, show="*", bg="#ddd", font=("Arial", 12))
    password_entry.grid(row=1, column=1, pady=5)

    login_button = tkinter.Button(frame, text="connexion", command=login, bg="#879ACB", fg="black", font=("Arial", 12))
    login_button.grid(row=2, column=0, pady=10)

    signup_button = tkinter.Button(frame, text="Inscription", command=show_signup, bg="#879ACB", fg="black", font=("Arial", 12))
    signup_button.grid(row=2, column=1, pady=10)

    login_label = tkinter.Label(frame, text="", bg="black", font=("Arial", 10))
    login_label.grid(row=3, column=0, columnspan=2, pady=5)

def show_signup():
    clear_frame()

    def register():
        user = signup_username.get()
        pwd = signup_password.get()
        confirm = signup_confirm.get()

        if not user or not pwd:
            status_label.config(text="Veuillez remplir tous les champs", fg="red")
        elif pwd != confirm:
            status_label.config(text="Les mots de passe ne correspondent pas", fg="red")
        else:
            status_label.config(text="Compte créé !", fg="green")

    tkinter.Label(frame, text="Créer un compte", font=("Arial", 14, "bold"), bg="black").grid(row=0, column=0, columnspan=2, pady=(0, 20))

    tkinter.Label(frame, text="Nom utilisateur", bg="black", font=("Arial", 12)).grid(row=1, column=0, sticky="w")
    signup_username = tkinter.Entry(frame, bg="#ddd", font=("Arial", 12))
    signup_username.grid(row=1, column=1)

    tkinter.Label(frame, text="Mot de passe", bg="black", font=("Arial", 12)).grid(row=2, column=0, sticky="w")
    signup_password = tkinter.Entry(frame, show="*", bg="#ddd", font=("Arial", 12))
    signup_password.grid(row=2, column=1)

    tkinter.Label(frame, text="Confirmer mot de passe", bg="black", font=("Arial", 12)).grid(row=3, column=0, sticky="w")
    signup_confirm = tkinter.Entry(frame, show="*", bg="#ddd", font=("Arial", 12))
    signup_confirm.grid(row=3, column=1)

    tkinter.Button(frame, text="Créer le compte", command=register, bg="#879ACB", fg="black", font=("Arial", 12)).grid(row=4, column=0, pady=10)
    tkinter.Button(frame, text="Retour", command=show_login, bg="#879ACB", fg="black", font=("Arial", 12)).grid(row=4, column=1, pady=10)

    status_label = tkinter.Label(frame, text="", bg="black", font=("Arial", 10))
    status_label.grid(row=5, column=0, columnspan=2, pady=5)

# Démarre avec l’écran de connexion
show_login()

window.mainloop()
class DbHandler():
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
        conn.commit()
        ret = fd.fetchall()
        if not ret:
            print("No user '" + username + "' in db")            
        for row in ret:
            if row[0] == username:
                if hashed == row[1]:
                    self.curUser = username
                else:
                    print("invalid password")


if __name__ == "__main__":
    app = Main()
    app.main()