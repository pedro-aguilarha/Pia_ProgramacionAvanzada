import datetime
#import librearia para usar los datos tipo fechas
class CONTACTO:
     #se crea el metodo _init_ para construir un objeto de la clase CONTACTO
    def __init__(self,NICKNAME,NOMBRE,CORREO,TELEFONO,
                 FECHA_NACIMIENTO,GASTO,REGISTRO= datetime.datetime.now()):
                 #self se ultiliza para llamar al objeto en si
        self.NICKNAME = NICKNAME    #se refiere al usuario como un id
        self.NOMBRE = NOMBRE
        self.CORREO  = CORREO
        self.TELEFONO = TELEFONO
        self.FECHA_NACIMIENTO = str(FECHA_NACIMIENTO)
        self.GASTO= GASTO                      # en gasto se almacenan los gastos del mes
        self.REGISTRO = str(REGISTRO)        # en registro se tiene la fecha en la que se crea
         # se convierte registro a str       # el objeto como defalut por lo tanto al instanciarlo
          # para que no ocurra errores       #no se necesita colocar ese atributo
          # al momento de convertilo a json
