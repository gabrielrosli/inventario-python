
# Sistema de Inventario de Chapas

Este es un sistema de inventario para chapas, implementado en Python con SQLite y la librería Colorama para una salida colorida en consola.

## Descripción General

El código permite gestionar un inventario de chapas con los siguientes datos:

- **Item**: Nombre o código del item. Admite cualquier tipo de datos ingresados
- **Largo**: Medida en milímetros del largo de la chapa. Admite valores enteros mayores a 0
- **Ancho**: Medida en milímetros del ancho de la chapa. Admite valores enteros mayores a 0
- **Espesor**: Medida en milímetros del espesor de la chapa. Admite valores flotantes mayores a 0
- **Grado**: Grado del material de la chapa. Admite cualquier tipo de datos ingresados
- **Cantidad**: Número de chapas disponibles en el inventario. Admite valores enteros mayores a 0

### Funcionalidades:

1. **Agregar chapa al inventario**: Permite ingresar un nuevo item con sus datos correspondientes, siempre validando las entradas y verificando si el item ya existe en el inventario.
   
2. **Mostrar inventario de chapas**: Muestra todos los items registrados en el inventario con sus respectivas características (largo, ancho, espesor, grado y cantidad).

3. **Buscar chapa en el inventario**: Permite buscar chapas según varios criterios:
   - Item
   - Largo
   - Ancho
   - Espesor
   - Grado

4. **Actualizar cantidad de un item**: Permite incrementar o reducir la cantidad de un item en el inventario, asegurándose de que no haya cantidades negativas.

5. **Eliminar un item**: Permite eliminar completamente un item del inventario, verificando previamente que existe dicho item en la base de datos

6. **Mostrar items con bajo stock**: Muestra los items cuyo stock esté por debajo de un umbral definido por el usuario.

7. **Salir**: Cierra el sistema.

## Explicación del Código

### 1. Base de Datos

Se utiliza SQLite para gestionar el inventario. La base de datos se guarda en un archivo llamado `inventario_chapas.db`. Si la base de datos o la tabla no existen, el código las crea automáticamente.

### 2. Función `validar_entrada()`

Es una función genérica que asegura que la entrada del usuario sea válida y que cumpla con las condiciones específicas. Si la entrada no es válida, muestra un mensaje de error y solicita una nueva entrada.

- **Parámetros**:
  - `mensaje`: El texto que se muestra al usuario.
  - `tipo`: El tipo esperado para la entrada (int, float, etc.).
  - `condicion`: Una función lambda que valida la entrada (por ejemplo, si el valor es positivo).

### 3. Funciones principales:

- **`agregar_chapa()`**: 
  - Solicita los datos de la chapa y los inserta en la base de datos, siempre validando los datos.
  
- **`mostrar_inventario()`**: 
  - Recupera todos los items de la base de datos y los muestra en consola.

- **`buscar_chapa()`**: 
  - Permite buscar chapas según varios criterios (item, largo, ancho, espesor, grado).
  - Utiliza consultas SQL dinámicas basadas en el tipo de búsqueda seleccionada.

- **`actualizar_cantidad()`**: 
  - Permite modificar la cantidad de un item específico en el inventario. Si la cantidad es negativa después de la actualización, muestra un error.

-**`eliminar_chapa()`**:
  - Permite eliminar un item completamente del inventario, solicita al usuario confirmacion para la eliminacion de dicho item. Si el item no existe muestra un mensaje de error. 

- **`bajo_stock()`**: 
  - Muestra los items cuyo stock esté por debajo de un umbral definido por el usuario.

### 4. Menú Principal

El programa muestra un menú con las opciones de las funcionalidades. El usuario debe ingresar el número correspondiente a la acción que desea realizar.

### 5. Validación de Entradas

En todas las interacciones con el usuario, el código valida la entrada para evitar errores. Esto se realiza mediante la función `validar_entrada()`, que garantiza que los datos ingresados sean del tipo adecuado y cumplan con las condiciones necesarias.

## Sugerencias

- **Mejorar la interfaz de usuario**: Aunque el sistema es funcional, la interacción con el usuario podría mejorarse, como por ejemplo con una interfaz gráfica.
  
- **Manejo de excepciones en la base de datos**: Si la base de datos no se puede abrir o hay un problema con las consultas, el sistema debería manejar estos errores y proporcionar un mensaje adecuado al usuario.
  
- **Optimización de consultas SQL**: Para operaciones de búsqueda o actualización, se podrían optimizar las consultas SQL, especialmente si la base de datos crece considerablemente en tamaño.

- **Respaldo de base de datos**: Sería útil implementar un sistema de respaldo para evitar la pérdida de datos en caso de que algo falle en la conexión o el archivo de base de datos.

## Uso:

1. Ejecuta el código en tu terminal.
2. Interactúa con el sistema seleccionando las opciones del menú.
3. Los resultados y mensajes de error se muestran en colores utilizando la librería `colorama` para mejorar la visibilidad.

## Requisitos:

- Python 3.x
- Biblioteca `colorama` (se puede instalar con: `pip install colorama`)
- SQLite (viene preinstalado con Python)

"""


