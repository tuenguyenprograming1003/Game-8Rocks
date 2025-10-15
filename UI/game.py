import pygame
import sys
import os
import time

# Thêm đường dẫn để import từ thư mục cha
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Alg.bfs import bfs_target
from Alg.dfs import dfs_target
from Alg.ucs import ucs_target
from Alg.dls import dls_target
from Alg.ids import ids_target
from Alg.greedy import greedy_target
from Alg.astar import astar_target
from Alg.hill_climbing import hill_climbing_target
from Alg.beam_search import beam_search_target
from Alg.simulated_annealing import simulated_annealing_target
from Alg.genetic import genetic_target
from Alg.and_or_search import and_or_search_target
from Alg.partial_observable import partial_observable_target
from Alg.backtracking import backtracking_target
from Alg.forward_tracking import forward_tracking_target
from Alg.observations import observations_target
from Alg.ac3 import ac3_target
from Alg.utils import tao_mau, n
from UI.render import *
from UI.render import rong, cao, sz, le, nen, den

def run_algorithm_with_tracking(algorithm_func, ban_mau, alg_name, history, current_board_hash, *args):
    """
    Chạy thuật toán và track thời gian, trạng thái
    Returns: (path, updated_history)
    """
    start_time = time.perf_counter()  # Độ chính xác cao hơn
    try:
        path = algorithm_func(ban_mau, *args)
        end_time = time.perf_counter()
        elapsed = end_time - start_time
        
        # Kiểm tra xem có tìm được solution không
        if path and len(path) > 0:
            # Kiểm tra state cuối có match target không
            final_state = path[-1] if isinstance(path[-1], list) else None
            if final_state == ban_mau:
                status = "Success"
            else:
                status = "Partial"  # Tìm được path nhưng chưa đến target
        else:
            status = "Failed"
        
        # Thêm vào history
        history.append({
            'algorithm': alg_name,
            'time': elapsed,
            'status': status,
            'board_hash': current_board_hash,
            'steps': len(path) if path else 0
        })
        
        return path, history
    except Exception as e:
        end_time = time.perf_counter()
        elapsed = end_time - start_time
        history.append({
            'algorithm': alg_name,
            'time': elapsed,
            'status': "Error",
            'board_hash': current_board_hash,
            'steps': 0
        })
        return [], history

