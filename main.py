import sqlite3
import bcrypt
import tkinter

DB = "test.db"

class Ui():
    def __init__(self):
        self.window = tkinter.Tk()
        self.window.geometry("920x480")
        self.window.title("Connexion / Inscription")
        self.window.configure(bg="black")

        self.frame = tkinter.Frame(self.window, bg="gray")
        self.frame.place(relx=0.5, rely=0.5, anchor="center")
        self.db = DbHandler()
    
    def clear_frame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

    def login(self):
        username = username_entry.get()
        password = password_entry.get()
        test = self.db.login(username, password)
        login_label = tkinter.Label(self.frame, text="", bg="black", font=("Arial", 10))
        login_label.grid(row=3, column=0, columnspan=2, pady=5)
        if test == True:
            login_label.config(text="Bienvenue", fg="green")
            self.curUser = username
            self.show_users()
        else:
            login_label.config(text="Identifiants incorrects", fg="red")

    def show_login(self):
        self.clear_frame()
    
        global username_entry, password_entry, login_label

        tkinter.Label(self.frame, text="Nom utilisateur", bg="gray", font=("Arial", 12)).grid(row=0, column=0, sticky="w", pady=5)
        username_entry = tkinter.Entry(self.frame, fg="black", bg="#ddd", font=("Arial", 12))
        username_entry.grid(row=0, column=1, pady=5)
        tkinter.Label(self.frame, text="Mot de passe", bg="gray", font=("Arial", 12)).grid(row=1, column=0, sticky="w", pady=5)
        password_entry = tkinter.Entry(self.frame, show="*",fg="black", bg="#ddd", font=("Arial", 12))
        password_entry.grid(row=1, column=1, pady=5)
        login_button = tkinter.Button(self.frame, text="connexion", command=self.login, bg="#879ACB", fg="black", font=("Arial", 12))
        login_button.grid(row=2, column=0, pady=10)
        signup_button = tkinter.Button(self.frame, text="Inscription", command=self.show_signup, bg="#879ACB", fg="black", font=("Arial", 12))
        signup_button.grid(row=2, column=1, pady=10)

    def register(self):
        user = self.signup_username.get()
        pwd = self.signup_password.get()
        confirm = self.signup_confirm.get()
        

        if not user or not pwd:
            self.status_label.config(text="Veuillez remplir tous les champs", fg="red")
        test = self.db.createUser(user,pwd,confirm)
    
        if test == -1:
            self.status_label.config(text="Les mots de passe ne correspondent pas", fg="red")
        elif test == True:
            self.status_label.config(text="Compte créé !", fg="green")
            self.show_login()
        elif test == False:
            self.status_label.config(text="Username taken", fg="red")

    
    def show_signup(self):
        self.clear_frame()
        tkinter.Label(self.frame, text="Créer un compte", font=("Arial", 14, "bold"), bg="gray").grid(row=0, column=0, columnspan=2, pady=(0, 20))

        tkinter.Label(self.frame, text="Nom utilisateur", bg="gray", font=("Arial", 12)).grid(row=1, column=0, sticky="w")
        self.signup_username = tkinter.Entry(self.frame, fg="black", bg="#ddd", font=("Arial", 12))
        self.signup_username.grid(row=1, column=1)

        tkinter.Label(self.frame, text="Mot de passe", bg="gray", font=("Arial", 12)).grid(row=2, column=0, sticky="w")
        self.signup_password = tkinter.Entry(self.frame, show="*", fg="black", bg="#ddd", font=("Arial", 12))
        self.signup_password.grid(row=2, column=1)

        tkinter.Label(self.frame, text="Confirmer mot de passe", bg="gray", font=("Arial", 12)).grid(row=3, column=0, sticky="w")
        self.signup_confirm = tkinter.Entry(self.frame, show="*", fg="black", bg="#ddd", font=("Arial", 12))
        self.signup_confirm.grid(row=3, column=1)

        tkinter.Button(self.frame, text="Créer le compte", command=self.register, bg="#879ACB", fg="black", font=("Arial", 12)).grid(row=4, column=0, pady=5)
        tkinter.Button(self.frame, text="Retour", command=self.show_login, bg="#879ACB", fg="black", font=("Arial", 12)).grid(row=4, column=1, pady=5)

    def show_users(self):
        self.clear_frame()
        tkinter.Label(self.frame, text="Liste des utilisateurs", font=("Arial", 14, "bold"), bg="gray").grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        canvas = tkinter.Canvas(self.frame, bg="black", highlightthickness=0)
        scrollbar = tkinter.Scrollbar(self.frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tkinter.Frame(canvas, bg="black")
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        canvas.grid(row=1, column=0, columnspan=2, sticky="nsew")
        scrollbar.grid(row=1, column=2, sticky="ns")
        
        users = self.db.users(self.curUser)
        compter = 0
        padding = 0
        for user in users:
            if user[0] == self.curUser:
                continue
            compter += 1
            if compter % 7 == 0:
                padding += 1
                compter = 1
            
            tkinter.Button(scrollable_frame, text=user, command=lambda u=user[0]: self.show_chat(u), bg="#879ACB", fg="black", font=("Arial", 12)).grid(row=compter, column=(padding), pady=5)

        self.status_label = tkinter.Label(self.frame, text="", bg="gray", font=("Arial", 10))
        self.status_label.grid(row=1, column=0, columnspan=2, pady=5)
        tkinter.Button(self.frame, text="Déconnexion", command=self.show_login, bg="#879ACB", fg="black", font=("Arial", 12)).grid(row=3, column=1, pady=10)

    def show_chat(self, user):
        self.clear_frame()
        tkinter.Label(self.frame, text=f"Chat avec {user}", font=("Arial", 14, "bold"), bg="gray", fg="white").grid(row=0, column=0, columnspan=2, pady=(0, 20))

        self.chat_display = tkinter.Text(self.frame, bg="black", fg="white", font=("Arial", 12), state="disabled", width=50, height=20)
        self.chat_display.grid(row=1, column=0, columnspan=2, pady=10)

        chats = self.db.chat(user, self.curUser)
        for chat in chats:
            self.chat_display.config(state="normal")
            self.chat_display.insert("end", f"{chat[1]}: {chat[2]}\n")
            self.chat_display.config(state="disabled")

        self.chat_input = tkinter.Entry(self.frame, fg="black", bg="#ddd", font=("Arial", 12), width=40)
        self.chat_input.grid(row=2, column=0, pady=10)

        send_button = tkinter.Button(self.frame, text="Envoyer",command=lambda: [self.db.createMessage(self.curUser,user,self.chat_input.get()),self.show_chat(user)], bg="#879ACB", fg="black", font=("Arial", 12))
        send_button.grid(row=2, column=1, pady=10)

        back_button = tkinter.Button(self.frame, text="Retour", command=self.show_users, bg="#879ACB", fg="black", font=("Arial", 12))
        back_button.grid(row=3, column=0, columnspan=1, pady=10)
        refresh_button = tkinter.Button(self.frame, text="refresh", command=lambda: self.show_chat(user), bg="#879ACB", fg="black", font=("Arial", 12))
        refresh_button.grid(row=3, column=1, columnspan=2, pady=10)
    
    def send_message(self, user):
        msg = self.chat_input.get()
        if msg:
            self.chat_display.insert("end", f"{self.current_user} : {msg}\n")
            self.chat_input.delete(0, "end")

    
class Main():
    def __init__(self):
        self.curUser = ""

    def main(self):
        ui = Ui()
        ui.show_login()
        ui.window.mainloop()
        """conn = sqlite3.connect(DB)
        if conn == False:
            return()
        fd = conn.cursor()
        fd.execute("CREATE TABLE IF NOT EXISTS Users(Username, Password)")
        fd.execute('''INSERT INTO Users VALUES('machin', 'test'),('truc','bidule')''')
        conn.commit()
        fd.execute("SELECT * FROM Users")
        ret = fd.fetchall()
        for row in ret:
            print(row)
        print(conn.total_changes)"""

class DbHandler():
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

    def createUser(self, username, password, passcheck):
        if password != passcheck:
            print("passwords do not match")
            return -1
        conn = self.connect()
        if conn == False:
            return -2
        fd = conn.cursor()
        fd.execute("CREATE TABLE IF NOT EXISTS Users(Username, Password)")
        conn.commit()
        fd.execute("SELECT Username FROM Users WHERE Username = ?;", (username,))
        ret = fd.fetchall()
        for row in ret:
            if row[0] == username:
                print("Username taken")
                conn.close()
                return False
        bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(bytes, salt)
  
        fd.execute("INSERT INTO Users VALUES(?,?)", (username, hashed))
        conn.commit()
        conn.close()
        return True
        
    def login(self, username, password):
        conn = self.connect()
        if conn == False:
            return False
        fd = conn.cursor()
        bytes = password.encode('utf-8')
        fd.execute("CREATE TABLE IF NOT EXISTS Users(Username, Password)")
        conn.commit()
        fd.execute("SELECT Username,Password FROM Users WHERE Username = ?;", (username,))
        conn.commit()
        ret = fd.fetchall()
        if not ret:
            print("No user '" + username + "' in db")
            conn.close()
            return -1         
        for row in ret:
            if row[0] == username:
                if bcrypt.checkpw(bytes, row[1]):
                    print('success')
                    conn.close()
                    return True
                else:
                    conn.close()
                    return False
                
    def users(self,curUser):
        conn = self.connect()
        if conn == False:
            return False
        fd = conn.cursor()
        #fd.execute("CREATE TABLE IF NOT EXISTS Users(Username, Password)")
        #conn.commit()
        fd.execute("SELECT Username FROM Users") 
        conn.commit()
        ret = fd.fetchall()
        conn.close()
        return ret
        for row in ret:
            if row[0] == curUser:
                continue
            print(row)
           
    def chat(self, user, curUser):
        conn = self.connect()
        if conn == False:
            return False
        fd = conn.cursor()
        fd.execute("CREATE TABLE IF NOT EXISTS Chat(Recipient, Emitter, Message)")
        conn.commit()
        fd.execute("INSERT INTO Chat VALUES(?,?,?)", (user,curUser,"message example"))
        conn.commit()
        fd.execute("SELECT * FROM Chat WHERE (Recipient = ? AND Emitter = ?) OR ((Recipient = ? AND Emitter = ?));", (user,curUser,curUser,user))
        conn.commit()
        ret = fd.fetchall()
        return ret


    def createMessage(self, emitter, recipient, message):
        conn = self.connect()
        if conn == False:
            return False
        fd = conn.cursor()
        fd.execute("CREATE TABLE IF NOT EXISTS Chat(Recipient, Emitter, Message)")
        conn.commit()
        fd.execute("INSERT INTO Chat VALUES(?,?,?)", (recipient,emitter,message))
        conn.commit()
        conn.close()



if __name__ == "__main__":
    app = Main()
    app.main()