from PyQt5.QtWidgets import QApplication

from .Vista_lista_autos import Vista_lista_autos
from .Vista_lista_mantenimientos import Vista_lista_mantenimientos
from .Vista_auto import Vista_auto
from .Vista_lista_acciones import Vista_lista_acciones
from .Vista_reporte_gastos import Vista_reporte_gastos

class App_AutoPerfecto(QApplication):
    """
    Clase principal de la interfaz que coordina las diferentes vistas/ventanas de la aplicación
    """
    __lista_autos = []
    __lista_mantenimientos = []
    __lista_acciones_auto = []

    def __init__(self, sys_argv, logica):
        """
        Constructor de la interfaz. Debe recibir la lógica e iniciar la aplicación en la ventana principal.
        """
        super(App_AutoPerfecto, self).__init__(sys_argv)
        self.__lista_autos = []
        self.__lista_mantenimientos = []
        self.__lista_acciones_auto = []
        self.logica = logica
        self.mostrar_vista_lista_autos()


    def mostrar_vista_lista_autos(self):
        """
        Esta función inicializa la ventana de la lista de automóviles
        """
        print('************** Método mostrar_vista_lista_autos **************')
        self.__lista_autos = self.logica.dar_autos()
        self.vista_lista_autos = Vista_lista_autos(self)
        self.vista_lista_autos.mostrar_autos(self.__lista_autos)

    def guardar_auto(self, marca, placa, modelo, kilometraje, color, cilindraje, tipo_combustible):
        """
        Esta función guarda un nuevo auto o los cambios sobre una existente
        """
        print('************** Método guardar_auto **************')
        if self.logica.validar_crear_editar_auto(marca, placa, modelo, kilometraje, color, cilindraje, tipo_combustible)==True:
            if self.auto_actual == -1:
                if self.logica.crear_auto(marca, placa, modelo, kilometraje, color, cilindraje, tipo_combustible) != True:
                    self.vista_lista_autos.error_crear_auto_existente()
            else:
                if self.logica.editar_auto(self.auto_actual, marca, placa, modelo, kilometraje, color, cilindraje, tipo_combustible) != True:
                    self.vista_lista_autos.error_editar_auto_no_existe()
            self.vista_lista_autos.mostrar_autos(self.logica.dar_autos())
        else:
            return False

    def vender_auto(self, kilometrajeVenta, valorVenta):
        """
        Esta función actualiza la venta de un auto
        """
        print('************** Método vender_auto **************')
        if self.logica.validar_vender_auto(self.auto_actual, kilometrajeVenta, valorVenta):
            if self.logica.vender_auto(self.auto_actual, float(kilometrajeVenta), float(valorVenta)):
                self.vista_lista_autos.mostrar_autos(self.logica.dar_autos())
                return True
            else:
                self.vista_lista_autos.error_vender_auto_acciones()
        else:
            self.vista_lista_autos.error_vender_auto()
            return False
        #self.vista_lista_autos.mostrar_autos(self.logica.dar_autos())

    def aniadir_mantenimiento(self, nombre, descripcion):
        """
        Esta función inserta un mantenimiento a la aplicación
        """
        print('************** Método aniadir_mantenimiento **************')
        if self.logica.validar_crear_editar_mantenimiento(nombre, descripcion):
            if self.logica.aniadir_mantenimiento(nombre, descripcion) != True: 
                self.vista_lista_mantenimientos.error_mantenimiento_existe()
        else:
            self.vista_lista_mantenimientos.error_mantenimiento()
        self.vista_lista_mantenimientos.mostrar_mantenimientos(self.logica.dar_mantenimientos())

    def editar_mantenimiento(self, id, nombre, descripcion):
        """
        Esta función edita la información de un mantenimiento
        """
        print('************** Método editar_mantenimiento **************')
        if self.logica.validar_crear_editar_mantenimiento(nombre, descripcion):
            print('Paso validacion parametros -->')
            if self.logica.editar_mantenimiento(nombre, descripcion) != True:
                self.vista_lista_mantenimientos.error_mantenimiento_no_existe()
        else:
            self.vista_lista_mantenimientos.error_mantenimiento()
        self.vista_lista_mantenimientos.mostrar_mantenimientos(self.logica.dar_mantenimientos())

    def mostrar_mantenimientos(self):
        """
        Esta función muestra la ventana con la lista de mantenimientos
        """
        print('************** Método mostrar_mantenimientos **************')
        self.__lista_mantenimientos = self.logica.dar_mantenimientos()
        self.vista_lista_mantenimientos=Vista_lista_mantenimientos(self)
        self.vista_lista_mantenimientos.mostrar_mantenimientos(self.__lista_mantenimientos)

    def dar_mantenimientos(self):
        """
        Esta función retorna la lista de mantenimientos desde la lógica
        """
        print('************** Método dar_mantenimientos **************')
        return self.logica.dar_mantenimientos()

    def mostrar_acciones(self, id_auto):
        """
        Esta función muestra las acciones de un auto
        """
        print('************** Método mostrar_acciones **************')
        self.auto_actual = id_auto
        marca_auto = self.logica.dar_auto(id_auto)['placa']
        self.__lista_acciones_auto = self.logica.dar_acciones_auto(id_auto)
        print('self.__lista_acciones_auto -->>>')
        print(self.__lista_acciones_auto)
        
        self.vista_lista_acciones=Vista_lista_acciones(self)
        self.vista_lista_acciones.mostrar_acciones(marca_auto, self.__lista_acciones_auto)

    def dar_accion(self, id_accion):
        """
        Esta función retorna la información de una acción particular
        """
        print('************** Método dar_accion **************')
        return self.logica.dar_accion(self.auto_actual, id_accion)

    def aniadir_accion(self, mantenimiento, valor, kilometraje, fecha):
        """
        Esta función crea una nueva acción asociada a un auto
        """
        print('************** Método aniadir_accion **************')
        if self.logica.validar_crear_editar_accion( mantenimiento, self.auto_actual, valor, kilometraje, fecha):
            self.logica.crear_accion(mantenimiento, self.auto_actual, float(valor), float(kilometraje), fecha)
            nombre_auto = self.logica.dar_auto(self.auto_actual)['placa']
            self.vista_lista_acciones.mostrar_acciones(nombre_auto, self.logica.dar_acciones_auto(self.auto_actual))
        else:
            self.vista_lista_acciones.error_crear_editar_accion()

    def editar_accion(self, id, mantenimiento, valor, kilometraje, fecha):
        """
        Esta función crea una nueva acción asociada a un auto
        """
        print('************** Método editar_accion **************')
        if self.logica.validar_crear_editar_accion(mantenimiento, self.auto_actual, valor, kilometraje, fecha):
            self.logica.editar_accion(id, mantenimiento, self.auto_actual, valor, kilometraje, fecha)
            nombre_auto = self.logica.dar_auto(self.auto_actual)['placa']
            self.vista_lista_acciones.mostrar_acciones(nombre_auto, self.logica.dar_acciones_auto(self.auto_actual))
        else:
            self.vista_lista_acciones.error_crear_editar_accion()

    def eliminar_auto(self, indice_auto):
        """
        Esta función elimina un auto
        """
        print('************** Método eliminar_auto **************')
        print('self.__lista_autos -->>>')
        print(self.__lista_autos)
        print('Auto Actual -->>>', indice_auto)
        auto = self.__lista_autos[indice_auto]
        print('Auto Actual -->>>', auto)
        self.logica.eliminar_auto(auto['id'])
        self.vista_lista_autos.mostrar_autos(self.logica.dar_autos())

    def mostrar_reporte_gastos(self):
        """
        Esta función muestra el reporte de gastos para un auto
        """
        print('************** Método mostrar_reporte_gastos **************')
        lista_gastos, valor_kilometro = self.logica.dar_reporte_ganancias(self.auto_actual)
        self.vista_reporte_gastos = Vista_reporte_gastos(self)
        self.vista_reporte_gastos.mostrar_gastos(lista_gastos, valor_kilometro)


    def eliminar_mantenimiento(self, id_mantenimiento):
        """
        Esta función elimina un mantenimiento
        """
        print('************** Método eliminar_mantenimiento **************')
        print('id_mantenimiento -->>>' + str(id_mantenimiento))
        self.logica.eliminar_mantenimiento(id_mantenimiento)
        self.vista_lista_mantenimientos.mostrar_mantenimientos(self.logica.dar_mantenimientos())

    def eliminar_accion(self, id_accion):
        """
        Esta función elimina una accion
        """
        print('************** Método eliminar_accion **************')
        print('self.__lista_acciones_auto -->>>')
        print(self.__lista_acciones_auto)
        print('Accion Actual id -->>>', id_accion)
        accion = self.__lista_acciones_auto[id_accion]
        print('Accion Actual -->>>', accion)      
        print('Auto Actual -->>>', self.auto_actual)        
        resultado = self.logica.eliminar_accion(self.logica.dar_auto(self.auto_actual)['id'], accion['Id'])
        marca_auto = self.logica.dar_auto(self.auto_actual)['placa']
        self.vista_lista_acciones.mostrar_acciones(marca_auto, self.logica.dar_acciones_auto(self.auto_actual))
        
    
    def mostrar_auto(self, id_auto=-1):
        """
        Esta función muestra un auto en la ventana de autos
        """
        print('************** Método mostrar_auto **************')
        print('Información de la lista __lista_autos -->>>')
        print(self.__lista_autos)
        self.auto_actual = id_auto
        print('ID Auto que llego -->>>',  self.auto_actual)
        if id_auto != -1:
            self.vista_auto = Vista_auto(self)
            self.vista_auto.mostrar_auto(self.logica.dar_auto(self.auto_actual))
        else:
            self.vista_auto = Vista_auto(self)
            self.vista_auto.mostrar_auto(None)

    def dar_auto(self, id_auto=-1):
        """
        Esta función retorna un auto
        """
        print('************** Método dar_auto **************')
        return self.logica.dar_auto(id_auto)