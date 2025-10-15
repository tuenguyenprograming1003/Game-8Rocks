from collections import deque
import random

n = 8

def is_safe_observation(board, row, col):
    """Kiểm tra xem có thể đặt quân xe tại (row, col) không"""
    for i in range(row):
        if board[i] == col:  # Cùng cột
            return False
    return True

class ObservationState:
    """
    Lớp biểu diễn trạng thái với full observation - biết chính xác trạng thái hiện tại
    """
    def __init__(self, board, observed_positions=None):
        self.board = board.copy()
        # Observed positions: những vị trí đã được observe/confirm
        self.observed_positions = observed_positions or set()
        self.action_history = []  # Lưu lại các action đã thực hiện
        
    def copy(self):
        new_state = ObservationState(self.board, self.observed_positions.copy())
        new_state.action_history = self.action_history.copy()
        return new_state
    
    def is_complete(self):
        """Kiểm tra xem đã đặt đủ 8 quân xe chưa"""
        return all(x is not None for x in self.board)
    
    def is_valid(self):
        """Kiểm tra tính hợp lệ của trạng thái hiện tại"""
        for i in range(n):
            if self.board[i] is not None:
                for j in range(i+1, n):
                    if self.board[j] is not None and self.board[i] == self.board[j]:
                        return False
        return True
    
    def get_next_row(self):
        """Lấy hàng tiếp theo cần đặt quân xe"""
        for i in range(n):
            if self.board[i] is None:
                return i
        return None
    
    def place_piece(self, row, col, is_observed=True):
        """Đặt quân xe và observe action"""
        new_state = self.copy()
        new_state.board[row] = col
        if is_observed:
            new_state.observed_positions.add(row)
        new_state.action_history.append(("PLACE", row, col, is_observed))
        return new_state
    
    def observe_position(self, row):
        """Observe một vị trí cụ thể - confirm thông tin"""
        new_state = self.copy()
        new_state.observed_positions.add(row)
        new_state.action_history.append(("OBSERVE", row, self.board[row], True))
        return new_state

def search_with_observations_bfs(target):
    """
    Searching with Observations sử dụng BFS
    - Biết chính xác trạng thái hiện tại
    - Có thể observe để confirm thông tin
    - Khác với belief state - không có uncertainty
    """
    initial_board = [None] * n
    initial_state = ObservationState(initial_board)
    
    queue = deque([(initial_state, [])])
    visited = set()
    observation_steps = []
    
    while queue:
        current_state, path = queue.popleft()
        
        # Tạo key dựa trên trạng thái và observed positions
        state_key = (tuple(current_state.board), tuple(sorted(current_state.observed_positions)))
        if state_key in visited:
            continue
        visited.add(state_key)
        
        # Lưu lại step cho visualization
        observation_steps.append({
            'state': current_state.board.copy(),
            'observed': current_state.observed_positions.copy(),
            'action_history': current_state.action_history.copy()
        })
        
        # Kiểm tra goal
        if current_state.is_complete():
            if target and current_state.board == target:
                return create_observation_path(observation_steps)
            elif not target or all(x is None for x in target):
                return create_observation_path(observation_steps)
        
        # Tìm hàng tiếp theo để đặt
        next_row = current_state.get_next_row()
        if next_row is not None:
            # Thử tất cả cột hợp lệ
            for col in range(n):
                if target and target[next_row] is not None and col != target[next_row]:
                    continue
                    
                if is_safe_observation(current_state.board, next_row, col):
                    # Tạo state mới với piece được đặt
                    new_state = current_state.place_piece(next_row, col, is_observed=True)
                    
                    if new_state.is_valid():
                        queue.append((new_state, path + [(next_row, col)]))
    
    return []

