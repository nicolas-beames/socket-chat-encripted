class Vegenere:
    def __init__(self):
        self.alphabet = "abcdefghijklmnopqrstuvwxyz"
        self.alphabet_list = list(self.alphabet)
        self.number_rotations = len(self.alphabet_list)

    def encrypt(self, msg: str, key: str) -> list:
        msg_list = list(msg)
        repeated_key = self.key_list(key, len(msg))
        matrices = self.matrice(self.alphabet_list, self.number_rotations)
        
        encrypted_msg = []

        for i in msg_list:
            pos_hor = matrices[0].index(i)
            for j in repeated_key:
                for matrice in matrices:
                    if matrice[0] == j:
                        pos_ver = matrices.index(matrice)
                        repeated_key.pop(0)
                break

            encrypted_msg.append(matrices[pos_ver][pos_hor])

        return "".join(encrypted_msg)

    def decrypt(self, msg:list, key:str) -> list:
        msg_list = list(msg)
        repeated_key = self.key_list(key, len(msg))
        matrices = self.matrice(self.alphabet_list, self.number_rotations)

        decrypted_msg = []

        for i in msg_list:
            for j in repeated_key:
                for matrice in matrices:
                    if j == matrice[0]:
                        pos_hor = matrice.index(i)
                        repeated_key.pop(0)
                break

            decrypted_msg.append(matrices[0][pos_hor])                

        return "".join(decrypted_msg)

    def key_list(self, key:str, msg_size:int) -> list:
        repeated_key = []
        key = list(key)

        counter = 0
        for i in range(msg_size):
            repeated_key.append(key[counter])
            if counter < len(key) -1:
                counter += 1
            else:
                counter = 0

        return repeated_key

    def shift(self, alphabet: list, amount: int) -> list:
        
        alphabet_list = alphabet.copy()

        for i in range(amount):
            alphabet_list.append(alphabet_list.pop(0))

        return alphabet_list

    def matrice(self, alphabet_list:list, number_rotations: int) -> list:
        matrice_list = []

        for i in range(number_rotations):
            matrice_list.append(self.shift(alphabet_list, i))

        return matrice_list


# i = Vegenere()

# enc = i.encrypt("atacarbasenorte", "fogo")

# print(enc)


# print(i.decrypt(enc, "fogo"))