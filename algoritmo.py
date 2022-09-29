from tablero import *

iMinimax = 0
iEvalua = 0

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

# devuelve número de jugadas disponibles en función de columnas con hueco
def posiblesMovimientos(tablero):
    opciones = 0
    
    for columna in range(tablero.getAncho()):
        if (busca(tablero, columna) != -1):
            opciones += 1

    return opciones

# llama al algoritmo que decide la jugada y devuelve la posición elegida
def juega(tablero):
    profundidad = 4
    mejorColumna = minimax(tablero, profundidad, False)[1]      
    fila = busca(tablero, mejorColumna)    
    
    print("iteraciones minimax: ", iMinimax)
    print("iteraciones evalua: ", iEvalua)    

    return fila, mejorColumna
    
def minimax(tablero, profundidad, jugador):  
    global iMinimax
    iMinimax += 1  
    fin = finArbol(tablero, profundidad)
    ganador = tablero.cuatroEnRaya()
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

    # se inicializa la 
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
                puntuacionActual = minimax(simulacionTablero, profundidad-1, False)[0]
                # si la puntuación es menor que las anteriores se guarda junto a la columna
                if (puntuacionActual < puntuacionMejor):
                    puntuacionMejor = puntuacionActual
                    mejorColumna = columna
            # juega máquina MAX
            else:
                simulacionTablero.setCelda(fila, columna, 2)
                # recibe la mayor puntuación de las siguientes jugadas
                puntuacionActual = minimax(simulacionTablero, profundidad-1, True)[0]
                # si la puntuación es mayor que las anteriores se guarda junto a la columna
                if (puntuacionActual > puntuacionMejor):
                    puntuacionMejor = puntuacionActual
                    mejorColumna = columna

    # devolverá la puntuación a nodos hijos para recordar la rama que les beneficie y la mejor columna a la raíz para así tomar la decisión
    return puntuacionMejor, mejorColumna

# evalua la situación global de ambos jugadores y devuelve una puntuación
def evaluarSituacion(tablero, jugador):
    global iEvalua
    iEvalua += 1
    fichaEnemiga = 1
    if (jugador):
        fichaEnemiga = 2
        
    puntuacion = puntuacionVertical(tablero, fichaEnemiga)
    puntuacion += puntuacionHorizontal(tablero, fichaEnemiga)
    puntuacion += puntuacionDiagDcha(tablero, fichaEnemiga)
    puntuacion += puntuacionDiagIzda(tablero, fichaEnemiga)

    if (jugador):
        return -puntuacion
    else:
        return puntuacion

# puntuacion de arriba a abajo por columnas            
def puntuacionVertical(tablero, fichaEnemiga):
    puntuacion = 0

    for columna in range(tablero.getAncho()):
        combinacion = []
        for fila in range(tablero.getAlto()):
            combinacion.append(tablero.getCelda(fila, columna))
            puntuacion += sumarPuntos(combinacion, fichaEnemiga)
            if (len(combinacion) == 4):
                combinacion.pop(0)
        combinacion.clear()
            
    return puntuacion

# puntuacion de izda a dcha por filas
def puntuacionHorizontal(tablero, ficha):
    puntuacion = 0

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

    return puntuacion

# puntuacion diagonal de izda a dcha por filas
def puntuacionDiagDcha(tablero, ficha):
    puntuacion = 0

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
            
    return puntuacion

# puntuacion diagonal de dcha a izda por filas
def puntuacionDiagIzda(tablero, ficha):
    puntuacion = 0

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
            
    return puntuacion

# Analiza la composición de la combinación de fichas
def analizarCombinacion(combinacion, fichaEnemiga):
    puntos = 0
    aliadas = 0

    for ficha in combinacion:
        if ((ficha != fichaEnemiga) and (ficha != 0)):
            aliadas += 1
        elif (ficha == fichaEnemiga):
            return 0

    match aliadas:
        case 1:
            return 1
        case 2:
            return 3
        case 3:
            return 7
    
    return sumarPuntos(aliadas)

# suma puntos en función de que posiciones del tablero están ocupadas y por qué jugador
def sumarPuntos(libres, aliadas, enemiga):
    puntos = 0

    # cuenta a adversario como ganador porque la siguiente jugada es suya
    if (not enemiga):
        if ()

    return puntos

# PUNTOS
# 3 ALIADAS 1 HUECO = 7
# 2 ALIADAS 2 HUECOS = 4
# 1 ALIADA 3 HUECOS = 1
# CUALQUIER ENEMIGA = 0

# 3 ENEMIGAS 1 HUECO = -1000
# 2 ENEMIGAS 2 HUECOS = -7
# 1 ENEMIGA 3 HUECOS = -4
# CUALQUIER ALIADA = 0