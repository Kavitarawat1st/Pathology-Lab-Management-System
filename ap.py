from tkinter import *
from tkinter import ttk
from tkinter import messagebox as tkMessageBox
from tkcalendar import DateEntry
import sqlite3
import datetime

display_screen = Tk()
display_screen.geometry("1300x900")
display_screen.title("Patient Management System")

name = StringVar()
contact = StringVar()
age = StringVar()
test = StringVar()
date = StringVar()
doctor = StringVar()
gender = StringVar()
update_id = None

def Database():
    global conn, cursor
    conn = sqlite3.connect("patientss.db")
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS patient1 (ID INTEGER PRIMARY KEY AUTOINCREMENT, NAME TEXT, CONTACT TEXT, AGE TEXT, TEST TEXT, DATE TEXT, DOCTOR TEXT, GENDER TEXT)")


def DisplayForm():
    global LForm, LView, LButton, name_entry, contact_entry, age_entry, test_entry, date_entry, doctor_entry, gender_combobox, tree, search_entry

    LForm = LabelFrame(display_screen, text="Patient Form", bd=1, relief=SOLID, font=("Arial", 12, "bold"))
    LForm.place(x=10, y=50, width=500, height=800)

    lbl_name = Label(LForm, text="Name:", font=("Arial", 12, "bold"))
    lbl_name.grid(row=0, column=0, padx=10, pady=10, sticky=W)
    name_entry = Entry(LForm, textvariable=name, font=("Arial", 12))
    name_entry.grid(row=0, column=1, padx=10, pady=10)

    lbl_contact = Label(LForm, text="Contact:", font=("Arial", 12, "bold"))
    lbl_contact.grid(row=1, column=0, padx=10, pady=10, sticky=W)
    contact_entry = Entry(LForm, textvariable=contact, font=("Arial", 12))
    contact_entry.grid(row=1, column=1, padx=10, pady=10)

    lbl_age = Label(LForm, text="Age:", font=("Arial", 12, "bold"))
    lbl_age.grid(row=2, column=0, padx=10, pady=10, sticky=W)
    age_entry = Entry(LForm, textvariable=age, font=("Arial", 12))
    age_entry.grid(row=2, column=1, padx=10, pady=10)


    lbl_test = Label(LForm, text="Test:", font=("Arial", 12, "bold"))
    lbl_test.grid(row=3, column=0, padx=10, pady=10, sticky=W)
    test_combobox = ttk.Combobox(LForm, textvariable=test, font=("Arial", 12))
    test_combobox['values'] = ("Urine Test", "Blood Test", "Blood Sugar Test", "Imaging Scan", "Basic Metabolic Panel",
                               "Thyroid Function Test", "Liver Panel Test")
    test_combobox.grid(row=3, column=1, padx=10, pady=10)

    lbl_date = Label(LForm, text="Date:", font=("Arial", 12, "bold"))
    lbl_date.grid(row=4, column=0, padx=10, pady=10, sticky=W)
    date_entry = DateEntry(LForm, textvariable=date, font=("Arial", 12), date_pattern='yyyy-mm-dd')
    date_entry.grid(row=4, column=1, padx=10, pady=10)

    lbl_doctor = Label(LForm, text="Doctor:", font=("Arial", 12, "bold"))
    lbl_doctor.grid(row=5, column=0, padx=10, pady=10, sticky=W)
    doctor_entry = Entry(LForm, textvariable=doctor, font=("Arial", 12))
    doctor_entry.grid(row=5, column=1, padx=10, pady=10)

    lbl_gender = Label(LForm, text="Gender:", font=("Arial", 12, "bold"))
    lbl_gender.grid(row=6, column=0, padx=10, pady=10, sticky=W)
    gender_combobox = ttk.Combobox(LForm, textvariable=gender, font=("Arial", 12))
    gender_combobox['values'] = ("Male", "Female", "Other")
    gender_combobox.grid(row=6, column=1, padx=10, pady=10)

    LButton = Frame(display_screen, bd=1, relief=SOLID)
    LButton.place(x=10, y=400, width=500, height=300)

    search_label = Label(LButton, text="Search:", font=("Arial", 12, "bold"))
    search_label.grid(row=0, column=0, padx=10, pady=10)

    search_entry = Entry(LButton, font=("Arial", 12))
    search_entry.grid(row=0, column=1, padx=5, pady=10)

    btn_search = Button(LButton, text="Search", font=("Arial", 12, "bold"), bg="skyblue", command=Search , width="10")
    btn_search.grid(row=0, column=2, padx=5, pady=10)

    btn_add = Button(LButton, text="Add", font=("Arial", 12, "bold"), bg="skyblue", command=register, width="10")
    btn_add.grid(row=1, column=0, padx=10, pady=10)

    btn_update = Button(LButton, text="Update", font=("Arial", 12, "bold"), bg="skyblue", command=Update, width="10")
    btn_update.grid(row=1, column=1, padx=10, pady=10)

    btn_delete = Button(LButton, text="Delete", font=("Arial", 12, "bold"), bg="skyblue", command=Delete, width="10")
    btn_delete.grid(row=1, column=2, padx=10, pady=10)

    btn_view_all = Button(LButton, text="View All", font=("Arial", 12, "bold"), bg="skyblue", command=ViewAll, width="10")
    btn_view_all.grid(row=2, column=0, padx=10, pady=10)

    btn_clear = Button(LButton, text="Clear", font=("Arial", 12, "bold"), bg="skyblue", command=Clear, width="10")
    btn_clear.grid(row=2, column=1, padx=10, pady=10)

    btn_go_to_doctor = Button(LButton, text="Go to Doctor", font=("Arial", 12, "bold"), bg="skyblue",command=GoToDoctor)
    btn_go_to_doctor.grid(row=2, column=2, padx=10, pady=10)

    btn_back = Button(LButton, text="Back", font=("Arial", 12, "bold"), bg="skyblue", command=GoBack, width="10")
    btn_back.grid(row=3, column=0, padx=10, pady=10)



    DisplayData()

