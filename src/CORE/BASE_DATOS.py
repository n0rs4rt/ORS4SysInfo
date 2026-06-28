import sqlite3, logging, json , shutil

from CORE.RUTAS import *

logger = logging.getLogger("logs")

class DB_Equipos:
    def __init__(self):
        pass
    
    def crear_db(self):
        """
        Crea la base de datos
        """
        try:
            with sqlite3.connect(ruta_db) as conn:
                cursor = conn.cursor()
                cursor.execute("PRAGMA foreign_keys = ON")
                cursor.execute ("""
                                CREATE TABLE IF NOT EXISTS equipos (
                                    id_equipo INTEGER PRIMARY KEY AUTOINCREMENT,
                                    custom_name TEXT,
                                    hostname TEXT,
                                    modelo TEXT,
                                    fabricante TEXT,
                                    serial_bios TEXT,
                                    bios_version TEXT,
                                    placa_madre TEXT,
                                    modelo_placa_madre TEXT,
                                    serial_placa_madre TEXT,
                                    version_placa_madre TEXT,
                                    procesador TEXT,
                                    sistema_operativo TEXT,
                                    licencia TEXT,
                                    zona_horaria TEXT,
                                    idioma TEXT,
                                    dominio_grupo_trabajo TEXT,
                                    fecha_registro TEXT,
                                    hora_registro TEXT,
                                    notas_equipo TEXT,
                                    UNIQUE (hostname, modelo, fabricante, serial_bios, serial_placa_madre)
                                )
                                """)
                cursor.execute ("""
                                CREATE TABLE IF NOT EXISTS usuarios (
                                    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
                                    id_equipo INTEGER,
                                    nombre TEXT,
                                    tipo TEXT,
                                    FOREIGN KEY (id_equipo) REFERENCES equipos (id_equipo) ON DELETE CASCADE
                                )
                                """)

                cursor.execute (""" 
                                CREATE TABLE IF NOT EXISTS disco (
                                    id_disco INTEGER PRIMARY KEY AUTOINCREMENT,
                                    id_equipo INTEGER,
                                    modelo TEXT,
                                    capacidad TEXT,
                                    serial TEXT,
                                    interfaz TEXT,
                                    fallos_criticos INTEGER,
                                    FOREIGN KEY (id_equipo) REFERENCES equipos (id_equipo) ON DELETE CASCADE
                                )
                                """)
                
                cursor.execute ("""
                                CREATE TABLE IF NOT EXISTS memorias (
                                    id_memoria INTEGER PRIMARY KEY AUTOINCREMENT,
                                    id_equipo INTEGER,
                                    fabricante TEXT,
                                    capacidad TEXT,
                                    serial TEXT,
                                    partnumber TEXT,
                                    tipo TEXT,
                                    FOREIGN KEY (id_equipo) REFERENCES equipos (id_equipo) ON DELETE CASCADE
                                    
                                )
                                """)
                
                cursor.execute ("""
                                CREATE TABLE IF NOT EXISTS gpu (
                                    id_gpu INTEGER PRIMARY KEY AUTOINCREMENT,
                                    id_equipo INTEGER,
                                    modelo TEXT,
                                    fabricante TEXT,
                                    capacidad TEXT,
                                    FOREIGN KEY (id_equipo) REFERENCES equipos (id_equipo) ON DELETE CASCADE
                                )
                                """)
                cursor.execute ("""
                                CREATE TABLE IF NOT EXISTS adaptadores_red (
                                    id_adaptador INTEGER PRIMARY KEY AUTOINCREMENT,
                                    id_equipo INTEGER,
                                    nombre TEXT,
                                    mac TEXT,
                                    velocidad TEXT,
                                    FOREIGN KEY (id_equipo) REFERENCES equipos (id_equipo) ON DELETE CASCADE
                                )
                                
                                """)
            return True
        
        except Exception as e:
            logger.error(f"Error al crear la base de datos: {str(e)}")
            return False
    
    def registros_db_existe (self):
        """
        Comprueba si la base de datos existe y tiene registros
        """
        
        if not ruta_db.exists():
            return False
        try:
            with sqlite3.connect(ruta_db) as conn:
                cursor = conn.cursor()
                cursor.execute ("SELECT * FROM equipos")
                datos =cursor.fetchall()
                if not datos:
                    return False
                return True
        except Exception as e:
            logger.error(f"Error al comprobar la base de datos: {str(e)}")
            return False
    
    def insertar_datos(self,datos_tabla_equipos,datos_tabla_usuarios,datos_tabla_discos,datos_tabla_memorias,datos_tabla_gpus,datos_tabla_adaptadores_red):
        """
        Inserta los datos en la base de datos
        """
        try:
            with sqlite3.connect (ruta_db) as conn:
                cursor = conn.cursor()
                cursor.execute("PRAGMA foreign_keys = ON")
                cursor.execute ("INSERT OR REPLACE INTO equipos (custom_name, hostname, modelo, fabricante, serial_bios, bios_version, placa_madre, modelo_placa_madre, serial_placa_madre, version_placa_madre, procesador, sistema_operativo, licencia, zona_horaria, idioma, dominio_grupo_trabajo, fecha_registro,hora_registro, notas_equipo) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", datos_tabla_equipos)
                
                id_equipo = cursor.lastrowid

                tabla_usuario = []
                
                for user in datos_tabla_usuarios:
                        tabla_usuario.append((id_equipo,) + user)
                
                cursor.executemany ("INSERT OR REPLACE INTO usuarios (id_equipo, nombre, tipo) VALUES (?,?,?)", tabla_usuario)
                
                tabla_discos =  []
                
                for disco in datos_tabla_discos:
                    tabla_discos.append((id_equipo,) + disco)
    
                cursor.executemany ("INSERT OR REPLACE INTO disco (id_equipo,modelo, capacidad, serial, interfaz, fallos_criticos) VALUES (?,?,?,?,?,?)", tabla_discos)


                tabla_memorias = []
                
                for memoria in datos_tabla_memorias:
                    tabla_memorias.append((id_equipo,) + memoria)
                
                cursor.executemany ("INSERT OR REPLACE INTO memorias (id_equipo,fabricante, capacidad, serial, partnumber, tipo) VALUES (?,?,?,?,?,?)", tabla_memorias)

                tabla_gpus = []

                for gpu in datos_tabla_gpus:
                    tabla_gpus.append((id_equipo,) + gpu)
                
                cursor.executemany ("INSERT OR REPLACE INTO gpu (id_equipo,modelo, fabricante, capacidad) VALUES (?,?,?,?)", tabla_gpus)

                tabla_adaptadores_red = []

                for adaptador in datos_tabla_adaptadores_red:
                    tabla_adaptadores_red.append((id_equipo,) + adaptador)
                
                cursor.executemany ("INSERT OR REPLACE INTO adaptadores_red (id_equipo,nombre, mac, velocidad) VALUES (?,?,?,?)", tabla_adaptadores_red)

            return True

        except Exception as e:
            logger.error(f"Error al insertar los datos en la base de datos: {str(e)}")
            
    def cantidad_equipos (self):
        """
        DEVUELVE LA CANTIDAD DE EQUIPOS EN LA DB
        """
        
        cantidad = 0
        try:
            with sqlite3.connect (ruta_db) as conn:
                cursor = conn.cursor()
                cursor.execute ("SELECT COUNT(*) FROM equipos")
                cantidad = cursor.fetchone()
                cantidad = cantidad[0]
            return cantidad
        except Exception as e:
            logger.error(f"Error al obtener la cantidad de equipos: {str(e)}")
            return cantidad
        
    def consultar_equipos(self):

        id_equipos = []
        lista_equipos = []

        #obtenemos los id de usuarios
        try:
            with sqlite3.connect (ruta_db) as conn:
                cursor = conn.cursor()
                cursor.execute ("SELECT id_equipo FROM equipos")
                ids = cursor.fetchall()
                
                for i in ids:
                    id_equipos.append(i[0])
                
        except Exception as e:
            logger.error(f"Error al consultar los equipos: {str(e)}")

        # print(id_equipos)
        for i in id_equipos:
            
            equipo = {"id": None,"info_general": None,"memorias": [], "discos": [], "gpus": [], "redes": [], "usuarios": []}
            
            try: 
                #extraemos la informacion general
                with sqlite3.connect (ruta_db) as conn:
                    cursor = conn.cursor()
                    cursor.execute ("SELECT equipos.custom_name, equipos.hostname,equipos.modelo, equipos.fabricante, equipos.serial_bios, equipos.bios_version, equipos.serial_placa_madre, equipos.modelo_placa_madre, equipos.version_placa_madre, equipos.sistema_operativo, equipos.zona_horaria, equipos.idioma, equipos.dominio_grupo_trabajo, equipos.fecha_registro, equipos.notas_equipo FROM equipos WHERE id_equipo = ?", (i,))

                    datos_info_general = cursor.fetchone()
                    # print(datos_info_general)
                    equipo["id"] = i
                    
                    info_general = {"custom_name":datos_info_general[0], "hostname":datos_info_general[1],"modelo": datos_info_general[2],"fabricante_bios": datos_info_general[3],"serial_bios": datos_info_general[4], "bios_version": datos_info_general[5], "placa_madre":datos_info_general[6],"modelo_placa_madre":datos_info_general[7], "version_placa_madre":datos_info_general[8], "sistema_operativo":datos_info_general[9], "zona_horaria":datos_info_general[10], "idioma":datos_info_general[11], "dominio_grupo_trabajo":datos_info_general[12], "fecha_registro":datos_info_general[13], "notas_equipo":datos_info_general[14]}
                    
                    equipo["info_general"]= info_general
                                
            
                #extraemos la informacion de la memoria
                with sqlite3.connect (ruta_db) as conn:
                    cursor= conn.cursor()
                    cursor.execute ("SELECT fabricante, capacidad, serial, partnumber, tipo FROM memorias WHERE id_equipo = ?", (i,))
                    datos_memorias = cursor.fetchall()

                    for dato in datos_memorias:
                        
                        memoria = {"fabricante":"desconocido", "capacidad":"desconocido", "serial":"desconocido", "partnumber":"desconocido", "tipo":"desconocido"}
                        
                        memoria["fabricante"] = dato[0]
                        memoria["capacidad"] = dato[1]
                        memoria["serial"] = dato[2]
                        memoria["partnumber"] = dato[3]
                        memoria["tipo"] = dato[4]
                        
                        equipo["memorias"].append(memoria)

                with sqlite3.connect (ruta_db) as conn:
                    cursor= conn.cursor()
                    cursor.execute ("SELECT modelo, capacidad, serial, interfaz, fallos_criticos FROM disco WHERE id_equipo = ?", (i,))
                    datos_discos = cursor.fetchall()

                    for dato in datos_discos:
                        
                        disco = {"modelo":"desconocido", "capacidad":"desconocido", "serial":"desconocido", "interfaz":"desconocido", "fallos_criticos":"No detectados"}
                        
                        disco["modelo"] = dato[0]
                        disco["capacidad"] = dato[1]
                        disco["serial"] = dato[2]
                        disco["interfaz"] = dato[3]
                        
                        if disco["fallos_criticos"] == 0:
                            disco["fallos_criticos"] = "Ser recomineda remplazar disco"
                        
                        equipo["discos"].append(disco)
                        
                with sqlite3.connect (ruta_db) as conn:
                    cursor = conn.cursor()
                    cursor.execute ("SELECT modelo, fabricante, capacidad FROM gpu WHERE id_equipo = ?", (i,))
                    datos_gpus = cursor.fetchall()
                    
                    for dato in datos_gpus:
                        gpu = {"modelo":"desconocido", "fabricante":"desconocido", "capacidad":"desconocido"}
                        
                        gpu["modelo"] = dato[0]
                        gpu["fabricante"] = dato[1]
                        gpu["capacidad"] = dato[2]                        
                        
                        equipo["gpus"].append(gpu)
                    

                with sqlite3.connect (ruta_db) as conn:
                    cursor = conn.cursor()
                    cursor.execute ("SELECT nombre, mac, velocidad FROM adaptadores_red WHERE id_equipo = ?", (i,))
                    datos_redes = cursor.fetchall()
                    
                    for dato in datos_redes:
                        red = {"nombre":"desconocido", "mac":"desconocido", "velocidad":"desconocido"}
                        
                        red["nombre"] = dato[0]
                        red["mac"] = dato[1]
                        red["velocidad"] = dato[2]
                        
                        equipo["redes"].append(red)
                    

                with sqlite3.connect (ruta_db) as conn:
                    cursor = conn.cursor()
                    cursor.execute ("SELECT nombre, tipo FROM usuarios WHERE id_equipo = ?", (i,))
                    datos_usuarios = cursor.fetchall()
                    
                    for dato in datos_usuarios:
                        usuario = {"nombre":"desconocido", "tipo":"desconocido"}
                        
                        usuario["nombre"] = dato[0]
                        usuario["tipo"] = dato[1]
                        
                        equipo["usuarios"].append(usuario)


                lista_equipos.append(equipo)
                
                
                return lista_equipos
            except Exception as e:
                logger.error(f"Error al consultar los equipos: {str(e)}")
                return False
                
        
    def consultar_nombres_equipos (self):
        """
        OBTIENE SOLO LO BASICO PARA LA LISTA DE EQUIPOS EN LA INTERFAZ (EQUIPOS REGISTRADOS)
        """
        
        lista_equipos = []
        
        try:
            with sqlite3.connect (ruta_db) as conn:
                cursor = conn.cursor()
                cursor.execute ("SELECT  id_equipo, custom_name, hostname, fecha_registro, hora_registro,serial_bios FROM equipos ORDER BY id_equipo DESC")
                equipos = cursor.fetchall()
                
                for equipo in equipos:
                    equipo = {"id_equipo":equipo[0], "custom_name":equipo[1], "hostname":equipo[2], "fecha_registro":equipo[3], "hora_registro":equipo[4], "serial_bios":equipo[5]}
                    lista_equipos.append(equipo)
                    
                return lista_equipos
        except Exception as e:
            logger.error(f"Error al consultar los equipos: {str(e)}")
            return False
        
    def obtener_datos_equipo (self, id_equipo):
        infogeneral = {}
        usuarios = []
        discos = []
        memorias = []
        gpus = []
        adapt_redes = []
        
        
        try:
            #informacion general
            with sqlite3.connect (ruta_db) as conn:
                cursor = conn.cursor()
                cursor.execute ("SELECT custom_name, hostname,modelo, fabricante, serial_bios, bios_version, serial_placa_madre, modelo_placa_madre, version_placa_madre, procesador, sistema_operativo, licencia, zona_horaria, idioma, dominio_grupo_trabajo, notas_equipo, fecha_registro, hora_registro FROM equipos WHERE id_equipo = ?", (id_equipo,))
                equipo = cursor.fetchone()
                
                if equipo:
                    infogeneral = {"custom_name":equipo[0], "hostname":equipo[1], "modelo": equipo[2], "fabricante_bios": equipo[3], "serial_bios": equipo[4],"bios_version":equipo[5], "serial_motherboard":equipo[6], "modelo_motherboard":equipo[7], "version_motherboard":equipo[8], "procesador":equipo[9], "sistema_operativo":equipo[10], "licencia":equipo[11], "zona_horaria":equipo[12], "idioma":equipo[13], "dominio_grupo_trabajo":equipo[14],  "notas_equipo":equipo[15], "fecha_registro": equipo[16], "hora_registro":equipo[17]}

            #informacion usuarios
            with sqlite3.connect (ruta_db) as conn:
                cursor = conn.cursor()
                cursor.execute ("SELECT nombre, tipo FROM usuarios WHERE id_equipo = ?", (id_equipo,))
                datos_usuarios = cursor.fetchall()

                for dato in datos_usuarios:
                    
                    usuario = {"nombre":dato[0], "tipo":dato[1]}
                    usuarios.append(usuario)

            #informacion disco (almacenamiento)
            with sqlite3.connect (ruta_db) as conn:
                cursor= conn.cursor()
                cursor.execute ("SELECT modelo, capacidad, serial, interfaz, fallos_criticos FROM disco WHERE id_equipo = ?", (id_equipo,))
                datos_discos = cursor.fetchall()
                                    
                for dato in datos_discos:
                    disco = {"modelo":dato[0], "capacidad":dato[1], "serial":dato[2], "interfaz":dato[3], "fallos_criticos":"No detectados"}

                    if dato[4] == 0:
                        disco["fallos_criticos"] = "Detectados"

                    discos.append(disco)
                
            #informacion memorias
            with sqlite3.connect (ruta_db) as conn:
                cursor= conn.cursor()
                cursor.execute ("SELECT fabricante, capacidad, serial, partnumber, tipo FROM memorias WHERE id_equipo = ?", (id_equipo,))
                datos_memorias = cursor.fetchall()

                for dato in datos_memorias:
                    
                    memoria = {"fabricante":dato[0], "capacidad":dato[1], "serial":dato[2], "partnumber":dato[3], "tipo":dato[4]}
                    memorias.append(memoria)
            
            
            #informacion adaptadores de red
            with sqlite3.connect (ruta_db) as conn:
                cursor = conn.cursor()
                cursor.execute ("SELECT nombre, mac, velocidad FROM adaptadores_red WHERE id_equipo = ?", (id_equipo,))
                datos_redes = cursor.fetchall()
                
                for dato in datos_redes:
                    red = {"nombre":dato[0], "mac":dato[1], "velocidad":dato[2]}
                    adapt_redes.append(red)
        
        
            with sqlite3.connect (ruta_db) as conn:
                cursor = conn.cursor()
                cursor.execute ("SELECT modelo, fabricante, capacidad FROM gpu WHERE id_equipo = ?", (id_equipo,))
                datos_gpus = cursor.fetchall()
                
                for dato in datos_gpus:
                    gpu = {"modelo":dato[0], "fabricante":dato[1], "capacidad":dato[2]}
                    gpus.append(gpu)
            
            
            
            
            return infogeneral, usuarios, discos, memorias, adapt_redes, gpus


        except Exception as e:
            logger.error(f"Error al consultar los equipos: {str(e)}")
            return False 

    def insertar_notas (self, notas, id_equipo):
        """
        Inserta las notas escrita desde la interfaz en la base de datos
        """
        try:
            with sqlite3.connect (ruta_db) as conn:
                cursor = conn.cursor()
                cursor.execute ("UPDATE equipos SET notas_equipo = ? WHERE id_equipo = ?", (notas, id_equipo))
                if cursor.rowcount == 0:
                    return False
                return True

        except Exception as e:
            logger.error(f"Error al insertar las notas: {str(e)}")
            return False

    def actualizar_custom_name (self, nombre_personalizado, id_equipo):
        """
        Actualiza el custom name en la base de datos
        """

        try:
            with sqlite3.connect (ruta_db) as conn:
                cursor = conn.cursor()
                cursor.execute ("UPDATE equipos SET custom_name = ? WHERE id_equipo = ?", (nombre_personalizado, id_equipo))
                if cursor.rowcount == 0:
                    return False
                
                return True

        except Exception as e:
            logger.error(f"Error al actualizar el custom name: {str(e)}")
            return False

    def eliminar_equipo (self, id, nombre_personalizado):

        try:
            with sqlite3.connect (ruta_db) as conn:
                cursor = conn.cursor()
                cursor.execute ("DELETE FROM equipos WHERE id_equipo = ? AND custom_name = ?", (id, nombre_personalizado))

                if cursor.rowcount == 0:
                    logger.error("Error al eliminar el equipo: el equipo no fue encontrado")
                    return False

                return True

        except Exception as e:
            logger.error(f"Error al eliminar el equipo: {str(e)}")
            return False

    def buscar_equipo (self, texto):
        """
        REALIZA BUSQUEDA PARCIAL DEL EQUIPO Y DEVUELE UNA LISTA DE TUPLAS
        """
        custom_name =f"%{texto}%"
        hostname = hostname =f"%{texto}%"
        serial_bios = serial_bios =f"%{texto}"
        lista_equipos = []
        
        try:
            with sqlite3.connect (ruta_db) as conn:
                cursor = conn.cursor()
                cursor.execute ("SELECT id_equipo, custom_name, hostname, fecha_registro, hora_registro,serial_bios FROM equipos WHERE custom_name LIKE ? OR hostname LIKE ? OR serial_bios LIKE ? ORDER BY fecha_registro DESC", (custom_name, hostname, serial_bios))

                equipos = cursor.fetchall()
                
                for equipo in equipos:
                    equipo = {"id_equipo":equipo[0], "custom_name":equipo[1], "hostname":equipo[2], "fecha_registro":equipo[3], "hora_registro":equipo[4], "serial_bios":equipo[5]}
                    lista_equipos.append(equipo)
                    
                return lista_equipos

        except Exception as e:
            logger.error(f"Error al buscar el equipo: {str(e)}")
            return lista_equipos

    def copia_seguridad (self, ruta):
        
        if ruta_db.exists():
            try:
                shutil.copy2(ruta_db, ruta)
                return True
            except Exception as e:
                
                logger.error(f"Error al copiar la base de datos: {str(e)}")
                return False

        return False            

    def importar_db (self, ruta):
        
            try:
                shutil.copy2(ruta, ruta_db)
                return True
            except Exception as e:
                logger.error(f"Error al importar la base de datos: {str(e)}")
                return False
            
