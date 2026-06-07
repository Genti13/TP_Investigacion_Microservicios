from flask import jsonify
from Microservicio_API import app
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")
HOST = os.getenv("DB_HOST")
DATABASE = os.getenv("DB_NAME")

DATABASE_URL = f"mssql+pyodbc://{USER}:{PASSWORD}@{HOST}/{DATABASE}?driver=ODBC+Driver+17+for+SQL+Server"
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

@app.route('/api/dashboard/metrics', methods=['GET'])
def obtener_metricas():
    metricas_db = {}
    query = text("""
        SELECT TOP 20 
            FORMAT(FechaRegistro, 'dd/MM HH:mm') as FechaHora, 
            ValorDecimal
        FROM dbo.asset_measurement
        ORDER BY FechaRegistro DESC;
    """)

    try:
        with engine.connect() as connection:
            result = connection.execute(query).fetchall()
            for row in result[::-1]:
                fecha_str = row.FechaHora
                valor = float(row.ValorDecimal) if row.ValorDecimal is not None else 0.0
                metricas_db[fecha_str] = valor

    except Exception as e:
        return jsonify({"error": f"Error crítico en la base de datos del Dashboard: {str(e)}"}), 500

    if not metricas_db:
        metricas_db = {"Sin datos": 0.0}

    total_valores = round(sum(metricas_db.values()), 2)

    respuesta = {
        "titulo": "Monitoreo de Variables en Tiempo Real",
        "datos": metricas_db,
        "total_procesado": int(total_valores),
        "estado_sistema": "Operacional"
    }
    
    return jsonify(respuesta)
