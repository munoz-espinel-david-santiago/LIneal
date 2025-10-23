# MARCO TEÓRICO COMPLETO
## RUTAS ÓPTIMAS EN REDES DE TELECOMUNICACIONES

---

## INTRODUCCIÓN

El álgebra lineal proporciona herramientas matemáticas para modelar, analizar y optimizar redes de comunicación. Este proyecto demuestra cómo usar:

1. **Teoría de Grafos** - para representar la red
2. **Álgebra Lineal** - para modelar la red mediante matrices
3. **Programación Lineal** - para encontrar automáticamente la ruta óptima

**Problema Central:** Encontrar la ruta de menor latencia total desde A hasta F, respetando las capacidades máximas de cada enlace, cuando se debe enviar 40 Gbps de tráfico.

---

## 1. TEORÍA DE GRAFOS

### 1.1 Definición Formal

Un **grafo** es una estructura matemática G = (V, E) donde:
- **V** = conjunto de vértices (nodos)
- **E** = conjunto de aristas (enlaces)

**En nuestro proyecto:**

V = {A, B, C, D, E, F}  (6 nodos)
E = {(A,B), (A,C), (B,D), (B,E), (C,D), (D,E), (D,F), (E,F)}  (8 enlaces)

### 1.2 Características del Grafo

- **No Dirigido:** Las aristas funcionan en ambas direcciones
- **Ponderado:** Cada arista tiene múltiples pesos (latencia, capacidad)
- **Conexo:** Existe un camino entre cualquier par de nodos

### 1.3 Visualización de la Red

```
                    A (ORIGEN)
                   /|\
                  / | \
             10ms |  | 15ms
            100Gb |  | 80Gb
               /  |  \
              B   |   C
              |\  |  /|
           5ms| \ | / |12ms
          50G | 8\|/90G
             |  \ |
             D   E
              \ /|
            20ms| |10ms
            60G | |150G
               \|/
                F (DESTINO)
```

### 1.4 Rutas Posibles de A a F

| Ruta | Cálculo | Latencia | Estado |
|------|---------|----------|--------|
| A → B → E → F | 10 + 8 + 10 | **28 ms** | ✓ ÓPTIMA |
| A → B → D → F | 10 + 5 + 20 | 35 ms | Alternativa |
| A → C → D → F | 15 + 12 + 20 | 47 ms | Alternativa |
| A → C → D → E → F | 15 + 12 + 4 + 10 | 41 ms | Alternativa |
| A → B → D → E → F | 10 + 5 + 4 + 10 | 29 ms | Alternativa |

**Objetivo del modelo:** Encontrar automáticamente que **28 ms es el mínimo** sin enumerar manualmente todas las rutas.

---

## 2. MATRICES DE ÁLGEBRA LINEAL

### 2.1 Matriz de Adyacencia A

Describe la **conectividad** entre nodos (1 = conectado, 0 = no conectado):

|   | A | B | C | D | E | F |
|---|---|---|---|---|---|---|
| **A** | 0 | 1 | 1 | 0 | 0 | 0 |
| **B** | 1 | 0 | 0 | 1 | 1 | 0 |
| **C** | 1 | 0 | 0 | 1 | 0 | 0 |
| **D** | 0 | 1 | 1 | 0 | 1 | 1 |
| **E** | 0 | 1 | 0 | 1 | 0 | 1 |
| **F** | 0 | 0 | 0 | 1 | 1 | 0 |

**Propiedades:**
- Matriz simétrica: A[i,j] = A[j,i] (grafo no dirigido)
- Diagonal principal: todos ceros (sin autolazos)

**Interpretación:**
- Fila A: [0,1,1,0,0,0] → A está conectado a B y C
- Fila D: [0,1,1,0,1,1] → D está conectado a B, C, E y F

### 2.2 Matriz de Costos (Latencias) C

Almacena la **latencia en milisegundos** de cada enlace:

|   | A | B | C | D | E | F |
|---|---|---|---|---|---|---|
| **A** | 0 | 10 | 15 | ∞ | ∞ | ∞ |
| **B** | 10 | 0 | ∞ | 5 | 8 | ∞ |
| **C** | 15 | ∞ | 0 | 12 | ∞ | ∞ |
| **D** | ∞ | 5 | 12 | 0 | 4 | 20 |
| **E** | ∞ | 8 | ∞ | 4 | 0 | 10 |
| **F** | ∞ | ∞ | ∞ | 20 | 10 | 0 |

**Interpretación:**
- C[A,B] = 10 ms (latencia de A a B es 10 milisegundos)
- C[D,E] = 4 ms (enlace más rápido)
- C[A,F] = ∞ (sin conexión directa)
- C[i,i] = 0 (latencia cero de un nodo a sí mismo)

### 2.3 Matriz de Capacidades Cap

Almacena el **ancho de banda máximo en Gbps** de cada enlace:

