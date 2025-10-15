from collections import deque

n = 8

class BeliefState:
    """
    Lớp biểu diễn belief state - tập hợp các trạng thái có thể
    """
    def __init__(self, possible_states=None):
        if possible_states is None:
            # Khởi tạo với trạng thái rỗng
            self.states = [tuple()]
        else:
            self.states = list(set(possible_states))  # Loại bỏ trùng lặp
    
    def __len__(self):
        return len(self.states)
    
    def is_goal(self, target):
        """Kiểm tra xem có trạng thái nào trong belief state là goal"""
        target_tuple = tuple(target)
        return any(len(state) == n and tuple(state) == target_tuple 
                  for state in self.states)
    
    def get_successors(self):
        """Lấy tất cả belief state kế tiếp bằng DFS"""
        next_states = []
        
        for state in self.states:
            if len(state) < n:
                # Thêm một quân xe vào hàng tiếp theo
                next_row = len(state)
                for col in range(n):
                    # Kiểm tra xung đột
                    valid = True
                    for i, existing_col in enumerate(state):
                        if existing_col == col:  # Cùng cột
                            valid = False
                            break
                        # Không kiểm tra đường chéo vì đây là 8 quân xe, không phải 8 quân hậu
                    
                    if valid:
                        new_state = tuple(list(state) + [col])
                        next_states.append(new_state)
        
        return BeliefState(next_states)
    
    def prune_unlikely(self, target, max_states=8):
        """Cắt tỉa các trạng thái không có khả năng"""
        if len(self.states) <= max_states:
            return self
        
        # Tính điểm cho mỗi trạng thái dựa trên khoảng cách đến target
        scored_states = []
        target_tuple = tuple(target)
        
        for state in self.states:
            score = 0
            # Điểm dựa trên số vị trí đã đúng
            for i in range(min(len(state), len(target_tuple))):
                if i < len(state) and state[i] == target_tuple[i]:
                    score += 10
            
            # Thưởng cho trạng thái dài hơn (gần hoàn thành hơn)
            score += len(state) * 2
            
            scored_states.append((score, state))
        
        # Sắp xếp theo điểm và lấy top states
        scored_states.sort(key=lambda x: x[0], reverse=True)
        best_states = [state for _, state in scored_states[:max_states]]
        
        return BeliefState(best_states)

def belief_state_dfs(tg, max_depth=15, max_belief_size=10):
    """
    Belief-state search kết hợp với DFS
    """
    target_tuple = tuple(tg)
    initial_belief = BeliefState()
    
    # DFS với stack chứa (belief_state, path, depth)
    stack = [(initial_belief, [], 0)]
    visited = set()
    
    while stack:
        current_belief, path, depth = stack.pop()
        
        # Kiểm tra độ sâu
        if depth > max_depth:
            continue
        
        # Tạo key để tránh lặp lại
        belief_key = tuple(sorted(current_belief.states))
        if belief_key in visited:
            continue
        visited.add(belief_key)
        
        # Kiểm tra goal
        if current_belief.is_goal(tg):
            # Tìm trạng thái goal trong belief state
            for state in current_belief.states:
                if len(state) == n and tuple(state) == target_tuple:
                    # Tái tạo đường đi
                    result_path = []
                    
                    # Thêm các bước trung gian
                    for i in range(1, len(state) + 1):
                        step_state = [None] * n
                        for j in range(i):
                            step_state[j] = state[j]
                        result_path.append(step_state)
                    
                    return result_path if result_path else [list(state)]
        
        # Tạo belief state kế tiếp
        next_belief = current_belief.get_successors()
        
        # Cắt tỉa belief state nếu quá lớn
        if len(next_belief) > max_belief_size:
            next_belief = next_belief.prune_unlikely(tg, max_belief_size)
        
        if len(next_belief) > 0:
            stack.append((next_belief, path + [current_belief], depth + 1))
    
    return []

def belief_state_target(tg):
    """Belief-state search để tìm lời giải cho bài toán 8 quân xe"""
    # Nếu target toàn None, tìm lời giải tổng quát
    if all(x is None for x in tg):
        # Tìm một lời giải hợp lệ bằng DFS đơn giản cho 8 quân xe
        def is_safe_simple(board, row, col):
            for i in range(row):
                if board[i] == col:  # Chỉ kiểm tra cùng cột, không kiểm tra đường chéo
                    return False
            return True
        
        def solve_simple(board, row):
            if row == 8:
                return board.copy()
            
            for col in range(8):
                if is_safe_simple(board, row, col):
                    board[row] = col
                    result = solve_simple(board, row + 1)
                    if result:
                        return result
                    board[row] = None
            return None
        
        board = [None] * 8
        solution = solve_simple(board, 0)
        if solution:
            # Tạo path step-by-step
            path = []
            for i in range(8):
                step = [None] * 8
                for j in range(i + 1):
                    step[j] = solution[j]
                path.append(step)
            return path
        return []
    
    # Nếu có target cụ thể (có thể partial), sử dụng DFS với constraint cho 8 quân xe
    def is_safe_constraint(board, row, col):
        for i in range(row):
            if board[i] == col:  # Chỉ kiểm tra cùng cột, không kiểm tra đường chéo
                return False
        return True
    
    def solve_with_constraint(board, row, target):
        if row == 8:
            # Kiểm tra match với target
            for i in range(8):
                if target[i] is not None and board[i] != target[i]:
                    return None
            return board.copy()
        
        # Nếu target[row] đã được chỉ định, chỉ thử giá trị đó
        if target[row] is not None:
            col = target[row]
            if is_safe_constraint(board, row, col):
                board[row] = col
                result = solve_with_constraint(board, row + 1, target)
                if result:
                    return result
                board[row] = None
        else:
            # Thử tất cả các giá trị có thể
            for col in range(8):
                if is_safe_constraint(board, row, col):
                    board[row] = col
                    result = solve_with_constraint(board, row + 1, target)
                    if result:
                        return result
                    board[row] = None
        return None
    
    board = [None] * 8
    solution = solve_with_constraint(board, 0, tg)
    if solution:
        # Tạo path step-by-step
        path = []
        for i in range(8):
            step = [None] * 8
            for j in range(i + 1):
                step[j] = solution[j]
            path.append(step)
        return path
    
    return []
