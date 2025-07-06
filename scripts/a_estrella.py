import heapq

class Nodo:
    def __init__(self, posicion, padre=None):
        self.posicion = posicion
        self.padre = padre
        self.g = 0
        self.h = 0
        self.f = 0

    def __lt__(self, other):
        return self.f < other.f

def a_estrella(mapa, inicio, objetivo):
    abiertos = []
    cerrados = set()
    inicio_nodo = Nodo(inicio)
    objetivo_nodo = Nodo(objetivo)
    heapq.heappush(abiertos, inicio_nodo)

    while abiertos:
        actual = heapq.heappop(abiertos)
        cerrados.add(actual.posicion)

        if actual.posicion == objetivo_nodo.posicion:
            camino = []
            while actual:
                camino.append(actual.posicion)
                actual = actual.padre
            return camino[::-1]

        x, y = actual.posicion
        vecinos = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]

        for nx, ny in vecinos:
            if not (0 <= nx < len(mapa[0]) and 0 <= ny < len(mapa)):
                continue
            if mapa[ny][nx] == 1 or (nx, ny) in cerrados:
                continue

            vecino = Nodo((nx, ny), actual)
            vecino.g = actual.g + 1
            vecino.h = abs(nx - objetivo[0]) + abs(ny - objetivo[1])
            vecino.f = vecino.g + vecino.h

            if any(n.posicion == vecino.posicion and n.f <= vecino.f for n in abiertos):
                continue

            heapq.heappush(abiertos, vecino)

    return None
