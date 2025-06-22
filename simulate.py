import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
from matplotlib.path import Path
import bits  # Thêm dòng này ở đầu file


polygons = {
    'PC': np.array([[30, 441], [68, 441], [68, 522], [27, 522]]),
    'IM': np.array([[110, 467], [216, 467], [216, 629], [108, 629]]),
    'Reg': np.array([[457, 452], [606, 452], [606, 642], [461, 642]]),
    'Mem': np.array([[972, 534], [1093, 534], [1093, 710], [968, 710]]),
    'ALU': np.array([[838, 511], [838, 584], [740, 623], [740, 568], [759, 549], [737, 527], [737, 473]]),
    'ADD2': np.array([[907, 132], [907, 192], [813, 226], [813, 179], [829, 163], [809, 143], [809, 105]]),
    'ADD1': np.array([[265, 63], [265, 115], [207, 140], [207, 104], [221, 90], [204, 73], [204, 34]]),
    'M1': np.array([[434, 492], [434, 559], [420, 573], [406, 559], [406, 497], [420, 483]]),
    'M2': np.array([[708, 559], [708, 623], [691, 640], [675, 626], [675, 564], [691, 548]]),
    'M3': np.array([[1173, 595], [1173, 656], [1152, 677], [1136, 661], [1136, 596], [1152, 580]]),
    'M4': np.array([[1122, 82], [1122, 167], [1106, 183], [1092, 169], [1092, 85], [1104, 73]]),
    'Flags': np.array([[729, 427], [848, 427], [848, 464], [726, 464]]),
    'SE': np.array([[539, 688], [562, 688], [589, 737], [562, 787], [537, 787], [509, 739]]),
    'ALUControl': np.array([[721, 713], [750, 713], [773, 759], [748, 808], [719, 808], [692, 760]]),
    'Control': np.array([[424, 220], [455, 220], [478, 295], [478, 372], [453, 437], [426, 439], [397, 370], [397, 293]]),
    'XOR': np.array([[1064, 241], [1083, 255], [1064, 274], [1041, 274], [1049, 259], [1041, 236]]),
    'AND1': np.array([[874, 419], [907, 419], [918, 437], [901, 452], [873, 452]]),
    'AND2': np.array([[966, 421], [966, 460], [991, 460], [1007, 441], [986, 416]]),
    'SL2': np.array([[737, 168], [765, 168], [765, 168], [781, 201], [781, 201], [760, 235], [760, 235], [733, 237], [733, 237], [715, 203], [715, 203]])
}

points = {'P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8'}

