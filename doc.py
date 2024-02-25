import datetime
from tkinter import *

import tkinter.messagebox as mb
from tkinter import ttk
from tkcalendar import DateEntry
import sqlite3
import re

headlabelfont = ("Calibri", 15, 'bold')
labelfont = ('Calibri', 14)
entryfont = ('Calibri', 14)

connector = sqlite3.connect('Pathologymanagement.db')
cursor = connector.cursor()
connector.execute("CREATE TABLE IF NOT EXISTS PATHOLOGY_MANAGEMENT(PATHOLOGY_ID INTEGER PRIMARY KEY NOT NULL, NAME TEXT,ADDRESS TEXT, PHONE_NO TEXT, GENDER TEXT, DOB TEXT, LAB_TEST TEXT,DOCTOR TEXT)")

root = Tk()
root.title('Pathology Management System')
root.geometry('1300x800')

def add_record():
    global name_strvar, address_strvar, contact_strvar, gender_strvar,dob,lab_test_strvar
    name = name_strvar.get()
    address = address_strvar.get()
    contact = contact_strvar.get()
    gender = gender_strvar.get()
    DOB = dob.get_date()
    lab_test = lab_test_strvar.get()

    if not name or not address or not contact or not gender or not DOB or not lab_test:
        mb.showerror('Error!', "Please enter all the details!")
        return


    if not re.match(r'^\d{10}$', contact):
        mb.showerror('Error!', 'Invalid contact number. Please enter a 10-digit number.')
        return

    if not re.match(r'^[A-Za-z\s]+$', name_strvar.get()):
        mb.showerror('Error!', 'Invalid name. Please enter alphabetic characters only.')
        return

    if not re.match(r'^[A-Za-z\s]+$', address_strvar.get()):
        mb.showerror('Error!', 'Invalid address. Please enter alphanumeric characters only.')
        return

    try:
        connector.execute(
            'INSERT INTO PATHOLOGY_MANAGEMENT(NAME, ADDRESS, PHONE_NO, GENDER, DOB, LAB_TEST) VALUES (?,?,?,?,?,?)',
            (name, address, contact, gender, DOB, lab_test))
        connector.commit()
        mb.showinfo('Record inserted', f"Record of {name} is added")
        reset_fields()
        display_records()
    except:
        mb.showerror('Error!', 'Failed to insert the record.')

def reset_fields():
    global name_strvar, address_strvar, contact_strvar, gender_strvar, dob, lab_test_strvar
    for i in ['name_strvar', 'address_strvar', 'contact_strvar', 'gender_strvar','lab_test_strvar']:
        exec(f"{i}.set('')")
    dob.set_date(datetime.datetime.now().date())

def remove_record():
    if not tree.selection():
        mb.showerror('Error!', 'Please select an item from the database')
    else:
        current_item = tree.focus()
        values = tree.item(current_item)
        selection = values["values"]
        tree.delete(current_item)
        connector.execute('DELETE FROM PATHOLOGY_MANAGEMENT WHERE PATHOLOGY_ID=%d' % selection[0])
        connector.commit()
        mb.showinfo('Done', 'The record is deleted successfully.')
        display_records()


def update_record():
    if not tree.selection():
        mb.showerror('Error!', 'Please select an item from the database')
    else:
        current_item = tree.focus()
        values = tree.item(current_item)
        selection = values["values"]
        name = name_strvar.get()
        address = address_strvar.get()
        contact = contact_strvar.get()
        gender = gender_strvar.get()
        DOB = dob.get_date()
        lab_test = lab_test_strvar.get()

        if not name or not address or not contact or not gender or not DOB or not lab_test:
            mb.showerror('Error!', "Please enter all the details!")
        else:
            if not re.match(r'^\d{10}$', contact):
                mb.showerror('Error!', 'Invalid contact number. Please enter a 10-digit number.')
                return

            try:
                connector.execute(
                    'UPDATE PATHOLOGY_MANAGEMENT SET NAME=?, ADDRESS=?, PHONE_NO=?, GENDER=?, DOB=?, LAB_TEST=? WHERE PATHOLOGY_ID=?',
                    (name, address, contact, gender, DOB, lab_test, selection[0]))
                connector.commit()
                mb.showinfo('Done', 'The record is updated successfully.')
                reset_fields()
                display_records()
            except:
                mb.showerror('Error!', 'Failed to update the record.')


def reset_form():
    global tree
    tree.delete(*tree.get_children())
    reset_fields()

def display_records(search_query=None):
    tree.delete(*tree.get_children())
    if search_query:
        c = connector.execute("SELECT * FROM PATHOLOGY_MANAGEMENT WHERE LAB_TEST LIKE ?", ('%' + search_query + '%',))
    else:
        c = connector.execute('SELECT * FROM PATHOLOGY_MANAGEMENT')
    data = c.fetchall()
    for records in data:
        tree.insert('', END, values=records)
def search_records():
    query = search_query_strvar.get()
    display_records(query)

def go_back():
    root.destroy()
    import ap

def go_to_menu():
    root.destroy()
    import main

def on_tree_select(event):
    selected_item = tree.focus()
    if selected_item:
        values = tree.item(selected_item)['values']
        name_strvar.set(values[1])
        address_strvar.set(values[2])
        contact_strvar.set(values[3])
        gender_strvar.set(values[4])
        dob.set_date(values[5])
        lab_test_strvar.set(values[6])


