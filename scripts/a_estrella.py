# a_estrella.py comentado por jesus rodriguez
# Autor: jesus rodriguez - 12-sisn-2-043

# Importamos la librería heapq para usar una cola de prioridad (min-heap)
import heapq

# Clase Nodo que representa una posición en el mapa
class Nodo:
    def __init__(self, posicion, padre=None):
        self.posicion = posicion  # Coordenadas (x, y)
        self.padre = padre        # Nodo padre para reconstruir el camino
        self.g = 0                # Costo desde el inicio hasta este nodo
        self.h = 0                # Heurística estimada al objetivo (distancia Manhattan)
        self.f = 0                # Costo total (f = g + h)

    def __lt__(self, other):
        # Permite comparar nodos por su costo total para usar en heapq
        return self.f < other.f

# Función A* para buscar el camino más corto entre dos puntos en un mapa
# mapa: matriz de 0s y 1s (1 = obstáculo, 0 = camino libre)
# inicio y objetivo: tuplas (x, y)
def a_estrella(mapa, inicio, objetivo):
    abiertos = []  # Lista de nodos abiertos (a explorar)
    cerrados = set()  # Conjunto de nodos ya evaluados
    inicio_nodo = Nodo(inicio)
    objetivo_nodo = Nodo(objetivo)
    heapq.heappush(abiertos, inicio_nodo)  # Insertamos el nodo inicial en la cola de prioridad

    while abiertos:
        # Extraemos el nodo con menor costo f
        actual = heapq.heappop(abiertos)
        cerrados.add(actual.posicion)

        # Si llegamos al objetivo, reconstruimos el camino y lo devolvemos
        if actual.posicion == objetivo_nodo.posicion:
            camino = []
            while actual:
                camino.append(actual.posicion)
                actual = actual.padre
            return camino[::-1]  # Lo invertimos para que vaya de inicio a objetivo

        # Generamos los vecinos (arriba, abajo, izquierda, derecha)
        x, y = actual.posicion
        vecinos = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]

        for nx, ny in vecinos:
            # Verificamos que la posición esté dentro de los límites del mapa
            if not (0 <= nx < len(mapa[0]) and 0 <= ny < len(mapa)):
                continue
            # Verificamos que no sea un obstáculo ni que ya haya sido evaluado
            if mapa[ny][nx] == 1 or (nx, ny) in cerrados:
                continue

            # Creamos un nuevo nodo vecino
            vecino = Nodo((nx, ny), actual)
            vecino.g = actual.g + 1  # Coste desde el inicio hasta este vecino
            vecino.h = abs(nx - objetivo[0]) + abs(ny - objetivo[1])  # Heurística Manhattan
            vecino.f = vecino.g + vecino.h  # Costo total

            # Si ya hay un nodo igual en abiertos con menor o igual f, lo ignoramos
            if any(n.posicion == vecino.posicion and n.f <= vecino.f for n in abiertos):
                continue

            # Insertamos el nuevo vecino en la cola de prioridad
            heapq.heappush(abiertos, vecino)

    # Si no se encontró camino, devolvemos None
    return None