|   | A | B | C | D | E | F |
|---|---|---|---|---|---|---|
| **A** | 0 | 100 | 80 | ∞ | ∞ | ∞ |
| **B** | 100 | 0 | ∞ | 50 | 120 | ∞ |
| **C** | 80 | ∞ | 0 | 90 | ∞ | ∞ |
| **D** | ∞ | 50 | 90 | 0 | 110 | 60 |
| **E** | ∞ | 120 | ∞ | 110 | 0 | 150 |
| **F** | ∞ | ∞ | ∞ | 60 | 150 | 0 |

**Interpretación:**
- Enlace A-B: 100 Gbps de capacidad
- Enlace B-D: 50 Gbps (cuello de botella, el más limitado)
- Enlace E-F: 150 Gbps (muy rápido)

---

## 3. PROGRAMACIÓN LINEAL

### 3.1 Conceptos Fundamentales

La **programación lineal** es una técnica de optimización que:
- **Minimiza o maximiza** una función objetivo lineal
- **Respeta** restricciones lineales
- **Garantiza** encontrar la solución óptima (si existe)

**Estructura general:**

```
Minimizar: Z = c₁x₁ + c₂x₂ + ... + cₙxₙ

Sujeto a:
  a₁₁x₁ + a₁₂x₂ + ... + a₁ₙxₙ ≤ b₁
  a₂₁x₁ + a₂₂x₂ + ... + a₂ₙxₙ ≤ b₂
  ...
  xᵢ ≥ 0 para todo i
```

### 3.2 Variables de Decisión

Para cada **enlace dirigido** (i,j), definimos:

**xᵢⱼ = cantidad de tráfico en Gbps que fluye de nodo i a nodo j**

**En nuestro proyecto tenemos 16 variables:**

xₐᵦ, xᵦₐ, xₐ꜀, x꜀ₐ, xᵦᵨ, xᵨᵦ, xᵦₑ, xₑᵦ, x꜀ᵨ, xᵨ꜀, xᵨₑ, xₑᵨ, xᵨ꜀, x꜀ᵨ, xₑ꜀, x꜀ₑ

### 3.3 Función Objetivo

**Minimizar la latencia total ponderada:**

Z = 10xₐᵦ + 10xᵦₐ + 15xₐ꜀ + 15x꜀ₐ + 5xᵦᵨ + 5xᵨᵦ + 8xᵦₑ + 8xₑᵦ + 12x꜀ᵨ + 12xᵨ꜀ + 4xᵨₑ + 4xₑᵨ + 20xᵨ꜀ + 20x꜀ᵨ + 10xₑ꜀ + 10x꜀ₑ

Cada variable se multiplica por su latencia correspondiente. El objetivo es minimizar Z respetando todas las restricciones.

### 3.4 Restricciones de Conservación de Flujo

**Nodo A (Origen):** Debe enviar exactamente 40 Gbps
```
xₐᵦ + xₐ꜀ = 40
```

**Nodo F (Destino):** Debe recibir exactamente 40 Gbps
```
xᵨ꜀ + xₑ꜀ = 40
```

**Nodo B (Intermedio):** Lo que entra = Lo que sale
```
xₐᵦ = xᵦₐ + xᵦᵨ + xᵦₑ
```

**Nodo C (Intermedio):**
```
xₐ꜀ = x꜀ₐ + x꜀ᵨ
```

**Nodo D (Intermedio):**
```
xᵦᵨ + x꜀ᵨ = xᵨᵦ + xᵨ꜀ + xᵨₑ + xᵨ꜀
```

**Nodo E (Intermedio):**
```
xᵦₑ + xᵨₑ = xₑᵦ + xₑᵨ + xₑ꜀
```

### 3.5 Restricciones de Capacidad

Cada enlace no puede transportar más que su capacidad máxima:

```
xₐᵦ ≤ 100    xᵦₐ ≤ 100
xₐ꜀ ≤ 80     x꜀ₐ ≤ 80
xᵦᵨ ≤ 50     xᵨᵦ ≤ 50
xᵦₑ ≤ 120    xₑᵦ ≤ 120
x꜀ᵨ ≤ 90     xᵨ꜀ ≤ 90
xᵨₑ ≤ 110    xₑᵨ ≤ 110
xᵨ꜀ ≤ 60     x꜀ᵨ ≤ 60
xₑ꜀ ≤ 150    x꜀ₑ ≤ 150
```

### 3.6 Restricción de No-Negatividad

Todo tráfico debe ser no negativo:

```
xᵢⱼ ≥ 0 para todos los enlaces (i,j)
```

---

## 4. SOLUCIÓN ÓPTIMA

### 4.1 Resultado del Algoritmo

El optimizador resuelve simultáneamente todas las restricciones y devuelve:

```
xₐᵦ = 40 Gbps
xᵦₑ = 40 Gbps
xₑ꜀ = 40 Gbps
Todos los demás xᵢⱼ = 0
```

### 4.2 Ruta Óptima

**A → B → E → F**

### 4.3 Flujo de Tráfico

- Nodo A: Envía 40 Gbps a B
- Nodo B: Recibe 40 Gbps de A y envía 40 Gbps a E
- Nodo E: Recibe 40 Gbps de B y envía 40 Gbps a F
- Nodo F: Recibe 40 Gbps de E