def Search():
    search_text = search_entry.get().strip()

    if not search_text:
        tkMessageBox.showwarning('', 'Please enter a name to search', icon="warning")
        return
    elif not search_text.isalpha():
        tkMessageBox.showwarning('', 'Name should contain alphabets only', icon="warning")
        return
    Database()
    tree.delete(*tree.get_children())
    cursor.execute("SELECT * FROM patient1 WHERE NAME LIKE ?", ('%' + search_text + '%',))

    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=data)

    cursor.close()
    conn.close()


def DisplayData():
    global tree
    Database()
    tree_frame = Frame(display_screen)
    tree_frame.place(x=470, y=60, width=860, height=700)

    scroll_x = Scrollbar(tree_frame, orient=HORIZONTAL)
    scroll_y = Scrollbar(tree_frame, orient=VERTICAL)

    tree = ttk.Treeview(tree_frame, columns=("id", "name", "contact", "age", "test", "date", "doctor","gender"),
                        xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

    scroll_x.pack(side=BOTTOM, fill=X)
    scroll_y.pack(side=RIGHT, fill=Y)

    scroll_x.config(command=tree.xview)
    scroll_y.config(command=tree.yview)

    tree.heading("id", text="ID")
    tree.heading("name", text="Name")
    tree.heading("contact", text="Contact")
    tree.heading("age", text="Age")
    tree.heading("test", text="Test")
    tree.heading("date", text="Date")
    tree.heading("doctor", text="Doctor")
    tree.heading("gender", text="Gender")

    tree['show'] = 'headings'
    tree.column("id", width=50)
    tree.column("name", width=150)
    tree.column("contact", width=150)
    tree.column("age", width=50)
    tree.column("test", width=150)
    tree.column("date", width=100)
    tree.column("doctor", width=100)
    tree.column("gender", width=100)

    tree.pack(fill=BOTH, expand=1)

    cursor.execute("SELECT * FROM patient1")
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=data)

    tree.bind('<ButtonRelease-1>', select_item)


def select_item(event):
    global update_id
    selecteditem = tree.selection()
    update_id = tree.item(selecteditem)['values'][0]
    name.set(tree.item(selecteditem)['values'][1])
    contact.set(tree.item(selecteditem)['values'][2])
    age.set(tree.item(selecteditem)['values'][3])
    test.set(tree.item(selecteditem)['values'][4])
    date.set(tree.item(selecteditem)['values'][5])
    doctor.set(tree.item(selecteditem)['values'][6])
    gender.set(tree.item(selecteditem)['values'][7])



