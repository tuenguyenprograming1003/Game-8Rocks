"""
AC-3 (Arc Consistency 3) algorithm for 8-Rooks CSP
Maintains arc consistency by removing inconsistent values from domains
"""
from collections import deque

def ac3_target(ban_mau):
    """
    Giải bài toán 8 quân xe bằng AC-3
    Trả về list các state từ initial đến goal (hoặc empty nếu không tìm thấy)
    """
    n = len(ban_mau)
    
    # Domain cho mỗi hàng - ban đầu mỗi hàng có thể đặt ở bất kỳ cột nào
    domains = {i: set(range(n)) for i in range(n)}
    
    # Thu hẹp domain dựa trên target
    for row, col in enumerate(ban_mau):
        if col is not None:
            domains[row] = {col}
    
    # Tạo list các arcs (cặp ràng buộc giữa 2 biến)
    arcs = deque()
    for i in range(n):
        for j in range(i + 1, n):
            arcs.append((i, j))
            arcs.append((j, i))
    
    # Tracking để visualization
    path = []
    path.append([None] * n)  # State ban đầu
    
    # AC-3 algorithm
    while arcs:
        (xi, xj) = arcs.popleft()
        
        if revise(domains, xi, xj):
            if len(domains[xi]) == 0:
                # Domain rỗng - không có solution
                return []
            
            # Tạo state hiện tại để visualization
            current_state = build_state_from_domains(domains, n)
            path.append(current_state)
            
            # Thêm lại các arcs liên quan
            for xk in range(n):
                if xk != xi and xk != xj:
                    arcs.append((xk, xi))
    
    # Sau khi AC-3, assign values từ domains
    final_state = []
    for i in range(n):
        if len(domains[i]) == 1:
            final_state.append(list(domains[i])[0])
        else:
            # Nếu còn nhiều giá trị, chọn giá trị đầu tiên
            final_state.append(min(domains[i]))
    
    # Kiểm tra và backtrack nếu cần
    if not is_valid_solution(final_state):
        final_state = backtrack_with_ac3(domains, n)
    
    path.append(final_state)
    return path

def revise(domains, xi, xj):
    """
    Loại bỏ các giá trị không nhất quán từ domain của xi
    Returns True nếu domain của xi bị thay đổi
    """
    revised = False
    to_remove = set()
    
    for val_i in domains[xi]:
        # Kiểm tra xem có tồn tại giá trị trong domain của xj
        # sao cho constraint được thỏa mãn
        satisfies = False
        for val_j in domains[xj]:
            if val_i != val_j:  # Constraint: không cùng cột
                satisfies = True
                break
        
        if not satisfies:
            to_remove.add(val_i)
            revised = True
    
    domains[xi] -= to_remove
    return revised

def build_state_from_domains(domains, n):
    """
    Tạo state từ domains hiện tại
    Nếu domain có 1 giá trị thì assign, ngược lại để None
    """
    state = []
    for i in range(n):
        if len(domains[i]) == 1:
            state.append(list(domains[i])[0])
        elif len(domains[i]) > 1:
            # Chọn giá trị nhỏ nhất từ domain
            state.append(min(domains[i]))
        else:
            state.append(None)
    return state

def is_valid_solution(state):
    """
    Kiểm tra xem state có hợp lệ không
    """
    if None in state:
        return False
    
    n = len(state)
    for i in range(n):
        for j in range(i + 1, n):
            if state[i] == state[j]:  # Cùng cột
                return False
    return True

def backtrack_with_ac3(domains, n):
    """
    Backtracking với AC-3 để tìm solution
    """
    assignment = {}
    if backtrack_recursive(assignment, domains, n):
        return [assignment[i] for i in range(n)]
    return [None] * n

def backtrack_recursive(assignment, domains, n):
    """
    Recursive backtracking
    """
    if len(assignment) == n:
        return True
    
    # Chọn variable chưa assign (Most Constrained Variable)
    unassigned = [i for i in range(n) if i not in assignment]
    var = min(unassigned, key=lambda x: len(domains[x]))
    
    for value in sorted(domains[var]):
        if is_consistent(var, value, assignment):
            assignment[var] = value
            
            # Thử tiếp
            if backtrack_recursive(assignment, domains, n):
                return True
            
            # Backtrack
            del assignment[var]
    
    return False

def is_consistent(var, value, assignment):
    """
    Kiểm tra xem assign var=value có nhất quán với assignment hiện tại không
    """
    for assigned_var, assigned_value in assignment.items():
        if assigned_value == value:  # Cùng cột
            return False
    return True
