import matplotlib.pyplot as plt
import matplotlib
from collections import defaultdict
import numpy as np

# Sử dụng backend MacOSX cho macOS hoặc Agg nếu không có display
try:
    import platform
    if platform.system() == 'Darwin':  # macOS
        matplotlib.use('MacOSX')
    else:
        matplotlib.use('Agg')
except:
    matplotlib.use('Agg')

def show_algorithm_chart(history):
    """
    Hiển thị đồ thị thống kê các thuật toán đã chạy
    history: list of dict với keys: algorithm, time, status, board_hash, steps
    """
    if not history:
        print("Chưa có dữ liệu để hiển thị đồ thị!")
        return
    
    # Tạo figure với nhiều subplot
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Biểu đồ đánh giá thuật toán', fontsize=16, fontweight='bold')
    
    # 1. Biểu đồ thời gian chạy (giống hình mẫu)
    plot_time_comparison(axes[0, 0], history)
    
    # 2. Biểu đồ số bước thực hiện
    plot_steps_comparison(axes[0, 1], history)
    
    # 3. Biểu đồ tỷ lệ thành công
    plot_success_rate(axes[1, 0], history)
    
    # 4. Bảng thống kê chi tiết
    plot_statistics_table(axes[1, 1], history)
    
    plt.tight_layout()
    plt.show()

