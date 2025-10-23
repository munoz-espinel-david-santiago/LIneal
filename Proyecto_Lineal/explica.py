"""
PROYECTO DE ÁLGEBRA LINEAL - IDEA 3: RUTAS ÓPTIMAS EN REDES
Autores: Dubin Andrés Soto, Juan David Idarraga, David Santiago Muñoz
Profesor: Juan Pablo Fernández Gutiérrez
"""

# Importar librerías principales
import numpy as np                  # Operaciones con matrices y arreglos numéricos
from scipy.optimize import linprog  # Función para resolver problemas de optimización lineal
import matplotlib.pyplot as plt     # Para graficar la topología de la red
import networkx as nx               # Para modelar la red como grafo
import pandas as pd                 # Para crear y exportar tablas de resultados

# -----------------------
# 1. Definir la topología
# -----------------------

nodos = ['A', 'B', 'C', 'D', 'E', 'F']           # Lista de routers de la red
n_nodos = len(nodos)                             # Cantidad de nodos
indice_nodos = {nodo: i for i, nodo in enumerate(nodos)}  # Asocia cada nodo a un índice numérico

# Enlaces entre nodos, con la latencia en ms
enlaces = [
    ('A', 'B', 10),
    ('A', 'C', 15),
    ('B', 'D', 5),
    ('B', 'E', 8),
    ('C', 'D', 12),
    ('D', 'E', 4),
    ('D', 'F', 20),
    ('E', 'F', 10),
]

# Crear diccionario de latencias (acceso por pareja de nodos, ambos sentidos)
latencias = {}
for n1, n2, lat in enlaces:
    latencias[(n1, n2)] = lat
    latencias[(n2, n1)] = lat

# Diccionario de capacidades máximas por cada enlace (Gbps)
capacidades = {
    ('A', 'B'): 100,
    ('A', 'C'): 80,
    ('B', 'D'): 50,
    ('B', 'E'): 120,
    ('C', 'D'): 90,
    ('D', 'E'): 110,
    ('D', 'F'): 60,
    ('E', 'F'): 150,
}

# Definir nodos origen y destino y el tráfico total a enviar (Gbps)
origen = 'A'
destino = 'F'
tráfico = 40

# -----------------------
# 2. Crear matriz de costos
# -----------------------

costos = np.full((n_nodos, n_nodos), np.inf)    # Inicia matriz NxN con infinito (no hay conexión por defecto)
for n1, n2, latencia in enlaces:
    i, j = indice_nodos[n1], indice_nodos[n2]
    costos[i, j] = latencia                    # Asigna valor de latencia si hay conexión
    costos[j, i] = latencia                    # Ambos sentidos (red no dirigida)
np.fill_diagonal(costos, 0)                    # Costo cero de nodo a sí mismo

# ---------------------------
# 3. Visualizar la red en gráfico
# ---------------------------

G = nx.Graph()                                  # Crea objeto grafo vacío
G.add_nodes_from(nodos)                         # Agrega los nodos a la red
for n1, n2, latencia in enlaces:
    G.add_edge(n1, n2, weight=latencia)         # Agrega cada enlace con su latencia como 'peso'

pos = nx.spring_layout(G, seed=42, k=2.5, iterations=50)   # Calcula posiciones (para visualizar mejor)
plt.figure(figsize=(12, 8))
nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=2000, edgecolors='black', linewidths=2)
nx.draw_networkx_edges(G, pos, width=2.5, alpha=0.7)
nx.draw_networkx_labels(G, pos, font_size=16, font_weight='bold')

# Etiquetas de los enlaces: latencia y capacidad
edge_labels = {}
for n1, n2, latencia in enlaces:
    cap = capacidades.get((n1, n2), capacidades.get((n2, n1)))
    edge_labels[(n1, n2)] = f"{latencia}ms\n{cap}Gbps"
nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=12)

plt.title("Topología de Red\nLatencia (ms) y Capacidad (Gbps)", fontsize=15, fontweight='bold')
plt.axis('off')
plt.tight_layout()
plt.savefig('topologia_red_completa.png', dpi=300, bbox_inches='tight')
plt.close()     # Guarda imagen y cierra gráfico

# -------------------------------------------------
# 4. Definir el problema para scipy.optimize.linprog
# -------------------------------------------------

aristas = []
for n1, n2, _ in enlaces:
    aristas.append((n1, n2))     # Dirección ida
    aristas.append((n2, n1))     # Dirección vuelta

n_aristas = len(aristas)         # Número total de variables (enlaces dirigidos)

# Crear vector de la función objetivo: latencia para cada variable
c = np.zeros(n_aristas)
for idx, (n1, n2) in enumerate(aristas):
    c[idx] = latencias[(n1, n2)]

