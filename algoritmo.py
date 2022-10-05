from tablero import *

# llama al algoritmo que decide la jugada y devuelve la posición elegida
def juega(tablero, jugador):
    profundidad = 5

    return minimax(tablero, profundidad, jugador)

# algoritmo minimax para decidir jugada óptima  
def minimax(tablero, profundidad, jugador):
    posicion = [None] * 2

    # se inicializa la puntuación a valor infinito para que cualquier jugada posible sea mejor
    alfa = float("-inf")
    beta = float("inf")
 
    # genera nodos en función de las jugadas posibles 
    for columna in range(tablero.getAncho()):        
        fila = busca(tablero, columna)
        # si hay huecos en la columna
        if fila != -1:
            simulacionTablero = Tablero(tablero)
            simulacionTablero.setCelda(fila, columna, jugador)
            puntuacionActual = juegaMin(simulacionTablero, profundidad-1, alfa, beta, fila, columna, jugador)
            if (puntuacionActual > alfa):
                alfa = puntuacionActual
                posicion[0] = fila
                posicion[1] = columna

    # devolverá la mejor columna para así tomar la decisión
    return posicion

# MIN será el oponente del jugador que invoque el algoritmo
def juegaMin(tablero, profundidad, alfa, beta, filaAnterior, columnaAnterior, jugadorEnemigo):
    # comprueba si se debe de ejecutar la función de evaluación
    resultadoHoja = esHoja(tablero, profundidad, filaAnterior, columnaAnterior)
    # evalúa la situación del nodo anterior, que es el oponente de MIN
    if (resultadoHoja > 0):
        return funcionEvaluacion(tablero, resultadoHoja, jugadorEnemigo)

    if (jugadorEnemigo == 1):
        jugador = 2
    else:
        jugador = 1

    # calcula los siguientes movimientos de MIN
    for columna in range(tablero.getAncho()):
        fila = busca(tablero, columna)
        # si hay huecos en la columna
        if (fila != -1):
            simulacionTablero = Tablero(tablero)
            simulacionTablero.setCelda(fila, columna, jugador)
            # actualiza beta para cada nodo MAX siguiente
            beta = min(beta, juegaMax(simulacionTablero, profundidad-1, alfa, beta, fila, columna, jugador))
            # no interesa seguir buscando porque no elegirá este nodo
            if (alfa >= beta):
                break

    return beta

# MAX será el jugador que invoque el algoritmo
def juegaMax(tablero, profundidad, alfa, beta, filaAnterior, columnaAnterior, jugadorEnemigo):
    # comprueba si se debe de ejecutar la función de evaluación
    resultadoHoja = esHoja(tablero, profundidad, filaAnterior, columnaAnterior)
    if (resultadoHoja > 0):
        return -funcionEvaluacion(tablero, resultadoHoja, jugadorEnemigo)

    if (jugadorEnemigo == 1):
        jugador = 2
    else:
        jugador = 1

    for columna in range(tablero.getAncho()):
        fila = busca(tablero, columna)
        if (fila != -1):
            simulacionTablero = Tablero(tablero)
            simulacionTablero.setCelda(fila, columna, jugador)
            # actualiza alfa para cada nodo MIN siguiente
            alfa = max(alfa, juegaMin(simulacionTablero, profundidad-1, alfa, beta, fila, columna, jugador))
            # no interesa seguir buscando porque no elegirá este nodo
            if (alfa >= beta):
                break

    return alfa

# devuelve la primer fila vacía de la columna indicada o -1 si están todas ocupadas
def busca(tablero, columna):
    ultimaFila = tablero.getAlto() - 1

    # recorre filas de la columna de arriba a abajo
    for fila in range(tablero.getAlto()):
        # si encuentra celda ocupada
        if (tablero.getCelda(fila, columna) != 0):
            fila -= 1
            return fila   

    return ultimaFila   

