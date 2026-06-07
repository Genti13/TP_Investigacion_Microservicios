"""
This script runs the Microservicio_Reporte application using a development server.
"""

from os import environ
from Microservicio_Reporte import app

if __name__ == '__main__':
    #Esto es ignorado, se debe configurar en las propiedades del proyecto
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
