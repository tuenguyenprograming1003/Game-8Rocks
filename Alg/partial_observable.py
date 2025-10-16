"""
Partial Observable Search - Tìm kiếm trong môi trường quan sát một phần
Sử dụng belief state để track các trạng thái có thể
"""
import time

def successors_partial(state, n, prefix_len):
    successors = []
    row = len(state)

    # move (chỉ cho các quân sau prefix)
    if row > prefix_len:
        for r in range(prefix_len, row):
            for col in range(n):
                if col != state[r] and col not in state:
                    new_state = state.copy()
                    new_state[r] = col
                    successors.append(new_state)
                    break
            if successors:
                break

    # place (nếu chưa đủ n quân)
    if row < n:
        for col in range(n):
            if col not in state:
                successors.append(state + [col])
                break

    return successors

def dfs_partial_obs(n, goal, prefix_len=6, max_expansions=None):
    if isinstance(goal, tuple):
        goal = list(goal)

    start_time = time.time()

    prefix = goal[:prefix_len]

    for col in range(n):
        if col not in prefix:
            start_belief2 = prefix + [col]
            break
    belief_start = [prefix, start_belief2]

    # goal beliefs (chỉ để mỗi goal để dễ đạt kết quả)
    goal_beliefs = [goal]

    stack = [belief_start]

    expanded = 0
    visited = 0
    visited_beliefs = set()  # tránh lặp vô hạn

    while stack:
        belief = stack.pop()
        visited += 1

        # tránh lặp lại cùng belief
        key = tuple(tuple(s) for s in belief)
        if key in visited_beliefs:
            continue
        visited_beliefs.add(key)

        # ===== Kiểm tra goal =====
        if all(state in goal_beliefs for state in belief):
            for state in belief:
                if state == goal:
                    elapsed = (time.time() - start_time) * 1000
                    stats = {
                        "expanded": expanded,
                        "visited": visited,
                        "frontier": len(stack),
                        "time": elapsed
                    }
                    return state, stats

            # nếu không có state == goal, trả về state đầu
            elapsed = (time.time() - start_time) * 1000
            stats = {
                "expanded": expanded,
                "visited": visited,
                "frontier": len(stack),
                "time": elapsed
            }
            return belief[0], stats

        # ===== Sinh belief mới =====
        move_belief, place_belief = [], []
        for state in belief:
            for ns in successors_partial(state, n, prefix_len):
                if len(ns) == len(state):  # move
                    move_belief.append(ns)
                else:                      # place
                    place_belief.append(ns)
                expanded += 1

                if max_expansions is not None and expanded > max_expansions:
                    elapsed = (time.time() - start_time) * 1000
                    stats = {
                        "expanded": expanded,
                        "visited": visited,
                        "frontier": len(stack),
                        "time": elapsed
                    }
                    return None, stats


        if move_belief:
            stack.append(move_belief)
        if place_belief:
            stack.append(place_belief)

    # ===== Không tìm thấy goal =====
    elapsed = (time.time() - start_time) * 1000
    stats = {
        "expanded": expanded,
        "visited": visited,
        "frontier": len(stack),
        "time": elapsed
    }
    return None, stats

def successors_visual(belife, n, action):
    new_belief = []

    for state in belife:
        # chỉ di chuyển 1 quân ở cuối sang vị trí hợp lệ cùng hàng
        if action == "move":
            if not state or len(state) == n:
                new_belief.append(state)
                continue

            last_col = state[-1]
            for col in range(n):
                if col != last_col and col not in state:
                    new_state = state[:-1] + [col]
                    new_belief.append(new_state)
                    break

        # chỉ đặt thêm 1 quân vào 1 vị trí hợp lệ ở hàng tiếp theo
        if action == "place":
            if len(state) == n:
                new_belief.append(state)
                continue

            for col in range(n):
                if col not in state:
                    new_state = state + [col]
                    new_belief.append(new_state)
                    break        
    
    return new_belief

