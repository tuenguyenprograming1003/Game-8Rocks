# 📁 Thư mục Assets - Hướng dẫn thêm GIF

Thư mục này chứa các file media (GIF, hình ảnh, biểu đồ) cho báo cáo.

## 📋 Danh sách file cần thêm

### 🎬 GIF minh họa thuật toán (Algorithm Demos)

Thêm các file GIF sau vào thư mục này:

1. **bfs_demo.gif** - Minh họa thuật toán BFS
2. **dfs_demo.gif** - Minh họa thuật toán DFS  
3. **ucs_demo.gif** - Minh họa thuật toán UCS
4. **dls_demo.gif** - Minh họa thuật toán DLS
5. **ids_dls_demo.gif** - Minh họa thuật toán IDS-DLS
6. **ids_dfs_demo.gif** - Minh họa thuật toán IDS-DFS
7. **greedy_demo.gif** - Minh họa thuật toán Greedy
8. **astar_demo.gif** - Minh họa thuật toán A*

### 📊 Biểu đồ so sánh (Comparison Charts)

9. **performance_chart.png** - Biểu đồ so sánh thời gian thực thi
10. **states_chart.png** - Biểu đồ so sánh số trạng thái sinh ra

---

## ✅ Checklist

- [ ] bfs_demo.gif
- [ ] dfs_demo.gif
- [ ] ucs_demo.gif
- [ ] dls_demo.gif
- [ ] ids_dls_demo.gif
- [ ] ids_dfs_demo.gif
- [ ] greedy_demo.gif
- [ ] astar_demo.gif
- [ ] performance_chart.png
- [ ] states_chart.png

---

## 💡 Gợi ý tạo GIF

### Cách 1: Screen Recording
1. Chạy ứng dụng và ghi lại màn hình
2. Sử dụng tool như **LICEcap**, **ScreenToGif**, hoặc **Gifox**
3. Crop và optimize GIF về kích thước phù hợp (< 5MB)

### Cách 2: Từ Code
1. Sử dụng matplotlib animation
2. Save animation thành GIF
3. Hoặc dùng thư viện `imageio`, `PIL`

### Cách 3: Online Tools
- [Ezgif](https://ezgif.com/) - Edit và optimize GIF
- [Canva](https://canva.com/) - Tạo animation đơn giản
- [Gifmaker](https://gifmaker.me/) - Tạo GIF từ ảnh

---

## 📊 Gợi ý tạo biểu đồ

### Sử dụng Python (Matplotlib/Seaborn):

```python
import matplotlib.pyplot as plt
import numpy as np

# Dữ liệu
algorithms = ['Greedy', 'DFS', 'UCS', 'IDS-DFS', 'A*', 'DLS', 'BFS', 'IDS-DLS']
times = [1.08, 4.92, 12.6, 20.59, 23.4, 24.37, 30.82, 42.13]
states = [2016, 16100, 54954, 125692, 96794, 93529, 109600, 203121]

# Biểu đồ thời gian
fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.bar(algorithms, times, color='skyblue', edgecolor='navy')
bars[0].set_color('gold')  # Highlight best
ax.set_xlabel('Thuật toán', fontsize=12)
ax.set_ylabel('Thời gian (giây)', fontsize=12)
ax.set_title('So sánh thời gian thực thi các thuật toán', fontsize=14, fontweight='bold')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('assets/performance_chart.png', dpi=300, bbox_inches='tight')
plt.show()

# Biểu đồ số trạng thái
fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.bar(algorithms, states, color='lightcoral', edgecolor='darkred')
bars[0].set_color('gold')  # Highlight best
ax.set_xlabel('Thuật toán', fontsize=12)
ax.set_ylabel('Số trạng thái', fontsize=12)
ax.set_title('So sánh số trạng thái sinh ra', fontsize=14, fontweight='bold')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('assets/states_chart.png', dpi=300, bbox_inches='tight')
plt.show()
```

---

## 📏 Khuyến nghị về kích thước

- **GIF:** 600-800px chiều rộng, < 5MB
- **PNG:** 1200-1600px chiều rộng, 300 DPI
- **Chất lượng:** Rõ nét, dễ nhìn, không bị vỡ

---

## 🔗 Liên kết trong README

Các file đã được liên kết sẵn trong `README.md` chính với cú pháp:

```markdown
![Description](./assets/filename.gif)
```

Chỉ cần thêm file vào thư mục này là sẽ tự động hiển thị!

---

**📝 Lưu ý:** Đảm bảo tên file khớp chính xác với tên trong README.md
