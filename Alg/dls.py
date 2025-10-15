n = 8

def dls_target(tg, limit):
    tg_t=tuple(tg)
    start=tuple()
    stack=[(start,0)]
    par={start:None}
    while stack:
        st,d=stack.pop()
        if st==tg_t: break
        if d==limit: continue
        r=len(st)
        for c in range(n):
            if c in st: continue
            ns=tuple(list(st)+[c])
            if ns not in par:
                par[ns]=st
                stack.append((ns,d+1))
                if ns==tg_t:
                    stack.clear()
                    break
    if tg_t not in par: return []
    path=[]
    cur=tg_t
    while cur is not None:
        s=[None]*n
        for i,v in enumerate(cur): s[i]=v
        path.append(s)
        cur=par.get(cur)
    return path[::-1]
