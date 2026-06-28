from flask import jsonify
from Microservicio_Reporte import app
from Microservicio_Reporte.report_generator import generar_reporte,send_file
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")
HOST = os.getenv("DB_HOST")
DATABASE = os.getenv("DB_NAME")


# URL limpia
DATABASE_URL = f"mssql+pyodbc://{USER}:{PASSWORD}@{HOST}/{DATABASE}"

# Forzamos la configuración aquí
connect_args = {
    "driver": "ODBC Driver 17 for SQL Server",
    "TrustServerCertificate": "yes", 
    "Encrypt": "no" 
}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True
)
@app.route('/api/reportes/decorado', methods=['GET'])
def obtener_reporte_decorado():
    metricas_db = {}

    query = text("""
        SELECT TOP 10 
            FORMAT(FechaRegistro, 'HH:mm') as Hora, 
            ValorDecimal
        FROM dbo.asset_measurement
        ORDER BY FechaRegistro DESC;
    """)


    try:
        with engine.connect() as connection:
            result = connection.execute(query).fetchall()

            for row in result[::-1]:
                hora_str = row.Hora
                valor = float(row.ValorDecimal) if row.ValorDecimal is not None else 0.0
                metricas_db[hora_str] = valor

    except Exception as e:
        return {"error": f"Error crítico en la base de datos: {str(e)}"}, 500

    if not metricas_db:
        metricas_db = {"Sin datos": 0.0}


    payload = {
        "titulo": "Últimas 10 Mediciones Confirmadas",
        "datos": metricas_db
    }

    pdf_generado = generar_reporte(payload)

    return send_file(pdf_generado, mimetype='application/pdf', as_attachment=True, download_name='reporte.pdf')
