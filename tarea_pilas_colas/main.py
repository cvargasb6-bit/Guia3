from datetime import datetime

from pasajero import Pasajero
from mi_pila import MiPila
from mi_cola import MiCola

pila = MiPila(10)
cola = MiCola(10)


# ------------------------- funciones de apoyo -------------------------
def leer_entero(mensaje, minimo=None, maximo=None):
    """Pide un entero y valida tipo y rango. Repite hasta que sea válido."""
    while True:
        try:
            valor = int(input(mensaje))
        except ValueError:
            print("  Debe ser un número entero.")
            continue
        if minimo is not None and valor < minimo:
            print(f"  Debe ser mayor o igual a {minimo}.")
        elif maximo is not None and valor > maximo:
            print(f"  Debe ser menor o igual a {maximo}.")
        else:
            return valor


def leer_nombre(mensaje):
    while True:
        texto = input(mensaje).strip()
        if texto == "":
            print("  El nombre no puede estar vacío.")
        elif not all(c.isalpha() or c == " " for c in texto):
            print("  El nombre solo puede tener letras y espacios.")
        else:
            return texto


def leer_cedula(mensaje):
    while True:
        texto = input(mensaje).strip()
        if len(texto) == 10 and texto.isdigit():
            return texto
        print("  La cédula debe tener exactamente 10 dígitos.")


def leer_fecha(mensaje):
    while True:
        texto = input(mensaje).strip()
        try:
            datetime.strptime(texto, "%Y-%m-%d")
            return texto
        except ValueError:
            print("  Fecha inválida. Use el formato AAAA-MM-DD (ej. 2026-11-15).")


def leer_destino(mensaje):
    while True:
        texto = input(mensaje).strip()
        if texto != "":
            return texto.title()
        print("  El destino no puede estar vacío.")


def leer_asiento(mensaje):
    while True:
        texto = input(mensaje).strip().upper()
        if len(texto) == 3 and texto[:2].isdigit() and texto[2] in "ABCDEF":
            return texto
        print("  Asiento inválido. Use dos dígitos y una letra A-F (ej. 12A).")


def leer_pasajero():
    numero = leer_entero("  N.º de pasajero: ", 1)
    nombre = leer_nombre("  Nombre: ")
    cedula = leer_cedula("  Cédula: ")
    edad = leer_entero("  Edad: ", 0, 120)
    fecha = leer_fecha("  Fecha de vuelo (AAAA-MM-DD): ")
    destino = leer_destino("  Destino: ")
    asiento = leer_asiento("  Asiento: ")
    return Pasajero(numero, nombre, cedula, edad, fecha, destino, asiento)


def datos_prueba():
    """Los 5 pasajeros de prueba en ORDEN DE LLEGADA (Diana llega primero, Elena última)."""
    return [
        Pasajero(1005, "Diana", "0923456789", 22, "2026-11-15", "Quito",  "12A"),
        Pasajero(1002, "Ana",   "0912345678", 28, "2026-11-15", "Lima",   "03C"),
        Pasajero(1009, "Luis",  "0987654321", 35, "2026-11-20", "Bogotá", "18F"),
        Pasajero(1004, "Beto",  "0934567890", 16, "2026-11-20", "Quito",  "07B"),
        Pasajero(1001, "Elena", "0901234567", 41, "2026-11-22", "Lima",   "01A"),
    ]


def mostrar_opciones(titulo, entrar, salir, ver):
    print(f"\n========== {titulo} ==========")
    print(f" 1. {entrar:<12}  2. Listar          3. {salir}")
    print(f" 4. {ver:<12}  5. Buscar          6. Modificar")
    print(" 7. Eliminar por número         8. Copiar")
    print(" 9. Longitud / ¿vacía?")
    print(" C. Cargar datos de prueba      0. Volver")


