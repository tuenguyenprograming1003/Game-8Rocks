n = 8

def is_safe(board, row, col):
    """Kiểm tra xem có thể đặt quân xe tại (row, col) không - chỉ kiểm tra hàng và cột"""
    for i in range(row):
        if board[i] == col:  # Cùng cột
            return False
        # Không kiểm tra đường chéo vì đây là quân xe, không phải quân hậu
    return True

def and_or_search_recursive(board, row, target):
    """
    AND-OR Search đệ quy
    - OR nodes: chọn một nước đi (có nhiều lựa chọn) 
    - AND nodes: phải thỏa mãn tất cả điều kiện
    """
    if row == n:
        # Đã hoàn thành bàn cờ, kiểm tra có match với target không
        # Nếu target[i] là None, chấp nhận bất kỳ giá trị nào
        # Nếu target[i] có giá trị, phải khớp chính xác
        for i in range(n):
            if target[i] is not None and board[i] != target[i]:
                return False, []
        return True, [board.copy()]
    
    # OR node: thử tất cả các nước đi hợp lệ
    for col in range(n):
        # Nếu target[row] đã được chỉ định, chỉ thử giá trị đó
        if target[row] is not None and col != target[row]:
            continue
            
        if is_safe(board, row, col):
            board[row] = col
            
            # AND node: kiểm tra nước đi này có dẫn đến lời giải không
            success, path = and_or_search_recursive(board, row + 1, target)
            
            if success:
                return True, [board.copy()] + path
            
            board[row] = None  # Backtrack
    
    return False, []

def and_or_search_target(tg):
    """AND-OR Search để tìm lời giải cho bài toán 8 quân xe"""
    # Nếu target toàn None, tìm lời giải tổng quát
    if all(x is None for x in tg):
        solution = and_or_search_general()
        if solution:
            # Chuyển đổi thành path step-by-step từ lời giải cuối cùng
            final_solution = solution[-1]  # Lời giải hoàn chỉnh
            path = []
            for i in range(n):
                step = [None] * n
                for j in range(i + 1):
                    step[j] = final_solution[j]
                path.append(step)
            return path
        return []
    
    # Nếu có target cụ thể, tìm đường đến target đó
    board = [None] * n
    success, path = and_or_search_recursive(board, 0, tg)
    
    if success and path:
        # Chuyển đổi path thành step-by-step progression
        final_solution = path[-1]  # Lời giải cuối cùng
        step_path = []
        for i in range(n):
            step = [None] * n
            for j in range(i + 1):
                step[j] = final_solution[j]
            step_path.append(step)
        return step_path
    else:
        return []

def and_or_search_general():
    """AND-OR Search để giải bài toán 8 quân xe tổng quát"""
    def solve_recursive(board, row):
        if row == n:
            return True, [board.copy()]
        
        # OR node: thử tất cả các nước đi hợp lệ
        for col in range(n):
            if is_safe(board, row, col):
                board[row] = col
                
                # AND node: kiểm tra nước đi này
                success, path = solve_recursive(board, row + 1)
                
                if success:
                    return True, [board.copy()] + path
                
                board[row] = None  # Backtrack
        
        return False, []
    
    board = [None] * n
    success, path = solve_recursive(board, 0)
    
    if success:
        return path
    else:
        return []
