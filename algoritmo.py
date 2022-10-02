from tablero import *
import math

# indica si es un nodo hoja por llegar al límite de profundidad o no quedan movimientos posibles
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

# devuelve número de columnas disponibles para la siguiente jugadas
def posiblesMovimientos(tablero):
    opciones = 0
    
    for columna in range(tablero.getAncho()):
        if (busca(tablero, columna) != -1):
            opciones += 1

    return opciones

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
    mejorColumna = 0
    
    # gana alguien, empate o límite de  profunidad
    if (fin or ganador != 0):
        # gana jugador
        if (ganador == 1):
            # si devuelve -infinito no podrá elegir entre dos jugadas que conduzcan a la derrota
            puntuacionMejor = -100000000
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
                simulacionTablero.setCelda(fila, columna, 1)
                # recibe la menor puntuación de las siguientes jugadas
                puntuacionActual = minimax(simulacionTablero, profundidad-1, False, fila, columna)[0]
                # si la puntuación es menor que las anteriores se guarda junto a la columna
                if (puntuacionActual < puntuacionMejor):
                    puntuacionMejor = puntuacionActual
                    mejorColumna = columna
            # juega máquina MAX
            else:
                simulacionTablero.setCelda(fila, columna, 2)
                # recibe la mayor puntuación de las siguientes jugadas
                puntuacionActual = minimax(simulacionTablero, profundidad-1, True, fila, columna)[0]
                # si la puntuación es mayor que las anteriores se guarda junto a la columna
                if (puntuacionActual > puntuacionMejor):
                    puntuacionMejor = puntuacionActual
                    mejorColumna = columna

    # devolverá la puntuación a nodos hijos para recordar la rama que les beneficie y la mejor columna a la raíz para así tomar la decisión
    return puntuacionMejor, mejorColumna

# evalúa la situación global de ambos jugadores y devuelve una puntuación
def evaluarSituacion(tablero, jugador):
    fichaEnemiga = 1
    if (jugador):
        fichaEnemiga = 2
        
    puntuacion = puntuacionVertical(tablero, fichaEnemiga)
    puntuacion += puntuacionHorizontal(tablero, fichaEnemiga)
    puntuacion += puntuacionDiagAsc(tablero, fichaEnemiga)
    puntuacion += puntuacionDiagDesc(tablero, fichaEnemiga)

    if (jugador):
        return -puntuacion
    else:
        return puntuacion

# puntuacion de abajo hacia arriba por columnas         
def puntuacionVertical(tablero, fichaEnemiga):
    puntuacion = 0

    for columna in range(tablero.getAncho()):
        combinacion = []
        for fila in range(tablero.getAlto()-1, 0, -1):
            # si encuentra una celda vacía no tiene sentido seguir buscando arriba
            if (tablero.estaVacia(fila, columna)):
                break
            combinacion.append(tablero.getCelda(fila, columna))
            if (len(combinacion) == 4):
                puntuacion += analizarCombinacion(combinacion, fichaEnemiga)
                combinacion.pop(0)
        combinacion.clear()
            
    return puntuacion

# puntuacion de izda a dcha por filas
def puntuacionHorizontal(tablero, fichaEnemiga):
    puntuacion = 0

    for fila in range(tablero.getAlto()-1, 0, -1):
        vacias = 0
        combinacion = []
        for columna in range(tablero.getAncho()):
            if (tablero.estaVacia(fila, columna)):
                vacias += 1
            combinacion.append(tablero.getCelda(fila, columna))
            if (len(combinacion) == 4):
                puntuacion += analizarCombinacion(combinacion, fichaEnemiga)
                combinacion.pop(0)
        combinacion.clear()
        # si una fila completa está vacía no tiene sentido seguir buscando por encima
        if (vacias == tablero.getAncho()):
            break
            
    return puntuacion

# puntuacion diagonal de izda a dcha ascendente
def puntuacionDiagAsc(tablero, fichaEnemiga):
    puntuacion = 0

    # primera parte
    longDiagonal = 0
    for fila in range(3, tablero.getAlto()):
        combinacion = []
        for columna in range(0, tablero.getAlto()-3 + longDiagonal):
            combinacion.append(tablero.getCelda(fila - columna, columna))
            if (len(combinacion) == 4):
                puntuacion += analizarCombinacion(combinacion, fichaEnemiga)
                combinacion.pop(0)
        combinacion.clear()
        longDiagonal += 1

    # segunda parte
    longDiagonal = 0
    for columna in range(1, tablero.getAncho() - 3):
        combinacion = []
        for fila in range(tablero.getAlto() -1, 0 + longDiagonal, -1):
            combinacion.append(tablero.getCelda(fila, tablero.getAlto() - fila))
            if (len(combinacion) == 4):
                puntuacion += analizarCombinacion(combinacion, fichaEnemiga)
                combinacion.pop(0)
        combinacion.clear()
        longDiagonal += 1
            
    return puntuacion

# puntuacion diagonal de izda a dcha descendente
def puntuacionDiagDesc(tablero, fichaEnemiga):
    puntuacion = 0

    # primera parte
    longDiagonal = 1
    for fila in range(0, tablero.getAlto() - 3):
        combinacion = []
        for columna in range(0, tablero.getAncho() - 1 - longDiagonal):
            combinacion.append(tablero.getCelda(fila + columna, columna))
            if (len(combinacion) == 4):
                puntuacion += analizarCombinacion(combinacion, fichaEnemiga)
                combinacion.pop(0)
        combinacion.clear()
        longDiagonal += 1

    # segunda parte
    longDiagonal = 0
    for columna in range(1, tablero.getAncho() -3):
        combinacion = []
        for fila in range(tablero.getAncho() - 1 - longDiagonal):
            combinacion.append(tablero.getCelda(fila, columna + fila))
            if (len(combinacion) == 4):
                puntuacion += analizarCombinacion(combinacion, fichaEnemiga)
                combinacion.pop(0)
        combinacion.clear()
        longDiagonal += 1
            
    return puntuacion

# analiza la composición de la combinación de fichas
def analizarCombinacion(combinacion, fichaEnemiga):
    aliadas = 0
    enemigas = 0

    for ficha in combinacion:
        if ((ficha != fichaEnemiga) and (ficha != 0)):
            aliadas += 1
        elif (ficha == fichaEnemiga):
            aliadas = 0
            break
    
    for ficha in combinacion:
        if (ficha == fichaEnemiga):
            enemigas += 1
        elif ((ficha != ficha) and (ficha != 0)):
            enemigas = 0
            break
    
    if (aliadas > 0):
        return sumarPuntos(aliadas, False)
    elif (enemigas > 0):
        return -sumarPuntos(enemigas, True)
    else:
        return 0

# suma puntos de las fichas en función del jugador
def sumarPuntos(fichas, enemigas):
    if (enemigas):
        match fichas:
            case 1:
                return 3
            case 2:
                return 7
            case 3: 
                return 1000
            case _:
                return 0
                
    else:
        match fichas:
            case 1:
                return 1
            case 2:
                return 3
            case 3: 
                return 7
            case _:
                return 0