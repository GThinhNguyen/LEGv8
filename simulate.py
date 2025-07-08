"""
Main simulation module - tổng hợp tất cả functionality
"""
import matplotlib.pyplot as plt

from simulate_data import *
from simulate_core import *
from simulate_render import *
from simulate_animation import *
from simulate_highlight import *

# Compatibility exports
__all__ = [
    # Data
    'polygons', 'lines', 'points', 'line_next', 'connection_map', 'full_names',
    
    # Core functions
    'logic_step_from_block', 'add2', 'get_simulation_order',
    
    # Rendering functions
    'show_polygons', 'show_lines', 'show_points', 'show_name', 'show_background',
    
    # Animation functions
    'run_by_step_with_animate', 'run_all_with_animate', 'clear_animated_squares',
    'AnimationManager', 'create_animated_square',
    
    # Highlighting functions
    'highlight_next_lines', 'clear_highlighted_lines', 'manage_line_highlights',
    
    # Matplotlib
    'plt'
]

def get_previous_block(current_step):
    """Trả về block trước đó dựa trên current_step"""
    order = [
        'PC', 'P1', 'IM', 'P2', 'Control',
        'P3', 'M1', 'Reg', 'P5',  
        'P4', 'ALUControl', 'SE', 'P6', 'M2', 'ALU', 'P7', 'Mem', 
        'M3', 'Flags', 'AND1', 'AND2', 'OR',
        'SL2', 'P8', 'ADD1', 'ADD2', 'M4'
    ]
    if current_step > 0:
        return order[current_step - 1]
    return None


# Convenience function for quick setup
def setup_simulation_plot(figsize=(25, 12)):
    """Thiết lập plot cơ bản cho simulation"""
    fig, ax = plt.subplots(figsize=figsize)
    
    show_polygons(ax, polygons)
    show_lines(ax, lines)
    show_points(ax, points)
    show_text(ax, polygons)
    
    ax.set_aspect('equal')
    ax.autoscale(enable=True)
    ax.invert_yaxis()
    ax.axis('off')
    
    return fig, ax