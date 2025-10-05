import random

# rsa

def mcd(n1: int, n2: int):
    res = 1
    for divider in range(1, min(n1, n2)):
        if n1 % divider == 0 and n2 % divider == 0: res = divider
    return res

def extended_euclid_alg(d: int, phi: int):
    DO_LOG = False
    r = [phi, d]
    q = [None, None]
    s = [1, 0]
    t = [0, 1]
    while r[-1] != 0:
        q.append(r[-2] // r[-1])
        r.append(r[-2] % r[-1])
        s.append(s[-2] - q[-1] * s[-1])
        t.append(t[-2] - q[-1] * t[-1])
    # return {
    #     'r': r,
    #     'q': q,
    #     's': s,
    #     't': t,
    # }
    if DO_LOG: print(f' [DEBUG] {r=}, {q=}, {s=}, {t=}')
    return t[-2] if t[-2] > 0 else t[-2] + t[-1]

def fast_multiplication(base, power, modulo):
    DO_LOG = False
    result = 1
    k = 1
    while power > 0:
        s = power % 2
        if s == 1:
            result = (result * base) % modulo
        if DO_LOG: print(f'{k=}, {base=}, {power=}, {s=}, {result=}')
        base = (base * base) % modulo
        power = (power - s) / 2
        k += 1
    return result


def gen_keys(p: int, q: int):
    DO_LOG = True
    if DO_LOG: print(f' [DEBUG] {p=}, {q=}')
    n = p * q
    if DO_LOG: print(f' [DEBUG] {n=}')
    phi = (p - 1) * (q - 1)
    if DO_LOG: print(f' [DEBUG] {phi=}')
    d = None
    while d is None or mcd(d, phi) > 1:
        d = (random.randint(1, 500) * 2 + 1) % phi
        if DO_LOG: print(f' [DEBUG] {d=}, {mcd(d, phi)=}')
    e = extended_euclid_alg(d, phi)
    if DO_LOG: print(f' [DEBUG] {e=}')
    return {
        "public": (e, n),
        "private": (d, n),
    }

def encode_rsa(public_key: tuple[int, int], text: str):
    DO_LOG = False
    text_ord = list(map(lambda x: ord(x) - 1039, list(text)))
    if DO_LOG: print(f' [DEBUG] Char codes of text: {text_ord}')
    encoded = list(map(lambda m: fast_multiplication(m, public_key[0], public_key[1]), text_ord))
    if DO_LOG: print(f' [DEBUG] encoded text: {encoded}')
    return encoded

def decode_rsa(private_key: tuple[int, int], encoded_text: list[int]):
    DO_LOG = False
    decoded = list(map(lambda c: fast_multiplication(c, private_key[0], private_key[1]), encoded_text))
    if DO_LOG: print(f' [DEBUG] decoded char codes {decoded}')
    text = ''.join(list(map(lambda c: chr(c + 1039), decoded)))
    if DO_LOG: print(f' [DEBUG] decoded text: {text}')
    return text

if __name__ == '__main__':
    DO_LOG = True
    p = 13
    q = 19
    keys = gen_keys(p, q)
    if DO_LOG: print(f' [DEBUG] {keys=}')
    text = "ОРЛ"
    encoded = encode_rsa(keys['public'], text)
    if DO_LOG: print(f' [DEBUG] {encoded=}')
    text = decode_rsa(keys['private'], encoded)
    if DO_LOG: print(f' [DEBUG] {text=}')
