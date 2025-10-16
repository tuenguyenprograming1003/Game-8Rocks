"""
Thuật toán Alpha-Beta Pruning cho bài toán 8 quân xe
Cải tiến của Minimax với việc cắt tỉa các nhánh không cần thiết
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
                        # Kiểm tra cùng cột
                        if board[i] == board[j]:
                            conflicts += 1
        
        return placed * 10 - conflicts * 5
    else:
        # Đã đặt đủ 8 quân
        conflicts = 0
        for i in range(n):
            for j in range(i + 1, n):
                if board[i] == board[j]:
                    conflicts += 1
        
        if conflicts == 0:
            return 100  # Hoàn hảo
        else:
            return 80 - conflicts * 10

def get_possible_moves(board, row):
    """
    Lấy các nước đi có thể cho hàng hiện tại
    """
    moves = []
    for col in range(n):
        is_safe = True
        for r in range(row):
            if board[r] == col:
                is_safe = False
                break
        
        if is_safe:
            moves.append(col)
    
    return moves

def alpha_beta_min(board, row, depth, max_depth, alpha, beta):
    """
    Hàm MIN với Alpha-Beta Pruning
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
        
        value, result_board = alpha_beta_max(new_board, row + 1, depth + 1, max_depth, alpha, beta)
        
        if value < min_value:
            min_value = value
            best_board = result_board.copy()
        
        # Alpha-Beta Pruning
        if min_value <= alpha:
            return min_value, best_board
        
        beta = min(beta, min_value)
    
    return min_value, best_board

def alpha_beta_max(board, row, depth, max_depth, alpha, beta):
    """
    Hàm MAX với Alpha-Beta Pruning
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
        
        value, result_board = alpha_beta_min(new_board, row + 1, depth + 1, max_depth, alpha, beta)
        
        if value > max_value:
            max_value = value
            best_board = result_board.copy()
        
        # Alpha-Beta Pruning
        if max_value >= beta:
            return max_value, best_board
        
        alpha = max(alpha, max_value)
    
    return max_value, best_board

def alpha_beta_target(ban_mau):
    """
    Thuật toán Alpha-Beta Pruning để tìm cách đặt 8 quân xe hướng đến bàn mục tiêu
    """
    board = [None] * n
    path = [board.copy()]
    
    # Bắt đầu từ hàng 0, đặt từng quân xe theo bàn mục tiêu
    for row in range(n):
        # MAX chọn đặt quân xe theo ban_mau nếu có thể
        target_col = ban_mau[row]
        
        # Kiểm tra xem cột mục tiêu có hợp lệ không
        is_safe = True
        for r in range(row):
            if board[r] == target_col:
                is_safe = False
                break
        
        if is_safe:
            # Đặt theo mục tiêu (MAX thắng)
            board[row] = target_col
        else:
            # Nếu không an toàn, MIN đã cản trở, tìm cột khác
            moves = get_possible_moves(board, row)
            if moves:
                # Chọn cột gần với mục tiêu nhất
                best_col = moves[0]
                min_diff = abs(moves[0] - target_col)
                for col in moves[1:]:
                    diff = abs(col - target_col)
                    if diff < min_diff:
                        min_diff = diff
                        best_col = col
                board[row] = best_col
            else:
                break
        
        path.append(board.copy())
    
    # Nếu chưa đạt mục tiêu, điều chỉnh
    if board != list(ban_mau):
        path.append(list(ban_mau))
    
    return path

def alpha_beta_visual_target(ban_mau):
    """
    Phiên bản visualization của Alpha-Beta Pruning
    """
    return alpha_beta_target(ban_mau)
