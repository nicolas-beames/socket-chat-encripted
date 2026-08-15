VALID_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def normalize_key(key: str):
    return "".join(
        char
        for char in "".join(dict.fromkeys(key)).split()[0].upper().replace("J", "I")
        if char in VALID_LETTERS
    )


def create_digraphs(message: str):
    normalized_message = message.upper().replace("J", "I").replace(" ", "")
    digraphs = []
    i = 0
    while i < len(normalized_message):
        if i + 1 == len(normalized_message):
            digraphs.append([normalized_message[i], "X"])
            break

        if normalized_message[i] == normalized_message[i + 1]:
            digraphs.append([normalized_message[i], "X"])
            i += 1
            continue

        digraphs.append([normalized_message[i], normalized_message[i + 1]])
        i += 2

    return digraphs


def create_matrix(key: str):
    normalized_key = normalize_key(key)
    normalized_key = f"{normalized_key}{VALID_LETTERS.replace("J", "")}"
    normalized_key = "".join(dict.fromkeys(normalized_key))
    return [
        list(normalized_key[0:5]),
        list(normalized_key[5:10]),
        list(normalized_key[10:15]),
        list(normalized_key[15:20]),
        list(normalized_key[20:]),
    ]


class Playfair:

    @staticmethod
    def encode(message: str, key: str):
        digraphs = create_digraphs(message)
        matrix = create_matrix(key)
        encoded_message = ""

        for digraph in digraphs:
            pos1 = 0, 0
            pos2 = 0, 0
            for i, line in enumerate(matrix):
                for j, item in enumerate(line):
                    if item == digraph[0]:
                        pos1 = i, j
                    if item == digraph[1]:
                        pos2 = i, j

            if pos1[0] == pos2[0]:
                pos1 = pos1[0], (pos1[1] + 1) if pos1[1] < 4 else 0
                pos2 = pos2[0], (pos2[1] + 1) if pos2[1] < 4 else 0
            elif pos1[1] == pos2[1]:
                pos1 = (pos1[0] + 1) if pos1[0] < 4 else 0, pos1[1]
                pos2 = (pos2[0] + 1) if pos2[0] < 4 else 0, pos2[1]
            else:
                encoded_message = f"{encoded_message}{matrix[pos1[0]][pos2[1]]}{matrix[pos2[0]][pos1[1]]}"
                continue

            encoded_message = (
                f"{encoded_message}{matrix[pos1[0]][pos1[1]]}{matrix[pos2[0]][pos2[1]]}"
            )

        return encoded_message

    @staticmethod
    def decode(message: str, key: str):
        digraphs = create_digraphs(message)
        matrix = create_matrix(key)
        decoded_message = ""

        for digraph in digraphs:
            pos1 = 0, 0
            pos2 = 0, 0
            for i, line in enumerate(matrix):
                for j, item in enumerate(line):
                    if item == digraph[0]:
                        pos1 = i, j
                    if item == digraph[1]:
                        pos2 = i, j

            if pos1[0] == pos2[0]:
                pos1 = pos1[0], (pos1[1] - 1) if pos1[1] > 0 else 4
                pos2 = pos2[0], (pos2[1] - 1) if pos2[1] > 0 else 4
            elif pos1[1] == pos2[1]:
                pos1 = (pos1[0] - 1) if pos1[0] > 0 else 4, pos1[1]
                pos2 = (pos2[0] - 1) if pos2[0] > 0 else 4, pos2[1]
            else:
                decoded_message = f"{decoded_message}{matrix[pos1[0]][pos2[1]]}{matrix[pos2[0]][pos1[1]]}"
                continue

            encoded_message = (
                f"{decoded_message}{matrix[pos1[0]][pos1[1]]}{matrix[pos2[0]][pos2[1]]}"
            )

        return decoded_message
