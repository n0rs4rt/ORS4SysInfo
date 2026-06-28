import wmi, logging

logger = logging.getLogger("logs")

# Clase para obtener datos del sistema operativo y bios
class Sistema_OP:
    def __init__(self):
        self.sistema_nombre = "Desconocido"
        self.bios_serial = "Desconocido"
        self.bios_fabricante = "Desconocido"
        self.bios_version = "Desconocido"
        self.arquitectura = "Desconocido"
        self.win =  wmi.WMI()
        self.dominio_grupo = "Desconocido"
        self.host = "Desconocido"
        self.modelo_PC = "Desconocido"

#DATOS DE LA BIOS
    def bios(self):

        for bios in self.win.Win32_BIOS():
            
            try: 
                self.bios_fabricante = bios.Manufacturer
            except Exception as e:
                logger.error(f"Error al obtener fabricante de la bios: {str(e)}") 
                
            try:
                #creamos una lista para agregar los datos de la version de la bios limpia sin espacios en blanco en caso que tenga
                version = []
                for i in bios.BIOSVersion:
                    version.append(i.strip()) #eliminamos los espacios en blanco
                self.bios_version = ( "".join(version)) #Unimos la cadena de caracteres
                
            except:
                logger.error(f"Error al obtener la version de la bios {str(e)}")
            
            try:
                self.bios_serial =  bios.SerialNumber
            except Exception as e:
                logger.error(f"Error al obtener el numero de serie de la bios: {str(e)}")

#DATOS DEL SYSTEMA
    def sistema(self):

        for sys in self.win.Win32_OperatingSystem():
        
            try:
                self.sistema_nombre = sys.Caption
            except Exception as e:
                logger.error(f"Error al obtener el nombre del sistema: {str(e)}")
                
            try:
                self.arquitectura = sys.OSArchitecture
            except Exception as e:
                logger.error(f"Error al obtener la arquitectura del sistema: {str(e)}")

    def dominio(self):
        try:
            for i in self.win.Win32_ComputerSystem():
                
                try:
                    self.fabricante = i.Manufacturer
                except Exception as e:
                    logger.error (f"Error al obtener el fabricante")
                
                try:
                    self.modelo_PC = i.Model
                except Exception as e:
                    logger.error (f"Error al obtener el modelo")
                
                try:
                    self.host = i.DNSHostName
                except Exception as e:
                    logger.error(f"Error al obtener el nombre del host: {str(e)}")
                try:
                    self.dominio_grupo = i.Domain
                except Exception as e:
                    logger.error(f"Error al obtener el dominio: {str(e)}")
        
        except Exception as e:
            logger.error(f"Error al obtener datos del dominio: {str(e)}")
            
    
    def resultado(self):
        
        datos = {"sistema" : self.sistema_nombre,
                "bios_serial" : self.bios_serial,
                "bios_fabricante" : self.bios_fabricante,
                "bios_version" : self.bios_version,
                "arquitectura" : self.arquitectura,
                "dominio" : self.dominio_grupo,
                "host" : self.host,
                "modelo_PC" : self.modelo_PC }
        
        return datos
        
