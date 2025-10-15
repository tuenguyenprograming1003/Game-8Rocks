n = 8

def dfs_target(tg):
    tg_t = tuple(tg)
    start = tuple()
    stack = [start]
    par = {start: None}
    while stack:
        st = stack.pop()
        if len(st) == n:
            if st == tg_t:
                break
            else:
                continue
        for c in range(n):
            if c in st: continue
            ns = tuple(list(st)+[c])
            if ns not in par:
                par[ns] = st
                stack.append(ns)
                if ns == tg_t:
                    stack.clear()
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
