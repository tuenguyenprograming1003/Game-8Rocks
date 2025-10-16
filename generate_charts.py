"""
Script tạo biểu đồ so sánh hiệu suất các thuật toán
Bài toán 8 quân xe
"""

import matplotlib.pyplot as plt
import numpy as np

# Thiết lập font tiếng Việt (tùy chọn)
plt.rcParams['font.family'] = 'DejaVu Sans'

# Dữ liệu từ kết quả thực nghiệm
algorithms = ['Greedy', 'DFS', 'UCS', 'IDS-DFS', 'A*', 'DLS', 'BFS', 'IDS-DLS']
times = [1.08, 4.92, 12.6, 20.59, 23.4, 24.37, 30.82, 42.13]
states = [2016, 16100, 54954, 125692, 96794, 93529, 109600, 203121]

# Màu sắc: Vàng cho tốt nhất, xanh cho thuật toán có thông tin, đỏ cho không thông tin
colors_time = ['gold', 'lightcoral', 'lightcoral', 'lightcoral', 'skyblue', 'lightcoral', 'lightcoral', 'lightcoral']
colors_states = ['gold', 'lightcoral', 'lightcoral', 'lightcoral', 'skyblue', 'lightcoral', 'lightcoral', 'lightcoral']

# ===== Biểu đồ 1: Thời gian thực thi =====
fig1, ax1 = plt.subplots(figsize=(14, 7))
bars1 = ax1.bar(algorithms, times, color=colors_time, edgecolor='black', linewidth=1.5)

# Thêm giá trị trên mỗi cột
for i, (bar, time) in enumerate(zip(bars1, times)):
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height,
             f'{time}s',
             ha='center', va='bottom', fontsize=10, fontweight='bold')

ax1.set_xlabel('Thuật toán', fontsize=14, fontweight='bold')
ax1.set_ylabel('Thời gian (giây)', fontsize=14, fontweight='bold')
ax1.set_title('So sánh thời gian thực thi các thuật toán\nBài toán 8 quân xe', 
              fontsize=16, fontweight='bold', pad=20)
ax1.grid(axis='y', alpha=0.3, linestyle='--')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('assets/performance_chart.png', dpi=300, bbox_inches='tight', facecolor='white')
print("✅ Đã tạo: assets/performance_chart.png")
plt.close()

# ===== Biểu đồ 2: Số trạng thái sinh ra =====
fig2, ax2 = plt.subplots(figsize=(14, 7))
bars2 = ax2.bar(algorithms, states, color=colors_states, edgecolor='black', linewidth=1.5)

# Thêm giá trị trên mỗi cột
for i, (bar, state) in enumerate(zip(bars2, states)):
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height,
             f'{state:,}',
             ha='center', va='bottom', fontsize=9, fontweight='bold')

ax2.set_xlabel('Thuật toán', fontsize=14, fontweight='bold')
ax2.set_ylabel('Số trạng thái sinh ra', fontsize=14, fontweight='bold')
ax2.set_title('So sánh số trạng thái sinh ra của các thuật toán\nBài toán 8 quân xe', 
              fontsize=16, fontweight='bold', pad=20)
ax2.grid(axis='y', alpha=0.3, linestyle='--')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('assets/states_chart.png', dpi=300, bbox_inches='tight', facecolor='white')
print("✅ Đã tạo: assets/states_chart.png")
plt.close()

# ===== Biểu đồ 3: So sánh tổng hợp (Line chart) =====
fig3, (ax3, ax4) = plt.subplots(1, 2, figsize=(16, 6))

# Subplot 1: Thời gian
ax3.plot(algorithms, times, marker='o', linewidth=2, markersize=10, color='#2E86AB')
ax3.scatter(0, times[0], color='gold', s=200, zorder=5, edgecolors='black', linewidth=2)
ax3.set_xlabel('Thuật toán', fontsize=12, fontweight='bold')
ax3.set_ylabel('Thời gian (giây)', fontsize=12, fontweight='bold')
ax3.set_title('Thời gian thực thi', fontsize=14, fontweight='bold')
ax3.grid(True, alpha=0.3, linestyle='--')
ax3.tick_params(axis='x', rotation=45)

# Subplot 2: Số trạng thái
ax4.plot(algorithms, states, marker='s', linewidth=2, markersize=10, color='#E63946')
ax4.scatter(0, states[0], color='gold', s=200, zorder=5, edgecolors='black', linewidth=2)
ax4.set_xlabel('Thuật toán', fontsize=12, fontweight='bold')
ax4.set_ylabel('Số trạng thái', fontsize=12, fontweight='bold')
ax4.set_title('Số trạng thái sinh ra', fontsize=14, fontweight='bold')
ax4.grid(True, alpha=0.3, linestyle='--')
ax4.tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('assets/comparison_line_chart.png', dpi=300, bbox_inches='tight', facecolor='white')
print("✅ Đã tạo: assets/comparison_line_chart.png")
plt.close()

# ===== Biểu đồ 4: Scatter plot (Thời gian vs Số trạng thái) =====
fig4, ax5 = plt.subplots(figsize=(12, 8))

# Phân loại thuật toán
informed = [0, 4]  # Greedy, A*
uninformed = [1, 2, 3, 5, 6, 7]  # Các thuật toán còn lại

# Vẽ uninformed
for i in uninformed:
    ax5.scatter(states[i], times[i], s=300, alpha=0.6, 
                color='lightcoral', edgecolors='darkred', linewidth=2)
    ax5.annotate(algorithms[i], (states[i], times[i]), 
                 xytext=(10, 10), textcoords='offset points',
                 fontsize=10, fontweight='bold')

# Vẽ informed
for i in informed:
    color = 'gold' if i == 0 else 'skyblue'
    ax5.scatter(states[i], times[i], s=400, alpha=0.8, 
                color=color, edgecolors='black', linewidth=2, zorder=5)
    ax5.annotate(algorithms[i], (states[i], times[i]), 
                 xytext=(10, 10), textcoords='offset points',
                 fontsize=11, fontweight='bold')

ax5.set_xlabel('Số trạng thái sinh ra', fontsize=14, fontweight='bold')
ax5.set_ylabel('Thời gian (giây)', fontsize=14, fontweight='bold')
ax5.set_title('Mối quan hệ giữa Thời gian và Số trạng thái\n(Vàng: Tốt nhất, Xanh: Có thông tin, Đỏ: Không thông tin)', 
              fontsize=14, fontweight='bold', pad=20)
ax5.grid(True, alpha=0.3, linestyle='--')

# Đánh dấu vùng tối ưu
ax5.axhline(y=5, color='green', linestyle='--', alpha=0.3, label='Vùng tối ưu (< 5s)')
ax5.axvline(x=20000, color='green', linestyle='--', alpha=0.3, label='Vùng tối ưu (< 20k states)')
ax5.legend(fontsize=10)

plt.tight_layout()
plt.savefig('assets/scatter_chart.png', dpi=300, bbox_inches='tight', facecolor='white')
print("✅ Đã tạo: assets/scatter_chart.png")
plt.close()

print("\n🎉 Hoàn thành! Đã tạo tất cả các biểu đồ trong thư mục assets/")
print("\n📊 Danh sách file đã tạo:")
print("   1. performance_chart.png - Biểu đồ cột thời gian")
print("   2. states_chart.png - Biểu đồ cột số trạng thái")
print("   3. comparison_line_chart.png - Biểu đồ đường so sánh")
print("   4. scatter_chart.png - Biểu đồ phân tán")
