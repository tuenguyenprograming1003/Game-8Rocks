import pygame

n = 8
sz = 64
le = 20
kc = 80
fps = 30
rong = 1600  # Mở rộng hơn nữa
cao = 950    # Tăng chiều cao

# Màu sắc
trang = (250,250,250)
den = (20,20,20)
sang = (240,217,181)
toi = (181,136,99)
nen = (245,245,245)
xanh = (30,120,180)
do = (200,40,40)
xanh_nhat = (200,230,255)
xam = (128,128,128)
vang = (255,215,0)
tim = (128,0,128)
tím_nhat = (230,200,255)
xanh_la = (40,180,40)
vang_dam = (255,140,0)
cam = (255,140,0)
xanh_duong_nhat = (230,240,255)

# Khởi tạo Pygame (sẽ được gọi từ game.py)
def init_pygame():
    pygame.init()
    mh = pygame.display.set_mode((rong,cao))
    pygame.display.set_caption("Game 8 Quân Xe - AI Search Algorithms")
    dh = pygame.time.Clock()
    
    font = pygame.font.SysFont("Arial",24)
    font_nho = pygame.font.SysFont("Arial",16)
    font_lon = pygame.font.SysFont("Arial",36)
    font_tieu_de = pygame.font.SysFont("Arial", 28, bold=True)
    
    return mh, dh, font, font_nho, font_lon, font_tieu_de

def ve_ban(mh, td, ban=None, tdg=None, kt=False):
    x0,y0 = td
    font = pygame.font.SysFont("Arial",24)
    font_lon = pygame.font.SysFont("Arial",36)
    
    if tdg:
        text = font.render(tdg,True,den)
        mh.blit(text,(x0,y0-28))
    for r in range(n):
        for c in range(n):
            o = pygame.Rect(x0+c*sz,y0+r*sz,sz,sz)
            mau = toi if (r+c)%2 else sang
            pygame.draw.rect(mh,mau,o)
            pygame.draw.rect(mh,den,o,1)
            if ban is not None and ban[r] is not None and ban[r]==c:
                q = font_lon.render("X",True,xanh)
                q_rect = q.get_rect(center=o.center)
                mh.blit(q,q_rect)
    if kt and ban is not None:
        for r in range(n):
            if ban[r] is not None:
                for r2 in range(r+1,n):
                    if ban[r2] is not None and ban[r2]==ban[r]:
                        cx = x0+ban[r]*sz+sz//2
                        cy = y0+r*sz+sz//2
                        pygame.draw.circle(mh,do,(cx,cy),8)
                        cx2 = x0+ban[r2]*sz+sz//2
                        cy2 = y0+r2*sz+sz//2
                        pygame.draw.circle(mh,do,(cx2,cy2),8)

def hien_vt(ban):
    ds = []
    for r,c in enumerate(ban):
        if c is not None and c!=-1:
            ds.append(f"R{r+1}C{c+1}")  # Rút gọn format
    if not ds:
        return "Trống"
    return " | ".join(ds)  # Hiển thị ngang thay vì dọc

def render_board_info(mh, font_nho, x, y, ban, title):
    """Render thông tin bàn cờ dưới mỗi bàn"""
    # Background
    pygame.draw.rect(mh, trang, (x-5, y, sz*n+10, 60), border_radius=5)
    pygame.draw.rect(mh, xam, (x-5, y, sz*n+10, 60), 1, border_radius=5)
    
    # Tiêu đề
    font_bold = pygame.font.SysFont("Arial", 14, bold=True)
    text = font_bold.render(title, True, xanh)
    mh.blit(text, (x, y + 5))
    
    # Vị trí các quân
    vt = hien_vt(ban)
    if len(vt) > 50:  # Nếu quá dài, chia thành 2 dòng
        mid = len(vt) // 2
        space_pos = vt.find(" | ", mid)
        if space_pos != -1:
            line1 = vt[:space_pos]
            line2 = vt[space_pos+3:]
            text1 = font_nho.render(line1, True, den)
            text2 = font_nho.render(line2, True, den)
            mh.blit(text1, (x, y + 25))
            mh.blit(text2, (x, y + 40))
        else:
            text = font_nho.render(vt, True, den)
            mh.blit(text, (x, y + 25))
    else:
        text = font_nho.render(vt, True, den)
        mh.blit(text, (x, y + 25))