lines = {
    #From Control
    #Reg2Log
    'L13': np.array([[451, 224], [476, 224], [476, 182], [229, 182], [229, 625], [424, 625], [424, 573]]),
    #UnsecondBranch
    'L14': np.array([[463, 244], [1047, 246]]),
    #FlagBranch
    'L15': np.array([[472, 267], [865, 267], [865, 429], [882, 429]]),
    #ZeroBranch
    'L16': np.array([[474, 288], [949, 288], [949, 433], [972, 433]]),
    #MemRead
    'L17': np.array([[476, 310], [1212, 310], [1212, 752], [1033, 752], [1033, 710]]),
    #MemToReg
    'L18': np.array([[478, 331], [1155, 331], [1155, 582]]),
    #MemWrite
    'L19': np.array([[478, 352], [1033, 352], [1033, 530]]),
    #FlagWrite
    'L20': np.array([[476, 371], [792, 371], [792, 428]]),
    #ALUSrc
    'L21': np.array([[471, 394], [694, 394], [694, 551]]),
    #ALUOp
    'L22': np.array([[465, 415], [635, 415], [635, 846], [733, 846], [733, 808]]),
    #RegWrite
    'L23': np.array([[449, 434], [532, 434], [533, 451]]),
    #ALUControl to ALU
    'L24': np.array([[768, 760], [788, 760], [788, 604]]),

    #from ALU
    'L25': np.array([[839, 530], [948, 530], [948, 450], [971, 450]]),
    'L26': np.array([[907, 438], [930, 438], [930, 260], [1046, 258]]),
    'L27': np.array([[1080, 256], [1106, 256], [1106, 179]]),
    'L28': np.array([[1002, 441], [1019, 441], [1017, 267], [1041, 267]]),

    'L45': np.array([[839, 568], [945, 568]]),#46, 47
    'L46': np.array([[945, 568], [971, 568]]),
    'L47': np.array([[945, 566], [945, 731], [1122, 733], [1122, 656], [1140, 654]]),

    'L48': np.array([[789, 490], [789, 466]]),

    # from Instruc Memory
    'L29': np.array([[219, 549], [242, 549]]),#32, 33, 34, 36, 39
    'L30': np.array([[242, 547], [242, 502]]),
    'L31': np.array([[240, 503], [240, 474]]),
    'L32': np.array([[240, 474], [240, 329], [394, 329]]),
    'L33': np.array([[239, 474], [457, 474]]),
    'L34': np.array([[237, 503], [403, 503]]),
    'L35': np.array([[242, 543], [242, 587]]),
    'L36': np.array([[242, 587], [352, 587]]), #37, 38
    'L37': np.array([[352, 587], [352, 555], [397, 555]]),
    'L38': np.array([[352, 583], [453, 583]]),
    'L39': np.array([[239, 588], [239, 736], [458, 736]]), #40, 53
    'L40': np.array([[458, 738], [505, 738]]),
    'L53': np.array([[457, 741], [457, 833], [646, 833], [646, 758], [692, 758]]),

    #from Registers
    'L41': np.array([[604, 503], [737, 503]]),
    'L42': np.array([[606, 566], [625, 566]]), #43, 44
    'L43': np.array([[625, 566], [673, 566]]),
    'L44': np.array([[624, 568], [624, 685], [968, 685]]),

    #from data memory
    'L49': np.array([[1092, 598], [1134, 598]]),

    #from multi
    'L50': np.array([[440, 530], [455, 530]]),
    'L51': np.array([[710, 593], [733, 593]]),
    'L52': np.array([[1167, 624], [1187, 624] , [1185, 854], [434, 856], [434, 624], [459, 624]]),
    'L9a': np.array([[1123, 126], [1185, 126], [1185, 11], [11, 11], [11, 482], [20, 482]]), # L9 (1)
    
    #from signed-extended
    'L54': np.array([[588, 737], [650, 737], [650, 625]]),#55, 56
    'L55': np.array([[652, 625], [674, 625]]),
    'L56': np.array([[650, 627], [650, 201], [710, 201]]),

    #from sift left 2
    'L57': np.array([[777, 201], [811, 201]]),

    'L60': np.array([[848, 450], [870, 450]]),

    #from PC
    'L58': np.array([[68, 482], [83, 482]]), #1, 59
    'L59': np.array([[83, 484], [104, 484]]),
    'L1': np.array([[83, 482], [83, 221]]), #2, 5
    'L5': np.array([[80, 221], [340, 221], [340, 127], [809, 122]]),
    'L2': np.array([[80, 217], [80, 57], [202, 57]]),

    'L4': np.array([[166, 116], [204, 116]]),
    
    #From Add
    'L8': np.array([[269, 85], [1089, 85]]),
    'L9b': np.array([[905, 162], [1085, 162]])
}

# Định nghĩa các đường nối tiếp dựa trên comment trong dict lines
# Sửa lại: dùng dict Python hợp lệ, key là tên line hoặc block, value là list tên line/block tiếp theo

