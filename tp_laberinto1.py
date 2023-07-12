class Nodo:
    def __init__(self, _estado, _padre, _distancia):
        self.estado = _estado
        self.padre = _padre
        self.distancia = _distancia


class FronteraStack:
    def __init__(self):
        self.frontera = []

    def __str__(self):
        return "Nodos en la frontera: " + " ".join(str(nodo.estado) for nodo in self.frontera)
    
    def agregar_nodo(self, _nodo):
        self.frontera.append(_nodo)

    def quitar_nodo(self):
        return self.frontera.pop()

    def esta_vacia(self):
        return len(self.frontera) == 0

    def contiene_estado(self, _estado):
        for nodo in self.frontera:
            if nodo.estado == _estado:
                return True
        return False


class FronteraQueue(FronteraStack):
    def quitar_nodo(self):
        return self.frontera.pop(0)


class FronteraGBFS(FronteraQueue):
    def agregar_nodo(self, _nodo):
        self.frontera.append(_nodo)
        self.frontera.sort(key=lambda n: n.distancia)
        
        
class FronteraAsearch(FronteraGBFS):
    pass


class Laberinto:
    def __init__(self, _algoritmo):
        with open('laberinto2.txt', 'r') as archivo:
            laberinto = archivo.read()
            laberinto = laberinto.splitlines()
        self.ancho = len(laberinto[0])
        self.alto = len(laberinto)
        self.paredes = []

        for fila in range(self.alto):
            fila_paredes = []
            for columna in range(self.ancho):
                if laberinto[fila][columna] == ' ':
                    fila_paredes.append(False)
                elif laberinto[fila][columna] == 'I':
                    self.inicio = (fila, columna)
                    fila_paredes.append(False)
                elif laberinto[fila][columna] == 'M':
                    self.meta = (fila, columna)
                    fila_paredes.append(False)
                else:
                    fila_paredes.append(True)
            self.paredes.append(fila_paredes)

        self.solucion = None
        self.algoritmo = _algoritmo

    def expandir_nodo(self, _nodo):
        fila, columna = _nodo.estado
        posiciones = [(fila + 1, columna), (fila, columna - 1), (fila - 1, columna), (fila, columna + 1)]
        vecinos = []
        for f, c in posiciones:
            if 0 <= f < self.alto and 0 <= c < self.ancho and not self.paredes[f][c]:
                vecinos.append((f, c))
        return vecinos

    def calcular_distancia(self, _posicion):
        filaA, colA = _posicion
        filaM, colM = self.meta
        distancia_h = abs(colM - colA)
        distancia_v = abs(filaM - filaA)
        return distancia_h + distancia_v
    
    def calcular_costo(self, _posicion):
        filaA, colA = _posicion
        filaI, colI = self.inicio
        distancia_h = abs(colI - colA)
        distancia_v = abs(filaI - filaA)
        return distancia_h + distancia_v
    def resolver(self):
        if self.algoritmo == 'BFS':
            frontera = FronteraQueue()
        elif self.algoritmo == 'DFS':
            frontera = FronteraStack()
        elif self.algoritmo == 'GBFS':
            frontera = FronteraGBFS()
        elif self.algoritmo == 'AS':
            frontera = FronteraAsearch()

        nodo_inicial = Nodo(self.inicio, None, self.calcular_distancia(self.inicio))
        frontera.agregar_nodo(nodo_inicial)
        self.explorados = []
        self.numero_explorado = 0
        
        while True:
            if frontera.esta_vacia():
                raise Exception("No hay solución")

            nodo_actual = frontera.quitar_nodo()

            if nodo_actual.estado == self.meta:
                print("Llegué a la meta")
                self.solucion = []
                while nodo_actual.padre is not None:
                    self.solucion.append(nodo_actual.padre)
                    nodo_actual = nodo_actual.padre
                self.solucion.reverse()
                return self.solucion

            self.explorados.append(nodo_actual.estado)
            self.numero_explorado += 1

            for posicion in self.expandir_nodo(nodo_actual):
                if (not frontera.contiene_estado(posicion) and not posicion in self.explorados):
                    if self.algoritmo == "AS":
                        hijo = Nodo(posicion, nodo_actual, self.calcular_distancia(posicion)+self.calcular_costo(posicion))
                    else:
                        hijo = Nodo(posicion, nodo_actual, self.calcular_distancia(posicion))
                    frontera.agregar_nodo(hijo)
            


laberinto = Laberinto("AS")
#print(laberinto.calcular_distancia(Nodo((0, 3), None, (1, 1))))

solucion = laberinto.resolver()
for nodo in solucion:
    print(nodo.estado)
#print(laberinto.numero_explorado)

#nodo1 = Nodo((4,3),None,(5,9))
#nodo2 = Nodo((7,2),None,(5,9))
#nodo3 = Nodo((15,2),None,(5,9))

#frontera = [nodo1,nodo2,nodo3]
#frontera.sort(key=lambda n: (n.distancia))
#for nodo in frontera:
#    print(nodo.distancia)

