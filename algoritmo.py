from tablero import *
import random

# variables globales
JUGADOR_MIN = 1
JUGADOR_MAX = 2
TOTAL_FILAS = 7
TOTAL_COLUMNAS = 8

# llama al algoritmo que decide la jugada y devuelve la posición elegida
def juega(tablero, profundidad=6, habilitarAlfaBeta=True, jugadorMax=True):
    global TOTAL_FILAS, TOTAL_COLUMNAS
    TOTAL_FILAS = tablero.getAlto()
    TOTAL_COLUMNAS = tablero.getAncho()
    posicion = [-1] * 2

    # se inicializa la puntuación a valor infinito para que cualquier jugada posible sea mejor
    alfa = float("-inf")
    beta = float("inf")

    columna = minimax(tablero, profundidad, alfa, beta, habilitarAlfaBeta, jugadorMax)[0]
    fila = busca(tablero, columna)
    posicion[0] = fila
    posicion[1] = columna

    return posicion

# algoritmo minimax para decidir jugada óptima  
def minimax(tablero, profundidad, alfa, beta, habilitarAlfaBeta, jugadorMax):
    # si es un nodo terminal
    if esHoja(tablero, profundidad):
        # devuelve el valor de la función de evaluación
        return -1, funcionEvaluacion(tablero)
    
    mejorColumna = 0
    # necesario almacenar la puntuación para que sea independiente al turno de MIN o MAX
    if (jugadorMax):
        mejorPuntuacion = float("-inf")
    else:
        mejorPuntuacion = float("inf")
    # genera nodos en función de las jugadas posibles
    jugadasPosibles = getJugadasPosibles(tablero)
    # se escoge jugada aleatoria para evitar una lógica predecible de la máquina
    random.shuffle(jugadasPosibles)
    # simula los siguientes movimientos
    for columna in jugadasPosibles:
        fila = busca(tablero, columna)
        # crea una copia del tablero
        simulacionTablero = Tablero(tablero)
        # turno de MAX
        if (jugadorMax):
            #  coloca una ficha
            simulacionTablero.setCelda(fila, columna, JUGADOR_MAX)
            # si el jugador gana con la última jugada
            if (victoria(simulacionTablero, fila, columna)):
                # devuelve la columna por si ocurre en el primer nivel del árbol
                return columna, 1000000 * profundidad
            # actualiza alfa para cada nodo MIN siguiente
            alfa = max(alfa, minimax(simulacionTablero, profundidad-1, alfa, beta, habilitarAlfaBeta, False)[1])
            # almacena la mejor puntuación y columna de este turno
            if alfa > mejorPuntuacion:
                mejorPuntuacion = alfa
                mejorColumna = columna
            # si se habilita la poda alfa-beta
            if (habilitarAlfaBeta == True and alfa >= beta):
                # no interesa seguir buscando porque no elegirá este nodo
                break

        # turno de MIN
        else:
            # coloca una ficha
            simulacionTablero.setCelda(fila, columna, JUGADOR_MIN)
            # si el jugador gana con la última jugada
            if (victoria(simulacionTablero, fila, columna)):
                # devuelve la columna por si ocurre en el primer nivel del árbol
                return columna, -1000000 * profundidad
            # actualiza beta para cada nodo MAX siguiente
            beta = min(beta, minimax(simulacionTablero, profundidad-1, alfa, beta, habilitarAlfaBeta, True)[1])
            # almacena la mejor puntuación y columna de este turno
            if beta < mejorPuntuacion:
                mejorPuntuacion = beta
                mejorColumna = columna
            # si se habilita la poda alfa-beta
            if (habilitarAlfaBeta == True and alfa >= beta):
                # no interesa seguir buscando porque no elegirá este nodo
                break

    # devolverá la mejor columna al nodo raíz y la mejor puntuación de cada nodo en recursión
    return mejorColumna, mejorPuntuacion

# obtiene lista de jugadas posibles en función sus posiciones como columnas
def getJugadasPosibles(tablero):
    jugadasPosibles = []

    for columna in range(TOTAL_COLUMNAS):
        if (busca(tablero, columna) != -1):
            jugadasPosibles.append(columna)
    
    return jugadasPosibles