line_next = {
    # Control outputs
    'Control': ['L14', 'L15', 'L16', 'L17', 'L18', 'L19', 'L20', 'L21', 'L22', 'L23', 'L13'],
    'PC': ['L58'],
    'IM': ['L29'],
    'Reg': ['L41', 'L42'],
    'ALU': ['L25', 'L45', 'L48'],
    'ALUControl': ['L24'],
    'Mem': ['L49'],
    'Flags': ['L60'],
    'ADD1': ['L8'],
    'ADD2': ['L9a', 'L9b'],
    'AND1': ['L26'],
    'AND2': ['L28'],
    'XOR': ['L27'],
    'SL2': ['L57'],
    'M1': ['L50'],
    'M2': ['L51'],
    'M3': ['L52'],
    'M4': ['L8'],


    # Points to lines
    'P1': ['L59', 'L1'],
    'P2': ['L32', 'L33', 'L34', 'L36', 'L39'],
    'P3': ['L37', 'L38'],
    'P4': ['L40', '53'],
    'P5': ['L43', 'L44'],
    'P6': ['L55', 'L56'],
    'P7': ['L46', 'L47'],
    'P8': ['L2', 'L5'],
}

# key là tên block, value là list các dict chứa thông tin đối tượng đích, cổng và giá trị hiện tại
connection_map = {
    'L13': [{'to': 'M1', 'port': 'Inp1', 'value': '0'}],
    'L14': [{'to': 'XOR', 'port': 'Inp0', 'value': '0'}],
    'L15': [{'to': 'AND1', 'port': 'Inp0', 'value': '0'}],
    'L16': [{'to': 'AND2', 'port': 'Inp0', 'value': '0'}],
    'L17': [{'to': 'Mem', 'port': 'ControlRead', 'value': '0'}],
    'L18': [{'to': 'M3', 'port': 'Control', 'value': '0'}],
    'L19': [{'to': 'Mem', 'port': 'ControlWrite', 'value': '0'}],
    'L20': [{'to': 'Flags', 'port': 'Control', 'value': '0'}],
    'L21': [{'to': 'M2', 'port': 'Control', 'value': '0'}],
    'L22': [{'to': 'ALUControl', 'port': 'Control', 'value': '0'}],
    'L23': [{'to': 'Reg', 'port': 'Control', 'value': '0'}],
    'L24': [{'to': 'ALU', 'port': 'Control', 'value': '0'}],
    'L25': [{'to': 'AND2', 'port': 'Inp1', 'value': '0'}],
    'L26': [{'to': 'XOR', 'port': 'Inp1', 'value': '0'}],
    'L27': [{'to': 'M4', 'port': 'Control', 'value': '0'}],
    'L28': [{'to': 'XOR', 'port': 'Inp2', 'value': '0'}],
    'L29': [{'to': 'P2', 'port': 'Inp0', 'value': '0'}],
    'L32': [{'to': 'Control', 'port': 'Inp0', 'value': '0'}],
    'L33': [{'to': 'Reg', 'port': 'ReadRegister1', 'value': '0'}],
    'L34': [{'to': 'M1', 'port': 'Inp0', 'value': '0'}],
    'L36': [{'to': 'P3', 'port': 'Inp0', 'value': '0'}],
    'L37': [{'to': 'M1', 'port': 'Inp1', 'value': '0'}],
    'L38': [{'to': 'Reg', 'port': 'WriteRegister', 'value': '0'}],
    'L39': [{'to': 'P4', 'port': 'Inp0', 'value': '0'}],
    'L40': [{'to': 'SE', 'port': 'Inp0', 'value': '0'}],
    'L41': [{'to': 'ALU', 'port': 'Inp0', 'value': '0'}],
    'L42': [{'to': 'P5', 'port': 'Inp0', 'value': '0'}],
    'L43': [{'to': 'M2', 'port': 'Inp0', 'value': '0'}],
    'L44': [{'to': 'Mem', 'port': 'WriteData', 'value': '0'}],
    'L45': [{'to': 'P7', 'port': 'Inp0', 'value': '0'}],
    'L46': [{'to': 'Mem', 'port': 'Address', 'value': '0'}],
    'L47': [{'to': 'M3', 'port': 'Inp0', 'value': '0'}],
    'L48': [{'to': 'Flags', 'port': 'Inp0', 'value': '0'}],
    'L49': [{'to': 'M3', 'port': 'Inp1', 'value': '0'}],
    'L50': [{'to': 'Reg', 'port': 'ReadRegister2', 'value': '0'}],
    'L51': [{'to': 'ALU', 'port': 'Inp1', 'value': '0'}],
    'L52': [{'to': 'Reg', 'port': 'WriteData', 'value': '0'}],
    'L53': [{'to': 'ALUControl', 'port': 'Inp0', 'value': '0'}],
    'L54': [{'to': 'P6', 'port': 'Inp0', 'value': '0'}],
    'L55': [{'to': 'M2', 'port': 'Inp1', 'value': '0'}],
    'L56': [{'to': 'SL2', 'port': 'Inp0', 'value': '0'}],
    'L57': [{'to': 'ADD2', 'port': 'Inp1', 'value': '0'}],
    'L58': [{'to': 'P1', 'port': 'Inp0', 'value': '0'}],
    'L59': [{'to': 'IM', 'port': 'ReadAddress', 'value': '0'}],
    'L60': [{'to': 'ADD1', 'port': 'Inp1', 'value': '0'}],
    'L1':  [{'to': 'P8', 'port': 'Inp0', 'value': '0'}],
    'L2':  [{'to': 'ADD1', 'port': 'Inp0', 'value': '0'}],
    'L4':  [{'to': 'ADD1', 'port': 'Inp1', 'value': '0'}],
    'L5':  [{'to': 'ADD2', 'port': 'Inp0', 'value': '0'}],
    'L8':  [{'to': 'M4', 'port': 'Inp0', 'value': '0'}],
    'L9a': [{'to': 'PC', 'port': 'Inp0', 'value': '0'}],
    'L9b': [{'to': 'M4', 'port': 'Inp1', 'value': '0'}],
}



