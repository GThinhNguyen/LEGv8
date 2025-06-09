import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation


# Dữ liệu của bạn
polygons = [
    np.array([[30, 441], [68, 441], [68, 522], [27, 522]]),
    np.array([[110, 467], [216, 467], [216, 629], [108, 629]]),
    np.array([[457, 452], [606, 452], [606, 642], [461, 642]]),
    np.array([[972, 534], [1093, 534], [1093, 710], [968, 710]]),
    np.array([[838, 511], [838, 584], [740, 623], [740, 568], [759, 549], [737, 527], [737, 473]]),
    np.array([[907, 132], [907, 192], [813, 226], [813, 179], [829, 163], [809, 143], [809, 105]]),
    np.array([[265, 63], [265, 115], [207, 140], [207, 104], [221, 90], [204, 73], [204, 34]]),
    np.array([[434, 492], [434, 559], [420, 573], [406, 559], [406, 497], [420, 483]]),
    np.array([[708, 559], [708, 623], [691, 640], [675, 626], [675, 564], [691, 548]]),
    np.array([[1173, 595], [1173, 656], [1152, 677], [1136, 661], [1136, 596], [1152, 580]]),
    np.array([[1122, 82], [1122, 167], [1106, 183], [1092, 169], [1092, 85], [1104, 73]]),
    np.array([[729, 427], [848, 427], [848, 464], [726, 464]]),
    np.array([[539, 688], [562, 688], [589, 737], [562, 787], [537, 787], [509, 739]]),
    np.array([[721, 713], [750, 713], [773, 759], [748, 808], [719, 808], [692, 760]]),
    np.array([[424, 220], [455, 220], [478, 295], [478, 372], [453, 437], [426, 439], [397, 370], [397, 293]]),
    np.array([[1064, 241], [1083, 255], [1064, 274], [1041, 274], [1049, 259], [1041, 236]]),
    np.array([[874, 419], [907, 419], [918, 437], [901, 452], [873, 452]]),
    np.array([[966, 421], [966, 460], [991, 460], [1007, 441], [986, 416]]),
    np.array([[737, 168], [765, 168], [765, 168], [781, 201], [781, 201], [760, 235], [760, 235], [733, 237], [733, 237], [715, 203], [715, 203]])
]


# Thêm các đường mới vào danh sách lines
lines = [
    #From Control
    np.array([[451, 224], [476, 224], [476, 182], [229, 182], [229, 625], [424, 625], [424, 573]]), #L13
    np.array([[463, 244], [1047, 246]]), #L14
    np.array([[472, 267], [865, 267], [865, 429], [882, 429]]), #L15
    np.array([[474, 288], [949, 288], [949, 433], [972, 433]]), #L16
    np.array([[476, 310], [1212, 310], [1212, 752], [1033, 752], [1033, 710]]), #L17
    np.array([[478, 331], [1155, 331], [1155, 582]]), #L18
    np.array([[478, 352], [1033, 352], [1033, 530]]), #L19
    np.array([[476, 371], [792, 371], [792, 428]]), #L20
    np.array([[476, 371], [792, 371], [792, 428]]), #L21
    np.array([[471, 394], [694, 394], [694, 551]]), #L22
    np.array([[465, 415], [635, 415], [635, 846], [733, 846], [733, 808]]), #L22
    np.array([[449, 434], [532, 434], [533, 451]]), #L23
    ########
    np.array([[768, 760], [788, 760], [788, 604]]), #L24
    np.array([[839, 530], [948, 530], [948, 450], [971, 450]]), #L25

    np.array([[907, 438], [930, 438], [930, 260], [1046, 258]]), #L26

    np.array([[1080, 256], [1106, 256], [1106, 179]]), #L27
    np.array([[1002, 441], [1019, 441], [1017, 267], [1041, 267]]),#L28
    
    # from Instruc Memory
    np.array([[219, 549], [242, 549]]), #L29
    np.array([[242, 547], [242, 502]]), #L30
    np.array([[240, 503], [240, 474]]), #L31
    np.array([[240, 474], [240, 329], [394, 329]]), #L32
    np.array([[239, 474], [457, 474]]), #L33
    np.array([[237, 503], [403, 503]]), #L34
    np.array([[242, 543], [242, 587]]), #L35
    np.array([[242, 587], [352, 587]]), #L36
    np.array([[352, 587], [352, 555], [397, 555]]), #L37
    np.array([[352, 583], [453, 583]]), #L38
    np.array([[239, 588], [239, 736], [458, 736]]), #L39
    np.array([[458, 738], [505, 738]]), #L40
    np.array([[457, 741], [457, 833], [646, 833], [646, 758], [692, 758]]),#L53

    #from Registers
    np.array([[604, 503], [737, 503]]), #L41
    np.array([[606, 566], [625, 566]]), #L42
    np.array([[625, 566], [673, 566]]), #L43
    np.array([[624, 568], [624, 685], [968, 685]]), #L44

    #from ALU
    np.array([[839, 568], [945, 568]]),#L45
    np.array([[945, 568], [971, 568]]),#L46
    np.array([[945, 566], [945, 731], [1122, 733], [1122, 656], [1140, 654]]),#L47

    np.array([[789, 490], [789, 466]]), #L48

    #from data memory
    np.array([[1092, 598], [1134, 598]]),#L49

    #from multi
    np.array([[440, 530], [455, 530]]),#L50
    np.array([[710, 593], [733, 593]]),#L51
    np.array([[1167, 624], [1187, 624] , [1185, 854], [434, 856], [434, 624], [459, 624]]),#L52
    np.array([[1123, 126], [1185, 126], [1185, 11], [11, 11], [11, 482], [20, 482]]), #L9

    #from signed-extended
    np.array([[588, 737], [650, 737], [650, 625]]),#L54
    np.array([[652, 625], [674, 625]]),#L55
    np.array([[650, 627], [650, 201], [710, 201]]),#L56

    #from sift left 2
    np.array([[777, 201], [811, 201]]),#L57

#   from PC
    np.array([[68, 482], [83, 482]]),#L58
    np.array([[83, 484], [104, 484]]),#L59
    np.array([[83, 482], [83, 221]]),#L1
    np.array([[80, 221], [340, 221], [340, 127], [809, 122]]),#L5
    np.array([[80, 217], [80, 57], [202, 57]]),#L2

    np.array([[166, 116], [204, 116]]),#L4
    #From Add
    np.array([[269, 85], [1089, 85]]), #L8
    np.array([[905, 162], [1085, 162]])#L9
]


