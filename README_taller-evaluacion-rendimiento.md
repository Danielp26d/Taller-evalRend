# Taller de Evaluación de Rendimiento

**Pontificia Universidad Javeriana — Facultad de Ingeniería**  
**Departamento de Ingeniería de Sistemas**  
**Asignatura:** Sistemas Operativos  
**Período:** Febrero – Abril 2026  

**Integrantes:**
- Daniel Prieto
- Esteban Cantillo
- Jorge Simental
- Alejandro Macías

---

## ¿De qué trata esto?

Para este taller nos pidieron comparar cuatro formas distintas de hacer multiplicación de matrices en C, variando tanto el algoritmo como el mecanismo de concurrencia. La idea es medir cuál combinación es más rápida dependiendo del tamaño de la matriz y la cantidad de hilos o procesos.

Las cuatro implementaciones son:

| Ejecutable     | Algoritmo         | Concurrencia  |
|----------------|-------------------|---------------|
| `mxmForkFxC`   | Clásico (FxC)     | `fork()`      |
| `mxmForkFxT`   | Transpuesta (FxT) | `fork()`      |
| `mxmPosixFxC`  | Clásico (FxC)     | `pthreads`    |
| `mxmPosixFxT`  | Transpuesta (FxT) | `pthreads`    |

- **FxC (Fila × Columna):** accede a la matriz B por columnas, lo cual no aprovecha bien el caché.
- **FxT (Fila × Transpuesta):** calcula la transpuesta de B primero y luego multiplica fila × fila, lo que mejora la localidad de referencia y en teoría debería ser más rápido.

Cada configuración se ejecutó **30 veces** para sacar un promedio confiable (Ley de los Grandes Números). La métrica que usamos es el tiempo de ejecución en microsegundos (µs), medido con `gettimeofday()`.

---

## Estructura del repositorio

```
taller-evaluacion-rendimiento/
├── src/
│   ├── moduloMM.h          # Cabecera con los prototipos del módulo de matrices
│   ├── moduloMM.c          # Implementación de iniMatrix, InicioMuestra, FinMuestra,
│   │                       #   impMatrix, matrixTRP, mxmForkFxC, mxmForkFxT
│   ├── mxmForkFxC.c        # Multiplicación clásica usando fork
│   ├── mxmForkFxT.c        # Multiplicación por transpuesta usando fork
│   ├── mxmPosixFxC.c       # Multiplicación clásica con hilos POSIX
│   └── mxmPosixFxT.c       # Multiplicación por transpuesta con hilos POSIX
├── bin/                    # Acá quedan los binarios después de compilar
│   ├── mxmForkFxC
│   ├── mxmForkFxT
│   ├── mxmPosixFxC
│   └── mxmPosixFxT
├── Soluciones/             # Archivos .dat con los tiempos de cada ejecución
│   └── <ejecutable>-<N>-Hilos-<h>.dat
├── docs/
│   └── Informe_EvaluacionRendimiento.docx   # Informe final del taller
├── Makefile                # Compila todo con GCC -O3 -lm -lpthread
├── lanzador.pl             # Script en Perl que automatiza las 30 repeticiones
├── calcularProm.py         # Calcula promedios y genera el Excel de resultados
├── promedios.xlsx          # Resultados consolidados (lo genera calcularProm.py)
└── README.md
```

---

## Máquinas usadas para las pruebas

Cada integrante corrió los experimentos en su propia VM Linux. Las tres máquinas que usamos fueron:

| Máquina             | CPU                               | CPUs lógicos | RAM    |
|---------------------|-----------------------------------|:------------:|--------|
| MasterJohn (Jorge)  | Intel Xeon E5-2650 v4 @ 2.20 GHz | 4            | 11 GiB |
| MIGV16 (Esteban)    | Intel Xeon Gold 6348 @ 2.60 GHz  | 6            | 15 GiB |
| MIG237 (Alejandro)  | Intel Xeon Gold 6348 @ 2.60 GHz  | 4            | 11 GiB |

Todas corrían Ubuntu 22.04.1 LTS. Tuvimos una cuarta máquina pero la descartamos porque tenía las mismas specs que MasterJohn y MIG237, así que no aportaba nada nuevo al análisis.

---

## Diseño del experimento

Los tamaños de matriz los escogimos para que cubran diferentes niveles de la jerarquía de memoria, desde L2 hasta presionar la RAM.

- **Máquinas de 4 CPUs → tamaños:** 100, 200, 400, 800 | **hilos:** 1, 2, 3, 4
- **Máquina de 6 CPUs → tamaños:** 120, 240, 480, 960 | **hilos:** 1, 2, 3, 6
- **Repeticiones por configuración:** 30
- **Total de ejecuciones por máquina:** 1,920

---

## Cómo compilar

```bash
make
```

Compila los cuatro ejecutables. Los de pthreads usan `-lpthread`, los de fork no. Con `-O3` el compilador aplica optimización máxima. Los binarios quedan en `bin/`.

```bash
make clean   # Borra los binarios
```

---

## Cómo ejecutar

### Un ejecutable a mano

```bash
./bin/mxmPosixFxC <tamaño_matriz> <num_hilos>
# Ejemplo:
./bin/mxmPosixFxC 400 4
```

### Batería completa automática

```bash
perl lanzador.pl
```

El script recorre todas las combinaciones posibles y va guardando los tiempos en `Soluciones/<ejecutable>-<N>-Hilos-<h>.dat`, cada uno con 30 líneas.

### Calcular promedios

```bash
pip install pandas openpyxl
python3 calcularProm.py
```

Genera `promedios.xlsx` con la media y la desviación estándar de cada configuración.

---

## Métricas que usamos

| Métrica        | Qué mide |
|----------------|----------|
| Tiempo (µs)    | Tiempo total de ejecución medido con `gettimeofday()`. Es la métrica principal. |
| Speedup (S)    | S = T(1) / T(n). Qué tan más rápido es con n hilos vs. en serie. |
| Eficiencia (E) | E = S / n. Qué tan bien aprovechamos los recursos disponibles. |

---

## Dependencias

| Herramienta | Versión |
|-------------|---------|
| GCC         | 9.x o superior |
| Perl        | 5.x |
| Python      | 3.8+ |
| pandas      | 1.x+ |
| openpyxl    | 3.x+ |

---

## Referencias

- Stevens, W. R., & Rago, S. A. (2013). *Advanced Programming in the UNIX Environment* (3rd ed.). Addison-Wesley.
- Butenhof, D. R. (1997). *Programming with POSIX Threads*. Addison-Wesley.
- Notas de clase: Sistemas Operativos 2026-10. Pontificia Universidad Javeriana.