### 4.4 Latencia Total del Camino

Latencia = C[A,B] + C[B,E] + C[E,F] = 10 + 8 + 10 = **28 milisegundos**

### 4.5 Valor de la Función Objetivo

Z = 10(40) + 8(40) + 10(40) = 400 + 320 + 400 = **1120 ms·Gbps**

---

## 5. VALIDACIÓN DE LA SOLUCIÓN

### 5.1 Conservación de Flujo ✓

| Nodo | Flujo Entrante | Flujo Saliente | Diferencia | Estado |
|------|----------------|----------------|-----------|--------|
| A | 0 | 40 | +40 | Origen ✓ |
| B | 40 | 40 | 0 | Intermedio ✓ |
| E | 40 | 40 | 0 | Intermedio ✓ |
| F | 40 | 0 | -40 | Destino ✓ |

### 5.2 Respeto de Capacidades ✓

| Enlace | Flujo (Gbps) | Capacidad (Gbps) | Cumple |
|--------|--------------|------------------|--------|
| A-B | 40 | 100 | ✓ 40 ≤ 100 |
| B-E | 40 | 120 | ✓ 40 ≤ 120 |
| E-F | 40 | 150 | ✓ 40 ≤ 150 |

**Conclusión:** La solución es **FACTIBLE y ÓPTIMA**.

---

## 6. ANÁLISIS COMPARATIVO

### Comparación con Otras Rutas

| Ruta | Latencia (ms) | Cuello Botella | Cap. Mín (Gbps) | Factible | Mejora |
|------|---------------|----------------|-----------------|----------|--------|
| **A→B→E→F** | **28** | A-B | 100 | ✓ | Base |
| A→B→D→F | 35 | B-D | 50 | ✓ | -7 ms |
| A→C→D→F | 47 | D-F | 60 | ✓ | -19 ms |
| A→C→D→E→F | 41 | A-C | 80 | ✓ | -13 ms |
| A→B→D→E→F | 29 | B-D | 50 | ✓ | -1 ms |

**Observaciones:**
- La ruta óptima tiene 28 ms
- Es 7 ms más rápida que la segunda mejor (35 ms)
- Es 19 ms más rápida que la peor (47 ms)
- Todas respetan la capacidad de 40 Gbps

---

## 7. VENTAJAS DEL MODELO

### 7.1 Automatización
✓ No requiere enumerar todas las rutas manualmente  
✓ Encuentra la mejor automáticamente  
✓ Escalable a redes con miles de nodos

### 7.2 Optimalidad Garantizada
✓ Si existe solución, es la mejor posible  
✓ No es aproximación, es exacta  
✓ Prueba matemática de optimalidad

### 7.3 Manejo de Múltiples Restricciones
✓ Simultáneamente: latencias, capacidades, flujo  
✓ Extensible a más restricciones  
✓ Decisiones globales óptimas

### 7.4 Aplicabilidad Práctica
✓ Usado en operadores de telecomunicaciones  
✓ Centros de datos  
✓ Redes de Internet (BGP routing)  
✓ Logística y transporte

---

## 8. CONCLUSIONES

### 8.1 Integración de Conceptos

Este proyecto demuestra cómo **tres áreas matemáticas** resuelven un problema real:

1. **Teoría de Grafos:** Modela la estructura de la red
2. **Álgebra Lineal:** Representa mediante matrices
3. **Programación Lineal:** Optimiza automáticamente

### 8.2 Resultado Final

- **Ruta Óptima:** A → B → E → F
- **Latencia Total:** 28 milisegundos
- **Tráfico Enrutado:** 40 Gbps
- **Estado de Restricciones:** Todas cumplidas
- **Solución:** ÓPTIMA y FACTIBLE

### 8.3 Aplicación en Ingeniería

El álgebra lineal no es solo teoría abstracta, sino una **herramienta práctica** fundamental para:
- Diseño de redes
- Optimización de recursos
- Toma de decisiones automáticas
- Escalabilidad a sistemas reales

---

## REFERENCIAS BIBLIOGRÁFICAS

1. Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009). Introduction to Algorithms (3rd ed.). MIT Press.

2. Boyd, S., & Vandenberghe, L. (2004). Convex Optimization. Cambridge University Press.

3. Bertsekas, D. P. (1998). Network Optimization: Continuous and Discrete Models. Athena Scientific.

4. Gross, J. L., & Yellen, J. (2005). Graph Theory and Its Applications (2nd ed.). Chapman and Hall/CRC.

5. Hillier, F. S., & Lieberman, G. J. (2010). Introduction to Operations Research (9th ed.). McGraw-Hill.

6. SciPy Documentation. scipy.optimize.linprog. https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.linprog.html

7. NetworkX Documentation. Network Analysis in Python. https://networkx.org/

---

**DOCUMENTO COMPLETADO**

Proyecto: Rutas Óptimas en Redes de Telecomunicaciones  
Aplicación: Programación Lineal y Álgebra Lineal  
Autor: Universidad de Medellín  
Fecha: 22 de octubre de 2025