# devuelve la primera fila vacía de la columna indicada o -1 si están todas ocupadas
def busca(tablero, columna):
    # recorre filas de la columna de abajo hacia arriba
    for fila in range(TOTAL_FILAS-1 , -1, -1):
        # si encuentra celda vacía
        if (tablero.getCelda(fila, columna) == 0):
            return fila   

    return -1  

# devuelve True si el jugador gana con el movimiento facilitado
# agiliza la comprobación de victoria limitando el campo de búsqueda de la combinación ganadora
def victoria(tablero, fila, columna):
    fichaBuscada = tablero.getCelda(fila, columna)

    if (combinacionHorizontal(tablero, fila, columna, fichaBuscada)):
        return True
    else:
        if (combinacionVertical(tablero, fila, columna, fichaBuscada)):
            return True
        else:
            if (combinacionDiagAsc(tablero, fila, columna, fichaBuscada)):
                return True
            else:
                if (combinacionDiagDesc(tablero, fila, columna, fichaBuscada)):
                    return True
    return False

# devuelve True si hay victoria en horizontal
def combinacionHorizontal(tablero, fila, columna, fichaBuscada):
    # comprueba si existe combinación ganadora teniendo en cuenta los 6 espacios adyacentes
    # a la posición pasada por parámetro.
    # primero recorre hacia la derecha
    for columnaInicio in range(columna, columna + 4):
        combinadas = 0
        # límite del tablero
        if (columnaInicio < TOTAL_COLUMNAS):
            # después recorre hacia la izquierda
            for columnaActual in range(columnaInicio, columna - 4, -1):
                # límite del tablero
                if (columnaActual >= 0):
                    fichaActual = tablero.getCelda(fila, columnaActual)
                    if (fichaActual == fichaBuscada):
                        combinadas += 1
                    # se rompe la secuencia. Vuelve al primer bucle
                    else:
                        break

                    # combinación ganadora
                    if (combinadas == 4):
                        return True
                # no tiene sentido seguir sobrepasando el límite
                else:
                    break
        # no tiene sentido seguir sobrepasando el límite
        else:
            return False

    return False
   
# devuelve True si hay victoria en vertical 
def combinacionVertical(tablero, fila, columna, fichaBuscada):
    # comprueba si existe combinación ganadora teniendo en cuenta los 6 espacios adyacentes
    # a la posición pasada por parámetro.
    # primero recorre hacia abajo
    for filaInicio in range(fila, fila + 4):
        combinadas = 0
        # límite del tablero
        if (filaInicio < TOTAL_FILAS):
            # después recorre hacia arriba
            for filaActual in range(filaInicio, fila - 4, -1):
                # límite del tablero
                if (filaActual >= 0):
                    fichaActual = tablero.getCelda(filaActual, columna)
                    if (fichaActual == fichaBuscada):
                        combinadas += 1
                    # se rompe la secuencia. Vuelve al primer bucle
                    else:
                        break

                    # combinación ganadora
                    if (combinadas == 4):
                        return True
                # no tiene sentido seguir sobrepasando el límite
                else:
                    break
        # no tiene sentido seguir sobrepasando el límite
        else:
            return False
                        
    return False
  
# devuelve True si hay victoria en diagonal ascendente
def combinacionDiagAsc(tablero, fila, columna, fichaBuscada):
    # iterador de la columna inicial
    i = 0
    # comprueba si existe combinación ganadora teniendo en cuenta los 6 espacios en diagonal
    # con pendiente ascendiente a la posición pasada por parámetro.
    # primero recorre hacia arriba
    for filaInicio in range(fila, fila-4, -1):
        combinadas = 0
        # sigue el traslado de la fila hacia la derecha
        columnaActual = columna + i
        # límites del tablero
        if ((filaInicio >= 0) and (columnaActual < TOTAL_COLUMNAS)):
            # después recorre hacia abajo
            for filaActual in range(filaInicio, fila+4):
                # límites del tablero
                if ((filaActual < TOTAL_FILAS) and (columnaActual >= 0)):
                    fichaActual = tablero.getCelda(filaActual, columnaActual)
                    if (fichaActual == fichaBuscada):
                        combinadas += 1
                    else:
                        break

                    # combinación ganadora
                    if (combinadas == 4):
                        return True
                    # sigue el traslado de la fila hacia la izquierda
                    columnaActual -= 1
                # no tiene sentido seguir sobrepasando el límite
                else:
                    break
            i += 1
        # no tiene sentido seguir sobrepasando el límite
        else:
            return False

                        
    return False