# Restricciones: conservación de flujo y capacidad
A_eq = np.zeros((n_nodos, n_aristas))  # Matriz para restricciones de conservación
for nodo_idx, nodo in enumerate(nodos):
    for arista_idx, (n1, n2) in enumerate(aristas):
        if nodo == n1:
            A_eq[nodo_idx, arista_idx] += 1   # Flujo saliente
        if nodo == n2:
            A_eq[nodo_idx, arista_idx] -= 1   # Flujo entrante

b_eq = np.zeros(n_nodos)                     # Vector de balance de flujo
b_eq[indice_nodos[origen]] = tráfico         # Nodo origen: envía tráfico
b_eq[indice_nodos[destino]] = -tráfico       # Nodo destino: recibe tráfico

A_ub = []
b_ub = []
for arista_idx, (n1, n2) in enumerate(aristas):
    restriccion = np.zeros(n_aristas)
    restriccion[arista_idx] = 1              # Para cada variable, aplica restricción independiente
    if (n1, n2) in capacidades:
        cap = capacidades[(n1, n2)]
    elif (n2, n1) in capacidades:
        cap = capacidades[(n2, n1)]
    else:
        cap = np.inf
    if cap != np.inf:
        A_ub.append(restriccion)
        b_ub.append(cap)
A_ub = np.array(A_ub)
b_ub = np.array(b_ub)
bounds = [(0, None) for _ in range(n_aristas)]    # El flujo debe ser ≥ 0

# ------------------------------------
# 5. Resolver el modelo de optimización
# ------------------------------------
resultado = linprog(
    c=c,
    A_ub=A_ub,
    b_ub=b_ub,
    A_eq=A_eq,
    b_eq=b_eq,
    bounds=bounds,
    method='highs'
)

# ------------------------------------
# 6. Procesar y mostrar resultados
# ------------------------------------
if resultado.success:
    flujo_optimo = resultado.x
    rutas_activas = []
    # Selecciona enlaces por los que realmente pasa tráfico
    for idx, flujo in enumerate(flujo_optimo):
        if flujo > 1e-6:
            n1, n2 = aristas[idx]
            rutas_activas.append((n1, n2, flujo))
    # Reconstruye la ruta óptima, empezando en A y avanzando hasta F
    camino = [origen]
    nodo_actual = origen
    while nodo_actual != destino:
        siguiente_encontrado = False
        for n1, n2, flujo in rutas_activas:
            if n1 == nodo_actual and flujo > 0.01:
                camino.append(n2)
                nodo_actual = n2
                siguiente_encontrado = True
                break
        if not siguiente_encontrado:
            break
    print("Camino óptimo:", " → ".join(camino))
    # Calcula la latencia total sumando los tiempos por enlace
    latencia_camino = 0
    for i in range(len(camino) - 1):
        latencia_camino += latencias[(camino[i], camino[i+1])]
    print("Latencia total:", latencia_camino, "ms")
else:
    print("✗ No se encontró solución óptima")

# ------------------------------------
# 7. Comparar rutas alternativas
# ------------------------------------
rutas_alternativas = [
    (['A', 'B', 'E', 'F'], "Óptima (linprog)"),
    (['A', 'B', 'D', 'F'], "Alternativa 1"),
    (['A', 'C', 'D', 'F'], "Alternativa 2"),
    (['A', 'C', 'D', 'E', 'F'], "Alternativa 3"),
    (['A', 'B', 'D', 'E', 'F'], "Alternativa 4"),
]
resultados = []
for ruta, desc in rutas_alternativas:
    lat_total = 0
    cap_min = np.inf
    enlace_cuello = None
    valida = True
    for i in range(len(ruta) - 1):
        n1, n2 = ruta[i], ruta[i+1]
        if (n1, n2) not in latencias:
            valida = False
            break
        lat_total += latencias[(n1, n2)]
        cap = capacidades.get((n1, n2), capacidades.get((n2, n1)))
        if cap < cap_min:
            cap_min = cap
            enlace_cuello = f"{n1}-{n2}"
    if valida:
        cumple = "✓ SÍ" if tráfico <= cap_min else "✗ NO"
        resultados.append({
            'Ruta': ' → '.join(ruta),
            'Descripción': desc,
            'Latencia (ms)': lat_total,
            'Saltos': len(ruta) - 1,
            'Cuello Botella': enlace_cuello,
            'Capacidad Mínima (Gbps)': cap_min,
            'Cumple Capacidad': cumple,
            'Costo (ms·Gbps)': lat_total * tráfico
        })
# Convierte resultados a tabla (DataFrame)
df = pd.DataFrame(resultados)
print("\n", df.to_string(index=False))
df.to_csv('analisis_rutas.csv', index=False, encoding='utf-8')    # Exporta tabla comparativa a CSV
