import tkinter as tk
from tkinter import messagebox, ttk

from lib.db import MySQL


class AdminView:
    def __init__(self, root, logout_callback):

        self.root = root
        self.logout_callback = logout_callback
        self.database = MySQL()

        # Header frame
        self.header_frame = tk.Frame(root)
        self.header_frame.pack(side=tk.TOP, fill=tk.X)

        # Netflix Admin label in the left corner
        tk.Label(self.header_frame, text="Netflix Admin", font=("Helvetica", 16)).pack(side=tk.LEFT, padx=10)

        # Logout button in the right corner
        tk.Button(self.header_frame, text="Logout", command=self.logout).pack(side=tk.RIGHT, padx=10)

        # Frame of the admin interface
        self.admin_frame = tk.Frame(root, padx=10, pady=10)
        self.admin_frame.pack(fill=tk.BOTH, expand=True)

        # Listbox to display tables
        self.table_listbox = tk.Listbox(self.admin_frame, selectmode=tk.SINGLE)
        self.table_listbox.pack(side=tk.LEFT, fill=tk.Y)
        self.populate_table_listbox()

        # Scrollbar for the listbox
        scrollbar = tk.Scrollbar(self.admin_frame, command=self.table_listbox.yview)
        scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        self.table_listbox.config(yscrollcommand=scrollbar.set)

        # Frame for CRUD operations and Treeview
        self.crud_frame = tk.Frame(self.admin_frame)
        self.crud_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Bind the click event on the table_listbox to show rows
        self.table_listbox.bind('<<ListboxSelect>>', self.show_rows)

    def populate_table_listbox(self):
        # Get the list of tables from the database
        connection = self.database.get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()

            for table in tables:
                self.table_listbox.insert(tk.END, table[0])

        except Exception as e:
            messagebox.showerror("Error", f"Error fetching tables: {e}")

        finally:
            cursor.close()

    def update_data(self):
        selected_table = self.get_selected_table()
        if selected_table:
            selected_row = self.get_selected_row()
            if selected_row:
                self.crud_frame.destroy()
                self.crud_frame = tk.Frame(self.admin_frame)
                print(selected_row)
                # Showing editable fields
                for key in selected_row:
                    label = (tk.Label(self.crud_frame, text=key))
                    label.pack(pady=5)
                    textfield = tk.Entry(self.crud_frame, width=30)
                    textfield.insert(0, selected_row[key])
                    textfield.pack(pady=10)

                tk.Button(self.crud_frame, text="Save", command=self.save_changes).pack(pady=5)
                tk.Button(self.crud_frame, text="Cancel", command=self.cancel_changes).pack(pady=5)
                self.crud_frame.pack()

    def delete_data(self):
        selected_table = self.get_selected_table()
        if selected_table:
            selected_row = self.get_selected_row()
            # if selected_row:

    def add_new_data(self):
        selected_table = self.get_selected_table()
        if selected_table:

            primer_elemento = self.treeview.get_children()[0]

            # Seleccionar el primer elemento y establecer el foco en él
            self.treeview.selection_set(primer_elemento)
            self.treeview.focus(primer_elemento)

            selected_row = self.get_selected_row()

            self.crud_frame.destroy()
            self.crud_frame = tk.Frame(self.admin_frame)

            print(selected_row)

            # Showing editable fields
            for key in selected_row:
                label = (tk.Label(self.crud_frame, text=key))
                label.pack(pady=5)
                textfield = tk.Entry(self.crud_frame, width=30)
                textfield.pack(pady=10)

            tk.Button(self.crud_frame, text="Save", command=self.save_changes).pack(pady=5)
            tk.Button(self.crud_frame, text="Cancel", command=self.cancel_changes).pack(pady=5)
            self.crud_frame.pack()

    def save_changes(self):

    def cancel_changes(self):
        print("canceled")

    def logout(self):
        if self.logout_callback:
            self.logout_callback()

    def get_selected_table(self):
        table = dict()
        selected_index = self.table_listbox.curselection()
        if selected_index:
            return self.table_listbox.get(selected_index)
        else:
            messagebox.showwarning("No Table Selected", "Please select a table from the list.")
            return None

    def show_rows(self, event):
        selected_table = self.get_selected_table()
        if selected_table:
            self.display_rows(selected_table)

    def get_selected_row(self):
        row = dict()

        selected_row = self.treeview.focus()

        if selected_row:

            keys = self.treeview["columns"]
            values = self.treeview.item(selected_row)['values']

            for key, value in zip(keys, values):
                row[key] = value

            return row
        else:
            messagebox.showwarning("No Row Selected", "Please select a row from the list.")
            return None

    def display_rows(self, table_name):
        if self.crud_frame:
            self.crud_frame.destroy()
        # Frame for CRUD operations and Treeview
        self.crud_frame = tk.Frame(self.admin_frame)
        self.crud_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Table operations buttons
        tk.Button(self.crud_frame, text="Update Data", command=self.update_data).pack(pady=5)
        tk.Button(self.crud_frame, text="Delete Data", command=self.delete_data).pack(pady=5)
        tk.Button(self.crud_frame, text="Add New Data", command=self.add_new_data).pack(pady=5)

        # Treeview for displaying rows
        self.treeview = ttk.Treeview(self.crud_frame, columns=(), show="headings", selectmode="browse")
        self.treeview.pack(fill=tk.BOTH, expand=True)

        # Get the rows from the selected table
        connection = self.database.get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()

            # Add columns to the Treeview
            if rows:
                columns = [desc[0] for desc in cursor.description]
                self.treeview["columns"] = columns
                for col in columns:
                    self.treeview.heading(col, text=col)
                    self.treeview.column(col, anchor=tk.CENTER, width=100)

                # Add rows to the Treeview
                for row in rows:
                    self.treeview.insert("", tk.END, values=row)

        except Exception as e:
            messagebox.showerror("Error", f"Error fetching rows: {e}")

        finally:
            cursor.close()

    def logout(self):
        # Destruir el marco de interfaz de administrador
        self.admin_frame.destroy()
        self.header_frame.destroy()

        # Llamar al callback de cierre de sesión proporcionado por el objeto principal
        if self.logout_callback:
            self.logout_callback()

    def destroy(self):
        # Método para permitir la destrucción del objeto desde el exterior
        self.admin_frame.destroy()
