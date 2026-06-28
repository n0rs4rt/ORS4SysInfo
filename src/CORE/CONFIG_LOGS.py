import logging
from CORE.RUTAS import ruta_logs

def config_logging():

    # Crear u obtener el logger principal llamado "logs"
    logger = logging.getLogger("logs")

    # Definir el nivel mínimo de logs (INFO, WARNING, ERROR, etc)
    logger.setLevel(logging.INFO)

    # Verificar si ya tiene handlers para evitar duplicados
    if not logger.handlers:

        # Definir el archivo donde se guardarán los logs
        handler = logging.FileHandler(ruta_logs / "logs.log")

        # Definir el formato del log
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )

        # Aplicar el formato al handler (archivo)
        handler.setFormatter(formatter)

        # Conectar el handler al logger
        logger.addHandler(handler)

    # Retornar el logger configurado
    return logger