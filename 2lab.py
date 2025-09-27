REPLACEMENT_BLOCK = [
   # 8   7   6   5   4   3   2   1
    [1,  13, 4,  6,  7,  5,  14, 4 ],
    [15, 11, 11, 12, 13, 8,  11, 10],
    [13, 4,  10, 7,  10, 1,  4,  9 ],
    [0,  1,  0,  1,  1,  13, 12, 2 ],
    [5,  3,  7,  5,  0,  10, 6,  13],
    [7,  15, 2,  15, 8,  3,  13, 8 ],
    [10, 5,  1,  13, 9,  4,  15, 0 ],
    [4,  9,  13, 8,  15, 2,  10, 14],
    [9,  0,  3,  4,  14, 14, 2,  6 ],
    [2,  10, 6,  10, 4,  15, 3,  11],
    [3,  14, 8,  9,  6,  12, 8,  1 ],
    [14, 7,  5,  14, 12, 7,  1,  12],
    [6,  6,  9,  0,  11, 6,  0,  7 ],
    [11, 8,  12, 3,  2,  0,  7,  15],
    [8,  2,  15, 11, 5,  9,  5,  5 ],
    [12, 12, 14, 2,  3,  11, 9,  3 ]
]

def cyph(text: str):
    def to_bin(c):
        code = 0
        if c == ' ':
            code = 32
        else:
            code = ord(c) - 848
        return bin(code)[2:].zfill(8)

    l0 = text[:4]
    r0 = text[4:8]
    k = text[8: 12]

    print(f" [DEBUG] изначальный текст {l0=}, {r0=}, {k=}")
    l0_bin = "".join(list(map(to_bin, l0)))
    r0_bin = "".join(list(map(to_bin, r0)))
    k_bin = "".join(list(map(to_bin, k)))
    print(f" [DEBUG] в двоичной {l0_bin=}, {r0_bin=}, {k_bin=}")
    r1 = str(bin(int(r0_bin, 2) + int(k_bin, 2)))[2:][-32:]
    print(f" [DEBUG] после сложения {r1=}")
    l0 = l0_bin[-32:]
    r1_replaced = []
    for i in range(8):
        part = r1[i * 4: (i+1) * 4]
        code = int(part, 2)
        print(f" [DEBUG] сменяемое число {part} {code}")
        print(f" [DEBUG] смененное число {REPLACEMENT_BLOCK[code][i]}")
        r1_replaced.append(bin(REPLACEMENT_BLOCK[code][i])[2:].zfill(4))
    r1 = "".join(r1_replaced)
    print(f" [DEBUG] после блока смены {r1=}")
    r1 = r1[11:] + r1[:11]
    print(f" [DEBUG] после сдвига {r1=}")
    r1_res = ""
    for i in range(len(r1)):
        r1_res += "1" if int(r1[i]) + int(l0[i]) == 1 else "0"
    print(f" [DEBUG] после сложения r1={r1_res}")
    return {'r1': r1_res, 'l1': l0, 'k': k_bin}

def decyph(l1: str, r1: str, k: str):
    def from_bin(code):
        c = ''
        if code == 32:
            c = ' '
        else:
            c = chr(code + 848)
        return c
    r1_res = ''
    for i in range(len(r1)):
        if r1[i] == '0':
            r1_res += '1' if l1[i] == '1' else '0'
        else:
            r1_res += '0' if l1[i] == '1' else '1'
    print(f" [DEBUG] после вычитания l1: {r1_res}")
    r1 = r1_res[-11:] + r1_res[:-11]
    print(f" [DEBUG] после обратного сдвига: {r1}")
    r1_replaced = []
    for i in range(8):
        part = r1[i * 4: (i+1) * 4]
        code = int(part, 2)
        index = list(map(lambda x: x[i], REPLACEMENT_BLOCK)).index(code)
        r1_replaced.append(bin(index)[2:].zfill(4))
    r1 = "".join(r1_replaced)
    print(f" [DEBUG] после обратной замены {r1}")
    r0 = str(bin(int(r1, 2) - int(k, 2)))[2:][-32:]
    print(f" [DEBUG] после вычитания {r0}")
    l0_decrypted = ''
    r0_decrypted = ''
    for i in range(4):
        l0_decrypted += from_bin(int(l1[i * 8 : (i + 1) * 8], 2))
        r0_decrypted += from_bin(int(r0[i * 8 : (i + 1) * 8], 2))
    print(l0_decrypted, r0_decrypted)





input_text = "ОРЛИЧЕНЯ АЛЕКСАНДР ВАСИЛЬЕВИЧ И КРИП"

encrypted = cyph(input_text)
decrypted = decyph(l1= encrypted['l1'], r1=encrypted['r1'], k=encrypted['k'])
