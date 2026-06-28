import wmi, logging

logger = logging.getLogger("logs")

class Red:
    def __init__(self):
        self.adaptadores = []
        self.total_adapt = 0
        self.win = wmi.WMI()
        
    def datos_adaptador(self):
        nombre = "Desconocido"
        mac = "Desconocido"
        velocidad = "Desconocido"
        
        try:
            for i in self.win.Win32_NetworkAdapter():
                if i.NetConnectionID : #Si devuelve informacion como el nombre es porque windows usa ese adaptador, sino es porque es un adaptador sin driver o no valido 
                    # print (i)
                    try:
                        nombre = i.NetConnectionID
                    except Exception as e:
                        logger.error(f"Error al detectar el nombre del adaptador de red: {e}")
                    try:
                        mac = i.MACAddress
                    except Exception as e:
                        logger.error(f"Error al detectar la MAC del adaptador de red: {e}")
                    try:
                        if i.speed:
                            #Si el adaptador no esta conectado devolvera el valor minimo en int64 o tal vez none por eso hacemos esta condicion
                            if int (i.speed) == 9223372036854775807:
                                velocidad = "Sin conexion a la red"
                            #una variable para hacer el calculo
                            else:
                                speed = int (int(i.speed) / 1_000_000)
                                if speed < 1000:
                                    velocidad = f"{speed} Mbps"
                                else:
                                    velodicad_gb = speed / 1000
                                    velocidad = f"{velodicad_gb:g} Gbps"
                    except Exception as e:
                        logger.error(f"Error al detectar la velocidad del adaptador de red: {e}")
                        
                    adaptador = {
                        "nombre": nombre,
                        "mac": mac,
                        "velocidad": velocidad
                    }
                    
                    #Lo agregamos dentro del propio if porque si no se cumple la condicion dara error porque adaptador aun no existiria
                    self.adaptadores.append(adaptador)


            return self.adaptadores
        
        except Exception as e:
            logger.error(f"Error al obtener los datos de los adaptadores de red: {str(e)}")

