from tkinter import *
from tkinter import messagebox
import os

def login():
    username = entry1.get()
    password = entry2.get()

    if username == '' and password == '':
        messagebox.showerror('Login', 'Please fill in the details')
    elif username == 'user' and password == '123':
        messagebox.showinfo('Login', 'Login Successful')
        root.destroy()
        import menu
    elif username == 'user' and password != '123':
        messagebox.showinfo('Login', 'Wrong password')
    elif username != 'user' and password == '123':
        messagebox.showinfo('Login', 'Wrong user name')
    else:
        messagebox.showerror('Login', 'Wrong input')



root = Tk()
root.geometry("1300x900")
root.configure(bg="cyan4")

label1 = Label(root, text="User Login", bg="cyan4", fg="white", font=("Arial", 50))
label1.place(x=500, y=20)

label2 = Label(root, text="User Name:", bg="cyan4", fg="cyan", font=("Arial", 20))
label2.place(x=300, y=200)

label3 = Label(root, text="Password:", bg="cyan4", fg="cyan", font=("Arial", 20))
label3.place(x=300, y=300)

entry1 = Entry(root, font=("Arial", 20))
entry1.place(x=500, y=200)

entry2 = Entry(root, font=("Arial", 20), show="*")
entry2.place(x=500, y=300)

button = Button(root, text="Login", bg="cyan4", fg="white", font=("Arial", 20), command=login)
button.place(x=600, y=400)

root.mainloop()