def show_polygons(ax, polygons_dict):
    for poly in polygons_dict.values():
        poly = np.array(poly)
        if poly.ndim != 2 or poly.shape[0] < 2:
            continue  # Skip empty or invalid polygons
        ax.plot(*poly.T, lw=2)
        if not np.allclose(poly[0], poly[-1]):
            ax.plot([poly[-1,0], poly[0,0]], [poly[-1,1], poly[0,1]], lw=2)

def show_lines(ax, lines_dict):
    for line in lines_dict.values():
        line = np.array(line)
        if line.ndim != 2 or line.shape[0] < 2:
            continue
        ax.plot(*line.T, lw=2, color='red')

def animate_square_from_block(ax, start_block, lines, line_next, ui, interval=20, speed=2):
    import matplotlib.patches as patches
    import matplotlib.animation as animation

    if not hasattr(ax, 'existing_squares'):
        ax.existing_squares = {}

    squares = []
    bit_tuple = bits.get_bits_for_path(start_block, ui)  # tuple chứa các chuỗi bit cho từng path

    def spawn_square(path, to_key, bit_str):
        key = (start_block, to_key)
        if key in ax.existing_squares:
            sq = ax.existing_squares[key]
            sq['distance_travelled'] = 0.0
            sq['text'].set_text(bit_str)
            squares.append(sq)
        else:
            temp_text = ax.text(0, 0, bit_str, color='white', ha='center', va='center', fontsize=10, zorder=11)
            renderer = ax.figure.canvas.get_renderer()
            bbox = temp_text.get_window_extent(renderer=renderer)
            inv = ax.transData.inverted()
            bbox_data = bbox.transformed(inv)
            width = bbox_data.width
            height = bbox_data.height
            temp_text.remove()

            rect = patches.Rectangle((0, 0), width, height, color='blue', zorder=10)
            ax.add_patch(rect)
            text = ax.text(width/2, height/2, bit_str, color='white', ha='center', va='center', fontsize=10, zorder=11)
            sq = {'patch': rect, 'text': text, 'path': path, 'distance_travelled': 0.0, 'to': to_key}
            ax.existing_squares[key] = sq
            squares.append(sq)

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
        for sq in squares:
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

    ani = animation.FuncAnimation(ax.figure, update, interval=interval, blit=False, cache_frame_data=False)
    return ani

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