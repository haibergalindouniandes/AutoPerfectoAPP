# Importación de librerias
import datetime
from sqlalchemy import inspect

# Clase que contiene funcionalidades utilitarias
class Utilitario():

    def validar_numero_entero(self, numero):
        """Método que permite validar si un valor es entero"""
        try:
            int(numero)
            return True
        except ValueError:
            return False

    def validar_numero_flotante(self, numero):# pragma: no cover
        """Método que permite validar si un valor es flotante"""
        try:
            float(numero)
            return True
        except ValueError:
            return False

    def validar_cadena_vacia(self, cadena):
        """Método que permite validar si una cadena esta vacia"""
        if len(str(cadena)) > 0:
            return True
        else:
            return False

    def validar_cadena_fecha(self, cadena):# pragma: no cover
        """Método que permite validar si una cadena es fecha (YYYY-MM-DD)"""
        esFecha = True
        try:
            datetime.datetime.strptime(cadena, '%Y-%m-%d')
        except ValueError:
            esFecha = False
        return esFecha        
    
    def formatear_fecha(self, fecha):
        """Método que permite formatear string a Date"""
        y, m, d = str(fecha).split('-')
        return datetime.date(int(y), int(m), int(d))

    def resulset_a_diccionario(self, resultset):
        """Método que permite convertir un resultset a diccionario, y convierte el key en Title"""
        return dict((k.title(), v) for k, v in resultset.items())         

    def objeto_a_diccionario(self, objeto):
        """Método que permite convertir un objeto a diccionario y elimina '_'"""
        return {
            c.key.title().replace("_", ""): getattr(objeto, c.key)
            for c in inspect(objeto).mapper.column_attrs
        }       