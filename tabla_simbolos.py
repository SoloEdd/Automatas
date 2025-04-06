import struct
import os
import re
from afd_identificadores import afd_identificador

# --- Configuración de estructura binaria ---
STRUCT_FORMAT = "20s 10s i"  # nombre, tipo, dirección
RECORD_SIZE = struct.calcsize(STRUCT_FORMAT)

# Ruta del archivo en la misma carpeta que este script
FILE_NAME = os.path.join(os.path.dirname(__file__), "tabla_simbolos.dat")

# --- Lista de palabras reservadas de ejemplo ---
RESERVED_WORDS = [
    "if", "else", "while", "for", "return", "int", "float", "char", "void", "main"
]

# --- Funciones para manejar el archivo de símbolos ---
def crear_archivo():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "wb") as f:
            pass

def agregar_simbolo(nombre, tipo, direccion):
    with open(FILE_NAME, "ab") as f:
        nombre = nombre.encode("utf-8").ljust(20, b'\x00')
        tipo = tipo.encode("utf-8").ljust(10, b'\x00')
        f.write(struct.pack(STRUCT_FORMAT, nombre, tipo, direccion))

def leer_simbolos():
    with open(FILE_NAME, "rb") as f:
        print("--- Tabla de Símbolos ---")
        while True:
            data = f.read(RECORD_SIZE)
            if not data:
                break
            nombre, tipo, direccion = struct.unpack(STRUCT_FORMAT, data)
            print(f"Nombre: {nombre.decode().strip()}, Tipo: {tipo.decode().strip()}, Dirección: {direccion}")

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

# # --- Punto de entrada opcional ---
# if __name__ == "__main__":
#     crear_archivo()
#     for i, palabra in enumerate(RESERVED_WORDS):
#         agregar_simbolo(palabra, "reservada", 1000 + i)

#     codigo_prueba = "int main() { float x = variable1 + variable_2; return x; }"
#     tokenizar(codigo_prueba)
#     leer_simbolos()
