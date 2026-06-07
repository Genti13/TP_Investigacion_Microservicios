from flask import Flask, request, send_file
import io
import matplotlib
# Configuración para que matplotlib funcione en entornos sin interfaz gráfica (como Docker)
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import seaborn as sns

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

PALETA_COLOR = {
    "primario": colors.HexColor("#1A365D"),    # Azul oscuro institucional
    "secundario": colors.HexColor("#2B6CB0"),  # Azul medio
    "fondo_tabla": colors.HexColor("#F7FAFC"), # Gris claro
    "borde": colors.HexColor("#E2E8F0"),       # Gris borde
    "texto": colors.HexColor("#2D3748")        # Gris oscuro para lectura
}

styles = getSampleStyleSheet()

ESTILO_TITULO = ParagraphStyle(
    'ReporteTitulo',
    parent=styles['Heading1'],
    fontSize=26,
    leading=30,
    textColor=PALETA_COLOR["primario"],
    spaceAfter=15
)

ESTILO_SUBTITULO = ParagraphStyle(
    'ReporteSubtitulo',
    parent=styles['Heading2'],
    fontSize=16,
    leading=20,
    textColor=PALETA_COLOR["secundario"],
    spaceBefore=12,
    spaceAfter=10
)

ESTILO_PARRAFO = ParagraphStyle(
    'ReporteCuerpo',
    parent=styles['Normal'],
    fontSize=10,
    leading=14,
    textColor=PALETA_COLOR["texto"],
    spaceAfter=10
)

def agregar_titulo(story, texto):
    """Agrega el título principal del reporte."""
    story.append(Paragraph(texto, ESTILO_TITULO))

def agregar_seccion(story, titulo_seccion, descripcion=None):
    """Agrega un encabezado de sección y una descripción opcional."""
    story.append(Paragraph(titulo_seccion, ESTILO_SUBTITULO))
    if descripcion:
        story.append(Paragraph(descripcion, ESTILO_PARRAFO))
    story.append(Spacer(1, 10))

def agregar_grafico_barras(story, datos, x_label, y_label, titulo_grafico, width=450, height=220):
    """Genera un gráfico de barras con Seaborn y lo añade al PDF."""
    # Crear el gráfico en un entorno cerrado
    fig, ax = plt.subplots(figsize=(6, 3))
    
    sns.barplot(x=list(datos.keys()), y=list(datos.values()), ax=ax, palette='Blues_d')
    ax.set_title(titulo_grafico, fontsize=10, fontweight='bold', color="#1A365D")
    ax.set_xlabel(x_label, fontsize=8)
    ax.set_ylabel(y_label, fontsize=8)
    sns.despine() # Limpia los bordes superior e derecho del gráfico
    
    # Guardar en memoria
    grafico_stream = io.BytesIO()
    plt.savefig(grafico_stream, format='png', bbox_inches='tight', dpi=200)
    plt.close(fig) # Liberar memoria de matplotlib
    grafico_stream.seek(0)
    
    # Insertar en el PDF
    img = Image(grafico_stream, width=width, height=height)
    story.append(img)
    story.append(Spacer(1, 15))

def agregar_tabla(story, encabezados, filas_datos, col_widths=None):
    """Construye una tabla formateada y la añade al PDF."""
    # Combinar encabezados con los datos
    matriz_datos = [encabezados] + filas_datos
    
    # Si no se definen anchos, ReportLab los calcula automáticamente
    t = Table(matriz_datos, colWidths=col_widths)
    
    # Estilo limpio y moderno
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PALETA_COLOR["primario"]),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 10),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('BOTTOMPADDING', (0,0), (-1,0), 8),
        ('TOPPADDING', (0,0), (-1,0), 8),
        # Filas de datos
        ('BACKGROUND', (0,1), (-1,-1), PALETA_COLOR["fondo_tabla"]),
        ('TEXTCOLOR', (0,1), (-1,-1), PALETA_COLOR["texto"]),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,1), (-1,-1), 9),
        ('BOTTOMPADDING', (0,1), (-1,-1), 6),
        # Líneas divisorias discretas
        ('LINEBELOW', (0,0), (-1,-1), 0.5, PALETA_COLOR["borde"]),
    ]))
    
    story.append(t)
    story.append(Spacer(1, 15))

def agregar_grafico_tendencia(story, datos, x_label, y_label, titulo_grafico, width=450, height=220):
    """Genera un gráfico de tendencia (líneas) con Seaborn y lo añade al PDF."""
    # 1. Crear el entorno del gráfico
    fig, ax = plt.subplots(figsize=(6, 3))
    
    meses = list(datos.keys())
    valores = list(datos.values())
    
    # 2. Dibujar la línea de tendencia con marcadores en los puntos
    sns.lineplot(
        x=meses, 
        y=valores, 
        ax=ax, 
        color="#2B6CB0",      # Color secundario de nuestra paleta
        linewidth=2.5, 
        marker='o',           # Marcador redondo en cada mes
        markersize=6,
        markerfacecolor="#1A365D" # Color oscuro para resaltar el punto
    )
    
    # Estilizado de títulos y ejes
    ax.set_title(titulo_grafico, fontsize=10, fontweight='bold', color="#1A365D", pad=10)
    ax.set_xlabel(x_label, fontsize=8, color="#4A5568")
    ax.set_ylabel(y_label, fontsize=8, color="#4A5568")
    
    # Mejoras visuales: cuadrícula horizontal sutil y quitar bordes innecesarios
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    sns.despine(left=True, bottom=False) # Deja solo el eje X
    
    # 3. Guardar en memoria (BytesIO)
    grafico_stream = io.BytesIO()
    plt.savefig(grafico_stream, format='png', bbox_inches='tight', dpi=200)
    plt.close(fig)
    grafico_stream.seek(0)
    
    # 4. Insertar en el PDF
    img = Image(grafico_stream, width=width, height=height)
    story.append(img)
    story.append(Spacer(1, 15))

def generar_reporte(data_request):
    titulo_doc = data_request.get('titulo', 'Reporte por Defecto')
    metricas = data_request.get('datos', {})
    
    pdf_stream = io.BytesIO()
    doc = SimpleDocTemplate(
        pdf_stream, 
        pagesize=letter, 
        rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40
    )
    
    story = []
    
    # --- Estructura del PDF ---
    agregar_titulo(story, titulo_doc)
    
    agregar_seccion(
        story, 
        titulo_seccion="1. Análisis de Tendencia Temporal", 
        descripcion="El siguiente gráfico muestra la dirección y velocidad del cambio en las métricas durante el período seleccionado."
    )
    
    # LLAMADA AL NUEVO GRÁFICO DE TENDENCIA
    agregar_grafico_tendencia(
        story, 
        datos=metricas, 
        x_label="Meses", 
        y_label="Progreso Académico", 
        titulo_grafico="Tendencia de Rendimiento Histórico"
    )
    
    agregar_seccion(story, titulo_seccion="2. Desglose de Datos")
    
    headers = ["Período", "Métricas Registradas"]
    filas = [[k, f"{v} pts"] for k, v in metricas.items()]
    
    agregar_tabla(story, encabezados=headers, filas_datos=filas, col_widths=[200, 150])
    
    # Compilar PDF
    doc.build(story)
    pdf_stream.seek(0)
    
    return pdf_stream