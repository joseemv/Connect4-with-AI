from tablero import *

# indica si es un nodo hoja por llegar al último nivel del árbol, alguien gana o no quedan movimientos
def finArbol(tablero, profundidad):
    if (profundidad == 0 or posiblesMovimientos(tablero) == 0):
        return True
    return False

# devuelve la primer fila vacía de la columna indicada o -1 si están todas ocupadas
def busca(tablero, col):
    i = tablero.getAlto()-1
    hueco = False
    
    # recorre filas de la columna de arriba a abajo
    while i < tablero.getAlto() and i >= 0 and hueco == False:
        # si encuentra celda vacía
        if (tablero.getCelda(i, col) == 0):
            hueco = True
   
        # si no encuentra hueco vacío
        else:
            i -= 1
            
    return i

# devuelve número de columnas disponibles para la siguiente jugada
def posiblesMovimientos(tablero):
    opciones = 0
    
    for columna in range(tablero.getAncho()):
        if (busca(tablero, columna) != -1):
            opciones += 1
    return opciones

<<<<<<< Updated upstream
# llama al algoritmo que decide la jugada
def juega(tablero):
    profundidad = 3
    mejorColumna = minimax(tablero, profundidad, False)[1]      
    fila = busca(tablero, mejorColumna)    
    
    return fila, mejorColumna
    
def minimax(tablero, profundidad, jugador):    
    fin = finArbol(tablero, profundidad)
    ganador = tablero.cuatroEnRaya()
    puntuacionMejor = 0
=======
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

def combinacionHorizontal(tablero, fila, columna):
    fichaBuscada = tablero.getCelda(fila, columna)
    combinadas = 1
    for columnaActual in range(columna + 1, columna + 4):
        if (columnaActual < tablero.getAncho()):
            fichaActual = tablero.getCelda(fila, columnaActual)
            if (fichaActual == fichaBuscada):
                combinadas += 1
            else:
                break
        else:
            break

    if (combinadas == 4):
        return True   

    for columnaActual in range(columna - 1, columna - 4, -1):
        if (columnaActual >= 0):
            fichaActual = tablero.getCelda(fila, columnaActual)
            if (fichaActual != fichaBuscada):
                return False
        else:
            return False
    return True
    
def combinacionVertical(tablero, fila, columna):
    fichaBuscada = tablero.getCelda(fila, columna)
    combinadas = 1
    for filaActual in range(fila + 1, fila + 4):
        if (filaActual < tablero.getAlto()):
            fichaActual = tablero.getCelda(filaActual, columna)
            if (fichaActual == fichaBuscada):
                combinadas += 1
            else:
                break
        else:
            break

    if (combinadas == 4):
        return True   

    for filaActual in range(fila - 1, fila - 4, -1):
        if (filaActual >= 0):
            fichaActual = tablero.getCelda(filaActual, columna)
            if (fichaActual != fichaBuscada):
                return False
        else:
            return False
            
    return True
  
def combinacionDiagAsc(tablero, fila, columna):
    fichaBuscada = tablero.getCelda(fila, columna)
    columnaActual = columna
    combinadas = 1
    for filaActual in range(fila - 1, fila - 4, -1):
        columnaActual += 1
        if ((filaActual >= 0) and (columnaActual < tablero.getAncho())):
            fichaActual = tablero.getCelda(filaActual, columnaActual)
            if (fichaActual == fichaBuscada):
                combinadas += 1
            else:
                break
        else:
            break

    if (combinadas == 4):
        return True   

    columnaActual = columna
    for filaActual in range(fila + 1, fila + 4):
        columnaActual -= 1
        if ((filaActual < tablero.getAlto()) and (columnaActual >= 0)):
            fichaActual = tablero.getCelda(filaActual, columnaActual)
            if (fichaActual != fichaBuscada):
                return False
        else:
            return False
            
    return True

def combinacionDiagDesc(tablero, fila, columna):
    fichaBuscada = tablero.getCelda(fila, columna)
    columnaActual = columna
    combinadas = 1
    for filaActual in range(fila - 1, fila - 4, -1):
        columnaActual -= 1
        if ((filaActual >= 0) and (columnaActual >= 0)):
            fichaActual = tablero.getCelda(filaActual, columnaActual)
            if (fichaActual == fichaBuscada):
                combinadas += 1
            else:
                break
        else:
            break

    if (combinadas == 4):
        return True   

    columnaActual = columna
    for filaActual in range(fila + 1, fila + 4):
        columnaActual += 1
        if ((filaActual < tablero.getAlto()) and (columnaActual < tablero.getAncho())):
            fichaActual = tablero.getCelda(filaActual, columnaActual)
            if (fichaActual != fichaBuscada):
                return False
        else:
            return False
            
    return True

# llama al algoritmo que decide la jugada y devuelve la posición elegida
def juega(tablero):
    profundidad = 5
    mejorColumna = minimax(tablero, profundidad, False, None, None)[1]      
    fila = busca(tablero, mejorColumna) 

    return fila, mejorColumna
    
