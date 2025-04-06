# AFD para reconocer identificadores válidos

def afd_identificador(cadena):
    estado = 0
    for c in cadena:
        if estado == 0:
            if c.isalpha() or c == '_':
                estado = 1
            else:
                return False
        elif estado == 1:
            if c.isalnum() or c == '_':
                continue
            else:
                return False
    return estado == 1
