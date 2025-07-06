"""
Module chứa các hàm highlight lines
"""
import numpy as np

def highlight_next_lines(ax, current_block, line_next, lines, zorder=2):
    """
    Highlight các đường line tiếp theo từ current_block
    """
    highlighted_lines = []
    next_lines = line_next.get(current_block, [])

    for line_name in next_lines:
        if line_name in lines:
            line_data = np.array(lines[line_name])
            if line_data.ndim == 2 and line_data.shape[0] >= 2:
                line_obj = ax.plot(*line_data.T, lw=3, color='blue', zorder=zorder, alpha=0.5)
                highlighted_lines.extend(line_obj)

    return highlighted_lines

def clear_highlighted_lines(highlighted_lines):
    """Xóa các đường line đã highlight"""
    for line in highlighted_lines:
        try:
            line.remove()
        except:
            pass

def manage_line_highlights(ax, current_block, line_next, lines, old_highlights=None):
    """
    Quản lý highlight các đường line - xóa cũ và tạo mới
    """
    if old_highlights:
        clear_highlighted_lines(old_highlights)
    
    return highlight_next_lines(ax, current_block, line_next, lines)