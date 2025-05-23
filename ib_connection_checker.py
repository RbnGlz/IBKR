#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para verificar la conexión a la API de Interactive Brokers.
Muestra solo mensajes relevantes y omite errores no esenciales.
"""

import sys
import logging
import time
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.common import *

# Configurar logging para mostrar solo mensajes relevantes
logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

class IBConnectionChecker(EWrapper, EClient):
    """
    Clase para verificar la conexión a Interactive Brokers.
    Hereda de EWrapper y EClient para manejar la comunicación con la API.
    """
    
    def __init__(self):
        EClient.__init__(self, self)
        self.connection_successful = False
        self.connection_error = None
        
    def error(self, reqId, errorCode, errorString, advancedOrderRejectJson=""):
        """
        Maneja los mensajes de error de la API.
        Filtra los errores no esenciales y registra solo los relevantes.
        """
        # Códigos de error no esenciales que queremos omitir
        non_essential_errors = [2104, 2106, 2158]
        
        if errorCode not in non_essential_errors:
            logger.error(f"Error {errorCode}: {errorString}")
            
            # Errores críticos de conexión
            critical_errors = [1100, 1101, 1102, 1300, 504, 502, 509, 10054]
            if errorCode in critical_errors:
                self.connection_error = f"Error crítico de conexión: {errorCode} - {errorString}"
    
    def connectAck(self):
        """
        Se llama cuando la conexión ha sido establecida.
        """
        super().connectAck()
        logger.info("Conexión establecida con Interactive Brokers")
        self.connection_successful = True
    
    def nextValidId(self, orderId):
        """
        Se llama después de una conexión exitosa con el siguiente ID válido.
        Este método confirma que la conexión está completamente establecida.
        """
        super().nextValidId(orderId)
        self.connection_successful = True
        print("✅ Conexión exitosa a la API de Interactive Brokers")
        print(f"   Siguiente ID de orden válido: {orderId}")
        
        # Desconectar después de verificar la conexión
        self.disconnect()

def check_connection(host='127.0.0.1', port=7497, client_id=1, timeout=10):
    """
    Verifica la conexión a la API de Interactive Brokers.
    
    Args:
        host (str): Dirección IP del TWS o IB Gateway
        port (int): Puerto de conexión (7497 para TWS demo, 7496 para TWS real,
                   4002 para IB Gateway demo, 4001 para IB Gateway real)
        client_id (int): ID de cliente único
        timeout (int): Tiempo máximo de espera para la conexión en segundos
    
    Returns:
        bool: True si la conexión fue exitosa, False en caso contrario
    """
    app = IBConnectionChecker()
    
    try:
        print(f"Intentando conectar a Interactive Brokers ({host}:{port})...")
        app.connect(host, port, client_id)
        
        # Iniciar el procesamiento de mensajes en un hilo separado
        api_thread = threading.Thread(target=app.run)
        api_thread.start()
        
        # Esperar hasta que se establezca la conexión o se agote el tiempo
        start_time = time.time()
        while not app.connection_successful and time.time() - start_time < timeout:
            time.sleep(0.1)
            
            if app.connection_error:
                print(f"❌ {app.connection_error}")
                app.disconnect()
                return False
        
        # Verificar si se agotó el tiempo de espera
        if not app.connection_successful:
            print(f"❌ Tiempo de espera agotado después de {timeout} segundos")
            app.disconnect()
            return False
            
        # Esperar a que se complete la desconexión
        api_thread.join(timeout=5)
        return app.connection_successful
        
    except Exception as e:
        print(f"❌ Error al conectar: {str(e)}")
        return False

if __name__ == "__main__":
    import argparse
    import threading
    
    parser = argparse.ArgumentParser(description='Verificador de conexión a Interactive Brokers')
    parser.add_argument('--host', default='127.0.0.1', help='Dirección IP del TWS o IB Gateway')
    parser.add_argument('--port', type=int, default=7497, 
                        help='Puerto (7497: TWS demo, 7496: TWS real, 4002: Gateway demo, 4001: Gateway real)')
    parser.add_argument('--client-id', type=int, default=1, help='ID de cliente')
    parser.add_argument('--timeout', type=int, default=10, help='Tiempo máximo de espera en segundos')
    
    args = parser.parse_args()
    
    # Ejecutar la verificación de conexión
    success = check_connection(
        host=args.host,
        port=args.port,
        client_id=args.client_id,
        timeout=args.timeout
    )
    
    # Establecer el código de salida
    sys.exit(0 if success else 1)
