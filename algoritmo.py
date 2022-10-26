from tablero import *
import random

# variables globales
JUGADOR_MIN = 1
JUGADOR_MAX = 2

# llama al algoritmo que decide la jugada y devuelve la posición elegida
def juega(tablero, profundidad=5, habilitarAlfaBeta=True, jugadorMax=True):
    return minimax(tablero, profundidad, habilitarAlfaBeta, jugadorMax)

# algoritmo minimax para decidir jugada óptima  
def minimax(tablero, profundidad, habilitarAlfaBeta, jugadorMax):
    posicion = [-1] * 2
    jugadorInicial = 1
    if (jugadorMax):
        jugadorInicial = 2

    # se inicializa la puntuación a valor infinito para que cualquier jugada posible sea mejor
    alfa = float("-inf")
    beta = float("inf")
 
    # genera nodos en función de las jugadas posibles
    jugadasPosibles = getJugadasPosibles(tablero)
    # se escoge jugada aleatoria para evitar una lógica predecible de la máquina
    random.shuffle(jugadasPosibles)
    for columna in jugadasPosibles:
        fila = busca(tablero, columna)
        simulacionTablero = Tablero(tablero)
        simulacionTablero.setCelda(fila, columna, jugadorInicial)
        # si gana en la primera jugada no tiene sentido continuar el algoritmo
        if (victoria(simulacionTablero, fila, columna)):
            posicion[0] = fila
            posicion[1] = columna
            return posicion

        if (jugadorMax):
            puntuacionActual = juegaMin(simulacionTablero, profundidad-1, alfa, beta, habilitarAlfaBeta)
            if (puntuacionActual > alfa):
                alfa = puntuacionActual
                posicion[0] = fila
                posicion[1] = columna
        else:
            puntuacionActual = juegaMax(simulacionTablero, profundidad-1, alfa, beta, habilitarAlfaBeta)
            if (puntuacionActual < beta):
                beta = puntuacionActual
                posicion[0] = fila
                posicion[1] = columna

    # devolverá la mejor columna para así tomar la decisión
    return posicion

# MIN será el oponente del jugador que invoque el algoritmo
def juegaMin(tablero, profundidad, alfa, beta, habilitarAlfaBeta):
    # si es un nodo terminal
    if esHoja(tablero, profundidad):
        # devuelve valor positivo para MAX
        return funcionEvaluacion(tablero)
 
    # genera nodos en función de las jugadas posibles
    jugadasPosibles = getJugadasPosibles(tablero)
    # se escoge jugada aleatoria para evitar una lógica predecible de la máquina
    random.shuffle(jugadasPosibles)
    # simula los siguientes movimientos de MIN
    for columna in range(tablero.getAncho()):
        fila = busca(tablero, columna)
        # crea una copia del tablero y coloca una ficha
        simulacionTablero = Tablero(tablero)
        simulacionTablero.setCelda(fila, columna, JUGADOR_MIN)
        if (victoria(simulacionTablero, fila, columna)):
            return -1000000
        # actualiza beta para cada nodo MAX siguiente
        beta = min(beta, juegaMax(simulacionTablero, profundidad-1, alfa, beta, habilitarAlfaBeta))
        # si se habilita la poda alfa-beta
        if (habilitarAlfaBeta == True and alfa >= beta):
            # no interesa seguir buscando porque no elegirá este nodo
            break

    return beta

# MAX será el jugador que invoque el algoritmo
def juegaMax(tablero, profundidad, alfa, beta, habilitarAlfaBeta):
    # si es un nodo terminal
    if esHoja(tablero, profundidad):
        # devuelve valor negativo para MIN
        return funcionEvaluacion(tablero)
 
    # genera nodos en función de las jugadas posibles
    jugadasPosibles = getJugadasPosibles(tablero)
    # se escoge jugada aleatoria para evitar una lógica predecible de la máquina
    random.shuffle(jugadasPosibles)
    # simula los siguientes movimientos de MAX
    for columna in range(tablero.getAncho()):
        fila = busca(tablero, columna)
        # crea una copia del tablero y coloca una ficha
        simulacionTablero = Tablero(tablero)
        simulacionTablero.setCelda(fila, columna, JUGADOR_MAX)
        if (victoria(simulacionTablero, fila, columna)):
            return 1000000
        # actualiza alfa para cada nodo MIN siguiente
        alfa = max(alfa, juegaMin(simulacionTablero, profundidad-1, alfa, beta, habilitarAlfaBeta))
        # si se habilita la poda alfa-beta
        if (habilitarAlfaBeta == True and alfa >= beta):
            # no interesa seguir buscando porque no elegirá este nodo
            break

    return alfa

