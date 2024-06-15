# Import de librerias
import unittest
from src.modelo.automovil import Automovil
from src.logica.Logica_mock import Logica_mock
import random
from faker import Faker
from faker.providers import DynamicProvider
from faker_vehicle import VehicleProvider


class AutomovilTestCase(unittest.TestCase):
    
    def setUp(self):
        """Método que permite preparar el ambiente necesario para realizar las pruebas"""
        self.logica = Logica_mock()
        # Generación de datos con libreria Faker
        self.data_factory = Faker()
        # Lista de tipos de mantenimiento
        tipos_mantenimientos_proveedor = DynamicProvider(
            provider_name="tipos_mantenimientos",
            elements=[
                "PAGO IMPUESTOS AUTOMOVIL",
                "LAVAR AUTOMOVIL",
                "TANQUEAR GASOLINA",
                "POLICHAR AUTOMOVIL",
                "REVISION TECNICO MECANICA",
                "COMPRAR SOA",
                "PINTAR AUTOMOVIL",
                "ECHAR AIRE A LAS LLANTAS",
                "CAMBIAR ACEITE",
            ],
        )
        # Agregamos proveedor de tipos de mantenimiento
        self.data_factory.add_provider(tipos_mantenimientos_proveedor)
        # Lista de tipos de combustible
        tipos_combustibles_proveedor = DynamicProvider(
            provider_name="tipos_combustibles",
            elements=["Gasolina Diesel", "Gasolina Corriente", "Electrico", "ACPM"],
        )
        # Agregamos proveedor de tipos de combustible
        self.data_factory.add_provider(tipos_combustibles_proveedor)
        # Agregar provedor de vehiculos
        self.data_factory.add_provider(VehicleProvider)

    def test_agregar_automovil_sin_valor(self):
        """Prueba para agregar un automovil sin el  valor en el campo de marca"""

        seCreoAutomovil = self.logica.crear_auto(
            "",
            self.data_factory.name().upper()[0:3] + str(random.randint(100, 999)),
            self.data_factory.vehicle_year(),
            self.data_factory.random_number(digits=4),
            self.data_factory.color_name(),
            self.data_factory.random_number(digits=4),
            self.data_factory.tipos_combustibles(),
        )
        self.assertFalse(seCreoAutomovil, "campos vacios")

    def test_agregar_automovil(self):
        """Prueba para agregar un automovil sin el  valor en el campo de marca"""
        seCreoAutomovil = self.logica.crear_auto(
            self.data_factory.vehicle_make_model(),
            self.data_factory.name().upper()[0:3] + str(random.randint(100, 999)),
            self.data_factory.vehicle_year(),
            self.data_factory.random_number(digits=4),
            self.data_factory.color_name(),
            self.data_factory.random_number(digits=4),
            self.data_factory.tipos_combustibles(),
        )
        self.assertTrue(seCreoAutomovil, "Se agrega Automovil")

    def test_agregar_automovil_placa_unica(self):
        """Prueba para agregar un automovil que no este registrado (la placa es el identificador y debe ser unica)"""
        self.logica.crear_auto(
            self.data_factory.vehicle_make_model(),
            "UCQ86C",
            self.data_factory.vehicle_year(),
            self.data_factory.random_number(digits=4),
            self.data_factory.color_name(),
            self.data_factory.random_number(digits=4),
            self.data_factory.tipos_combustibles(),
        )

        seCreoAutomovil = self.logica.crear_auto(
            self.data_factory.vehicle_make_model(),
            "UCQ86C",
            self.data_factory.vehicle_year(),
            self.data_factory.random_number(digits=4),
            self.data_factory.color_name(),
            self.data_factory.random_number(digits=4),
            self.data_factory.tipos_combustibles(),
        )

        self.assertFalse(seCreoAutomovil, "Automovil duplicado")

    def test_automovil_consultar_automoviles(self):
        """Prueba para  consultar Automoviles Registrados"""
        self.logica.eliminar_autos()
        self.logica.crear_auto(
            self.data_factory.vehicle_make_model(),
            self.data_factory.name().upper()[0:3] + str(random.randint(100, 999)),
            self.data_factory.vehicle_year(),
            self.data_factory.random_number(digits=4),
            self.data_factory.color_name(),
            self.data_factory.random_number(digits=4),
            self.data_factory.tipos_combustibles(),
        )
        self.logica.crear_auto(
            self.data_factory.vehicle_make_model(),
            self.data_factory.name().upper()[0:3] + str(random.randint(100, 999)),
            self.data_factory.vehicle_year(),
            self.data_factory.random_number(digits=4),
            self.data_factory.color_name(),
            self.data_factory.random_number(digits=4),
            self.data_factory.tipos_combustibles(),
        )
        self.logica.crear_auto(
            self.data_factory.vehicle_make_model(),
            "AAA86C",
            self.data_factory.vehicle_year(),
            self.data_factory.random_number(digits=4),
            self.data_factory.color_name(),
            self.data_factory.random_number(digits=4),
            self.data_factory.tipos_combustibles(),
        )

        automovil = Automovil(
            "Ferrari",
            "AAA86C",
            "2013",
            35000.0,
            "Plateado",
            "5000",
            "Gasolina",
            False,
            5000,
            1000,
        )
        automoviles = self.logica.dar_autos()
        self.assertEqual(automovil.placa, automoviles[0]['placa'], "Lista con resultados")

    def test_vender_automovil_parametros_vacios(self):
        """Prueba para validar que no se envien parametros vacios al momento de vender un Automovil"""    
        seVendioAutomovil = self.logica.vender_auto("", self.data_factory.random_number(digits=5), self.data_factory.random_number(digits=6))
        self.assertFalse(seVendioAutomovil,'Se valida que los parametros de entrada no esten vacios')

    def test_vender_automovil(self):
        """Prueba para vender un Automovil""" 
        placaAutomovil = self.data_factory.name().upper()[0:3] + str(random.randint(100, 999))
        self.logica.crear_auto(self.data_factory.vehicle_make_model(), placaAutomovil,
                               self.data_factory.vehicle_year(), self.data_factory.random_number(
                                   digits=4), self.data_factory.color_name(),
                               self.data_factory.random_number(digits=4), self.data_factory.tipos_combustibles())
        seVendioAutomovil = self.logica.vender_auto(placaAutomovil, self.data_factory.random_number(digits=5), self.data_factory.random_number(digits=6))     
        self.assertTrue(seVendioAutomovil,'Se raliza venta del Automovil')      

    def test_vender_automovil_tiene_acciones(self):
        """Prueba para validar que no se venda un Automovil que tenga acciones registradas""" 
        placaAutomovil = self.data_factory.name().upper()[0:3] + str(random.randint(100, 999))
        self.logica.crear_auto(self.data_factory.vehicle_make_model(), placaAutomovil,
                               self.data_factory.vehicle_year(), self.data_factory.random_number(
                                   digits=4), self.data_factory.color_name(),
                               self.data_factory.random_number(digits=4), self.data_factory.tipos_combustibles())
        for item in range(1, 3):
            nombreManimiento = self.data_factory.tipos_mantenimientos() + str(random.randint(1, 10000))
            self.logica.aniadir_mantenimiento(nombreManimiento, self.data_factory.sentence()) 
            for itemManto in range(1, 2):
                self.logica.crear_accion(nombreManimiento, placaAutomovil, float(random.uniform((10000), 300000)), float(random.uniform((10000), 300000)),
                                         self.data_factory.date_between(start_date='-2y'))
        seVendioAutomovil = self.logica.vender_auto(placaAutomovil, self.data_factory.random_number(digits=5), self.data_factory.random_number(digits=6))        
        self.assertFalse(seVendioAutomovil,'Se valida que no se realice la venta de un Automovil que tiene acciones registradas')       

    def validar_modelo(self,new_modelo, modelo_auto):
        resultado = False
        if new_modelo == modelo_auto:
            resultado= True

        return resultado


    def test_editar_automovil(self):
        """Prueba para editar un automovil editar el valor del  modelo"""
        modelo = int(self.data_factory.vehicle_year())
        placa = self.data_factory.name().upper()[0:3] + str(random.randint(100, 999))
        seCreoAutomovil = self.logica.crear_auto(
            self.data_factory.vehicle_make_model(),
            placa,
            modelo,
            self.data_factory.random_number(digits=4),
            self.data_factory.color_name(),
            self.data_factory.random_number(digits=4),
            self.data_factory.tipos_combustibles(),
        )
        automovil = self.logica.dar_auto(placa)
        nuevo_modelo = modelo + 1
        seEditoAutomovil = self.logica.editar_auto(automovil['id'],
            automovil['marca'],
            automovil['placa'],
            nuevo_modelo,
            automovil['kilometraje'],
            automovil['color'],
            automovil['cilindraje'],
            automovil['tipo_combustible'])

        automovil_editado= self.logica.dar_auto(placa)        
        self.assertTrue(self.validar_modelo(nuevo_modelo,int(automovil_editado['modelo'])), "Se agrega Automovil")

    def test_eliminar_automovil(self):
        """Prueba para eliminar un automovil"""
        resultado = False
        placa = self.data_factory.name().upper()[0:3] + str(random.randint(100, 999))
        seCreoAutomovil = self.logica.crear_auto(
            self.data_factory.vehicle_make_model(),
            placa,
            int(self.data_factory.vehicle_year()),
            self.data_factory.random_number(digits=4),
            self.data_factory.color_name(),
            self.data_factory.random_number(digits=4),
            self.data_factory.tipos_combustibles(),
        )
        automovil = self.logica.dar_auto(placa)

        se_elimino_automovil = self.logica.eliminar_auto(automovil['id'])
        self.assertTrue(se_elimino_automovil, "Se Elimina Automovil")

    def test_eliminar_Accion_auto(self):
        """Prueba para eliminar un mantenimiento"""
        resultado = False        
        placa = self.data_factory.name().upper()[0:3] + str(random.randint(100, 999))
        seCreoAutomovil = self.logica.crear_auto(
            self.data_factory.vehicle_make_model(),
            placa,
            int(self.data_factory.vehicle_year()),
            self.data_factory.random_number(digits=4),
            self.data_factory.color_name(),
            self.data_factory.random_number(digits=4),
            self.data_factory.tipos_combustibles(),
        )
        automovil = self.logica.dar_auto(placa)
        for item in range(1, 3):
            nombreManimiento = self.data_factory.tipos_mantenimientos() + str(random.randint(1, 10000))
            self.logica.aniadir_mantenimiento(nombreManimiento, self.data_factory.sentence()) 
            for itemManto in range(1, 2):
                self.logica.crear_accion(nombreManimiento, placa, float(random.uniform((10000), 300000)), float(random.uniform((10000), 300000)),
                                         self.data_factory.date_between(start_date='-2y'))

       
        se_elimino_accion = self.logica.eliminar_accion(automovil['id'], 1)
        self.assertTrue(se_elimino_accion, "Se Elimina Mantenimiento")  