import random

ALPHABET = "абвгдеёжзийклмнопрстуфхцчшщыьэюя" # "abcdefghijklmnopqrstuvwxyz"

def shift_str(string: str, offset=3):
    res = ""
    for letter in string.lower():
        if letter.isalpha():
            res += ALPHABET[(ALPHABET.find(letter) + offset)  % len(ALPHABET)]
        else:
            res += letter
    return res

def cesar(string):
    return shift_str(string, 300)

def cesar_reverse(string):
    return shift_str(string, -300)

string = "александр орличеня васильевич"

print("cesar")

res = cesar(string)
print(res)
print(cesar_reverse(res))

# макс 3 проги за раз

def reverse_alphabet(string):
    res = ""
    for letter in string.lower():
        if letter.isalpha():
            res += ALPHABET[len(ALPHABET) - ALPHABET.find(letter) - 1]
        else:
            res += letter
    return res

def atbash(string):
    return reverse_alphabet(string)


print("atbash")

res = atbash(string)
print(res)
print(atbash(res))

def kamasutra(string):
    new_alphabet = list(ALPHABET[int(len(ALPHABET) / 2):])
    random.shuffle(new_alphabet)
    new_alphabet = ''.join(new_alphabet)
    for letter in ALPHABET[int(len(ALPHABET) / 2):]:
        new_alphabet += ALPHABET[new_alphabet.find(letter)]

    res = ""
    for letter in string:
        if letter.isalpha():
            res += new_alphabet[ALPHABET.find(letter)]
        else:
            res += letter
    print(ALPHABET)
    print(new_alphabet)
    return {
        "string": res,
        "alphabet": new_alphabet
    }

def kamasutra_reverse(string, alphabet):
    res = ""
    for letter in string:
        if letter.isalpha():
            res += ALPHABET[alphabet.find(letter)]
        else:
            res += letter
    return res

print("kamasutra")

res = kamasutra(string)
print(res)
print(kamasutra_reverse(res["string"], res["alphabet"]))
