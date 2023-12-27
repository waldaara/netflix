import tkinter as tk
from tkinter import messagebox

import MySQLdb

from views.admin_view import AdminView
from views.user_view import UserView
from lib.db import MySQL


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Netflix")
        self.root.geometry("700x500")  # Tamaño de la ventana

        # Variables de email y contraseña
        self.email_var = tk.StringVar()
        self.password_var = tk.StringVar()

        # Frame de inicio de sesión
        self.login_frame = tk.Frame(root, padx=10, pady=10)
        self.login_frame.pack()

        # Etiquetas y campos de entrada para usuario y contraseña
        tk.Label(self.login_frame, text="Email:").grid(row=0, column=0, sticky=tk.E)
        tk.Entry(self.login_frame, textvariable=self.email_var).grid(row=0, column=1)
        tk.Label(self.login_frame, text="Contraseña:").grid(row=1, column=0, sticky=tk.E)
        tk.Entry(self.login_frame, textvariable=self.password_var, show="*").grid(row=1, column=1)

        # Botón de inicio de sesión
        tk.Button(self.login_frame, text="Iniciar Sesión", command=self.login).grid(row=2, column=0, columnspan=2)

        # Frame de interfaz de usuario o admin (inicialmente vacío)
        self.current_interface_frame = tk.Frame(root, padx=10, pady=10)

    def login(self):
        # Verificar el usuario y la contraseña (ejemplo básico)
        email = self.email_var.get().strip().lower()
        password = self.password_var.get().strip().lower()

        if email == "admin@admin.com" and password == "admin":
            return self.show_admin_interface()

        # Get the singleton instance
        database = MySQL()

        # Use the database connection
        connection = database.get_connection()

        try:
            # Create a cursor to interact with the database
            cursor = connection.cursor()

            # Execute query
            cursor.execute(f"SELECT correo_cuenta, contrasena FROM cuenta WHERE correo_cuenta = '{email}' AND contrasena = '{password}'")

            # Fetch all the rows
            rows = cursor.fetchall()

            if len(rows) == 1:
                return self.show_user_interface()

        except MySQLdb.Error as e:
            print("MySQL Error:", e)

        finally:
            # Close the cursor
            cursor.close()

        messagebox.showerror("Error de inicio de sesión", "Usuario o contraseña incorrectos")

    def show_admin_interface(self):
        # Ocultar el marco de inicio de sesión
        self.login_frame.pack_forget()

        # Destruir la interfaz actual (si existe)
        if hasattr(self.current_interface_frame, 'destroy'):
            self.current_interface_frame.destroy()

        # Crear la interfaz de administrador y pasar el callback de cierre de sesión
        admin_interface = AdminView(self.root, self.logout)
        self.current_interface_frame = admin_interface

    def show_user_interface(self):
        # Ocultar el marco de inicio de sesión
        self.login_frame.pack_forget()

        # Destruir la interfaz actual (si existe)
        if hasattr(self.current_interface_frame, 'destroy'):
            self.current_interface_frame.destroy()

        # Crear la interfaz de usuario y pasar el callback de cierre de sesión
        user_interface = UserView(self.root, self.logout)
        self.current_interface_frame = user_interface

    def logout(self):
        # Destruir la interfaz actual
        self.current_interface_frame.destroy()

        # Volver a mostrar el marco de inicio de sesión
        self.login_frame.pack()


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