# indica si es un nodo hoja por llegar al límite de profundidad o no quedan movimientos posibles
def esHoja(tablero, profundidad, fila, columna):
    if victoria(tablero, fila, columna):
        return 1
    elif (not jugadaPosible(tablero)):
        return 2
    elif (profundidad == 0):
        return 3
    else:
        return -1

# devuelve número de columnas disponibles para la siguiente jugada
def jugadaPosible(tablero):    
    for columna in range(tablero.getAncho()):
        if (busca(tablero, columna) != -1):
            return True

    return False

# devuelve un jugador si ha ganado o 0 si no
def victoria(tablero, fila, columna):
    if (combinacionHorizontal(tablero, fila, columna)):
        return True
    else:
        if (combinacionVertical(tablero, fila, columna)):
            return True
        else:
            if (combinacionDiagAsc(tablero, fila, columna)):
                return True
            else:
                if (combinacionDiagDesc(tablero, fila, columna)):
                    return True
    return False

# devuelve true si hay victoria en horizontal
def combinacionHorizontal(tablero, fila, columna):
    fichaBuscada = tablero.getCelda(fila, columna)

    for columnaInicio in range(columna, columna + 4):
        combinadas = 0
        if (columnaInicio < tablero.getAncho()):
            for columnaActual in range(columnaInicio, columna - 4, -1):
                if (columnaActual >= 0):
                    fichaActual = tablero.getCelda(fila, columnaActual)
                    if (fichaActual == fichaBuscada):
                        combinadas += 1
                    else:
                        break

                    if (combinadas == 4):
                        return True

    return False
   
# devuelve true si hay victoria en vertical 
def combinacionVertical(tablero, fila, columna):
    fichaBuscada = tablero.getCelda(fila, columna)

    for filaInicio in range(fila, fila + 4):
        combinadas = 0
        if (filaInicio < tablero.getAlto()):
            for filaActual in range(filaInicio, fila - 4, -1):
                if (filaActual >= 0):
                    fichaActual = tablero.getCelda(filaActual, columna)
                    if (fichaActual == fichaBuscada):
                        combinadas += 1
                    else:
                        break

                    if (combinadas == 4):
                        return True
                        
    return False
  
# devuelve true si hay victoria en diagonal ascendente
def combinacionDiagAsc(tablero, fila, columna):
    fichaBuscada = tablero.getCelda(fila, columna)

    i = 0
    for filaInicio in range(fila, fila-4, -1):
        combinadas = 0
        columnaActual = columna + i
        if ((filaInicio >= 0) and (columnaActual < tablero.getAncho())):
            for filaActual in range(filaInicio, fila+4):
                if ((filaActual < tablero.getAlto()) and (columnaActual >= 0)):
                    fichaActual = tablero.getCelda(filaActual, columnaActual)
                    if (fichaActual == fichaBuscada):
                        combinadas += 1
                    else:
                        break

                    if (combinadas == 4):
                        return True
                    columnaActual -= 1
            i += 1
                        
    return False

# devuelve true si hay victoria en diagonal descendente
def combinacionDiagDesc(tablero, fila, columna):
    fichaBuscada = tablero.getCelda(fila, columna)

    i = 0
    for filaInicio in range(fila, fila+4):
        combinadas = 0
        columnaActual = columna + i
        if ((filaInicio < tablero.getAlto()) and (columnaActual < tablero.getAncho())):
            for filaActual in range(filaInicio, fila-4, -1):
                if ((filaActual >= 0) and (columnaActual >= 0)):
                    fichaActual = tablero.getCelda(filaActual, columnaActual)
                    if (fichaActual == fichaBuscada):
                        combinadas += 1
                    else:
                        break

                    if (combinadas == 4):
                        return True
                    columnaActual -= 1
        i += 1
                        
    return False

def funcionEvaluacion(tablero, resultadoHoja, jugador):
    # gana jugador
    if (resultadoHoja == 1):
        return 100000
    # empate
    elif (resultadoHoja == 2):
        return 0
    # límite profundidad
    elif (resultadoHoja == 3):
        return evaluarSituacion(tablero, jugador)

