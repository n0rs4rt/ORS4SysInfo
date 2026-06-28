import wmi, logging

logger = logging.getLogger("logs")

class Disco ():
    def __init__(self):
        self.discos = []
        self.win = wmi.WMI()

    def leer_disco (self):
        disco = {}
        modelo = "Desconocido"
        capacidad = "Desconocido"
        almacenamiento = "Desconocido"
        serial = "Desconocido"
        tipo = "Desconocido"
        estado = "Desconocido"

        try:
            for i in self.win.Win32_DiskDrive():
                # print (i)
                try:
                    modelo = i.Model
                except Exception as e:
                    logger.error(f"Error al obtener el modelo de disco {e}")
                    
                try:
                    capacidad = int(int(i.Size) / (1024**3))
                    if capacidad < 1000:
                        almacenamiento = f"{capacidad} GB"
                    else:
                        almacenamiento = f"{capacidad / 1000} TB"

                except Exception as e:
                    logger.error (f"Error al detectar la capacidad del disco {e}")

                try:
                    serial = i.SerialNumber.strip()
                except Exception as e:
                    logger.error (f"Error al detectar el serial del disco {e}")

                try:
                    if i.InterfaceType == "IDE":
                        tipo = "SATA"
                    elif i.InterfaceType == "SCSI" and  i.PNPDeviceID and "NVME" in i.PNPDeviceID.upper():
                        tipo = "NVMe"
                    elif i.InterfaceType == "SCSI" and i.MediaType and "FIXED" not in i.MediaType.upper():
                        tipo = "USB"
                    elif i.InterfaceType == "SCSI" and  i.PNPDeviceID and "NVME" not in i.PNPDeviceID.upper() and i.MediaType and "FIXED" in i.MediaType.upper():
                        tipo = "eMMC"
                    elif i.InterfaceType == "USB":
                        tipo = "USB"
                except Exception as e:
                    logger.error (f"Error al detectar el tipo de disco {e}")

                try:
                    if i.Status == "OK":
                        estado = 1
                    else:
                        estado = 0
                except Exception as e:
                    logger.error (f"Error al detectar el estado critico del disco {e}")

                disco = {"modelo": modelo, "almacenamiento": almacenamiento, "serial" : serial, "tipo": tipo, "estado": estado}

                self.discos.append(disco)

            return self.discos

        except Exception as e:
            logger.error(f"Error al obtener datos del disco: {str(e)}")
            disco = {"modelo": modelo, "almacenamiento": almacenamiento, "serial" : serial, "tipo": tipo, "estado": estado}
            
            self.discos.append(disco)
            
            return self.discos
