import string


def normalize_key(key: int):
    return key % 26


def shift_alphabet(key: int):
    alphabet = list(string.ascii_uppercase)
    for _ in range(key):
        alphabet.append(alphabet.pop(0))
    return "".join(alphabet)


def encrypt(msg: str, key: int) -> str:
    return msg.translate(
        str.maketrans(string.ascii_uppercase, shift_alphabet(normalize_key(key)))
    )


def decrypt(msg: str, key: int) -> str:
    return msg.translate(
        str.maketrans(shift_alphabet(normalize_key(key)), string.ascii_uppercase)
    )
