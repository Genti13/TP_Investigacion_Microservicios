from flask import Flask, jsonify
from sqlalchemy import create_engine, text
from Microservicio_OEE import app
from dotenv import load_dotenv
import os
import traceback

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

@app.route('/api/oee/all-equipment', methods=['GET'])
def obtener_oee_todos_los_equipos():
    query = text("""
        WITH RowDataOrdenada AS (
            SELECT 
                e.EquipmentID,
                e.NombreName,
                e.Area,
                s.TiempoPlanificadoMinutos,
                s.VelocidadIdealPorMinuto,
                r.TiempoParadaMinutos,
                r.TotalProducido,
                r.TotalDefectuosos,
                ROW_NUMBER() OVER (PARTITION BY e.EquipmentID ORDER BY r.FechaRegistro DESC) as Position
            FROM dbo.oee_raw_data r
            INNER JOIN dbo.production_shift s ON r.ShiftID = s.ShiftID
            INNER JOIN dbo.asset_equipment e ON s.EquipmentID = e.EquipmentID
        )
        SELECT * FROM RowDataOrdenada WHERE Position = 1;
    """)

    try:
        with engine.connect() as connection:
            result = connection.execute(query).fetchall()
            
            lista_equipos = []
            for row in result:
                t_planificado = row.TiempoPlanificadoMinutos
                v_ideal = row.VelocidadIdealPorMinuto
                t_parada = row.TiempoParadaMinutos
                t_producido = row.TotalProducido
                t_defectuosos = row.TotalDefectuosos

                t_operativo = t_planificado - t_parada
                disponibilidad = (t_operativo / t_planificado) if t_planificado > 0 else 0

                capacidad_maxima = t_operativo * v_ideal
                rendimiento = (t_producido / capacidad_maxima) if capacidad_maxima > 0 else 0
                
                piezas_buenas = t_producido - t_defectuosos
                calidad = (piezas_buenas / t_producido) if t_producido > 0 else 0

                oee_final = disponibilidad * rendimiento * calidad

                lista_equipos.append({
                    "id": row.EquipmentID,
                    "nombre": row.NombreName,
                    "area": row.Area,
                    "disponibilidad": round(disponibilidad * 100, 2),
                    "rendimiento": round(rendimiento * 100, 2),
                    "calidad": round(calidad * 100, 2),
                    "oee": round(oee_final * 100, 2)
                })

            return jsonify(lista_equipos)

    except Exception as e:
        print("--- ERROR DETECTADO ---")
        traceback.print_exc() 
        return jsonify({"error": f"Error crítico: {str(e)}"}), 500