# devuelve True si hay victoria en diagonal descendente
def combinacionDiagDesc(tablero, fila, columna, fichaBuscada):
    # iterador de la columna inicial
    i = 0
    # comprueba si existe combinación ganadora teniendo en cuenta los 6 espacios en diagonal
    # con pendiente descendiente a la posición pasada por parámetro.
    # primero recorre hacia abajo
    for filaInicio in range(fila, fila+4):
        combinadas = 0
        # sigue el traslado de la fila hacia la derecha
        columnaActual = columna + i
        # límites del tablero
        if ((filaInicio < TOTAL_FILAS) and (columnaActual < TOTAL_COLUMNAS)):
            # después recorre hacia arriba
            for filaActual in range(filaInicio, fila-4, -1):
                # límites del tablero
                if ((filaActual >= 0) and (columnaActual >= 0)):
                    fichaActual = tablero.getCelda(filaActual, columnaActual)
                    if (fichaActual == fichaBuscada):
                        combinadas += 1
                    else:
                        break

                    # combinación ganadora
                    if (combinadas == 4):
                        return True
                    # sigue el traslado de la fila hacia la izquierda
                    columnaActual -= 1
                # no tiene sentido seguir sobrepasando el límite
                else:
                    break
            i += 1
        # no tiene sentido seguir sobrepasando el límite
        else:
            return False
                        
    return False

# indica si es un nodo hoja por finalizar la partida o alcanzar máximo de profundidad
def esHoja(tablero, profundidad):
    # alcanzado máximo de profundidad o empate
    if ((profundidad == 0) or (not jugadaPosible(tablero))):
        return True
    else:
        return False

# devuelve True si aún quedan espacios libres
def jugadaPosible(tablero):    
    for columna in range(TOTAL_COLUMNAS):
        if (busca(tablero, columna) != -1):
            return True

    return False

# evalúa la situación global de ambos jugadores y devuelve una puntuación
def funcionEvaluacion(tablero):
    puntuacion = puntuacionCentral(tablero)
    puntuacion += puntuacionVertical(tablero)
    puntuacion += puntuacionHorizontal(tablero)
    puntuacion += puntuacionDiagDcha(tablero)
    puntuacion += puntuacionDiagIzda(tablero)

    return puntuacion

# puntuación prioritaria de las columnas centrales
def puntuacionCentral(tablero):
    columnasCentrales = []

	# almacena las fichas de las columnas en una lista
    for fila in range(TOTAL_FILAS):
        for columna in range(3,5):
            columnasCentrales.append(tablero.getCelda(fila, columna))
    # cuenta las fichas de la lista que pertenezcan al jugador
    contadorMax = columnasCentrales.count(JUGADOR_MAX)
    contadorMin = columnasCentrales.count(JUGADOR_MIN)
    puntuacion = (contadorMax - contadorMin)

    return puntuacion

# puntuacion de abajo hacia arriba por columnas         
def puntuacionVertical(tablero):
    puntuacion = 0

    # primero recorre tablero hacia la derecha
    for columna in range(TOTAL_COLUMNAS):
        # segundo recorre el tablero hacia arriba.
        # se limita la altura para restringir combinaciones no válidas para ganar
        for fila in range(TOTAL_FILAS-1, TOTAL_FILAS-5, -1):
            # si encuentra una celda vacía no tiene sentido seguir buscando arriba
            if (tablero.estaVacia(fila, columna)):
                break
            fichasMin = 0
            fichasMax = 0
            # vuelve a recorrer 3 posiciones hacia arriba para completar secuencia
            for filaActual in range(fila, fila-4, -1):
                ficha = tablero.getCelda(filaActual, columna)
                if (ficha == JUGADOR_MAX):
                    fichasMax += 1
                elif (ficha == JUGADOR_MIN):
                    fichasMin += 1
            # valora la secuencia de fichas observadas
            puntuacion += sumarPuntos(fichasMax, fichasMin)
            
    return puntuacion

