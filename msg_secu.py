import tkinter

window = tkinter.Tk()
window.geometry("1920x1080")
window.title("Connexion / Inscription")
window.configure(bg="black")

frame = tkinter.Frame(window, bg="black")
frame.place(relx=0.5, rely=0.5, anchor="center")

def clear_frame():
    for widget in frame.winfo_children():
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