def main():
    # Khởi tạo
    mh, dh, font, font_nho, font_lon, font_tieu_de = init_pygame()
    
    # Biến game
    ban_mau = tao_mau()
    ban_ai = [None]*n
    path = []
    step = 0
    anim = False
    mode = "Chưa chọn"
    history = []  # Lưu lịch sử chạy thuật toán: [{alg, time, status, board_hash}]
    current_board_hash = str(ban_mau)  # Để tracking bàn cờ hiện tại
    
    # Vị trí bàn cờ - căn chỉnh lại
    trai = (le, le+60)  # Bàn AI
    phai = (le+sz*n+kc, le+60)  # Bàn target
    
    chay = True
    while chay:
        for sk in pygame.event.get():
            if sk.type==pygame.QUIT:
                chay=False
            elif sk.type==pygame.KEYDOWN:
                if sk.key==pygame.K_ESCAPE:
                    chay=False
                elif sk.key==pygame.K_SPACE:
                    ban_mau = tao_mau()
                    path = []
                    step = 0
                    ban_ai = [None]*n
                    history = []  # Xóa history khi reset bàn cờ
                    current_board_hash = str(ban_mau)
                elif sk.key==pygame.K_c:
                    ban_ai = [None]*n
                    path = []
                    step = 0
                elif sk.key==pygame.K_b:
                    mode = "BFS"
                    path, history = run_algorithm_with_tracking(bfs_target, ban_mau, "BFS", history, current_board_hash)
                    step = 0
                    ban_ai = path[0].copy() if path else [None]*n
                elif sk.key==pygame.K_d:
                    mode = "DFS"
                    path, history = run_algorithm_with_tracking(dfs_target, ban_mau, "DFS", history, current_board_hash)
                    step = 0
                    ban_ai = path[0].copy() if path else [None]*n
                elif sk.key==pygame.K_u:
                    mode = "UCS"
                    path, history = run_algorithm_with_tracking(ucs_target, ban_mau, "UCS", history, current_board_hash)
                    step = 0
                    ban_ai = path[0].copy() if path else [None]*n
                elif sk.key==pygame.K_l:
                    mode = "DLS"
                    path, history = run_algorithm_with_tracking(dls_target, ban_mau, "DLS", history, current_board_hash, 8)
                    step = 0
                    ban_ai = path[0].copy() if path else [None]*n
                elif sk.key==pygame.K_s:
                    mode = "A*"
                    path, history = run_algorithm_with_tracking(astar_target, ban_mau, "A*", history, current_board_hash)
                    step = 0
                    ban_ai = path[0].copy() if path else [None]*n
                elif sk.key==pygame.K_i:
                    mode = "IDS"
                    path, history = run_algorithm_with_tracking(ids_target, ban_mau, "IDS", history, current_board_hash)
                    step = 0
                    ban_ai = path[0].copy() if path else [None]*n
                elif sk.key==pygame.K_g:
                    mode = "Greedy"
                    path, history = run_algorithm_with_tracking(greedy_target, ban_mau, "Greedy", history, current_board_hash)
                    step = 0
                    ban_ai = path[0].copy() if path else [None]*n
                elif sk.key==pygame.K_s:
                    mode = "A*"
                    path, history = run_algorithm_with_tracking(astar_target, ban_mau, "A*", history, current_board_hash)
                    step = 0
                    ban_ai = path[0].copy() if path else [None]*n
                elif sk.key==pygame.K_h:
                    mode = "Hill Climbing"
                    path, history = run_algorithm_with_tracking(hill_climbing_target, ban_mau, "Hill Climbing", history, current_board_hash)
                    step = 0
                    ban_ai = path[0].copy() if path else [None]*n
                elif sk.key==pygame.K_k:
                    mode = "K-Beam"
                    path, history = run_algorithm_with_tracking(beam_search_target, ban_mau, "K-Beam", history, current_board_hash, 3)
                    step = 0
                    ban_ai = path[0].copy() if path else [None]*n
                elif sk.key==pygame.K_m:
                    mode = "Simulated Annealing"
                    path, history = run_algorithm_with_tracking(simulated_annealing_target, ban_mau, "Simulated Annealing", history, current_board_hash)
                    step = 0
                    ban_ai = path[0].copy() if path else [None]*n
                elif sk.key==pygame.K_e:
                    mode = "Genetic"
                    path, history = run_algorithm_with_tracking(genetic_target, ban_mau, "Genetic", history, current_board_hash)
                    step = 0
                    ban_ai = path[0].copy() if path else [None]*n
                elif sk.key==pygame.K_o:
                    mode = "AND-OR"
                    path, history = run_algorithm_with_tracking(and_or_search_target, ban_mau, "AND-OR", history, current_board_hash)
                    step = 0
                    ban_ai = path[0].copy() if path else [None]*n
                elif sk.key==pygame.K_p:
                    mode = "Partial Observable"
                    path, history = run_algorithm_with_tracking(partial_observable_target, ban_mau, "Partial Observable", history, current_board_hash)
                    step = 0
                    ban_ai = path[0].copy() if path else [None]*n
                elif sk.key==pygame.K_p:
                    mode = "Partial Observable"
                    path, history = run_algorithm_with_tracking(partial_observable_target, ban_mau, "Partial Observable", history, current_board_hash)
                    step = 0
                    ban_ai = path[0].copy() if path else [None]*n
                elif sk.key==pygame.K_w:
                    mode = "Observations"
                    path, history = run_algorithm_with_tracking(observations_target, ban_mau, "Observations", history, current_board_hash)
                    step = 0
                    ban_ai = path[0].copy() if path else [None]*n
                elif sk.key==pygame.K_t:
                    mode = "Backtracking"
                    path, history = run_algorithm_with_tracking(backtracking_target, ban_mau, "Backtracking", history, current_board_hash)
                    step = 0
                    ban_ai = path[0].copy() if path else [None]*n
                elif sk.key==pygame.K_f:
                    mode = "Forward Checking"
                    path, history = run_algorithm_with_tracking(forward_tracking_target, ban_mau, "Forward Checking", history, current_board_hash)
                    step = 0
                    ban_ai = path[0].copy() if path else [None]*n
                elif sk.key==pygame.K_x:
                    mode = "AC-3"
                    path, history = run_algorithm_with_tracking(ac3_target, ban_mau, "AC-3", history, current_board_hash)
                    step = 0
                    ban_ai = path[0].copy() if path else [None]*n
                elif sk.key==pygame.K_f:
                    mode = "Forward Tracking"
                    path, history = run_algorithm_with_tracking(forward_tracking_target, ban_mau, "Forward Tracking", history, current_board_hash)
                    step = 0
                    ban_ai = path[0].copy() if path else [None]*n
                elif sk.key==pygame.K_w:
                    mode = "Observations"
                    path, history = run_algorithm_with_tracking(observations_target, ban_mau, "Observations", history, current_board_hash)
                    step = 0
                    ban_ai = path[0].copy() if path else [None]*n
                elif sk.key==pygame.K_n:
                    if path and step < len(path)-1:
                        step += 1
                        ban_ai = path[step].copy()
                elif sk.key==pygame.K_r:
                    if path:
                        step = 0
                        ban_ai = path[0].copy()
                elif sk.key==pygame.K_a:
                    anim = not anim
                    
        # Animation
        if anim and path and step < len(path)-1:
            step += 1
            ban_ai = path[step].copy()
            
        # Vẽ
        mh.fill(nen)
        
        # Tiêu đề chính
        title = font_tieu_de.render("GAME 8 QUÂN XE - THUẬT TOÁN TÌM KIẾM", True, den)
        title_rect = title.get_rect(center=(rong//2, 20))
        mh.blit(title, title_rect)
        
        # Vẽ các bàn cờ
        ve_ban(mh,trai,ban=ban_ai,tdg=f"BÀN AI ({mode})",kt=True)
        ve_ban(mh,phai,ban=ban_mau,tdg="BÀN MỤC TIÊU")
        
        # Thông tin dưới mỗi bàn
        render_board_info(mh, font_nho, trai[0], trai[1]+sz*n+10, ban_ai, f"Bước {step}/{len(path)-1 if path else 0}")
        render_board_info(mh, font_nho, phai[0], phai[1]+sz*n+10, ban_mau, "Target Pattern")
        
        # Panel điều khiển
        render_game_info(mh, font_nho, None, trai, phai, cao, le, ban_ai, path, mode, step, history)
        
        pygame.display.flip()
        dh.tick(fps)
        
    pygame.quit()
    sys.exit()

if __name__=='__main__':
    main()
