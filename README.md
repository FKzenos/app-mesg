# app-mesg
Requirements:

python 3.12 or >
bcrypt (pip3 install py-bcrypt)
cryptodome (pip3 install pycryptodome)
tkinger (pip3 install tk)
translate (pip3 install deeptranslator)

A small simulation of a message app with password and message encryption.

# how to use

python3 main.py

Create multiple users and you will be able to send messages between each other.
User data is stored in the Users table, it has 3 columns: Username(self explanatory), Password(which is encrypted),
and PubKey(Public key used to encrypt incoming messages).
In an actual app we would have user emitted messages in a locale database before encryption, otherwise we would not be able
to decrypt our sent messages from the server database. In this simulation, this is solved by using the private keys.

We would normally have only our user's private key stored locally, however in this simulation since we have all the private keys anyway it was found more convenient to use them straight away. The private keys are stored in './keys' folder, which should create itself on user creation.

We encrypt the messages using the recipient's public key from the "server" database, and we store them in the Chat table, which has the columns Recipient, Emitter and Message, giving us the tools to decrypt any message.

Sqlite3 was used as a mobile and lightweight alternative to any "bigger" database module, as the goal here was to make a fast simulation of encryption messaging. It was also chosen because it is already installed with Python.

bcrypt is used for password encryption because we think its the best option for a lightweight and efficient app. It allowed for full encryption with salt.

cryptodome is used for assymetryc encryption, cryptography was considered but felt better for symmetric encryption. It is used to make public and private keys.

tkinter was used for all the ui, we probably could have used any other graphic library but we had experience with it.

# team

Julien (backend)
Mokrane (frontend)