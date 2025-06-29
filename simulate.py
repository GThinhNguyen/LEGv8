import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
from matplotlib.path import Path
import bits  # Thêm dòng này ở đầu file
# Đã cộng thêm 200 vào các tọa độ X lớn hơn hoặc bằng 1310
polygons = {
    'PC': np.array([[ -250, 520], [ -200, 570]]),  # -90-100, -40-100
    'IM': np.array([[-120, 470], [ 30, 630]]),     # 40-100, 180-100
    'Reg': np.array([[600, 450], [770, 690]]),
    'Mem': np.array([[1200, 620], [1350, 800]]),  # 1200,1300 -> 1400,1500
    'Flags': np.array([[1000, 400], [1160, 440]]),

    'M1': np.array([[470, 480], [500, 580]]),
    'M2': np.array([[900, 550], [930, 650]]),
    'M3': np.array([[1690, 560], [1720, 660]]),  # 1490,1520 -> 1690,1720
    'M4': np.array([[1630, 45], [1660, 145]]),   # 1430,1460 -> 1630,1660

    'SE': np.array([[680, 700], [780, 800]]),
    'SL2': np.array([[940, 110], [1020, 190]]),
    'ALUControl': np.array([[910, 770], [1010, 870]]),
    'Control': np.array([[360, 220], [460, 440]]),

    'ALU': np.array([[1120, 520], [1120, 600], [1000, 640], [1000, 570], [1030, 560], [1000, 550], [1000, 480]]),
    'ADD2': np.array([[1180, 110], [1180, 145], [1120, 165], [1120, 132.5], [1135, 127.5], [1120, 122.5], [1120, 90]]),
    'ADD1': np.array([[240, 50], [240, 85], [180, 105], [180, 72.5], [195, 67.5], [180, 62.5], [180, 30]]),

    'OR': np.array([[1550, 240], [1610, 320]]),   # 1350,1410 -> 1550,1610
    'AND1': np.array([[1380, 360], [1480, 440]]), # 1350,1410 -> 1550,1610
    'AND2': np.array([[1380, 480], [1480, 560]]), # 1350,1410 -> 1550,1610
}

# Tọa độ các điểm dựa vào connection_map và lines
points = {
    'P1': (-160, 530),         # Đầu vào của IM (L59)
    'P2': (210, 550),          # Nút giao L29, L30, L31, L32, L33, L34, L35, L36, L39
    'P3': (360, 590),          # Nút giao L36, L37, L38
    'P4': (600, 750),          # Nút giao L39, L40, L53
    'P5': (810, 570),          # Nút giao L42, L43, L44
    'P6': (850, 630),          # Nút giao L54, L55, L56
    'P7': (1150, 570),         # Nút giao L45, L46, L47
    'P8': (-160, 100),         # Nút giao L1, L2, L5
}

