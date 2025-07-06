"""
Module chứa các hàm animation
"""
import numpy as np
import matplotlib.patches as patches
import matplotlib.animation as animation
from matplotlib.patches import FancyBboxPatch
from simulate_core import logic_step_from_block, add2
from simulate_data import points, connection_map
import bits

class AnimationManager:
    """Class quản lý animation squares"""
    
    def __init__(self, ax):
        self.ax = ax
        if not hasattr(ax, 'existing_squares'):
            ax.existing_squares = {}
    
    def clear_all_squares(self):
        """Xóa tất cả animation squares"""
        if hasattr(self.ax, 'existing_squares'):
            for sq in list(self.ax.existing_squares.values()):
                try:
                    sq['patch'].remove()
                    sq['text'].remove()
                except Exception:
                    pass
            self.ax.existing_squares.clear()
    
    def move_squares_to_end(self):
        """Đưa tất cả squares về cuối đường"""
        for sq in self.ax.existing_squares.values():
            path = sq['path']
            seg_lens = np.linalg.norm(np.diff(path, axis=0), axis=1)
            total_len = np.sum(seg_lens)
            sq['distance_travelled'] = total_len

            # Điều chỉnh vị trí kết thúc
            width = sq['patch'].get_width()
            height = sq['patch'].get_height()
            patch_center_x = path[-1][0]
            patch_center_y = path[-1][1]
            sq['patch'].set_x(patch_center_x - width)
            sq['patch'].set_y(patch_center_y)            
            sq['text'].set_position((patch_center_x - width/2, patch_center_y + height/2))  # ← SỬA ĐÂY
            
def create_animated_square(ax, path, start_block, to_key, bit_str, zorder=10):
    """Tạo một animated square mới"""
    key = (start_block, to_key)
    display_bit_str = add2(bit_str, [to_key])
    
    # Xóa squares liên quan nếu start_block là point
    if start_block in points:
        remove_keys = [
            k for k, sq in ax.existing_squares.items()
            if any(conn['to'] == start_block for conn in connection_map.get(sq['to'], []))
        ]
        for k in remove_keys:
            sq_rm = ax.existing_squares.pop(k)
            sq_rm['patch'].remove()
            sq_rm['text'].remove()

    if key in ax.existing_squares:
        return _update_existing_square(ax, key, path, display_bit_str, bit_str)
    else:
        return _create_new_square(ax, key, path, display_bit_str, bit_str, to_key, zorder)

def _update_existing_square(ax, key, path, display_bit_str, bit_str):
    """Cập nhật square đã tồn tại"""
    sq = ax.existing_squares[key]
    sq['distance_travelled'] = 0.0
    sq['text'].set_text(display_bit_str)
    sq['text'].set_weight('bold')

    # Cập nhật kích thước
    renderer = ax.figure.canvas.get_renderer()
    sq['text'].set_text(bit_str)
    bbox = sq['text'].get_window_extent(renderer=renderer)
    inv = ax.transData.inverted()
    bbox_data = bbox.transformed(inv)
    width = bbox_data.width
    height = bbox_data.height
    
    # Cập nhật patch size
    if hasattr(sq['patch'], 'set_width'):
        sq['patch'].set_width(width)
        sq['patch'].set_height(height)

    # Điều chỉnh vị trí spawn
    patch_center_x = path[0][0]
    patch_center_y = path[0][1]
    sq['patch'].set_xy((patch_center_x - width/2, patch_center_y - height/2))
    sq['text'].set_position((patch_center_x - width/2, patch_center_y + height/2))  # ← SỬA ĐÂY
    return sq

def _create_new_square(ax, key, path, display_bit_str, bit_str, to_key, zorder):
    """Tạo square mới"""
    # Tính kích thước text
    temp_text = ax.text(0, 0, display_bit_str, color='white', ha='center', va='center', 
                        fontsize=10, zorder=zorder, weight='bold')
    renderer = ax.figure.canvas.get_renderer()
    bbox = temp_text.get_window_extent(renderer=renderer)
    inv = ax.transData.inverted()
    bbox_data = bbox.transformed(inv)
    width = bbox_data.width
    height = bbox_data.height
    temp_text.remove()

    # Vị trí spawn
    patch_center_x = path[0][0]
    patch_center_y = path[0][1]

    rect = patches.FancyBboxPatch(
        (patch_center_x - width, patch_center_y), 
        width, height,
        boxstyle="round4,pad=0.02",
        edgecolor='black',
        linewidth=1,
        zorder=zorder
    )

    ax.add_patch(rect)
    
    
    # Tạo text với tọa độ mới
    text = ax.text(
        patch_center_x - width/2, patch_center_y + height/2, display_bit_str,  # ← SỬA ĐÂY
        color='white', ha='center', va='center', fontsize=10, zorder=zorder+1,
        weight='bold'
    )
    
    # Tạo square object
    sq = {
        'patch': rect, 
        'text': text, 
        'path': path, 
        'distance_travelled': 0.0, 
        'to': to_key,
        'seg_lens': np.linalg.norm(np.diff(path, axis=0), axis=1),
        'total_len': np.sum(np.linalg.norm(np.diff(path, axis=0), axis=1))
    }
    ax.existing_squares[key] = sq
    return sq

