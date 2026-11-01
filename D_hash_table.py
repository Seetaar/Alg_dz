import sys

primes = [
    31, 61, 127, 251, 509, 1021, 2039, 4093, 8191,
    16381, 32749, 65537, 131071, 262139, 524287
]

def nextPrime(n):
    for p in primes:
        if p >= n:
            return p
    return n

def stringHash(s):
    h = 0
    for ch in s:
        h = (h * 31 + ord(ch)) & 0x7FFFFFFF
    return h

class HashTable:
    def __init__(self):
        self.cap = primes[0]
        self.buckets = [[] for _ in range(self.cap)]
        self.size = 0
        self.loadFactor = 0.75

    def bucketIndex(self, key):
        return stringHash(key) % self.cap

    def resize(self):
        newCap = nextPrime(self.cap * 2)
        newBuckets = [[] for _ in range(newCap)]
        for bucket in self.buckets:
            for key, val in bucket:
                i = stringHash(key) % newCap
                newBuckets[i].append((key, val))
        self.buckets = newBuckets
        self.cap = newCap

    def put(self, key, val):
        i = self.bucketIndex(key)
        bucket = self.buckets[i]
        for j, (k, v) in enumerate(bucket):
            if k == key:
                bucket[j] = (key, val)
                return
        bucket.append((key, val))
        self.size += 1
        if self.size > self.cap * self.loadFactor:
            self.resize()

    def get(self, key):
        for k, v in self.buckets[self.bucketIndex(key)]:
            if k == key:
                return v
        return None

    def delete(self, key):
        i = self.bucketIndex(key)
        bucket = self.buckets[i]
        for j, (k, v) in enumerate(bucket):
            if k == key:
                bucket.pop(j)
                self.size -= 1
                return v
        return None

def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    q = int(data[pos]); pos += 1
    ht = HashTable()
    out = []

    for _ in range(q):
        cmd = data[pos]; pos += 1
        if cmd == b'put':
            key = data[pos].decode(); pos += 1
            val = int(data[pos]); pos += 1
            ht.put(key, val)
        elif cmd == b'get':
            key = data[pos].decode(); pos += 1
            v = ht.get(key)
            out.append(str(v) if v is not None else 'Error')
        elif cmd == b'del':
            key = data[pos].decode(); pos += 1
            v = ht.delete(key)
            out.append(str(v) if v is not None else 'Error')
        elif cmd == b'size':
            out.append(str(ht.size))

    sys.stdout.write('\n'.join(out) + '\n')

main()