lines = {
    'L18': np.array([[420, 220], [1705, 220], [1705, 550]]),  # 1505+200
    'L14': np.array([[430, 242], [1550, 242]]),               # 1350+200
    'L15': np.array([[440, 264], [1340, 264], [1340, 380], [1380, 380]]),  # 1270+200,1275+200
    'L16': np.array([[450, 286], [1300, 286], [1300, 500], [1380, 500]]),  # 1250+200,1270+200
    'L17': np.array([[460, 308], [1260, 308], [1260, 620]]),               # 1240+200
    'L19': np.array([[460, 330], [1220, 330], [1220, 620]]),               # 1200+200
    'L20': np.array([[460, 352], [1080, 352], [1080, 400]]),
    'L22': np.array([[450, 374], [960, 374], [960, 750]]),
    'L21': np.array([[440, 396], [915, 396], [915, 550]]),
    'L23': np.array([[430, 418], [685, 418], [685, 450]]),
    'L13': np.array([[420, 440], [485, 440], [485, 480]]),

    'L24': np.array([[1010, 820], [1070, 820], [1070, 600]]),

    'L25': np.array([[1120, 540], [1380, 540]]),              # 1250+200
    'L26': np.array([[1440, 400], [1480, 400], [1480, 280], [1560, 280]]),  # 1320+200,1325+200,1350+200
    'L27': np.array([[1605, 280], [1645, 280], [1645, 145]]),               # 1410+200,1440+200
    'L28': np.array([[1440, 520], [1520, 520], [1520, 315], [1560, 315]]),  # 1320+200,1330+200,1350+200

    'L45': np.array([[1120, 580], [1160, 580]]),              # 1230+200
    'L46': np.array([[1150, 570], [1150, 650], [1200, 650]]), # 1200+200
    'L47': np.array([[1160, 580], [1690, 580]]),              # 1230+200,1490+200

    'L48': np.array([[1070, 490], [1070, 450]]),

    'L29': np.array([[30, 550], [210, 550]]),
    'L30': np.array([[210, 550], [210, 500]]),
    'L31': np.array([[210, 500], [210, 470]]),
    'L32': np.array([[210, 470], [210, 330], [360, 330]]),
    'L33': np.array([[210, 470], [600, 470]]),
    'L34': np.array([[210, 500], [470, 500]]),
    'L35': np.array([[210, 540], [210, 590]]),
    'L36': np.array([[210, 590], [360, 590]]),
    'L37': np.array([[360, 590], [360, 560], [470, 560]]),
    'L38': np.array([[360, 590], [600, 590]]),
    'L39': np.array([[210, 590], [210, 750], [600, 750]]),
    'L40': np.array([[600, 750], [660, 750]]),
    'L53': np.array([[600, 740], [600, 820], [910, 820]]),

    'L41': np.array([[770, 500], [1000, 500]]),
    'L42': np.array([[770, 570], [810, 570]]),
    'L43': np.array([[810, 570], [900, 570]]),
    'L44': np.array([[810, 570], [810, 690], [1200, 690]]),   # 1200+200

    'L49': np.array([[1350, 640], [1690, 640]]),              # 1300+200,1490+200

    'L50': np.array([[500, 530], [600, 530]]),
    'L51': np.array([[930, 600], [1000, 600]]),
    'L52': np.array([[1720, 600], [1740, 600], [1740, 890], [570, 890], [570, 620], [600, 620]]),  # 1520+200,1540+200
    'L9a': np.array([[1660, 90], [1740, 90], [1740, 10], [ -225, 10], [ -225, 520]]),            # 1460+200,1540+200

    'L54': np.array([[770, 750], [850, 750], [850, 630]]),
    'L55': np.array([[850, 630], [900, 630]]),
    'L56': np.array([[850, 630], [850, 150], [920, 150]]),

    'L57': np.array([[1020, 150], [1120, 150]]),

    'L60': np.array([[1160, 420], [1380, 420]]),              # 1260+200

    'L58': np.array([[-200, 530], [-160, 530]]),
    'L59': np.array([[-160, 530], [-120, 530]]),
    'L1': np.array([[-160, 530], [-160, 100]]),
    'L5': np.array([[-160, 100], [1120, 100]]),
    'L2': np.array([[-160, 100], [-160, 40], [170, 40]]),

    'L4': np.array([[120, 80], [170, 80]]),

    'L8': np.array([[250, 70], [1620, 70]]),                  # 1420+200
    'L9b': np.array([[1180, 125], [1610, 125]])               # 1410+200
}



line_next = {
    # Control outputs
    'Control': ['L13','L14', 'L15', 'L16', 'L17', 'L18', 'L19', 'L20', 'L21', 'L22', 'L23'],
    'PC': ['L58'],
    'IM': ['L29'],
    'Reg': ['L41', 'L42'],
    'ALU': ['L25', 'L45', 'L48'],
    'ALUControl': ['L24'],
    'Mem': ['L49'],
    'Flags': ['L60'],
    'ADD1': ['L8'],
    'ADD2': ['L9b'],
    'AND1': ['L26'],
    'AND2': ['L28'],
    'OR': ['L27'],
    'SL2': ['L57'],
    'M1': ['L50'],
    'M2': ['L51'],
    'M3': ['L52'],
    'M4': ['L9a'],
    'SE': ['L54'],

    # Points to lines
    'P1': ['L59', 'L1'],
    'P2': ['L32', 'L33', 'L34', 'L36', 'L39'],
    'P3': ['L37', 'L38'],
    'P4': ['L40', 'L53'],
    'P5': ['L43', 'L44'],
    'P6': ['L55', 'L56'],
    'P7': ['L46', 'L47'],
    'P8': ['L2', 'L5'],
}

