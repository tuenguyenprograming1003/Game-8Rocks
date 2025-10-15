import random

n = 8

def count_conflicts(st):
    """Đếm số xung đột trong trạng thái hiện tại"""
    cf = 0
    for i in range(len(st)):
        if st[i] is None:
            continue
        for j in range(i+1, len(st)):
            if st[j] is None:
                continue
            # Cùng cột
            if st[i] == st[j]:
                cf += 1
            # Đường chéo
            if abs(st[i] - st[j]) == abs(i - j):
                cf += 1
    return cf

def get_neighbors(st):
    """Tạo tất cả các trạng thái láng giềng bằng cách di chuyển một quân xe"""
    nb = []
    for r in range(len(st)):
        if st[r] is None:
            continue
        cur = st[r]
        for c in range(n):
            if c != cur:
                ng = st.copy()
                ng[r] = c
                nb.append(ng)
    return nb

def hill_climbing_target(tg):
    """Hill Climbing để tìm đường từ trạng thái random đến target"""
    cur = [random.randint(0, n-1) for _ in range(n)]
    path = [cur.copy()]
    
    max_it = 1000
    it = 0
    
    while it < max_it:
        # Kiểm tra xem đã đạt target chưa
        if cur == tg:
            break
            
        # Tạo các trạng thái láng giềng
        nb = get_neighbors(cur)
        
        # Tính khoảng cách đến target cho trạng thái hiện tại
        cur_d = sum(1 for i in range(n) if cur[i] != tg[i])
        
        # Tìm láng giềng tốt nhất (gần target nhất)
        best = None
        best_d = cur_d
        
        for ng in nb:
            d = sum(1 for i in range(n) if ng[i] != tg[i])
            if d < best_d:
                best_d = d
                best = ng
        
        # Nếu không có láng giềng nào tốt hơn, dừng lại (local optimum)
        if best is None:
            break
            
        cur = best
        path.append(cur.copy())
        it += 1
    
    return path

def hill_climbing_simple():
    """Hill Climbing đơn giản để giải bài toán 8 quân xe"""
    cur = [random.randint(0, n-1) for _ in range(n)]
    path = [cur.copy()]
    
    max_it = 1000
    it = 0
    
    while it < max_it:
        cur_cf = count_conflicts(cur)
        
        # Nếu không có xung đột, ta đã tìm được lời giải
        if cur_cf == 0:
            break
            
        # Tạo các trạng thái láng giềng
        nb = get_neighbors(cur)
        
        # Tìm láng giềng tốt nhất (ít xung đột nhất)
        best = None
        best_cf = cur_cf
        
        for ng in nb:
            cf = count_conflicts(ng)
            if cf < best_cf:
                best_cf = cf
                best = ng
        
        # Nếu không có láng giềng nào tốt hơn, dừng lại
        if best is None:
            # Restart với trạng thái random mới
            cur = [random.randint(0, n-1) for _ in range(n)]
        else:
            cur = best
            
        path.append(cur.copy())
        it += 1
    
    return path
