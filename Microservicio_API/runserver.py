"""
This script runs the Microservicio_Reporte application using a development server.
"""
from os import environ
from Microservicio_API import app

if __name__ == '__main__':
    # 🚀 CORRECCIÓN PARA DOCKER:
    # 0.0.0.0 permite que el contenedor acepte conexiones desde afuera (el Gateway)
    # El puerto 5000 es el que configuramos en el docker-compose
    HOST = '0.0.0.0'
    PORT = 5000
    
    app.run(host=HOST, port=PORT)