def show_polygons_and_lines(ax, polygons, lines):
    # Vẽ polygons
    for poly in polygons:
        poly = np.array(poly)
        ax.plot(*poly.T, lw=2)
        if not np.allclose(poly[0], poly[-1]):
            ax.plot([poly[-1,0], poly[0,0]], [poly[-1,1], poly[0,1]], lw=2)
    # Vẽ lines
    for line in lines:
        line = np.array(line)
        ax.plot(*line.T, lw=2, color='red')




def animate_squares_along_paths(ax, paths, interval=20, total_frames=300):
    # paths: list of np.array
    squares = []
    all_points = []
    max_points = 0

    # Chuẩn bị các điểm di chuyển cho từng path
    for path in paths:
        path = np.array(path)
        # Tính chiều dài từng đoạn và tổng chiều dài
        segment_lengths = [np.linalg.norm(path[i+1] - path[i]) for i in range(len(path)-1)]
        total_length = sum(segment_lengths)
        # Tính số điểm trên mỗi đoạn dựa trên chiều dài đoạn
        points = []
        for i, seg_len in enumerate(segment_lengths):
            n_points = max(2, int(total_frames * seg_len / total_length))
            x_vals = np.linspace(path[i, 0], path[i+1, 0], n_points, endpoint=False)
            y_vals = np.linspace(path[i, 1], path[i+1, 1], n_points, endpoint=False)
            points.extend(list(zip(x_vals, y_vals)))
        points.append(tuple(path[-1]))  # Thêm điểm cuối cùng
        all_points.append(points)
        max_points = max(max_points, len(points))
        # Tạo ô vuông tại vị trí bắt đầu
        square_size = 15
        square = patches.Rectangle((points[0][0] - square_size/2, points[0][1] - square_size/2),
                                  square_size, square_size, fc='red')
        ax.add_patch(square)
        squares.append(square)

    def update(frame):
        for square, points in zip(squares, all_points):
            idx = min(frame, len(points)-1)
            x, y = points[idx]
            square.set_xy((x - square.get_width()/2, y - square.get_height()/2))
        return squares

    ani = FuncAnimation(ax.figure, update, frames=max_points, interval=interval, blit=True)
    return ani

# --- Dữ liệu polygons và lines giữ nguyên như bạn đã có ở trên ---

# Vẽ tất cả trên cùng một hình
# fig, ax = plt.subplots(figsize=(25, 12))
# show_polygons_and_lines(ax, polygons, lines)
# ax.set_aspect('equal')
# ax.autoscale(enable=True)
# ax.invert_yaxis()
# ax.axis('off')
# Tạo animation

# L13_path = lines[0]
# L14_path = lines[1]
# ani = animate_squares_along_paths(ax, [L13_path, L14_path])
# plt.tight_layout()
# plt.show()