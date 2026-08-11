alphabet = 'abcdefghijklmnopqrstuvwxyz'
alphabet = list(alphabet)


def encrypt(message, key):
    message = list(message)
    encrypted_message = []
    for char in message:
        try: 
            pos = alphabet.index(char)

            encrypted_message.append(key[pos])
        except:
            pass

    return encrypted_message


def decrypt(message, key):
    message = list(message)
    decrypted_message = []
    for char in message:
        try:
            pos = key.index(char)

            decrypted_message.append(alphabet[pos])
        except:
            pass
    
    return decrypted_message