def search_with_observations_dfs(target, max_depth=15):
    """
    Searching with Observations sử dụng DFS với observation strategy
    """
    initial_board = [None] * n
    initial_state = ObservationState(initial_board)
    
    stack = [(initial_state, [], 0)]
    visited = set()
    observation_steps = []
    
    while stack:
        current_state, path, depth = stack.pop()
        
        if depth > max_depth:
            continue
            
        state_key = (tuple(current_state.board), tuple(sorted(current_state.observed_positions)))
        if state_key in visited:
            continue
        visited.add(state_key)
        
        # Record observation step
        observation_steps.append({
            'state': current_state.board.copy(),
            'observed': current_state.observed_positions.copy(),
            'action_history': current_state.action_history.copy(),
            'depth': depth
        })
        
        # Check goal
        if current_state.is_complete():
            if target and current_state.board == target:
                return create_observation_path(observation_steps)
            elif not target or all(x is None for x in target):
                return create_observation_path(observation_steps)
        
        # Get next position to fill
        next_row = current_state.get_next_row()
        if next_row is not None:
            # Try all valid columns (in reverse order for DFS)
            for col in reversed(range(n)):
                if target and target[next_row] is not None and col != target[next_row]:
                    continue
                    
                if is_safe_observation(current_state.board, next_row, col):
                    # Create new state with observation
                    new_state = current_state.place_piece(next_row, col, is_observed=True)
                    
                    # Add observation step
                    new_state = new_state.observe_position(next_row)
                    
                    if new_state.is_valid():
                        stack.append((new_state, path + [(next_row, col)], depth + 1))
    
    return []

def create_observation_path(observation_steps):
    """
    Tạo path cho game từ observation steps
    Thể hiện quá trình observation rõ ràng
    """
    if not observation_steps:
        return []
    
    path = []
    
    for step in observation_steps:
        state = step['state']
        # Tạo progressive state
        progressive_state = [None] * n
        placed_count = sum(1 for x in state if x is not None)
        
        # Fill theo thứ tự để tạo smooth animation
        filled = 0
        for i in range(n):
            if state[i] is not None and filled < placed_count:
                progressive_state[i] = state[i]
                filled += 1
        
        path.append(progressive_state)
        
        # Dừng khi đã có solution hoàn chỉnh
        if all(x is not None for x in state):
            break
    
    return path

def observations_target(tg):
    """
    Main function cho Searching with Observations
    """
    # Nếu target toàn None, tìm lời giải tổng quát
    if all(x is None for x in tg):
        return search_with_observations_simple()
    
    # Thử BFS trước (faster for specific targets)
    result = search_with_observations_bfs(tg)
    if result:
        return result
    
    # Nếu BFS không tìm được, thử DFS
    return search_with_observations_dfs(tg)

def search_with_observations_simple():
    """
    Searching with Observations cho bài toán tổng quát
    """
    def simple_place(board, row):
        if row == n:
            return [board.copy()]
        
        for col in range(n):
            if is_safe_observation(board, row, col):
                board[row] = col
                result = simple_place(board, row + 1)
                if result:
                    return result
                board[row] = None
        return None
    
    board = [None] * n
    solution = simple_place(board, 0)
    
    if solution:
        # Tạo step-by-step path với observation characteristic
        path = []
        final_solution = solution[0]
        
        for i in range(n):
            step = [None] * n
            for j in range(i + 1):
                step[j] = final_solution[j]
            path.append(step)
        
        return path
    
    return []

# Test function
def test_observations():
    """Test function để kiểm tra searching with observations"""
    print("=== SEARCHING WITH OBSERVATIONS TEST ===")
    
    # Test 1: Empty target
    print("\\nTest 1: Empty target")
    result1 = observations_target([None]*8)
    print(f"Steps: {len(result1)}")
    if result1:
        print(f"Solution: {result1[-1]}")
    
    # Test 2: Specific target
    print("\\nTest 2: Specific target [0,1,2,3,4,5,6,7]")
    result2 = observations_target([0,1,2,3,4,5,6,7])
    print(f"Steps: {len(result2)}")
    if result2:
        print(f"Solution: {result2[-1]}")
        print(f"Match target: {result2[-1] == [0,1,2,3,4,5,6,7]}")
    
    # Test 3: Complex target
    print("\\nTest 3: Complex target [7,6,5,4,3,2,1,0]")
    result3 = observations_target([7,6,5,4,3,2,1,0])
    print(f"Steps: {len(result3)}")
    if result3:
        print(f"Solution: {result3[-1]}")

if __name__ == "__main__":
    test_observations()