def plot_time_comparison(ax, history):
    """Biểu đồ cột so sánh thời gian chạy (giống hình mẫu)"""
    # Nhóm theo thuật toán và lấy thời gian trung bình
    alg_times = defaultdict(list)
    alg_success = defaultdict(list)
    
    for entry in history:
        alg = entry['algorithm']
        time_val = entry['time'] * 1000  # Convert to ms
        status = entry['status']
        
        alg_times[alg].append(time_val)
        alg_success[alg].append(status == 'Success')
    
    # Tính trung bình
    algorithms = []
    avg_times = []
    can_find = []
    cannot_find = []
    partial = []
    
    for alg in sorted(alg_times.keys()):
        algorithms.append(alg)
        avg_time = np.mean(alg_times[alg])
        avg_times.append(avg_time)
        
        # Phân loại
        success_rate = np.mean(alg_success[alg])
        if success_rate >= 0.8:
            can_find.append(avg_time)
            cannot_find.append(0)
            partial.append(0)
        elif success_rate >= 0.3:
            can_find.append(0)
            cannot_find.append(0)
            partial.append(avg_time)
        else:
            can_find.append(0)
            cannot_find.append(avg_time)
            partial.append(0)
    
    # Vẽ biểu đồ cột xếp chồng
    x = np.arange(len(algorithms))
    width = 0.6
    
    ax.bar(x, can_find, width, label='Tìm thấy mục tiêu', color='#3366CC')
    ax.bar(x, cannot_find, width, bottom=can_find, label='Không tìm thấy mục tiêu', color='#DC3912')
    ax.bar(x, partial, width, bottom=np.array(can_find) + np.array(cannot_find), 
           label='Tìm một tập hoặc một trạng thái gần đích', color='#FF9900')
    
    ax.set_ylabel('Thời gian (ms)', fontsize=10)
    ax.set_xlabel('Thuật toán (theo giai đoạn)', fontsize=10)
    ax.set_title('Biểu đồ đánh giá thuật toán', fontsize=12, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(algorithms, rotation=45, ha='right', fontsize=8)
    ax.legend(fontsize=8, loc='upper left')
    ax.grid(axis='y', alpha=0.3)

def plot_steps_comparison(ax, history):
    """Biểu đồ so sánh số bước"""
    # Nhóm theo thuật toán
    alg_steps = defaultdict(list)
    
    for entry in history:
        alg = entry['algorithm']
        steps = entry['steps']
        if steps > 0:  # Chỉ tính các kết quả có bước
            alg_steps[alg].append(steps)
    
    algorithms = []
    avg_steps = []
    min_steps = []
    max_steps = []
    
    for alg in sorted(alg_steps.keys()):
        if alg_steps[alg]:  # Có dữ liệu
            algorithms.append(alg)
            avg_steps.append(np.mean(alg_steps[alg]))
            min_steps.append(np.min(alg_steps[alg]))
            max_steps.append(np.max(alg_steps[alg]))
    
    if algorithms:
        x = np.arange(len(algorithms))
        width = 0.35
        
        ax.bar(x - width/2, min_steps, width, label='Min steps', color='#90EE90', alpha=0.7)
        ax.bar(x + width/2, max_steps, width, label='Max steps', color='#FFB6C1', alpha=0.7)
        ax.plot(x, avg_steps, 'ro-', label='Avg steps', linewidth=2, markersize=6)
        
        ax.set_ylabel('Số bước', fontsize=10)
        ax.set_xlabel('Thuật toán', fontsize=10)
        ax.set_title('So sánh số bước thực hiện', fontsize=12, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(algorithms, rotation=45, ha='right', fontsize=8)
        ax.legend(fontsize=8)
        ax.grid(axis='y', alpha=0.3)
    else:
        ax.text(0.5, 0.5, 'Chưa có dữ liệu\nsố bước', 
                ha='center', va='center', fontsize=12)

def plot_success_rate(ax, history):
    """Biểu đồ tròn tỷ lệ thành công"""
    # Đếm trạng thái
    status_count = defaultdict(int)
    for entry in history:
        status_count[entry['status']] += 1
    
    if status_count:
        labels = []
        sizes = []
        colors = []
        
        status_colors = {
            'Success': '#4CAF50',
            'Partial': '#FFC107',
            'Failed': '#F44336',
            'Error': '#9E9E9E'
        }
        
        status_labels = {
            'Success': 'Thành công',
            'Partial': 'Một phần',
            'Failed': 'Thất bại',
            'Error': 'Lỗi'
        }
        
        for status, count in status_count.items():
            labels.append(f"{status_labels.get(status, status)}\n({count} lần)")
            sizes.append(count)
            colors.append(status_colors.get(status, '#9E9E9E'))
        
        ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
               startangle=90, textprops={'fontsize': 9})
        ax.set_title('Tỷ lệ kết quả', fontsize=12, fontweight='bold')
    else:
        ax.text(0.5, 0.5, 'Chưa có dữ liệu', ha='center', va='center', fontsize=12)

def plot_statistics_table(ax, history):
    """Bảng thống kê chi tiết"""
    ax.axis('off')
    
    # Nhóm dữ liệu và lưu thứ tự xuất hiện đầu tiên
    alg_data = defaultdict(lambda: {'count': 0, 'success': 0, 'total_time': 0, 'total_steps': 0, 'first_index': -1})
    
    for idx, entry in enumerate(history):
        alg = entry['algorithm']
        # Lưu index lần xuất hiện đầu tiên
        if alg_data[alg]['first_index'] == -1:
            alg_data[alg]['first_index'] = idx
        
        alg_data[alg]['count'] += 1
        if entry['status'] == 'Success':
            alg_data[alg]['success'] += 1
        alg_data[alg]['total_time'] += entry['time']
        alg_data[alg]['total_steps'] += entry['steps']
    
    # Tạo bảng
    table_data = []
    headers = ['STT', 'Thuật toán', 'Lần chạy', 'Tỷ lệ\nthành công', 'Thời gian TB\n(ms)', 'Bước TB']
    
    # Sắp xếp theo thứ tự xuất hiện đầu tiên (first_index)
    sorted_algs = sorted(alg_data.keys(), key=lambda alg: alg_data[alg]['first_index'])
    
    # Thêm STT khi tạo dữ liệu
    for idx, alg in enumerate(sorted_algs, start=1):
        data = alg_data[alg]
        count = data['count']
        success_rate = f"{data['success']/count*100:.0f}%"
        avg_time = f"{data['total_time']/count*1000:.2f}"
        avg_steps = f"{data['total_steps']/count:.1f}" if data['total_steps'] > 0 else "0"
        
        table_data.append([str(idx), alg, str(count), success_rate, avg_time, avg_steps])
    
    if table_data:
        table = ax.table(cellText=table_data, colLabels=headers,
                        cellLoc='center', loc='center',
                        colWidths=[0.08, 0.22, 0.13, 0.17, 0.18, 0.15])
        
        table.auto_set_font_size(False)
        table.set_fontsize(8)
        table.scale(1, 2)
        
        # Style cho header
        for i in range(len(headers)):
            table[(0, i)].set_facecolor('#4CAF50')
            table[(0, i)].set_text_props(weight='bold', color='white')
        
        # Style cho các dòng
        for i in range(1, len(table_data) + 1):
            for j in range(len(headers)):
                if i % 2 == 0:
                    table[(i, j)].set_facecolor('#f0f0f0')
                else:
                    table[(i, j)].set_facecolor('#ffffff')
        
        ax.set_title('Bảng thống kê chi tiết', fontsize=12, fontweight='bold', pad=20)
    else:
        ax.text(0.5, 0.5, 'Chưa có dữ liệu', ha='center', va='center', fontsize=12)

def show_algorithm_comparison_simple(history):
    """Biểu đồ đơn giản hơn - chỉ so sánh thời gian"""
    if not history:
        print("Chưa có dữ liệu để hiển thị!")
        return
    
    # Nhóm theo thuật toán
    alg_times = defaultdict(list)
    alg_success = defaultdict(list)
    
    for entry in history:
        alg = entry['algorithm']
        time_val = entry['time'] * 1000  # ms
        alg_times[alg].append(time_val)
        alg_success[alg].append(entry['status'] == 'Success')
    
    # Vẽ
    fig, ax = plt.subplots(figsize=(12, 6))
    
    algorithms = sorted(alg_times.keys())
    avg_times = [np.mean(alg_times[alg]) for alg in algorithms]
    success_rates = [np.mean(alg_success[alg]) * 100 for alg in algorithms]
    
    # Màu theo tỷ lệ thành công
    colors = ['#4CAF50' if sr >= 80 else '#FFC107' if sr >= 30 else '#F44336' 
              for sr in success_rates]
    
    x = np.arange(len(algorithms))
    bars = ax.bar(x, avg_times, color=colors, alpha=0.7, edgecolor='black')
    
    # Thêm giá trị trên cột
    for i, (bar, time_val, sr) in enumerate(zip(bars, avg_times, success_rates)):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{time_val:.1f}ms\n({sr:.0f}%)',
                ha='center', va='bottom', fontsize=8)
    
    ax.set_xlabel('Thuật toán', fontsize=12)
    ax.set_ylabel('Thời gian trung bình (ms)', fontsize=12)
    ax.set_title('So sánh hiệu suất thuật toán', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(algorithms, rotation=45, ha='right')
    ax.grid(axis='y', alpha=0.3)
    
    # Legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#4CAF50', label='Tỷ lệ thành công ≥ 80%'),
        Patch(facecolor='#FFC107', label='Tỷ lệ thành công 30-80%'),
        Patch(facecolor='#F44336', label='Tỷ lệ thành công < 30%')
    ]
    ax.legend(handles=legend_elements, loc='upper left')
    
    plt.tight_layout()
    plt.show()
