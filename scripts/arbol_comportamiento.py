class Nodo:
    def ejecutar(self):
        raise NotImplementedError("Este método debe ser implementado por las subclases")

class Secuencia(Nodo):
    def __init__(self, nodos):
        self.nodos = nodos

    def ejecutar(self):
        for nodo in self.nodos:
            if not nodo.ejecutar():
                return False
        return True

class Selector(Nodo):
    def __init__(self, nodos):
        self.nodos = nodos

    def ejecutar(self):
        for nodo in self.nodos:
            if nodo.ejecutar():
                return True
        return False

class Condicion(Nodo):
    def __init__(self, funcion):
        self.funcion = funcion

    def ejecutar(self):
        return self.funcion()

class Accion(Nodo):
    def __init__(self, funcion):
        self.funcion = funcion

    def ejecutar(self):
        self.funcion()
        return True