def minimax(tablero, profundidad, jugador, filaAnterior, columnaAnterior):
    fin = finArbol(tablero, profundidad)
    ganador = jugadaGanadora(tablero, filaAnterior, columnaAnterior)
>>>>>>> Stashed changes
    mejorColumna = 0
    
    # gana alguien, empate o límite de  profunidad
    if (fin or ganador != 0):
        # gana jugador
        if (ganador == 1):
            puntuacionMejor = -float("inf")
        # gana máquina
        elif (ganador == 2):
            puntuacionMejor = float("inf")
        # límite profundidad
        elif (profundidad == 0):
            puntuacionMejor = evaluarSituacion(tablero, jugador)
        # empate
        else:
            puntuacionMejor = 0

        # solo devuelve puntuación porque solo importa la posición elegida por la raíz
        return puntuacionMejor, None

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
            # juega persona MIN
            if (jugador):
                simulacionTablero.setCelda(fila, columna, 1)
<<<<<<< Updated upstream
                # recibe la mejor puntuación de las siguientes jugadas
                puntuacionActual = minimax(simulacionTablero, profundidad-1, False)[0]
                # si la puntuación es mejor que las anteriores se guarda la columna
=======
                # recibe la menor puntuación de las siguientes jugadas
                puntuacionActual = minimax(simulacionTablero, profundidad-1, False, fila, columna)[0]
                # si la puntuación es menor que las anteriores se guarda junto a la columna
>>>>>>> Stashed changes
                if (puntuacionActual < puntuacionMejor):
                    puntuacionMejor = puntuacionActual
                    mejorColumna = columna
            # juega máquina MAX
            else:
                simulacionTablero.setCelda(fila, columna, 2)
<<<<<<< Updated upstream
                puntuacionActual = minimax(simulacionTablero, profundidad-1, True)[0]
=======
                # recibe la mayor puntuación de las siguientes jugadas
                puntuacionActual = minimax(simulacionTablero, profundidad-1, True, fila, columna)[0]
                # si la puntuación es mayor que las anteriores se guarda junto a la columna
>>>>>>> Stashed changes
                if (puntuacionActual > puntuacionMejor):
                    puntuacionMejor = puntuacionActual
                    mejorColumna = columna
    # devolverá la puntuación a nodos hijos para recordar la rama que les beneficie y la mejor columna a la raíz para así tomar la decisión
    return puntuacionMejor, mejorColumna

def evaluarSituacion(tablero, jugador):
    puntuacion = 0
    
    ficha = 2
    if (jugador):
        ficha = 1
        
    # puntuacion vertical
    for fila in range(tablero.getAlto()-3):
        for columna in range(tablero.getAncho()):
            libres = 0
            ocupadas = 0
            enemigas = 0
            for i in range(4):
                if (tablero.getCelda(fila+i, columna) == 0):
                    libres += 1
                elif (tablero.getCelda(fila+i, columna) == ficha):
                    ocupadas += 1
                else:
                    enemigas += 1
            puntuacion += sumarPuntos(libres, ocupadas, enemigas)
    
    # puntuacion horizontal
    for fila in range(tablero.getAlto()):
        for columna in range(tablero.getAncho()-3):
            libres = 0
            ocupadas = 0
            enemigas = 0
            for i in range(4):
                if (tablero.getCelda(fila, columna+i) == 0):
                    libres += 1
                elif (tablero.getCelda(fila, columna+i) == ficha):
                    ocupadas += 1
                else:
                    enemigas += 1
            puntuacion += sumarPuntos(libres, ocupadas, enemigas)
    
    # puntuacion diagonal de izda a dcha
    for fila in range(tablero.getAlto()-3):
        for columna in range(tablero.getAncho()-3):
            libres = 0
            ocupadas = 0
            enemigas = 0
            for i in range(4):
                if (tablero.getCelda(fila+i, columna+i) == 0):
                    libres += 1
                elif (tablero.getCelda(fila+i, columna+i) == ficha):
                    ocupadas += 1
                else:
                    enemigas += 1
            puntuacion += sumarPuntos(libres, ocupadas, enemigas)
    
    # puntuacion diagonal de dcha a izda
    for fila in range(tablero.getAlto()-3):
        for columna in range(3, tablero.getAncho()):
            libres = 0
            ocupadas = 0
            enemigas = 0
            for i in range(4):
                if (tablero.getCelda(fila+i, columna-i) == 0):
                    libres += 1
                elif (tablero.getCelda(fila+i, columna-i) == ficha):
                    ocupadas += 1
                else:
                    enemigas += 1
            puntuacion += sumarPuntos(libres, ocupadas, enemigas)

    if (jugador):
        return -puntuacion
    return puntuacion
                
def sumarPuntos(libres, ocupadas, enemigas):
    puntos = 0

    if (enemigas == 3 and libres == 1):
        puntos = -10
    elif (enemigas == 2 and libres == 2):
        puntos = -5
    elif (ocupadas == 3 and libres == 1):
        puntos = 7
    elif (ocupadas == 2 and libres == 2):
        puntos = 4
    elif (ocupadas == 1 and libres == 3):
        puntos = 1

    return puntos