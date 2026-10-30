import os

def _rotl8(x: int, n: int) -> int:
    return ((x << n) | (x >> (8 - n))) & 0xFF

def _generate_sboxes():
    sbox = [0] * 256
    p = q = 1
    while True:
        p = p ^ ((p << 1) & 0xFF) ^ (0x1B if p & 0x80 else 0)
        q ^= (q << 1) & 0xFF
        q ^= (q << 2) & 0xFF
        q ^= (q << 4) & 0xFF
        if q & 0x80:
            q ^= 0x09
        x = q ^ _rotl8(q, 1) ^ _rotl8(q, 2) ^ _rotl8(q, 3) ^ _rotl8(q, 4)
        sbox[p] = x ^ 0x63
        if p == 1:
            break
    sbox[0] = 0x63 

    inv_sbox = [0] * 256
    for i, v in enumerate(sbox):
        inv_sbox[v] = i
    return sbox, inv_sbox

SBOX, INV_SBOX = _generate_sboxes()

def xtime(a: int) -> int:
    a <<= 1
    if a & 0X100:
        a ^= 0x11B
    return a & 0xFF

def gmul(a: int, b: int) -> int:
    resultado = 0
    while b:
        if b & 1:         
            resultado ^= a
        a = xtime(a)      
        b >>= 1
    return resultado


def expandir_chave(chave: bytes):
    if len(chave) != 16:
        return "Chave tem que ser 16 bits!!"

    num_rodadas = 10 
    palavras_totais = 44

    palavras = [list(chave[4 * i:4 * i + 4]) for i in range(4)]

    rcon = 0x01

    for i in range(4, palavras_totais):
        temp = palavras[i - 1][:]
        if i % 4 == 0:
            temp = temp[1:] + temp[:1]
            temp = [SBOX[b] for b in temp]
            temp[0] ^= rcon
            rcon = xtime(rcon)
        palavras.append([a ^ b for a, b in zip(palavras[i - 4], temp)])

    chave_rodada = []
    for rodada in range(num_rodadas + 1):
        rk = []
        for palavra in palavras[4 * rodada:4 * rodada + 4]:
            rk.extend(palavra)
        chave_rodada.append(rk)
    return chave_rodada, num_rodadas

def adicionar_chave_rodada(estado, chave_rodada):
    return [s ^ k for s, k in zip(estado, chave_rodada)]

def sub_bytes(estado):
    return [SBOX[b] for b in estado]

def inv_sub_bytes(estado):
    return [INV_SBOX[b] for b in estado]

def mover_coluna(estado):
    out = [0] * 16
    for r in range(4):
        for c in range(4):
            out[r + 4 * c] = estado[r + 4 * ((c + r) % 4)]
    return out

def inv_mover_coluna(estado):
    out = [0] * 16
    for r in range(4):
        for c in range(4):
            out[r + 4 * ((c + r) % 4)] = estado[r + 4 * c]
    return out

def misturar_colunas(estado):
    out = [0] * 16
    for c in range(4):
        a0, a1, a2, a3 = estado[4 * c:4 * c + 4]
        out[4 * c + 0] = gmul(a0, 2) ^ gmul(a1, 3) ^ a2 ^ a3
        out[4 * c + 1] = a0 ^ gmul(a1, 2) ^ gmul(a2, 3) ^ a3
        out[4 * c + 2] = a0 ^ a1 ^ gmul(a2, 2) ^ gmul(a3, 3)
        out[4 * c + 3] = gmul(a0, 3) ^ a1 ^ a2 ^ gmul(a3, 2)
    return out

def inv_misturar_colunas(estado):
    out = [0] * 16
    for c in range(4):
        a0, a1, a2, a3 = estado[4 * c:4 * c + 4]
        out[4 * c + 0] = gmul(a0, 14) ^ gmul(a1, 11) ^ gmul(a2, 13) ^ gmul(a3, 9)
        out[4 * c + 1] = gmul(a0, 9) ^ gmul(a1, 14) ^ gmul(a2, 11) ^ gmul(a3, 13)
        out[4 * c + 2] = gmul(a0, 13) ^ gmul(a1, 9) ^ gmul(a2, 14) ^ gmul(a3, 11)
        out[4 * c + 3] = gmul(a0, 11) ^ gmul(a1, 13) ^ gmul(a2, 9) ^ gmul(a3, 14)
    return out

def encriptar_bloco(bloco: bytes, chave_rodada, num_rodadas: int) -> bytes:
    estado = adicionar_chave_rodada(list(bloco), chave_rodada[0])

    for r in range(1, num_rodadas):
        estado = sub_bytes(estado)
        estado = mover_coluna(estado)
        estado = misturar_colunas(estado)
        estado = adicionar_chave_rodada(estado, chave_rodada[r])
    estado = sub_bytes(estado)
    estado = mover_coluna(estado)
    estado = adicionar_chave_rodada(estado, chave_rodada[num_rodadas])

    return bytes(estado)

def decriptar_bloco(bloco: bytes, chave_rodada, num_rodadas: int) -> bytes:
    estado = adicionar_chave_rodada(list(bloco), chave_rodada[num_rodadas])

    for r in range(num_rodadas - 1, 0, -1):          
        estado = inv_mover_coluna(estado)
        estado = inv_sub_bytes(estado)
        estado = adicionar_chave_rodada(estado, chave_rodada[r])
        estado = inv_misturar_colunas(estado)

    estado = inv_mover_coluna(estado)
    estado = inv_sub_bytes(estado)
    estado = adicionar_chave_rodada(estado, chave_rodada[0])  

    return bytes(estado)

def pad(data: bytes) -> bytes:
    n = 16 - (len(data) % 16)
    return data + bytes([n]) * n

def unpad(data: bytes) -> bytes:
    if not data or len(data) % 16 != 0:
        raise ValueError("Dados com tamanho invalido.")
    n = data[-1]
    if n < 1 or n > 16 or data[-n:] != bytes([n]) * n:
        raise ValueError("padding invalido")
    return data[:-n]

def encriptar(texto: bytes, chave: bytes) -> bytes:
    chave_rodada, num_rodadas = expandir_chave(chave)
    data = pad(texto)
    texto_cifrado = bytearray()
    for i in range(0, len(data), 16):
        texto_cifrado += encriptar_bloco(data[i:i + 16], chave_rodada, num_rodadas)

    return bytes(texto_cifrado)

def decriptar(texto_cifrado: bytes, chave: str) -> bytes:
    chave = chave.encode("utf-8")
    if len(texto_cifrado) == 0 or len(texto_cifrado) % 16 != 0:
        raise ValueError("Tamanho de texto cifrado invalido!!")
    chave_rodada, num_rodadas = expandir_chave(chave)
    texto = bytearray()
    for i in range(0, len(texto_cifrado), 16):
        texto += decriptar_bloco(texto_cifrado[i:i + 16], chave_rodada, num_rodadas)

    return unpad(bytes(texto))

def encode_encriptar(texto: str, chave: str):
    return encriptar(texto.encode("utf-8"), chave.encode("utf-8"))


if __name__ == "__main__":
    pass 

    message = "ABCDEFGHIJKLMNOP"
    key_str = "1234567890ABCDEF"

    cifrado = encode_encriptar(message, key_str)

    print(f'cifrado = {cifrado[:len(message)].hex().upper()} \n decriptado = {decriptar(cifrado, key_str)}')
