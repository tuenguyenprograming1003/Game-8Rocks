import random
import math

n = 8

def count_conflicts(st):
    """Đếm số xung đột trong trạng thái"""
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

def get_random_neighbor(st):
    """Tạo một láng giềng ngẫu nhiên bằng cách di chuyển một quân xe"""
    ng = st.copy()
    # Chọn ngẫu nhiên một hàng để di chuyển
    r = random.randint(0, n-1)
    # Di chuyển đến cột ngẫu nhiên khác
    new_c = random.randint(0, n-1)
    ng[r] = new_c
    return ng

def simulated_annealing_target(tg, max_it=10000, init_temp=100, cool_rate=0.95):
    """Simulated Annealing để tìm đường đến target"""
    # Bắt đầu từ trạng thái ngẫu nhiên
    cur = [random.randint(0, n-1) for _ in range(n)]
    path = [cur.copy()]
    
    temp = init_temp
    best = cur.copy()
    best_score = sum(1 for i in range(n) if cur[i] != tg[i])
    
    for it in range(max_it):
        # Kiểm tra nếu đã đạt target
        if cur == tg:
            break
            
        # Tạo láng giềng ngẫu nhiên
        ng = get_random_neighbor(cur)
        
        # Tính điểm cho trạng thái hiện tại và láng giềng
        cur_score = sum(1 for i in range(n) if cur[i] != tg[i])
        ng_score = sum(1 for i in range(n) if ng[i] != tg[i])
        
        # Tính delta (thay đổi năng lượng)
        delta = ng_score - cur_score
        
        # Chấp nhận láng giềng nếu tốt hơn hoặc theo xác suất
        if delta < 0 or (temp > 0 and random.random() < math.exp(-delta / temp)):
            cur = ng
            path.append(cur.copy())
            
            # Cập nhật best nếu tốt hơn
            if ng_score < best_score:
                best = ng.copy()
                best_score = ng_score
        
        # Giảm nhiệt độ
        temp *= cool_rate
        
        # Nếu nhiệt độ quá thấp, dừng
        if temp < 0.01:
            break
    
    # Nếu không đạt target, trả về đường đi đến trạng thái tốt nhất
    if cur != tg and best != cur:
        path.append(best)
    
    return path

def simulated_annealing_simple(max_it=10000, init_temp=100, cool_rate=0.95):
    """Simulated Annealing để giải bài toán 8 quân xe tổng quát"""
    # Bắt đầu từ trạng thái ngẫu nhiên
    cur = [random.randint(0, n-1) for _ in range(n)]
    path = [cur.copy()]
    
    temp = init_temp
    best = cur.copy()
    best_cf = count_conflicts(cur)
    
    for it in range(max_it):
        cur_cf = count_conflicts(cur)
        
        # Nếu không có xung đột, ta đã tìm được lời giải
        if cur_cf == 0:
            break
            
        # Tạo láng giềng ngẫu nhiên
        ng = get_random_neighbor(cur)
        ng_cf = count_conflicts(ng)
        
        # Tính delta
        delta = ng_cf - cur_cf
        
        # Chấp nhận láng giềng
        if delta < 0 or (temp > 0 and random.random() < math.exp(-delta / temp)):
            cur = ng
            path.append(cur.copy())
            
            # Cập nhật best
            if ng_cf < best_cf:
                best = ng.copy()
                best_cf = ng_cf
        
        # Giảm nhiệt độ
        temp *= cool_rate
        
        if temp < 0.01:
            break
    
    # Nếu không tìm được lời giải hoàn hảo, trả về trạng thái tốt nhất
    if count_conflicts(cur) > 0 and best != cur:
        path.append(best)
    
    return path
