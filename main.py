import sys
from PyQt5 import QtWidgets, QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import simulate        # module của bạn chứa show_polygons_and_lines, animate_squares_along_paths
from mainwindow_ui import Ui_MainWindow  # file pyuic5 sinh ra
from matplotlib.animation import FuncAnimation
from process import handle_open_file, handle_close_file

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # self.ani = None  # Thêm dòng này để giữ animation

        # Thiết lập UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Tạo figure và canvas
        self.fig, self.ax = simulate.plt.subplots(figsize=(30, 18))
        simulate.show_polygons(self.ax, simulate.polygons)
        simulate.show_lines(self.ax, simulate.lines)        
        self.ax.set_aspect('equal')
        self.ax.autoscale(enable=True)
        self.ax.invert_yaxis()
        self.ax.axis('off')
        self.canvas = FigureCanvas(self.fig)

        # Đặt canvas vào sim_frame
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.ui.sim_frame.setLayout(layout)
        layout.addWidget(self.canvas)

        self.ui.open_bottom.clicked.connect(lambda: handle_open_file(self.ui))
        self.ui.close_bottom.clicked.connect(lambda: handle_close_file(self.ui))
        self.ui.run_all_bottom.clicked.connect(self.simulate_add)  # Thêm dòng này
        self.ui.run_step_bottom.clicked.connect(self.simulate_add_step)  # Kết nối nút step


    def simulate_add(self):
        # Lấy lệnh từ code frame
        code = self.ui.textEdit.toPlainText().strip()
        if not code:
            return

        # Giả sử chỉ xử lý dòng đầu tiên, dạng: ADD Xd, Xn, Xm
        line = code.splitlines()[0]
        parts = line.replace(',', '').split()
        if len(parts) != 4 or parts[0].upper() != "ADD":
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Chỉ hỗ trợ lệnh: ADD Xd, Xn, Xm")
            return

        _, dst, src1, src2 = parts
        # Lấy chỉ số thanh ghi
        dst_idx = int(dst[1:])
        src1_idx = int(src1[1:])
        src2_idx = int(src2[1:])

        # Lấy giá trị hiện tại của các thanh ghi (nếu chưa có thì là 0)
        def get_reg(idx):
            item = self.ui.registerShow.item(idx, 0)
            return int(item.text()) if item and item.text().isdigit() else 0

        val1 = get_reg(src1_idx)
        val2 = get_reg(src2_idx)
        result = val1 + val2

        # Cập nhật kết quả lên thanh ghi đích
        self.ui.registerShow.setItem(dst_idx, 0, QtWidgets.QTableWidgetItem(str(result)))

        # Sau khi xử lý xong, gọi animation (ví dụ animate từ 'Control')
        if self.ani:
            self.ani.event_source.stop()
        self.ani = simulate.animate_square_from_block(
            self.ax, 'Control', simulate.lines, simulate.line_next, square_size=18, interval=20, speed=2
        )
        self.canvas.draw_idle()


    def simulate_add_step(self):
        # Danh sách các block theo thứ tự animation
        order = [
            'PC', 'P1', 'IM', 'P2', 'Control', 'ALUControl', 'P3', 'M1', 'Reg', 'P5',
            'P4', 'SE', 'P6', 'M2', 'ALU', 'P7', 'Mem', 'M3', 'AND1', 'AND2', 'XOR',
            'SL2', 'P8', 'A1', 'A2', 'M4'
        ]

        # Khởi tạo biến đếm bước nếu chưa có
        if not hasattr(self, 'current_step'):
            self.current_step = 0

        block = order[self.current_step]

        # Xóa animation cũ nếu có
        if hasattr(self, 'ani') and self.ani:
            self.ani.event_source.stop()

        # Animate block/line hiện tại
        self.ani = simulate.animate_square_from_block(
            self.ax, block, simulate.lines, simulate.line_next, interval=20, speed=5
        )
        self.canvas.draw_idle()
        self.current_step += 1


    def get_rn_rm_from_code(self):
        """
        Lấy chỉ số Rn, Rm từ dòng đầu tiên của code frame (giả sử dạng: ADD Xd, Xn, Xm)
        Trả về (rn_idx, rm_idx)
        """
        code = self.ui.textEdit.toPlainText().strip()
        if not code:
            return None, None
        line = code.splitlines()[0]
        parts = line.replace(',', '').split()
        if len(parts) != 4 or parts[0].upper() != "ADD":
            return None, None
        # _, dst, rn, rm
        _, _, rn, rm = parts
        try:
            rn_idx = int(rn[1:])
            rm_idx = int(rm[1:])
            return rn_idx, rm_idx
        except Exception:
            return None, None



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()

    w.showMaximized()

    sys.exit(app.exec_())