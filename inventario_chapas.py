import sqlite3
from colorama import Fore, Style, Back

# Crear o conectar a la base de datos
conexion = sqlite3.connect('inventario_chapas.db')
cursor = conexion.cursor()

# Crear la tabla si no existe
cursor.execute('''
CREATE TABLE IF NOT EXISTS inventario (
    item TEXT PRIMARY KEY,
    largo INTEGER,
    ancho INTEGER,
    espesor REAL,
    grado TEXT,
    cantidad INTEGER
)
''')
conexion.commit()

def validar_entrada(mensaje, tipo=int, condicion=lambda x: True):
    while True:
        try:
            entrada = tipo(input(mensaje))
            if condicion(entrada):
                return entrada
            else:
                print(Fore.RED + "Error: Entrada no válida, no cumple con las condiciones especificadas." + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + "Error: Entrada no válida, asegúrese de ingresar un valor correcto." + Style.RESET_ALL)

def agregar_chapa():
    item = input("Ingrese el nombre o código del item: ")

    # Verificar si el ítem ya está en la base de datos
    cursor.execute("SELECT * FROM inventario WHERE item = ?", (item,))
    if cursor.fetchone():
        print(Fore.RED + "El item ya se encuentra en el inventario. Utiliza la opción 4 para actualizar." + Style.RESET_ALL)
        return

    largo = validar_entrada("Ingrese el largo de la chapa (en mm): ", int, lambda x: x > 0)
    ancho = validar_entrada("Ingrese el ancho de la chapa (en mm): ", int, lambda x: x > 0)
    espesor = validar_entrada("Ingrese el espesor de la chapa (en mm): ", float, lambda x: x > 0)
    grado = input("Ingrese el grado de la chapa: ")
    cantidad = validar_entrada("Ingrese la cantidad de chapas disponibles: ", int, lambda x: x > 0)

    cursor.execute('''
    INSERT INTO inventario (item, largo, ancho, espesor, grado, cantidad)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (item, largo, ancho, espesor, grado, cantidad))
    conexion.commit()
    print(Fore.GREEN + f"Chapa item '{item}' agregada con éxito." + Style.RESET_ALL)

def mostrar_inventario():
    cursor.execute("SELECT * FROM inventario")
    chapas = cursor.fetchall()
    if chapas:
        print(Fore.GREEN + "\nInventario de Chapas:" + Style.RESET_ALL)
        for chapa in chapas:
            print(f"Item: {chapa[0]}, Largo: {chapa[1]} mm, Ancho: {chapa[2]} mm, Espesor: {chapa[3]} mm, Grado: {chapa[4]}, Cantidad: {chapa[5]}")
    else:
        print(Fore.RED + "El inventario de chapas está vacío." + Style.RESET_ALL)

def buscar_chapa():
    print("\nOpciones de búsqueda:")
    print("1. Buscar por item")
    print("2. Buscar por largo")
    print("3. Buscar por ancho")
    print("4. Buscar por espesor")
    print("5. Buscar por grado")
    opcion_busqueda = input("Seleccione una opción de búsqueda: ")

    campo = None
    valor = None

    if opcion_busqueda == "1":
        campo = "item"
        valor = input("Ingrese el nombre o código del item: ")
    elif opcion_busqueda == "2":
        campo = "largo"
        valor = validar_entrada("Ingrese el largo de la chapa (en mm): ", int, lambda x: x > 0)
    elif opcion_busqueda == "3":
        campo = "ancho"
        valor = validar_entrada("Ingrese el ancho de la chapa (en mm): ", int, lambda x: x > 0)
    elif opcion_busqueda == "4":
        campo = "espesor"
        valor = validar_entrada("Ingrese el espesor de la chapa (en mm): ", float, lambda x: x > 0)
    elif opcion_busqueda == "5":
        campo = "grado"
        valor = input("Ingrese el grado de la chapa: ")
    else:
        print(Fore.RED + "Opción no válida." + Style.RESET_ALL)
        return

    # Conversión explícita de tipos para evitar errores en la consulta SQL
    if campo in ["largo", "ancho"]:
        valor = int(valor)
    elif campo == "espesor":
        valor = float(valor)

    cursor.execute(f"SELECT * FROM inventario WHERE {campo} = ?", (valor,))
    resultados = cursor.fetchall()

    if resultados:
        print(Fore.GREEN + "\nResultados de búsqueda:" + Style.RESET_ALL)
        for chapa in resultados:
            print(f"Item: {chapa[0]}, Largo: {chapa[1]} mm, Ancho: {chapa[2]} mm, Espesor: {chapa[3]} mm, Grado: {chapa[4]}, Cantidad: {chapa[5]}")
    else:
        print(Fore.RED + "No se encontraron chapas que coincidan con los criterios de búsqueda." + Style.RESET_ALL)

def actualizar_cantidad():
    item = input("Ingrese el nombre o código del item para actualizar su cantidad: ")
    cursor.execute("SELECT cantidad FROM inventario WHERE item = ?", (item,))
    resultado = cursor.fetchone()

    if resultado:
        cantidad_actual = resultado[0]
        print(f"Cantidad actual de item '{item}': {cantidad_actual}")
        ajuste = validar_entrada("Ingrese el número de chapas a agregar (positivo) o quitar (negativo): ", int, lambda x: True)

        nueva_cantidad = cantidad_actual + ajuste

        if nueva_cantidad < 0:
            print(Fore.RED + "Error: La cantidad no puede ser negativa. Operación cancelada." + Style.RESET_ALL)
        else:
            cursor.execute("UPDATE inventario SET cantidad = ? WHERE item = ?", (nueva_cantidad, item))
            conexion.commit()
            print(Fore.GREEN + f"Cantidad de item '{item}' actualizada a {nueva_cantidad}." + Style.RESET_ALL)
    else:
        print(Fore.RED + f"No se encontró el item '{item}' en el inventario." + Style.RESET_ALL)
        
def eliminar_chapa():
    item = input("Ingrese el nombre o código del item a eliminar: ")

    # Verificar si el ítem existe en el inventario
    cursor.execute("SELECT * FROM inventario WHERE item = ?", (item,))
    if cursor.fetchone():
        # Preguntar al usuario si está seguro de querer eliminar el ítem
        confirmacion = input(f"¿Está seguro de que desea eliminar el item '{item}'? (s/n): ").lower()
        
        if confirmacion == 's':
            cursor.execute("DELETE FROM inventario WHERE item = ?", (item,))
            conexion.commit()
            print(Fore.GREEN + f"El item '{item}' ha sido eliminado con éxito." + Style.RESET_ALL)
        else:
            print(Fore.YELLOW + "Eliminación cancelada." + Style.RESET_ALL)
    else:
        print(Fore.RED + f"No se encontró el item '{item}' en el inventario." + Style.RESET_ALL)



def bajo_stock(umbral_stock):
    cursor.execute("SELECT * FROM inventario WHERE cantidad < ?", (umbral_stock,))
    resultados = cursor.fetchall()

    if resultados:
        print(Fore.RED + f"\nItems con stock por debajo de {umbral_stock}:" + Style.RESET_ALL)
        for chapa in resultados:
            print(Fore.RED + f"Item: {chapa[0]}, Largo: {chapa[1]} mm, Ancho: {chapa[2]} mm, Espesor: {chapa[3]} mm, Grado: {chapa[4]}, Cantidad: {chapa[5]}" + Style.RESET_ALL)
    else:
        print(Fore.GREEN + f"No hay items con stock por debajo de {umbral_stock}." + Style.RESET_ALL)

# Menú principal
while True:
    print(Fore.MAGENTA +"\nSistema de Inventario de Chapas" + Style.RESET_ALL)
    print(Fore.CYAN +"\n1. Agregar chapa al inventario"+ Style.RESET_ALL)
    print(Fore.CYAN +"2. Mostrar inventario de chapas"+ Style.RESET_ALL)
    print(Fore.CYAN +"3. Buscar chapa en el inventario"+ Style.RESET_ALL)
    print(Fore.CYAN +"4. Actualizar cantidad de un item"+ Style.RESET_ALL)
    print(Fore.CYAN +"5. Eliminar un item"+ Style.RESET_ALL)
    print(Fore.CYAN +"6. Mostrar items con bajo stock"+ Style.RESET_ALL)
    print(Fore.CYAN +"7. Salir"+ Style.RESET_ALL)

    opcion = input(Fore.GREEN + "\nSeleccione una opción: "+ Style.RESET_ALL)

    if opcion == "1":
        agregar_chapa()
    elif opcion == "2":
        mostrar_inventario()
    elif opcion == "3":
        buscar_chapa()
    elif opcion == "4":
        actualizar_cantidad()
    elif opcion == "5":
        eliminar_chapa()  
    elif opcion == "6":
        umbral = validar_entrada("Ingrese el umbral de bajo stock: ", int, lambda x: x > 0)
        bajo_stock(umbral)
    elif opcion == "7":
        print(Fore.RED + "\nSaliendo del sistema." + Style.RESET_ALL)
        break
    else:
        print(Fore.RED + "\nOpción no válida. Intente de nuevo." + Style.RESET_ALL)


# Cerrar la conexión a la base de datos al finalizar
conexion.close()
