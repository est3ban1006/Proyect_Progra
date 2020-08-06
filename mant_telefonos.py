from tkinter import * 
from tkinter import font
from tkinter import messagebox as msg
from tkinter import ttk 


from tksheet import Sheet 

from tkcalendar import Calendar, DateEntry 

#Incluye el objeto de persona
from modelo import Telefono
from modelo import Persona


from modelo import TelefonosBO
from modelo import PersonoBO

class MantTelefonos():
    

    def __init__(self, parent):
        self.parent = parent

        
        self.raiz = Toplevel(self.parent) #para crear ventanas secundarias
        self.raiz.title ("Mantenimiento de Telefonos")
        self.raiz.geometry('900x510') 

        menubar = Menu(self.raiz)
        self.raiz.config(menu=menubar)

        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Acerca de..")
        filemenu.add_separator()
        filemenu.add_command(label="Salir", command=self.raiz.quit)

        mantmenu = Menu(menubar, tearoff=0)
        mantmenu.add_command(label="Personas", command=self.mostrar_mant_personas)
        mantmenu.add_command(label="Direcciones")

        menubar.add_cascade(label="Archivo", menu=filemenu)
        menubar.add_cascade(label="Mantenimiento", menu=mantmenu)

        #*************************************************************************
        #crea un objeto tipo fuenta
        #*************************************************************************
        self.fuente = font.Font(weight="bold")

        #*************************************************************************
        #se crean atributos de la clase
        #*************************************************************************
        self.telefono = Telefono.Telefono() #se crea el objeto de dominio para guardar la información
        self.insertando = True
        self.nombrePersona = StringVar() #crea un objeto de tipo string var para asociarlo al nombre de la persona 

        self.persona = Persona.Persona()
        
        #*************************************************************************
        #se crean los campos de la pantalla
        #*************************************************************************

        #Se coloca un label del titulo
        self.lb_tituloPantalla = Label(self.raiz, text = "MANTENIMIENTO DE TELEFONOS", font = self.fuente)
        self.lb_tituloPantalla.place(x = 320, y = 20) #colocar por medio de espacion en pixeles de la parte superior de la pantalla considerando un eje x y un eje y
        
        #coloca en el formulario el campo y el label de cedula
        self.lb_cedula = Label(self.raiz, text = "Cedula:")
        self.lb_cedula.place(x = 240, y = 60)
        self.txt_cedula = Entry(self.raiz, textvariable=self.telefono.cedula, justify="right", width=12)
        self.txt_cedula.place(x = 370, y = 60)

        #coloca el boton de consultar persona
        self.bt_consultar = Button(self.raiz, text="Consultar", width=15, command = self.consultarNombre)
        self.bt_consultar.place(x = 512, y = 60)

        #coloca en el formulario el campo y el label de nombre
        self.lb_nombre = Label(self.raiz, text = "Nombre:")
        self.lb_nombre.place(x = 240, y = 90)
        self.txt_nombre = Entry(self.raiz, textvariable=self.nombrePersona, justify="right", width=30)
        self.txt_nombre.place(x = 370, y = 90)

        #coloca en el formulario el campo y el label de telefono
        self.lb_telefono = Label(self.raiz, text = "Telefono:")
        self.lb_telefono.place(x = 240, y = 120)
        self.txt_telefono = Entry(self.raiz, textvariable=self.telefono.telefono, justify="right", width=30)
        self.txt_telefono.place(x = 370, y = 120)


        #coloca en el formulario el campo y el label de descripcion
        self.lb_descripcion = Label(self.raiz, text = "Descripción:")
        self.lb_descripcion.place(x = 240, y = 150)
        self.txt_descripcion = Entry(self.raiz, textvariable=self.telefono.descripcion, justify="right", width=30)
        self.txt_descripcion.place(x = 370, y = 150)

        #coloca los botones enviar y borrar
        self.bt_borrar = Button(self.raiz, text="Limpiar", width=15, command=self.limpiarInformacion)
        self.bt_borrar.place(x = 370, y = 180)

        self.bt_enviar = Button(self.raiz, text="Enviar", width=15, command=self.enviarInformacion)
        self.bt_enviar.place(x = 510, y = 180)

        #Se coloca un label del informacion
        self.lb_tituloPantalla = Label(self.raiz, text = "INFORMACIÓN INCLUIDA", font = self.fuente)
        self.lb_tituloPantalla.place(x = 350, y = 230) #colocar por medio de espacion en pixeles de la parte superior de la pantalla considerando un eje x y un eje y

        #*************************************************************************
        #tabla con informacion
        #*************************************************************************
        
        self.sheet = Sheet(self.raiz,
                            page_up_down_select_row = True,
                            column_width = 120,
                            startup_select = (0,1,"rows"),
                            headers = ['Cédula', 'Nombre', 'Telefono', 'Descripción'],
                            height = 195, #height and width arguments are optional
                            width = 720 #For full startup arguments see DOCUMENTATION.md
                            )
        
        self.sheet.enable_bindings(("single_select", 
                                    "column_select",
                                    "row_select",
                                    "column_width_resize",
                                    "double_click_column_resize",
                                    "arrowkeys",
                                    "row_height_resize",
                                    "double_click_row_resize",
                                    "right_click_popup_menu",
                                    "rc_select",
                                    "rc_insert_column",
                                    "rc_delete_column",
                                    "rc_insert_row",
                                    "rc_delete_row"))
        self.sheet.place(x = 20, y = 260)

        #*************************************************************************
        #coloca los botones cargar y eliminar
        #*************************************************************************
        self.bt_cargar = Button(self.raiz, text="Cargar", width=15, command=self.cargarInformacion)
        self.bt_cargar.place(x = 750, y = 255)

        self.bt_eliminar = Button(self.raiz, text="Eliminar", width=15, command=self.eliminarInformacion)
        self.bt_eliminar.place(x = 750, y = 295)
        
        #*************************************************************************
        #se llama el metodo para cargar la informacion
        #*************************************************************************
        self.cargarTodaInformacion()

        #*************************************************************************
        #se inicial el main loop de la pantalla
        #*************************************************************************
        
        #Esconde la pantalla principal sin destruirla
        self.parent.withdraw()

        #Se configura el evento al cerrar la pantalla hija
        self.raiz.protocol("WM_DELETE_WINDOW", self.on_closing) #cuando se cierra la pantalla hija debe cerrar la principal



    def enviarInformacion(self):
        try:
            self.telefonoBo = TelefonosBO.TelefonosBO() #se crea un objeto de logica de negocio
            if(self.insertando == True):
                self.telefonoBo.guardar(self.telefono)
            else:
                self.telefonoBo.modificar(self.telefono)
            
            self.cargarTodaInformacion()
            self.telefono.limpiar()
            self.nombrePersona.set("")

            if(self.insertando == True):
                msg.showinfo("Acción: Agregar teléfono", "La información del teléfono ha sido incluida correctamente") # Se muestra el mensaje de que todo esta correcto
            else:
                msg.showinfo("Acción: Modificar teléfono", "La información del teléfono ha sido modificada correctamente") # Se muestra el mensaje de que todo esta correcto
            
            self.insertando = True

        except Exception as e: 
            msg.showerror("Error",  str(e)) #si se genera algun tipo de error muestra un mensache con dicho error


    def limpiarInformacion(self):
        self.telefono.limpiar() #llama al metodo de la clase persona para limpiar los atritudos de la clase
        self.nombrePersona.set("")
        self.insertando = True
        msg.showinfo("Acción del sistema", "La información del formulario ha sido eliminada correctamente") # muestra un mensaje indicando que se limpio el formulario



    def consultarNombre(self):
        try:
            self.personaBo = PersonoBO.PersonaBO()
            self.persona.cedula.set(self.telefono.cedula.get()) #setea la cédula de la persona
            self.personaBo.consultarPersona(self.persona) #se envia a consultar
            if self.persona.nombre.get() == "" :
                self.nombrePersona = "No existe la persona "
            else:
                self.nombrePersona.set(self.persona.nombre.get() + " " + self.persona.apellido1.get() + " " + self.persona.apellido2.get())

        except Exception as e: 
            msg.showerror("Error",  str(e)) #si se genera algun tipo de error muestra un mensache con dicho error


    def cargarTodaInformacion(self):
        try:
            self.telefonosBo = TelefonosBO.TelefonosBO() #se crea un objeto de logica de negocio
            resultado = self.telefonosBo.consultar()

            self.sheet.set_sheet_data(resultado)
        except Exception as e: 
            msg.showerror("Error",  str(e)) #si se genera algun tipo de error muestra un mensache con dicho error


    def cargarInformacion(self):
        try:
            datoSeleccionado = self.sheet.get_currently_selected()
            telefono = (self.sheet.get_cell_data(datoSeleccionado[0],2))
            self.telefono.telefono.set(telefono)
            self.telefonoBo = TelefonosBO.TelefonosBO() #se crea un objeto de logica de negocio
            self.telefonoBo.consultarTelefono(self.telefono) #se envia a consultar
            self.consultarNombre()
            self.insertando = False
            msg.showinfo("Acción: Consultar teléfono", "La información del teléfono ha sido consultada correctamente") # Se muestra el mensaje de que todo esta correcto
            
        except Exception as e: 
            msg.showerror("Error",  str(e)) #si se genera algun tipo de error muestra un mensache con dicho error



    def eliminarInformacion(self):
        try:
            datoSeleccionado = self.sheet.get_currently_selected()
            telefono = (self.sheet.get_cell_data(datoSeleccionado[0],2))
            nombre = (self.sheet.get_cell_data(datoSeleccionado[0],1))

            resultado = msg.askquestion("Eliminar",  "¿Desear eliminar el telefono "+telefono+" de "+nombre+" de la base de datos?")
            if resultado == "yes":
                self.telefono.telefono.set(telefono)
                self.telefonoBo = TelefonosBO.TelefonosBO() #se crea un objeto de logica de negocio
                self.telefonoBo.eliminar(self.telefono) #se envia a consultar
                self.cargarTodaInformacion()
                self.telefono.limpiar()
                self.nombrePersona.set("")

        except Exception as e: 
            msg.showerror("Error",  str(e)) #si se genera algun tipo de error muestra un mensache con dicho error


    def mostrar_mant_personas(self):
        self.parent.deiconify()
        self.raiz.destroy()

    def on_closing(self):
       self.parent.destroy()

  

