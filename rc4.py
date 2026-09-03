def to_ascii_list(plain_text: str) -> list[int]:
    byte_data = plain_text.encode("latin-1", errors="replace")
    ascii_values = [byte for byte in byte_data]
    return ascii_values


def from_ascii_list(ascii_values: list[int]) -> str:
    text_string = bytes(ascii_values).decode("latin-1")
    return text_string


def encrypt(message: str, key: str) -> str:
    S = list(range(256))
    key_ascii = to_ascii_list(key)
    T = [key_ascii[i % len(key)] for i, _ in enumerate(range(256))]

    j = 0
    for i in range(256):
        j = (j + S[i] + T[i]) % 256
        S[i], S[j] = S[j], S[i]

    k = [0] * len(message)
    i, j = 0, 0
    for l in range(len(message)):
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        t = (S[i] + S[j]) % 256
        k[l] = S[t]

    k = bytes(k)
    p = message.encode("latin-1", errors="replace")

    encrypted_message = bytes(a ^ b for a, b in zip(k, p))
    ascii_values = [byte for byte in encrypted_message]
    # print(ascii_values)
    encrypted_message = from_ascii_list(ascii_values)

    return encrypted_message


def decrypt(message: str, key: str) -> str:
    return encrypt(message, key)
