class CaesarCypher:

    max_value = 1114111

    @staticmethod
    def encrypt(msg: str, key: int) -> str:
        ascii_msg = list(map(ord, msg))
        ascii_msg = list(map(lambda x: (x + key) % CaesarCypher.max_value, ascii_msg))
        msg = "".join(map(chr, ascii_msg))
        return msg

    @staticmethod
    def decrypt(msg: str, key: int) -> str:
        ascii_msg = list(map(ord, msg))
        ascii_msg = list(map(lambda x: (x - key) % CaesarCypher.max_value, ascii_msg))
        msg = "".join(map(chr, ascii_msg))
        return msg
