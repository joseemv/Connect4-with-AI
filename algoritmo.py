# busca en col la primera celda vacía
def busca(tablero, col):
    # si no está vacía
    if tablero.getCelda(0,col) != 0:
        i=-1
    i=0
    
    # mientras queden huecos en la columna
    while i<tablero.getAlto() and tablero.getCelda(i,col)==0:          
        i=i+1      
    i=i-1
   
    return i

# llama al algoritmo que decide la jugada
def juega(tablero, posicion):   
#     enc=False
#     c=0
#     while not enc and c<tablero.getAncho():
#         f=busca(tablero, c)
#         if f!=-1:
#             enc=True
#         else:
#             c=c+1
#     if f!=-1:

def minimax(tablero, posicion, profundidad):
    # f(N): función de evaluación.
    # N: estado.
    # B: factor de ramificación.
    
    while profunidad != 0:
        profundidad--
        for n in range(8):
            if busca(tablero, n):
                simulacion = Tablero(tablero)
                
                puntuacion = minimax(simulacion, posicion, profundidad)
                    
    # Devuelve solución minimax
#     posicion[0]=f
#     posicion[1]=c