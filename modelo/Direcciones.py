from tkinter import StringVar #Para asociar los campos de texto con el compomente texto
from tkinter import IntVar #Para asociar los campos de numero con el compomente radio

class Direccion: #POJO

    def __init__(self):
        self.cedula = StringVar()
        self.nomb_Lugar = StringVar()
        self.direccion = StringVar()
        self.apellido2 = StringVar()
        self.lastUser = ""
        self.lastModification = StringVar()

    def limpiar(self):
        self.cedula.set("")
        self.nomb_Lugar.set("")
        self.direccion.set("")
      

    def printInfo(self):
        print(f"Cedula:{self.cedula.get()}")
        print(f"Nombre del Lugar:{self.nomb_Lugar.get()}")
        print(f"Direccion:{self.direccion.get()}")
   