def register():
    Database()
    if name.get() == "" or contact.get() == "" or age.get() == "" or test.get() == "" or date.get() == "" or doctor.get() == "" or gender.get() == "":
        tkMessageBox.showwarning('', 'Please Complete The Required Fields', icon="warning")
    elif not name.get().isalpha():
        tkMessageBox.showwarning('', 'Name should contain alphabets only', icon="warning")
    elif not contact.get().isdigit() or len(contact.get()) != 10 or contact.get()[0] < '7':
        tkMessageBox.showwarning('', 'Contact should be a valid 10-digit number starting from 70 or above',
                                 icon="warning")
    elif not age.get().isdigit() or not 1 <= int(age.get()) <= 100:
        tkMessageBox.showwarning('', 'Age should be a numeric value between 1 to 100', icon="warning")
    elif not doctor.get().replace(" ", "").isalpha():
        tkMessageBox.showwarning('', 'Doctor name should contain alphabets only', icon="warning")
    else:
        cursor.execute("SELECT * FROM patient1 WHERE DOCTOR=?", (doctor.get(),))
        fetch = cursor.fetchall()
        if fetch:
            tkMessageBox.showwarning('', 'Doctor name already exists. Please enter a new doctor name.', icon="warning")
        else:
            try:
                cursor.execute("INSERT INTO patient1 (NAME, CONTACT, AGE, TEST, DATE, DOCTOR, GENDER) VALUES (?, ?, ?, ?, ?, ?, ?)",
                               (str(name.get()), str(contact.get()), str(age.get()), str(test.get()),  str(date.get()), str(doctor.get()) , str(gender.get())))
                conn.commit()
            except sqlite3.Error as e:
                tkMessageBox.showerror('', f"Error inserting data: {e}")
            finally:
                name.set('')
                contact.set('')
                age.set('')
                test.set('')
                date.set('')
                doctor.set('')
                gender.set('')
                cursor.close()
                conn.close()
                tree.delete(*tree.get_children())
                DisplayData()


def Update():
    Database()
    if name.get() == "" or contact.get() == "" or age.get() == "" or test.get() == "" or date.get() == "" or doctor.get() == "" or gender == "":
        tkMessageBox.showwarning('', 'Please Complete The Required Fields', icon="warning")
    elif not name.get().isalpha():
        tkMessageBox.showwarning('', 'Name should contain alphabets only', icon="warning")
    elif not age.get().isdigit() or not 1 <= int(age.get()) <= 100:
        tkMessageBox.showwarning('', 'Age should be a numeric value between 1 to 100', icon="warning")
    elif not contact.get().isdigit() or len(contact.get()) != 10 or contact.get()[0] < '7':
        tkMessageBox.showwarning('', 'Contact should be a valid 10-digit number starting from 70 or above',
                                 icon="warning")
    elif not doctor.get().replace(" ", "").isalpha():
        tkMessageBox.showwarning('', 'Doctor name should contain alphabets only', icon="warning")
    else:
        print("Updating data...")
        print(f"Name: {name.get()}")
        print(f"Contact: {contact.get()}")
        print(f"Age: {age.get()}")
        print(f"Test: {test.get()}")
        print(f"Date: {date.get()}")
        print(f"Doctor: {doctor.get()}")
        print(f"Gender: {gender.get()}")
        print(f"Update ID: {update_id}")

        cursor.execute("UPDATE patient1 SET NAME=?, CONTACT=?, AGE=?, TEST=?, DATE=?, DOCTOR=?, GENDER =? WHERE id=?",
                       (str(name.get()), str(contact.get()), str(age.get()), str(test.get()),str(date.get()),
                        str(doctor.get()) ,str(gender.get()) , int(update_id)))

        conn.commit()

        name.set('')
        contact.set('')
        age.set('')
        test.set('')
        date.set('')
        doctor.set('')
        gender.set('')
        cursor.close()
        conn.close()
        tree.delete(*tree.get_children())
        DisplayData()
def ViewAll():
    Database()
    tree.delete(*tree.get_children())
    cursor.execute("SELECT * FROM patient1")
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=data)
    cursor.close()
    conn.close()


def Delete():
    Database()
    if not tree.selection():
        result = tkMessageBox.showwarning('', 'Please Select Something First!', icon="warning")
    else:
        result = tkMessageBox.askquestion('', 'Are you sure you want to delete this record?', icon="warning")
        if result == 'yes':
            selecteditem = tree.selection()[0]
            tree.delete(selecteditem)
            cursor.execute("DELETE FROM patient1 WHERE id = ?", (int(update_id),))
            conn.commit()
            cursor.close()
            conn.close()





def Clear():
    name.set('')
    contact.set('')
    age.set('')
    test.set('')
    date.set('')
    doctor.set('')
    gender.set('')

def GoToDoctor():
    display_screen.destroy()
    import doc


def GoBack():
    display_screen.destroy()
    import main

Database()
DisplayForm()
display_screen.mainloop()