# key là tên block, value là list các dict chứa thông tin đối tượng đích, cổng và giá trị hiện tại
connection_map = {
    'L13': [{'to': 'M1', 'port': 'Control', 'value': '0'}],
    'L14': [{'to': 'OR', 'port': 'Inp0', 'value': '0'}],
    'L15': [{'to': 'AND1', 'port': 'Inp0', 'value': '0'}],
    'L16': [{'to': 'AND2', 'port': 'Inp0', 'value': '0'}],
    'L17': [{'to': 'Mem', 'port': 'MemRead', 'value': '0'}],
    'L18': [{'to': 'M3', 'port': 'Control', 'value': '0'}],
    'L19': [{'to': 'Mem', 'port': 'MemWrite', 'value': '0'}],
    'L20': [{'to': 'Flags', 'port': 'Control', 'value': '0'}],
    'L21': [{'to': 'M2', 'port': 'Control', 'value': '0'}],
    'L22': [{'to': 'ALUControl', 'port': 'ALUop', 'value': '0'}],
    'L23': [{'to': 'Reg', 'port': 'RegWrite', 'value': '0'}],
    'L24': [{'to': 'ALU', 'port': 'ALUControl', 'value': '0'}],
    'L25': [{'to': 'AND2', 'port': 'Inp1', 'value': '0'}],
    'L26': [{'to': 'OR', 'port': 'Inp1', 'value': '0'}],
    'L27': [{'to': 'M4', 'port': 'Control', 'value': '0'}],
    'L28': [{'to': 'OR', 'port': 'Inp2', 'value': '0'}],
    'L29': [{'to': 'P2', 'port': 'Inp0', 'value': '0'}],
    'L32': [{'to': 'Control', 'port': 'Inp0', 'value': '0'}],
    'L33': [{'to': 'Reg', 'port': 'ReadRegister1', 'value': '0'}],
    'L34': [{'to': 'M1', 'port': 'Inp0', 'value': '0'}],
    'L36': [{'to': 'P3', 'port': 'Inp0', 'value': '0'}],
    'L37': [{'to': 'M1', 'port': 'Inp1', 'value': '0'}],
    'L38': [{'to': 'Reg', 'port': 'WriteRegister', 'value': '0'}],
    'L39': [{'to': 'P4', 'port': 'Inp0', 'value': '0'}],
    'L40': [{'to': 'SE', 'port': 'Inp', 'value': '0'}],
    'L41': [{'to': 'ALU', 'port': 'ReadData1', 'value': '0'}],
    'L42': [{'to': 'P5', 'port': 'Inp0', 'value': '0'}],
    'L43': [{'to': 'M2', 'port': 'Inp0', 'value': '0'}],
    'L44': [{'to': 'Mem', 'port': 'WriteData', 'value': '0'}],
    'L45': [{'to': 'P7', 'port': 'Inp0', 'value': '0'}],
    'L46': [{'to': 'Mem', 'port': 'Address', 'value': '0'}],
    'L47': [{'to': 'M3', 'port': 'Inp0', 'value': '0'}],
    'L48': [{'to': 'Flags', 'port': 'NZCVtmp', 'value': '0'}],
    'L49': [{'to': 'M3', 'port': 'Inp1', 'value': '0'}],
    'L50': [{'to': 'Reg', 'port': 'ReadRegister2', 'value': '0'}],
    'L51': [{'to': 'ALU', 'port': 'ReadData2', 'value': '0'}],
    'L52': [{'to': 'Reg', 'port': 'WriteData', 'value': '0'}],
    'L53': [{'to': 'ALUControl', 'port': 'Ins', 'value': '0'}],
    'L54': [{'to': 'P6', 'port': 'Inp0', 'value': '0'}],
    'L55': [{'to': 'M2', 'port': 'Inp1', 'value': '0'}],
    'L56': [{'to': 'SL2', 'port': 'Inp0', 'value': '0'}],
    'L57': [{'to': 'ADD2', 'port': 'Inp1', 'value': '0'}],
    'L58': [{'to': 'P1', 'port': 'Inp0', 'value': '0'}],
    'L59': [{'to': 'IM', 'port': 'ReadAddress', 'value': '0'}],
    'L60': [{'to': 'AND1', 'port': 'Inp1', 'value': '0'}],
    'L1':  [{'to': 'P8', 'port': 'Inp0', 'value': '0'}],
    'L2':  [{'to': 'ADD1', 'port': 'Inp0', 'value': '0'}],
    'L4':  [{'to': 'ADD1', 'port': 'Inp1', 'value': '100'}],
    'L5':  [{'to': 'ADD2', 'port': 'Inp0', 'value': '0'}],
    'L8':  [{'to': 'M4', 'port': 'Inp0', 'value': '0'}],
    'L9a': [{'to': 'PC', 'port': 'Inp0', 'value': '0'}],
    'L9b': [{'to': 'M4', 'port': 'Inp1', 'value': '0'}],
}

