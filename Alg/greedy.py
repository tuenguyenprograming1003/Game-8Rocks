import heapq

n = 8

def heuristic(state, target):
    h = 0
    state_list = list(state)
    for i in range(len(state_list)):
        if i < len(state_list) and state_list[i] != target[i]:
            h += 1
    return h

def greedy_target(tg):
    tg_t = tuple(tg)
    start = tuple()
    pq = [(heuristic(start, tg_t), start)]  # (h, state)
    par = {start: None}
    
    while pq:
        h, st = heapq.heappop(pq)
        if st == tg_t:
            break
        
        r = len(st)
        if r >= n:
            continue
            
        for c in range(n):
            if c in st:
                continue
            ns = tuple(list(st) + [c])
            if ns not in par:
                h = heuristic(ns, tg_t)
                heapq.heappush(pq, (h, ns))
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
