"""
Thuật toán Minimax Decision cho bài toán 8 quân xe
Thuật toán đối kháng với 2 người chơi: MAX và MIN
"""

from .utils import n

def evaluate_board(board):
    """
    Hàm đánh giá bàn cờ
    Trả về điểm dựa trên số xung đột giữa các quân xe
    """
    if None in board:
        # Chưa đặt đủ quân xe
        conflicts = 0
        placed = 0
        for i in range(n):
            if board[i] is not None:
                placed += 1
                for j in range(i + 1, n):
                    if board[j] is not None:
                        # Kiểm tra cùng cột (cùng hàng không thể vì mỗi hàng 1 quân)
                        if board[i] == board[j]:
                            conflicts += 1
        
        # Điểm = số quân đã đặt - số xung đột
        return placed * 10 - conflicts * 5
    else:
        # Đã đặt đủ 8 quân
        conflicts = 0
        for i in range(n):
            for j in range(i + 1, n):
                # Kiểm tra cùng cột
                if board[i] == board[j]:
                    conflicts += 1
        
        if conflicts == 0:
            return 100  # Trạng thái hoàn hảo
        else:
            return 80 - conflicts * 10

def get_possible_moves(board, row):
    """
    Lấy các nước đi có thể cho hàng hiện tại
    """
    moves = []
    for col in range(n):
        # Kiểm tra xem cột này đã có quân xe chưa
        is_safe = True
        for r in range(row):
            if board[r] == col:
                is_safe = False
                break
        
        if is_safe:
            moves.append(col)
    
    return moves

def minimax_min(board, row, depth, max_depth):
    """
    Hàm MIN - chọn trạng thái xấu nhất cho MAX
    """
    # Base case
    if row >= n or depth >= max_depth:
        return evaluate_board(board), board.copy()
    
    min_value = float('inf')
    best_board = board.copy()
    
    moves = get_possible_moves(board, row)
    if not moves:
        return evaluate_board(board), board.copy()
    
    for col in moves:
        new_board = board.copy()
        new_board[row] = col
        
        value, result_board = minimax_max(new_board, row + 1, depth + 1, max_depth)
        
        if value < min_value:
            min_value = value
            best_board = result_board.copy()
    
    return min_value, best_board

def minimax_max(board, row, depth, max_depth):
    """
    Hàm MAX - chọn trạng thái tốt nhất
    """
    # Base case
    if row >= n or depth >= max_depth:
        return evaluate_board(board), board.copy()
    
    max_value = float('-inf')
    best_board = board.copy()
    
    moves = get_possible_moves(board, row)
    if not moves:
        return evaluate_board(board), board.copy()
    
    for col in moves:
        new_board = board.copy()
        new_board[row] = col
        
        value, result_board = minimax_min(new_board, row + 1, depth + 1, max_depth)
        
        if value > max_value:
            max_value = value
            best_board = result_board.copy()
    
    return max_value, best_board

def minimax_target(ban_mau):
    """
    Thuật toán Minimax để tìm cách đặt 8 quân xe
    """
    # Khởi tạo bàn cờ trống
    board = [None] * n
    path = [board.copy()]
    
    # Bắt đầu từ hàng 0
    for row in range(n):
        moves = get_possible_moves(board, row)
        
        if not moves:
            # Không có nước đi hợp lệ, backtrack
            break
        
        # MAX chọn nước đi tốt nhất
        best_value = float('-inf')
        best_col = moves[0]
        
        for col in moves:
            temp_board = board.copy()
            temp_board[row] = col
            
            # MIN đánh giá
            value, _ = minimax_min(temp_board, row + 1, 0, 3)  # Giới hạn depth = 3
            
            if value > best_value:
                best_value = value
                best_col = col
        
        # Đặt quân xe
        board[row] = best_col
        path.append(board.copy())
        
        # Kiểm tra nếu đã hoàn thành
        if None not in board and evaluate_board(board) == 100:
            break
    
    return path

def minimax_visual_target(ban_mau):
    """
    Phiên bản visualization của Minimax
    Trả về từng bước đặt quân xe
    """
    return minimax_target(ban_mau)
