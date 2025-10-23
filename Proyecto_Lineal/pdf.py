from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from datetime import datetime

pdf_name = "Entrega_Proyecto_Algebra_Lineal_FINAL.pdf"
doc = SimpleDocTemplate(pdf_name, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
elements = []
styles = getSampleStyleSheet()

title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontSize=20, textColor=colors.HexColor('#003366'), alignment=1, spaceAfter=12)
heading_style = ParagraphStyle('Heading', parent=styles['Heading2'], fontSize=12, textColor=colors.HexColor('#003366'), spaceAfter=6)

# PORTADA
elements.append(Spacer(1, 1*inch))
elements.append(Paragraph("PROYECTO DE ALGEBRA LINEAL", title_style))
elements.append(Spacer(1, 0.2*inch))
elements.append(Paragraph("ENTREGA #2", title_style))
elements.append(Spacer(1, 0.3*inch))
elements.append(Paragraph("Rutas Optimas en Redes de Telecomunicaciones", heading_style))
elements.append(Spacer(1, 0.5*inch))

fecha = datetime.now().strftime("%d de %B de %Y")
info = f"""<b>Estudiantes:</b><br/>
Dubin Andres Soto Parodi<br/>
Juan David Idarraga Porras<br/>
David Santiago Munoz Espinel<br/><br/>
<b>Profesor:</b> Juan Pablo Fernandez Gutierrez<br/>
<b>Universidad:</b> Universidad de Medellin<br/>
<b>Fecha:</b> {fecha}"""
elements.append(Paragraph(info, styles['Normal']))
elements.append(PageBreak())

# TABLA CONTENIDOS
elements.append(Paragraph("TABLA DE CONTENIDOS", heading_style))
elements.append(Spacer(1, 0.2*inch))
for item in ["1. Marco Teorico", "2. Formulacion del Problema", "3. Solucion Optima", "4. Validacion de Restricciones", "5. Analisis Comparativo", "6. Conclusiones"]:
    elements.append(Paragraph(item, styles['Normal']))
elements.append(PageBreak())

# 1. MARCO TEORICO
elements.append(Paragraph("1. MARCO TEORICO", heading_style))

# Teoria Grafos
elements.append(Paragraph("<b>1.1 Teoria de Grafos</b>", styles['Heading3']))
marco1 = """Un grafo G = (V, E) consta de:<br/>
- V = vertices (nodos): {A, B, C, D, E, F}<br/>
- E = aristas (enlaces): {(A,B), (A,C), (B,D), (B,E), (C,D), (D,E), (D,F), (E,F)}<br/><br/>
Caracteristicas:<br/>
- No dirigido: enlaces bidireccionales<br/>
- Ponderado: cada enlace tiene peso (latencia, capacidad)<br/>
- Conexo: existe camino entre cualquier par de nodos"""
elements.append(Paragraph(marco1, styles['Normal']))
elements.append(Spacer(1, 0.1*inch))

# Tabla enlaces
enlaces_data = [
    ["Enlace", "Latencia (ms)", "Capacidad (Gbps)"],
    ["A-B", "10", "100"], ["A-C", "15", "80"], ["B-D", "5", "50"],
    ["B-E", "8", "120"], ["C-D", "12", "90"], ["D-E", "4", "110"],
    ["D-F", "20", "60"], ["E-F", "10", "150"]
]
t1 = Table(enlaces_data, colWidths=[1.5*inch, 2*inch, 2*inch])
t1.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003366')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
]))
elements.append(t1)
elements.append(Spacer(1, 0.15*inch))

# Caminos
elements.append(Paragraph("<b>Caminos posibles de A a F:</b>", styles['Heading3']))
caminos_data = [
    ["Ruta", "Calculo", "Latencia Total"],
    ["A->B->E->F", "10+8+10", "28 ms [OPTIMA]"],
    ["A->B->D->F", "10+5+20", "35 ms"],
    ["A->C->D->F", "15+12+20", "47 ms"],
    ["A->C->D->E->F", "15+12+4+10", "41 ms"],
    ["A->B->D->E->F", "10+5+4+10", "29 ms"]
]
t_caminos = Table(caminos_data, colWidths=[1.5*inch, 2*inch, 2*inch])
t_caminos.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003366')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 8),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#FFFFE0')),
]))
elements.append(t_caminos)
elements.append(PageBreak())

# Matrices
elements.append(Paragraph("<b>1.2 Matrices de Algebra Lineal</b>", styles['Heading3']))
matrices = """<b>Matriz de Adyacencia:</b> Muestra conectividad entre nodos (1=conectado, 0=no)<br/><br/>
<b>Matriz de Costos:</b> Almacena latencia en ms de cada enlace<br/>
Ejemplo: C[A,B]=10, C[B,E]=8, C[E,F]=10<br/><br/>
<b>Matriz de Capacidades:</b> Almacena ancho de banda maximo en Gbps<br/>
Ejemplo: Cap[A,B]=100, Cap[B,E]=120, Cap[E,F]=150<br/><br/>
Estas matrices permiten representar la red algebraicamente para procesarla matematicamente."""
elements.append(Paragraph(matrices, styles['Normal']))
elements.append(Spacer(1, 0.1*inch))

