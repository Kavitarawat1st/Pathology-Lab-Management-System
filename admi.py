from tkinter import *
import sqlite3
import re
from tkinter import messagebox

global root;
root = Tk()

root.geometry('1300x900')
root.title("Login Form")
root.config(bg="cyan")

nameVar = StringVar()
emailVar = StringVar()
passVar = StringVar()
genderVar = IntVar()
javaVar = IntVar()
pythonVar = IntVar()

def validateEmail(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)


def addNew():
    name = nameVar.get()
    email = emailVar.get()
    password = passVar.get()
    gender = genderVar.get()

    if not name:
        messagebox.showerror("Invalid name")
        return

    if not validateEmail(email):
        messagebox.showerror("Invalid email format")
        return

    conn = sqlite3.connect('AdminData.db')
    with conn:
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM AdminTable WHERE Email=?', (email,))
        if cursor.fetchone() is not None:
            messagebox.showerror("Email already in use")
            return
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS AdminTable (Name TEXT,Email TEXT,Password TEXT,Gender TEXT)')
        cursor.execute('INSERT INTO AdminTable (Name,Email,Password,Gender) VALUES(?,?,?,?)',
                       (name, email, password, gender))
        count = cursor.rowcount
        if count > 0:
            messagebox.showinfo("Signup done")
        else:
            messagebox.showerror("Signup error")
        conn.commit()
def backToMainLogin():
    root.destroy()
    import new
def loginNow():
    email = emailVar.get()
    password = passVar.get()

    conn = sqlite3.connect('AdminData.db')
    with conn:
        cursor = conn.cursor()
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS AdminTable (Name TEXT,Email TEXT,Password Text,Gender TEXT)')
    cursor.execute('SELECT * FROM AdminTable WHERE Email=?', (email,))
    user_data = cursor.fetchone()

    if user_data is not None:
        if user_data[2] == password:
            messagebox.showinfo("Login Successful")
            root.destroy()
            import main
        else:
            messagebox.showerror("Login Failed", "Incorrect password")
    else:
        messagebox.showerror("Login Failed", "Email not found")

    conn.commit()

def goBackToLogin():
    loginNow()
def registerWindow():
    registerScreen = Toplevel(root)

    registerScreen.title("Registration Here")

    registerScreen.geometry('1300x900')


    label = Label(registerScreen, text="Registration", width=20, fg="cyan4", font=("bold", 20))
    label.place(x=500, y=53)

    nameLabel = Label(registerScreen, text="FullName", width=20, font=("bold", 10))
    nameLabel.place(x=450, y=130)

    nameEntery = Entry(registerScreen, textvar=nameVar)
    nameEntery.place(x=600, y=130)

    emailLabel = Label(registerScreen, text="Email", width=20, font=("bold", 10))
    emailLabel.place(x=450, y=180)


    emailEntry = Entry(registerScreen, textvar=emailVar)
    emailEntry.place(x=600, y=180)


    passLabel = Label(registerScreen, text="Password", width=20, font=("bold", 10))
    passLabel.place(x=450, y=230)

    passEntry = Entry(registerScreen, textvar=passVar, show='*')
    passEntry.place(x=600, y=230)

    genderLabel = Label(registerScreen, text="Gender", width=20, font=("bold", 10))
    genderLabel.place(x=450, y=280)

    Radiobutton(registerScreen, text="Male", padx=5, variable=genderVar, value=1).place(x=600, y=280)
    Radiobutton(registerScreen, text="Female", padx=5, variable=genderVar, value=2).place(x=600, y=300)

    Button(registerScreen, text='Submit', width=20, bg='pink', fg='white', pady=5, command=addNew).place(x=600, y=350)
    Button(registerScreen, text='Back', width=20, bg='gray', fg='white', pady=5, command=goBackToLogin).place(x=600,
                                                                                                              y=400)


label = Label(root, text="Admin Login", width=20, fg="blue",bg="cyan" ,font=("bold", 30))
label.place(x=450, y=53)

emailLabel = Label(root, text="Email", width=20, bg="cyan",font=("bold", 10))
emailLabel.place(x=450, y=130)

emailEntry = Entry(root, textvar=emailVar)
emailEntry.place(x=600, y=130)

passwordLabel = Label(root, text="Password", width=20, bg="cyan",font=("bold", 10))
passwordLabel.place(x=450, y=180)

passwordEntry = Entry(root, textvar=passVar, show='*')
passwordEntry.place(x=600, y=180)

Button(root, text='Login Now', width=20, bg='skyblue', fg='white', pady=5, command=loginNow).place(x=600, y=230)

Button(root, text="Create New Account", bg="purple", fg="white", font=("bold", 10), command=registerWindow).place(
    x=600, y=280)
Button(root, text="Back to Main Login", bg="gray", fg="white", font=("bold", 10), command=backToMainLogin).place(
    x=600, y=320)

root.mainloop()