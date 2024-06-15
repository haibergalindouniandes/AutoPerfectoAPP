# Import de librerias
import unittest
import random
from faker import Faker
from faker.providers import DynamicProvider
from src.logica.Logica_mock import Logica_mock

# Clase que contiene la logica necesaria para realizar las pruebas de Mantenimiento
class MantenimientoTestCase(unittest.TestCase):
    def setUp(self):
        """Método que permite preparar el ambiente necesario para realizar las pruebas"""
        # Se genera instancia de Logica_Mock
        self.logica = Logica_mock()
        # Generación de datos con libreria Faker
        self.data_factory = Faker()
        # Lista de tipos de mantenimiento
        tipos_mantenimientos_proveedor = DynamicProvider(provider_name="tipos_mantenimientos", 
                                                       elements=["PAGO IMPUESTOS AUTOMOVIL", "LAVAR AUTOMOVIL", "TANQUEAR GASOLINA", 
                                                                 "POLICHAR AUTOMOVIL", "REVISION TECNICO MECANICA", "COMPRAR SOA",
                                                                 "PINTAR AUTOMOVIL", "ECHAR AIRE A LAS LLANTAS", "CAMBIAR ACEITE"])
        # Agregamos proveedor de tipos de mantenimiento
        self.data_factory.add_provider(tipos_mantenimientos_proveedor)
        # Lista de tipos de combustible
        tipos_combustibles_proveedor = DynamicProvider(provider_name="tipos_combustibles", 
                                                       elements=["Gasolina Diesel", "Gasolina Corriente", "Electrico", "ACPM"])
        # Agregamos proveedor de tipos de combustible
        self.data_factory.add_provider(tipos_combustibles_proveedor)
    
    def test_agregar_mantenimiento(self):
        """Prueba para agregar un mantenimiento"""    
        seCreoMantenimiento = self.logica.aniadir_mantenimiento(self.data_factory.tipos_mantenimientos() + str(random.randint(1, 10000)), self.data_factory.sentence())
        self.assertTrue(seCreoMantenimiento)

    def test_agregar_mantenimiento_unico(self):
        """Prueba para agregar un mantenimiento que no este registrado (el nombre es el identificador y debe ser unico)"""        
        nombreMantenimiento = self.data_factory.tipos_mantenimientos() + str(random.randint(1, 10000))
        self.logica.aniadir_mantenimiento(nombreMantenimiento, self.data_factory.sentence())
        seCreoMantenimiento = self.logica.aniadir_mantenimiento(nombreMantenimiento, self.data_factory.sentence())
        self.assertFalse(seCreoMantenimiento)
    
    def test_agregar_mantenimiento_parametros_vacios(self):
        """Prueba para validar que los parametros nombre y descripcion no se envien vacios"""
        seCreoMantenimiento = self.logica.aniadir_mantenimiento("", self.data_factory.sentence())
        self.assertFalse(seCreoMantenimiento)

    def test_agregar_mantenimiento_nombre_mayuscula(self):
        """Prueba para validar que el parametro nombre se envie en mayuscula"""
        seCreoMantenimiento = self.logica.aniadir_mantenimiento(self.data_factory.tipos_mantenimientos().lower(), self.data_factory.sentence())
        self.assertFalse(seCreoMantenimiento)	

    def test_consultar_lista_vacia_mantenimientos(self):
        """Prueba que retorna una lista vacia de mantenimientos"""
        self.logica.eliminar_mantenimientos()
        self.assertEqual(self.logica.dar_mantenimientos(), [], 'Consultar lista vacia de mantenimientos')        

    def test_consultar_mantenimientos(self):
        """Prueba consultar los mantenimientos que se encuentran registrados"""
        for item in range(1, 5):
            self.logica.aniadir_mantenimiento(self.data_factory.tipos_mantenimientos() + str(random.randint(1, 10000)), self.data_factory.sentence())
        self.assertGreater(self.logica.dar_mantenimientos(), [], 'Consultar los mantenimientos registrados')        

    def test_editar_mantenimiento_parametros_vacios(self):
        """Prueba para validar que no se actualice un mantenimiento por parametros vacios"""
        seEditoMantenimiento = self.logica.editar_mantenimiento(self.data_factory.tipos_mantenimientos() + str(random.randint(1, 10000)), "")
        self.assertFalse(seEditoMantenimiento, 'No se actualiza el mantenimiento por parametros vacios')

    def test_editar_mantenimiento(self):
        """Prueba para validar que se actualice un mantenimiento"""
        nombreManimiento = self.data_factory.tipos_mantenimientos() + str(random.randint(1, 10000))
        self.logica.aniadir_mantenimiento(nombreManimiento, self.data_factory.sentence()) 
        seEditoMantenimiento = self.logica.editar_mantenimiento(nombreManimiento, self.data_factory.sentence())
        self.assertTrue(seEditoMantenimiento, 'Se actualiza mantenimiento')		                


    def test_eliminar_mantenimiento(self):
        """Prueba para eliminar un mantenimiento"""
        resultado = False
        nombreMantenimiento = self.data_factory.tipos_mantenimientos() + str(random.randint(1, 10000))
        self.logica.aniadir_mantenimiento(nombreMantenimiento, self.data_factory.sentence())
        seCreoMantenimiento = self.logica.aniadir_mantenimiento(nombreMantenimiento, self.data_factory.sentence())

        se_elimino_mantenimiento = self.logica.eliminar_mantenimiento(nombreMantenimiento)
        self.assertTrue(se_elimino_mantenimiento, "Se Elimina Mantenimiento")