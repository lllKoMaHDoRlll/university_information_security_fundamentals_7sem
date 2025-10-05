import random

# rsa

def mcd(n1: int, n2: int):
    res = 1
    for divider in range(min(n1, n2)):
        if n1 % divider == 0 and n2 % divider: res = divider
    return res

def extended_euclid_alg(d: int, phi: int):
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
    return t[-2] if t[-2] > 0 else t[-2] + t[-1]

def gen_keys(p: int, q: int):
    n = p * q
    phi = (p - 1) * (q - 1)
    d = None
    while d is None or mcd(d, phi) > 1:
        d = random.randint(1, 500) * 2 + 1
    e = extended_euclid_alg(d, phi)

print(extended_euclid_alg(25, 216))
