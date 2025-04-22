import sqlite3
import bcrypt
import tkinter
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes
import os
from tkinter import ttk
import tkinter.messagebox as messagebox 
from deep_translator import GoogleTranslator


DB = "test.db"

class Ui():
    def __init__(self):
        self.window = tkinter.Tk()
        self.window.geometry("920x700")
        self.window.title("Connexion / Inscription")
        self.window.configure(bg="#2C3E50") 
        
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TLabel", background="#2C3E50", foreground="white", font=("Arial", 12))
        self.style.configure("TButton", background="#3498DB", foreground="white", font=("Arial", 12), padding=5)
        self.style.map("TButton", background=[("active", "#2980B9")])
        self.style.configure("TEntry", font=("Arial", 12), padding=5)

        self.frame = tkinter.Frame(self.window, bg="#34495E", bd=5, relief="ridge")
        self.frame.place(relx=0.5, rely=0.5, anchor="center")
        self.selected_language = "fr" 
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

        tkinter.Label(self.frame, text="Nom utilisateur", bg="#2C3E50", font=("Arial", 12)).grid(row=0, column=0, sticky="w", pady=5)
        username_entry = tkinter.Entry(self.frame, fg="black", bg="#ddd", font=("Arial", 12))
        username_entry.grid(row=0, column=1, pady=5)
        tkinter.Label(self.frame, text="Mot de passe", bg="#2C3E50", font=("Arial", 12)).grid(row=1, column=0, sticky="w", pady=5)
        password_entry = tkinter.Entry(self.frame, show="*",fg="black", bg="#ddd", font=("Arial", 12))
        password_entry.grid(row=1, column=1, pady=5)
        login_button = tkinter.Button(self.frame, text="connexion", command=self.login, bg="#879ACB", fg="black", font=("Arial", 12))
        login_button.grid(row=2, column=0, pady=10)
        signup_button = tkinter.Button(self.frame, text="Inscription", command=self.show_signup, bg="#879ACB", fg="black", font=("Arial", 12))
        signup_button.grid(row=2, column=1, pady=10)
        quit_button = tkinter.Button(self.frame, text="Quitter", command=self.window.quit, bg="#E74C3C", fg="black", font=("Arial", 12))
        quit_button.grid(row=3, column=0, columnspan=2, pady=10)

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
        tkinter.Label(self.frame, text="Créer un compte", font=("Arial", 14, "bold"), bg="#2C3E50").grid(row=0, column=0, columnspan=2, pady=(0, 20))

        tkinter.Label(self.frame, text="Nom utilisateur", bg="#2C3E50", font=("Arial", 12)).grid(row=1, column=0, sticky="w")
        self.signup_username = tkinter.Entry(self.frame, fg="black", bg="#ddd", font=("Arial", 12))
        self.signup_username.grid(row=1, column=1)

        tkinter.Label(self.frame, text="Mot de passe", bg="#2C3E50", font=("Arial", 12)).grid(row=2, column=0, sticky="w")
        self.signup_password = tkinter.Entry(self.frame, show="*", fg="black", bg="#ddd", font=("Arial", 12))
        self.signup_password.grid(row=2, column=1)

        tkinter.Label(self.frame, text="Confirmer mot de passe", bg="#2C3E50", font=("Arial", 12)).grid(row=3, column=0, sticky="w")
        self.signup_confirm = tkinter.Entry(self.frame, show="*", fg="black", bg="#ddd", font=("Arial", 12))
        self.signup_confirm.grid(row=3, column=1)

        tkinter.Button(self.frame, text="Créer le compte", command=self.register, bg="#879ACB", fg="black", font=("Arial", 12)).grid(row=4, column=0, pady=5)
        tkinter.Button(self.frame, text="Retour", command=self.show_login, bg="#879ACB", fg="black", font=("Arial", 12)).grid(row=4, column=1, pady=5)
       
        self.status_label = tkinter.Label(self.frame, text="", bg="#2C3E50", font=("Arial", 10))
        self.status_label.grid(row=5, column=0, columnspan=2, pady=5)


        self.status_label = tkinter.Label(self.frame, text="", bg="gray", font=("Arial", 10))
        self.status_label.grid(row=5, column=0, columnspan=2, pady=5)

    def show_users(self):
        self.clear_frame()
        tkinter.Label(self.frame, text="Liste des utilisateurs", font=("Arial", 14, "bold"), bg="#2C3E50").grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
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
            
            tkinter.Button(self.frame, text=user, command=lambda u=user[0]: self.show_chat(u), bg="#879ACB", fg="black", font=("Arial", 12)).grid(row=compter, column=(padding), pady=5)

        self.status_label = tkinter.Label(self.frame, text="", bg="#2C3E50", font=("Arial", 10))
        self.status_label.grid(row=compter + 1, column=0, columnspan=2, pady=5)
        tkinter.Button(self.frame, text="Déconnexion", command=self.show_login, bg="#879ACB", fg="black", font=("Arial", 12)).grid(row=compter + 20, column=0, columnspan=2, pady=10)

    def show_chat(self, user):
        self.clear_frame()

        # Titre du chat
        tkinter.Label(
            self.frame, text=f"Chat avec {user}", font=("Arial", 14, "bold"),
            bg="#2C3E50", fg="white"
        ).grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Zone d'affichage des messages
        self.chat_display = tkinter.Text(
            self.frame, bg="black", fg="white", font=("Arial", 12),
            state="disabled", width=50, height=20
        )
        self.chat_display.grid(row=1, column=0, columnspan=2, pady=10)

        # Chargement des messages
        chats = self.db.chat(user, self.curUser)

        # --- Chargement des clés RSA ---
        try:
            with open(f"./keys/{self.curUser}/key.pem", "rb") as f:
                key = f.read()
                if b"-----BEGIN" not in key or b"-----END" not in key:
                    raise ValueError("Le format de la clé n'est pas PEM.")
                rsa_key = RSA.import_key(key.strip())
                cipher_rsa = PKCS1_OAEP.new(rsa_key)
        except Exception as e:
            print(f"[ERREUR CLE PRIVEE] {e}")
            messagebox.showerror("Erreur", "Impossible de charger la clé privée de l'utilisateur courant.")
            return

        try:
            with open(f"./keys/{user}/key.pem", "rb") as f:
                userkey = f.read()
                if b"-----BEGIN" not in userkey or b"-----END" not in userkey:
                    raise ValueError("Le format de la clé n'est pas PEM.")
                userrsa_key = RSA.import_key(userkey.strip())
                usercipher_rsa = PKCS1_OAEP.new(userrsa_key)
        except Exception as e:
            print(f"[ERREUR CLE PUBLIQUE] {e}")
            messagebox.showerror("Erreur", "Impossible de charger la clé publique du destinataire.")
            return

        # Zone d’entrée de message
        self.message_entry = tkinter.Entry(self.frame, font=("Arial", 12))
        self.message_entry.grid(row=2, column=0, padx=10, pady=10)

        # --- Menu de sélection de langue ---
        languages = {
            "Français": "fr",
            "Anglais": "en",
            "Espagnol": "es",
            "Allemand": "de",
            "Italien": "it",
            "Portugais": "pt",
            "Néerlandais": "nl",
            "Polonais": "pl",
            "Arabe": "ar",
            "Japonais": "ja",
            "Chinois": "zh-CN"
        }
        self.lang_dropdown = ttk.Combobox(self.frame, values=list(languages.keys()), font=("Arial", 10))
        self.lang_dropdown.set("Français")
        self.lang_dropdown.grid(row=2, column=1, padx=10, pady=10)


        # Bouton retour
        tkinter.Button(
            self.frame, text="Retour", command=self.show_users,
            bg="#e67e22", fg="white", font=("Arial", 12)
        ).grid(row=4, column=0, pady=10)

        # Bouton déconnexion
        tkinter.Button(
            self.frame, text="Déconnexion", command=self.show_login,
            bg="#c0392b", fg="white", font=("Arial", 12)
        ).grid(row=4, column=1, pady=10)

        # Chargement des messages dans le chat_display
        self.db.chat(user,self.curUser)

        def update_language(event):
            lang_name = self.lang_dropdown.get()
            self.selected_language = languages[lang_name]

        self.lang_dropdown.bind("<<ComboboxSelected>>", update_language)


        # Affichage des messages décryptés
        for chat in chats:
            self.chat_display.config(state="normal")
            if (chat[0] == self.curUser):
                try:
                    decrypted = cipher_rsa.decrypt(chat[2])
                    message_text = decrypted.decode("utf-8")
                except Exception as e:
                    message_text = "[Erreur de déchiffrement]"
                    print(f"Erreur de déchiffrement: {e}")
            elif (chat[0] == user):
                try:
                    decrypted = usercipher_rsa.decrypt(chat[2])
                    message_text = decrypted.decode("utf-8")
                except Exception as e:
                    message_text = "[Erreur de déchiffrement]"
                    print(f"Erreur de déchiffrement: {e}")

            # Insère le message décrypté dans la zone de chat
            self.chat_display.insert("end", f"{chat[1]}: {message_text}\n")
            self.chat_display.config(state="disabled")

        # Fait défiler la zone de chat vers le bas
        self.chat_display.see("end")

        # Zone de saisie pour un nouveau message
        self.chat_input = tkinter.Entry(self.frame, fg="black", bg="#ddd", font=("Arial", 12), width=40)
        self.chat_input.grid(row=2, column=0, pady=10)

        # Bouton d'envoi du message
        send_button = tkinter.Button(self.frame, text="Envoyer", command=lambda: [self.db.createMessage(user, self.curUser,GoogleTranslator(source='auto', target=self.selected_language).translate(self.chat_input.get())),self.show_chat(user)], bg="#879ACB", fg="black", font=("Arial", 12))
        send_button.grid(row=2, column=1, pady=10)

        # Bouton "Retour" pour revenir à la liste des utilisateurs
        back_button = tkinter.Button(self.frame, text="Retour", command=self.show_users, bg="#879ACB", fg="black", font=("Arial", 12))
        back_button.grid(row=3, column=0, pady=10)

        # Bouton "Actualiser" pour rafraîchir le chat
        refresh_button = tkinter.Button(self.frame, text="Actualiser", command=lambda: self.show_chat(user), bg="#879ACB", fg="black", font=("Arial", 12))
        refresh_button.grid(row=3, column=1, pady=10)   


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
        fd.execute("CREATE TABLE IF NOT EXISTS Users(Username, Password, PubKey)")
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
        if os.path.exists("./keys/") == False:
            os.mkdir("./keys")
            if (os.path.exists("./keys/" + username)) == False:
                os.mkdir("./keys/" + username)                
                if os.path.exists("./keys/" + username + "/key.pem"):
                    os.remove("./keys/" + username + "/key.pem")
            else:
                os.mkdir("./keys" + username)
        elif (os.path.exists("./keys/" + username)) == False:
            os.mkdir("./keys/" + username)   

        f = open("./keys/" + username + "/key.pem", "w+")
        key = RSA.generate(2048)
        private_key = key.export_key().decode('utf-8')
        public_key = key.publickey().export_key().decode('utf-8')
        f.write((private_key))
        f.close()
        fd.execute("INSERT INTO Users VALUES(?,?,?)", (username, hashed, public_key))
        conn.commit() 
        conn.close()
        return True
        
    def login(self, username, password):
        conn = self.connect()
        if conn == False:
            return False
        fd = conn.cursor()
        bytes = password.encode('utf-8')
        fd.execute("CREATE TABLE IF NOT EXISTS Users(Username, Password, PubKey)")
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
        fd.execute("SELECT * FROM Chat WHERE (Recipient = ? AND Emitter = ?) OR ((Recipient = ? AND Emitter = ?));", (user,curUser,curUser,user))
        conn.commit()
        ret = fd.fetchall()
        return ret


    def createMessage(self, emitter, recipient, message):
        conn = self.connect()
        if not conn:
            return False
        fd = conn.cursor()
        fd.execute("CREATE TABLE IF NOT EXISTS Chat(Recipient TEXT, Emitter TEXT, Message BLOB)")
        conn.commit()
        fd.execute("SELECT PubKey FROM Users WHERE Username = ?;", (recipient,))
        ret = fd.fetchone()
        if not ret:
            print("Public key not found.")
            return False
        public_key = ret[0]
        bytes_msg = message.encode("utf-8")
        try:
            if isinstance(public_key, str):
                public_key = public_key.encode('utf-8')
            rsa_key = RSA.import_key(public_key)
            cipher_rsa = PKCS1_OAEP.new(rsa_key)
            cipher_text = cipher_rsa.encrypt(bytes_msg)
            fd.execute("INSERT INTO Chat(Recipient, Emitter, Message) VALUES (?, ?, ?)", (recipient, emitter, cipher_text))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Erreur lors du chiffrement du message: {e}")
            return False

class Main():
    def __init__(self):
        self.curUser = ""

    def main(self):
        ui = Ui()
        ui.show_login()
        ui.window.mainloop()





if __name__ == "__main__":
    app = Main()
    app.main()