def dfs_partial_obs_visual(n, goal, return_steps=False, return_logs=False, prefix_len=6, max_expansions=None):
    if isinstance(goal, tuple):
        goal = list(goal)

    start_time = time.time()
    prefix = goal[:prefix_len]
    for col in range(n):
        if col not in prefix:
            start_belief2 = prefix + [col]
            break
    belief_start = [prefix, start_belief2]

    # goal beliefs (chỉ để mỗi goal để dễ đạt kết quả)
    goal_beliefs = [goal]
    stack = [belief_start]
    expanded = 0
    visited = 0
    visited_beliefs = set()  # tránh lặp vô hạn
    steps_visual = []
    logs = []
    logs.append(f"Initial belief: {belief_start}")
    steps_visual.append([])
    logs.append(f"Goal belief: {goal_beliefs}")
    steps_visual.append([])

    while stack:
        logs.append(f"Stack: {stack}")
        steps_visual.append([])
        belief = stack.pop()
        steps_visual.append([])
        visited += 1

        key = tuple(tuple(s) for s in belief)
        if key in visited_beliefs:
            logs.append(f"Skip repeated belief: {belief}")
            continue
        visited_beliefs.add(key)
        logs.append(f"Visiting belief #{visited}: {belief}")
        steps_visual.append(belief[0])
        steps_visual.append(belief[1] if len(belief) == 2 else belief[0])

        # ===== Kiểm tra goal =====
        if all(state in goal_beliefs for state in belief):
            for state in belief:
                if state == goal:
                    elapsed = (time.time() - start_time) * 1000
                    stats = {
                        "expanded": expanded,
                        "visited": visited,
                        "frontier": len(stack),
                        "time": elapsed
                    }
                    logs.append(f"Found GOAL state: {state}")
                    if return_steps:
                        if return_logs:
                            return state, steps_visual, logs

            elapsed = (time.time() - start_time) * 1000
            stats = {
                "expanded": expanded,
                "visited": visited,
                "frontier": len(stack),
                "time": elapsed
            }
            logs.append(f"Goal belief found (not exact match): {belief[0]}")
            if return_steps:
                if return_logs:
                    return belief[0], steps_visual, logs

        # sinh belief mới từ move và place
        move_belief = successors_visual(belief, n, action="move")
        if belief[0] != move_belief[0]:
            expanded += 1
        if belief[1] != move_belief[1]:
            expanded += 1
        place_belief = successors_visual(belief, n, action="place")
        if belief[0] != place_belief[0]:
            expanded += 1
        if belief[1] != place_belief[1]:
            expanded += 1

        if max_expansions is not None and expanded > max_expansions:
            elapsed = (time.time() - start_time) * 1000
            stats = {
                "expanded": expanded,
                "visited": visited,
                "frontier": len(stack),
                "time": elapsed
            }
            logs.append(f"Max expansion limit reached ({max_expansions}), stop.")
            if return_steps:
                if return_logs:
                    return None, steps_visual, logs
        
        stack.append(move_belief)
        stack.append(place_belief)
        logs.append(f"Push move_belief: {move_belief}")
        logs.append(f"Push place_belief: {place_belief}")

    # ===== Không tìm thấy goal =====
    elapsed = (time.time() - start_time) * 1000
    stats = {
        "expanded": expanded,
        "visited": visited,
        "frontier": len(stack),
        "time": elapsed
    }
    logs.append("No goal found after full search.")
    if return_steps:
        if return_logs:
            return None, steps_visual, logs

def partial_observable_target(ban_mau):
    """
    Wrapper function để tích hợp vào game
    Trả về path từ initial state đến goal
    Mô phỏng môi trường partial observable:
    - 6 quân đầu được quan sát đầy đủ
    - 2 quân cuối có uncertainty (belief state)
    """
    n = len(ban_mau)
    path = []
    
    # Bước 1: Bàn rỗng
    path.append([None] * n)
    
    # Bước 2-7: Thêm từng quân từ prefix (6 quân đầu được "quan sát")
    prefix_len = 6
    current_state = [None] * n
    for i in range(prefix_len):
        current_state[i] = ban_mau[i]
        path.append(current_state.copy())
    
    # Bước 8: Thêm quân thứ 7 - nhưng không chắc chắn (đặt sai)
    # Tìm cột khác với goal để đặt (mô phỏng uncertainty)
    wrong_col = None
    for col in range(n):
        if col not in current_state[:prefix_len] and col != ban_mau[6]:
            wrong_col = col
            break
    if wrong_col is not None:
        current_state[6] = wrong_col
        path.append(current_state.copy())
        
        # Bước 9: Phát hiện sai và sửa quân thứ 7
        current_state[6] = ban_mau[6]
        path.append(current_state.copy())
    else:
        # Nếu không có cột sai, đặt luôn đúng
        current_state[6] = ban_mau[6]
        path.append(current_state.copy())
    
    # Bước 10: Thêm quân thứ 8 - cũng không chắc chắn (đặt sai)
    wrong_col = None
    for col in range(n):
        if col not in current_state[:7] and col != ban_mau[7]:
            wrong_col = col
            break
    if wrong_col is not None:
        current_state[7] = wrong_col
        path.append(current_state.copy())
        
        # Bước 11: Sửa quân thứ 8 về đúng và hoàn thành
        current_state[7] = ban_mau[7]
        path.append(current_state.copy())
    else:
        # Nếu không có cột sai, đặt luôn đúng
        current_state[7] = ban_mau[7]
        path.append(current_state.copy())
    
    return path
