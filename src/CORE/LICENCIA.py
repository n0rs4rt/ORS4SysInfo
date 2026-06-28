import wmi, logging

logger = logging.getLogger("logs")

class Licencia:
    def __init__(self):
        self.win = wmi.WMI()

    def obtener(self):
        llave = {"licencia": "No Disponible"}
        try:
            for licencia in self.win.SoftwareLicensingProduct():
            
                try:
                                    
                    if licencia.PartialProductKey and licencia.LicenseStatus == 1 and "windows" in licencia.Name.lower() and "operating system" in licencia.Description.lower():

                        llave["licencia"] = licencia.PartialProductKey
                        return llave

                except Exception as e:
                    continue

        except Exception as e:
            logger.error(f"Error al obtener la licencia: {str(e)}")
            return llave

        return llave
    