# Mapping for full names of blocks, allow line breaks with \n
full_names = {
    'IM': 'Instruction\nmemory',
    'Reg': 'Registers',
    'Mem': 'Data\nmemory',
    'SE': 'Sign\nextend',
    'ALUControl': 'ALU\ncontrol',
    'SL2': 'Shift\nleft 2'
}
def format_multiline(text):
    """
    Định dạng tên block cho phép xuống dòng bằng ký tự '\\n'.
    """
    return r"$\bf{" + text.replace('\n', r'}$' + '\n' + r'$\bf{') + r"}$"

def show_name(ax, polygons_dict):
    """
    Hiển thị tên block và các nhãn phụ cho sơ đồ, cho phép tên xuống dòng.
    """
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
                ax.text(right - 3, top - 3, format_multiline(display_name), color='black', fontsize=11, ha='right', va='bottom', zorder=200, linespacing=0.8)
            elif name in ellipses:
                ax.text(cx, cy, format_multiline(display_name), color='black', fontsize=11, ha='center', va='center', zorder=200, linespacing=0.8)
            elif name.startswith('M') and name in rounded_rects:
                ax.text(cx, bottom + 30, '0', color='black', fontsize=11, ha='center', va='bottom', zorder=200)
                ax.text(cx, top - 30, '1', color='black', fontsize=11, ha='center', va='top', zorder=200)
        elif name == 'ALU':
            poly_alu = np.array(polygons_dict['ALU'])
            min_x, max_x = np.min(poly_alu[:, 0]), np.max(poly_alu[:, 0])
            min_y, max_y = np.min(poly_alu[:, 1]), np.max(poly_alu[:, 1])
            cx_alu = (min_x + max_x) / 2
            cy_alu = (min_y + max_y) / 2
            ax.text(cx_alu, cy_alu, format_multiline('ALU'), color='black', fontsize=11, ha='center', va='center', zorder=200, linespacing=0.8)

    # Nhãn phụ cho IM
    ax.text(30 - 3, 470 + 3, "Instruction\n[31-0]", color='black', fontsize=9, ha='right', va='top', zorder=200, linespacing=0.8)
    ax.text(-120 + 3, 520 - 3, "Read\naddress", color='black', fontsize=9, ha='left', va='top', zorder=200, linespacing=0.8)

    # Nhãn cho Reg
    reg_left, reg_right = 600, 770
    reg_labels_left = [
        ("Read\nregister 1", 470),
        ("Read\nregister 2", 530),
        ("Write\nregister", 590),
        ("Write data", 635)
    ]
    for label, y in reg_labels_left:
        ax.text(reg_left + 3, y, label, color='black', fontsize=9, ha='left', va='center', zorder=200, linespacing=0.8)
    reg_labels_right = [("Read\ndata 1", 500), ("Read\ndata 2", 570)]
    for label, y in reg_labels_right:
        ax.text(reg_right - 3, y, label, color='black', fontsize=9, ha='right', va='center', zorder=200, linespacing=0.8)

    # Nhãn cho Mem
    mem_left, mem_right = polygons_dict['Mem'][0][0], polygons_dict['Mem'][1][0]
    mem_labels_left = [("Address", 650), ("Write\ndata", 700)]
    for label, y in mem_labels_left:
        ax.text(mem_left + 3, y, label, color='black', fontsize=9, ha='left', va='center', zorder=200, linespacing=0.8)
    ax.text(mem_right - 3, 640, "Read\ndata", color='black', fontsize=9, ha='right', va='center', zorder=200, linespacing=0.8)

    # Nhãn cho ALU (Zero)
    alu_zero_x, alu_zero_y = polygons_dict.get('ALU', np.array([[0,0]]))[0]
    ax.text(alu_zero_x - 3, 520, "Zero", color='black', fontsize=9, ha='right', va='center', zorder=200, linespacing=0.8)

    # Hiển thị tên các cổng đầu ra của Control (bên phải, căn trái)
    control_right = polygons_dict['Control'][1][0]
    control_lines = [lines[n] for n in line_next.get('Control', []) if n in lines]
    control_ports = [
        "Reg2Loc", "Uncondbranch", "Branch", "ZeroBranch", "MemRead",
        "MemtoReg", "MemWrite", "FlagWrite", "ALUSrc", "ALUOp", "RegWrite"
    ]
    if len(control_lines) == len(control_ports):
        for port, line in zip(control_ports, control_lines):
            ax.text(control_right + 10, line[0][1] - 7, port, color='black', fontsize=9,
                    ha='left', va='center', zorder=200)


