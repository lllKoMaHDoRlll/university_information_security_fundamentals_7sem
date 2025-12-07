import math
import random

def extended_euclid_alg(d: int, phi: int):
    DO_LOG = True
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

def mcd(n1: int, n2: int):
    res = 1
    for divider in range(1, min(n1, n2)):
        if n1 % divider == 0 and n2 % divider == 0: res = divider
    return res

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

def rabin_miller_test(p: int, k: int = 5):
    DO_LOG = False
    if p < 2 or p % 2 == 0:
        return False
    if p == 2 or p == 3:
        return True

    p_bin = bin(p - 1)[2:]
    b = 0
    for i in range(len(p_bin) - 1, -1, -1):
        if p_bin[i] == '0':
            b += 1
        else:
            break

    m = (p - 1) // (2 ** b)
    if DO_LOG: print(f' [DEBUG] p={p}, p-1={p-1}, b={b}, m={m}')

    for round_num in range(k):
        a = random.randint(2, p - 2)
        if DO_LOG: print(f' [DEBUG] Round {round_num + 1}: a={a}')

        z = fast_multiplication(a, m, p)
        if DO_LOG: print(f' [DEBUG] z = a^m mod p = {z}')

        if z == 1 or z == p - 1:
            if DO_LOG: print(f' [DEBUG] z={z}, continuing to next round')
            continue

        composite = True
        for j in range(b - 1):
            z = (z * z) % p
            if DO_LOG: print(f' [DEBUG] Squaring {j + 1}: z={z}')

            if z == 1:
                if DO_LOG: print(f' [DEBUG] z=1, p is composite')
                return False

            if z == p - 1:
                composite = False
                if DO_LOG: print(f' [DEBUG] z=p-1, round passes')
                break

        if composite:
            if DO_LOG: print(f' [DEBUG] Never found p-1, p is composite')
            return False

    return True

def generate_prime(n: int = 10):
    DO_LOG = False
    while True:
        PRIMES = [
            3, 5, 7, 11, 13, 17, 19, 23, 29,
            31, 37, 41, 43, 47, 53, 59, 61,
            67, 71, 73, 79, 83, 89, 97, 101,
            103, 107, 109, 113, 127, 131, 137,
            139, 149, 151, 157, 163, 167, 173,
            179, 181, 191, 193, 197, 199
        ]
        p = int('1' + ''.join(random.choices('01', k=n - 2)) + '1', 2)
        if DO_LOG: print(f' [DEBUG] Generated prime number: {p}')
        is_prime = True
        for prime in PRIMES:
            if p % prime == 0:
                is_prime = False
                if DO_LOG: print(f' [DEBUG] Found divider number in PRIMES: {prime}')
                break
        if not is_prime:
            continue

        if rabin_miller_test(p):
            return p

def solve_equation(p: int):
    for x in range(1, p):
        for k in range(10):
            y_squared = k * p + (x**3 + x)
            y = math.sqrt(y_squared)
            if y == int(y):
                return (x, int(y))

def obr(a, b):
    g = extended_euclid_alg(a, b)
    return g

def add(p: tuple[int, int], q: tuple[int, int], modulo):
    if p == ('*', 'inf'): p, q = q, p
    if q == ('*', 'inf'):
        return p
    if p[0] != q[0]:
        k = ((q[1] - p[1]) * obr(q[0] - p[0], modulo)) % modulo # через обратный алгоритм евклида
        x = (k*k - (p[0] + q[0])) % modulo
        y = (k*(p[0] - x) - p[1]) % modulo
        print(k, x, y)
        return (x, y)
    elif q[0] == p[0] and p[1] + q[1] == 0:
        return ('*', 'inf')
    elif q[0] == p[0] and q[1] == p[1]:
        k = ((3 * p[0] * p[0] + 1) * obr(2 * p[1], modulo)) % modulo
        x = (k*k - 2 * p[0]) % modulo
        y = (k * (p[0] - x) - p[1]) % modulo
        return (x, y)
    return p

if __name__ == '__main__':
    modulo = 19319
    point = solve_equation(modulo)
    ps = [point]
    d = str(bin(151))[2:]
    for i in range(1, len(d)):
        ps.append(add(ps[-1], ps[-1], modulo))
    res = None
    for i in range(len(d) - 1, -1, -1):
        if d[i] == '1':
            if res is None: res = ps[len(ps) - 1 - i]
            else:
                res = add(res, ps[len(ps) - 1 - i], modulo)

    print(res)