# evalúa la situación global de ambos jugadores y devuelve una puntuación
def evaluarSituacion(tablero, jugador):
    puntuacion = puntuacionVertical(tablero, jugador)
    puntuacion += puntuacionHorizontal(tablero, jugador)
    puntuacion += puntuacionDiagDcha(tablero, jugador)
    puntuacion += puntuacionDiagIzda(tablero, jugador)

    return puntuacion

# puntuacion de abajo hacia arriba por columnas         
def puntuacionVertical(tablero, jugador):
    puntuacion = 0

    for columna in range(tablero.getAncho()):
        for fila in range(tablero.getAlto()-3):
            # si encuentra una celda vacía no tiene sentido seguir buscando arriba
            if (tablero.estaVacia(fila, columna)):
                break            
            vacias = 0
            enemigas = 0
            aliadas = 0
            for filaActual in range(fila, fila + 4):
                ficha = tablero.getCelda(filaActual, columna)
                if (ficha == 0):
                    vacias += 1
                elif (ficha == jugador):
                    aliadas += 1
                else:
                    enemigas += 1
            puntuacion += sumarPuntos(vacias, aliadas, enemigas)
            
    return puntuacion

# puntuacion de izda a dcha por filas
def puntuacionHorizontal(tablero, jugador):
    puntuacion = 0

    for fila in range(tablero.getAlto()-1, 0, -1):
        columnasVacias = 0
        for columna in range(tablero.getAncho() - 3):
            vacias = 0
            enemigas = 0
            aliadas = 0
            for columnaActual in range(columna, columna + 4):
                ficha = tablero.getCelda(fila, columnaActual)
                if (ficha == 0):
                    vacias += 1
                elif (ficha == jugador):
                    aliadas += 1
                else:
                    enemigas += 1
            puntuacion += sumarPuntos(vacias, aliadas, enemigas)

            if (tablero.getCelda(fila, columna) == 0):
                columnasVacias += 1
        # si una fila completa está vacía no tiene sentido seguir buscando por encima
        if (vacias == tablero.getAncho()):
            break
            
    return puntuacion

# puntuacion diagonal de izda a dcha descendente
def puntuacionDiagDcha(tablero, jugador):
    puntuacion = 0

    for fila in range(tablero.getAlto() - 3):
        for columna in range(tablero.getAncho() - 3):
            vacias = 0
            enemigas = 0
            aliadas = 0
            for posicion in range(4):
                ficha = tablero.getCelda(fila + posicion, columna + posicion)
                if (ficha == 0):
                    vacias += 1
                elif (ficha == jugador):
                    enemigas += 1
                else:
                    aliadas += 1
            puntuacion += sumarPuntos(vacias, aliadas, enemigas)

    return puntuacion

# puntuacion diagonal de dcha a izda descendente
def puntuacionDiagIzda(tablero, jugador):
    puntuacion = 0

    for fila in range(tablero.getAlto() - 3):
        for columna in range(3, tablero.getAncho()):
            vacias = 0
            enemigas = 0
            aliadas = 0
            for posicion in range(4):
                ficha = tablero.getCelda(fila + posicion, columna - posicion)
                if (ficha == 0):
                    vacias += 1
                elif (ficha == jugador):
                    aliadas += 1
                else:
                    enemigas += 1
            puntuacion += sumarPuntos(vacias, aliadas, enemigas)

    return puntuacion

# suma puntos de las fichas en función del jugador
def sumarPuntos(vacias, aliadas, enemigas):
    # puntos enemigo
    if (enemigas > 0 and aliadas == 0):
        if (enemigas == 3 and vacias == 1):
            return -1000
        elif (enemigas == 2 and vacias == 2):
            return -7
        elif (enemigas == 1 and vacias == 3):
            return -3
    
    # puntos jugador
    elif (aliadas > 0 and enemigas == 0):
        if (aliadas == 3 and vacias == 1):
            return 7
        elif (aliadas == 2 and vacias == 2):
            return 3
        elif (aliadas == 1 and vacias == 3):
            return 1

    else:
        return 0