import struct
import os
import re
from afd_identificadores import afd_identificador

# --- Configuración de estructura binaria ---
STRUCT_FORMAT = "20s 10s i"  # nombre, tipo, dirección
RECORD_SIZE = struct.calcsize(STRUCT_FORMAT)
TABLE_SIZE = 20000
# Ruta del archivo en la misma carpeta que este script
FILE_NAME = os.path.join(os.path.dirname(__file__), "tabla_simbolos.dat")

# --- Función hash (DJB2) ---
def hash_djb2(token):
    hash_value = 5381
    for c in token:
        hash_value = ((hash_value << 5) + hash_value) + ord(c)
    return hash_value % TABLE_SIZE

# --- Lista de palabras reservadas de ejemplo ---
RESERVED_WORDS = [
    "if", "else", "while", "for", "return", "int", "float", "char", "void", "main"
]

# --- Crear archivo tabla de símbolos ---
def crear_archivo():
    with open(FILE_NAME, "wb") as f:
        empty_record = struct.pack(STRUCT_FORMAT, b'\x00'*20, b'\x00'*10, 0)
        for _ in range(TABLE_SIZE):
            f.write(empty_record)


# --- Insertar token con manejo de colisiones ---
def agregar_simbolo(nombre, tipo, direccion):
    index = hash_djb2(nombre)
    with open(FILE_NAME, "rb+") as f:
        for i in range(TABLE_SIZE):
            pos = (index + i) % TABLE_SIZE
            f.seek(pos * RECORD_SIZE)
            data = f.read(RECORD_SIZE)
            if data != b'\x00' * RECORD_SIZE:
                nombre_guardado, tipo_guardado, _ = struct.unpack(STRUCT_FORMAT, data)
                if nombre_guardado.decode().strip() == nombre:
                    # Ya está registrado, no lo insertes otra vez
                    return
            else:
                # Espacio vacío, insertar
                f.seek(pos * RECORD_SIZE)
                nombre_p = nombre.encode("utf-8").ljust(20, b'\x00')
                tipo_p = tipo.encode("utf-8").ljust(10, b'\x00')
                f.write(struct.pack(STRUCT_FORMAT, nombre_p, tipo_p, direccion))
                return
        print(f"Error: Tabla de símbolos llena para {nombre}")

# --- Leer tabla de símbolos ---
def leer_simbolos(add_error_message=None):
    try:
        with open(FILE_NAME, "rb") as f:
            for i in range(TABLE_SIZE):
                data = f.read(RECORD_SIZE)
                if not data or len(data) < RECORD_SIZE or data == b'\x00' * RECORD_SIZE:
                    continue
                nombre, tipo, direccion = struct.unpack(STRUCT_FORMAT, data)
                mensaje = f"Pos {i} - Nombre: {nombre.decode().strip()}, Tipo: {tipo.decode().strip()}, Dir: {direccion}"

                if add_error_message:
                    add_error_message(mensaje)
                else:
                    print(mensaje)
    except Exception as e:
        if add_error_message:
            add_error_message(f"Error en leer_simbolos: {str(e)}")
        else:
            print(f"Error en leer_simbolos: {str(e)}")

# --- Función para tokenizar código fuente y agregar identificadores ---
def tokenizar(codigo):
    tokens = re.findall(r"\w+|\S", codigo)
    print("\n--- Tokens ---")
    direccion_base = 2000  # Base para direcciones de identificadores
    identificadores_agregados = 0
    for token in tokens:
        print(token)
        if afd_identificador(token) and token not in RESERVED_WORDS:
            agregar_simbolo(token, "id", direccion_base + identificadores_agregados)
            identificadores_agregados += 1
    return tokens

# --- Verificar identificador válido (AFD simple) ---
def es_identificador(cadena):
    if not cadena or not (cadena[0].isalpha() or cadena[0] == '_'):
        return False
    return all(c.isalnum() or c == '_' for c in cadena)
# # --- Punto de entrada opcional ---
# if __name__ == "__main__":
#     crear_archivo()
#     for i, palabra in enumerate(RESERVED_WORDS):
#         agregar_simbolo(palabra, "reservada", 1000 + i)

#     codigo_prueba = "int main() { float x = variable1 + variable_2; return x; }"
#     tokenizar(codigo_prueba)
#     leer_simbolos()
