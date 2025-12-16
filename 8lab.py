
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

def isqrt(n: int) -> int:
    if n == 0:
        return 0

    x = n
    y = (x + 1) // 2

    while y < x:
        x = y
        y = (x + n // x) // 2

    return x

def baby_step_giant_step(p: int, g: int, a: int):
    DEBUG = True
    if DEBUG: print(f'[DEBUG] {p=}, {g=}, {a=}')
    m = isqrt(p) + 1
    if DEBUG: print(f'[DEBUG] {m=}')
    giant_steps = []
    for i in range(1, m + 1):
        if DEBUG: print(f'[DEBUG] giant step params: {g=}, {i*m=}, {p=}')
        giant_steps.append(fast_multiplication(g, i*m, p))
        if DEBUG: print(f'[DEBUG] giant step value: {giant_steps[-1]}')
    if DEBUG: print(f'[DEBUG] {giant_steps=}')

    for j in range(m):
        if DEBUG: print(f'[DEBUG] baby step params: {g=}, {j=}, {p=}')
        baby_step_value = (fast_multiplication(g, j, p) * a) % p
        if DEBUG: print(f'[DEBUG] baby step value: {baby_step_value}')
        if baby_step_value in giant_steps:
            if DEBUG: print(f'[DEBUG] Found: {giant_steps.index(baby_step_value) + 1}*{m} - {j}')
            return ((giant_steps.index(baby_step_value) + 1) * m - j)

def solve_linear_system_mod(matrix, modulo):
    DEBUG = True

    m = len(matrix)
    n = len(matrix[0]) - 1
    aug_matrix = [row[:] for row in matrix]

    if DEBUG: print(f"[DEBUG] Matrix size: {m} equations, {n} variables")

    current_row = 0

    for col in range(n):
        if DEBUG: print(f"\n[DEBUG] === Processing column {col} ===")

        pivot_row = None
        for row in range(current_row, m):
            if aug_matrix[row][col] % modulo != 0:
                pivot_row = row
                break

        if pivot_row is None:
            continue

        if pivot_row != current_row:
            aug_matrix[current_row], aug_matrix[pivot_row] = aug_matrix[pivot_row], aug_matrix[current_row]
            if DEBUG: print(f"[DEBUG] Swapped rows {current_row} and {pivot_row}")

        pivot = aug_matrix[current_row][col] % modulo
        if DEBUG: print(f"[DEBUG] Pivot at row {current_row}, col {col}: {pivot}")

        try:
            pivot_inv = extended_euclid_alg(pivot, modulo)
            if DEBUG: print(f"[DEBUG] Pivot inverse: {pivot_inv}")

            if (pivot * pivot_inv) % modulo != 1:
                if DEBUG: print(f"[DEBUG] Invalid inverse.")
                current_row += 1
                continue
        except:
            if DEBUG: print(f"[DEBUG] Could not find inverse for {pivot}")
            current_row += 1
            continue

        for j in range(len(aug_matrix[current_row])):
            aug_matrix[current_row][j] = (aug_matrix[current_row][j] * pivot_inv) % modulo

        if DEBUG: print(f"[DEBUG] Scaled row {current_row}: {aug_matrix[current_row]}")

        for row in range(m):
            if row != current_row:
                factor = aug_matrix[row][col] % modulo
                if factor != 0:
                    for j in range(len(aug_matrix[row])):
                        aug_matrix[row][j] = (aug_matrix[row][j] - factor * aug_matrix[current_row][j]) % modulo

        current_row += 1
        if current_row >= m:
            break

    if DEBUG: print(f"\n[DEBUG] After gaus.")
    if DEBUG:
        for i, row in enumerate(aug_matrix):
            print(f"[DEBUG] Row {i}: {row}")

    solution = [0] * n

    for row in range(min(m, n)):
        pivot_col = None
        for col in range(n):
            if aug_matrix[row][col] % modulo == 1:
                is_pivot = True
                for c in range(col):
                    if aug_matrix[row][c] % modulo != 0:
                        is_pivot = False
                        break
                if is_pivot:
                    pivot_col = col
                    break

        if pivot_col is not None:
            solution[pivot_col] = aug_matrix[row][-1] % modulo
            if DEBUG: print(f"[DEBUG] From row {row}: x{pivot_col} = {solution[pivot_col]}")

    if DEBUG: print(f"\n[DEBUG] Final solution: {solution}")

    if DEBUG: print(f"\n[DEBUG] Verifying solution with all equations:")
    all_correct = True
    for i in range(len(matrix)):
        lhs = sum(matrix[i][j] * solution[j] for j in range(n)) % modulo
        rhs = matrix[i][-1] % modulo
        match = lhs == rhs
        if lhs != rhs:
            all_correct = False
        if DEBUG and (i < 5 or lhs != rhs):
            print(f"[DEBUG] Equation {i}: {lhs} = {rhs} (mod {modulo}) {match}")

    if DEBUG: print(f"[DEBUG] All equations satisfied: {all_correct}")

    return solution

def order_calculation_method(p: int, g: int, a: int, c: int = 10, t: int = 10, max_retries: int = 10):
    DEBUG = True

    for retry in range(max_retries):
        if retry > 0:
            if DEBUG: print(f"\n[DEBUG] ===== RETRY #{retry + 1}/{max_retries} =====\n")

        try:
            result = _order_calculation_attempt(p, g, a, c, t, DEBUG)
            if result is not None:
                if fast_multiplication(g, result, p) == a:
                    return result
                else:
                    if DEBUG: print(f"[DEBUG] Result verification failed: {g}^{result} mod {p} = {fast_multiplication(g, result, p)}, expected {a}")
            else:
                if DEBUG: print(f"[DEBUG] Attempt failed, retrying...")
        except Exception as e:
            if DEBUG: print(f"[DEBUG] Exception occurred: {e}, retrying...")

    if DEBUG: print(f"[DEBUG] All {max_retries} attempts failed.")
    return None

def _order_calculation_attempt(p: int, g: int, a: int, c: int, t: int, DEBUG: bool):

    def get_primes(limit):
        primes = []
        num = 2
        while len(primes) < limit:
            is_prime = True
            for p in primes:
                if p * p > num:
                    break
                if num % p == 0:
                    is_prime = False
                    break
            if is_prime:
                primes.append(num)
            num += 1
        return primes

    factor_base = get_primes(t)
    if DEBUG: print(f"[DEBUG] Factor base S: {factor_base}")

    n = p - 1
    if DEBUG: print(f"[DEBUG] {n=}")

    relations = []
    k_values = []

    import random
    max_attempts = 100000

    for attempt in range(max_attempts):
        if attempt % 1000 == 0 and DEBUG:
            print(f"[DEBUG] Attempt #{attempt+1}/{max_attempts}, found {len(relations)} relations")

        k = random.randint(1, n - 1)
        gk = fast_multiplication(g, k, p)

        temp = gk
        alphas = []

        for pi in factor_base:
            alpha_i = 0
            while temp % pi == 0:
                temp //= pi
                alpha_i += 1
            alphas.append(alpha_i)

        if temp == 1:
            relations.append(alphas)
            k_values.append(k)
            if DEBUG: print(f" [DEBUG] Relation found: #{len(relations)}: g^{k} = {' * '.join([f'{factor_base[i]}^{alphas[i]}' for i in range(len(alphas)) if alphas[i] > 0])}")

            if len(relations) >= t + c:
                if DEBUG: print(f"[DEBUG] Found enough relations.")
                break

    if len(relations) < t + c:
        if DEBUG: print(f"[DEBUG] Could not find enough relations: {len(relations)}/{t + c}")
        return None

    if DEBUG: print(f"[DEBUG] Building matrix.")
    matrix = []
    for i in range(len(relations)):
        row = relations[i] + [k_values[i]]
        matrix.append(row)

    if DEBUG: print(f"[DEBUG] Got matrix with {len(matrix)} equations and {len(factor_base)} variables.")

    if DEBUG: print(f"[DEBUG] Solving linear system for factor base logs.")
    logs_list = solve_linear_system_mod(matrix, n)

    logs = {}
    for i, pi in enumerate(factor_base):
        logs[pi] = logs_list[i]
        if DEBUG: print(f"[DEBUG] log_{g}({pi}) = {logs[pi]}")

    if DEBUG: print(f"\n[DEBUG] Verifying computed logs:")
    all_logs_correct = True
    for pi in factor_base:
        computed = fast_multiplication(g, logs[pi], p)
        is_correct = computed == pi
        if not is_correct:
            all_logs_correct = False
        if DEBUG: print(f"[DEBUG] {g}^{logs[pi]} mod {p} = {computed}, expected {pi}, match: {is_correct}")

    if not all_logs_correct:
        if DEBUG: print(f"[DEBUG] Some logs are incorrect, this attempt failed.")
        return None

    for attempt in range(max_attempts):
        if attempt % 1000 == 0 and DEBUG:
            print(f"[DEBUG] Phase 2: Attempt #{attempt+1}/{max_attempts}")

        k = random.randint(1, n - 1)
        agk = (a * fast_multiplication(g, k, p)) % p

        temp = agk
        betas = []

        for pi in factor_base:
            beta_i = 0
            while temp % pi == 0:
                temp //= pi
                beta_i += 1
            betas.append(beta_i)

        if temp == 1:
            if DEBUG: print(f"[DEBUG] Found relation: ag^{k} = {' * '.join([f'{factor_base[i]}^{betas[i]}' for i in range(len(betas)) if betas[i] > 0])}")

            if DEBUG: print(f"[DEBUG] Calculating x=log_g(a)")
            x = 0
            for i in range(len(factor_base)):
                x += betas[i] * logs[factor_base[i]]
            x = (x - k) % n

            if DEBUG: print(f"[DEBUG] Result: log_{g}({a}) = {x}")
            return x

    if DEBUG: print(f"[DEBUG] Could not find representation of a*g^k in phase 2.")
    return None

if __name__ == '__main__':
    p = 263
    g = 7
    a = 19

    print("=== Baby-step Giant-step ===")
    result = baby_step_giant_step(p, g, a)
    print(f'Baby-step Giant-step: {result}')
    print(f'Проверка: {g}^{result} mod {p} = {fast_multiplication(g, result, p)}')

    print("=== Метод исчисления порядка ===")
    result_order = order_calculation_method(p, g, a)
    if result_order is not None:
        print(f'\nМетод исчисления порядка: {result_order}')
        print(f'Проверка: {g}^{result_order} mod {p} = {fast_multiplication(g, result_order, p)}')
