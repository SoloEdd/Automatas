import re
from tabla_simbolos import crear_archivo, agregar_simbolo, leer_simbolos, es_identificador

RESERVED_WORDS = {"if", "else", "while", "int", "float", "return", "main", "def"}
direccion_base = 2000

# --- Tokenizar (Lexer) ---
def tokenizar(codigo):
    tokens = re.findall(r"(==|!=|<=|>=|[()\{\},;=+\-*/<>]|\w+)", codigo)
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
        nombre_var = obtener_token()
        if not es_identificador(nombre_var):
            raise SyntaxError(f"Nombre de variable inválido: {nombre_var}")
        match(nombre_var)
        
        # Parte opcional de inicialización
        if obtener_token() == "=":
            match("=")
            parse_expresion()
            
        match(";")
    else:
        raise SyntaxError("Se esperaba tipo de variable (int/float/bool)")
    
def parse_funcion():
    match("def")
    nombre_funcion = obtener_token()
    if not es_identificador(nombre_funcion):
        raise SyntaxError(f"Nombre de función inválido: {nombre_funcion}")
    match(nombre_funcion)
    match("(")
    parse_parametros()
    match(")")
    parse_bloque() 

def parse_parametros():
    token = obtener_token()
    if token != ")":  # Si no hay parámetros
        if not es_identificador(token):
            raise SyntaxError(f"Identificador de parámetro inválido: {token}")
        match(token)
        while obtener_token() == ",":
            match(",")
            token = obtener_token()
            if not es_identificador(token):
                raise SyntaxError(f"Identificador de parámetro inválido: {token}")
            match(token)

def parse_bloque():
    match("{")
    parse_sentencias()
    match("}")

def parse_sentencias():
    while obtener_token() not in {"}", None}:
        parse_sentencia()

def parse_sentencia():
    token = obtener_token()
    if token in {"int", "float", "bool"}:
        parse_declaracion()
    elif token == "if":
        parse_decision()
    elif token == "while":
        parse_while()
    elif token == "for":
        parse_for()
    elif es_identificador(token):
        siguiente = tokens[indice + 1] if indice + 1 < len(tokens) else None
        if siguiente == "=":
            parse_asignacion()
        else:
            parse_expresion()
            match(";")
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
    parse_bloque()
    if obtener_token() == "else":
        match("else")
        parse_bloque()

def parse_while():
    match("while")
    match("(")
    parse_condicion()
    match(")")
    parse_bloque()

def parse_for():
    match("for")
    match("(")
    parse_declaracion()
    parse_condicion()
    match(";")
    parse_asignacion()
    match(")")
    parse_bloque()

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
    if token in {"==", "!=", ">", "<", ">=", "<="}:
        match(token)
        parse_expresion()
    else:
        raise SyntaxError(f"Se esperaba un comparador (==, !=, >, <) y se encontró '{token}'")

def analizar_sintaxis(codigo):
    global tokens, indice
    tokens = tokenizar(codigo)
    print("Tokens:", tokens)
    indice = 0
    parse_programa()
    if obtener_token() is not None:
        raise SyntaxError("Código inválido: tokens adicionales encontrados.")
    return "Análisis sintáctico exitoso"