def render_algorithm_group(mh, font_nho, x, y, width, title, algorithms, color):
    """
    Hiển thị nhóm thuật toán với title và danh sách
    algorithms: list of tuples (key, name)
    """
    # Background cho nhóm
    height = 40 + len(algorithms) * 26
    pygame.draw.rect(mh, (255, 255, 255), (x, y, width, height), border_radius=10)
    pygame.draw.rect(mh, color, (x, y, width, height), 3, border_radius=10)
    
    # Tiêu đề nhóm với background
    title_rect = pygame.Rect(x + 4, y + 4, width - 8, 30)
    pygame.draw.rect(mh, color, title_rect, border_radius=6)
    font_bold = pygame.font.SysFont("Arial", 13, bold=True)
    text = font_bold.render(title, True, trang)
    text_rect = text.get_rect(center=(x + width//2, y + 18))
    mh.blit(text, text_rect)
    
    # Danh sách thuật toán
    font_item = pygame.font.SysFont("Arial", 11)
    for i, (key, name) in enumerate(algorithms):
        y_item = y + 38 + i*26
        
        # Key với background
        key_rect = pygame.Rect(x + 8, y_item, 24, 20)
        pygame.draw.rect(mh, color, key_rect, border_radius=5)
        key_font = pygame.font.SysFont("Arial", 12, bold=True)
        key_text = key_font.render(key, True, trang)
        key_text_rect = key_text.get_rect(center=(x + 20, y_item + 10))
        mh.blit(key_text, key_text_rect)
        
        # Tên thuật toán - không cắt text
        name_text = font_item.render(name, True, den)
        mh.blit(name_text, (x + 38, y_item + 5))

def render_game_info(mh, font_nho, tb, trai, phai, cao, le, ban_ai, path, mode, step, history=None):
    # Panel điều khiển bên phải - 2 cột
    panel_x = le + sz*n*2 + kc + 20
    panel_w = rong - panel_x - le  # Sử dụng toàn bộ không gian còn lại
    
    # Vẽ background cho panel
    pygame.draw.rect(mh, nen, (panel_x, le, panel_w, cao-le*2), border_radius=10)
    pygame.draw.rect(mh, xanh, (panel_x, le, panel_w, cao-le*2), 3, border_radius=10)
    
    # Tiêu đề panel
    font_tieu_de = pygame.font.SysFont("Arial", 24, bold=True)
    title = font_tieu_de.render("THUẬT TOÁN TÌM KIẾM AI", True, xanh)
    mh.blit(title, (panel_x + 20, le + 15))
    
    # Chia làm 2 cột
    col1_x = panel_x + 20
    col2_x = panel_x + panel_w // 2 + 15
    col_width = panel_w // 2 - 35
    
    y_pos = le + 60
    
    # Cột 1: Uninformed + Informed + Local Search
    render_algorithm_group(mh, font_nho, col1_x, y_pos, col_width, "I. UNINFORMED SEARCH", [
        ("B", "BFS - Breadth-First Search"),
        ("U", "UCS - Uniform-Cost Search"),
        ("L", "DLS - Depth-Limited Search"),
        ("D", "DFS - Depth-First Search"),
        ("I", "IDS - Iterative Deepening Search")
    ], xanh)
    
    y_pos += 180
    render_algorithm_group(mh, font_nho, col1_x, y_pos, col_width, "II. INFORMED SEARCH", [
        ("G", "Greedy Best-First Search"),
        ("S", "A* Search")
    ], do)
    
    y_pos += 100
    render_algorithm_group(mh, font_nho, col1_x, y_pos, col_width, "III. LOCAL SEARCH", [
        ("H", "Hill Climbing"),
        ("M", "Simulated Annealing"),
        ("K", "K-Beam Search"),
        ("E", "Genetic Algorithm")
    ], cam)
    
    # Cột 2: Complex Environment + CSP
    y_pos2 = le + 60
    render_algorithm_group(mh, font_nho, col2_x, y_pos2, col_width, "IV. COMPLEX ENVIRONMENT", [
        ("O", "AND-OR Search"),
        ("P", "Partial Observable Search"),
        ("W", "Observations Search")
    ], tim)
    
    y_pos2 += 135
    render_algorithm_group(mh, font_nho, col2_x, y_pos2, col_width, "V. CSP (Constraint Satisfaction)", [
        ("T", "Backtracking Search"),
        ("F", "Forward Checking"),
        ("X", "AC-3 (Arc Consistency)")
    ], xanh_la)
    
    y_pos2 += 130
    render_algorithm_group(mh, font_nho, col2_x, y_pos2, col_width, "VI. ADVERSARIAL SEARCH", [
        ("V", "Minimax Decision"),
        ("Z", "Alpha-Beta Pruning")
    ], do)
    
    # Điều khiển game
    y_pos2 += 85
    render_control_section(mh, font_nho, col2_x, y_pos2, "ĐIỀU KHIỂN GAME:", [
        "N - Bước tiếp theo",
        "R - Về bước đầu", 
        "A - Chế độ tự động",
        "SPACE - Tạo bàn mới",
        "C - Xóa bàn AI",
        "ESC - Thoát"
    ], col_width)
    
    # Thông tin trạng thái - full width ở dưới cùng (di chuyển lên trên)
    status_y = cao - 380  # Tăng từ 280 lên 340 để di chuyển lên trên
    render_status_info(mh, font_nho, panel_x + 20, status_y, mode, step, path, ban_ai, panel_w - 40)
    
    # History section - ngay dưới status
    if history:
        history_y = status_y + 105
        render_history_section(mh, font_nho, panel_x + 20, history_y, history, panel_w - 40)
        
        # Nút xem đồ thị - dưới history
        chart_button_y = history_y + min(len(history) * 26 + 42, 160) + 10
        chart_button_rect = render_chart_button(mh, font_nho, panel_x + 20, chart_button_y, panel_w - 40)
        return chart_button_rect
    
    return None

def render_algorithm_section(mh, font_nho, x, y, title, items):
    # Tiêu đề section
    font_bold = pygame.font.SysFont("Arial", 16, bold=True)
    text = font_bold.render(title, True, xanh)
    mh.blit(text, (x + 10, y))
    
    # Các item
    for i, item in enumerate(items):
        text = font_nho.render(item, True, den)
        mh.blit(text, (x + 15, y + 25 + i*18))

def render_control_section(mh, font_nho, x, y, title, items, width=320):
    # Background
    height = 42 + len(items) * 24
    pygame.draw.rect(mh, (255, 255, 255), (x, y, width, height), border_radius=10)
    pygame.draw.rect(mh, do, (x, y, width, height), 3, border_radius=10)
    
    # Tiêu đề với background
    title_rect = pygame.Rect(x + 4, y + 4, width - 8, 30)
    pygame.draw.rect(mh, do, title_rect, border_radius=6)
    font_bold = pygame.font.SysFont("Arial", 13, bold=True)
    text = font_bold.render(title, True, trang)
    text_rect = text.get_rect(center=(x + width//2, y + 18))
    mh.blit(text, text_rect)
    
    # Các item
    font_item = pygame.font.SysFont("Arial", 11)
    for i, item in enumerate(items):
        text = font_item.render(item, True, den)
        mh.blit(text, (x + 12, y + 40 + i*24))

def render_status_info(mh, font_nho, x, y, mode, step, path, ban_ai, width=270):
    # Background cho status
    pygame.draw.rect(mh, (255, 255, 255), (x, y, width, 95), border_radius=10)
    pygame.draw.rect(mh, vang_dam, (x, y, width, 95), 3, border_radius=10)
    
    # Header
    header_rect = pygame.Rect(x + 4, y + 4, width - 8, 30)
    pygame.draw.rect(mh, vang_dam, header_rect, border_radius=6)
    font_bold = pygame.font.SysFont("Arial", 14, bold=True)
    text = font_bold.render("TRẠNG THÁI", True, trang)
    text_rect = text.get_rect(center=(x + width//2, y + 18))
    mh.blit(text, text_rect)
    
    # Thuật toán hiện tại
    font_info = pygame.font.SysFont("Arial", 12, bold=True)
    text = font_info.render(f"Thuật toán: {mode}", True, den)
    mh.blit(text, (x + 12, y + 42))
    
    # Số bước
    font_detail = pygame.font.SysFont("Arial", 11)
    if path:
        text = font_detail.render(f"Tổng bước: {len(path)} | Hiện tại: {step}", True, den)
        mh.blit(text, (x + 12, y + 62))
        text = font_detail.render("Nhấn N để bước tiếp", True, xanh)
        mh.blit(text, (x + 12, y + 78))
    else:
        text = font_detail.render("Chưa chạy thuật toán", True, xam)
        mh.blit(text, (x + 12, y + 62))
        text = font_detail.render("Chọn thuật toán để bắt đầu", True, xam)
        mh.blit(text, (x + 12, y + 78))

def render_history_section(mh, font_nho, x, y, history, width=270):
    """Hiển thị lịch sử các thuật toán đã chạy"""
    # Background
    history_height = min(len(history) * 26 + 42, 160)
    pygame.draw.rect(mh, (255, 255, 255), (x, y, width, history_height), border_radius=10)
    pygame.draw.rect(mh, tim, (x, y, width, history_height), 3, border_radius=10)
    
    # Header
    header_rect = pygame.Rect(x + 4, y + 4, width - 8, 30)
    pygame.draw.rect(mh, tim, header_rect, border_radius=6)
    font_bold = pygame.font.SysFont("Arial", 13, bold=True)
    text = font_bold.render("LỊCH SỬ THUẬT TOÁN", True, trang)
    text_rect = text.get_rect(center=(x + width//2, y + 18))
    mh.blit(text, text_rect)
    
    # Hiển thị tối đa 5 entries gần nhất
    visible_history = history[-5:] if len(history) > 5 else history
    
    font_mini = pygame.font.SysFont("Arial", 11)
    for i, entry in enumerate(visible_history):
        y_offset = y + 40 + i * 26
        
        # Màu theo trạng thái
        if entry['status'] == 'Success':
            status_color = xanh_la
        elif entry['status'] == 'Partial':
            status_color = vang_dam
        elif entry['status'] == 'Failed':
            status_color = do
        else:  # Error
            status_color = tim
        
        # Tên thuật toán (rút gọn nếu quá dài)
        alg_name = entry['algorithm'][:12]
        
        # Thời gian - hiển thị ms nếu < 1s, ngược lại hiển thị giây
        time_val = entry['time']
        if time_val < 1.0:
            time_str = f"{time_val*1000:.1f}ms"
        else:
            time_str = f"{time_val:.2f}s"
        
        # Hiển thị: Tên | Thời gian | Trạng thái
        text_line = f"{alg_name:<12} {time_str:>8} {entry['status']}"
        text = font_mini.render(text_line, True, den)
        mh.blit(text, (x + 10, y_offset))
        
        # Indicator màu cho status
        pygame.draw.circle(mh, status_color, (x + width - 15, y_offset + 6), 4)

def render_chart_button(mh, font_nho, x, y, width):
    """Vẽ nút xem đồ thị và return rect để detect click"""
    button_height = 50
    button_rect = pygame.Rect(x, y, width, button_height)
    
    # Background với gradient effect (đơn giản hóa)
    pygame.draw.rect(mh, (70, 150, 220), button_rect, border_radius=10)
    pygame.draw.rect(mh, (40, 120, 200), button_rect, 3, border_radius=10)
    
    # Icon (đồ thị đơn giản)
    icon_x = x + 15
    icon_y = y + button_height // 2
    # Vẽ 3 cột nhỏ
    for i in range(3):
        col_height = 15 + i * 5
        col_rect = pygame.Rect(icon_x + i * 12, icon_y + 10 - col_height, 8, col_height)
        pygame.draw.rect(mh, trang, col_rect, border_radius=2)
    
    # Text
    font_button = pygame.font.SysFont("Arial", 14, bold=True)
    text = font_button.render("XEM ĐỒ THỊ THỐNG KÊ", True, trang)
    text_rect = text.get_rect(center=(x + width//2 + 15, y + button_height//2))
    mh.blit(text, text_rect)
    
    # Hint text
    font_hint = pygame.font.SysFont("Arial", 9)
    hint = font_hint.render("Click để xem biểu đồ so sánh", True, (230, 240, 255))
    hint_rect = hint.get_rect(center=(x + width//2 + 15, y + button_height//2 + 13))
    mh.blit(hint, hint_rect)
    
    return button_rect
