import heapq

n = 8

def tinh_chi_phi(ban, r, c):
    used = set([x for x in ban if x is not None])
    if c in used:
        return 20
    remain = n - r - 1
    return 1 + (n - remain)

def heuristic(state, target):
    h = 0
    state_list = list(state)
    for i in range(len(state_list)):
        if i < len(state_list) and state_list[i] != target[i]:
            h += 1
    return h

def astar_target(tg):
    tg_t = tuple(tg)
    start = tuple()
    pq = [(0 + heuristic(start, tg_t), 0, start)]  # (f=g+h, g, state)
    par = {start: None}
    g_scores = {start: 0}
    
    while pq:
        f, g, st = heapq.heappop(pq)
        if st == tg_t:
            break
        
        r = len(st)
        if r >= n:
            continue
            
        for c in range(n):
            if c in st:
                continue
            ns = tuple(list(st) + [c])
            new_g = g + tinh_chi_phi(st, r, c)
            
            if ns not in g_scores or new_g < g_scores[ns]:
                g_scores[ns] = new_g
                f = new_g + heuristic(ns, tg_t)
                heapq.heappush(pq, (f, new_g, ns))
                par[ns] = st
                
    if tg_t not in par:
        return []
        
    path = []
    cur = tg_t
    while cur is not None:
        s = [None]*n
        for i,v in enumerate(cur):
            s[i] = v
        path.append(s)
        cur = par.get(cur)
    return path[::-1]
