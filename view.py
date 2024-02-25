import tkinter as tk
from tkinter import ttk
import sqlite3


class LabTestDetails:
    def __init__(self, master):
        self.master = master
        self.master.title("Lab Test Details")
        self.master.geometry("1300x800")
        self.master.config(bg="skyblue")
        self.style = ttk.Style()
        self.style.configure("Treeview.Heading", foreground="black", font=("timesnewromen", 10, "bold"))

        self.data_treeview = ttk.Treeview(self.master)

        self.data_treeview.grid(row=3, column=0, columnspan=2, padx=20, pady=20, sticky=tk.N + tk.S + tk.W + tk.E)

        self.data_treeview["columns"] = ("ID", "Test", "Price")
        self.data_treeview.column("#0", width=0, stretch=tk.NO)
        self.data_treeview.column("ID", width=150, anchor=tk.CENTER)
        self.data_treeview.column("Test", width=150, anchor=tk.CENTER)
        self.data_treeview.column("Price", width=100, anchor=tk.CENTER)

        self.data_treeview.heading("#0", text="", anchor=tk.CENTER)
        self.data_treeview.heading("ID", text="ID", anchor=tk.CENTER)
        self.data_treeview.heading("Test", text="Test", anchor=tk.CENTER)
        self.data_treeview.heading("Price", text="Price", anchor=tk.CENTER)

        self.create_database()
        self.populate_treeview()
        self.data_treeview.bind("<<TreeviewSelect>>", self.selection_changed)

        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)
        self.master.grid_rowconfigure(3, weight=1)

    def create_database(self):
        conn = sqlite3.connect("lab_tests.db")
        c = conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS lab_test_details (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        test_name TEXT,
                        price TEXT
                    )''')

        conn.commit()
        conn.close()

    def populate_treeview(self):
        conn = sqlite3.connect("lab_tests.db")
        c = conn.cursor()
        c.execute("SELECT * FROM lab_test_details")
        rows = c.fetchall()
        self.data_treeview.delete(*self.data_treeview.get_children())
        for row in rows:
            self.data_treeview.insert("", tk.END, text="", values=row)
        conn.close()

    def selection_changed(self, event):
        selected_item = self.data_treeview.focus()
        if selected_item:
            item_data = self.data_treeview.item(selected_item)
            item_values = item_data["values"]
            self.test_combobox.set("")
            self.price_var.set("")
            if len(item_values) >= 2:
                self.test_combobox.set(item_values[1])
            if len(item_values) >= 3:
                self.price_var.set(item_values[2])

    def validate_price(self, new_value):
        if not new_value or new_value.isnumeric():
            return True
        else:
            return False

    def add(self):
        test = self.test_var.get()
        price = self.price_var.get()

        conn = sqlite3.connect("lab_tests.db")
        c = conn.cursor()
        c.execute('''INSERT INTO lab_test_details (test_name, price)
                        VALUES (?, ?)''',
                  (test, price))
        conn.commit()
        conn.close()

        self.populate_treeview()

    def update(self):
        selected_item = self.data_treeview.focus()
        if selected_item:
            item_data = self.data_treeview.item(selected_item)
            item_id = item_data["values"][0]
            test = self.test_var.get()
            price = self.price_var.get()

            conn = sqlite3.connect("lab_tests.db")
            c = conn.cursor()
            c.execute('''UPDATE lab_test_details SET test_name=?, price=?
                            WHERE id=?''',
                      (test, price, item_id))
            conn.commit()
            conn.close()

            self.populate_treeview()

    def delete(self):
        selected_item = self.data_treeview.focus()
        if selected_item:
            item_data = self.data_treeview.item(selected_item)
            item_id = item_data["values"][0]

            conn = sqlite3.connect("lab_tests.db")
            c = conn.cursor()
            c.execute("DELETE FROM lab_test_details WHERE id=?", (item_id,))
            conn.commit()
            conn.close()

            self.populate_treeview()

    def create_widgets(self):
        self.back_button = tk.Button(self.master, text="Back", command=self.back)
        self.back_button.grid(row=0, column=0, padx=20, pady=10)

    def back(self):
        self.master.destroy()
        import main


if __name__ == "__main__":
    root = tk.Tk()
    app = LabTestDetails(root)
    root.mainloop()