# ---------------------- MENÚ 1 · PILA ----------------------
def menu_pila():
    while True:
        mostrar_opciones("MENÚ 1 · PILA (LIFO)", "Apilar", "Desapilar", "Ver tope")
        op = input("Opción: ").strip().upper()

        if op == "1":
            pasajero = leer_pasajero()                 # 1. LEER
            if pila.apilar(pasajero):                  # 2. LLAMAR
                print("  ✓ Apilado: ahora es el tope") # 3. MOSTRAR
        elif op == "2":
            pila.listar()
        elif op == "3":
            salio = pila.desapilar()                   # 2. LLAMAR
            if salio is None:                          # 3. MOSTRAR
                print("  ⚠ La pila está vacía")
            else:
                print(f"  ✓ Salió: {salio.nombre}")
                nuevo = pila.ver_tope()
                if nuevo is None:
                    print("  La pila quedó vacía")
                else:
                    print(f"  Nuevo tope: {nuevo.nombre}")
        elif op == "4":
            tope = pila.ver_tope()
            if tope is None:
                print("  ⚠ La pila está vacía")
            else:
                print(f"  Tope: {tope.nombre} ({tope.numero})")
        elif op == "5":
            if pila.esta_vacia():
                print("  ⚠ La pila está vacía")
            else:
                numero = leer_entero("  N.º de pasajero a buscar: ")
                pos = pila.buscar(numero)
                if pos == -1:
                    print("  No existe ese pasajero")
                else:
                    print(f"  Encontrado en [{pos}]: {pila.datos[pos].nombre}")
                    print(f"  {pila.datos[pos]}")
        elif op == "6":
            if pila.esta_vacia():
                print("  ⚠ La pila está vacía")
            else:
                numero = leer_entero("  N.º de pasajero a modificar: ")
                if pila.buscar(numero) == -1:
                    print("  No existe ese pasajero")
                else:
                    destino = leer_destino("  Nuevo destino: ")
                    asiento = leer_asiento("  Nuevo asiento: ")
                    if pila.modificar(numero, destino, asiento):
                        print("  ✓ Pasajero modificado")
                        print(f"  {pila.datos[pila.buscar(numero)]}")
        elif op == "7":
            if pila.esta_vacia():
                print("  ⚠ La pila está vacía")
            else:
                numero = leer_entero("  N.º de pasajero a eliminar: ")
                if pila.eliminar_por_numero(numero):
                    print("  ✓ Pasajero eliminado (el orden se mantiene)")
                else:
                    print("  No existe ese pasajero")
        elif op == "8":
            copia = pila.copiar()
            print("  ✓ Copia creada:")
            copia.listar()
        elif op == "9":
            print(f"  Longitud: {pila.longitud()}")
            if pila.esta_vacia():
                print("  La pila está vacía")
            else:
                print("  La pila no está vacía")
        elif op == "C":
            for p in datos_prueba():
                pila.apilar(p)
            print("  ✓ Datos de prueba apilados")
        elif op == "0":
            break
        else:
            print("  Opción no válida")


# ---------------------- MENÚ 2 · COLA ----------------------
def menu_cola():
    while True:
        mostrar_opciones("MENÚ 2 · COLA (FIFO)", "Encolar", "Desencolar", "Ver frente")
        op = input("Opción: ").strip().upper()

        if op == "1":
            pasajero = leer_pasajero()                 # 1. LEER
            if cola.encolar(pasajero):                 # 2. LLAMAR
                print("  ✓ Encolado: está al final")   # 3. MOSTRAR
        elif op == "2":
            cola.listar()
        elif op == "3":
            salio = cola.desencolar()                  # 2. LLAMAR
            if salio is None:                          # 3. MOSTRAR
                print("  ⚠ La cola está vacía")
            else:
                print(f"  ✓ Salió: {salio.nombre}")
                nuevo = cola.ver_frente()
                if nuevo is None:
                    print("  La cola quedó vacía")
                else:
                    print(f"  Nuevo frente: {nuevo.nombre}")
        elif op == "4":
            frente = cola.ver_frente()
            if frente is None:
                print("  ⚠ La cola está vacía")
            else:
                print(f"  Frente: {frente.nombre} ({frente.numero})")
        elif op == "5":
            if cola.esta_vacia():
                print("  ⚠ La cola está vacía")
            else:
                numero = leer_entero("  N.º de pasajero a buscar: ")
                pos = cola.buscar(numero)
                if pos == -1:
                    print("  No existe ese pasajero")
                else:
                    print(f"  Encontrado en [{pos}]: {cola.datos[pos].nombre}")
                    print(f"  {cola.datos[pos]}")
        elif op == "6":
            if cola.esta_vacia():
                print("  ⚠ La cola está vacía")
            else:
                numero = leer_entero("  N.º de pasajero a modificar: ")
                if cola.buscar(numero) == -1:
                    print("  No existe ese pasajero")
                else:
                    destino = leer_destino("  Nuevo destino: ")
                    asiento = leer_asiento("  Nuevo asiento: ")
                    if cola.modificar(numero, destino, asiento):
                        print("  ✓ Pasajero modificado")
                        print(f"  {cola.datos[cola.buscar(numero)]}")
        elif op == "7":
            if cola.esta_vacia():
                print("  ⚠ La cola está vacía")
            else:
                numero = leer_entero("  N.º de pasajero a eliminar: ")
                if cola.eliminar_por_numero(numero):
                    print("  ✓ Pasajero eliminado (el orden se mantiene)")
                else:
                    print("  No existe ese pasajero")
        elif op == "8":
            copia = cola.copiar()
            print("  ✓ Copia creada:")
            copia.listar()
        elif op == "9":
            print(f"  Longitud: {cola.longitud()}")
            if cola.esta_vacia():
                print("  La cola está vacía")
            else:
                print("  La cola no está vacía")
        elif op == "C":
            for p in datos_prueba():
                cola.encolar(p)
            print("  ✓ Datos de prueba encolados")
        elif op == "0":
            break
        else:
            print("  Opción no válida")


# ---------------------- MENÚ PRINCIPAL ----------------------
def main():
    while True:
        print("\n===== TAREA PILAS Y COLAS · PASAJEROS ✈ =====")
        print("1. Menú 1 · Pila")
        print("2. Menú 2 · Cola")
        print("3. Salir")
        op = input("Opción: ").strip()
        if op == "1":
            menu_pila()
        elif op == "2":
            menu_cola()
        elif op == "3":
            print("¡Hasta pronto!")
            break
        else:
            print("Opción no válida")


if __name__ == "__main__":
    main()