# puntuacion de izda a dcha por filas
def puntuacionHorizontal(tablero):
    puntuacion = 0

    # primero recorre tablero hacia abajo
    for fila in range(TOTAL_FILAS-1, 0, -1):
        # se cuentan las columnas vacías
        columnasVacias = 0
        # segundo recorre el tablero hacia la derecha.
        # se limita la anchura para restringir combinaciones no válidas para ganar
        for columna in range(TOTAL_COLUMNAS - 3):
            fichasMin = 0
            fichasMax = 0
            # vuelve a recorrer 3 posiciones hacia la derecha para completar secuencia
            for columnaActual in range(columna, columna + 4):
                ficha = tablero.getCelda(fila, columnaActual)
                if (ficha == JUGADOR_MAX):
                    fichasMax += 1
                elif (ficha == JUGADOR_MIN):
                    fichasMin += 1
            # valora la secuencia de fichas observadas
            puntuacion += sumarPuntos(fichasMax, fichasMin)

            if (tablero.getCelda(fila, columna) == 0):
                columnasVacias += 1
        # si una fila completa está vacía no tiene sentido seguir buscando por encima
        if (columnasVacias == TOTAL_COLUMNAS):
            break
            
    return puntuacion

# puntuacion diagonal de izda a dcha descendente
def puntuacionDiagDcha(tablero):
    puntuacion = 0

    # primero recorre tablero hacia abajo
    # se limita la altura para restringir combinaciones no válidas para ganar
    for fila in range(TOTAL_FILAS - 3):
        # segundo recorre el tablero hacia la derecha.
        # se limita la anchura para restringir combinaciones no válidas para ganar
        for columna in range(TOTAL_COLUMNAS - 3):
            fichasMin = 0
            fichasMax = 0
            # vuelve a recorrer 3 posiciones hacia abajo y a la derecha para completar secuencia
            for posicion in range(4):
                ficha = tablero.getCelda(fila + posicion, columna + posicion)
                if (ficha == JUGADOR_MAX):
                    fichasMax += 1
                elif (ficha == JUGADOR_MIN):
                    fichasMin += 1
            # valora la secuencia de fichas observadas
            puntuacion += sumarPuntos(fichasMax, fichasMin)

    return puntuacion

# puntuacion diagonal de dcha a izda descendente
def puntuacionDiagIzda(tablero):
    puntuacion = 0

    # primero recorre tablero hacia abajo
    for fila in range(TOTAL_FILAS - 3):
        # segundo recorre el tablero hacia la derecha.
        # se limita la anchura para restringir combinaciones no válidas para ganar
        for columna in range(3, TOTAL_COLUMNAS):
            fichasMin = 0
            fichasMax = 0
            # vuelve a recorrer 3 posiciones hacia abajo y a la izquierda para completar secuencia
            for posicion in range(4):
                ficha = tablero.getCelda(fila + posicion, columna - posicion)
                if (ficha == JUGADOR_MAX):
                    fichasMax += 1
                elif (ficha == JUGADOR_MIN):
                    fichasMin += 1
            # valora la secuencia de fichas observadas
            puntuacion += sumarPuntos(fichasMax, fichasMin)

    return puntuacion

# suma puntos de las fichas en función de su combinación
def sumarPuntos(fichasMax, fichasMin):
    # puntos MAX
    if (fichasMax > 0 and fichasMin == 0):
        if (fichasMax == 3):
            return 100
        elif (fichasMax == 2):
            return 10
        else:
            return 1

    # puntos MIN
    elif (fichasMin > 0 and fichasMax == 0):
        if (fichasMin == 3):
            return -100
        elif (fichasMin == 2):
            return -10
        else:
            return -1

    # no puntúa     
    else:
        return 0