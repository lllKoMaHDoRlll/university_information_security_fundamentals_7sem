import random


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
    DO_LOG = True
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


if __name__ == '__main__':
    print(generate_prime(24))
