# Game 8 Quân Xe - AI Search Algorithms Visualization

**Một ứng dụng trực quan hóa 17 thuật toán AI tìm kiếm cho bài toán 8 quân xe**

---

## Mục lục

- [Giới thiệu](#giới-thiệu)
- [Tính năng](#tính-năng)
- [Cài đặt](#cài-đặt)
- [Sử dụng](#sử-dụng)
- [Thuật toán](#thuật-toán)
- [Cấu trúc dự án](#cấu-trúc-dự-án)
- [Yêu cầu hệ thống](#yêu-cầu-hệ-thống)

---

## Giới thiệu

**Game 8 Quân Xe** là một ứng dụng giáo dục được phát triển bằng Python và Pygame, giúp trực quan hóa và so sánh **17 thuật toán AI** khác nhau trong việc giải quyết bài toán 8 quân xe (8-Rooks problem).

### Bài toán 8 Quân Xe

Đặt 8 quân xe trên bàn cờ 8x8 sao cho không có 2 quân xe nào cùng hàng hoặc cùng cột. Khác với bài toán 8 quân hậu, quân xe **không kiểm tra đường chéo**.

### Mục đích

- Học tập: Hiểu rõ cách hoạt động của các thuật toán AI
- So sánh: Đánh giá hiệu suất giữa các thuật toán
- Trực quan hóa: Xem từng bước thực thi của thuật toán
- Thực hành: Áp dụng lý thuyết vào thực tế

---

## Tính năng

### Giao diện

- Giao diện đồ họa Pygame mượt mà, hiện đại
- Hiển thị 2 bàn cờ: Bàn AI và Bàn Target
- 17 thuật toán được phân nhóm theo loại
- Màu sắc phân biệt rõ ràng cho từng nhóm
- Panel điều khiển 2 cột rộng rãi

### Visualization

- Xem từng bước thực thi thuật toán
- History tracking: Lịch sử các lần chạy
- Hiển thị thời gian chạy (ms/s)
- Trạng thái: Success/Partial/Failed/Error
- Indicator màu cho mỗi trạng thái

### Điều khiển

- Step-by-step: Xem từng bước (phím N)
- Auto-run: Chạy tự động (phím A)
- Reset: Tạo bàn cờ mới (SPACE)
- Speed control: Điều chỉnh tốc độ (1-9, 0)
- Clear: Xóa bàn AI (phím C)

### Performance Tracking

- Thời gian chạy chính xác (perf_counter)
- Số bước thực thi
- Kết quả chi tiết
- Lịch sử 5-6 lần chạy gần nhất

---

## Cài đặt

### Yêu cầu

- Python 3.13+
- Pygame 2.6.1+

### Các bước cài đặt

1. **Clone repository**

```bash
git clone https://github.com/yourusername/Game-8Rocks.git
cd Game-8Rocks
```

2. **Cài đặt dependencies**

```bash
pip install pygame
```

3. **Chạy game**

```bash
python UI/game.py
```

hoặc với Python 3.13:

```bash
python3.13 UI/game.py
```

---

## Sử dụng

### Keyboard Controls

#### Chọn thuật toán

| Key | Thuật toán | Nhóm |
|-----|-----------|------|
| **B** | BFS (Breadth-First Search) | Uninformed |
| **D** | DFS (Depth-First Search) | Uninformed |
| **U** | UCS (Uniform-Cost Search) | Uninformed |
| **L** | DLS (Depth-Limited Search) | Uninformed |
| **I** | IDS (Iterative Deepening Search) | Uninformed |
| **G** | Greedy Best-First Search | Informed |
| **S** | A* Search | Informed |
| **H** | Hill Climbing | Local Search |
| **M** | Simulated Annealing | Local Search |
| **K** | K-Beam Search | Local Search |
| **E** | Genetic Algorithm | Local Search |
| **O** | AND-OR Search | Complex Environment |
| **P** | Partial Observable Search | Complex Environment |
| **W** | Observations Search | Complex Environment |
| **T** | Backtracking Search | CSP |
| **F** | Forward Checking | CSP |
| **X** | AC-3 (Arc Consistency) | CSP |

#### Điều khiển game

| Key | Chức năng |
|-----|-----------|
| **N** | Bước tiếp theo (Next) |
| **R** | Về bước đầu (Reset step) |
| **A** | Chế độ tự động (Auto-run) |
| **SPACE** | Tạo bàn cờ mới |
| **C** | Xóa bàn AI |
| **1-9** | Điều chỉnh tốc độ (1=chậm, 9=nhanh) |
| **0** | Tốc độ cực nhanh |
| **ESC** | Thoát game |

### Workflow

1. **Khởi động game** → Bàn target được tạo ngẫu nhiên
2. **Chọn thuật toán** → Nhấn phím tương ứng (B, D, U, ...)
3. **Xem kết quả** → Thuật toán chạy và hiển thị path
4. **Step through** → Nhấn N để xem từng bước
5. **So sánh** → Chạy nhiều thuật toán và xem history
6. **Reset** → Nhấn SPACE để tạo bàn mới

---

## Thuật toán

### I. Uninformed Search (Tìm kiếm không thông tin)

#### 1. BFS - Breadth-First Search
- Đặc điểm: Duyệt theo tầng, sử dụng Queue
- Độ phức tạp: O(b^d)
- Tối ưu: Có (với cost đều)
- Đầy đủ: Có

#### 2. DFS - Depth-First Search
- Đặc điểm: Duyệt theo chiều sâu, sử dụng Stack
- Độ phức tạp: O(b^m)
- Tối ưu: Không
- Bộ nhớ: Ít hơn BFS

#### 3. UCS - Uniform-Cost Search
- Đặc điểm: Mở rộng theo chi phí nhỏ nhất
- Cấu trúc: Priority Queue
- Tối ưu: Có (với cost dương)
- Đầy đủ: Có

#### 4. DLS - Depth-Limited Search
- Đặc điểm: DFS với giới hạn độ sâu
- Tránh: Lặp vô hạn
- Tối ưu: Không

#### 5. IDS - Iterative Deepening Search
- Đặc điểm: Kết hợp ưu điểm BFS và DFS
- Độ phức tạp: O(b^d)
- Tối ưu: Có
- Bộ nhớ: O(bd)

### II. Informed Search (Tìm kiếm có thông tin)

#### 6. Greedy Best-First Search
- Hàm đánh giá: f(n) = h(n)
- Đặc điểm: Mở rộng nút gần đích nhất
- Tối ưu: Không
- Tốc độ: Nhanh

#### 7. A* Search
- Hàm đánh giá: f(n) = g(n) + h(n)
- Đặc điểm: Kết hợp chi phí thực tế và ước lượng
- Tối ưu: Có (nếu h(n) admissible)
- Đầy đủ: Có

### III. Local Search (Tìm kiếm cục bộ)

#### 8. Hill Climbing
- Đặc điểm: Chọn trạng thái láng giềng tốt nhất
- Vấn đề: Dễ kẹt cực trị cục bộ
- Bộ nhớ: Rất ít (O(1))

#### 9. Simulated Annealing
- Đặc điểm: Cho phép move tệ với xác suất giảm dần
- Tránh: Local minima
- Temperature: Giảm theo thời gian

#### 10. K-Beam Search
- Đặc điểm: Giữ lại K nút tốt nhất
- Tốc độ: Nhanh
- Tối ưu: Không

#### 11. Genetic Algorithm
- Đặc điểm: Mô phỏng tiến hóa tự nhiên
- Operators: Selection, Crossover, Mutation
- Population: Nhiều thế hệ

### 3. Complex Environment
Môi trường phức tạp với trạng thái không hoàn toàn quan sát được

#### 12. And-Or Tree Search
- Môi trường: Không xác định
- Kế hoạch: Contingency plans
- Cấu trúc: Cây And/Or

#### 13. Online DFS Agent
- Đặc điểm: Học trong quá trình explore
- State: Không biết trước hoàn toàn
- Real-time: Quyết định tức thời

#### 14. LRTA* (Learning Real-Time A*)
- Đặc điểm: Cập nhật heuristic khi di chuyển
- Học: Từ kinh nghiệm
- Real-time: Hành động nhanh

#### 15. Partial Observable Search
- Đặc điểm: Quan sát một phần trạng thái
- Belief States: Tập trạng thái có thể
- Uncertainty: Xử lý không chắc chắn

#### 14. Observations Search
- Đặc điểm: Full observations (vs Partial)
- State: Quan sát đầy đủ
- BFS/DFS: Trên observation graph

### 4. CSP (Constraint Satisfaction Problem)
Giải quyết bài toán thỏa mãn ràng buộc

#### 16. Backtracking Search
- Đặc điểm: Quay lui khi vi phạm ràng buộc
- Pruning: Cắt nhánh sớm
- Tối ưu: Có với bài toán CSP

#### 17. AC-3 (Arc Consistency)
- Đặc điểm: Loại bỏ giá trị không nhất quán
- Domain Reduction: Thu hẹp miền giá trị
- Preprocessing: Trước khi backtracking

---

## Cấu trúc dự án

```
Game-8Rocks/
├── Alg/                          # Thư mục thuật toán
│   ├── __init__.py
│   ├── utils.py                  # Utilities (tạo mẫu, kiểm tra)
│   ├── bfs.py                    # Breadth-First Search
│   ├── dfs.py                    # Depth-First Search
│   ├── ucs.py                    # Uniform-Cost Search
│   ├── dls.py                    # Depth-Limited Search
│   ├── ids.py                    # Iterative Deepening Search
│   ├── greedy.py                 # Greedy Best-First Search
│   ├── astar.py                  # A* Search
│   ├── hill_climbing.py          # Hill Climbing
│   ├── simulated_annealing.py    # Simulated Annealing
│   ├── beam_search.py            # K-Beam Search
│   ├── genetic.py                # Genetic Algorithm
│   ├── and_or_search.py          # AND-OR Search
│   ├── partial_observable.py     # Partial Observable Search
│   ├── observations.py           # Observations Search
│   ├── backtracking.py           # Backtracking (Stack-based)
│   ├── forward_tracking.py       # Forward Checking
│   └── ac3.py                    # AC-3 Algorithm
│
├── UI/                           # Thư mục giao diện
│   ├── __init__.py
│   ├── render.py                 # Rendering functions
│   └── game.py                   # Main game loop
│
├── README.md                     # Documentation
└── requirements.txt              # Dependencies

```

---

## Yêu cầu hệ thống

### Tối thiểu
- OS: Windows 10, macOS 10.14+, Linux
- Python: 3.10+
- RAM: 4GB
- Display: 1600x950+

### Khuyến nghị
- Python: 3.13+
- RAM: 8GB+
- Display: 1920x1080+

