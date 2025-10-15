import heapq
import random

n = 8

def heuristic_distance(st, tg):
    """Tính khoảng cách heuristic đến target"""
    d = 0
    for i in range(len(st)):
        if i < len(st) and i < len(tg):
            if st[i] != tg[i]:
                d += 1
    # Thêm penalty cho các vị trí chưa được đặt
    d += max(0, len(tg) - len(st))
    return d

def get_successors(st):
    """Tạo các trạng thái kế tiếp bằng cách thêm một quân xe"""
    sc = []
    nr = len(st)
    
    if nr >= n:
        return sc
        
    for c in range(n):
        ns = tuple(list(st) + [c])
        sc.append(ns)
    
    return sc

def beam_search_target(tg, beam_width=3):
    """K-Beam Search để tìm đường đến target"""
    tg_t = tuple(tg)
    start = tuple()
    
    # Khởi tạo beam với trạng thái ban đầu
    cur_bm = [start]
    pd = {start: []}
    
    max_it = 100
    it = 0
    
    while cur_bm and it < max_it:
        nxt_bm = []
        
        # Mở rộng tất cả trạng thái trong beam hiện tại
        for st in cur_bm:
            if st == tg_t:
                # Tìm thấy target, trả về đường đi
                path = pd[st]
                rp = []
                for ss in path + [st]:
                    fs = [None] * n
                    for i, c in enumerate(ss):
                        fs[i] = c
                    rp.append(fs)
                return rp
            
            # Tạo các trạng thái kế tiếp
            sc = get_successors(st)
            
            for s in sc:
                if s not in pd:
                    pd[s] = pd[st] + [st]
                    nxt_bm.append(s)
        
        # Chọn beam_width trạng thái tốt nhất dựa trên heuristic
        if len(nxt_bm) > beam_width:
            # Tính heuristic cho tất cả trạng thái
            ss = []
            for st in nxt_bm:
                h = heuristic_distance(st, tg_t)
                ss.append((h, st))
            
            # Sắp xếp theo heuristic và chọn beam_width trạng thái tốt nhất
            ss.sort(key=lambda x: x[0])
            nxt_bm = [st for _, st in ss[:beam_width]]
        
        cur_bm = nxt_bm
        it += 1
    
    # Không tìm thấy đường đi
    return []

def beam_search_general(beam_width=3):
    """K-Beam Search tổng quát để giải bài toán 8 quân xe"""
    def has_conflicts(sl):
        """Kiểm tra xem có xung đột không"""
        for i in range(len(sl)):
            for j in range(i+1, len(sl)):
                # Cùng cột
                if sl[i] == sl[j]:
                    return True
                # Đường chéo
                if abs(sl[i] - sl[j]) == abs(i - j):
                    return True
        return False
    
    def count_conflicts(sl):
        """Đếm số xung đột"""
        cf = 0
        for i in range(len(sl)):
            for j in range(i+1, len(sl)):
                if sl[i] == sl[j]:
                    cf += 1
                if abs(sl[i] - sl[j]) == abs(i - j):
                    cf += 1
        return cf
    
    start = tuple()
    cur_bm = [start]
    pd = {start: []}
    
    max_it = 100
    it = 0
    
    while cur_bm and it < max_it:
        nxt_bm = []
        
        for st in cur_bm:
            # Kiểm tra xem đã hoàn thành chưa
            if len(st) == n and not has_conflicts(list(st)):
                path = pd[st]
                rp = []
                for ss in path + [st]:
                    fs = [None] * n
                    for i, c in enumerate(ss):
                        fs[i] = c
                    rp.append(fs)
                return rp
            
            # Tạo các trạng thái kế tiếp
            sc = get_successors(st)
            
            for s in sc:
                if s not in pd:
                    pd[s] = pd[st] + [st]
                    nxt_bm.append(s)
        
        # Chọn beam_width trạng thái tốt nhất
        if len(nxt_bm) > beam_width:
            ss = []
            for st in nxt_bm:
                sl = list(st)
                cf = count_conflicts(sl)
                # Heuristic: ưu tiên ít xung đột hơn
                sc = cf * 10 + (n - len(sl))
                ss.append((sc, st))
            
            ss.sort(key=lambda x: x[0])
            nxt_bm = [st for _, st in ss[:beam_width]]
        
        cur_bm = nxt_bm
        it += 1
    
    return []