# obtiene vector de jugadas posibles en función sus posiciones como columnas
def getJugadasPosibles(tablero):
    jugadasPosibles = []

    for columna in range(tablero.getAncho()):
        if (busca(tablero, columna) != -1):
            jugadasPosibles.append(columna)
    
    return jugadasPosibles

# devuelve la primera fila vacía de la columna indicada o -1 si están todas ocupadas
def busca(tablero, columna):
    # recorre filas de la columna de abajo hacia arriba
    for fila in range(tablero.getAlto()-1 , -1, -1):
        # si encuentra celda vacía
        if (tablero.getCelda(fila, columna) == 0):
            return fila   

    return -1  

# devuelve True si el jugador gana con el movimiento facilitado
# agiliza la comprobación de victoria limitando el campo de búsqueda de la combinación ganadora
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

# devuelve True si hay victoria en horizontal
def combinacionHorizontal(tablero, fila, columna):
    fichaBuscada = tablero.getCelda(fila, columna)

    # comprueba si existe combinación ganadora teniendo en cuenta los 6 espacios adyacentes
    # a la posición pasada por parámetro.
    # primero recorre hacia la derecha
    for columnaInicio in range(columna, columna + 4):
        combinadas = 0
        # límite del tablero
        if (columnaInicio < tablero.getAncho()):
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
def combinacionVertical(tablero, fila, columna):
    fichaBuscada = tablero.getCelda(fila, columna)

    # comprueba si existe combinación ganadora teniendo en cuenta los 6 espacios adyacentes
    # a la posición pasada por parámetro.
    # primero recorre hacia abajo
    for filaInicio in range(fila, fila + 4):
        combinadas = 0
        # límite del tablero
        if (filaInicio < tablero.getAlto()):
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
def combinacionDiagAsc(tablero, fila, columna):
    fichaBuscada = tablero.getCelda(fila, columna)

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
        if ((filaInicio >= 0) and (columnaActual < tablero.getAncho())):
            # después recorre hacia abajo
            for filaActual in range(filaInicio, fila+4):
                # límites del tablero
                if ((filaActual < tablero.getAlto()) and (columnaActual >= 0)):
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
def combinacionDiagDesc(tablero, fila, columna):
    fichaBuscada = tablero.getCelda(fila, columna)

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
        if ((filaInicio < tablero.getAlto()) and (columnaActual < tablero.getAncho())):
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
    for columna in range(tablero.getAncho()):
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
    for fila in range(tablero.getAlto()):
        for columna in range(3,4):
            columnasCentrales.append(tablero.getCelda(fila, columna))
    # cuenta las fichas de la lista que pertenezcan al jugador
    contadorMax = columnasCentrales.count(JUGADOR_MAX)
    contadorMin = columnasCentrales.count(JUGADOR_MIN)
    puntuacion = contadorMax - contadorMin

    return puntuacion

# puntuacion de abajo hacia arriba por columnas         
def puntuacionVertical(tablero):
    puntuacion = 0

    # primero recorre tablero hacia la derecha
    for columna in range(tablero.getAncho()):
        # segundo recorre el tablero hacia arriba.
        # se limita la altura para restringir combinaciones no válidas para ganar
        for fila in range(tablero.getAlto()-1, tablero.getAlto()-5, -1):
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
    for fila in range(tablero.getAlto()-1, 0, -1):
        # se cuentan las columnas vacías
        columnasVacias = 0
        # segundo recorre el tablero hacia la derecha.
        # se limita la anchura para restringir combinaciones no válidas para ganar
        for columna in range(tablero.getAncho() - 3):
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
        if (columnasVacias == tablero.getAncho()):
            break
            
    return puntuacion

# puntuacion diagonal de izda a dcha descendente
def puntuacionDiagDcha(tablero):
    puntuacion = 0

    # primero recorre tablero hacia abajo
    # se limita la altura para restringir combinaciones no válidas para ganar
    for fila in range(tablero.getAlto() - 3):
        # segundo recorre el tablero hacia la derecha.
        # se limita la anchura para restringir combinaciones no válidas para ganar
        for columna in range(tablero.getAncho() - 3):
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
    for fila in range(tablero.getAlto() - 3):
        # segundo recorre el tablero hacia la derecha.
        # se limita la anchura para restringir combinaciones no válidas para ganar
        for columna in range(3, tablero.getAncho()):
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
    # puntos jugador
    if (fichasMax > 0 and fichasMin == 0):
        if (fichasMax == 4):
            return 100
        elif (fichasMax == 3):
            return 10
        elif (fichasMax == 2):
            return 1
        else:
            return 0

    # puntos enemigo
    elif (fichasMin > 0 and fichasMax == 0):
        if (fichasMin == 4):
            return -100
        elif (fichasMin == 3):
            return -10
        elif (fichasMin == 2):
            return -1
        else:
            return 0

    # no puntúa     
    else:
        return 0