import math
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
        power = (power - s) // 2
        k += 1
    return result

def isqrt(n: int) -> int:
    if n == 0:
        return 0

    x = n
    y = (x + 1) // 2

    while y < x:
        x = y
        y = (x + n // x) // 2

    return x


def is_perfect_square(n: int) -> tuple[bool, int]:
    if n < 0:
        return (False, 0)

    root = isqrt(n)
    if root * root == n:
        return (True, root)
    return (False, root)


def fermat_factorization(n: int):
    DO_LOG = False

    if n % 2 == 0:
        if DO_LOG: print(f' [DEBUG] n четное, возвращаем (2, {n // 2})')
        return (2, n // 2)

    for i in range(3, 1000000, 2):
        if n % i == 0:
            if DO_LOG: print(f' [DEBUG] пробное деление {(i, n // i)}')
            return (i, n // i)

    a = isqrt(n)
    if a * a < n:
        a += 1

    if DO_LOG: print(f' [DEBUG] начинаем ферма с a = ceil(sqrt({n})) = {a}')

    max_iterations = 10_000_000
    b_squared = a * a - n

    for iteration in range(max_iterations):
        is_perfect, b = is_perfect_square(b_squared)

        if iteration % 10000 == 0:
            print(a + b, a - b)

        if is_perfect:
            p = a + b
            q = a - b
            if DO_LOG: print(f' [DEBUG] найденные делители: p={p}, q={q}')
            if p * q == n:
                return (p, q)

        a += 1
        b_squared += a*a - n


    if DO_LOG: print(f' [DEBUG] вышли за пределы по итерациям')
    return (None, None)


def find_all_factors(n: int):
    DO_LOG = False

    if DO_LOG: print(f' [DEBUG] ищем все делители {n}')

    if n == 1:
        return []

    if n == 2:
        return [2]

    if rabin_miller_test(n, 10):
        if DO_LOG: print(f' [DEBUG] {n} простое')
        return [n]

    p, q = fermat_factorization(n)

    if p is None:
        print(f" [ERROR] ошибка метода ферма")
        return [n]

    factors = []
    factors.extend(find_all_factors(p))
    factors.extend(find_all_factors(q))

    return sorted(factors)

def rabin_miller_test(p: int, k: int = 5):
    DO_LOG = False
    if p == 2 or p == 3:
        return True
    if p < 2 or p % 2 == 0:
        return False

    p_bin = bin(p - 1)[2:]
    b = 0
    for i in range(len(p_bin) - 1, -1, -1):
        if p_bin[i] == '0':
            b += 1
        else:
            break

    m = (p - 1) // (2 ** b)
    if DO_LOG: print(f' [DEBUG] p={p}, p-1={p-1}, b={b}, m={m}')

    for _ in range(k):
        a = random.randint(2, p - 2)
        if DO_LOG: print(f' [DEBUG] Round: a={a}')

        z = fast_multiplication(a, m, p)
        if DO_LOG: print(f' [DEBUG] z = a^m mod p = {z}')

        if z == 1 or z == p - 1:
            if DO_LOG: print(f' [DEBUG] z={z}, continuing to next round')
            continue

        for _ in range(b - 1):
            z = fast_multiplication(z, 2, p)
            if DO_LOG: print(f' [DEBUG] Squaring: z={z}')
            if z == p - 1:
                break
        else:
            if DO_LOG: print(f' [DEBUG] Never found p-1, p is composite')
            return False

    return True

if __name__ == '__main__':
    n = [None for _ in range(31)]

    n[1]= 459815140061495110658001985470439569453709795016952965385917
    n[2]= 1076259412231815019865125804167605592839315742411540973272839
    n[3]= 14554137880788423915514734980557110302769737399620545126091
    n[4]= 147872897588996798681411517668530454151700817458090471306057
    n[ 5 ]= 343307067711615047372182962356629442952289267108875003956201
    n[ 6 ]= 11391035927007347815972448788654755662185624388776525399183
    n[ 7 ]= 177089006521129342654978783090588830391135282114111742670367
    n[ 8 ]= 183483903543663118800683335500060438797379801801396319200491
    n[ 9 ]= 509608207264673804753102004815261943798045580747165058779913
    n[ 10 ]= 1586684831692131610153296320797561138217567504388254780459
    n[ 11 ]= 964758387457354683609980045464712160753368874876361319018239
    n[ 12 ]= 92978831446527927064539719775506181151010499772447865126477
    n[ 13 ]= 21078917190183585592715638706004862806827590109994148804973
    n[ 14 ]= 103311351230629013535108887217099755806929397625109022634789
    n[ 15 ]= 1337696339928982909586628808438874666391449118623896454693047
    n[ 16 ]= 1089810507792762720362254830141236745576712137708202769254243
    n[ 17 ]= 119085790223305523923827791175557636910242489365045086145177
    n[ 18 ]= 541820263085512183692830798149515383361147723174659116188511
    n[ 19 ]= 4374208415220496432912893532769785156459194076736398159111
    n[ 20 ]= 1353354175328598478245469115101071230588584064102913457666793
    n[ 21 ]= 1306691811057227102896266821563564639795065373404858604903919
    n[ 22 ]= 317495676810599057231709047823391550221845129009040088621267
    n[ 23 ]= 499517941060070456313665576547039003336292020387236828944459
    n[ 24 ]= 500822238486126037858630088990539424312577913699892996636521
    n[ 25 ]= 185080760076958069539801778813501214108319189668655638954567
    n[ 26 ]= 3378269570418420681530983916998218027829340764498864474459
    n[ 27 ]= 1178016179343739470394039383628225591199012438273423994122873
    n[ 28 ]= 402819037631291815043762446556303119919847596046522791095493
    n[ 29 ]= 553635738592841024015036052236172349141155301006727667252643
    n[ 30 ]= 90531694464813459650597725911504303945211895831619408158089

    for item in n[1:]:
        print(f'n[{item}] = {find_all_factors(item)}')
