from tablero import *

# llama al algoritmo que decide la jugada y devuelve la posición elegida
def juega(tablero):
    profundidad = 6
    mejorColumna = minimax(tablero, profundidad, float("-inf"), float("inf"), False, None, None)[1]      
    fila = busca(tablero, mejorColumna) 

    return fila, mejorColumna

# algoritmo minimax para decidir jugada óptima  
def minimax(tablero, profundidad, alfa, beta, jugador, filaAnterior, columnaAnterior):
    fin = finArbol(tablero, profundidad)
    ganador = jugadaGanadora(tablero, filaAnterior, columnaAnterior)
    mejorColumna = 0
    
    # gana alguien, empate o límite de  profunidad
    if (fin or ganador != 0):
        # gana jugador
        if (ganador == 1):
            # si devuelve -infinito no podrá elegir entre dos jugadas que conduzcan a la derrota
            puntuacionMejor = -100000000
        # gana máquina
        elif (ganador == 2):
            puntuacionMejor = 100000000
        # límite profundidad
        elif (profundidad == 0):
            puntuacionMejor = evaluarSituacion(tablero, jugador)
        # empate
        else:
            puntuacionMejor = 0

        # solo devuelve puntuación porque solo importa la posición elegida por la raíz
        return puntuacionMejor, None

    # se inicializa la puntuación a valor infinito para que cualquier jugada posible sea mejor
    if (jugador):
        puntuacionMejor = float("inf")
    else:
        puntuacionMejor = -float("inf")

    # genera nodos en función de las jugadas posibles  
    for columna in range(tablero.getAncho()):        
        fila = busca(tablero, columna)
        # si hay huecos en la columna
        if fila != -1:
            # genera copia del tablero para simular las jugadas
            simulacionTablero = Tablero(tablero)

            # juega jugador MIN
            if (jugador):
                puntuacionActual = float("inf")
                if (alfa < beta):
                    simulacionTablero.setCelda(fila, columna, 1)
                    # recibe la menor puntuación de las siguientes jugadas
                    puntuacionActual = minimax(simulacionTablero, profundidad-1, alfa, beta, False, fila, columna)[0]
                    # si la puntuación es menor que las anteriores se guarda junto a la columna
                    if (puntuacionActual < puntuacionMejor):
                        puntuacionMejor = puntuacionActual
                        mejorColumna = columna
                if (puntuacionActual < beta):
                    beta = puntuacionActual

            # juega máquina MAX
            else:
                puntuacionActual = float("-inf")
                if (alfa < beta):
                    simulacionTablero.setCelda(fila, columna, 2)
                    # recibe la mayor puntuación de las siguientes jugadas
                    puntuacionActual = minimax(simulacionTablero, profundidad-1, alfa, beta, True, fila, columna)[0]
                    # si la puntuación es mayor que las anteriores se guarda junto a la columna
                    if (puntuacionActual > puntuacionMejor):
                        puntuacionMejor = puntuacionActual
                        mejorColumna = columna
                    if (puntuacionActual > alfa):
                        alfa = puntuacionActual

    # devolverá la puntuación a nodos hijos para recordar la rama que les beneficie y la mejor columna a la raíz para así tomar la decisión
    return puntuacionMejor, mejorColumna

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
def finArbol(tablero, profundidad):
    if (profundidad == 0 or not jugadaPosible(tablero)):
        return True
    return False

# devuelve número de columnas disponibles para la siguiente jugada
def jugadaPosible(tablero):    
    for columna in range(tablero.getAncho()):
        if (busca(tablero, columna) != -1):
            return True

    return False

# devuelve un jugador si ha ganado o 0 si no
def jugadaGanadora(tablero, fila, columna):
    if ((fila is not None) and (columna is not None)):
        ultimoJugador = tablero.getCelda(fila, columna)
        if (combinacionHorizontal(tablero, fila, columna)):
            return ultimoJugador
        else:
            if (combinacionVertical(tablero, fila, columna)):
                return ultimoJugador
            else:
                if (combinacionDiagAsc(tablero, fila, columna)):
                    return ultimoJugador
                else:
                    if (combinacionDiagDesc(tablero, fila, columna)):
                        return ultimoJugador
    return 0

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

# evalúa la situación global de ambos jugadores y devuelve una puntuación
def evaluarSituacion(tablero, jugador):
    fichaEnemiga = 1
    if (jugador):
        fichaEnemiga = 2
        
    puntuacion = puntuacionVertical(tablero, fichaEnemiga)
    puntuacion += puntuacionHorizontal(tablero, fichaEnemiga)
    puntuacion += puntuacionDiagDcha(tablero, fichaEnemiga)
    puntuacion += puntuacionDiagIzda(tablero, fichaEnemiga)

    return puntuacion

# puntuacion de abajo hacia arriba por columnas         
def puntuacionVertical(tablero, fichaEnemiga):
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
                elif (ficha == fichaEnemiga):
                    enemigas += 1
                else:
                    aliadas += 1
            puntuacion += sumarPuntos(vacias, enemigas, aliadas)
            
    return puntuacion

# puntuacion de izda a dcha por filas
def puntuacionHorizontal(tablero, fichaEnemiga):
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
                elif (ficha == fichaEnemiga):
                    enemigas += 1
                else:
                    aliadas += 1
            puntuacion += sumarPuntos(vacias, enemigas, aliadas)

            if (tablero.getCelda(fila, columna) == 0):
                columnasVacias += 1
        # si una fila completa está vacía no tiene sentido seguir buscando por encima
        if (vacias == tablero.getAncho()):
            break
            
    return puntuacion

# puntuacion diagonal de izda a dcha descendente
def puntuacionDiagDcha(tablero, fichaEnemiga):
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
                elif (ficha == fichaEnemiga):
                    enemigas += 1
                else:
                    aliadas += 1
            puntuacion += sumarPuntos(vacias, enemigas, aliadas)

    return puntuacion

# puntuacion diagonal de dcha a izda descendente
def puntuacionDiagIzda(tablero, fichaEnemiga):
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
                elif (ficha == fichaEnemiga):
                    enemigas += 1
                else:
                    aliadas += 1
            puntuacion += sumarPuntos(vacias, enemigas, aliadas)

    return puntuacion

# suma puntos de las fichas en función del jugador
def sumarPuntos(vacias, enemigas, aliadas):
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