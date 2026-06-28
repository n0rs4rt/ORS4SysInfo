import logging, sqlite3, logging
from datetime import datetime
from CORE.CONFIG_LOGS import config_logging
from CORE.BASE_DATOS import DB_Equipos
from CORE.RUTAS import *

from CORE.SYSTEMA import Sistema_OP
from CORE.PROCESADOR import Procesador
from CORE.LICENCIA import Licencia
from CORE.PLACA_MADRE import Placa_madre
from CORE.IDIOMA_REGION import Region
from CORE.USUARIOS import User
from CORE.DISCOS import Disco
from CORE.MEMORIA import Memoria
from CORE.GRAFICA import Grafica
from CORE.RED import Red


logger = logging.getLogger("logs")

class Escanear:
    def __init__(self):
        
        self.datos_sistema = None
        self.datos_procesador = None
        self.datos_licencia = None
        self.datos_placa_madre = None
        self.datos_region = None
        self.datos_usuarios = None
        self.datos_discos = None
        self.datos_memorias = None
        self.datos_GPUs = None
        self.datos_adaptadores = None
        
        self.notas = ""
        
        self.datos_tabla_equipos = None
        self.datos_tabla_usuarios = []
        self.datos_tabla_discos = []
        self.datos_tabla_memorias = []
        self.datos_tabla_gpus = []
        self.datos_tabla_adaptadores_red = []
        
    def obtener_datos (self):

        sistema = Sistema_OP()
        sistema.bios()
        sistema.sistema()
        sistema.dominio()
        self.datos_sistema = sistema.resultado()

        placa = Placa_madre()
        self.datos_placa_madre = placa.datos_motherboard()
        
        region = Region()
        region.region_idioma()
        self.datos_region = region.resultado()
        
        procesador = Procesador()
        self.procesador = procesador.datos_procesador()
        
        licencia = Licencia()
        self.datos_licencia = licencia.obtener()
        
        usuarios = User()
        self.datos_usuarios = usuarios.usuario()
        
        discos = Disco()
        self.datos_discos = discos.leer_disco()
        
        memoria = Memoria()
        self.datos_memorias = memoria.datos_memoria()
        
        graficas = Grafica()
        self.datos_GPUs = graficas.analizar_gpu()
        
        adaptadores_reds = Red()
        self.datos_adaptadores = adaptadores_reds.datos_adaptador()
        
        # print ("Datos obtenidos")
    def guardar_notas_equipo (self):
        """
        METODO  QUE GUARDA LAS NOTAS EN CASO QUE EL EQUIPO EXISTA Y SEA ACTUALIZADO
        """
        
        try:
            with sqlite3.connect (ruta_db) as conn:
                cursor = conn.cursor()
                cursor.execute ("SELECT notas_equipo FROM equipos WHERE hostname = ? AND modelo = ? AND fabricante =? AND serial_bios = ? AND serial_placa_madre = ?", (self.datos_sistema["host"], self.datos_sistema["modelo_PC"], self.datos_sistema["bios_fabricante"],  self.datos_sistema["bios_serial"], self.datos_placa_madre["serial"]))
                
                notas = cursor.fetchone()
                
                if notas:
                    self.notas = notas[0]
                
        except Exception as e:
            logger.error(f"Error al guardar las notas en la base de datos: {str(e)}")
    def preparar_datos_db (self):
        
        fecha = datetime.now().strftime("%Y-%m-%d")
        hora = datetime.now().strftime("%H:%M")
        self.datos_tabla_equipos = (self.datos_sistema["host"], self.datos_sistema["host"], self.datos_sistema["modelo_PC"], self.datos_sistema["bios_fabricante"],  self.datos_sistema["bios_serial"], self.datos_sistema["bios_version"], self.datos_placa_madre["fabricante"], self.datos_placa_madre["modelo"], self.datos_placa_madre["serial"], self.datos_placa_madre["version"], self.procesador["procesador"], self.datos_sistema["sistema"], self.datos_licencia["licencia"], self.datos_region["zona_horaria"], self.datos_region["idioma"], self.datos_sistema["dominio"],fecha, hora, self.notas)
        
        for user in self.datos_usuarios:
            self.datos_tabla_usuarios.append((user["nombre"], user["tipo"]))
        
        for disco in self.datos_discos:
            self.datos_tabla_discos.append((disco["modelo"], disco["almacenamiento"],disco["serial"], disco["tipo"], disco["estado"]))
        
        for memoria in self.datos_memorias:
            self.datos_tabla_memorias.append((memoria["fabricante"], memoria["capacidad"], memoria["serial"], memoria["partnumber"], memoria["tipo"]))
        
        for gpu in self.datos_GPUs:
            self.datos_tabla_gpus.append((gpu["nombre"], gpu["fabricante"], gpu["capacidad"]))
        
        for adaptador in self.datos_adaptadores:
            self.datos_tabla_adaptadores_red.append((adaptador["nombre"], adaptador["mac"], adaptador["velocidad"]))
        
    
    def insertar_datos_db (self):
        db = DB_Equipos()
        db.insertar_datos(self.datos_tabla_equipos, self.datos_tabla_usuarios, self.datos_tabla_discos, self.datos_tabla_memorias, self.datos_tabla_gpus, self.datos_tabla_adaptadores_red)
        