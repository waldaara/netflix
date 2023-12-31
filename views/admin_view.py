import tkinter as tk
from tkinter import messagebox, ttk

from lib.db import MySQL


class AdminView:
    def __init__(self, root, logout_callback):
        self.edited_row = {}
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
                self.edited_row = {}
                for i, key in enumerate(selected_row):
                    label = tk.Label(self.crud_frame, text=key)
                    label.pack(pady=5)

                    # Condición para hacer editable solo el primer elemento
                    if i != 0:
                        entry_var = tk.StringVar(value=selected_row[key])
                        entry = tk.Entry(self.crud_frame, width=30, textvariable=entry_var)
                        entry.pack(pady=10)

                        # Almacena la variable asociada al Entry en el diccionario
                        self.edited_row[key] = entry_var
                    else:
                        entry_var = tk.StringVar(value=selected_row[key])
                        entry = tk.Entry(self.crud_frame, width=30, textvariable=entry_var)
                        entry.pack(pady=10)
                        entry.config(state="readonly")
                        self.edited_row[key] = entry_var

                tk.Button(self.crud_frame, text="Save", command=self.save_changes_update).pack(pady=5)
                tk.Button(self.crud_frame, text="Cancel", command=self.cancel_changes).pack(pady=5)
                self.crud_frame.pack()

    def delete_data(self):
        selected_table = self.get_selected_table()
        if selected_table:
            selected_row = self.get_selected_row()
            if selected_row:
                self.crud_frame.destroy()
                self.crud_frame = tk.Frame(self.admin_frame)
                print(selected_row)
                # Showing editable fields
                self.edited_row = {}
                for i, key in enumerate(selected_row):
                    label = tk.Label(self.crud_frame, text=key)
                    label.pack(pady=5)

                    entry_var = tk.StringVar(value=selected_row[key])
                    entry = tk.Entry(self.crud_frame, width=30, textvariable=entry_var)
                    entry.pack(pady=10)
                    entry.config(state="readonly")

                    # Almacena la variable asociada al Entry en el diccionario
                    self.edited_row[key] = entry_var

                tk.Button(self.crud_frame, text="Save", command=self.save_changes_delete).pack(pady=5)
                tk.Button(self.crud_frame, text="Cancel", command=self.cancel_changes).pack(pady=5)
                self.crud_frame.pack()

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
            self.edited_row = {}

            # Showing editable fields
            for i, key in enumerate(selected_row):
                label = tk.Label(self.crud_frame, text=key)
                label.pack(pady=5)

                # Condición para hacer editable solo el primer elemento
                if i != 0:
                    entry_var = tk.StringVar()
                    entry = tk.Entry(self.crud_frame, width=30, textvariable=entry_var)
                    entry.pack(pady=10)

                    # Almacena la variable asociada al Entry en el diccionario
                    self.edited_row[key] = entry_var
                else:
                    label_value = tk.Label(self.crud_frame)
                    label_value.pack(pady=10)

            tk.Button(self.crud_frame, text="Save", command=self.save_changes_add).pack(pady=5)
            tk.Button(self.crud_frame, text="Cancel", command=self.cancel_changes).pack(pady=5)
            self.crud_frame.pack()
            print(self.edited_row)

    def save_changes_add(self):
        # Save changes for adding data
        connection = self.database.get_connection()
        cursor = connection.cursor()
        try:
            print(self.get_selected_table())
            table = self.get_selected_table()

            # Valores del diccionario menos el primero, ya que ese no se debe editar
            # Obtengo a los valores de la key en forma de tupla,y luego los coloco en el formato necesario para la Query
            tuple_key = tuple(self.edited_row.keys())
            str_key = "("
            for key in tuple_key:
                if (key != tuple_key[-1]):
                    str_key = str_key + key + ","
                else:
                    str_key = str_key + key
            str_key = str_key + ")"
            # Valores del diccionario en forma de tupla
            tuple_value = tuple(var.get() for var in self.edited_row.values())
            if len(tuple_key) == 1:
                print(f"INSERT INTO {table} ({tuple_key[0]}) VALUES ('{tuple_value[0]}')")
                cursor.execute(f"INSERT INTO {table} ({tuple_key[0]}) VALUES ('{tuple_value[0]}')")
            else:
                print(f"INSERT INTO {table} {str_key} VALUES {tuple_value}")
                cursor.execute(f"INSERT INTO {table} {str_key} VALUES {tuple_value}")
            connection.commit()
            print("Insercion exitosa")
        except Exception as e:
            messagebox.showerror("Error", f"Error adding new data: {e}")

        finally:
            cursor.close()

        self.show_rows(self)

    def save_changes_update(self):
        # Save changes for adding data
        connection = self.database.get_connection()
        cursor = connection.cursor()
        try:
            print(self.get_selected_table())
            table = self.get_selected_table()
            # Valores del diccionario menos el primero, ya que ese no se debe editar
            # Obtengo a los valores de la key en forma de tupla,y luego los coloco en el formato necesario para la Query
            tuple_key = tuple(self.edited_row.keys())
            tuple_value = tuple(var.get() for var in self.edited_row.values())
            for key,value in zip(tuple_key,tuple_value):
                if key != tuple_key[0]:
                    print(f"UPDATE {table} SET {key} = '{value}' WHERE {tuple_key[0]} = '{tuple_value[0]}'")
                    cursor.execute(f"UPDATE {table} SET {key} = '{value}' WHERE {tuple_key[0]} = '{tuple_value[0]}'")
            connection.commit()
            print("Insercion exitosa")
        except Exception as e:
            messagebox.showerror("Error", f"Error adding new data: {e}")

        finally:
            cursor.close()

        self.show_rows(self)

    def save_changes_delete(self):
        # Save changes for adding data
        connection = self.database.get_connection()
        cursor = connection.cursor()
        try:
            print(self.get_selected_table())
            table = self.get_selected_table()
            # Valores del diccionario menos el primero, ya que ese no se debe editar
            # Obtengo a los valores de la key en forma de tupla,y luego los coloco en el formato necesario para la Query
            tuple_key = tuple(self.edited_row.keys())
            tuple_value = tuple(var.get() for var in self.edited_row.values())

            print(f"DELETE FROM {table} WHERE {tuple_key[0]} = '{tuple_value[0]}'")
            cursor.execute(f"DELETE FROM {table} WHERE {tuple_key[0]} = '{tuple_value[0]}'")
            connection.commit()
            print("Insercion exitosa")
        except Exception as e:
            messagebox.showerror("Error", f"Error adding new data: {e}")

        finally:
            cursor.close()

        self.show_rows(self)

    def cancel_changes(self):
        self.show_rows(self)

    def logout(self):
        if self.logout_callback:
            self.logout_callback()

    def get_selected_table(self):
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
