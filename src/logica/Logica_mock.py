'''
Esta clase es tan sólo un mock con datos para probar la interfaz
'''
from asyncio.windows_events import NULL
import traceback
from src.modelo.constantes import Constantes
from src.modelo.utilitario import Utilitario
from src.modelo.automovil import Automovil
from src.modelo.mantenimiento import Mantenimiento
from src.modelo.accion import Accion
from src.modelo.declarative_base import engine, Base, session
from sqlalchemy import func


class Logica_mock():

    def __init__(self):
        #Instanciamos la clase utilitario
        self.utilitario = Utilitario()
        #Instanciamos la clase constantes
        self.constante = Constantes()
        #Crea todas las tablas de la BD
        Base.metadata.create_all(engine)
        #Este constructor contiene los datos falsos para probar la interfaz
        self.autos = [{'Marca':'Volkswagen', 'Placa':'KBL000', 'Modelo': '2010', 'Kilometraje': 150000.0, \
                        'Color':'Rojo', 'Cilindraje': '2000', 'TipoCombustible':'Gasolina', 'Vendido': False, \
                        'ValorVenta': 0, 'KilometrajeVenta':0 },
                    {'Marca':'Renault', 'Placa':'BSQ782', 'Modelo': '2015', 'Kilometraje': 182000.0, \
                        'Color':'Plateado', 'Cilindraje': '1600', 'TipoCombustible':'Gasolina', 'Vendido': True, \
                        'ValorVenta': 18000000, 'KilometrajeVenta':195000 }]
        self.gastos = [{'Marca':'Volkswagen', 'Gastos':[('2019',1200000),('2020',1300000), ('2021',2000000), ('2022',2500000), \
                        ('Total',7000000)], 'ValorKilometro': 175},\
                       {'Marca':'Renault', 'Gastos':[('2020',900000), ('2021',1100000), ('2022',1300000), \
                        ('Total',3300000)], 'ValorKilometro': 128},]


    def validar_entrada(self, marca, placa, modelo, kilometraje, color, cilindraje, tipo_combustible):# pragma: no cover
        
        error = 0

        if marca == ""  or marca == NULL or (len(str(marca)) < 3  or len(str(marca)) > 100 ):
            error += 1

        if placa == ""  or placa == NULL or (len(str(placa)) < 3 or len(str(placa)) > 6 ):
            error += 1

        if modelo == ""  or modelo == NULL or (len(str(modelo)) < 3 or len(str(modelo)) > 4 ):
            error += 1

        if kilometraje == ""  or kilometraje == NULL or (len(str(kilometraje)) < 1 or len(str(kilometraje)) > 6):
            error += 1

        if color == ""  or color == NULL or (len(str(color)) < 3 or len(str(color)) > 100):
            error += 1

        if cilindraje == ""  or cilindraje == NULL or (len(str(cilindraje)) < 3  or len(str(cilindraje)) > 6):
            error += 1

        if tipo_combustible == ""  or tipo_combustible == NULL or (len(str(tipo_combustible)) < 3 or  len(str(tipo_combustible)) > 100) :
            error += 1

        print('Error validaciones --> ' , error)
        return error

    def dar_autos(self):    
        lista_autos = []            
        automoviles = session.query(Automovil).order_by(Automovil.placa.asc()).all()
        
        for auto in automoviles:           
            
            diccionario_autos = dict(auto)
            print('*** auto ***')
            print(diccionario_autos)
            lista_autos.append(diccionario_autos)
        
        session.close()

        return lista_autos     

    def eliminar_autos(self):
        session.execute('''DELETE FROM Automovil''')
        session.commit()
        session.close()

    
    def dar_auto(self, id_auto):
        print(id_auto)
        if self.utilitario.validar_numero_entero(id_auto):
            automovil = session.query(Automovil).filter(Automovil.id == id_auto).scalar()     
        else:
            automovil = session.query(Automovil).filter(Automovil.placa == id_auto).scalar()     
        
        diccionarioAuto = dict(automovil)
        print('***Diccionario Auto ***')
        print(diccionarioAuto)        
        session.close()        
        return diccionarioAuto.copy()
    
    def crear_auto(self, marca, placa, modelo, kilometraje, color, cilindraje, tipo_combustible):
        print('************** Método crear_auto **************')
        print('marca = ' + str(marca) + ', placa = ' + str(placa) + ', modelo = ' + str(modelo) + ', kilometraje = ' + str(kilometraje) + ', color = ' + str(color) + ', cilindraje = ' + str(cilindraje) + ', tipo_combustible = ' + str(tipo_combustible))
        error = self.validar_entrada(marca, placa.upper(), modelo, kilometraje, color, cilindraje, tipo_combustible)
        if error > 0:
            return False
        try:
            busquedaAutomovil = session.query(func.count(Automovil.id)).filter(
                Automovil.placa == placa).scalar()
            if busquedaAutomovil == 0:
                automovil = Automovil(
                        marca=marca, placa=placa, modelo=modelo, kilometraje=kilometraje, color=color, cilindraje=cilindraje,
                        tipo_combustible=tipo_combustible, vendido=False, valor_venta=0,  kilometraje_venta=0)
                session.add(automovil)
                session.commit()
                return True
            else:
                return False
        except:
            traceback.print_exc()
        

    def editar_auto(self, id, marca, placa, modelo, kilometraje, color, cilindraje, tipo_combustible):
        resultado = False
        print('Editar auto Logica id --> ', id)
        try:
            if self.validar_entrada( marca, placa, modelo, kilometraje, color, cilindraje, tipo_combustible) == 0:
                busquedaAutomovil = self.dar_auto(id)
                print('Editar auto Logica placa --> ', busquedaAutomovil['placa'])                
                if busquedaAutomovil != None:
                    print('***actualziar auto ***')
                    autoActualizar = session.query(Automovil).filter(Automovil.id == busquedaAutomovil['id']).one()     
                    autoActualizar.marca = marca
                    autoActualizar.placa = placa
                    autoActualizar.modelo = modelo
                    autoActualizar.kilometraje = kilometraje
                    autoActualizar.cilindraje = cilindraje
                    autoActualizar.tipo_combustible = tipo_combustible
                    autoActualizar.color = color
                    session.commit()
                    resultado = True
        finally:
            session.close()
            return resultado 

    def vender_auto(self, id, kilometraje_venta, valor_venta):# pragma: no cover
        seVendioAutomovil = False
        automovilVendido = None
        try:
            if self.validar_vender_auto(id, kilometraje_venta, valor_venta):
                if len(self.dar_acciones_auto(id)) == 0:
                    if self.utilitario.validar_numero_entero(id):
                        automovilVendido = session.query(Automovil).filter(Automovil.id == id).one()
                    else:
                        automovilVendido = session.query(Automovil).filter(Automovil.placa == id).one()
                    automovilVendido.vendido = True
                    automovilVendido.kilometraje_venta = kilometraje_venta
                    automovilVendido.valor_venta = valor_venta
                    session.commit()
                    seVendioAutomovil = True
        finally:
            session.close()
            return seVendioAutomovil

    def eliminar_auto(self, id):
        resultado = False
        print('eliminar auto Logica id --> ', id)
        try:
            busquedaAutomovil = self.dar_auto(id)
            print('eliminar auto Logica placa --> ', busquedaAutomovil['placa'])                
            if busquedaAutomovil != None:
                print('***Eliminar auto ***')
                autoEliminar = session.query(Automovil).filter(Automovil.id == busquedaAutomovil['id']).one()     
                session.delete(autoEliminar)
                print('***se elimino auto ***')
                session.commit()
                resultado = True
        finally:
            session.close()
            return resultado 

        
    def validar_crear_editar_auto(self, marca, placa, modelo, kilometraje, color, cilindraje, tipo_combustible):# pragma: no cover
        validacion = False
        try:
            if (self.utilitario.validar_cadena_vacia(marca) and self.utilitario.validar_cadena_vacia(placa)
                and self.utilitario.validar_cadena_vacia(modelo) and self.utilitario.validar_numero_flotante(kilometraje)
                and self.utilitario.validar_cadena_vacia(color) and self.utilitario.validar_cadena_vacia(cilindraje)
                and self.utilitario.validar_cadena_vacia(tipo_combustible)):
                validacion = True
        finally:
            return validacion
        
    def validar_vender_auto(self, id, kilometraje_venta, valor_venta):
        validacion = False
        if (self.utilitario.validar_cadena_vacia(id) and self.utilitario.validar_numero_flotante(kilometraje_venta) 
            and self.utilitario.validar_numero_flotante(valor_venta)):
          validacion = True
        return validacion
    
    # Funcionalidades de mantenimiento
    def dar_mantenimientos(self):
        lista_mantenimientos = []
        mantenimientos = session.query(Mantenimiento).order_by(Mantenimiento.nombre.asc()).all()
        for mantenimiento in mantenimientos:
            lista_mantenimientos.append(self.utilitario.objeto_a_diccionario(mantenimiento))
        session.close()
        return lista_mantenimientos

    def dar_mantenimiento(self, mantenimiento_id):
        mantenimiento = None
        try:
            if self.utilitario.validar_numero_entero(mantenimiento_id):
                mantenimientoBuscado = session.query(Mantenimiento).filter(Mantenimiento.id == mantenimiento_id).one()
            else:
                mantenimientoBuscado = session.query(Mantenimiento).filter(Mantenimiento.nombre == mantenimiento_id).one()
            mantenimiento = self.utilitario.objeto_a_diccionario(mantenimientoBuscado)
        finally:
            session.close()
            return mantenimiento

    def aniadir_mantenimiento(self, nombre, descripcion):
        resultado = False
        if self.validar_crear_editar_mantenimiento(nombre, descripcion):
            busquedaMantenimiento = session.query(func.count(Mantenimiento.id)).filter(
                Mantenimiento.nombre == nombre).scalar()
            if busquedaMantenimiento == 0:
                mantenimiento = Mantenimiento(
                    nombre=nombre, descripcion=descripcion)
                session.add(mantenimiento)
                session.commit()
                session.close()
                resultado = True
        return resultado	
    
    def editar_mantenimiento(self, nombre, descripcion):
        resultado = False
        try:
            if self.validar_crear_editar_mantenimiento(nombre, descripcion):
                mantenimientoBuscado = self.dar_mantenimiento(nombre)
                if mantenimientoBuscado != None:
                    mantenimientoActualizar = session.query(Mantenimiento).filter(Mantenimiento.id == mantenimientoBuscado['Id']).one()     
                    mantenimientoActualizar.nombre = nombre
                    mantenimientoActualizar.descripcion = descripcion
                    session.commit()
                    resultado = True
        finally:
            session.close()
            return resultado 
    
    def eliminar_mantenimiento(self, id):
        resultado = False
        try:
            mantenimiento_buscado = self.dar_mantenimiento(id)
            if mantenimiento_buscado != None:
                mantenimiento_eliminar = session.query(Mantenimiento).filter(Mantenimiento.id == mantenimiento_buscado['Id']).one()     
                session.delete(mantenimiento_eliminar)
                print('***Se Elino Mantenimiento***')
                session.commit()
                resultado = True
        finally:
            session.close()
            return resultado       

        
    def eliminar_mantenimientos(self):
        session.execute(self.constante.ELIMINAR_MANTENIMIENTOS)
        session.commit()
        session.close()        

    def validar_crear_editar_mantenimiento(self, nombre, descripcion):
        validacion = False
        if len(str(nombre)) > 5 and len(str(descripcion)) > 5 and nombre.isupper():
            validacion = True
        return validacion
        
    def dar_acciones_auto(self, id_auto):        
        lista_acciones = []
        automovil = self.dar_auto(id_auto)
        sql =  self.constante.CONSULTA_ACCIONES_POR_AUTOMOVIL.format(auto_id=str(automovil['id']))
        resultado = engine.execute(sql)
        for regitro in resultado:
            diccionarioRecord = dict(regitro)
            diccionarioAccion = self.utilitario.resulset_a_diccionario(diccionarioRecord)
            lista_acciones.append(diccionarioAccion)
        session.close()
        return lista_acciones

    def dar_accion(self, id_auto, id_accion):
        accioneBuscada = []
        try:
            accioneBuscada = self.dar_acciones_auto(id_auto)[id_accion].copy()
        except:
            traceback.print_exc()
        finally:
            return accioneBuscada

    def crear_accion(self, id_mantenimiento, id_auto, valor, kilometraje, fecha):
        registroExitoso = False
        try:
            if self.utilitario.validar_numero_entero(id_mantenimiento):
                mantenimiento_id = id_mantenimiento
            else:
                mantenimiento = self.dar_mantenimiento(id_mantenimiento)
                mantenimiento_id = mantenimiento['Id']
            if self.utilitario.validar_numero_entero(id_auto):
                auto_id = id_auto
            else:
                automovil = self.dar_auto(id_auto)
                auto_id = str(automovil['id'])
            accion = Accion(round(float(kilometraje), 2), round(float(valor), 2), self.utilitario.formatear_fecha(fecha), mantenimiento_id, auto_id)
            session.add(accion)
            session.commit()
            registroExitoso = True
        finally:
            session.close()
            return registroExitoso
            
    def editar_accion(self, id_accion, mantenimiento, id_auto, valor, kilometraje, fecha):
        resultado = False
        try:
            accionBuscada = self.dar_accion(id_auto, id_accion)
            if not(isinstance(accionBuscada, str)):
                mantenimiento = self.dar_mantenimiento(mantenimiento)
                accionActualizar = session.query(Accion).filter(Accion.id == accionBuscada['Id']).one()     
                accionActualizar.valor = round(float(valor), 2)
                accionActualizar.kilometraje = round(float(kilometraje), 2)
                accionActualizar.fecha = self.utilitario.formatear_fecha(fecha)
                accionActualizar.mantenimiento_id = mantenimiento['Id']
                session.commit()
                resultado = True
        finally:
            session.close()
            return resultado 

    def eliminar_accion(self, id_auto, id_accion):
        print('***Inicio Eliminar Accion***')
        print('idauto -->',id_auto)
        print('id_accion -->',id_accion)
        resultado = False
        try:            
            accion_eliminar = session.query(Accion).filter(Accion.id == id_accion).one()     
            session.delete(accion_eliminar)
            print('***Se Elino Accion***')
            session.commit()
            resultado = True
        finally:
            session.close()
            return resultado       
                        
    def eliminar_acciones(self):# pragma: no cover
        session.execute(self.constante.ELIMINAR_ACCIONES)
        session.commit()
        session.close()               
        
    def validar_crear_editar_accion(self, mantenimiento_id, auto_id, valor, kilometraje, fecha):# pragma: no cover
        validacionExitosa = False
        if (self.utilitario.validar_cadena_vacia(mantenimiento_id) and self.utilitario.validar_cadena_vacia(auto_id)
            and self.utilitario.validar_numero_flotante(valor) and self.utilitario.validar_numero_flotante(kilometraje)
            and self.utilitario.validar_cadena_fecha(fecha)):
            validacionExitosa = True
        return validacionExitosa

    def dar_reporte_ganancias(self, id_auto):
        automovil = self.dar_auto(id_auto)
        lista_gastos = []
        id_mantenimiento = 0
        num_mantenimiento = 0
        total_gasto_mantenimiento = 0
        km_inicial = 0
        km_final = 0
        promedio_total = 0
        acciones_totales = 0

        sql =  self.constante.CONSULTA_ACCIONES_POR_AUTOMOVIL_ANIO.format(id_auto=str(automovil['id']))
        resultado = engine.execute(sql)
        for regitro in resultado:
            diccionario_record = dict(regitro)
            
            lista_gastos.append((diccionario_record['FECHA'],diccionario_record['GASTOS'] ))


        sql =  self.constante.CONSULTA_AGRUPADA_GASTOS_AUTOMOVIL_ANIO.format(id_auto=str(automovil['id']))
        resultado = engine.execute(sql)
        for registro in resultado:
            id_mantenimiento = int(registro['ID_MANTENIMIENTO'])
            num_mantenimiento = int(registro['NUM_MANTENIMIENTO'])
            total_gasto_mantenimiento = int(registro['GASTOS'])

            sql1 =  self.constante.CONSULTA_AGRUPADA_KM_AUTOMOVIL_ANIO.format(id_auto=str(automovil['id']),id_accion=str(id_mantenimiento))
            resultado2 = engine.execute(sql1)
            for registro2 in resultado2:
                km_inicial = int(registro2['KM_INICIAL'])
                km_final = int(registro2['KM_FINAL'])
            
            
            if km_final == km_inicial :
                km_recorrido = 1 # pragma: no cover
            else:
                if km_final > km_inicial:
                    km_recorrido =  km_final - km_inicial # pragma: no cover
                else: 
                    km_recorrido = 1

            promedio_accion =  total_gasto_mantenimiento / km_recorrido
            promedio_total += int(promedio_accion)
            acciones_totales += 1

        if acciones_totales == 0 :
            promedio_final_auto =  promedio_total / 1 # pragma: no cover
        else:
            promedio_final_auto =  promedio_total / acciones_totales


        session.close()
        print('***valores****')
        print(str(promedio_final_auto))
        print(lista_gastos)

        return lista_gastos, str(promedio_final_auto)