def show_background(ax, path):
    import matplotlib.image as mpimg
    img = mpimg.imread(path)
    ax.imshow(img, extent=[0, img.shape[1], img.shape[0], 0], zorder=0)

def show_polygons(ax, polygons_dict):
    import matplotlib.patches as patches
    from matplotlib.patches import FancyBboxPatch

    rounded_rects = {'M1', 'M2', 'M3', 'M4'}
    ellipses = {'SE', 'ALUControl', 'Control', 'SL2'}

    for name, poly in polygons_dict.items():
        poly = np.array(poly)
        if poly.ndim != 2 or poly.shape[0] < 2:
            continue
        if poly.shape[0] == 2:
            x0, y0 = poly[0]
            x1, y1 = poly[1]
            left, right = min(x0, x1), max(x0, x1)
            bottom, top = min(y0, y1), max(y0, y1)
            width, height = right - left, top - bottom

            if name in ['AND1', 'AND2']:
                # Vẽ nửa hình chữ nhật bên trái và nửa hình tròn bên phải cho AND1, AND2
                rect_width = width * 0.2
                # Vẽ 3 cạnh của hình chữ nhật bên trái (trên, trái, dưới)
                # Trên (chỉ vẽ 0.2 chiều dài)
                ax.plot([left, left + rect_width], [bottom, bottom], color='red', lw=2, zorder=5)
                # Trái
                ax.plot([left, left], [bottom, top], color='red', lw=2, zorder=5)
                # Dưới (chỉ vẽ 0.2 chiều dài)
                ax.plot([left, left + rect_width], [top, top], color='red', lw=2, zorder=5)
                # Nửa hình tròn bên phải
                center_x = left + rect_width
                center_y = bottom + height / 2
                theta1 = -90
                theta2 = 90
                arc = patches.Arc((center_x, center_y), height, height, angle=0,
                                  theta1=theta1, theta2=theta2, linewidth=2, edgecolor='red', zorder=5)
                ax.add_patch(arc)
            elif name in ['OR']:
                # Đường cong bên trái (dạng OR gate)
                # Vẽ một đường cong lồi bên trái, dùng Bezier
                p0 = [left, bottom]
                p1 = [left + width * 0.25, bottom + height * 0.5]
                p2 = [left, top]
                bezier_x = []
                bezier_y = []
                for t in np.linspace(0, 1, 100):
                    x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
                    y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
                    bezier_x.append(x)
                    bezier_y.append(y)
                ax.plot(bezier_x, bezier_y, color='red', lw=2, zorder=5)

                # Đường cong bên phải (nửa hình tròn)
                rect_width = width * 0.2
                center_x = left + rect_width
                center_y = bottom + height / 2
                theta = np.linspace(-np.pi/2, np.pi/2, 100)
                arc_x = center_x + (height/2) * np.cos(theta)
                arc_y = center_y + (height/2) * np.sin(theta)
                ax.plot(arc_x, arc_y, color='red', lw=2, zorder=5)
                # Nối đường cong với nửa đường tròn bằng đoạn thẳng
                # Điểm cuối của đường cong Bezier (p2)
                # Điểm đầu của nửa hình tròn (arc_x[0], arc_y[0])
                # Nối điểm đầu của đường cong Bezier với điểm đầu của nửa hình tròn
                ax.plot([bezier_x[0], arc_x[0]], [bezier_y[0], arc_y[0]], color='red', lw=2, zorder=5)
                # Nối điểm cuối của đường cong Bezier với điểm cuối của nửa hình tròn
                ax.plot([bezier_x[-1], arc_x[-1]], [bezier_y[-1], arc_y[-1]], color='red', lw=2, zorder=5)


            elif name in rounded_rects:
                ax.add_patch(FancyBboxPatch((left, bottom), width, height,
                                            boxstyle="round,pad=0.02,rounding_size=15",
                                            linewidth=2, edgecolor='red', facecolor='none', zorder=5))
            elif name in ellipses:
                ax.add_patch(patches.Ellipse(((left + right) / 2, (bottom + top) / 2),
                                             width, height, linewidth=2, edgecolor='red',
                                             facecolor='none', zorder=5))
            else:
                ax.add_patch(patches.Rectangle((left, bottom), width, height,
                                               linewidth=2, edgecolor='red', facecolor='none', zorder=5))
        else:
            ax.plot(*poly.T, lw=2, color='red', zorder=5)
            if not np.allclose(poly[0], poly[-1]):
                ax.plot([poly[-1,0], poly[0,0]], [poly[-1,1], poly[0,1]], lw=2, color='red', zorder=5)

    # Vẽ 4 ô nhỏ và nhãn ZNCV cho Flags
    if 'Flags' in polygons_dict:
        poly = np.array(polygons_dict['Flags'])
        x0, y0 = poly[0]
        x1, y1 = poly[1]
        left, right = min(x0, x1), max(x0, x1)
        bottom, top = min(y0, y1), max(y0, y1)
        width, height = right - left, top - bottom
        box_width = width / 4
        labels = ['N', 'Z', 'C', 'V']
        for i, label in enumerate(labels):
            ax.add_patch(patches.Rectangle((left + i * box_width, bottom), box_width, height,
                                           linewidth=2, edgecolor='red', facecolor='none', zorder=6))
            cx = left + (i + 0.5) * box_width
            cy = bottom + height / 2
            ax.text(cx, cy, label, color='black', fontsize=12, ha='center', va='center', zorder=200)

    show_name(ax, polygons_dict)

