import tkinter as tk
from tkinter import END, ACTIVE

import MySQLdb
from lib.db import MySQL


class UserView:

    def __init__(self, root, logout_callback):
        self.root = root
        self.logout_callback = logout_callback

        # Frame de interfaz de usuario
        self.user_frame = tk.Frame(root, padx=10, pady=10)
        self.user_frame.grid()

        tk.Label(self.user_frame, text="Netflix", font=("Arial", 25)).grid(row=0, column=0, padx=(0, 600), pady=(0, 0))

        # Botón de cerrar sesión
        tk.Button(self.user_frame, text="Cerrar Sesión", command=self.logout).grid(row=0, padx=(600, 0), pady=(0, 0))
        self.userOptions()
        # self.getProfiles()

    def logout(self):
        # Destruir el marco de interfaz de usuario
        self.user_frame.destroy()

        # Llamar al callback de cierre de sesión proporcionado por el objeto principal
        if self.logout_callback:
            self.logout_callback()

    def destroy(self):
        # Método para permitir la destrucción del objeto desde el exterior
        self.user_frame.destroy()

    def chargeMovies(self):

        database = MySQL()
        connection = database.get_connection()

        try:
            # Create a cursor to interact with the database
            cursor = connection.cursor()

            # Execute query
            cursor.execute("SELECT pelicula.titulo FROM pelicula")

            # Fetch all the rows
            rows = cursor.fetchall()
            data = []

            for row in rows:
                data.append(row[0])

            self.searchBar(data)

        except MySQLdb.Error as e:
            print("MySQL Error:", e)

        finally:
            # Close the cursor
            cursor.close()

    def chargeseries(self):

        database = MySQL()
        connection = database.get_connection()

        try:
            # Create a cursor to interact with the database
            cursor = connection.cursor()

            # Execute query
            cursor.execute("SELECT serie.titulo FROM serie")

            # Fetch all the rows
            rows = cursor.fetchall()
            data = []

            for row in rows:
                data.append(row[0])

            self.searchBar(data)

        except MySQLdb.Error as e:
            print("MySQL Error:", e)

        finally:
            # Close the cursor
            cursor.close()

    def getProfiles(self):


        database = MySQL()
        connection = database.get_connection()

        try:
            # Create a cursor to interact with the database
            cursor = connection.cursor()

            # Execute query
            cursor.execute("SELECT p.nombre"
                           "FROM perfil p JOIN cuenta USING(correo_cuenta)")

            # Fetch all the rows
            rows = cursor.fetchall()
            data = []

            for row in rows:
                data.append(row[0])

            self.showProfile(data)

        except MySQLdb.Error as e:
            print("MySQL Error:", e)

        finally:
            # Close the cursor
            cursor.close()

    def showProfile(self, listProfiles):
        for profile in listProfiles:
            tk.Button(self.user_frame, text= profile, width=50)

    def userOptions(self):
        moviesButton = tk.Button(self.user_frame, text="Find movies", width=12, command=self.chargeMovies)
        seriesButton = tk.Button(self.user_frame, text="Find series", width=12, command=self.chargeseries)
        myListButton = tk.Button(self.user_frame, text="Your list", width=12)

        moviesButton.grid(row=1, column=0, padx=(0, 600), pady=(0, 5))
        seriesButton.grid(row=2, column=0, padx=(0, 600), pady=(0, 5))
        myListButton.grid(row=3, column=0, padx=(0, 600), pady=(0, 5))

    def update(self, data, my_List):
        my_List.delete(0, END)
        for item in data:
            my_List.insert(END, item)

    def searchBar(self, rows):
        my_Label = tk.Label(self.user_frame, text="Start Typing...")
        my_Label.grid(row=1, padx=(200, 0), pady=(0, 0))
        my_Entry = tk.Entry(self.user_frame)
        my_Entry.grid(row=2, padx=(200, 0), pady=(0, 0))
        my_List = tk.Listbox(self.user_frame, width=50)
        my_List.grid(row=4, padx=(200, 0), pady=(0, 0))
        self.update(rows, my_List)

        def fillout(e):
            my_Entry.delete(0, END)
            my_Entry.insert(0, my_List.get(ACTIVE))

        def check(e):
            typed = my_Entry.get()
            if typed == "":
                data = rows
            else:
                data = []
                for item in rows:
                    if typed.lower() in item.lower():
                        data.append(item)
            self.update(data, my_List)

        my_List.bind("<<ListboxSelect>>", fillout)
        my_Entry.bind("<KeyRelease>", check)

# david.miller@email.com
