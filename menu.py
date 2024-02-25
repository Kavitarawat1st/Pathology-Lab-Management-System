from tkinter import *
import tkinter as tk
import os

window =Tk()
window.title("Pathology Management System")
window.geometry("1920x1080+0+0")
window.config(bg="seagreen")


def booking():
    window.destroy()
    import appoint

def test():
    window.destroy()
    os.system('view.py')

def back():
    window.destroy()

title_label = tk.Label(window, text="Pathology Management System", font=("Arial", 50), bg="seagreen")
title_label.grid(row=0, column=0, columnspan=10, pady=10)
patient_button = tk.Button(window, text="Booking Test", command=booking,font=("Arial", 28), bg="cyan", fg="white", width=20)
patient_button.grid(row=1, column=3, padx=10, pady=10)


test_button = tk.Button(window, text="Test Prices", command=test, font=("Arial", 28), bg="orange", fg="white", width=20)
test_button.grid(row=3, column=3, padx=10, pady=10)

test_button = tk.Button(window, text="Back", command=back, font=("Arial", 28), bg="blue", fg="white", width=20)
test_button.grid(row=4, column=3, padx=10, pady=10)


window.grid_rowconfigure(0, weight=1)
window.grid_rowconfigure(5, weight=1)
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(6, weight=1)

window.mainloop()


