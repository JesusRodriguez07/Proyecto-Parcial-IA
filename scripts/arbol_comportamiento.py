# Clase base abstracta para todos los nodos del árbol de comportamiento
# Autor: jesus rodriguez - 12-sisn-2-043
class Nodo:
    def ejecutar(self):
        # Método abstracto, debe ser implementado por todas las subclases
        raise NotImplementedError("Este método debe ser implementado por las subclases")


# Nodo compuesto: Secuencia (Sequence Node)
# Ejecuta cada nodo hijo en orden, se detiene si uno falla
class Secuencia(Nodo):
    def __init__(self, nodos):
        self.nodos = nodos  # Lista de nodos hijos

    def ejecutar(self):
        for nodo in self.nodos:
            if not nodo.ejecutar():  # Si uno falla, la secuencia falla
                return False
        return True  # Todos los nodos se ejecutaron con éxito


# Nodo compuesto: Selector (Selector Node)
# Ejecuta cada nodo hijo hasta que uno tenga éxito
class Selector(Nodo):
    def __init__(self, nodos):
        self.nodos = nodos  # Lista de nodos hijos

    def ejecutar(self):
        for nodo in self.nodos:
            if nodo.ejecutar():  # Si uno tiene éxito, el selector también
                return True
        return False  # Todos fallaron


# Nodo hoja: Condición (Condition Node)
# Evalúa una función booleana y devuelve su resultado
class Condicion(Nodo):
    def __init__(self, funcion):
        self.funcion = funcion  # Función que retorna True o False

    def ejecutar(self):
        return self.funcion()  # Se ejecuta la función y se devuelve el resultado


# Nodo hoja: Acción (Action Node)
# Ejecuta una acción (función) y siempre retorna True
class Accion(Nodo):
    def __init__(self, funcion):
        self.funcion = funcion  # Función que representa la acción a realizar

    def ejecutar(self):
        self.funcion()  # Ejecuta la acción
        return True  # Siempre retorna éxito
