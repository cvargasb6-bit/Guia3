from pasajero import Pasajero


class MiPila:
    """Pila (LIFO) hecha a mano sobre un arreglo de tamaño fijo.
    datos -> [fondo, ..., TOPE, None, None]
    TOPE  -> datos[cantidad - 1]  (el último que entró: el único que se ve y el único que sale)
    ⛔ Mismas prohibiciones que MiLista: sin append, pop, insert, remove, index,
       sort, reverse, copy, len(), in, slicing ni comprensiones.
    """

    def __init__(self, capacidad=10):
        self.datos = [None] * capacidad
        self.capacidad = capacidad
        self.cantidad = 0

    def apilar(self, pasajero):                      # = añadir de MiLista
        if self.cantidad == self.capacidad:
            print("  ⚠ La pila está llena")
            return False
        if self.buscar(pasajero.numero) != -1:        # mejora: no repetir números
            print(f"  ⚠ Ya existe un pasajero con el número {pasajero.numero}")
            return False
        self.datos[self.cantidad] = pasajero          # el nuevo queda encima: es el TOPE
        self.cantidad = self.cantidad + 1
        return True

    def listar(self):                                 # EJEMPLO: del TOPE al FONDO
        if self.cantidad == 0:
            print("  (pila vacía)")
            return
        for i in range(self.cantidad - 1, -1, -1):    # cantidad-1, ..., 1, 0  (hacia atrás)
            if i == self.cantidad - 1:
                print(f"  [{i}] {self.datos[i]}  ← TOPE")
            elif i == 0:
                print(f"  [{i}] {self.datos[i]}  ← FONDO")
            else:
                print(f"  [{i}] {self.datos[i]}")

    # ------- recorre SIEMPRE del tope al fondo -------
    def desapilar(self):
        """Saca SOLO el tope. Retorna el pasajero, o None si la pila está vacía."""
        if self.cantidad == 0:
            return None
        tope = self.datos[self.cantidad - 1]
        self.datos[self.cantidad - 1] = None          # no se corre nada: solo se vacía el cajón
        self.cantidad = self.cantidad - 1
        return tope

    def ver_tope(self):
        """Retorna el tope SIN sacarlo (None si está vacía)."""
        if self.cantidad == 0:
            return None
        return self.datos[self.cantidad - 1]

    def buscar(self, numero):
        """Búsqueda lineal del tope al fondo. Retorna la posición o -1."""
        for i in range(self.cantidad - 1, -1, -1):
            if self.datos[i].numero == numero:
                return i
        return -1

    def modificar(self, numero, nuevo_destino, nuevo_asiento):
        """Cambia destino y asiento. Nadie cambia de lugar. Retorna True/False."""
        pos = self.buscar(numero)
        if pos == -1:
            return False
        self.datos[pos].destino = nuevo_destino
        self.datos[pos].asiento = nuevo_asiento
        return True

    def eliminar_por_numero(self, numero):
        """No se puede sacar del medio: se desapila hacia una pila auxiliar hasta
        encontrarlo, se descarta, y se vuelve a apilar lo de la auxiliar (mismo orden)."""
        if self.buscar(numero) == -1:
            return False
        aux = MiPila(self.capacidad)
        encontrado = False
        while self.cantidad > 0 and not encontrado:
            p = self.desapilar()
            if p.numero == numero:
                encontrado = True                     # se descarta
            else:
                aux.apilar(p)
        while aux.cantidad > 0:                       # devolver en el orden original
            self.apilar(aux.desapilar())
        return True

    def copiar(self):
        """Nueva pila con los mismos pasajeros y el mismo tope (se apila del fondo al tope)."""
        nueva = MiPila(self.capacidad)
        for i in range(self.cantidad):                # 0 -> cantidad-1
            p = self.datos[i]
            nueva.apilar(Pasajero(p.numero, p.nombre, p.cedula, p.edad,
                                  p.fecha_vuelo, p.destino, p.asiento))
        return nueva

    def longitud(self):
        return self.cantidad

    def esta_vacia(self):
        return self.cantidad == 0
