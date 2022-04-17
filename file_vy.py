with open("rc4.txt", "rb") as f:  #
    file = f.read()

m = []
for i in file:
    m.append(i)
# m1 = [0x7c, 0x4, 0x4d, 0xcd, 0x45, 0xfd, 0x1e, 0x6a, 0x31, 0x24, 0x7d, 0x5b, 0x65, 0x32, 0x32, 0x9f, 0xea, 0x15, 0x98,
#       0x12, 0xc2, 0x87, 0x96, 0x93, 0x9]
m1 = m
k = "keykeykey"


def re4_init(s, k, len):
    s1 = [0] * 256
    j = 0
    for i in range(256):
        s[i] = i
        s1[i] = k[i % len]
    for i in range(256):
        j = (j + s[i] + ord(s1[i])) % 256
        s[i], s[j] = s[j], s[i]


def re4_crypt(s, m, len):
    i = 0
    j = 0
    for h in range(len):
        i = (i + 1) % 256
        j = (j + s[i]) % 256
        s[i], s[j] = s[j], s[i]
        t = (s[i] + s[j]) % 256
        m[h] ^= s[t]


s = [0] * 256
s2 = [0] * 256
re4_init(s, k, len(k))  # 初始化
for i in range(256):
    s2[i] = s[i]

re4_crypt(s2, m1, len(m1))
for i in range(len(m1)):
    print(hex(m1[i]), end="")
    txt = 'rc4.txt'
    RC4 = open(txt, 'w', encoding='utf-8')
    for i in range(len(m1)):
        RC4.write(chr(m1[i]))
    RC4.close()
# value = ''.join([hex(i).replace('0x', '') for i in m1])
# if len(value)%2:
#     value += '0'
# value = bytes.fromhex(value)
# with open('rc4.txt', 'wb') as fp:
#     fp.write(value)
