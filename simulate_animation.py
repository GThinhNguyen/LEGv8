"""
Module chứa các hàm animation
"""
import numpy as np
import matplotlib.patches as patches
import matplotlib.animation as animation
from matplotlib.patches import FancyBboxPatch
from simulate_core import logic_step_from_block, add2
from simulate_data import points, connection_map, lines
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

    def clear_all_squares_from(self, paths):
        """Xóa tất cả animated squares có path nằm trong danh sách paths"""
        if hasattr(self.ax, 'existing_squares'):
            # Python
            print(paths)
            remove_keys = []
            for k, sq in self.ax.existing_squares.items():
                found = False
                for p in paths:
                    if np.array_equal(sq['path'], lines[p]):
                        found = True
                        break
                if found:
                    remove_keys.append(k)

            for k in remove_keys:
                try:
                    sq = self.ax.existing_squares.pop(k)
                    sq['patch'].remove()
                    sq['text'].remove()
                except Exception:
                    pass


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
            sq['text'].set_position((patch_center_x - width/2, patch_center_y + height/2))


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

    return _create_new_square(ax, key, path, display_bit_str, bit_str, to_key, zorder)


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

CURRENT_ANIMATION_SPEED = 10  # Giá trị mặc định

def set_animation_speed(speed):
    """Cập nhật tốc độ animation ngay lập tức"""
    global CURRENT_ANIMATION_SPEED
    CURRENT_ANIMATION_SPEED = (speed - 1) ** 1.7

def update_square_position(sq, speed=None):
    """Cập nhật vị trí của một square"""
    global CURRENT_ANIMATION_SPEED
    # Sử dụng tốc độ hiện tại nếu không truyền vào
    speed_to_use = CURRENT_ANIMATION_SPEED
    
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
    sq['text'].set_position((pos[0] - width/2, pos[1] + height/2))

    # Cập nhật distance sử dụng tốc độ hiện tại
    if distance_travelled < total_len:
        sq['distance_travelled'] = min(total_len, distance_travelled + speed_to_use)


def run_by_step_with_animate(
    ax, start_block, lines, line_next, ui, interval=2, speed=15, zorder=10, on_finished=None
):
    """
    Chạy animation cho một block với tối ưu performance.
    - ax: matplotlib axes
    - start_block: block bắt đầu
    - lines: dict các đường đi
    - line_next: dict các block tiếp theo
    - ui: dữ liệu giao diện
    - interval: thời gian giữa các frame (ms)
    - speed: tốc độ di chuyển square
    - zorder: thứ tự vẽ
    - on_finished: callback khi hoàn thành
    """
    # Đưa tất cả squares về cuối đường (reset trạng thái)
    animation_manager = AnimationManager(ax)
    animation_manager.move_squares_to_end()

    # Lấy dữ liệu bit và xử lý logic cho block hiện tại
    bit_tuple = bits.get_bits_for_path(start_block, ui)
    logic_step_from_block(start_block, lines, line_next, ui)

    # Tạo danh sách các squares sẽ di chuyển
    move_squares = []
    # Lấy các block tiếp theo hợp lệ
    next_blocks = [n for n in line_next.get(start_block, []) if n in lines]

    for idx, next_name in enumerate(next_blocks):
        next_path = lines[next_name]
        # Lấy bit string phù hợp cho từng nhánh
        if isinstance(bit_tuple, (tuple, list)):
            bit_str = bit_tuple[idx] if idx < len(bit_tuple) else bit_tuple[-1]
        else:
            bit_str = str(bit_tuple)
        # Tạo square và thêm vào danh sách
        sq = create_animated_square(ax, next_path, start_block, next_name, bit_str, zorder)
        move_squares.append(sq)

    # Cờ đánh dấu đã hoàn thành cho từng square
    finished_flags = [False] * len(move_squares)

    def update(frame):
        """
        Hàm update cho animation, di chuyển các squares.
        """
        all_done = True
        for i, sq in enumerate(move_squares):
            update_square_position(sq, speed)
            # Kiểm tra đã đến cuối đường chưa
            if sq['distance_travelled'] < sq['total_len']:
                all_done = False
            else:
                finished_flags[i] = True
                
        # CÁCH SỬA: Gọi callback trực tiếp và dừng animation khi xong
        if all_done and on_finished and not getattr(update, "_called", False):
            update._called = True
            print("Calling on_finished callback")
            # Dừng animation trước khi gọi callback
            ani.event_source.stop()
            # Gọi callback trực tiếp
            on_finished()
            
        # Trả về các artist để vẽ lại
        return [sq['patch'] for sq in move_squares] + [sq['text'] for sq in move_squares]

    # Tạo animation FuncAnimation
    ani = animation.FuncAnimation(
        ax.figure, update,
        interval=interval,
        blit=False,
        cache_frame_data=False
    )
    return ani

def clear_animated_squares(ax):
    """Xóa tất cả animated squares"""
    animation_manager = AnimationManager(ax)
    animation_manager.clear_all_squares()

def clear_animated_squares_from(ax, paths):
    """Xóa tất cả animated squares bắt đầu trên paths"""
    animation_manager = AnimationManager(ax)
    animation_manager.clear_all_squares_from(paths)