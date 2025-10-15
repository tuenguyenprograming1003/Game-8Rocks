from collections import deque

n = 8

def bfs_target(tg):
    tg_t = tuple(tg)
    start = tuple()
    q = deque([start])
    par = {start: None}
    while q:
        st = q.popleft()
        if len(st) == n:
            if tuple(st) == tg_t:
                break
            else:
                continue
        for c in range(n):
            if c in st: continue
            ns = tuple(list(st)+[c])
            if ns not in par:
                par[ns] = st
                q.append(ns)
                if ns == tg_t:
                    q.clear()
                    break
    if tg_t not in par: return []
    path = []
    cur = tg_t
    while cur is not None:
        s = [None]*n
        for i,v in enumerate(cur): s[i]=v
        path.append(s)
        cur = par.get(cur)
    return path[::-1]
