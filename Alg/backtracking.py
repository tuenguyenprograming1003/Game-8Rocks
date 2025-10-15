n = 8

def is_safe_backtrack(board, row, col):
    """Kiểm tra xem có thể đặt quân xe tại (row, col) không - chỉ kiểm tra cùng cột"""
    for i in range(row):
        if board[i] == col:  # Cùng cột
            return False
    return True

def backtrack_with_stack(target, path_trace):
    """
    Backtracking sử dụng stack thay vì đệ quy
    Stack lưu: (board_state, row, col_to_try)
    """
    board = [None] * n
    stack = [(board.copy(), 0, 0)]  # (state, row, next_col_to_try)
    
    path_trace.append(("INIT", 0, board.copy()))
    
    while stack:
        board, row, col = stack.pop()
        
        # Base case: đã đặt hết 8 quân
        if row == n:
            # Kiểm tra có match với target không
            if target and all(target[i] is None or board[i] == target[i] for i in range(n)):
                path_trace.append(("SUCCESS", row, board.copy()))
                return board
            elif not target or all(x is None for x in target):
                path_trace.append(("SUCCESS", row, board.copy()))
                return board
            else:
                path_trace.append(("FAIL", row, board.copy()))
                continue
        
        # Đánh dấu đang thử hàng này
        path_trace.append(("TRY_ROW", row, board.copy()))
        
        # Tìm cột hợp lệ bắt đầu từ col
        found = False
        for try_col in range(col, n):
            # Nếu target đã chỉ định cột cho hàng này
            if target and target[row] is not None and try_col != target[row]:
                continue
            
            if is_safe_backtrack(board, row, try_col):
                # Tạo state mới với quân xe được đặt
                new_board = board.copy()
                new_board[row] = try_col
                path_trace.append(("PLACE", row, new_board.copy(), f"Place at ({row},{try_col})"))
                
                # Push state để backtrack nếu cần (thử cột tiếp theo)
                if try_col + 1 < n:
                    stack.append((board.copy(), row, try_col + 1))
                
                # Push state để tiếp tục với hàng tiếp theo
                stack.append((new_board.copy(), row + 1, 0))
                found = True
                break
        
        if not found and row > 0:
            # Không tìm được cột hợp lệ - backtrack
            path_trace.append(("BACKTRACK", row, board.copy(), f"No valid column for row {row}"))
    
    return None

def backtracking_target(tg):
    """Backtracking để tìm lời giải - thể hiện quá trình thử và quay lui"""
    path_trace = []
    
    # Chạy backtracking với stack
    result_board = backtrack_with_stack(tg, path_trace)
    
    if not result_board:
        return []
    
    # Chuyển đổi trace thành game format
    # Chỉ lấy các states PLACE và SUCCESS để tạo smooth progression
    result = []
    current_board = [None] * n
    
    for action_tuple in path_trace:
        action_type = action_tuple[0]
        row = action_tuple[1]
        state = action_tuple[2]
        
        if action_type == "PLACE":
            # Tạo progressive state
            progressive_state = [None] * n
            for i in range(row + 1):
                if state[i] is not None:
                    progressive_state[i] = state[i]
            result.append(progressive_state.copy())
        elif action_type == "SUCCESS":
            # Đảm bảo có solution cuối cùng
            if not result or result[-1] != state:
                result.append(state.copy())
            break
    
    return result

def backtracking_with_trace(tg):
    """Backtracking với full trace để debug - trả về detailed steps"""
    path_trace = []
    
    result_board = backtrack_with_stack(tg, path_trace)
    
    return path_trace, result_board is not None

def backtracking_simple():
    """Backtracking đơn giản để tìm một lời giải bất kỳ"""
    board = [None] * n
    path_trace = []
    
    def simple_backtrack(row):
        path_trace.append(("STATE", row, board.copy()))
        
        if row == n:
            return True
            
        for col in range(n):
            if is_safe_backtrack(board, row, col):
                board[row] = col
                path_trace.append(("PLACE", row, board.copy()))
                
                if simple_backtrack(row + 1):
                    return True
                    
                board[row] = None
                path_trace.append(("BACKTRACK", row, board.copy()))
        
        return False
    
    if simple_backtrack(0):
        # Tạo smooth progression
        result = []
        for action_type, row, state in path_trace:
            if action_type == "PLACE":
                progressive_state = [None] * n
                for i in range(row + 1):
                    if state[i] is not None:
                        progressive_state[i] = state[i]
                result.append(progressive_state.copy())
        return result
    
    return []

# Test function
def test_backtracking():
    """Test function để kiểm tra backtracking"""
    print("=== BACKTRACKING TEST ===")
    
    # Test 1: Empty target
    print("\\nTest 1: Empty target")
    result1 = backtracking_target([None]*8)
    print(f"Steps: {len(result1)}")
    if result1:
        print(f"Solution: {result1[-1]}")
    
    # Test 2: Specific target
    print("\\nTest 2: Specific target [0,1,2,3,4,5,6,7]")
    result2 = backtracking_target([0,1,2,3,4,5,6,7])
    print(f"Steps: {len(result2)}")
    if result2:
        print(f"Solution: {result2[-1]}")
    
    # Test 3: With trace
    print("\\nTest 3: Trace for target [0,1,2,3,4,5,6,7]")
    trace, success = backtracking_with_trace([0,1,2,3,4,5,6,7])
    print(f"Success: {success}")
    print(f"Total trace steps: {len(trace)}")
    
    # Show first few trace steps
    for i, step in enumerate(trace[:10]):
        action_type = step[0]
        row = step[1] 
        state = step[2]
        info = step[3] if len(step) > 3 else ""
        print(f"  {i}: {action_type} row={row} {info}")

if __name__ == "__main__":
    test_backtracking()