def show_lines(ax, lines_dict):
    for name, line in lines_dict.items():
        line = np.array(line)
        if line.ndim != 2 or line.shape[0] < 2:
            continue
        ax.plot(*line.T, lw=1, color='black')
        # # Hiển thị tên line ở giữa đường
        # mid_idx = len(line) // 2
        # if len(line) % 2 == 0:
        #     mid_point = (line[mid_idx - 1] + line[mid_idx]) / 2
        # else:
        #     mid_point = line[mid_idx]
        # ax.text(mid_point[0], mid_point[1], name, color='blue', fontsize=7, ha='center', va='center', zorder=50)

def show_points(ax, point_coords):
    for name, (x, y) in point_coords.items():
        ax.plot(x, y, 'o', color='red', markersize=3, zorder=20)



def animate_square_from_block(ax, start_block, lines, line_next, ui, interval=20, speed=2):
    import matplotlib.patches as patches
    import matplotlib.animation as animation

    if not hasattr(ax, 'existing_squares'):
        ax.existing_squares = {}


    # Đưa tất cả các ô vuông cũ về cuối đường trước khi xóa hoặc tạo mới
    for sq in ax.existing_squares.values():
        path = sq['path']
        seg_lens = np.linalg.norm(np.diff(path, axis=0), axis=1)
        total_len = np.sum(seg_lens)
        sq['distance_travelled'] = total_len
        pos = path[-1]
        sq['patch'].set_xy((pos[0] - sq['patch'].get_width()/2, pos[1] - sq['patch'].get_height()/2))
        sq['text'].set_position((pos[0], pos[1]))

    move_squares = []

    bit_tuple = bits.get_bits_for_path(start_block, ui)  # tuple chứa các chuỗi bit cho từng path

    # Cập nhật giá trị bit cho các line tiếp theo và cập nhật bits.data
    next_blocks = line_next[start_block]

    for i, next_line in enumerate(next_blocks):
        # Gán giá trị bit cho connection_map
        bit_str = bit_tuple[i]
        if next_line in connection_map:
            for conn in connection_map[next_line]:
                conn['value'] = str(bit_str)

                # Cập nhật bits.data nếu cần
                bits.data[conn['to']] [conn['port']] = conn['value']

    def spawn_square(path, to_key, bit_str):
        key = (start_block, to_key)
        # Nếu start_block là point, xóa các square có đích là point này trước khi spawn mới
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
            sq = ax.existing_squares[key]
            sq['distance_travelled'] = 0.0
            sq['text'].set_text(bit_str)
            # Cập nhật lại kích thước ô vuông cho khít text mới
            renderer = ax.figure.canvas.get_renderer()
            sq['text'].set_text(bit_str)
            bbox = sq['text'].get_window_extent(renderer=renderer)
            inv = ax.transData.inverted()
            bbox_data = bbox.transformed(inv)
            width = bbox_data.width
            height = bbox_data.height
            sq['patch'].set_width(width)
            sq['patch'].set_height(height)
            move_squares.append(sq)
        else:
            temp_text = ax.text(0, 0, bit_str, color='white', ha='center', va='center', fontsize=10, zorder=11)
            renderer = ax.figure.canvas.get_renderer()
            bbox = temp_text.get_window_extent(renderer=renderer)
            inv = ax.transData.inverted()
            bbox_data = bbox.transformed(inv)
            width = bbox_data.width
            height = bbox_data.height
            temp_text.remove()

            start_pos = path[0]
            rect = patches.Rectangle(
                (start_pos[0] - width/2, start_pos[1] - height/2), width, height, color='blue', zorder=100
            )
            ax.add_patch(rect)
            text = ax.text(
                start_pos[0], start_pos[1], bit_str, color='white', ha='center', va='center', fontsize=10, zorder=101
            )
            sq = {'patch': rect, 'text': text, 'path': path, 'distance_travelled': 0.0, 'to': to_key}
            ax.existing_squares[key] = sq
            move_squares.append(sq)

    spawned = set()
    next_blocks = [n for n in line_next.get(start_block, []) if n in lines]
    for idx, next_name in enumerate(next_blocks):
        next_path = lines[next_name]
        # Lấy bit_str đúng thứ tự, nếu thiếu thì lấy bit cuối cùng
        if isinstance(bit_tuple, (tuple, list)):
            if idx < len(bit_tuple):
                bit_str = bit_tuple[idx]
            else:
                bit_str = bit_tuple[-1]
        else:
            bit_str = str(bit_tuple)
        spawn_square(next_path, next_name, bit_str)
        spawned.add(next_name)

    def update(frame):
        active_patches = []
        for sq in move_squares:
            path = sq['path']
            distance_travelled = sq['distance_travelled']
            seg_lens = np.linalg.norm(np.diff(path, axis=0), axis=1)
            total_len = np.sum(seg_lens)
            dist = distance_travelled
            remain = dist
            for i, seg_len in enumerate(seg_lens):
                if remain < seg_len:
                    t = remain / seg_len
                    pos = (1-t)*path[i] + t*path[i+1]
                    break
                remain -= seg_len
            else:
                pos = path[-1]

            sq['patch'].set_xy((pos[0] - sq['patch'].get_width()/2, pos[1] - sq['patch'].get_height()/2))
            sq['text'].set_position((pos[0], pos[1]))

            if distance_travelled < total_len:
                sq['distance_travelled'] = min(total_len, distance_travelled + speed)
            active_patches.append(sq['patch'])
            active_patches.append(sq['text'])
        return active_patches

    ani = animation.FuncAnimation(ax.figure, update, interval=30, blit=False, cache_frame_data=False)
    return ani

