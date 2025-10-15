n = 8

def is_safe_forward(board, row, col):
    """Kiểm tra xem có thể đặt quân xe tại (row, col) không"""
    for i in range(row):
        if board[i] == col:  # Cùng cột
            return False
    return True

def count_valid_options(board, row):
    """Đếm số lựa chọn hợp lệ cho hàng hiện tại"""
    count = 0
    for col in range(n):
        if is_safe_forward(board, row, col):
            count += 1
    return count

def get_most_constrained_position(board, remaining_rows):
    """Forward tracking: chọn vị trí có ít lựa chọn nhất (Most Constrained Variable)"""
    if not remaining_rows:
        return None
    
    min_options = float('inf')
    best_row = None
    
    for row in remaining_rows:
        options = count_valid_options(board, row)
        if options < min_options:
            min_options = options
            best_row = row
    
    return best_row, min_options

def forward_tracking_recursive(board, remaining_rows, target, path_trace):
    """
    Forward Tracking - chọn biến có ít domain nhất trước
    """
    # Thêm trạng thái hiện tại
    path_trace.append(("STATE", len([x for x in board if x is not None]), board.copy()))
    
    # Base case: đã đặt hết
    if not remaining_rows:
        # Kiểm tra target constraint
        if target and all(target[i] is None or board[i] == target[i] for i in range(n)):
            path_trace.append(("SUCCESS", n, board.copy()))
            return True
        elif not target or all(x is None for x in target):
            path_trace.append(("SUCCESS", n, board.copy()))
            return True
        else:
            path_trace.append(("FAIL", n, board.copy()))
            return False
    
    # Forward tracking: chọn hàng có ít lựa chọn nhất
    result = get_most_constrained_position(board, remaining_rows)
    if result is None:
        return False
        
    chosen_row, options_count = result
    path_trace.append(("CHOOSE", chosen_row, board.copy(), f"Row {chosen_row} has {options_count} options"))
    
    # Thử tất cả giá trị hợp lệ cho hàng đã chọn
    valid_cols = []
    for col in range(n):
        if is_safe_forward(board, chosen_row, col):
            # Kiểm tra target constraint
            if target and target[chosen_row] is not None and col != target[chosen_row]:
                continue
            valid_cols.append(col)
    
    # Sắp xếp theo Least Constraining Value (giá trị ít hạn chế nhất)
    valid_cols.sort(key=lambda col: count_future_constraints(board, chosen_row, col, remaining_rows))
    
    for col in valid_cols:
        # Đặt quân xe
        board[chosen_row] = col
        path_trace.append(("PLACE", chosen_row, board.copy(), f"Place at ({chosen_row},{col})"))
        
        # Tạo remaining_rows mới
        new_remaining = remaining_rows.copy()
        new_remaining.remove(chosen_row)
        
        # Đệ quy
        if forward_tracking_recursive(board, new_remaining, target, path_trace):
            return True
        
        # Backtrack
        board[chosen_row] = None
        path_trace.append(("UNDO", chosen_row, board.copy(), f"Undo ({chosen_row},{col})"))
    
    return False

def count_future_constraints(board, row, col, remaining_rows):
    """Đếm số constraints mà việc đặt (row,col) sẽ tạo ra cho các hàng còn lại"""
    temp_board = board.copy()
    temp_board[row] = col
    
    total_constraints = 0
    for future_row in remaining_rows:
        if future_row != row:
            constraints = 0
            for future_col in range(n):
                if not is_safe_forward(temp_board, future_row, future_col):
                    constraints += 1
            total_constraints += constraints
    
    return total_constraints

def forward_tracking_target(tg):
    """Forward Tracking để tìm lời giải - thể hiện MCV và LCV heuristics"""
    board = [None] * n
    remaining_rows = list(range(n))
    path_trace = []
    
    success = forward_tracking_recursive(board, remaining_rows, tg, path_trace)
    
    if not success:
        return []
    
    # Chuyển đổi thành game format - smooth progression
    result = []
    
    for action_type, row_or_count, state, *info in path_trace:
        if action_type == "PLACE":
            # Tạo progressive state
            placed_count = len([x for x in state if x is not None])
            progressive_state = [None] * n
            
            # Sắp xếp lại theo thứ tự hàng để hiển thị smooth
            placed_positions = []
            for i in range(n):
                if state[i] is not None:
                    placed_positions.append((i, state[i]))
            
            # Sắp xếp theo hàng
            placed_positions.sort()
            
            # Tạo progressive display
            for idx, (row, col) in enumerate(placed_positions):
                if idx < placed_count:
                    progressive_state[row] = col
            
            result.append(progressive_state.copy())
        elif action_type == "SUCCESS":
            # Đảm bảo có final state
            if not result or result[-1] != state:
                result.append(state.copy())
            break
    
    return result

def forward_tracking_with_trace(tg):
    """Forward tracking với full trace để analysis"""
    board = [None] * n
    remaining_rows = list(range(n))
    path_trace = []
    
    success = forward_tracking_recursive(board, remaining_rows, tg, path_trace)
    
    return path_trace, success

def forward_tracking_simple():
    """Forward tracking đơn giản để tìm một lời giải"""
    board = [None] * n
    remaining_rows = list(range(n))
    path_trace = []
    
    if forward_tracking_recursive(board, remaining_rows, None, path_trace):
        # Tạo smooth result
        result = []
        for action_type, row_or_count, state, *info in path_trace:
            if action_type == "PLACE":
                placed_count = len([x for x in state if x is not None])
                progressive_state = [None] * n
                
                placed_positions = [(i, state[i]) for i in range(n) if state[i] is not None]
                placed_positions.sort()
                
                for idx, (row, col) in enumerate(placed_positions):
                    progressive_state[row] = col
                
                result.append(progressive_state.copy())
        return result
    
    return []

# Test function
def test_forward_tracking():
    """Test function để kiểm tra forward tracking"""
    print("=== FORWARD TRACKING TEST ===")
    
    # Test 1: Empty target
    print("\\nTest 1: Empty target")
    result1 = forward_tracking_target([None]*8)
    print(f"Steps: {len(result1)}")
    if result1:
        print(f"Solution: {result1[-1]}")
        print("First 3 steps:")
        for i in range(min(3, len(result1))):
            print(f"  Step {i}: {result1[i]}")
    
    # Test 2: Specific target
    print("\\nTest 2: Specific target [0,1,2,3,4,5,6,7]")
    result2 = forward_tracking_target([0,1,2,3,4,5,6,7])
    print(f"Steps: {len(result2)}")
    if result2:
        print(f"Solution: {result2[-1]}")
    
    # Test 3: Complex target
    print("\\nTest 3: Complex target [7,6,5,4,3,2,1,0]")
    result3 = forward_tracking_target([7,6,5,4,3,2,1,0])
    print(f"Steps: {len(result3)}")
    if result3:
        print(f"Solution: {result3[-1]}")
    
    # Test 4: With detailed trace
    print("\\nTest 4: Trace analysis")
    trace, success = forward_tracking_with_trace([0,1,2,3,4,5,6,7])
    print(f"Success: {success}")
    print(f"Total trace steps: {len(trace)}")
    
    # Show decision making process
    choose_steps = [step for step in trace if step[0] == "CHOOSE"]
    print(f"Decision points: {len(choose_steps)}")
    for i, step in enumerate(choose_steps[:3]):
        print(f"  Decision {i}: {step[3] if len(step) > 3 else 'No info'}")

if __name__ == "__main__":
    test_forward_tracking()
