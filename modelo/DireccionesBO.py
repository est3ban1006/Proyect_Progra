import mysql.connector 



class DireccionesBO:

    def __init__(self):
 
        self.db = mysql.connector.connect(host ="localhost", 
                                     user = "root", 
                                     password = "root", 
                                     db ="mydb") 

    def __del__(self):
        self.db.close() 
  
    def guardar(self, direccion):
        try:
            if(self.validar(direccion)):#se valida que tenga la información

                if(not self.exist(direccion)): #si no existe lo agrega
                    direccion.lastUser = "ChGari"
                    
                    insertSQL = "INSERT INTO Direcciones (`PKA_ID_Direccion`, `PK_FK_cedula`, `nom_Lugar`,`direccion`, `lastUser`, `lastModification`) VALUES (%s, %s, %s, %s, CURDATE())"
                    insertValores =  (direccion.direccion.get(),direccion.cedula.get(),direccion.nomb_Lugar.get(), direccion.lastUser)
                    cursor = self.db.cursor() #crea un cursos con la conexión lo que nos permite conectarnos a la base de datos
                    cursor.execute(insertSQL, insertValores) #ejecuta el SQL con las valores
                    self.db.commit() #crea un commit en la base de datos
                else:
                    raise Exception('La cedula indicada en el formulario existe en la base de datos')  # si existe el registro con la misma cedual genera el error
            else:
                raise Exception('Los datos no fueron digitados por favor validar la información')  # si no tiene todos los valores de genera un error
        except mysql.connector.Error as e:
            raise Exception(str(e)) 
        except Exception as e: 
            raise Exception(str(e)) 
    
    def exist(self , direccion):
        try:
            existe = False
            selectSQL = "Select * from Direccion where PKA_ID_DIRECCION = " + direccion.direccion.get()
            cursor = self.db.cursor()
            cursor.execute(selectSQL)
            if (cursor.fetchone()) : #Metodo obtiene un solo registro o none si no existe información
                existe  = True

            return existe
            
        except mysql.connector.Error as e:
            print("Something went wrong: {}".format(e))
            raise Exception(str(e)) 
        except Exception as e: 
            raise Exception(str(e)) 


    def validar (self, direccion):
        valido = True
        direccion.printInfo()
        if direccion.cedula.get() == "" :
            valido = False
        
        if direccion.nomb__Lugar.get() == "" :
            valido = False

        if direccion.direccion.get() == "" :
            valido = False

        return valido

    def consultar(self ):
        try:
            selectSQL = 'select t.PK_FK_cedula as cedula, \
                            CONCAT( p.nombre, " ", p.apellido1, " ", p.apellido2 ) as nombre, \
                            t.pk_direccion as direccion, \
                            t.descripcion \
                        from Direcciones t inner join personas p on t.PK_FK_cedula = p.pk_cedula'
            cursor = self.db.cursor()
            cursor.execute(selectSQL)
            myresult = cursor.fetchall()
            final_result = [list(i) for i in myresult]
            return final_result
            
        except mysql.connector.Error as e:
            print("Something went wrong: {}".format(e))
            raise Exception(str(e)) 
        except Exception as e: 
            raise Exception(str(e)) 


    def consultarDireccion(self, direccion):
        try:
            selectSQL = "Select * from Direcciones where PKA_ID_DIRECCION = " + direccion.direccion.get()
            cursor = self.db.cursor()
            cursor.execute(selectSQL)
            personaDB = cursor.fetchone()
            if (personaDB) : #Metodo obtiene un solo registro o none si no existe información
                direccion.direccion.set(personaDB[0])
                direccion.cedula.set(personaDB[1])
                direccion.nomb_Lugar.set(personaDB[2])
            else:
                raise Exception("La cédula consultada no existe en la base de datos") 
            
        except mysql.connector.Error as e:
            print("Something went wrong: {}".format(e))
            raise Exception(str(e)) 
        except Exception as e: 
            raise Exception(str(e)) 

    def eliminar(self, direccion):
        try:
            deleteSQL = "delete  from Direcciones where PKA_ID_DIRECCION = " + direccion.direccion.get()
            cursor = self.db.cursor() #crea un cursos con la conexión lo que nos permite conectarnos a la base de datos
            cursor.execute(deleteSQL) #ejecuta el SQL con las valores
            self.db.commit() #crea un commit en la base de datos
        except mysql.connector.Error as e:
            print("Something went wrong: {}".format(e))
            raise Exception(str(e)) 
        except Exception as e: 
            if str(e) == "tiene FK":
                raise Exception("El dato no se puede eliminar por que tiene datos asociados, por favor eliminarlos primero")     
            else:
                raise Exception(str(e)) 


    def modificar(self, direccion):
        try:
            if(self.validar(direccion)):#se valida que tenga la información

                if(self.exist(direccion)): #si  existe lo modifica
                    telefono.lastUser = "asas"
                    updateSQL = "UPDATE Direcciones  set `PK_FK_cedula` = %s, `nom_Lugar` = %s, `lastUser` = %s, `lastModification` = CURDATE() WHERE `PK_telefono` =  %s"
                    updateValores =  (direccion.cedula.get(),direccion.nomb_Lugar.get(),direccion.lastUser, direccion.direccion.get())
                    #print(insertValores)
                    cursor = self.db.cursor() #crea un cursos con la conexión lo que nos permite conectarnos a la base de datos
                    cursor.execute(updateSQL, updateValores) #ejecuta el SQL con las valores
                    self.db.commit() #crea un commit en la base de datos
                else:
                    raise Exception('La cédula indicada en el formulario no existe en la base de datos')  # si existe el registro con la misma cedual genera el error
            else:
                raise Exception('Los datos no fueron digitados por favor validar la información')  # si no tiene todos los valores de genera un error
        except mysql.connector.Error as e:
            raise Exception(str(e)) 
        except Exception as e: 
            raise Exception(str(e)) 
    