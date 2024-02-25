import tkinter as tk
from tkinter import *
import os

window =Tk()
window.title("Pathology Management System")
window.geometry("1920x1080+0+0")
window.config(bg="pink")


def user():
    window.destroy()
    import user


def admin_page():
    window.destroy()
    os.system('admi.py')

def back():
    window.destroy()

title_label = tk.Label(window, text="Pathology Management System", font=("Arial", 50), bg="pink")
title_label.grid(row=0, column=0, columnspan=10, pady=10)
admin_button = tk.Button(window, text="Admin", command=admin_page,font=("Arial", 28), bg="skyblue", fg="white", width=20)
admin_button.grid(row=1, column=3, padx=10, pady=10)

user_button = tk.Button(window, text="User", command=user, font=("Arial", 28), bg="orange", fg="white", width=20)
user_button.grid(row=2, column=3, padx=10, pady=10)

test_button = tk.Button(window, text="Back", command=back, font=("Arial", 28), bg="purple", fg="white", width=20)
test_button.grid(row=4, column=3, padx=10, pady=10)


window.grid_rowconfigure(0, weight=1)
window.grid_rowconfigure(5, weight=1)
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(6, weight=1)

window.mainloop()


