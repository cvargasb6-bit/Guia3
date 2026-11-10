from pasajero import Pasajero


class MiCola:
    """Cola (FIFO) hecha a mano sobre un arreglo de tamaño fijo.
    datos  -> [FRENTE, ..., FINAL, None, None]
    FRENTE -> datos[0]             (el primero que llegó: el único que sale)
    FINAL  -> datos[cantidad - 1]  (los nuevos se ponen detrás de él)
    ⛔ Mismas prohibiciones que MiLista: sin append, pop, insert, remove, index,
       sort, reverse, copy, len(), in, slicing ni comprensiones.
    """

    def __init__(self, capacidad=10):
        self.datos = [None] * capacidad
        self.capacidad = capacidad
        self.cantidad = 0

    def encolar(self, pasajero):                     # = añadir de MiLista
        if self.cantidad == self.capacidad:
            print("  ⚠ La cola está llena")
            return False
        if self.buscar(pasajero.numero) != -1:        # mejora: no repetir números
            print(f"  ⚠ Ya existe un pasajero con el número {pasajero.numero}")
            return False
        self.datos[self.cantidad] = pasajero          # se pone a la fila por detrás
        self.cantidad = self.cantidad + 1
        return True

    def listar(self):                                 # EJEMPLO: del FRENTE al FINAL
        if self.cantidad == 0:
            print("  (cola vacía)")
            return
        for i in range(self.cantidad):                # 0, 1, ..., cantidad-1  (hacia adelante)
            if i == 0:
                print(f"  [{i}] {self.datos[i]}  ← FRENTE")
            elif i == self.cantidad - 1:
                print(f"  [{i}] {self.datos[i]}  ← FINAL")
            else:
                print(f"  [{i}] {self.datos[i]}")

    # ------- recorre SIEMPRE del frente al final -------
    def desencolar(self):
        """Saca SOLO el frente datos[0] y corre todos a la izquierda.
        Retorna el pasajero, o None si la cola está vacía."""
        if self.cantidad == 0:
            return None
        frente = self.datos[0]
        for i in range(self.cantidad - 1):
            self.datos[i] = self.datos[i + 1]
        self.datos[self.cantidad - 1] = None
        self.cantidad = self.cantidad - 1
        return frente

    def ver_frente(self):
        """Retorna el frente SIN sacarlo (None si está vacía)."""
        if self.cantidad == 0:
            return None
        return self.datos[0]

    def buscar(self, numero):
        """Búsqueda lineal del frente al final. Retorna la posición o -1."""
        for i in range(self.cantidad):
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
        """No se puede sacar del medio: se desencola 'cantidad' veces; si no es el
        buscado se vuelve a encolar, si lo es se descarta. La fila da una vuelta completa."""
        if self.buscar(numero) == -1:
            return False
        total = self.cantidad
        for i in range(total):
            p = self.desencolar()
            if p.numero != numero:
                self.encolar(p)
        return True

    def copiar(self):
        """Nueva cola con los mismos pasajeros (se encola del frente al final)."""
        nueva = MiCola(self.capacidad)
        for i in range(self.cantidad):
            p = self.datos[i]
            nueva.encolar(Pasajero(p.numero, p.nombre, p.cedula, p.edad,
                                   p.fecha_vuelo, p.destino, p.asiento))
        return nueva

    def longitud(self):
        return self.cantidad

    def esta_vacia(self):
        return self.cantidad == 0