# Programacion Lineal
elements.append(Paragraph("<b>1.3 Programacion Lineal</b>", styles['Heading3']))
proglin = """<b>Objetivo:</b> Minimizar latencia total<br/>
<b>Variables:</b> xij = trafico (Gbps) nodo i a nodo j<br/>
<b>Funcion Objetivo:</b> MIN Z = Suma(latenciaij x xij)<br/>
<b>Restricciones:</b><br/>
1. Conservacion de flujo (balance en nodos intermedios)<br/>
2. Capacidad maxima: xij <= capacidadij<br/>
3. No-negatividad: xij >= 0<br/>
4. Trafico: A envia 40 Gbps, F recibe 40 Gbps"""
elements.append(Paragraph(proglin, styles['Normal']))
elements.append(PageBreak())

# 2. FORMULACION
elements.append(Paragraph("2. FORMULACION DEL PROBLEMA", heading_style))
form = """<b>Variables de Decision:</b>
xij = cantidad de trafico (Gbps) que fluye del nodo i al nodo j
Total: 16 variables (8 enlaces x 2 direcciones)<br/><br/>

<b>Funcion Objetivo:</b>
Minimizar Z = Suma(latenciaij x xij)<br/><br/>

<b>Restricciones:</b>
1. Conservacion: Flujo_saliente - Flujo_entrante = Trafico_neto
2. Capacidad: xij <= capacidadij para cada enlace
3. No-negatividad: xij >= 0
4. Trafico origen-destino: x_out(A) = 40, x_in(F) = 40"""
elements.append(Paragraph(form, styles['Normal']))
elements.append(PageBreak())

# 3. SOLUCION OPTIMA
elements.append(Paragraph("3. SOLUCION OPTIMA", heading_style))
sol = """<b>Ruta Optima Encontrada:</b>
A -> B -> E -> F<br/><br/>

<b>Flujo de Trafico:</b>
- xAB = 40 Gbps (A envia a B)
- xBE = 40 Gbps (B envia a E)
- xEF = 40 Gbps (E envia a F)
- Todos los demas enlaces = 0<br/><br/>

<b>Latencia Total:</b>
Latencia = 10 (A-B) + 8 (B-E) + 10 (E-F) = <b>28 milisegundos</b><br/><br/>

<b>Valor Funcion Objetivo:</b>
Z = 10(40) + 8(40) + 10(40) = 1120 ms-Gbps"""
elements.append(Paragraph(sol, styles['Normal']))
elements.append(PageBreak())

# 4. VALIDACION
elements.append(Paragraph("4. VALIDACION DE RESTRICCIONES", heading_style))
val = """<b>Conservacion de Flujo:</b>
- Nodo A: Envia 40 Gbps (origen)
- Nodo B: 40 entra (de A), 40 sale (a E) = Equilibrado
- Nodo E: 40 entra (de B), 40 sale (a F) = Equilibrado
- Nodo F: Recibe 40 Gbps (destino)<br/><br/>

<b>Respeto de Capacidades:</b>
- Enlace A-B: 40 Gbps <= 100 Gbps (OK)
- Enlace B-E: 40 Gbps <= 120 Gbps (OK)
- Enlace E-F: 40 Gbps <= 150 Gbps (OK)<br/><br/>

<b>Conclusion:</b> Solucion es FACTIBLE y OPTIMA"""
elements.append(Paragraph(val, styles['Normal']))
elements.append(PageBreak())

# 5. ANALISIS COMPARATIVO
elements.append(Paragraph("5. ANALISIS COMPARATIVO", heading_style))
rutas_data = [
    ["Ruta", "Latencia", "Saltos", "Cuello Botella", "Estado"],
    ["A->B->E->F", "28 ms", "3", "A-B (100G)", "OPTIMA"],
    ["A->B->D->F", "35 ms", "3", "B-D (50G)", "ALT"],
    ["A->C->D->F", "47 ms", "3", "D-F (60G)", "ALT"],
    ["A->C->D->E->F", "41 ms", "4", "A-C (80G)", "ALT"],
    ["A->B->D->E->F", "29 ms", "4", "B-D (50G)", "ALT"]
]
t_rutas = Table(rutas_data, colWidths=[1.1*inch, 0.9*inch, 0.8*inch, 1.1*inch, 1*inch])
t_rutas.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003366')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 8),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#90EE90')),
]))
elements.append(t_rutas)
elements.append(Spacer(1, 0.15*inch))

analisis = """La ruta optima (28 ms) es 7 ms mas rapida que la segunda mejor. 
Todas cumplen restricciones. El algoritmo identifica automaticamente la mejor solucion."""
elements.append(Paragraph(analisis, styles['Normal']))
elements.append(PageBreak())

# 6. CONCLUSIONES
elements.append(Paragraph("6. CONCLUSIONES", heading_style))
conc = """<b>Integracion de Conceptos:</b>
- Teoria de Grafos: estructura de la red
- Algebra Lineal: representacion matricial
- Programacion Lineal: optimizacion automatica<br/><br/>

<b>Resultados:</b>
- Ruta optima: A -> B -> E -> F
- Latencia: 28 milisegundos
- Todas restricciones cumplidas
- Validado con 5 alternativas<br/><br/>

<b>Aplicabilidad:</b>
Telecomunicaciones, centros de datos, Internet, logistica."""
elements.append(Paragraph(conc, styles['Normal']))

try:
    doc.build(elements)
    print("PDF GENERADO: Entrega_Proyecto_Algebra_Lineal_FINAL.pdf")
except Exception as e:
    print(f"Error: {e}")
