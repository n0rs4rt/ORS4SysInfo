import sqlite3,  smtplib , ssl, logging
from cryptography.fernet import Fernet
from email.message import EmailMessage

from CORE.RUTAS import *

logger = logging.getLogger("logs")
class Email:
    def __init__(self,  smtp_server = None, smtp_port = None, seguridad = None, email = None, usuario = None, password = None ):
        clave_master = b'tCGcvp_7v6fO2kAFJumr2r-q1IwGwUKqWNN27t9Ft0I=' #clave maestra para desencriptar la pass del usuario
        
        self.Fernet = Fernet(clave_master) #objeto cifrador
        
        self.password_cifrada = None #pass cifrada
        self.password_descifrada = None #pass descifrada
        
        self.usuario = usuario
        self.password = password #password del usuario
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.email = email
        self.seguridad = seguridad
        
    def _cifrar_contrasena (self, password):
        self.password_cifrada = self.Fernet.encrypt(password.encode("utf-8"))
        
    def _descifrar_contrasena (self):
        self.password_descifrada = self.Fernet.decrypt(self.password_cifrada).decode("utf-8")
        
        
    def enviar_teste (self):
        """
        Envia un email de prueba para verificar la configuracion de e-mail
        """
        
        try:
            self._cifrar_contrasena(self.password)
            self._descifrar_contrasena()
            msg = EmailMessage()
            msg ["From"] = self.email
            msg["To"] = self.email
            msg["Subject"] = "ORS4SysInfo - Prueba de envío de e-mail"
            msg.set_content ("Este es un mensaje de prueba enviado desde ORS4SysInfo.\nLa configuración de e-mail es correcta.")
            
            if self.seguridad == "STARTTLS":
            
                #Conectarse al servidor
                with smtplib.SMTP(self.smtp_server, self.smtp_port,timeout=8) as smtp:
                    smtp.ehlo()
                    smtp.starttls(context=ssl.create_default_context())
                    smtp.ehlo()
                    smtp.login(self.usuario, self.password_descifrada)
                    smtp.send_message(msg)
                    return True
            
            elif self.seguridad == "SSL/TLS":
                with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port,timeout=8) as smtp:
                    smtp.login(self.usuario, self.password_descifrada)
                    smtp.send_message(msg)
                    return True

        except Exception as e :
            logger.error (f"error al enviar el email: {self.email} {e}")
            return False

    def guardar_config_email (self):
        """
        GUARDA O ACTUALIZA LA CONFIGURACION DEL EMAIL EN LA DB
        """
        id_config = 1
        try:
            with sqlite3.connect (ruta_config_email) as conn:
                cursor = conn.cursor()
                cursor.execute ("""
                                CREATE TABLE IF NOT EXISTS config (
                                    id_config INTEGER,
                                    smtp_server TEXT,
                                    smtp_port INTEGER,
                                    seguridad TEXT,
                                    email TEXT,
                                    usuario TEXT,
                                    password TEXT
                                )
                                """)

                cursor.execute ("SELECT COUNT(*) FROM config")
                configuracion = cursor.fetchone()[0]
                
                if configuracion:
                    
                    cursor.execute( "UPDATE config SET smtp_server = ?, smtp_port = ?, seguridad=?, usuario=?, email=?, password=? WHERE id_config  = ?", ( self.smtp_server, self.smtp_port, self.seguridad, self.usuario, self.email, self.password_cifrada.decode("utf-8"), id_config) )
                    
                    if cursor.rowcount == 0:
                        logger.error("Error al guardar la configuración del E-mail") 
                        return False
                    
                else: 
                    cursor.execute ("""
                                    INSERT INTO config (id_config, smtp_server, smtp_port, seguridad, usuario, email, password) VALUES (?, ?, ?, ?, ?,?, ?)
                                    """,(id_config, self.smtp_server,self.smtp_port,self.seguridad,self.usuario,self.email,self.password_cifrada.decode("utf-8")))
                return True

        except Exception as e:
            logger.error(f"Error al guardar la configuración del E-mail: {e}")
            return False

    def leer_config_email (self):
        """
        Lee la configuración del E-mail desde la base de datos

        """
        
        if ruta_config_email.exists():
            try:
                with sqlite3.connect (ruta_config_email) as conn:
                    cursor = conn.cursor()
                    cursor.execute ("SELECT smtp_server, smtp_port, seguridad, usuario, email, password FROM config")
                    resultado = cursor.fetchone()
                
                if resultado:
                    
                    self.smtp_server = resultado[0]
                    self.smtp_port = resultado[1]
                    self.seguridad = resultado[2]
                    self.usuario = resultado[3]
                    self.email = resultado[4]
                    self.password_cifrada = resultado[5].encode("utf-8")
                    self._descifrar_contrasena()

                    return (self.smtp_server, self.smtp_port, self.seguridad, self.usuario, self.email, self.password_descifrada)
            
            except Exception as e:
                logger.error(f"Error al leer la configuración del E-mail: {e}")
                return False

    def enviar_reporte (self, destinatario, cc, asunto, mensaje, adjunto):
        try:
            msg = EmailMessage()
            msg ["From"] = self.email
            msg["To"] = destinatario
            if cc:
                msg["Cc"] = cc
            msg["Subject"] = asunto
            msg.set_content (mensaje)
            
            with open(adjunto, "rb") as reporte:
                contenido = reporte.read()
                msg.add_attachment(contenido, maintype = "application", subtype = "pdf", filename = adjunto.name)
            
            if self.seguridad == "STARTTLS":
            
                #Conectarse al servidor
                with smtplib.SMTP(self.smtp_server, self.smtp_port,timeout=8) as smtp:
                    smtp.ehlo()
                    smtp.starttls(context=ssl.create_default_context())
                    smtp.ehlo()
                    smtp.login(self.usuario, self.password_descifrada)
                    smtp.send_message(msg)
                    
                
                return True
            
            elif self.seguridad == "SSL/TLS":
                with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port,timeout=8) as smtp:
                    smtp.login(self.usuario, self.password_descifrada)
                    smtp.send_message(msg)
                
                return True

        except Exception as e :
            logger.error (f"error al enviar el email: {self.email} {e}")
            return False
        