def update_square_position(sq, speed):
    """Cập nhật vị trí của một square"""
    path = sq['path']
    distance_travelled = sq['distance_travelled']
    seg_lens = sq.get('seg_lens', np.linalg.norm(np.diff(path, axis=0), axis=1))
    total_len = sq.get('total_len', np.sum(seg_lens))
    
    # Tính vị trí mới
    remain = distance_travelled
    pos = None
    
    for i, seg_len in enumerate(seg_lens):
        if remain < seg_len:
            t = remain / seg_len
            pos = (1 - t) * path[i] + t * path[i + 1]
            break
        remain -= seg_len
    else:
        pos = path[-1]

    # Cập nhật vị trí patch và text
    width = sq['patch'].get_width()
    height = sq['patch'].get_height()
    sq['patch'].set_x(pos[0] - width)
    sq['patch'].set_y(pos[1])
    sq['text'].set_position((pos[0] - width/2, pos[1] + height/2))  # Thay vì (pos[0] - width, pos[1])

    # Cập nhật distance
    if distance_travelled < total_len:
        sq['distance_travelled'] = min(total_len, distance_travelled + speed)

def run_by_step_with_animate(ax, start_block, lines, line_next, ui, interval=20, speed=30, zorder=10):
    """
    Chạy animation cho một block với tối ưu performance
    """
    animation_manager = AnimationManager(ax)
    animation_manager.move_squares_to_end()

    # Lấy dữ liệu và xử lý logic
    bit_tuple = bits.get_bits_for_path(start_block, ui)
    logic_step_from_block(start_block, lines, line_next, ui)

    # Tạo squares
    move_squares = []
    next_blocks = [n for n in line_next.get(start_block, []) if n in lines]
    
    for idx, next_name in enumerate(next_blocks):
        next_path = lines[next_name]
        
        # Lấy bit string
        if isinstance(bit_tuple, (tuple, list)):
            bit_str = bit_tuple[idx] if idx < len(bit_tuple) else bit_tuple[-1]
        else:
            bit_str = str(bit_tuple)
            
        # Tạo square
        sq = create_animated_square(ax, next_path, start_block, next_name, bit_str, zorder)
        move_squares.append(sq)

    def update(frame):
        """Update function được tối ưu"""
        active_patches = []
        for sq in move_squares:
            update_square_position(sq, speed)
            active_patches.extend([sq['patch'], sq['text']])
        return active_patches

    # Tạo animation với interval được tối ưu
    ani = animation.FuncAnimation(
        ax.figure, update, 
        interval=max(interval, 50),  # Minimum 50ms để tránh lag
        blit=False, 
        cache_frame_data=False
    )
    return ani

def run_all_with_animate(ax, start_blocks, lines, line_next, ui, interval=20, speed=30, zorder=10, delay_between_animations=500):
    """
    Chạy animation liên tục cho nhiều blocks
    """
    if not start_blocks:
        return None
    
    current_index = [0]
    current_animation = [None]
    
    def run_next_animation():
        if current_index[0] >= len(start_blocks):
            print("Đã hoàn thành tất cả animation!")
            return
        
        current_block = start_blocks[current_index[0]]
        print(f"Đang chạy animation cho block: {current_block}")
        
        # Chạy animation
        ani = run_by_step_with_animate(ax, current_block, lines, line_next, ui, interval, speed, zorder)
        current_animation[0] = ani
        
        # Tính thời gian animation
        next_blocks = line_next.get(current_block, [])
        animation_time = _calculate_animation_time(next_blocks, lines, speed, interval, delay_between_animations)
        
        current_index[0] += 1
        
        # Lên lịch animation tiếp theo
        def schedule_next():
            ax.figure.canvas.draw_idle()
            run_next_animation()
        
        timer = ax.figure.canvas.new_timer(interval=animation_time)
        timer.single_shot = True
        timer.add_callback(schedule_next)
        timer.start()
    
    run_next_animation()
    return current_animation[0]

def _calculate_animation_time(next_blocks, lines, speed, interval, delay):
    """Tính thời gian animation dựa trên độ dài đường"""
    max_length = 0
    for next_name in next_blocks:
        if next_name in lines:
            line_data = np.array(lines[next_name])
            if line_data.ndim == 2 and line_data.shape[0] >= 2:
                seg_lens = np.linalg.norm(np.diff(line_data, axis=0), axis=1)
                total_len = np.sum(seg_lens)
                max_length = max(max_length, total_len)
    
    return int((max_length / speed) * interval) + delay if max_length > 0 else delay

def clear_animated_squares(ax):
    """Xóa tất cả animated squares"""
    animation_manager = AnimationManager(ax)
    animation_manager.clear_all_squares()