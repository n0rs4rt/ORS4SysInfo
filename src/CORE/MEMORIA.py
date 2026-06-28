import wmi, logging

logger = logging.getLogger("logs")

#clase para obtener la memoria:

        
        
""" Clase para tipo de memoria
Campo    	        Fuente de datos	                            ¿Siempre funciona?              	 Valores esperados
MemoryType	        Reportado por Windows vía WMI	            A veces falla o es None     	     20 (DDR), 21 (DDR2), 24 (DDR3), 26 (DDR4), 34 (DDR5) o None
SMBIOSMemoryType	Extraído directamente del SMBIOS (BIOS)	    Más confiable en PCs modernas	     20 (DDR), 21 (DDR2), 24 (DDR3), 26 (DDR4), 34 (DDR5) o None
"""



class Memoria():
    def __init__(self):
        self.memorias = []
        self.win = wmi.WMI()
    
    def datos_memoria(self):        

        capacidad = "Desconocida"
        fabricante = "Desconocido"
        serial = "Desconocido"
        tipo = "Desconocido"
        partnumber = "Desconocido"
        ddr = {20:"DDR", 21:"DDR2", 24:"DDR3", 26:"DDR4", 34:"DDR5"}
        
        try:
            for i in self.win.Win32_PhysicalMemory():
            # print (i)
                capacidad = int(i.Capacity) / (1024**3)
                if i.Manufacturer:
                    fabricante = i.Manufacturer
                
                if i.SerialNumber:
                    serial = i.SerialNumber
                
                if i.PartNumber:
                    partnumber = i.PartNumber
                
                if i.SMBIOSMemoryType:
                    
                    try:
                        if i.SMBIOSMemoryType: #verificamos si retorna un valor o numero
                            tipo = ddr[i.SMBIOSMemoryType]
                        else: 
                            tipo = ddr[i.MemoryType]
                            
                    except Exception as e :
                        logger.error(f" Error al obtener el tipo de la memoria {str(e)} ")
                        
                datos = {"capacidad": capacidad,
                    "fabricante": fabricante,
                    "serial" : serial,
                    "tipo" : tipo,
                    "partnumber" : str(partnumber).strip()} #aveces el partnum se devuelve con espacios en blanco al final e inicio
        
                self.memorias.append(datos)        
    
        except Exception as e:
            logger.error(f" No fue posible octener los datos de la ram, error {e}")
            
            datos = {"capacidad": capacidad,
                "fabricante": fabricante,
                "serial" : serial,
                "tipo" : tipo,
                "partnumber" : str(partnumber).strip()} #aveces el partnum se devuelve con espacios en blanco al final e inicio
        
            self.memorias.append(datos)  

        if not self.memorias:
            datos = {"capacidad": capacidad,
                "fabricante": fabricante,
                "serial" : serial,
                "tipo" : tipo,
                "partnumber" : str(partnumber).strip()} #aveces el partnum se devuelve con espacios en blanco al final e inicio
        
            self.memorias.append(datos)  
        
        
        return self.memorias
