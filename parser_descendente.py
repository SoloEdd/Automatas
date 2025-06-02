import re
from tabla_simbolos import crear_archivo, agregar_simbolo, leer_simbolos, es_identificador

RESERVED_WORDS = {"if", "else", "while", "int", "float", "return", "main"}
direccion_base = 2000

# --- Tokenizar (Lexer) ---
def tokenizar(codigo):
    tokens = re.findall(r"(==|!=|<=|>=|[()\{\};=+\-*/<>]|\w+)", codigo)
    pos = 0
    for token in tokens:
        if es_identificador(token) and token not in RESERVED_WORDS:
            agregar_simbolo(token, "id", 2000 + pos)
            pos += 1
    return tokens

# --- Parser (descendente recursivo) ---
tokens = []
indice = 0

def obtener_token():
    global indice
    if indice < len(tokens):
        return tokens[indice]
    return None

def match(esperado):
    global indice
    if obtener_token() == esperado:
        indice += 1
    else:
        raise SyntaxError(f"Error: Se esperaba '{esperado}' y se encontró '{obtener_token()}'")

def parse_programa():
    while obtener_token() in {"int", "float", "bool"}:
        parse_declaracion()
    while obtener_token() == "def":
        parse_funcion()
    parse_sentencias()

def parse_declaracion():
    tipo = obtener_token()
    if tipo in {"int", "float", "bool"}:
        match(tipo)
        match(obtener_token())  # id
        match(";")
    else:
        raise SyntaxError("Se esperaba tipo de variable")
    
def parse_funcion():
    match("def")
    match(obtener_token())  # nombre de la función
    match("(")
    match(")")
    match("{")
    parse_sentencias()
    match("}")

def parse_sentencias():
    while obtener_token() in {"if", "while", "for"} or es_identificador(obtener_token()):
        parse_sentencia()

def parse_sentencia():
    token = obtener_token()
    if token == "if":
        parse_decision()
    elif token == "while":
        parse_while()
    elif token == "for":
        parse_for()
    elif es_identificador(token):
        parse_asignacion()
    else:
        raise SyntaxError(f"Sentencia no válida: {token}")


def parse_asignacion():
    match(obtener_token())
    match("=")
    parse_expresion()
    match(";")

def parse_decision():
    match("if")
    match("(")
    parse_condicion()
    match(")")
    match("{")
    parse_sentencias()
    match("}")
    if obtener_token() == "else":
        match("else")
        match("{")
        parse_sentencias()
        match("}")

def parse_while():
    match("while")
    match("(")
    parse_condicion()
    match(")")
    match("{")
    parse_sentencias()
    match("}")

def parse_for():
    match("for")
    match("(")
    parse_asignacion()
    parse_condicion()
    match(";")
    parse_asignacion()
    match(")")
    match("{")
    parse_sentencias()
    match("}")

def parse_expresion():
    token = obtener_token()
    if es_identificador(token) or token.isdigit():
        match(token)
        while obtener_token() in {"+", "-"}:
            match(obtener_token())
            token2 = obtener_token()
            if es_identificador(token2) or token2.isdigit():
                match(token2)
            else:
                raise SyntaxError(f"Expresión inválida: se esperaba identificador o número, se encontró '{token2}'")
    else:
        raise SyntaxError(f"Expresión inválida: se esperaba identificador o número, se encontró '{token}'")

def parse_condicion():
    parse_expresion()
    token = obtener_token()
    if token in {"==", "!=", ">", "<"}:
        match(token)
        parse_expresion()
    else:
        raise SyntaxError(f"Se esperaba un comparador (==, !=, >, <) y se encontró '{token}'")

def analizar_sintaxis(codigo):
    global tokens, indice
    tokens = tokenizar(codigo)
    indice = 0
    parse_programa()
    if obtener_token() is not None:
        raise SyntaxError("Código inválido: tokens adicionales encontrados.")
    return "Análisis sintáctico exitoso"
