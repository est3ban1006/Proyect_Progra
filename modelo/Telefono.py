from tkinter import StringVar #Para asociar los campos de texto con el compomente texto
from tkinter import IntVar #Para asociar los campos de numero con el compomente radio

class Telefono: #POJO

    def __init__(self):
        self.cedula = StringVar()
        self.telefono = StringVar()
        self.descripcion = StringVar()
        self.lastUser = ""
        self.lastModification = StringVar()

    def limpiar(self):
        self.cedula.set("")
        self.telefono.set("")
        self.descripcion.set("")

    def printInfo(self):
        print(f"Cedula:{self.cedula.get()}")
        print(f"Telefono:{self.telefono.get()}")
        print(f"Descripcion:{self.descripcion.get()}")

    
        