import tkinter as tk


class UserView:
    def __init__(self, root, logout_callback):
        self.root = root
        self.logout_callback = logout_callback

        # Frame de interfaz de usuario
        self.user_frame = tk.Frame(root, padx=10, pady=10)
        self.user_frame.pack()

        tk.Label(self.user_frame, text="Interfaz de Usuario").pack()

        # Botón de cerrar sesión
        tk.Button(self.user_frame, text="Cerrar Sesión", command=self.logout).pack()

    def logout(self):
        # Destruir el marco de interfaz de usuario
        self.user_frame.destroy()

        # Llamar al callback de cierre de sesión proporcionado por el objeto principal
        if self.logout_callback:
            self.logout_callback()

    def destroy(self):
        # Método para permitir la destrucción del objeto desde el exterior
        self.user_frame.destroy()
