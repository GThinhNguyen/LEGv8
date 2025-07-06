"""
Module chứa các hàm vẽ và hiển thị
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
from simulate_data import lines, full_names, line_next

def format_multiline(text):
    """Định dạng tên block cho phép xuống dòng bằng ký tự '\\n'."""
    return r"$\bf{" + text.replace('\n', r'}$' + '\n' + r'$\bf{') + r"}$"

def draw_bezier(ax, p0, p1, p2, color='red', lw=2, zorder=1, num=100):
    """Vẽ đường cong Bezier bậc 2 từ p0, p1, p2"""
    t = np.linspace(0, 1, num)
    bezier_x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
    bezier_y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
    ax.plot(bezier_x, bezier_y, color=color, lw=lw, zorder=zorder)


#draw shapes
def _draw_rectangular_shapes(ax, name, poly, rounded_rects, ellipses, zorder):
    """Vẽ các hình chữ nhật và biến thể"""
    x0, y0 = poly[0]
    x1, y1 = poly[1]
    left, right = min(x0, x1), max(x0, x1)
    bottom, top = min(y0, y1), max(y0, y1)
    width, height = right - left, top - bottom

    if name in ['AND1', 'AND2']:
        _draw_and_gate(ax, left, bottom, top, width, height, zorder)
    elif name in ['OR']:
        _draw_or_gate(ax, left, bottom, top, width, height, zorder)
    elif name in rounded_rects:
        ax.add_patch(FancyBboxPatch((left, bottom), width, height,
                                    boxstyle="round,pad=0.02,rounding_size=15",
                                    linewidth=2, edgecolor='red', facecolor='none', zorder=zorder))
    elif name in ellipses:
        ax.add_patch(patches.Ellipse(((left + right) / 2, (bottom + top) / 2),
                                     width, height, linewidth=2, edgecolor='red',
                                     facecolor='none', zorder=zorder))
    else:
        ax.add_patch(patches.Rectangle((left, bottom), width, height,
                                       linewidth=2, edgecolor='red', facecolor='none', zorder=zorder))

def _draw_and_gate(ax, left, bottom, top, width, height, zorder):
    """Vẽ cổng AND"""
    rect_width = width * 0.2
    ax.plot([left, left + rect_width], [bottom, bottom], color='red', lw=2, zorder=zorder)
    ax.plot([left, left], [bottom, top], color='red', lw=2, zorder=zorder)
    ax.plot([left, left + rect_width], [top, top], color='red', lw=2, zorder=zorder)
    center_x = left + rect_width
    center_y = bottom + height / 2
    arc = patches.Arc((center_x, center_y), height, height, angle=0,
                      theta1=-90, theta2=90, linewidth=2, edgecolor='red', zorder=zorder)
    ax.add_patch(arc)

def _draw_or_gate(ax, left, bottom, top, width, height, zorder):
    """Vẽ cổng OR sử dụng hàm bezier"""
    # Left curved side
    p0 = [left, bottom]
    p1 = [left + width * 0.5, bottom + height * 0.5]
    p2 = [left, top]
    draw_bezier(ax, p0, p1, p2, zorder=zorder)

    # Top curved side
    p0_top = [left, top]
    p1_top = [left + width * 0.7, top]
    p2_top = [left + width, bottom + height * 0.5]
    draw_bezier(ax, p0_top, p1_top, p2_top, zorder=zorder)

    # Bottom curved side
    p0_bot = [left, bottom]
    p1_bot = [left + width * 0.7, bottom]
    p2_bot = [left + width, bottom + height * 0.5]
    draw_bezier(ax, p0_bot, p1_bot, p2_bot, zorder=zorder)

def _draw_add_shapes(ax, poly, zorder):
    """Vẽ các hình phức tạp (ALU, ADD gates)"""
    ax.plot(*poly.T, lw=2, color='red', zorder=zorder)
    if not np.allclose(poly[0], poly[-1]):
        ax.plot([poly[-1,0], poly[0,0]], [poly[-1,1], poly[0,1]], lw=2, color='red', zorder=zorder)

def _add_component_labels(ax, polygons_dict):
    """Thêm các nhãn cho components"""
    # Labels for IM
    ax.text(40 - 3, 470 + 3, "Instruction\n[31-0]", color='black', 
           fontsize=9, ha='right', va='top', zorder=2, linespacing=0.8)
    ax.text(-120 + 3, 520 - 3, "Read\naddress", color='black', 
           fontsize=9, ha='left', va='top', zorder=2, linespacing=0.8)

    # Labels for Registers
    reg_left, reg_right = 600, 770
    reg_labels_left = [
        ("Read\nregister 1", 470),
        ("Read\nregister 2", 530),
        ("Write\nregister", 590),
        ("Write data", 635)
    ]
    for label, y in reg_labels_left:
        ax.text(reg_left + 3, y, label, color='black', fontsize=9, 
               ha='left', va='center', zorder=2, linespacing=0.8)
               
    reg_labels_right = [("Read\ndata 1", 500), ("Read\ndata 2", 570)]
    for label, y in reg_labels_right:
        ax.text(reg_right - 3, y, label, color='black', fontsize=9, 
               ha='right', va='center', zorder=2, linespacing=0.8)

    # Labels for Memory
    mem_left, mem_right = polygons_dict['Mem'][0][0], polygons_dict['Mem'][1][0]
    mem_labels_left = [("Address", 650), ("Write\ndata", 700)]
    for label, y in mem_labels_left:
        ax.text(mem_left + 3, y, label, color='black', fontsize=9, 
               ha='left', va='center', zorder=2, linespacing=0.8)
    ax.text(mem_right - 3, 640, "Read\ndata", color='black', fontsize=9, 
           ha='right', va='center', zorder=2, linespacing=0.8)

    # ALU Zero label
    alu_zero_x, alu_zero_y = polygons_dict.get('ALU', np.array([[0,0]]))[0]
    ax.text(alu_zero_x - 3, 540, "Zero", color='black', fontsize=9, 
           ha='right', va='center', zorder=2, linespacing=0.8)

    # Control output ports
    control_right = polygons_dict['Control'][1][0]
    control_lines = [lines[n] for n in line_next.get('Control', []) if n in lines]
    control_ports = [
        "Reg2Loc", "Uncondbranch", "Branch", "ZeroBranch", "MemRead",
        "MemtoReg", "MemWrite", "FlagWrite", "ALUSrc", "ALUOp", "RegWrite"
    ]
    if len(control_lines) == len(control_ports):
        for port, line in zip(control_ports, control_lines):
            ax.text(control_right + 10, line[0][1] - 7, port, color='black', 
                   fontsize=9, ha='left', va='center', zorder=2)

    # Instruction field labels
    instruction_labels = [
        (100 + 4, 500 - 12, "Inst[31-0]"),
        (210 + 4, 560 - 12, "Inst[4-0]"),
        (210 + 4, 500 - 12, "Inst[20-16]"),
        (210 + 4, 470 - 12, "Inst[9-5]"),
        (210 + 4, 330 - 12, "Inst[31-21]"),
        (210 + 4, 750 - 12, "Inst[31-0]"),
        (440 + 4, 750 - 12, "Inst[31-0]"),
        (440 + 4, 820 - 12, "Inst[31-21]"),
        (120 - 4, 30 - 12, "4"),
    ]
    
    for x, y, label in instruction_labels:
        ax.text(x, y, label, color='black', fontsize=9, 
               ha='left', va='center', zorder=2)


def show_text(ax, polygons_dict):
    """Hiển thị tên block, các nhãn phụ và vẽ component Flags cho sơ đồ"""
    rects = {'PC', 'IM', 'Reg', 'Mem'}
    rounded_rects = {'M1', 'M2', 'M3', 'M4'}
    ellipses = {'SE', 'ALUControl', 'Control', 'SL2'}

    for name, poly in polygons_dict.items():
        poly = np.array(poly)
        if poly.ndim != 2 or poly.shape[0] < 2:
            continue

        display_name = full_names.get(name, name)

        if poly.shape[0] == 2:
            x0, y0 = poly[0]
            x1, y1 = poly[1]
            left, right = min(x0, x1), max(x0, x1)
            bottom, top = min(y0, y1), max(y0, y1)
            cx, cy = (left + right) / 2, (bottom + top) / 2

            if name in rects:
                ax.text(right - 3, top - 3, format_multiline(display_name),
                        color='black', fontsize=11, ha='right', va='bottom',
                        zorder=3, linespacing=0.8)
            elif name in ellipses:
                ax.text(cx, cy, format_multiline(display_name),
                        color='black', fontsize=11, ha='center', va='center',
                        zorder=3, linespacing=0.8)
            elif name.startswith('M') and name in rounded_rects:
                ax.text(cx, bottom + 30, '0', color='black', fontsize=11,
                        ha='center', va='bottom', zorder=3)
                ax.text(cx, top - 30, '1', color='black', fontsize=11,
                        ha='center', va='top', zorder=3)
            if name == 'Flags':
                width, height = right - left, top - bottom
                box_width = width / 4
                labels = ['N', 'Z', 'C', 'V']
                for i, label in enumerate(labels):
                    ax.add_patch(patches.Rectangle((left + i * box_width, bottom), box_width, height,
                                                   linewidth=2, edgecolor='red', facecolor='none', zorder=3))
                    cx_box = left + (i + 0.5) * box_width
                    cy_box = bottom + height / 2
                    ax.text(cx_box, cy_box, label, color='black', fontsize=12, ha='center', va='center', zorder=3)
        elif name == 'ALU':
            poly_alu = np.array(polygons_dict['ALU'])
            min_x, max_x = np.min(poly_alu[:, 0]), np.max(poly_alu[:, 0])
            min_y, max_y = np.min(poly_alu[:, 1]), np.max(poly_alu[:, 1])
            cx_alu = (min_x + max_x) / 2
            cy_alu = (min_y + max_y) / 2
            ax.text(cx_alu, cy_alu + 20, format_multiline('ALU'),
                    color='black', fontsize=11, ha='center', va='center',
                    zorder=3, linespacing=0.8)

    _add_component_labels(ax, polygons_dict)

def show_background(ax, path, zorder=0):
    """Hiển thị background image"""
    import matplotlib.image as mpimg
    img = mpimg.imread(path)
    ax.imshow(img, extent=[0, img.shape[1], img.shape[0], 0], zorder=zorder)

def show_polygons(ax, polygons_dict, zorder=3):
    """Vẽ tất cả các polygon shapes"""
    rounded_rects = {'M1', 'M2', 'M3', 'M4'}
    ellipses = {'SE', 'ALUControl', 'Control', 'SL2'}

    for name, poly in polygons_dict.items():
        poly = np.array(poly)
        if poly.ndim != 2 or poly.shape[0] < 2:
            continue
            
        if poly.shape[0] == 2:
            _draw_rectangular_shapes(ax, name, poly, rounded_rects, ellipses, zorder)
        else:
            _draw_add_shapes(ax, poly, zorder)

def show_lines(ax, lines_dict, zorder=2):
    """Vẽ tất cả các đường lines"""
    brown_lines = set(
        [f"L{i}" for i in range(13, 24)] +
        [f"L{i}" for i in range(24, 29)] +
        ["L60", "L48"]
    )
    
    for name, line in lines_dict.items():
        line = np.array(line)
        if line.ndim != 2 or line.shape[0] < 2:
            continue
            
        if name in brown_lines:
            color = "#AF7B62"
            lw = 1
        else:
            color = 'black'
            lw = 1.1
            
        ax.plot(*line.T, lw=lw, color=color, zorder=zorder)

def show_points(ax, point_coords, zorder=5):
    """Vẽ tất cả các points"""
    for name, (x, y) in point_coords.items():
        ax.plot(x, y, 'o', color='red', markersize=4, zorder=zorder)