import hashlib
import mmh3 as m

sha256_cache = {}
with open("sha256.csv", "r") as f:
    for line in f:
        ps = line.split(",")
        sha256_cache[int(ps[0])] = int(ps[1], 16)
    f.close()

mmh3_cache = {}
with open("mmh3.csv", "r") as f:
    for line in f:
        ps = line.split(",")
        mmh3_cache[int(ps[0])] = int(ps[1])
    f.close()

def sha256(x):
    """SHA256"""

    #return hashlib.sha256(bytes(x)).hexdigest()
    return sha256_cache[x]

def sha256_4(x):
    """SHA256 with 4 bit output"""

    #return int(sha256(x)[:1], 16)
    return (sha256_cache[x] % (2 ** 4)) + 1

def sha256_8(x):
    """SHA256 with 8 bit output"""

    #return int(sha256(x)[:2], 16)
    return (sha256_cache[x] % (2 ** 8)) + 1

def sha256_12(x):
    """SHA256 with 12 bit output"""

    #return int(sha256(x)[:3], 16)
    return (sha256_cache[x] % (2 ** 12)) + 1

def sha256_16(x):
    """SHA256 with 16 bit output"""

    #return int(sha256(x)[:4], 16)
    return (sha256_cache[x] % (2 ** 16)) + 1

def sha256_32(x):
    """SHA256 with 32 bit output"""

    #return int(sha256(x)[:8], 16)
    return (sha256_cache[x] % (2 ** 32)) + 1

def sha256_n(x, n):
    """SHA256 with n bit output"""

    return (sha256_cache[x] % (2 ** n)) + 1

def mmh3(x):
    """MurmurHash3"""

    #return m.hash(bytes(x))
    return mmh3_cache[x]

def mmh3_N(x, N):
    """MurmurHash3 with output mod N"""

    #return m.hash(bytes(x)) % N
    return (mmh3_cache[x] % N) + 1

def mmh3_4(x):
    """MurmurHash3 with 4 bit output"""

    #return (mmh3(x) % (2 ** 4)) + 1
    return (mmh3_cache[x] % (2 ** 4)) + 1

def mmh3_8(x):
    """MurmurHash3 with 8 bit output"""

    #return (mmh3(x) % (2 ** 8)) + 1
    return (mmh3_cache[x] % (2 ** 8)) + 1

def mmh3_12(x):
    """MurmurHash3 with 12 bit output"""

    #return (mmh3(x) % (2 ** 12)) + 1
    return (mmh3_cache[x] % (2 ** 12)) + 1

def mmh3_16(x):
    """MurmurHash3 with 16 bit output"""

    #return (mmh3(x) % (2 ** 16)) + 1
    return (mmh3_cache[x] % (2 ** 16)) + 1
