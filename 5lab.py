import random

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

def factorize(n: int) -> list[int]:
    factors = []
    divider = 2

    while divider * divider <= n:
        while n % divider == 0:
            if not factors or factors[-1] != divider:
                factors.append(divider)
            n //= divider
        divider += 1

    if n > 1:
        factors.append(n)

    return factors

def get_primitive(p: int):
    DO_LOG = False
    phi = p - 1
    dividers = factorize(phi)
    if DO_LOG: print(f' [DEBUG] Делители phi(p-1): {dividers}')
    nums = list(range(2, p))
    random.shuffle(nums)
    primitive = None
    for a in nums:
        if DO_LOG: print(f' [DEBUG] Проверка возможности примитивности числа a={a}')
        is_possible_primitive = True
        for divider in dividers:
            if a % divider == 0:
                if DO_LOG: print(f' [DEBUG] Число {a} не является простым для делителя {divider}')
                is_possible_primitive = False
                break
        if is_possible_primitive:
            if DO_LOG: print(f' [DEBUG] проверка примитивности числа a={a}')
            is_primitive = True
            for divider in dividers:
                res = fast_multiplication(a, divider, p)
                if DO_LOG: print(f'a={a}, d={divider}, a^d mod p={res}')
                if res == 1:
                    is_primitive = False
                    break
            if is_primitive:
                primitive = a

    primitives = []
    if primitive is not None:
        primitives.append(primitive)
        print(f' [DEBUG] Найден первый примитивный элемент: {primitive}')
        for t in range(2, p - 1):
            if mcd(t, p - 1) == 1:
                new_primitive = primitives[-1] ** t
                primitives.append(new_primitive)
                print(f' [DEBUG] Добавлен новый примитивный элемент: {new_primitive=}, {primitives[-2]=}, {t=}')
                if len(primitives) >= 5:
                    break

    return primitives




def get_key_pair(p: int, g: int):
    x = random.randint(1, p - 1)
    y = fast_multiplication(g, x, p)
    return {'x': x, 'y': y}

if __name__ == '__main__':
    p = generate_prime(21)
    g_list = get_primitive(p)
    print(f'Простое число p: {p}, примитивные числа g: {g_list} ')

    alisa_key_pair = get_key_pair(p, g_list[0])
    bob_key_pair = get_key_pair(p, g_list[0])

    common_secret_key_alisa = fast_multiplication(bob_key_pair["y"], alisa_key_pair["x"], p)
    common_secret_key_bob = fast_multiplication(alisa_key_pair["y"], bob_key_pair["x"], p)

    print(f'Ключ Alisa: {alisa_key_pair}')
    print(f'Ключ Bob: {bob_key_pair}')
    print(f'Общий секретный ключ Alisa: {common_secret_key_alisa}')
    print(f'Общий секретный ключ Bob: {common_secret_key_bob}')
    print(f'Проверка общего секретного ключа: {common_secret_key_alisa == common_secret_key_bob}')