def logic_step_from_block(start_block, lines, line_next, ui):
    """
    Xử lý logic truyền dữ liệu giữa các block, KHÔNG tạo animation.
    """
    import bits
    bit_tuple = bits.get_bits_for_path(start_block, ui)
    next_blocks = line_next.get(start_block, [])
    for i, next_line in enumerate(next_blocks):
        bit_str = bit_tuple[i] if isinstance(bit_tuple, (tuple, list)) and i < len(bit_tuple) else str(bit_tuple[-1]) if isinstance(bit_tuple, (tuple, list)) else str(bit_tuple)
        if next_line in connection_map:
            for conn in connection_map[next_line]:
                conn['value'] = str(bit_str)
                bits.data[conn['to']][conn['port']] = conn['value']

def clear_animated_squares(ax):
    """Xóa tất cả các khối vuông động (animation square) trên ax."""
    if hasattr(ax, 'existing_squares'):
        for sq in list(ax.existing_squares.values()):
            try:
                sq['patch'].remove()
                sq['text'].remove()
            except Exception:
                pass
        ax.existing_squares.clear()
# --- Dữ liệu polygons và lines giữ nguyên như bạn đã có ở trên ---

# Vẽ tất cả trên cùng một hình
# fig, ax = plt.subplots(figsize=(25, 12))
# show_polygons(ax, polygons)
# show_lines(ax, lines)
# ax.set_aspect('equal')
# ax.autoscale(enable=True)
# ax.invert_yaxis()
# ax.axis('off')
# # Demo: animate a square from the 'PC' block
# ani = animate_square_from_block(ax, 'Control', lines, line_next)
# plt.show()