lf_bg = 'SteelBlue'
name_strvar = StringVar()
address_strvar = StringVar()
contact_strvar = StringVar()
gender_strvar = StringVar()
lab_test_strvar = StringVar()
search_query_strvar = StringVar()



Label(root, text="PATHOLOGY MANAGEMENT SYSTEM", font='Arial', bg='SkyBlue').pack(side=TOP, fill=X)
left_frame = Frame(root, bg=lf_bg)
left_frame.place(x=0, y=30, height=1000, width=600)
right_frame = Frame(root, bg="gray")
right_frame.place(x=400, y=30, height=1300, width=900)


Label(left_frame, text="Name", font=labelfont, bg=lf_bg).place(x=30, y=50)
Label(left_frame, text="Contact Number", font=labelfont, bg=lf_bg).place(x=30, y=100)
Label(left_frame, text="Address", font=labelfont, bg=lf_bg).place(x=30, y=150)
Label(left_frame, text="Gender", font=labelfont, bg=lf_bg).place(x=30, y=200)
Label(left_frame, text="Date of Joining", font=labelfont, bg=lf_bg).place(x=30, y=250)
Label(left_frame, text="Specialization", font=labelfont, bg=lf_bg).place(x=30, y=300)
Label(left_frame, text="Search", font=labelfont, bg=lf_bg).place(x=30, y=350)
Entry(left_frame, width=20, textvariable=search_query_strvar, font=entryfont).place(x=170, y=350)
Entry(left_frame, width=20, textvariable=name_strvar, font=entryfont).place(x=170, y=50)
Entry(left_frame, width=19, textvariable=contact_strvar, font=entryfont).place(x=170, y=100)
Entry(left_frame, width=19, textvariable=address_strvar, font=entryfont).place(x=170, y=150)

ttk.Combobox(left_frame, textvariable=lab_test_strvar, values=[
    "Urine Test", "Blood Test", "Blood Sugar Test", "Imaging Scan", "Basic Metabolic Panel",
    "Thyroid Function Test", "Liver Panel Test"]).place(x=170, y=300, width=160)
OptionMenu(left_frame, gender_strvar, 'Male', "Female").place(x=170, y=200, width=70)
dob = DateEntry(left_frame, font=("Arial", 12), width=15)
dob.place(x=180, y=250)
Button(left_frame, text='Search', font=labelfont, command=search_records, width=15).place(x=30, y=380)
Button(left_frame, text='Add Record', font=labelfont, command=add_record, width=15).place(x=200, y=380)
Button(left_frame, text='Delete Record', font=labelfont, command=remove_record, width=15).place(x=30, y=450)
Button(left_frame, text='Update Record', font=labelfont, command=update_record, width=15).place(x=200, y=450)
Button(left_frame, text='View Record', font=labelfont, command=display_records, width=15).place(x=30, y=520)
Button(left_frame, text='Clear Fields', font=labelfont, command=reset_fields, width=15).place(x=200, y=520)
Button(left_frame, text='Go to Menu', font=labelfont, command=go_to_menu, width=15).place(x=30, y=590)

Label(left_frame, text='Doctor Records', font='Arial', bg='DarkBlue', fg='LightCyan').pack(side=TOP, fill=X)
Button(left_frame, text='Go Back', font=labelfont, command=go_back, width=15).place(x=200, y=590)

Label(right_frame, text='Doctor Records', font='Arial', bg='DarkBlue', fg='LightCyan').pack(side=TOP, fill=X)
tree = ttk.Treeview(right_frame, height=300, selectmode=BROWSE,
                    columns=('Path ID', "Name", "Address", "Contact No", "Gender", "Date of Joining", "Specialization"))
X_scroller = Scrollbar(tree, orient=HORIZONTAL, command=tree.xview)
Y_scroller = Scrollbar(tree, orient=VERTICAL, command=tree.yview)
X_scroller.pack(side=BOTTOM, fill=X)
Y_scroller.pack(side=RIGHT, fill=Y)
tree.config(yscrollcommand=Y_scroller.set, xscrollcommand=X_scroller.set)
tree.bind('<<TreeviewSelect>>', on_tree_select)

tree.heading('Path ID', text='ID', anchor=CENTER)
tree.heading('Name', text='Name', anchor=CENTER)
tree.heading('Address', text='Address', anchor=CENTER)
tree.heading('Contact No', text='Phone No', anchor=CENTER)
tree.heading('Gender', text='Gender', anchor=CENTER)
tree.heading('Date of Joining', text='DOJ', anchor=CENTER)
tree.heading('Specialization', text='Specialization', anchor=CENTER)
tree.column('#0', width=0, stretch=NO)
tree.column('#1', width=40, stretch=NO)
tree.column('#2', width=120, stretch=NO)
tree.column('#3', width=200, stretch=NO)
tree.column('#4', width=100, stretch=NO)
tree.column('#5', width=100, stretch=NO)
tree.column('#6', width=70, stretch=NO)
tree.place(y=30, relwidth=1, relheight=0.9, relx=0)

display_records()
root.update()
root.mainloop()