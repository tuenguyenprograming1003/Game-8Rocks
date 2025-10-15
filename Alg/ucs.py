import heapq

n = 8

def tinh_chi_phi(ban, r, c):
    used = set([x for x in ban if x is not None])
    if c in used:
        return 20
    remain = n - r - 1
    return 1 + (n - remain)

def ucs_target(tg):
    tg_t = tuple(tg)
    start = tuple()
    pq = [(0, start)]  # (chi phí, trạng thái)
    par = {start: None}
    cost = {start: 0}
    while pq:
        g, st = heapq.heappop(pq)
        if st == tg_t:
            break
        r = len(st)
        if r >= n: continue
        for c in range(n):
            if c in st: continue
            ns = tuple(list(st)+[c])
            new_cost = g + tinh_chi_phi(st, r, c)
            if ns not in cost or new_cost < cost[ns]:
                cost[ns] = new_cost
                par[ns] = st
                heapq.heappush(pq,(new_cost,ns))
    if tg_t not in par: return []
    path=[]
    cur=tg_t
    while cur is not None:
        s=[None]*n
        for i,v in enumerate(cur): s[i]=v
        path.append(s)
        cur=par.get(cur)
    return path[::-1]
