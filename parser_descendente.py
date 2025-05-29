import re

# === TOKENIZADOR BÁSICO ===
def tokenize(code):
    token_spec = [
        ('NUM',      r'\d+'),
        ('ID',       r'[a-zA-Z_]\w*'),
        ('OP',       r'[+\-*/=<>!]=?|==|!='),
        ('LPAREN',   r'\('),
        ('RPAREN',   r'\)'),
        ('LBRACE',   r'\{'),
        ('RBRACE',   r'\}'),
        ('COMMA',    r','),
        ('SEMICOLON',r';'),
        ('SKIP',     r'[ \t\n]+'),
        ('MISMATCH', r'.'),
    ]

    tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_spec)
    tokens = []
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            raise SyntaxError(f'Token inesperado: {value}')
        tokens.append((kind, value))
    return tokens

# === PARSER DESCENDENTE ===
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else (None, None)

    def eat(self, expected_type=None, expected_value=None):
        token = self.current()
        if expected_type and token[0] != expected_type:
            raise SyntaxError(f'Se esperaba tipo {expected_type} y se encontró {token}')
        if expected_value and token[1] != expected_value:
            raise SyntaxError(f'Se esperaba valor "{expected_value}" y se encontró {token}')
        self.pos += 1
        return token

    def programa(self):
        instrucciones = []
        while self.pos < len(self.tokens):
            instrucciones.append(self.instruccion())
        return ('Programa', instrucciones)

    def instruccion(self):
        token = self.current()
        if token[1] == 'var':
            return self.declaracion()
        elif token[0] == 'ID':
            next_tok = self.tokens[self.pos + 1]
            if next_tok[1] == '=':
                return self.asignacion()
            elif next_tok[1] == '(':
                return self.llamada_funcion()
        elif token[1] == 'print':
            return self.impresion()
        elif token[1] == 'if':
            return self.decision()
        elif token[1] == 'while':
            return self.while_()
        elif token[1] == 'for':
            return self.for_()
        elif token[1] == 'func':
            return self.funcion()
        else:
            raise SyntaxError(f'Instrucción no válida: {token}')

    def declaracion(self):
        self.eat(expected_value='var')
        id_ = self.eat('ID')
        self.eat(expected_value='=')
        expr = self.expresion()
        return ('Declaracion', id_[1], expr)

    def asignacion(self):
        id_ = self.eat('ID')
        self.eat(expected_value='=')
        expr = self.expresion()
        return ('Asignacion', id_[1], expr)

    def impresion(self):
        self.eat(expected_value='print')
        expr = self.expresion()
        return ('Impresion', expr)

    def decision(self):
        self.eat(expected_value='if')
        self.eat(expected_value='(')
        cond = self.condicion()
        self.eat(expected_value=')')
        bloque_if = self.bloque()
        if self.current()[1] == 'else':
            self.eat()
            bloque_else = self.bloque()
            return ('IfElse', cond, bloque_if, bloque_else)
        return ('If', cond, bloque_if)

    def while_(self):
        self.eat(expected_value='while')
        self.eat(expected_value='(')
        cond = self.condicion()
        self.eat(expected_value=')')
        bloque = self.bloque()
        return ('While', cond, bloque)

    def for_(self):
        self.eat(expected_value='for')
        self.eat(expected_value='(')
        decl = self.declaracion()
        self.eat(expected_value=';')
        cond = self.condicion()
        self.eat(expected_value=';')
        asign = self.asignacion()
        self.eat(expected_value=')')
        bloque = self.bloque()
        return ('For', decl, cond, asign, bloque)

    def funcion(self):
        self.eat(expected_value='func')
        id_ = self.eat('ID')
        self.eat(expected_value='(')
        params = self.parametros()
        self.eat(expected_value=')')
        bloque = self.bloque()
        return ('Funcion', id_[1], params, bloque)

    def parametros(self):
        if self.current()[0] == 'ID':
            param = self.eat('ID')[1]
            lista = self.lista_parametros()
            return [param] + lista
        return []

    def lista_parametros(self):
        if self.current()[1] == ',':
            self.eat()
            param = self.eat('ID')[1]
            return [param] + self.lista_parametros()
        return []

    def llamada_funcion(self):
        id_ = self.eat('ID')
        self.eat(expected_value='(')
        args = self.argumentos()
        self.eat(expected_value=')')
        return ('LlamadaFuncion', id_[1], args)

    def argumentos(self):
        if self.current()[0] in ('ID', 'NUM', 'LPAREN'):
            arg = self.expresion()
            return [arg] + self.lista_argumentos()
        return []

    def lista_argumentos(self):
        if self.current()[1] == ',':
            self.eat()
            arg = self.expresion()
            return [arg] + self.lista_argumentos()
        return []

    def bloque(self):
        self.eat(expected_value='{')
        prog = self.programa()
        self.eat(expected_value='}')
        return prog

    def condicion(self):
        izq = self.expresion()
        op = self.eat('OP')[1]
        der = self.expresion()
        return ('Condicion', op, izq, der)

    def expresion(self):
        left = self.termino()
        while self.current()[1] in ('+', '-'):
            op = self.eat()[1]
            right = self.termino()
            left = (op, left, right)
        return left

    def termino(self):
        left = self.factor()
        while self.current()[1] in ('*', '/'):
            op = self.eat()[1]
            right = self.factor()
            left = (op, left, right)
        return left

    def factor(self):
        token = self.current()
        if token[1] == '(':
            self.eat()
            expr = self.expresion()
            self.eat(expected_value=')')
            return expr
        elif token[0] == 'NUM':
            return int(self.eat('NUM')[1])
        elif token[0] == 'ID':
            return self.eat('ID')[1]
        else:
            raise SyntaxError(f'Factor no válido: {token}')



if __name__ == "__main__":
    print("Inicio")
    try:
        codigo = 'print 5 + 2'
        tokens = tokenize(codigo)
        parser = Parser(tokens)
        arbol = parser.programa()

        from pprint import pprint
        pprint(arbol)
    except Exception as e:
        print("¡Ocurrió un error durante el análisis!")
        print(e)



