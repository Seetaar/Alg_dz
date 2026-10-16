import sys

input = sys.stdin.readline


class Node:
    def __init__(self, key):
        self.key = key
        self.left = self.right = None
        self.height = 1


def h(n): return n.height if n else 0


def bal(n): return h(n.right) - h(n.left) if n else 0


def upd(n):
    if n: n.height = 1 + max(h(n.left), h(n.right))


def rotL(a):
    b = a.right
    a.right = b.left
    b.left = a
    upd(a);
    upd(b)
    return b


def rotR(a):
    b = a.left
    a.left = b.right
    b.right = a
    upd(a);
    upd(b)
    return b


def fix(n):
    upd(n)
    b = bal(n)
    if b == 2:
        if bal(n.right) >= 0: return rotL(n)
        n.right = rotR(n.right)
        return rotL(n)
    if b == -2:
        if bal(n.left) <= 0: return rotR(n)
        n.left = rotL(n.left)
        return rotR(n)
    return n


def ins(n, k):
    if not n: return Node(k)
    if k < n.key:
        n.left = ins(n.left, k)
    elif k > n.key:
        n.right = ins(n.right, k)
    else:
        return n
    return fix(n)


def fmin(n):
    while n.left: n = n.left
    return n


def rem(n, k):
    if not n: return None
    if k < n.key:
        n.left = rem(n.left, k)
    elif k > n.key:
        n.right = rem(n.right, k)
    else:
        if not n.left: return n.right
        if not n.right: return n.left
        m = fmin(n.right)
        n.key = m.key
        n.right = rem(n.right, m.key)
    return fix(n)


def has(n, k):
    while n:
        if k == n.key: return True
        n = n.left if k < n.key else n.right
    return False


def nxt(n, k):
    r = None
    while n:
        if n.key >= k:
            r, n = n.key, n.left
        else:
            n = n.right
    return r


def prv(n, k):
    r = None
    while n:
        if n.key <= k:
            r, n = n.key, n.right
        else:
            n = n.left
    return r


def pre(n):
    if not n: return []
    return [n.key] + pre(n.left) + pre(n.right)


Q = int(input())
root = None
out = []

for _ in range(Q):
    p = input().split()
    c, x = p[0], int(p[1]) if len(p) > 1 else None

    if c == 'add':
        root = ins(root, x)
    elif c == 'del':
        root = rem(root, x)
    elif c == 'exists':
        out.append('YES' if has(root, x) else 'NO')
    elif c == 'next':
        r = nxt(root, x); out.append(str(r) if r is not None else 'Nope')
    elif c == 'prev':
        r = prv(root, x); out.append(str(r) if r is not None else 'Nope')
    elif c == 'root':
        out.append(str(root.key) if root else 'Empty')
    elif c == 'height':
        out.append(str(h(root)))
    elif c == 'print':
        r = pre(root); out.append(' '.join(map(str, r)) if r else 'Empty')

print('\n'.join(out))