from tablero import *

# indica si es un nodo hoja por llegar al último nivel del árbol, alguien gana o no quedan movimientos
def finArbol(tablero, profundidad):
    if (profundidad == 0 or posiblesMovimientos(tablero) == 0):
        return True
    return False

# devuelve la primer fila vacía de la columna indicada o -1 si están todas ocupadas
def busca(tablero, col):
    i = 0
    # recorre filas de la columna
    while i < tablero.getAlto():
        # si encuentra celda vacía
        if (tablero.getCelda(i, col) == 0):
            return i
        i += 1
   
   # si no encuentra hueco vacío
    return -1

# devuelve número de columnas disponibles para la siguiente jugada
def posiblesMovimientos(tablero):
    opciones = 0
    
    for columna in range(tablero.getAncho()):
        if (busca(tablero, columna) != -1):
            opciones += 1
    return opciones

# llama al algoritmo que decide la jugada
def juega(tablero):
    profundidad = 5
    posicion = minimax(tablero, profundidad, False, 0)
    return posicion
    
def minimax(tablero, profundidad, jugador, puntuacionMejor):
    # f(N): función de evaluación.
    # N: estado.
    # B: factor de ramificación.
    # profunidad: tiene que ser impar para mantener orden de jugadores
    
    posicion = [0][0]
    fin = finArbol(tablero, profundidad)
    ganador = tablero.cuatroEnRaya()
    
    if (fin or ganador != 0):
        if (ganador == 1):
            puntuacionMejor = -float("inf")
        elif (ganador == 2):
            puntuacionMejor = float("inf")
        return None, puntuacionMejor            
            
    for columna in range(tablero.getAncho()):
        fila = busca(tablero, columna)
        if fila != -1:
            simulacionTablero = Tablero(tablero)
            if (jugador):
                simulacionTablero.setCelda(fila, columna, 1)
                puntuacionMejor = float("inf")
                puntuacionActual = minimax(simulacionTablero, profundidad-1, False, puntuacionMejor)[1]
                if (puntuacionActual < puntuacionMejor):
                    puntuacionMejor = puntuacionActual
            else:
                simulacionTablero.setCelda(fila, columna, 2)
                puntuacionMejor = -float("inf")
                puntuacionActual = minimax(simulacionTablero, profundidad-1, True, puntuacionMejor)[1]
                if (puntuacionActual > puntuacionMejor):
                    puntuacionMejor = puntuacionActual
            posicion[0] = columna
            posicion[1] = fila
    return posicion, puntuacionMejor